# Copyright 2014 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Create / interact with gcloud storage keys."""

import copy
import mimetypes
import os
import time
import datetime
from StringIO import StringIO
import urllib

from _gcloud_vendor.apitools.base.py import http_wrapper
from _gcloud_vendor.apitools.base.py import transfer

from gcloud.storage._helpers import _PropertyMixin
from gcloud.storage._helpers import _scalar_property
from gcloud.storage.acl import ObjectACL


class Key(_PropertyMixin):
    """A wrapper around Cloud Storage's concept of an ``Object``."""

    CUSTOM_PROPERTY_ACCESSORS = {
        'acl': 'acl',
        'cacheControl': 'cache_control',
        'contentDisposition': 'content_disposition',
        'contentEncoding': 'content_encoding',
        'contentLanguage': 'content_language',
        'contentType': 'content_type',
        'componentCount': 'component_count',
        'etag': 'etag',
        'generation': 'generation',
        'id': 'id',
        'mediaLink': 'media_link',
        'metageneration': 'metageneration',
        'name': 'name',
        'owner': 'owner',
        'selfLink': 'self_link',
        'size': 'size',
        'storageClass': 'storage_class',
        'timeDeleted': 'time_deleted',
        'updated': 'updated',
    }
    """Map field name -> accessor for fields w/ custom accessors."""

    CHUNK_SIZE = 1024 * 1024  # 1 MB.
    """The size of a chunk of data whenever iterating (1 MB).

    This must be a multiple of 256 KB per the API specification.
    """
    # ACL rules are lazily retrieved.
    _acl = None

    def __init__(self, bucket=None, name=None, properties=None):
        """Key constructor.

        :type bucket: :class:`gcloud.storage.bucket.Bucket`
        :param bucket: The bucket to which this key belongs.

        :type name: string
        :param name: The name of the key.  This corresponds to the
                     unique path of the object in the bucket.

        :type properties: dict
        :param properties: All the other data provided by Cloud Storage.
        """
        super(Key, self).__init__(name=name, properties=properties)
        self.bucket = bucket

    @property
    def acl(self):
        """Create our ACL on demand."""
        if self._acl is None:
            self._acl = ObjectACL(self)
        return self._acl

    @classmethod
    def from_dict(cls, key_dict, bucket=None):
        """Instantiate a :class:`Key` from data returned by the JSON API.

        :type key_dict: dict
        :param key_dict: A dictionary of data returned from getting an
                         Cloud Storage object.

        :type bucket: :class:`gcloud.storage.bucket.Bucket`
        :param bucket: The bucket to which this key belongs (and by
                       proxy, which connection to use).

        :rtype: :class:`Key`
        :returns: A key based on the data provided.
        """

        return cls(bucket=bucket, name=key_dict['name'], properties=key_dict)

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

        return self.bucket.path + '/o/' + urllib.quote(self.name, safe='')

    @property
    def public_url(self):
        """The public URL for this key's object.

        :rtype: `string`
        :returns: The public URL for this key.
        """
        return '{storage_base_url}/{bucket_name}/{quoted_name}'.format(
            storage_base_url='http://commondatastorage.googleapis.com',
            bucket_name=self.bucket.name,
            quoted_name=urllib.quote(self.name, safe=''))

    def generate_signed_url(self, expiration, method='GET'):
        """Generates a signed URL for this key.

        If you have a key that you want to allow access to for a set
        amount of time, you can use this method to generate a URL that
        is only valid within a certain time period.

        This is particularly useful if you don't want publicly
        accessible keys, but don't want to require users to explicitly
        log in.

        :type expiration: int, long, datetime.datetime, datetime.timedelta
        :param expiration: When the signed URL should expire.

        :type method: string
        :param method: The HTTP verb that will be used when requesting the URL.

        :rtype: string
        :returns: A signed URL you can use to access the resource
                  until expiration.
        """
        resource = '/{bucket_name}/{quoted_name}'.format(
            bucket_name=self.bucket.name,
            quoted_name=urllib.quote(self.name, safe=''))
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
          This method will first duplicate the data and then delete the
          old key.  This means that with very large objects renaming
          could be a very (temporarily) costly or a very slow operation.

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
        :raises: :class:`gcloud.storage.exceptions.NotFound`
                 (propagated from
                 :meth:`gcloud.storage.bucket.Bucket.delete_key`).
        """
        return self.bucket.delete_key(self)

    def download_to_file(self, file_obj):
        """Download the contents of this key into a file-like object.

        :type file_obj: file
        :param file_obj: A file handle to which to write the key's data.

        :raises: :class:`gcloud.storage.exceptions.NotFound`
        """

        download_url = self.media_link

        # Use apitools 'Download' facility.
        download = transfer.Download.FromStream(file_obj, auto_transfer=False)
        download.chunksize = self.CHUNK_SIZE
        headers = {'Range': 'bytes=0-%d' % (self.CHUNK_SIZE - 1)}
        request = http_wrapper.Request(download_url, 'GET', headers)

        download.InitializeDownload(request, self.connection.http)

        # Should we be passing callbacks through from caller?  We can't
        # pass them as None, because apitools wants to print to the console
        # by default.
        download.StreamInChunks(callback=lambda *args: None,
                                finish_callback=lambda *args: None)

    # NOTE: Alias for boto-like API.
    get_contents_to_file = download_to_file

    def download_to_filename(self, filename):
        """Download the contents of this key into a named file.

        :type filename: string
        :param filename: A filename to be passed to ``open``.

        :raises: :class:`gcloud.storage.exceptions.NotFound`
        """
        with open(filename, 'wb') as file_obj:
            self.download_to_file(file_obj)

        mtime = time.mktime(datetime.datetime.strptime(
                            self.properties['updated'],
                            '%Y-%m-%dT%H:%M:%S.%fz').timetuple())
        os.utime(file_obj.name, (mtime, mtime))

    # NOTE: Alias for boto-like API.
    get_contents_to_filename = download_to_filename

    def download_as_string(self):
        """Download the contents of this key as a string.

        :rtype: string
        :returns: The data stored in this key.
        :raises: :class:`gcloud.storage.exceptions.NotFound`
        """
        string_buffer = StringIO()
        self.download_to_file(string_buffer)
        return string_buffer.getvalue()

    # NOTE: Alias for boto-like API.
    get_contents_as_string = download_as_string

    def upload_from_file(self, file_obj, rewind=False, size=None,
                         content_type=None, num_retries=6):
        """Upload the contents of this key from a file-like object.

        .. note::
           The effect of uploading to an existing key depends on the
           "versioning" and "lifecycle" policies defined on the key's
           bucket.  In the absence of those policies, upload will
           overwrite any existing contents.

           See the `object versioning
           <https://cloud.google.com/storage/docs/object-versioning>`_ and
           `lifecycle <https://cloud.google.com/storage/docs/lifecycle>`_
           API documents for details.

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
        conn = self.connection
        headers = {
            'Accept': 'application/json',
            'Accept-Encoding': 'gzip, deflate',
            'User-Agent': conn.USER_AGENT,
        }

        upload = transfer.Upload(file_obj,
                                 content_type or 'application/unknown',
                                 total_bytes, auto_transfer=False,
                                 chunksize=self.CHUNK_SIZE)

        url_builder = _UrlBuilder(bucket_name=self.bucket.name,
                                  object_name=self.name)
        upload_config = _UploadConfig()

        # Temporary URL, until we know simple vs. resumable.
        upload_url = conn.build_api_url(
            path=self.bucket.path + '/o', upload=True)

        # Use apitools 'Upload' facility.
        request = http_wrapper.Request(upload_url, 'POST', headers)

        upload.ConfigureRequest(upload_config, request, url_builder)
        query_params = url_builder.query_params
        request.url = conn.build_api_url(path=self.bucket.path + '/o',
                                         query_params=query_params,
                                         upload=True)
        upload.InitializeUpload(request, conn.http)

        # Should we be passing callbacks through from caller?  We can't
        # pass them as None, because apitools wants to print to the console
        # by default.
        if upload.strategy == transfer._RESUMABLE_UPLOAD:
            upload.StreamInChunks(callback=lambda *args: None,
                                  finish_callback=lambda *args: None)
        else:
            http_wrapper.MakeRequest(conn.http, request, retries=num_retries)

    # NOTE: Alias for boto-like API.
    set_contents_from_file = upload_from_file

    def upload_from_filename(self, filename):
        """Upload this key's contents from the content of f named file.

        .. note::
           The effect of uploading to an existing key depends on the
           "versioning" and "lifecycle" policies defined on the key's
           bucket.  In the absence of those policies, upload will
           overwrite any existing contents.

           See the `object versioning
           <https://cloud.google.com/storage/docs/object-versioning>`_ and
           `lifecycle <https://cloud.google.com/storage/docs/lifecycle>`_
           API documents for details.

        :type filename: string
        :param filename: The path to the file.
        """
        content_type, _ = mimetypes.guess_type(filename)

        with open(filename, 'rb') as file_obj:
            self.upload_from_file(file_obj, content_type=content_type)

    # NOTE: Alias for boto-like API.
    set_contents_from_filename = upload_from_filename

    def upload_from_string(self, data, content_type='text/plain'):
        """Upload contents of this key from the provided string.

        .. note::
           The effect of uploading to an existing key depends on the
           "versioning" and "lifecycle" policies defined on the key's
           bucket.  In the absence of those policies, upload will
           overwrite any existing contents.

           See the `object versioning
           <https://cloud.google.com/storage/docs/object-versioning>`_ and
           `lifecycle <https://cloud.google.com/storage/docs/lifecycle>`_
           API documents for details.

        :type data: string
        :param data: The data to store in this key.

        :rtype: :class:`Key`
        :returns: The updated Key object.
        """
        string_buffer = StringIO()
        string_buffer.write(data)
        self.upload_from_file(file_obj=string_buffer, rewind=True,
                              size=string_buffer.len,
                              content_type=content_type)
        return self

    # NOTE: Alias for boto-like API.
    set_contents_from_string = upload_from_string

    def make_public(self):
        """Make this key public giving all users read access.

        :returns: The current object.
        """
        self.acl.all().grant_read()
        self.acl.save()
        return self

    cache_control = _scalar_property('cacheControl')
    """HTTP 'Cache-Control' header for this object.

    See: https://tools.ietf.org/html/rfc7234#section-5.2 and
         https://cloud.google.com/storage/docs/json_api/v1/objects

    :rtype: string
    """

    content_disposition = _scalar_property('contentDisposition')
    """HTTP 'Content-Disposition' header for this object.

    See: https://tools.ietf.org/html/rfc6266 and
            https://cloud.google.com/storage/docs/json_api/v1/objects

    :rtype: string
    """

    content_encoding = _scalar_property('contentEncoding')
    """HTTP 'Content-Encoding' header for this object.

    See: https://tools.ietf.org/html/rfc7231#section-3.1.2.2 and
            https://cloud.google.com/storage/docs/json_api/v1/objects

    :rtype: string
    """

    content_language = _scalar_property('contentLanguage')
    """HTTP 'Content-Language' header for this object.

    See: http://tools.ietf.org/html/bcp47 and
            https://cloud.google.com/storage/docs/json_api/v1/objects

    :rtype: string
    """

    content_type = _scalar_property('contentType')
    """HTTP 'Content-Type' header for this object.

    See: https://tools.ietf.org/html/rfc2616#section-14.17 and
            https://cloud.google.com/storage/docs/json_api/v1/objects

    :rtype: string
    """

    crc32c = _scalar_property('crc32c')
    """CRC32C checksum for this object.

    See: http://tools.ietf.org/html/rfc4960#appendix-B and
            https://cloud.google.com/storage/docs/json_api/v1/objects

    :rtype: string
    """

    @property
    def component_count(self):
        """Number of underlying components that make up this object.

        See: https://cloud.google.com/storage/docs/json_api/v1/objects

        :rtype: integer
        """
        return self.properties['componentCount']

    @property
    def etag(self):
        """Retrieve the ETag for the object.

        See: http://tools.ietf.org/html/rfc2616#section-3.11 and
             https://cloud.google.com/storage/docs/json_api/v1/objects

        :rtype: string
        """
        return self.properties['etag']

    @property
    def generation(self):
        """Retrieve the generation for the object.

        See: https://cloud.google.com/storage/docs/json_api/v1/objects

        :rtype: integer
        """
        return self.properties['generation']

    @property
    def id(self):
        """Retrieve the ID for the object.

        See: https://cloud.google.com/storage/docs/json_api/v1/objects

        :rtype: string
        """
        return self.properties['id']

    md5_hash = _scalar_property('md5Hash')
    """MD5 hash for this object.

    See: http://tools.ietf.org/html/rfc4960#appendix-B and
            https://cloud.google.com/storage/docs/json_api/v1/objects

    :rtype: string
    """

    @property
    def media_link(self):
        """Retrieve the media download URI for the object.

        See: https://cloud.google.com/storage/docs/json_api/v1/objects

        :rtype: string
        """
        return self.properties['mediaLink']

    @property
    def metadata(self):
        """Retrieve arbitrary/application specific metadata for the object.

        See: https://cloud.google.com/storage/docs/json_api/v1/objects

        :rtype: dict
        """
        return copy.deepcopy(self.properties['metadata'])

    @metadata.setter
    def metadata(self, value):
        """Update arbitrary/application specific metadata for the object.

        See: https://cloud.google.com/storage/docs/json_api/v1/objects

        :type value: dict
        """
        self._patch_properties({'metadata': value})

    @property
    def metageneration(self):
        """Retrieve the metageneration for the object.

        See: https://cloud.google.com/storage/docs/json_api/v1/objects

        :rtype: integer
        """
        return self.properties['metageneration']

    @property
    def owner(self):
        """Retrieve info about the owner of the object.

        See: https://cloud.google.com/storage/docs/json_api/v1/objects

        :rtype: dict
        :returns: mapping of owner's role/ID.
        """
        return self.properties['owner'].copy()

    @property
    def self_link(self):
        """Retrieve the URI for the object.

        See: https://cloud.google.com/storage/docs/json_api/v1/objects

        :rtype: string
        """
        return self.properties['selfLink']

    @property
    def size(self):
        """Size of the object,  in bytes.

        See: https://cloud.google.com/storage/docs/json_api/v1/objects

        :rtype: integer
        """
        return self.properties['size']

    @property
    def storage_class(self):
        """Retrieve the storage class for the object.

        See: https://cloud.google.com/storage/docs/json_api/v1/objects and
        https://cloud.google.com/storage/docs/durable-reduced-availability#_DRA_Bucket

        :rtype: string
        :returns: Currently one of "STANDARD", "DURABLE_REDUCED_AVAILABILITY"
        """
        return self.properties['storageClass']

    @property
    def time_deleted(self):
        """Retrieve the timestamp at which the object was deleted.

        See: https://cloud.google.com/storage/docs/json_api/v1/objects

        :rtype: string or None
        :returns: timestamp in RFC 3339 format, or None if the object
                  has a "live" version.
        """
        return self.properties.get('timeDeleted')

    @property
    def updated(self):
        """Retrieve the timestamp at which the object was updated.

        See: https://cloud.google.com/storage/docs/json_api/v1/objects

        :rtype: string
        :returns: timestamp in RFC 3339 format.
        """
        return self.properties['updated']


class _UploadConfig(object):
    """ Faux message FBO apitools' 'ConfigureRequest'.

    Values extracted from apitools
    'samples/storage_sample/storage/storage_v1_client.py'
    """
    accept = ['*/*']
    max_size = None
    resumable_multipart = True
    resumable_path = u'/resumable/upload/storage/v1/b/{bucket}/o'
    simple_multipart = True
    simple_path = u'/upload/storage/v1/b/{bucket}/o'


class _UrlBuilder(object):
    """Faux builder FBO apitools' 'ConfigureRequest'"""
    def __init__(self, bucket_name, object_name):
        self.query_params = {'name': object_name}
        self._bucket_name = bucket_name
        self._relative_path = ''
