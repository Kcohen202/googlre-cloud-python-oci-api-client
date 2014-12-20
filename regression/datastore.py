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

import datetime
import pytz
import unittest2

from gcloud import datastore
datastore._DATASET_ENV_VAR_NAME = 'GCLOUD_TESTS_DATASET_ID'
datastore._set_dataset_from_environ()
# This assumes the command is being run via tox hence the
# repository root is the current directory.
from regression import populate_datastore


class TestDatastore(unittest2.TestCase):

    def setUp(self):
        self.case_entities_to_delete = []

    def tearDown(self):
        with datastore.transaction.Transaction():
            for entity in self.case_entities_to_delete:
                entity.delete()


class TestDatastoreAllocateIDs(TestDatastore):

    def test_allocate_ids(self):
        incomplete_key = datastore.key.Key(path=[{'kind': 'Kind'}])
        num_ids = 10
        allocated_keys = datastore.allocate_ids(incomplete_key, num_ids)
        self.assertEqual(len(allocated_keys), num_ids)

        unique_ids = set()
        for key in allocated_keys:
            unique_ids.add(key.id())
            self.assertEqual(key.name(), None)
            self.assertNotEqual(key.id(), None)

        self.assertEqual(len(unique_ids), num_ids)


class TestDatastoreSave(TestDatastore):

    def _get_post(self, name=None, key_id=None, post_content=None):
        post_content = post_content or {
            'title': u'How to make the perfect pizza in your grill',
            'tags': [u'pizza', u'grill'],
            'publishedAt': datetime.datetime(2001, 1, 1, tzinfo=pytz.utc),
            'author': u'Silvano',
            'isDraft': False,
            'wordCount': 400,
            'rating': 5.0,
        }
        # Create an entity with the given content.
        entity = datastore.entity.Entity(kind='Post')
        entity.update_properties(post_content)

        # Update the entity key.
        key = None
        if name is not None:
            key = entity.key().name(name)
        if key_id is not None:
            key = entity.key().id(key_id)
        if key is not None:
            entity.key(key)

        return entity

    def _generic_test_post(self, name=None, key_id=None):
        entity = self._get_post(name=name, key_id=key_id)
        entity.save()

        # Register entity to be deleted.
        self.case_entities_to_delete.append(entity)

        if name is not None:
            self.assertEqual(entity.key().name(), name)
        if key_id is not None:
            self.assertEqual(entity.key().id(), key_id)
        retrieved_entity = datastore.get_entity(entity.key())
        # Check the keys are the same.
        self.assertEqual(retrieved_entity.key().path(), entity.key().path())
        self.assertEqual(retrieved_entity.key().namespace(),
                         entity.key().namespace())

        # Check the data is the same.
        self.assertEqual(retrieved_entity.to_dict(), entity.to_dict())

    def test_post_with_name(self):
        self._generic_test_post(name='post1')

    def test_post_with_id(self):
        self._generic_test_post(key_id=123456789)

    def test_post_with_generated_id(self):
        self._generic_test_post()

    def test_save_multiple(self):
        with datastore.transaction.Transaction():
            entity1 = self._get_post()
            entity1.save()
            # Register entity to be deleted.
            self.case_entities_to_delete.append(entity1)

            second_post_content = {
                'title': u'How to make the perfect homemade pasta',
                'tags': [u'pasta', u'homemade'],
                'publishedAt': datetime.datetime(2001, 1, 1),
                'author': u'Silvano',
                'isDraft': False,
                'wordCount': 450,
                'rating': 4.5,
            }
            entity2 = self._get_post(post_content=second_post_content)
            entity2.save()
            # Register entity to be deleted.
            self.case_entities_to_delete.append(entity2)

        keys = [entity1.key(), entity2.key()]
        matches = datastore.get_entities(keys)
        self.assertEqual(len(matches), 2)

    def test_empty_kind(self):
        posts = datastore.query.Query(kind='Post').limit(2).fetch()
        self.assertEqual(posts, [])


