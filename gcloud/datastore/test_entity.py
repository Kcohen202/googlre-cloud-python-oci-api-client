import unittest2

_MARKER = object()
_DATASET_ID = 'DATASET'
_KIND = 'KIND'
_ID = 1234


class TestEntity(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.datastore.entity import Entity

        return Entity

    def _makeOne(self, dataset=_MARKER, kind=_KIND):
        from gcloud.datastore.dataset import Dataset

        klass = self._getTargetClass()
        if dataset is _MARKER:
            dataset = Dataset(_DATASET_ID)
        return klass(dataset, kind)

    def test_ctor_defaults(self):
        klass = self._getTargetClass()
        entity = klass()
        self.assertEqual(entity.key(), None)
        self.assertEqual(entity.dataset(), None)
        self.assertEqual(entity.kind(), None)

    def test_ctor_explicit(self):
        from gcloud.datastore.dataset import Dataset

        dataset = Dataset(_DATASET_ID)
        entity = self._makeOne(dataset, _KIND)
        self.assertTrue(entity.dataset() is dataset)

    def test_key_getter(self):
        from gcloud.datastore.key import Key

        entity = self._makeOne()
        key = entity.key()
        self.assertIsInstance(key, Key)
        self.assertEqual(key.dataset().id(), _DATASET_ID)
        self.assertEqual(key.kind(), _KIND)

    def test_key_setter(self):
        entity = self._makeOne()
        key = object()
        entity.key(key)
        self.assertTrue(entity.key() is key)

    def test_from_key(self):
        from gcloud.datastore.dataset import Dataset
        from gcloud.datastore.key import Key

        klass = self._getTargetClass()
        dataset = Dataset(_DATASET_ID)
        key = Key(dataset=dataset).kind(_KIND).id(_ID)
        entity = klass.from_key(key)
        self.assertTrue(entity.dataset() is dataset)
        self.assertEqual(entity.kind(), _KIND)
        key = entity.key()
        self.assertEqual(key.kind(), _KIND)
        self.assertEqual(key.id(), _ID)

    def test_from_protobuf(self):
        from gcloud.datastore import datastore_v1_pb2 as datastore_pb
        from gcloud.datastore.dataset import Dataset

        entity_pb = datastore_pb.Entity()
        entity_pb.key.partition_id.dataset_id = _DATASET_ID
        entity_pb.key.path_element.add(kind=_KIND, id=_ID)
        prop_pb = entity_pb.property.add()
        prop_pb.name = 'foo'
        prop_pb.value.string_value = 'Foo'
        dataset = Dataset(_DATASET_ID)
        klass = self._getTargetClass()
        entity = klass.from_protobuf(entity_pb, dataset)
        self.assertTrue(entity.dataset() is dataset)
        self.assertEqual(entity.kind(), _KIND)
        self.assertEqual(entity['foo'], 'Foo')
        key = entity.key()
        self.assertTrue(key.dataset() is dataset)
        self.assertEqual(key.kind(), _KIND)
        self.assertEqual(key.id(), _ID)

    def test_reload_no_key(self):
        from gcloud.datastore.entity import NoKey

        entity = self._makeOne(None, None)
        entity['foo'] = 'Foo'
        self.assertRaises(NoKey, entity.reload)

    def test_reload_miss(self):
        dataset = _Dataset()
        key = _Key(dataset)
        entity = self._makeOne()
        entity.key(key)
        entity['foo'] = 'Foo'
        # Does not raise, does not update on miss.
        self.assertTrue(entity.reload() is entity)
        self.assertEqual(entity['foo'], 'Foo')

    def test_reload_hit(self):
        dataset = _Dataset()
        dataset['KEY'] = {'foo': 'Bar'}
        key = _Key(dataset)
        entity = self._makeOne()
        entity.key(key)
        entity['foo'] = 'Foo'
        self.assertTrue(entity.reload() is entity)
        self.assertEqual(entity['foo'], 'Bar')

    def test_save_no_key(self):
        from gcloud.datastore.entity import NoKey

        entity = self._makeOne(None, None)
        entity['foo'] = 'Foo'
        self.assertRaises(NoKey, entity.save)

    def test_save_wo_transaction_wo_auto_id_wo_returned_key(self):
        connection = _Connection()
        dataset = _Dataset(connection)
        key = _Key(dataset)
        entity = self._makeOne()
        entity.key(key)
        entity['foo'] = 'Foo'
        self.assertTrue(entity.save() is entity)
        self.assertEqual(entity['foo'], 'Foo')
        self.assertEqual(connection._saved,
                         (_DATASET_ID, 'KEY', {'foo': 'Foo'}))
        self.assertEqual(key._path, None)

    def test_save_w_transaction_wo_partial_key(self):
        connection = _Connection()
        transaction = connection._transaction = _Transaction()
        dataset = _Dataset(connection)
        key = _Key(dataset)
        entity = self._makeOne()
        entity.key(key)
        entity['foo'] = 'Foo'
        self.assertTrue(entity.save() is entity)
        self.assertEqual(entity['foo'], 'Foo')
        self.assertEqual(connection._saved,
                         (_DATASET_ID, 'KEY', {'foo': 'Foo'}))
        self.assertEqual(transaction._added, ())
        self.assertEqual(key._path, None)

    def test_save_w_transaction_w_partial_key(self):
        connection = _Connection()
        transaction = connection._transaction = _Transaction()
        dataset = _Dataset(connection)
        key = _Key(dataset)
        key._partial = True
        entity = self._makeOne()
        entity.key(key)
        entity['foo'] = 'Foo'
        self.assertTrue(entity.save() is entity)
        self.assertEqual(entity['foo'], 'Foo')
        self.assertEqual(connection._saved,
                         (_DATASET_ID, 'KEY', {'foo': 'Foo'}))
        self.assertEqual(transaction._added, (entity, ))
        self.assertEqual(key._path, None)

    def test_save_w_returned_key(self):
        from gcloud.datastore import datastore_v1_pb2 as datastore_pb
        key_pb = datastore_pb.Key()
        key_pb.partition_id.dataset_id = _DATASET_ID
        key_pb.path_element.add(kind=_KIND, id=_ID)
        connection = _Connection()
        connection._save_result = key_pb
        dataset = _Dataset(connection)
        key = _Key(dataset)
        entity = self._makeOne()
        entity.key(key)
        entity['foo'] = 'Foo'
        self.assertTrue(entity.save() is entity)
        self.assertEqual(entity['foo'], 'Foo')
        self.assertEqual(connection._saved,
                         (_DATASET_ID, 'KEY', {'foo': 'Foo'}))
        self.assertEqual(key._path, [{'kind': _KIND, 'id': _ID}])

    def test_delete_no_key(self):
        from gcloud.datastore.entity import NoKey

        entity = self._makeOne(None, None)
        entity['foo'] = 'Foo'
        self.assertRaises(NoKey, entity.delete)

    def test_delete(self):
        connection = _Connection()
        dataset = _Dataset(connection)
        key = _Key(dataset)
        entity = self._makeOne()
        entity.key(key)
        entity['foo'] = 'Foo'
        self.assertTrue(entity.delete() is None)
        self.assertEqual(connection._deleted, (_DATASET_ID, 'KEY'))

    def test___repr___no_key_empty(self):
        entity = self._makeOne(None, None)
        self.assertEqual(repr(entity), '<Entity {}>')

    def test___repr___w_key_non_empty(self):
        connection = _Connection()
        dataset = _Dataset(connection)
        key = _Key(dataset)
        key.path('/bar/baz')
        entity = self._makeOne()
        entity.key(key)
        entity['foo'] = 'Foo'
        self.assertEqual(repr(entity), "<Entity/bar/baz {'foo': 'Foo'}>")


class _Key(object):
    _MARKER = object()
    _key = 'KEY'
    _partial = False
    _path = None

    def __init__(self, dataset):
        self._dataset = dataset

    def dataset(self):
        return self._dataset

    def to_protobuf(self):
        return self._key

    def is_partial(self):
        return self._partial

    def path(self, path=_MARKER):
        if path is self._MARKER:
            return self._path
        self._path = path


class _Dataset(dict):
    def __init__(self, connection=None):
        self._connection = connection

    def id(self):
        return _DATASET_ID

    def connection(self):
        return self._connection

    def get_entity(self, key):
        return self.get(key)


class _Connection(object):
    _transaction = _saved = _deleted = None
    _save_result = True

    def transaction(self):
        return self._transaction

    def save_entity(self, dataset_id, key_pb, properties):
        self._saved = (dataset_id, key_pb, properties)
        return self._save_result

    def delete_entity(self, dataset_id, key_pb):
        self._deleted = (dataset_id, key_pb)


class _Transaction(object):
    _added = ()

    def __nonzero__(self):
        return True
    __bool__ = __nonzero__

    def add_auto_id_entity(self, entity):
        self._added += (entity, )
