# Copyright 2016 Google Inc.
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

import os
import unittest

from google.cloud import exceptions
from google.cloud import speech
from google.cloud import storage
from google.cloud.speech.transcript import Transcript

from system_test_utils import unique_resource_id
from retry import RetryErrors
from retry import RetryResult

AUDIO_FILE = os.path.join(os.path.dirname(__file__), 'data', 'hello.wav')


def _operation_complete(result):
    """Return operation result."""
    return result


def _wait_until_complete(operation, max_attempts=5):
    """Wait until an operation has completed.

    :type operation: :class:`google.cloud.operation.Operation`
    :param operation: Operation that has not completed.

    :type max_attempts: int
    :param max_attempts: (Optional) The maximum number of times to check if
                         the operation has completed. Defaults to 5.

    :rtype: bool
    :returns: Boolean indicating if the operation is complete.
    """
    retry = RetryResult(_operation_complete, max_tries=max_attempts)
    return retry(operation.poll)()


class Config(object):
    """Run-time configuration to be modified at set-up.

    This is a mutable stand-in to allow test set-up to modify
    global state.
    """
    CLIENT = None
    TEST_BUCKET = None
    USE_GAX = True


def setUpModule():
    Config.CLIENT = speech.Client()
    Config.USE_GAX = Config.CLIENT._use_gax
    Config.CLIENT = speech.Client
    # Now create a bucket for GCS stored content.
    storage_client = storage.Client()
    bucket_name = 'new' + unique_resource_id()
    Config.TEST_BUCKET = storage_client.bucket(bucket_name)
    # 429 Too Many Requests in case API requests rate-limited.
    retry_429 = RetryErrors(exceptions.TooManyRequests)
    retry_429(Config.TEST_BUCKET.create)()


def tearDownModule():
    # 409 Conflict if the bucket is full.
    # 429 Too Many Requests in case API requests rate-limited.
    bucket_retry = RetryErrors(
        (exceptions.TooManyRequests, exceptions.Conflict))
    bucket_retry(Config.TEST_BUCKET.delete)(force=True)


class TestSpeechClient(unittest.TestCase):
    ASSERT_TEXT = 'thank you for using Google Cloud platform'

    def setUp(self):
        self.to_delete_by_case = []

    def tearDown(self):
        for value in self.to_delete_by_case:
            value.delete()

    def _make_sync_request(self, content=None, source_uri=None,
                           max_alternatives=None, use_gax=True):
        client = Config.CLIENT(use_gax=use_gax)
        sample = client.sample(content=content,
                               source_uri=source_uri,
                               encoding=speech.Encoding.LINEAR16,
                               sample_rate=16000)
        return client.sync_recognize(sample,
                                     language_code='en-US',
                                     max_alternatives=max_alternatives,
                                     profanity_filter=True,
                                     speech_context=['Google', 'cloud'])

    def _make_async_request(self, content=None, source_uri=None,
                            max_alternatives=None):
        client = Config.CLIENT
        sample = client.sample(content=content,
                               source_uri=source_uri,
                               encoding=speech.Encoding.LINEAR16,
                               sample_rate=16000)
        return client.async_recognize(sample,
                                      language_code='en-US',
                                      max_alternatives=max_alternatives,
                                      profanity_filter=True,
                                      speech_context=['Google', 'cloud'])

    def _check_best_results(self, results):
        top_result = results[0]
        self.assertIsInstance(top_result, Transcript)
        self.assertEqual(top_result.transcript,
                         'hello ' + self.ASSERT_TEXT)
        self.assertGreater(top_result.confidence, 0.90)

    def test_sync_recognize_local_file(self):
        with open(AUDIO_FILE, 'rb') as file_obj:
            results = self._make_sync_request(content=file_obj.read(),
                                              max_alternatives=2)
            second_alternative = results[1]
            self.assertEqual(len(results), 2)
            self._check_best_results(results)
            self.assertIsInstance(second_alternative, Transcript)
            self.assertEqual(second_alternative.transcript, self.ASSERT_TEXT)
            self.assertEqual(second_alternative.confidence, 0.0)

    def test_sync_recognize_gcs_file(self):
        bucket_name = Config.TEST_BUCKET.name
        blob_name = 'hello.wav'
        blob = Config.TEST_BUCKET.blob(blob_name)
        self.to_delete_by_case.append(blob)  # Clean-up.
        with open(AUDIO_FILE, 'rb') as file_obj:
            blob.upload_from_file(file_obj)

        source_uri = 'gs://%s/%s' % (bucket_name, blob_name)
        result = self._make_sync_request(source_uri=source_uri,
                                         max_alternatives=1)
        self._check_best_results(result)

    def test_sync_recognize_local_file_rest(self):
        with open(AUDIO_FILE, 'rb') as file_obj:
            results = self._make_sync_request(content=file_obj.read(),
                                              max_alternatives=2,
                                              use_gax=False)
            second_alternative = results[1]
            self.assertEqual(len(results), 2)
            self._check_best_results(results)
            self.assertIsInstance(second_alternative, Transcript)
            self.assertEqual(second_alternative.transcript, self.ASSERT_TEXT)
            self.assertEqual(second_alternative.confidence, None)

    def test_sync_recognize_gcs_file_rest(self):
        bucket_name = Config.TEST_BUCKET.name
        blob_name = 'hello.wav'
        blob = Config.TEST_BUCKET.blob(blob_name)
        self.to_delete_by_case.append(blob)  # Clean-up.
        with open(AUDIO_FILE, 'rb') as file_obj:
            blob.upload_from_file(file_obj)

        source_uri = 'gs://%s/%s' % (bucket_name, blob_name)
        result = self._make_sync_request(source_uri=source_uri,
                                         max_alternatives=1,
                                         use_gax=False)
        self._check_best_results(result)

    def test_async_recognize_local_file(self):
        if Config.USE_GAX:
            self.skipTest('async_recognize gRPC not yet implemented.')
        with open(AUDIO_FILE, 'rb') as file_obj:
            content = file_obj.read()

        operation = self._make_async_request(content=content,
                                             max_alternatives=2)

        _wait_until_complete(operation)

        self.assertEqual(len(operation.results), 2)
        self._check_best_results(operation.results)

        results = operation.results
        self.assertIsInstance(results[1], Transcript)
        self.assertEqual(results[1].transcript, self.ASSERT_TEXT)
        self.assertEqual(results[1].confidence, None)

    def test_async_recognize_gcs_file(self):
        if Config.USE_GAX:
            self.skipTest('async_recognize gRPC not yet implemented.')
        bucket_name = Config.TEST_BUCKET.name
        blob_name = 'hello.wav'
        blob = Config.TEST_BUCKET.blob(blob_name)
        self.to_delete_by_case.append(blob)  # Clean-up.
        with open(AUDIO_FILE, 'rb') as file_obj:
            blob.upload_from_file(file_obj)

        source_uri = 'gs://%s/%s' % (bucket_name, blob_name)
        operation = self._make_async_request(source_uri=source_uri,
                                             max_alternatives=2)

        _wait_until_complete(operation)

        self.assertEqual(len(operation.results), 2)
        self._check_best_results(operation.results)

        results = operation.results
        self.assertIsInstance(results[1], Transcript)
        self.assertEqual(results[1].transcript, self.ASSERT_TEXT)
        self.assertEqual(results[1].confidence, None)
