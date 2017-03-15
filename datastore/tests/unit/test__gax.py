# Copyright 2017 Google Inc.
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

import unittest

import mock

from google.cloud.datastore.client import _HAVE_GRPC


@unittest.skipUnless(_HAVE_GRPC, 'No gRPC')
class Test__grpc_catch_rendezvous(unittest.TestCase):

    def _call_fut(self):
        from google.cloud.datastore._gax import _grpc_catch_rendezvous

        return _grpc_catch_rendezvous()

    @staticmethod
    def _fake_method(exc, result=None):
        if exc is None:
            return result
        else:
            raise exc

    @staticmethod
    def _make_rendezvous(status_code, details):
        from grpc._channel import _RPCState
        from google.cloud.exceptions import GrpcRendezvous

        exc_state = _RPCState((), None, None, status_code, details)
        return GrpcRendezvous(exc_state, None, None, None)

    def test_success(self):
        expected = object()
        with self._call_fut():
            result = self._fake_method(None, expected)
        self.assertIs(result, expected)

    def test_failure_aborted(self):
        from grpc import StatusCode
        from google.cloud.exceptions import Conflict

        details = 'Bad things.'
        exc = self._make_rendezvous(StatusCode.ABORTED, details)
        with self.assertRaises(Conflict):
            with self._call_fut():
                self._fake_method(exc)

    def test_failure_invalid_argument(self):
        from grpc import StatusCode
        from google.cloud.exceptions import BadRequest

        details = ('Cannot have inequality filters on multiple '
                   'properties: [created, priority]')
        exc = self._make_rendezvous(StatusCode.INVALID_ARGUMENT, details)
        with self.assertRaises(BadRequest):
            with self._call_fut():
                self._fake_method(exc)

    def test_failure_cancelled(self):
        from google.cloud.exceptions import GrpcRendezvous
        from grpc import StatusCode

        exc = self._make_rendezvous(StatusCode.CANCELLED, None)
        with self.assertRaises(GrpcRendezvous):
            with self._call_fut():
                self._fake_method(exc)

    def test_commit_failure_non_grpc_err(self):
        exc = RuntimeError('Not a gRPC error')
        with self.assertRaises(RuntimeError):
            with self._call_fut():
                self._fake_method(exc)

    def test_gax_error(self):
        from google.gax.errors import GaxError
        from grpc import StatusCode
        from google.cloud.exceptions import Forbidden

        # First, create low-level GrpcRendezvous exception.
        details = 'Some error details.'
        cause = self._make_rendezvous(StatusCode.PERMISSION_DENIED, details)
        # Then put it into a high-level GaxError.
        msg = 'GAX Error content.'
        exc = GaxError(msg, cause=cause)

        with self.assertRaises(Forbidden):
            with self._call_fut():
                self._fake_method(exc)

    def test_gax_error_not_mapped(self):
        from google.gax.errors import GaxError
        from grpc import StatusCode

        cause = self._make_rendezvous(StatusCode.CANCELLED, None)
        exc = GaxError(None, cause=cause)

        with self.assertRaises(GaxError):
            with self._call_fut():
                self._fake_method(exc)


@unittest.skipUnless(_HAVE_GRPC, 'No gRPC')
class TestGAPICDatastoreAPI(unittest.TestCase):

    @staticmethod
    def _get_target_class():
        from google.cloud.datastore._gax import GAPICDatastoreAPI

        return GAPICDatastoreAPI

    def _make_one(self, *args, **kwargs):
        return self._get_target_class()(*args, **kwargs)

    def test_commit(self):
        from google.cloud.gapic.datastore.v1 import datastore_client

        patch1 = mock.patch.object(
            datastore_client.DatastoreClient, '__init__',
            return_value=None)
        patch2 = mock.patch.object(datastore_client.DatastoreClient, 'commit')
        patch3 = mock.patch(
            'google.cloud.datastore._gax._grpc_catch_rendezvous')

        with patch1 as mock_constructor:
            ds_api = self._make_one()
            mock_constructor.assert_called_once_with()
            with patch2 as mock_commit:
                with patch3 as mock_catch_rendezvous:
                    mock_catch_rendezvous.assert_not_called()
                    ds_api.commit(1, 2, a=3)
                    mock_commit.assert_called_once_with(1, 2, a=3)
                    mock_catch_rendezvous.assert_called_once_with()


@unittest.skipUnless(_HAVE_GRPC, 'No gRPC')
class Test_make_datastore_api(unittest.TestCase):

    def _call_fut(self, client):
        from google.cloud.datastore._gax import make_datastore_api

        return make_datastore_api(client)

    @mock.patch(
        'google.cloud.datastore._gax.GAPICDatastoreAPI',
        return_value=mock.sentinel.ds_client)
    @mock.patch('google.cloud.datastore._gax.make_secure_channel',
                return_value=mock.sentinel.channel)
    def test_it(self, make_chan, mock_klass):
        from google.cloud.gapic.datastore.v1 import datastore_client
        from google.cloud._http import DEFAULT_USER_AGENT
        from google.cloud.datastore import __version__

        client = mock.Mock(
            _credentials=mock.sentinel.credentials, spec=['_credentials'])
        ds_api = self._call_fut(client)
        self.assertIs(ds_api, mock.sentinel.ds_client)

        make_chan.assert_called_once_with(
            mock.sentinel.credentials, DEFAULT_USER_AGENT,
            datastore_client.DatastoreClient.SERVICE_ADDRESS)
        mock_klass.assert_called_once_with(
            channel=mock.sentinel.channel, lib_name='gccl',
            lib_version=__version__)
