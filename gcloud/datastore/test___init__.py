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


class Test_get_connection(unittest2.TestCase):

    def _callFUT(self):
        from gcloud.datastore import get_connection
        return get_connection()

    def test_it(self):
        from gcloud import credentials
        from gcloud.datastore.connection import Connection
        from gcloud.test_credentials import _Client
        from gcloud._testing import _Monkey

        client = _Client()
        with _Monkey(credentials, client=client):
            found = self._callFUT()
        self.assertTrue(isinstance(found, Connection))
        self.assertTrue(found._credentials is client._signed)
        self.assertTrue(client._get_app_default_called)


class Test__set_dataset_from_environ(unittest2.TestCase):

    def _callFUT(self):
        from gcloud.datastore import _set_dataset_from_environ
        return _set_dataset_from_environ()

    def _test_with_environ(self, environ, expected_result):
        import os
        from gcloud._testing import _Monkey
        from gcloud import datastore
        from gcloud.datastore import _implicit_environ

        # Check the environment is unset.
        self.assertEqual(_implicit_environ.DATASET, None)

        def custom_getenv(key):
            return environ.get(key)

        def custom_get_dataset(dataset_id):
            return dataset_id

        with _Monkey(os, getenv=custom_getenv):
            with _Monkey(datastore, get_dataset=custom_get_dataset):
                self._callFUT()

        self.assertEqual(_implicit_environ.DATASET, expected_result)

    def test_set_from_env_var(self):
        from gcloud.datastore import _DATASET_ENV_VAR_NAME

        # Make a custom getenv function to Monkey.
        DATASET = 'dataset'
        VALUES = {
            _DATASET_ENV_VAR_NAME: DATASET,
        }
        self._test_with_environ(VALUES, DATASET)

    def test_no_env_var_set(self):
        self._test_with_environ({}, None)


class Test_get_dataset(unittest2.TestCase):

    def _callFUT(self, dataset_id):
        from gcloud.datastore import get_dataset
        return get_dataset(dataset_id)

    def test_it(self):
        from gcloud import credentials
        from gcloud.datastore.connection import Connection
        from gcloud.datastore.dataset import Dataset
        from gcloud.test_credentials import _Client
        from gcloud._testing import _Monkey

        DATASET_ID = 'DATASET'
        client = _Client()
        with _Monkey(credentials, client=client):
            found = self._callFUT(DATASET_ID)
        self.assertTrue(isinstance(found, Dataset))
        self.assertTrue(isinstance(found.connection(), Connection))
        self.assertEqual(found.id(), DATASET_ID)
        self.assertTrue(client._get_app_default_called)


class Test_implicit_behavior(unittest2.TestCase):

    def test__require_dataset(self):
        import gcloud.datastore
        from gcloud.datastore import _implicit_environ
        original_dataset = _implicit_environ.DATASET

        try:
            _implicit_environ.DATASET = None
            self.assertRaises(EnvironmentError,
                              gcloud.datastore._require_dataset)
            NEW_DATASET = object()
            _implicit_environ.DATASET = NEW_DATASET
            self.assertEqual(gcloud.datastore._require_dataset(), NEW_DATASET)
        finally:
            _implicit_environ.DATASET = original_dataset

    def test_get_entity(self):
        import gcloud.datastore
        from gcloud.datastore import _implicit_environ
        from gcloud.datastore.test_entity import _Dataset
        from gcloud._testing import _Monkey

        CUSTOM_DATASET = _Dataset()
        DUMMY_KEY = object()
        DUMMY_VAL = object()
        CUSTOM_DATASET[DUMMY_KEY] = DUMMY_VAL
        with _Monkey(_implicit_environ, DATASET=CUSTOM_DATASET):
            result = gcloud.datastore.get_entity(DUMMY_KEY)
        self.assertTrue(result is DUMMY_VAL)

    def test_get_entities(self):
        import gcloud.datastore
        from gcloud.datastore import _implicit_environ
        from gcloud.datastore.test_entity import _Dataset
        from gcloud._testing import _Monkey

        CUSTOM_DATASET = _Dataset()
        DUMMY_KEYS = [object(), object()]
        DUMMY_VALS = [object(), object()]
        for key, val in zip(DUMMY_KEYS, DUMMY_VALS):
            CUSTOM_DATASET[key] = val

        with _Monkey(_implicit_environ, DATASET=CUSTOM_DATASET):
            result = gcloud.datastore.get_entities(DUMMY_KEYS)
        self.assertTrue(result == DUMMY_VALS)

    def test_allocate_ids(self):
        import gcloud.datastore
        from gcloud.datastore import _implicit_environ
        from gcloud.datastore.key import Key
        from gcloud.datastore.test_entity import _Dataset
        from gcloud._testing import _Monkey

        CUSTOM_DATASET = _Dataset()
        INCOMPLETE_KEY = Key()
        NUM_IDS = 2
        with _Monkey(_implicit_environ, DATASET=CUSTOM_DATASET):
            result = gcloud.datastore.allocate_ids(INCOMPLETE_KEY, NUM_IDS)

        # Check the IDs returned.
        self.assertEqual([key.id() for key in result], range(1, NUM_IDS + 1))

    def test_set_DATASET(self):
        import os
        from gcloud._testing import _Monkey
        from gcloud.test_credentials import _Client
        from gcloud import credentials
        from gcloud.datastore import _implicit_environ

        # Make custom client for doing auth. Have to fake auth since we
        # can't monkey patch `datastore.get_dataset` while reloading the
        # `datastore.__init__` module.
        client = _Client()

        # Fake auth variables.
        DATASET = 'dataset'

        # Make a custom getenv function to Monkey.
        VALUES = {
            'GCLOUD_DATASET_ID': DATASET,
        }

        def custom_getenv(key):
            return VALUES.get(key)

        # Perform the import again with our test patches.
        with _Monkey(credentials, client=client):
            with _Monkey(os, getenv=custom_getenv):
                import gcloud.datastore
                reload(gcloud.datastore)

        # Check that the DATASET was correctly implied from the environ.
        implicit_dataset = _implicit_environ.DATASET
        self.assertEqual(implicit_dataset.id(), DATASET)
        # Check that the credentials on the implicit DATASET was set on the
        # fake client.
        cnxn_credentials = implicit_dataset.connection().credentials
        self.assertTrue(cnxn_credentials is client._signed)
