import unittest2


class TestDataset(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.datastore.dataset import Dataset
        return Dataset

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_ctor_missing_dataset_id(self):
        self.assertRaises(TypeError, self._makeOne)

    def test_ctor_defaults(self):
        DATASET_ID = 'DATASET'
        dataset = self._makeOne(DATASET_ID)
        self.assertEqual(dataset.id(), DATASET_ID)
        self.assertEqual(dataset.connection(), None)

    def test_ctor_explicit(self):
        DATASET_ID = 'DATASET'
        CONNECTION = object()
        dataset = self._makeOne(DATASET_ID, CONNECTION)
        self.assertEqual(dataset.id(), DATASET_ID)
        self.assertTrue(dataset.connection() is CONNECTION)

    def test_transaction_factory(self):
        from gcloud.datastore.transaction import Transaction
        DATASET_ID = 'DATASET'
        dataset = self._makeOne(DATASET_ID)
        transaction = dataset.transaction()
        self.assertIsInstance(transaction, Transaction)
        self.assertTrue(transaction.dataset() is dataset)

    def test_get_entities_miss(self):
        from gcloud.datastore.key import Key
        DATASET_ID = 'DATASET'
        connection = _Connection()
        dataset = self._makeOne(DATASET_ID, connection)
        key = Key(path=[{'kind': 'Kind', 'id': 1234}])
        self.assertEqual(dataset.get_entities([key]), [])

    def test_get_entities_hit(self):
        from gcloud.datastore.connection import datastore_pb
        from gcloud.datastore.key import Key
        DATASET_ID = 'DATASET'
        KIND = 'Kind'
        ID = 1234
        PATH = [{'kind': KIND, 'id': ID}]
        entity_pb = datastore_pb.Entity()
        entity_pb.key.partition_id.dataset_id = DATASET_ID
        path_element = entity_pb.key.path_element.add()
        path_element.kind = KIND
        path_element.id = ID
        prop = entity_pb.property.add()
        prop.name = 'foo'
        prop.value.string_value = 'Foo'
        connection = _Connection(entity_pb)
        dataset = self._makeOne(DATASET_ID, connection)
        key = Key(path=PATH)
        result, = dataset.get_entities([key])
        key = result.key()
        self.assertEqual(key._dataset_id, DATASET_ID)
        self.assertEqual(key.path(), PATH)
        self.assertEqual(list(result), ['foo'])
        self.assertEqual(result['foo'], 'Foo')

    def test_get_entity_miss(self):
        from gcloud.datastore.key import Key
        DATASET_ID = 'DATASET'
        connection = _Connection()
        dataset = self._makeOne(DATASET_ID, connection)
        key = Key(path=[{'kind': 'Kind', 'id': 1234}])
        self.assertEqual(dataset.get_entity(key), None)

    def test_get_entity_hit(self):
        from gcloud.datastore.connection import datastore_pb
        from gcloud.datastore.key import Key
        DATASET_ID = 'DATASET'
        KIND = 'Kind'
        ID = 1234
        PATH = [{'kind': KIND, 'id': ID}]
        entity_pb = datastore_pb.Entity()
        entity_pb.key.partition_id.dataset_id = DATASET_ID
        path_element = entity_pb.key.path_element.add()
        path_element.kind = KIND
        path_element.id = ID
        prop = entity_pb.property.add()
        prop.name = 'foo'
        prop.value.string_value = 'Foo'
        connection = _Connection(entity_pb)
        dataset = self._makeOne(DATASET_ID, connection)
        key = Key(path=PATH)
        result = dataset.get_entity(key)
        key = result.key()
        self.assertEqual(key._dataset_id, DATASET_ID)
        self.assertEqual(key.path(), PATH)
        self.assertEqual(list(result), ['foo'])
        self.assertEqual(result['foo'], 'Foo')


class _Connection(object):
    _called_with = None

    def __init__(self, *result):
        self._result = list(result)

    def lookup(self, **kw):
        self._called_with = kw
        return self._result
