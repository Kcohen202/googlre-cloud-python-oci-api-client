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

import unittest2


class Test_Key(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.storage.key import Key
        return Key

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_ctor_defaults(self):
        key = self._makeOne()
        self.assertEqual(key.bucket, None)
        self.assertEqual(key.connection, None)
        self.assertEqual(key.name, None)
        self.assertEqual(key._properties, {})
        self.assertTrue(key._acl is None)

    def test_ctor_explicit(self):
        KEY = 'key'
        connection = _Connection()
        bucket = _Bucket(connection)
        properties = {'key': 'value'}
        key = self._makeOne(bucket, KEY, properties)
        self.assertTrue(key.bucket is bucket)
        self.assertTrue(key.connection is connection)
        self.assertEqual(key.name, KEY)
        self.assertEqual(key.properties, properties)
        self.assertTrue(key._acl is None)

    def test_from_dict_defaults(self):
        KEY = 'key'
        properties = {'key': 'value', 'name': KEY}
        klass = self._getTargetClass()
        key = klass.from_dict(properties)
        self.assertEqual(key.bucket, None)
        self.assertEqual(key.connection, None)
        self.assertEqual(key.name, KEY)
        self.assertEqual(key.properties, properties)
        self.assertTrue(key._acl is None)

    def test_from_dict_explicit(self):
        KEY = 'key'
        connection = _Connection()
        bucket = _Bucket(connection)
        properties = {'key': 'value', 'name': KEY}
        klass = self._getTargetClass()
        key = klass.from_dict(properties, bucket)
        self.assertTrue(key.bucket is bucket)
        self.assertTrue(key.connection is connection)
        self.assertEqual(key.name, KEY)
        self.assertEqual(key.properties, properties)
        self.assertTrue(key._acl is None)

    def test_acl_property(self):
        from gcloud.storage.acl import ObjectACL
        key = self._makeOne()
        acl = key.acl
        self.assertTrue(isinstance(acl, ObjectACL))
        self.assertTrue(acl is key._acl)

    def test_path_no_bucket(self):
        key = self._makeOne()
        self.assertRaises(ValueError, getattr, key, 'path')

    def test_path_no_name(self):
        connection = _Connection()
        bucket = _Bucket(connection)
        key = self._makeOne(bucket)
        self.assertRaises(ValueError, getattr, key, 'path')

    def test_path_normal(self):
        KEY = 'key'
        connection = _Connection()
        bucket = _Bucket(connection)
        key = self._makeOne(bucket, KEY)
        self.assertEqual(key.path, '/b/name/o/%s' % KEY)

    def test_path_w_slash_in_name(self):
        KEY = 'parent/child'
        connection = _Connection()
        bucket = _Bucket(connection)
        key = self._makeOne(bucket, KEY)
        self.assertEqual(key.path, '/b/name/o/parent%2Fchild')

    def test_public_url(self):
        KEY = 'key'
        connection = _Connection()
        bucket = _Bucket(connection)
        key = self._makeOne(bucket, KEY)
        self.assertEqual(key.public_url,
                         'http://commondatastorage.googleapis.com/name/%s' %
                         KEY)

    def test_public_url_w_slash_in_name(self):
        KEY = 'parent/child'
        connection = _Connection()
        bucket = _Bucket(connection)
        key = self._makeOne(bucket, KEY)
        self.assertEqual(
            key.public_url,
            'http://commondatastorage.googleapis.com/name/parent%2Fchild')

    def test_generate_signed_url_w_default_method(self):
        KEY = 'key'
        EXPIRATION = '2014-10-16T20:34:37Z'
        connection = _Connection()
        bucket = _Bucket(connection)
        key = self._makeOne(bucket, KEY)
        self.assertEqual(key.generate_signed_url(EXPIRATION),
                         'http://example.com/abucket/akey?Signature=DEADBEEF'
                         '&Expiration=2014-10-16T20:34:37Z')
        self.assertEqual(connection._signed,
                         [('/name/key', EXPIRATION, {'method': 'GET'})])

    def test_generate_signed_url_w_slash_in_name(self):
        KEY = 'parent/child'
        EXPIRATION = '2014-10-16T20:34:37Z'
        connection = _Connection()
        bucket = _Bucket(connection)
        key = self._makeOne(bucket, KEY)
        self.assertEqual(key.generate_signed_url(EXPIRATION),
                         'http://example.com/abucket/akey?Signature=DEADBEEF'
                         '&Expiration=2014-10-16T20:34:37Z')
        self.assertEqual(connection._signed,
                         [('/name/parent%2Fchild',
                           EXPIRATION, {'method': 'GET'})])

    def test_generate_signed_url_w_explicit_method(self):
        KEY = 'key'
        EXPIRATION = '2014-10-16T20:34:37Z'
        connection = _Connection()
        bucket = _Bucket(connection)
        key = self._makeOne(bucket, KEY)
        self.assertEqual(key.generate_signed_url(EXPIRATION, method='POST'),
                         'http://example.com/abucket/akey?Signature=DEADBEEF'
                         '&Expiration=2014-10-16T20:34:37Z')
        self.assertEqual(connection._signed,
                         [('/name/key', EXPIRATION, {'method': 'POST'})])

    def test_exists_miss(self):
        NONESUCH = 'nonesuch'
        connection = _Connection()
        bucket = _Bucket(connection)
        key = self._makeOne(bucket, NONESUCH)
        self.assertFalse(key.exists())

    def test_exists_hit(self):
        KEY = 'key'
        connection = _Connection()
        bucket = _Bucket(connection)
        key = self._makeOne(bucket, KEY)
        bucket._keys[KEY] = 1
        self.assertTrue(key.exists())

    def test_rename(self):
        KEY = 'key'
        NEW_NAME = 'new-name'
        connection = _Connection()
        bucket = _Bucket(connection)
        key = self._makeOne(bucket, KEY)
        bucket._keys[KEY] = 1
        new_key = key.rename(NEW_NAME)
        self.assertEqual(key.name, KEY)
        self.assertEqual(new_key.name, NEW_NAME)
        self.assertFalse(KEY in bucket._keys)
        self.assertTrue(KEY in bucket._deleted)
        self.assertTrue(NEW_NAME in bucket._keys)

    def test_delete(self):
        KEY = 'key'
        connection = _Connection()
        bucket = _Bucket(connection)
        key = self._makeOne(bucket, KEY)
        bucket._keys[KEY] = 1
        key.delete()
        self.assertFalse(key.exists())

    def test_download_to_file(self):
        import httplib
        from StringIO import StringIO
        KEY = 'key'
        chunk1_response = {'status': httplib.PARTIAL_CONTENT,
                           'content-range': 'bytes 0-2/6'}
        chunk2_response = {'status': httplib.OK,
                           'content-range': 'bytes 3-5/6'}
        connection = _Connection(
            (chunk1_response, 'abc'),
            (chunk2_response, 'def'),
        )
        bucket = _Bucket(connection)
        MEDIA_LINK = 'http://example.com/media/'
        properties = {'mediaLink': MEDIA_LINK}
        key = self._makeOne(bucket, KEY, properties)
        key.CHUNK_SIZE = 3
        fh = StringIO()
        key.download_to_file(fh)
        self.assertEqual(fh.getvalue(), 'abcdef')

    def test_download_to_filename(self):
        import httplib
        import os
        import time
        import datetime
        from tempfile import NamedTemporaryFile
        KEY = 'key'
        chunk1_response = {'status': httplib.PARTIAL_CONTENT,
                           'content-range': 'bytes 0-2/6'}
        chunk2_response = {'status': httplib.OK,
                           'content-range': 'bytes 3-5/6'}
        connection = _Connection(
            (chunk1_response, 'abc'),
            (chunk2_response, 'def'),
        )
        bucket = _Bucket(connection)
        MEDIA_LINK = 'http://example.com/media/'
        properties = {'mediaLink': MEDIA_LINK,
                      'updated': '2014-12-06T13:13:50.690Z'}
        key = self._makeOne(bucket, KEY, properties)
        key.CHUNK_SIZE = 3
        with NamedTemporaryFile() as f:
            key.download_to_filename(f.name)
            f.flush()
            with open(f.name) as g:
                wrote = g.read()
                mtime = os.path.getmtime(f.name)
                updatedTime = time.mktime(datetime.datetime.strptime(
                                          key.properties['updated'],
                                          '%Y-%m-%dT%H:%M:%S.%fz')
                                          .timetuple())
        self.assertEqual(wrote, 'abcdef')
        self.assertEqual(mtime, updatedTime)

    def test_download_as_string(self):
        import httplib
        KEY = 'key'
        chunk1_response = {'status': httplib.PARTIAL_CONTENT,
                           'content-range': 'bytes 0-2/6'}
        chunk2_response = {'status': httplib.OK,
                           'content-range': 'bytes 3-5/6'}
        connection = _Connection(
            (chunk1_response, 'abc'),
            (chunk2_response, 'def'),
        )
        bucket = _Bucket(connection)
        MEDIA_LINK = 'http://example.com/media/'
        properties = {'mediaLink': MEDIA_LINK}
        key = self._makeOne(bucket, KEY, properties)
        key.CHUNK_SIZE = 3
        fetched = key.download_as_string()
        self.assertEqual(fetched, 'abcdef')

    def test_upload_from_file_simple(self):
        import httplib
        from tempfile import NamedTemporaryFile
        from urlparse import parse_qsl
        from urlparse import urlsplit
        KEY = 'key'
        DATA = 'ABCDEF'
        response = {'status': httplib.OK}
        connection = _Connection(
            (response, ''),
        )
        bucket = _Bucket(connection)
        key = self._makeOne(bucket, KEY)
        key.CHUNK_SIZE = 5
        with NamedTemporaryFile() as fh:
            fh.write(DATA)
            fh.flush()
            key.upload_from_file(fh, rewind=True)
        rq = connection.http._requested
        self.assertEqual(len(rq), 1)
        self.assertEqual(rq[0]['method'], 'POST')
        uri = rq[0]['uri']
        scheme, netloc, path, qs, _ = urlsplit(uri)
        self.assertEqual(scheme, 'http')
        self.assertEqual(netloc, 'example.com')
        self.assertEqual(path, '/b/name/o')
        self.assertEqual(dict(parse_qsl(qs)),
                         {'uploadType': 'media', 'name': 'key'})
        headers = dict(
            [(x.title(), str(y)) for x, y in rq[0]['headers'].items()])
        self.assertEqual(headers['Content-Length'], '6')
        self.assertEqual(headers['Content-Type'], 'application/unknown')

    def test_upload_from_file_resumable(self):
        import httplib
        from tempfile import NamedTemporaryFile
        from urlparse import parse_qsl
        from urlparse import urlsplit
        from gcloud._testing import _Monkey
        from _gcloud_vendor.apitools.base.py import http_wrapper
        from _gcloud_vendor.apitools.base.py import transfer
        KEY = 'key'
        UPLOAD_URL = 'http://example.com/upload/name/key'
        DATA = 'ABCDEF'
        loc_response = {'status': httplib.OK, 'location': UPLOAD_URL}
        chunk1_response = {'status': http_wrapper.RESUME_INCOMPLETE,
                           'range': 'bytes 0-4'}
        chunk2_response = {'status': httplib.OK}
        connection = _Connection(
            (loc_response, ''),
            (chunk1_response, ''),
            (chunk2_response, ''),
        )
        bucket = _Bucket(connection)
        key = self._makeOne(bucket, KEY)
        key.CHUNK_SIZE = 5
        # Set the threshhold low enough that we force a resumable uploada.
        with _Monkey(transfer, _RESUMABLE_UPLOAD_THRESHOLD=5):
            with NamedTemporaryFile() as fh:
                fh.write(DATA)
                fh.flush()
                key.upload_from_file(fh, rewind=True)
        rq = connection.http._requested
        self.assertEqual(len(rq), 3)
        self.assertEqual(rq[0]['method'], 'POST')
        uri = rq[0]['uri']
        scheme, netloc, path, qs, _ = urlsplit(uri)
        self.assertEqual(scheme, 'http')
        self.assertEqual(netloc, 'example.com')
        self.assertEqual(path, '/b/name/o')
        self.assertEqual(dict(parse_qsl(qs)),
                         {'uploadType': 'resumable', 'name': 'key'})
        headers = dict(
            [(x.title(), str(y)) for x, y in rq[0]['headers'].items()])
        self.assertEqual(headers['X-Upload-Content-Length'], '6')
        self.assertEqual(headers['X-Upload-Content-Type'],
                         'application/unknown')
        self.assertEqual(rq[1]['method'], 'PUT')
        self.assertEqual(rq[1]['uri'], UPLOAD_URL)
        headers = dict(
            [(x.title(), str(y)) for x, y in rq[1]['headers'].items()])
        self.assertEqual(rq[1]['body'], DATA[:5])
        headers = dict(
            [(x.title(), str(y)) for x, y in rq[1]['headers'].items()])
        self.assertEqual(headers['Content-Range'], 'bytes 0-4/6')
        self.assertEqual(rq[2]['method'], 'PUT')
        self.assertEqual(rq[2]['uri'], UPLOAD_URL)
        self.assertEqual(rq[2]['body'], DATA[5:])
        headers = dict(
            [(x.title(), str(y)) for x, y in rq[2]['headers'].items()])
        self.assertEqual(headers['Content-Range'], 'bytes 5-5/6')

    def test_upload_from_file_w_slash_in_name(self):
        import httplib
        from tempfile import NamedTemporaryFile
        from urlparse import parse_qsl
        from urlparse import urlsplit
        from _gcloud_vendor.apitools.base.py import http_wrapper
        KEY = 'parent/child'
        UPLOAD_URL = 'http://example.com/upload/name/parent%2Fchild'
        DATA = 'ABCDEF'
        loc_response = {'status': httplib.OK, 'location': UPLOAD_URL}
        chunk1_response = {'status': http_wrapper.RESUME_INCOMPLETE,
                           'range': 'bytes 0-4'}
        chunk2_response = {'status': httplib.OK}
        connection = _Connection(
            (loc_response, ''),
            (chunk1_response, ''),
            (chunk2_response, ''),
        )
        bucket = _Bucket(connection)
        key = self._makeOne(bucket, KEY)
        key.CHUNK_SIZE = 5
        with NamedTemporaryFile() as fh:
            fh.write(DATA)
            fh.flush()
            key.upload_from_file(fh, rewind=True)
        rq = connection.http._requested
        self.assertEqual(len(rq), 1)
        self.assertEqual(rq[0]['method'], 'POST')
        uri = rq[0]['uri']
        scheme, netloc, path, qs, _ = urlsplit(uri)
        self.assertEqual(scheme, 'http')
        self.assertEqual(netloc, 'example.com')
        self.assertEqual(path, '/b/name/o')
        self.assertEqual(dict(parse_qsl(qs)),
                         {'uploadType': 'media', 'name': 'parent/child'})
        headers = dict(
            [(x.title(), str(y)) for x, y in rq[0]['headers'].items()])
        self.assertEqual(headers['Content-Length'], '6')
        self.assertEqual(headers['Content-Type'], 'application/unknown')

    def test_upload_from_filename(self):
        import httplib
        from tempfile import NamedTemporaryFile
        from urlparse import parse_qsl
        from urlparse import urlsplit
        from _gcloud_vendor.apitools.base.py import http_wrapper
        KEY = 'key'
        UPLOAD_URL = 'http://example.com/upload/name/key'
        DATA = 'ABCDEF'
        loc_response = {'status': httplib.OK, 'location': UPLOAD_URL}
        chunk1_response = {'status': http_wrapper.RESUME_INCOMPLETE,
                           'range': 'bytes 0-4'}
        chunk2_response = {'status': httplib.OK}
        connection = _Connection(
            (loc_response, ''),
            (chunk1_response, ''),
            (chunk2_response, ''),
        )
        bucket = _Bucket(connection)
        key = self._makeOne(bucket, KEY)
        key.CHUNK_SIZE = 5
        with NamedTemporaryFile(suffix='.jpeg') as fh:
            fh.write(DATA)
            fh.flush()
            key.upload_from_filename(fh.name)
        rq = connection.http._requested
        self.assertEqual(len(rq), 1)
        self.assertEqual(rq[0]['method'], 'POST')
        uri = rq[0]['uri']
        scheme, netloc, path, qs, _ = urlsplit(uri)
        self.assertEqual(scheme, 'http')
        self.assertEqual(netloc, 'example.com')
        self.assertEqual(path, '/b/name/o')
        self.assertEqual(dict(parse_qsl(qs)),
                         {'uploadType': 'media', 'name': 'key'})
        headers = dict(
            [(x.title(), str(y)) for x, y in rq[0]['headers'].items()])
        self.assertEqual(headers['Content-Length'], '6')
        self.assertEqual(headers['Content-Type'], 'image/jpeg')

    def test_upload_from_string(self):
        import httplib
        from urlparse import parse_qsl
        from urlparse import urlsplit
        from _gcloud_vendor.apitools.base.py import http_wrapper
        KEY = 'key'
        UPLOAD_URL = 'http://example.com/upload/name/key'
        DATA = 'ABCDEF'
        loc_response = {'status': httplib.OK, 'location': UPLOAD_URL}
        chunk1_response = {'status': http_wrapper.RESUME_INCOMPLETE,
                           'range': 'bytes 0-4'}
        chunk2_response = {'status': httplib.OK}
        connection = _Connection(
            (loc_response, ''),
            (chunk1_response, ''),
            (chunk2_response, ''),
        )
        bucket = _Bucket(connection)
        key = self._makeOne(bucket, KEY)
        key.CHUNK_SIZE = 5
        key.upload_from_string(DATA)
        rq = connection.http._requested
        self.assertEqual(len(rq), 1)
        self.assertEqual(rq[0]['method'], 'POST')
        uri = rq[0]['uri']
        scheme, netloc, path, qs, _ = urlsplit(uri)
        self.assertEqual(scheme, 'http')
        self.assertEqual(netloc, 'example.com')
        self.assertEqual(path, '/b/name/o')
        self.assertEqual(dict(parse_qsl(qs)),
                         {'uploadType': 'media', 'name': 'key'})
        headers = dict(
            [(x.title(), str(y)) for x, y in rq[0]['headers'].items()])
        self.assertEqual(headers['Content-Length'], '6')
        self.assertEqual(headers['Content-Type'], 'text/plain')

    def test_make_public(self):
        from gcloud.storage.acl import _ACLEntity
        KEY = 'key'
        permissive = [{'entity': 'allUsers', 'role': _ACLEntity.READER_ROLE}]
        after = {'acl': permissive}
        connection = _Connection(after)
        bucket = _Bucket(connection)
        key = self._makeOne(bucket, KEY)
        key.acl.loaded = True
        key.make_public()
        self.assertEqual(list(key.acl), permissive)
        kw = connection._requested
        self.assertEqual(len(kw), 1)
        self.assertEqual(kw[0]['method'], 'PATCH')
        self.assertEqual(kw[0]['path'], '/b/name/o/%s' % KEY)
        self.assertEqual(kw[0]['data'], {'acl': permissive})
        self.assertEqual(kw[0]['query_params'], {'projection': 'full'})

    def test_cache_control_getter(self):
        KEY = 'key'
        connection = _Connection()
        bucket = _Bucket(connection)
        CACHE_CONTROL = 'no-cache'
        properties = {'cacheControl': CACHE_CONTROL}
        key = self._makeOne(bucket, KEY, properties)
        self.assertEqual(key.cache_control, CACHE_CONTROL)

    def test_cache_control_setter(self):
        KEY = 'key'
        CACHE_CONTROL = 'no-cache'
        after = {'cacheControl': CACHE_CONTROL}
        connection = _Connection(after)
        bucket = _Bucket(connection)
        key = self._makeOne(bucket, KEY)
        key.cache_control = CACHE_CONTROL
        self.assertEqual(key.cache_control, CACHE_CONTROL)
        kw = connection._requested
        self.assertEqual(len(kw), 1)
        self.assertEqual(kw[0]['method'], 'PATCH')
        self.assertEqual(kw[0]['path'], '/b/name/o/%s' % KEY)
        self.assertEqual(kw[0]['data'], {'cacheControl': CACHE_CONTROL})
        self.assertEqual(kw[0]['query_params'], {'projection': 'full'})

    def test_component_count(self):
        KEY = 'key'
        connection = _Connection()
        bucket = _Bucket(connection)
        COMPONENT_COUNT = 42
        properties = {'componentCount': COMPONENT_COUNT}
        key = self._makeOne(bucket, KEY, properties)
        self.assertEqual(key.component_count, COMPONENT_COUNT)

    def test_content_disposition_getter(self):
        KEY = 'key'
        connection = _Connection()
        bucket = _Bucket(connection)
        CONTENT_DISPOSITION = 'Attachment; filename=example.jpg'
        properties = {'contentDisposition': CONTENT_DISPOSITION}
        key = self._makeOne(bucket, KEY, properties)
        self.assertEqual(key.content_disposition, CONTENT_DISPOSITION)

    def test_content_disposition_setter(self):
        KEY = 'key'
        CONTENT_DISPOSITION = 'Attachment; filename=example.jpg'
        after = {'contentDisposition': CONTENT_DISPOSITION}
        connection = _Connection(after)
        bucket = _Bucket(connection)
        key = self._makeOne(bucket, KEY)
        key.content_disposition = CONTENT_DISPOSITION
        self.assertEqual(key.content_disposition, CONTENT_DISPOSITION)
        kw = connection._requested
        self.assertEqual(len(kw), 1)
        self.assertEqual(kw[0]['method'], 'PATCH')
        self.assertEqual(kw[0]['path'], '/b/name/o/%s' % KEY)
        self.assertEqual(kw[0]['data'],
                         {'contentDisposition': CONTENT_DISPOSITION})
        self.assertEqual(kw[0]['query_params'], {'projection': 'full'})

    def test_content_encoding_getter(self):
        KEY = 'key'
        connection = _Connection()
        bucket = _Bucket(connection)
        CONTENT_ENCODING = 'gzip'
        properties = {'contentEncoding': CONTENT_ENCODING}
        key = self._makeOne(bucket, KEY, properties)
        self.assertEqual(key.content_encoding, CONTENT_ENCODING)

    def test_content_encoding_setter(self):
        KEY = 'key'
        CONTENT_ENCODING = 'gzip'
        after = {'contentEncoding': CONTENT_ENCODING}
        connection = _Connection(after)
        bucket = _Bucket(connection)
        key = self._makeOne(bucket, KEY)
        key.content_encoding = CONTENT_ENCODING
        self.assertEqual(key.content_encoding, CONTENT_ENCODING)
        kw = connection._requested
        self.assertEqual(len(kw), 1)
        self.assertEqual(kw[0]['method'], 'PATCH')
        self.assertEqual(kw[0]['path'], '/b/name/o/%s' % KEY)
        self.assertEqual(kw[0]['data'],
                         {'contentEncoding': CONTENT_ENCODING})
        self.assertEqual(kw[0]['query_params'], {'projection': 'full'})

    def test_content_language_getter(self):
        KEY = 'key'
        connection = _Connection()
        bucket = _Bucket(connection)
        CONTENT_LANGUAGE = 'pt-BR'
        properties = {'contentLanguage': CONTENT_LANGUAGE}
        key = self._makeOne(bucket, KEY, properties)
        self.assertEqual(key.content_language, CONTENT_LANGUAGE)

    def test_content_language_setter(self):
        KEY = 'key'
        CONTENT_LANGUAGE = 'pt-BR'
        after = {'contentLanguage': CONTENT_LANGUAGE}
        connection = _Connection(after)
        bucket = _Bucket(connection)
        key = self._makeOne(bucket, KEY)
        key.content_language = CONTENT_LANGUAGE
        self.assertEqual(key.content_language, CONTENT_LANGUAGE)
        kw = connection._requested
        self.assertEqual(len(kw), 1)
        self.assertEqual(kw[0]['method'], 'PATCH')
        self.assertEqual(kw[0]['path'], '/b/name/o/%s' % KEY)
        self.assertEqual(kw[0]['data'],
                         {'contentLanguage': CONTENT_LANGUAGE})
        self.assertEqual(kw[0]['query_params'], {'projection': 'full'})

    def test_content_type_getter(self):
        KEY = 'key'
        connection = _Connection()
        bucket = _Bucket(connection)
        CONTENT_TYPE = 'image/jpeg'
        properties = {'contentType': CONTENT_TYPE}
        key = self._makeOne(bucket, KEY, properties)
        self.assertEqual(key.content_type, CONTENT_TYPE)

    def test_content_type_setter(self):
        KEY = 'key'
        CONTENT_TYPE = 'image/jpeg'
        after = {'contentType': CONTENT_TYPE}
        connection = _Connection(after)
        bucket = _Bucket(connection)
        key = self._makeOne(bucket, KEY)
        key.content_type = CONTENT_TYPE
        self.assertEqual(key.content_type, CONTENT_TYPE)
        kw = connection._requested
        self.assertEqual(len(kw), 1)
        self.assertEqual(kw[0]['method'], 'PATCH')
        self.assertEqual(kw[0]['path'], '/b/name/o/%s' % KEY)
        self.assertEqual(kw[0]['data'],
                         {'contentType': CONTENT_TYPE})
        self.assertEqual(kw[0]['query_params'], {'projection': 'full'})

    def test_crc32c_getter(self):
        KEY = 'key'
        connection = _Connection()
        bucket = _Bucket(connection)
        CRC32C = 'DEADBEEF'
        properties = {'crc32c': CRC32C}
        key = self._makeOne(bucket, KEY, properties)
        self.assertEqual(key.crc32c, CRC32C)

    def test_crc32c_setter(self):
        KEY = 'key'
        CRC32C = 'DEADBEEF'
        after = {'crc32c': CRC32C}
        connection = _Connection(after)
        bucket = _Bucket(connection)
        key = self._makeOne(bucket, KEY)
        key.crc32c = CRC32C
        self.assertEqual(key.crc32c, CRC32C)
        kw = connection._requested
        self.assertEqual(len(kw), 1)
        self.assertEqual(kw[0]['method'], 'PATCH')
        self.assertEqual(kw[0]['path'], '/b/name/o/%s' % KEY)
        self.assertEqual(kw[0]['data'],
                         {'crc32c': CRC32C})
        self.assertEqual(kw[0]['query_params'], {'projection': 'full'})

    def test_etag(self):
        KEY = 'key'
        connection = _Connection()
        bucket = _Bucket(connection)
        ETAG = 'ETAG'
        properties = {'etag': ETAG}
        key = self._makeOne(bucket, KEY, properties)
        self.assertEqual(key.etag, ETAG)

    def test_generation(self):
        KEY = 'key'
        connection = _Connection()
        bucket = _Bucket(connection)
        GENERATION = 42
        properties = {'generation': GENERATION}
        key = self._makeOne(bucket, KEY, properties)
        self.assertEqual(key.generation, GENERATION)

    def test_id(self):
        KEY = 'key'
        connection = _Connection()
        bucket = _Bucket(connection)
        ID = 'ID'
        properties = {'id': ID}
        key = self._makeOne(bucket, KEY, properties)
        self.assertEqual(key.id, ID)

    def test_md5_hash_getter(self):
        KEY = 'key'
        connection = _Connection()
        bucket = _Bucket(connection)
        MD5_HASH = 'DEADBEEF'
        properties = {'md5Hash': MD5_HASH}
        key = self._makeOne(bucket, KEY, properties)
        self.assertEqual(key.md5_hash, MD5_HASH)

    def test_md5_hash_setter(self):
        KEY = 'key'
        MD5_HASH = 'DEADBEEF'
        after = {'md5Hash': MD5_HASH}
        connection = _Connection(after)
        bucket = _Bucket(connection)
        key = self._makeOne(bucket, KEY)
        key.md5_hash = MD5_HASH
        self.assertEqual(key.md5_hash, MD5_HASH)
        kw = connection._requested
        self.assertEqual(len(kw), 1)
        self.assertEqual(kw[0]['method'], 'PATCH')
        self.assertEqual(kw[0]['path'], '/b/name/o/%s' % KEY)
        self.assertEqual(kw[0]['data'],
                         {'md5Hash': MD5_HASH})
        self.assertEqual(kw[0]['query_params'], {'projection': 'full'})

    def test_media_link(self):
        KEY = 'key'
        connection = _Connection()
        bucket = _Bucket(connection)
        MEDIA_LINK = 'http://example.com/media/'
        properties = {'mediaLink': MEDIA_LINK}
        key = self._makeOne(bucket, KEY, properties)
        self.assertEqual(key.media_link, MEDIA_LINK)

    def test_metadata_getter(self):
        KEY = 'key'
        connection = _Connection()
        bucket = _Bucket(connection)
        METADATA = {'foo': 'Foo'}
        properties = {'metadata': METADATA}
        key = self._makeOne(bucket, KEY, properties)
        self.assertEqual(key.metadata, METADATA)

    def test_metadata_setter(self):
        KEY = 'key'
        METADATA = {'foo': 'Foo'}
        after = {'metadata': METADATA}
        connection = _Connection(after)
        bucket = _Bucket(connection)
        key = self._makeOne(bucket, KEY)
        key.metadata = METADATA
        self.assertEqual(key.metadata, METADATA)
        kw = connection._requested
        self.assertEqual(len(kw), 1)
        self.assertEqual(kw[0]['method'], 'PATCH')
        self.assertEqual(kw[0]['path'], '/b/name/o/%s' % KEY)
        self.assertEqual(kw[0]['data'],
                         {'metadata': METADATA})
        self.assertEqual(kw[0]['query_params'], {'projection': 'full'})

    def test_metageneration(self):
        KEY = 'key'
        connection = _Connection()
        bucket = _Bucket(connection)
        METAGENERATION = 42
        properties = {'metageneration': METAGENERATION}
        key = self._makeOne(bucket, KEY, properties)
        self.assertEqual(key.metageneration, METAGENERATION)

    def test_owner(self):
        KEY = 'key'
        connection = _Connection()
        bucket = _Bucket(connection)
        OWNER = {'entity': 'project-owner-12345', 'entityId': '23456'}
        properties = {'owner': OWNER}
        key = self._makeOne(bucket, KEY, properties)
        owner = key.owner
        self.assertEqual(owner['entity'], 'project-owner-12345')
        self.assertEqual(owner['entityId'], '23456')

    def test_self_link(self):
        KEY = 'key'
        connection = _Connection()
        bucket = _Bucket(connection)
        SELF_LINK = 'http://example.com/self/'
        properties = {'selfLink': SELF_LINK}
        key = self._makeOne(bucket, KEY, properties)
        self.assertEqual(key.self_link, SELF_LINK)

    def test_size(self):
        KEY = 'key'
        connection = _Connection()
        bucket = _Bucket(connection)
        SIZE = 42
        properties = {'size': SIZE}
        key = self._makeOne(bucket, KEY, properties)
        self.assertEqual(key.size, SIZE)

    def test_storage_class(self):
        KEY = 'key'
        connection = _Connection()
        bucket = _Bucket(connection)
        STORAGE_CLASS = 'http://example.com/self/'
        properties = {'storageClass': STORAGE_CLASS}
        key = self._makeOne(bucket, KEY, properties)
        self.assertEqual(key.storage_class, STORAGE_CLASS)

    def test_time_deleted(self):
        KEY = 'key'
        connection = _Connection()
        bucket = _Bucket(connection)
        TIME_DELETED = '2014-11-05T20:34:37Z'
        properties = {'timeDeleted': TIME_DELETED}
        key = self._makeOne(bucket, KEY, properties)
        self.assertEqual(key.time_deleted, TIME_DELETED)

    def test_updated(self):
        KEY = 'key'
        connection = _Connection()
        bucket = _Bucket(connection)
        UPDATED = '2014-11-05T20:34:37Z'
        properties = {'updated': UPDATED}
        key = self._makeOne(bucket, KEY, properties)
        self.assertEqual(key.updated, UPDATED)


class _Responder(object):

    def __init__(self, *responses):
        self._responses = responses[:]
        self._requested = []

    def _respond(self, **kw):
        self._requested.append(kw)
        response, self._responses = self._responses[0], self._responses[1:]
        return response


class _Connection(_Responder):

    API_BASE_URL = 'http://example.com'
    USER_AGENT = 'testing 1.2.3'

    def __init__(self, *responses):
        super(_Connection, self).__init__(*responses)
        self._signed = []
        self.http = _HTTP(*responses)

    def api_request(self, **kw):
        return self._respond(**kw)

    def build_api_url(self, path, query_params=None,
                      api_base_url=API_BASE_URL, upload=False):
        from urllib import urlencode
        from urlparse import urlsplit
        from urlparse import urlunsplit
        # mimic the build_api_url interface, but avoid unused param and
        # missed coverage errors
        upload = not upload  # pragma NO COVER
        qs = urlencode(query_params or {})
        scheme, netloc, _, _, _ = urlsplit(api_base_url)
        return urlunsplit((scheme, netloc, path, qs, ''))

    def generate_signed_url(self, resource, expiration, **kw):
        self._signed.append((resource, expiration, kw))
        return ('http://example.com/abucket/akey?Signature=DEADBEEF'
                '&Expiration=%s' % expiration)


class _HTTP(_Responder):

    def request(self, uri, method, headers, body, **kw):
        return self._respond(uri=uri, method=method, headers=headers,
                             body=body, **kw)


class _Bucket(object):
    path = '/b/name'
    name = 'name'

    def __init__(self, connection):
        self.connection = connection
        self._keys = {}
        self._deleted = []

    def get_key(self, key):
        return self._keys.get(key)

    def copy_key(self, key, destination_bucket, new_name):
        destination_bucket._keys[new_name] = self._keys[key.name]
        return key.from_dict({'name': new_name}, bucket=destination_bucket)

    def delete_key(self, key):
        del self._keys[key.name]
        self._deleted.append(key.name)
