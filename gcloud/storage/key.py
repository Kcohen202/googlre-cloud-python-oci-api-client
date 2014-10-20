"""Create / interact with gcloud storage keys."""

import mimetypes
import os
from StringIO import StringIO

from gcloud.storage.acl import ObjectACL
from gcloud.storage.iterator import Iterator
from gcloud.storage.iterator import KeyDataIterator


class Key(object):
    """A wrapper around Cloud Storage's concept of an ``Object``."""

    CHUNK_SIZE = 1024 * 1024  # 1 MB.
    """The size of a chunk of data whenever iterating (1 MB).

    This must be a multiple of 256 KB per the API specification.
    """

    def __init__(self, bucket=None, name=None, metadata=None):
        """Key constructor.

        :type bucket: :class:`gcloud.storage.bucket.Bucket`
        :param bucket: The bucket to which this key belongs.

        :type name: string
        :param name: The name of the key.
                     This corresponds to the unique path of the object
                     in the bucket.

        :type metadata: dict
        :param metadata: All the other data provided by Cloud Storage.
        """

        self.bucket = bucket
        self.name = name
        self.metadata = metadata or {}

        # Lazily get the ACL information.
        self.acl = None

    @classmethod
    def from_dict(cls, key_dict, bucket=None):
        """Instantiate a :class:`Key` from data returned by the JSON API.

        :type key_dict: dict
        :param key_dict: A dictionary of data returned from
                         getting an Cloud Storage object.

        :type bucket: :class:`gcloud.storage.bucket.Bucket`
        :param bucket: The bucket to which this key belongs
                       (and by proxy, which connection to use).

        :rtype: :class:`Key`
        :returns: A key based on the data provided.
        """

        return cls(bucket=bucket, name=key_dict['name'], metadata=key_dict)

    def __repr__(self):
        if self.bucket:
            bucket_name = self.bucket.name
        else:
            bucket_name = None

        return '<Key: %s, %s>' % (bucket_name, self.name)

    @property
    def connection(self):
        """Getter property for the connection to use with this Key.

        :rtype: :class:`gcloud.storage.connection.Connection` or None
        :returns: The connection to use, or None if no connection is set.
        """

        if self.bucket and self.bucket.connection:
            return self.bucket.connection

    @property
    def path(self):
        """Getter property for the URL path to this Key.

        :rtype: string
        :returns: The URL path to this Key.
        """

        if not self.bucket:
            raise ValueError('Cannot determine path without a bucket defined.')
        elif not self.name:
            raise ValueError('Cannot determine path without a key name.')

        return self.bucket.path + '/o/' + self.name

    @property
    def public_url(self):
        """
        :rtype: `string`
        :returns: The public URL for this key.
        """
        return '{storage_base_url}/{self.bucket.name}/{self.name}'.format(
            storage_base_url='http://commondatastorage.googleapis.com',
            self=self)

    def generate_signed_url(self, expiration, method='GET'):
        """Generates a signed URL for this key.

        If you have a key that you want to allow access to
        for a set amount of time,
        you can use this method to generate a URL
        that is only valid within a certain time period.

        This is particularly useful if you don't want publicly accessible keys,
        but don't want to require users to explicitly log in.

        :type expiration: int, long, datetime.datetime, datetime.timedelta
        :param expiration: When the signed URL should expire.

        :type method: string
        :param method: The HTTP verb that will be used when requesting the URL.

        :rtype: string
        :returns: A signed URL you can use to access the resource
                  until expiration.
        """

        resource = '/{self.bucket.name}/{self.name}'.format(self=self)
        return self.connection.generate_signed_url(resource=resource,
                                                   expiration=expiration,
                                                   method=method)

    def exists(self):
        """Determines whether or not this key exists.

        :rtype: bool
        :returns: True if the key exists in Cloud Storage.
        """

        return self.bucket.get_key(self.name) is not None

    def rename(self, new_name):
        """Renames this key using copy and delete operations.

        Effectively, copies key to the same bucket with a new name, then
        deletes the key.

        .. warning::
          This method will first duplicate the data
          and then delete the old key.
          This means that with very large objects
          renaming could be a very (temporarily) costly
          or a very slow operation.

        :type new_name: string
        :param new_name: The new name for this key.

        :rtype: :class:`Key`
        :returns: The newly-copied key.
        """
        new_key = self.bucket.copy_key(self, self.bucket, new_name)
        self.bucket.delete_key(self)
        return new_key

    def delete(self):
        """Deletes a key from Cloud Storage.

        :rtype: :class:`Key`
        :returns: The key that was just deleted.
        """

        return self.bucket.delete_key(self)

    def get_contents_to_file(self, file_obj):
        """Gets the contents of this key to a file-like object.

        :type file_obj: file
        :param file_obj: A file handle to which to write the key's data.

        :raises: :class:`gcloud.storage.exceptions.NotFoundError`
        """

        for chunk in KeyDataIterator(self):
            file_obj.write(chunk)

    def get_contents_to_filename(self, filename):
        """Get the contents of this key to a file by name.

        :type filename: string
        :param filename: A filename to be passed to ``open``.

        :raises: :class:`gcloud.storage.exceptions.NotFoundError`
        """

        with open(filename, 'wb') as file_obj:
            self.get_contents_to_file(file_obj)

    def get_contents_as_string(self):
        """Gets the data stored on this Key as a string.

        :rtype: string
        :returns: The data stored in this key.
        :raises: :class:`gcloud.storage.exceptions.NotFoundError`
        """

        string_buffer = StringIO()
        self.get_contents_to_file(string_buffer)
        return string_buffer.getvalue()

    def set_contents_from_file(self, file_obj, rewind=False, size=None,
                               content_type=None):
        """Set the contents of this key to the contents of a file handle.

        :type file_obj: file
        :param file_obj: A file handle open for reading.

        :type rewind: bool
        :param rewind: If True, seek to the beginning of the file handle before
                       writing the file to Cloud Storage.

        :type size: int
        :param size: The number of bytes to read from the file handle.
                     If not provided, we'll try to guess the size using
                     :func:`os.fstat`
        """

        # Rewind the file if desired.
        if rewind:
            file_obj.seek(0, os.SEEK_SET)

        # Get the basic stats about the file.
        total_bytes = size or os.fstat(file_obj.fileno()).st_size
        bytes_uploaded = 0

        # Set up a resumable upload session.
        headers = {
            'X-Upload-Content-Type': content_type or 'application/unknown',
            'X-Upload-Content-Length': total_bytes,
        }

        upload_url = self.connection.build_api_url(
            path=self.bucket.path + '/o',
            query_params={'uploadType': 'resumable', 'name': self.name},
            api_base_url=self.connection.API_BASE_URL + '/upload')

        response, _ = self.connection.make_request(
            method='POST', url=upload_url,
            headers=headers)

        # Get the resumable upload URL.
        upload_url = response['location']

        while bytes_uploaded < total_bytes:
            # Construct the range header.
            data = file_obj.read(self.CHUNK_SIZE)
            chunk_size = len(data)

            start = bytes_uploaded
            end = bytes_uploaded + chunk_size - 1

            headers = {
                'Content-Range': 'bytes %d-%d/%d' % (start, end, total_bytes),
            }

            response, _ = self.connection.make_request(
                content_type='text/plain',
                method='POST', url=upload_url, headers=headers, data=data)

            bytes_uploaded += chunk_size

    def set_contents_from_filename(self, filename):
        """Open a path and set this key's contents to the content of that file.

        :type filename: string
        :param filename: The path to the file.
        """

        content_type, _ = mimetypes.guess_type(filename)

        with open(filename, 'rb') as file_obj:
            self.set_contents_from_file(file_obj, content_type=content_type)

    def set_contents_from_string(self, data, content_type='text/plain'):
        """Sets the contents of this key to the provided string.

        You can use this method to quickly set the value of a key::

          >>> from gcloud import storage
          >>> connection = storage.get_connection(project, email, key_path)
          >>> bucket = connection.get_bucket(bucket_name)
          >>> key = bucket.new_key('my_text_file.txt')
          >>> key.set_contents_from_string('This is the contents of my file!')

        Under the hood this is using a string buffer
        and calling :func:`gcloud.storage.key.Key.set_contents_from_file`.

        :type data: string
        :param data: The data to store in this key.

        :rtype: :class:`Key`
        :returns: The updated Key object.
        """

        string_buffer = StringIO()
        string_buffer.write(data)
        self.set_contents_from_file(file_obj=string_buffer, rewind=True,
                                    size=string_buffer.len,
                                    content_type=content_type)
        return self

    def has_metadata(self, field=None):
        """Check if metadata is available locally.

        :type field: string
        :param field: (optional) the particular field to check for.

        :rtype: bool
        :returns: Whether metadata is available locally.
        """

        if not self.metadata:
            return False
        elif field and field not in self.metadata:
            return False
        else:
            return True

    def reload_metadata(self, full=False):
        """Reload metadata from Cloud Storage.

        :type full: bool
        :param full: If True, loads all data (include ACL data).

        :rtype: :class:`Key`
        :returns: The key you just reloaded data for.
        """

        projection = 'full' if full else 'noAcl'
        query_params = {'projection': projection}
        self.metadata = self.connection.api_request(
            method='GET', path=self.path, query_params=query_params)
        return self

    def get_metadata(self, field=None, default=None):
        """Get all metadata or a specific field.

        If you request a field that isn't available,
        and that field can be retrieved by refreshing data
        from Cloud Storage,
        this method will reload the data using
        :func:`Key.reload_metadata`.

        :type field: string
        :param field: (optional) A particular field to retrieve from metadata.

        :type default: anything
        :param default: The value to return if the field provided wasn't found.

        :rtype: dict or anything
        :returns: All metadata or the value of the specific field.
        """

        if not self.has_metadata(field=field):
            full = (field and field == 'acl')
            self.reload_metadata(full=full)

        if field:
            return self.metadata.get(field, default)
        else:
            return self.metadata

    def patch_metadata(self, metadata):
        """Update particular fields of this key's metadata.

        This method will only update the fields provided
        and will not touch the other fields.

        It will also reload the metadata locally
        based on the servers response.

        :type metadata: dict
        :param metadata: The dictionary of values to update.

        :rtype: :class:`Key`
        :returns: The current key.
        """

        self.metadata = self.connection.api_request(
            method='PATCH', path=self.path, data=metadata,
            query_params={'projection': 'full'})
        return self

    def reload_acl(self):
        """Reload the ACL data from Cloud Storage.

        :rtype: :class:`Key`
        :returns: The current key.
        """

        self.acl = ObjectACL(key=self)

        for entry in self.get_metadata('acl', []):
            entity = self.acl.entity_from_dict(entry)
            self.acl.add_entity(entity)

        return self

    def get_acl(self):
        """Get ACL metadata as a :class:`gcloud.storage.acl.ObjectACL` object.

        :rtype: :class:`gcloud.storage.acl.ObjectACL`
        :returns: An ACL object for the current key.
        """

        if not self.acl:
            self.reload_acl()
        return self.acl

    def save_acl(self, acl=None):
        """Save the ACL data for this key.

        :type acl: :class:`gcloud.storage.acl.ACL`
        :param acl: The ACL object to save.
                    If left blank, this will save the ACL
                    set locally on the key.
        """

        # We do things in this weird way because [] and None
        # both evaluate to False, but mean very different things.
        if acl is None:
            acl = self.acl

        if acl is None:
            return self

        self.patch_metadata({'acl': list(acl)})
        self.reload_acl()
        return self

    def clear_acl(self):
        """Remove all ACL rules from the key.

        Note that this won't actually remove *ALL* the rules,
        but it will remove all the non-default rules.
        In short,
        you'll still have access
        to a key that you created
        even after you clear ACL rules
        with this method.
        """

        return self.save_acl(acl=[])

    def make_public(self):
        """Make this key public giving all users read access.

        :rtype: :class:`Key`
        :returns: The current key.
        """

        self.get_acl().all().grant_read()
        self.save_acl()
        return self


class KeyIterator(Iterator):
    """An iterator listing keys.

    You shouldn't have to use this directly,
    but instead should use the helper methods
    on :class:`gcloud.storage.key.Key` objects.

    :type bucket: :class:`gcloud.storage.bucket.Bucket`
    :param bucket: The bucket from which to list keys.
    """

    def __init__(self, bucket):
        self.bucket = bucket
        super(KeyIterator, self).__init__(
            connection=bucket.connection, path=bucket.path + '/o')

    def get_items_from_response(self, response):
        """Factory method, yields :class:`.storage.key.Key` items from response.

        :type response: dict
        :param response: The JSON API response for a page of keys.
        """
        for item in response.get('items', []):
            yield Key.from_dict(item, bucket=self.bucket)