class TestDatastoreSaveKeys(TestDatastore):

    def test_save_key_self_reference(self):
        key = datastore.key.Key.from_path('Person', 'name')
        entity = datastore.entity.Entity(kind=None).key(key)
        entity['fullName'] = u'Full name'
        entity['linkedTo'] = key  # Self reference.

        entity.save()
        self.case_entities_to_delete.append(entity)

        query = datastore.query.Query(kind='Person').filter(
            'linkedTo', '=', key).limit(2)

        stored_persons = query.fetch()
        self.assertEqual(len(stored_persons), 1)

        stored_person = stored_persons[0]
        self.assertEqual(stored_person['fullName'], entity['fullName'])
        self.assertEqual(stored_person.key().path(), key.path())
        self.assertEqual(stored_person.key().namespace(), key.namespace())


class TestDatastoreQuery(TestDatastore):

    @classmethod
    def setUpClass(cls):
        super(TestDatastoreQuery, cls).setUpClass()
        cls.CHARACTERS = populate_datastore.CHARACTERS
        cls.ANCESTOR_KEY = datastore.key.Key(
            path=[populate_datastore.ANCESTOR])

    def _base_query(self):
        return datastore.query.Query(kind='Character').ancestor(
            self.ANCESTOR_KEY)

    def test_limit_queries(self):
        limit = 5
        query = self._base_query().limit(limit)

        # Fetch characters.
        character_entities, cursor, _ = query.fetch_page()
        self.assertEqual(len(character_entities), limit)

        # Check cursor after fetch.
        self.assertTrue(cursor is not None)

        # Fetch next batch of characters.
        new_query = self._base_query().with_cursor(cursor)
        new_character_entities = new_query.fetch()
        characters_remaining = len(self.CHARACTERS) - limit
        self.assertEqual(len(new_character_entities), characters_remaining)

    def test_query_simple_filter(self):
        query = self._base_query().filter('appearances', '>=', 20)
        expected_matches = 6
        # We expect 6, but allow the query to get 1 extra.
        entities = query.fetch(limit=expected_matches + 1)
        self.assertEqual(len(entities), expected_matches)

    def test_query_multiple_filters(self):
        query = self._base_query().filter(
            'appearances', '>=', 26).filter('family', '=', 'Stark')
        expected_matches = 4
        # We expect 4, but allow the query to get 1 extra.
        entities = query.fetch(limit=expected_matches + 1)
        self.assertEqual(len(entities), expected_matches)

    def test_ancestor_query(self):
        filtered_query = self._base_query()

        expected_matches = 8
        # We expect 8, but allow the query to get 1 extra.
        entities = filtered_query.fetch(limit=expected_matches + 1)
        self.assertEqual(len(entities), expected_matches)

    def test_query___key___filter(self):
        rickard_key = datastore.key.Key(
            path=[populate_datastore.ANCESTOR, populate_datastore.RICKARD])

        query = self._base_query().filter('__key__', '=', rickard_key)
        expected_matches = 1
        # We expect 1, but allow the query to get 1 extra.
        entities = query.fetch(limit=expected_matches + 1)
        self.assertEqual(len(entities), expected_matches)

    def test_ordered_query(self):
        query = self._base_query().order('appearances')
        expected_matches = 8
        # We expect 8, but allow the query to get 1 extra.
        entities = query.fetch(limit=expected_matches + 1)
        self.assertEqual(len(entities), expected_matches)

        # Actually check the ordered data returned.
        self.assertEqual(entities[0]['name'], self.CHARACTERS[0]['name'])
        self.assertEqual(entities[7]['name'], self.CHARACTERS[3]['name'])

    def test_projection_query(self):
        filtered_query = self._base_query().projection(['name', 'family'])

        # NOTE: There are 9 responses because of Catelyn. She has both
        #       Stark and Tully as her families, hence occurs twice in
        #       the results.
        expected_matches = 9
        # We expect 9, but allow the query to get 1 extra.
        entities = filtered_query.fetch(limit=expected_matches + 1)
        self.assertEqual(len(entities), expected_matches)

        arya_entity = entities[0]
        self.assertEqual(arya_entity.to_dict(),
                         {'name': 'Arya', 'family': 'Stark'})

        catelyn_stark_entity = entities[2]
        self.assertEqual(catelyn_stark_entity.to_dict(),
                         {'name': 'Catelyn', 'family': 'Stark'})

        catelyn_tully_entity = entities[3]
        self.assertEqual(catelyn_tully_entity.to_dict(),
                         {'name': 'Catelyn', 'family': 'Tully'})

        # Check both Catelyn keys are the same.
        catelyn_stark_key = catelyn_stark_entity.key()
        catelyn_tully_key = catelyn_tully_entity.key()
        self.assertEqual(catelyn_stark_key.path(), catelyn_tully_key.path())
        self.assertEqual(catelyn_stark_key.namespace(),
                         catelyn_tully_key.namespace())
        # Also check the _dataset_id since both retrieved from datastore.
        self.assertEqual(catelyn_stark_key._dataset_id,
                         catelyn_tully_key._dataset_id)

        sansa_entity = entities[8]
        self.assertEqual(sansa_entity.to_dict(),
                         {'name': 'Sansa', 'family': 'Stark'})

    def test_query_paginate_with_offset(self):
        query = self._base_query()
        offset = 2
        limit = 3
        page_query = query.offset(offset).limit(limit).order('appearances')

        # Fetch characters.
        entities, cursor, _ = page_query.fetch_page()
        self.assertEqual(len(entities), limit)
        self.assertEqual(entities[0]['name'], 'Robb')
        self.assertEqual(entities[1]['name'], 'Bran')
        self.assertEqual(entities[2]['name'], 'Catelyn')

        # Use cursor to begin next query.
        next_query = page_query.with_cursor(cursor).offset(0)
        self.assertEqual(next_query.limit(), limit)
        # Fetch next set of characters.
        entities = next_query.fetch()
        self.assertEqual(len(entities), limit)
        self.assertEqual(entities[0]['name'], 'Sansa')
        self.assertEqual(entities[1]['name'], 'Jon Snow')
        self.assertEqual(entities[2]['name'], 'Arya')

    def test_query_paginate_with_start_cursor(self):
        query = self._base_query()
        offset = 2
        limit = 2
        page_query = query.offset(offset).limit(limit).order('appearances')

        # Fetch characters.
        entities, cursor, _ = page_query.fetch_page()
        self.assertEqual(len(entities), limit)

        # Use cursor to create a fresh query.
        fresh_query = self._base_query()
        fresh_query = fresh_query.order('appearances').with_cursor(cursor)

        new_entities = fresh_query.fetch()
        characters_remaining = len(self.CHARACTERS) - limit - offset
        self.assertEqual(len(new_entities), characters_remaining)
        self.assertEqual(new_entities[0]['name'], 'Catelyn')
        self.assertEqual(new_entities[3]['name'], 'Arya')

    def test_query_group_by(self):
        query = self._base_query().group_by(['alive'])

        expected_matches = 2
        # We expect 2, but allow the query to get 1 extra.
        entities = query.fetch(limit=expected_matches + 1)
        self.assertEqual(len(entities), expected_matches)

        self.assertEqual(entities[0]['name'], 'Catelyn')
        self.assertEqual(entities[1]['name'], 'Arya')


class TestDatastoreTransaction(TestDatastore):

    def test_transaction(self):
        key = datastore.key.Key.from_path('Company', 'Google')
        entity = datastore.entity.Entity(kind=None).key(key)
        entity['url'] = u'www.google.com'

        with datastore.transaction.Transaction():
            retrieved_entity = datastore.get_entity(key)
            if retrieved_entity is None:
                entity.save()
                self.case_entities_to_delete.append(entity)

        # This will always return after the transaction.
        retrieved_entity = datastore.get_entity(key)
        self.assertEqual(retrieved_entity.to_dict(), entity.to_dict())
        retrieved_entity.delete()
