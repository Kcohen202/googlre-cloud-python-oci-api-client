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

"""Class for representing a single entity in the Cloud Datastore."""

from gcloud.datastore import datastore_v1_pb2 as datastore_pb
from gcloud.datastore.key import Key


class NoKey(RuntimeError):
    """Exception raised by Entity methods which require a key."""


class NoDataset(RuntimeError):
    """Exception raised by Entity methods which require a dataset."""


class Entity(object):
    """Entities are akin to rows in a relational database

    An entity storing the actual instance of data.

    Each entity is officially represented with a
    :class:`gcloud.datastore.key.Key` class, however it is possible that
    you might create an Entity with only a partial Key (that is, a Key
    with a Kind, and possibly a parent, but without an ID).  In such a
    case, the datastore service will automatically assign an ID to the
    partial key.

    Entities in this API act like dictionaries with extras built in that
    allow you to delete or persist the data stored on the entity.

    Entities are mutable and properties can be set, updated and deleted
    like keys in a dictionary. This means you could take an existing entity
    and change the key to duplicate the object.

    Use :func:`gcloud.datastore.dataset.Dataset.get_entity`
    to retrieve an existing entity.

      >>> dataset.get_entity(key)
      <Entity[{'kind': 'EntityKind', id: 1234}] {'property': 'value'}>

    You can the set values on the entity just like you would on any
    other dictionary.

    >>> entity['age'] = 20
    >>> entity['name'] = 'JJ'
    >>> entity
    <Entity[{'kind': 'EntityKind', id: 1234}] {'age': 20, 'name': 'JJ'}>

    And you can convert an entity to a regular Python dictionary

    >>> entity.to_dict()
    {'age': 20, 'name': 'JJ'}

    .. note::

       When saving an entity to the backend, values which are "text"
       ('unicode' in Python2, 'str' in Python3) will be saved using
       the 'text_value' field, after being encoded to UTF-8.  When
       retrieved from the back-end, such values will be decoded to "text"
       again.  Values which are "bytes" ('str' in Python2, 'bytes' in
       Python3), will be saved using the 'blob_value' field, without
       any decoding / encoding step.

    :type dataset: :class:`gcloud.datastore.dataset.Dataset`
    :param dataset: The dataset in which this entity belongs.

    :type kind: string
    :param kind: The kind of entity this is, akin to a table name in a
                 relational database.

    :type dataset: :class:`gcloud.datastore.dataset.Dataset`, or None
    :param dataset: the Dataset instance associated with this entity.

    :type kind: str
    :param kind: the "kind" of the entity (see
                 https://cloud.google.com/datastore/docs/concepts/entities#Datastore_Kinds_and_identifiers)

    :param exclude_from_indexes: names of fields whose values are not to be
                                 indexed for this entity.
    """

    def __init__(self, dataset=None, kind=None, exclude_from_indexes=()):
        self._dataset = dataset
        self._data = {}
        if kind:
            self._key = Key().kind(kind)
        else:
            self._key = None
        self._exclude_from_indexes = set(exclude_from_indexes)

    def __getitem__(self, item_name):
        return self._data[item_name]

    def __setitem__(self, item_name, value):
        self._data[item_name] = value

    def __delitem__(self, item_name):
        del self._data[item_name]

    def clear_properties(self):
        """Clear all properties from the Entity."""
        self._data.clear()

    def update_properties(self, *args, **kwargs):
        """Allows entity properties to be updated in bulk.

        Either takes a single dictionary or uses the keywords passed in.

          >>> entity
          <Entity[{'kind': 'Foo', 'id': 1}] {}>
          >>> entity.update_properties(prop1=u'bar', prop2=u'baz')
          >>> entity
          <Entity[{'kind': 'Foo', 'id': 1}] {'prop1': u'bar', 'prop2': u'baz'}>
          >>> entity.update_properties({'prop1': 0, 'prop2': 1})
          >>> entity
          <Entity[{'kind': 'Foo', 'id': 1}] {'prop1': 0, 'prop2': 1}>

        :raises: `TypeError` a mix of positional and keyword arguments are
                 used or if more than one positional argument is used.
        """
        if args and kwargs or len(args) > 1:
            raise TypeError('Only a single dictionary or keyword arguments '
                            'may be used')
        if args:
            dict_arg, = args
            self._data.update(dict_arg)
        else:
            self._data.update(kwargs)

    def to_dict(self):
        """Converts the stored properties to a dictionary."""
        return self._data.copy()

    def dataset(self):
        """Get the :class:`.dataset.Dataset` in which this entity belongs.

        .. note::
          This is based on the :class:`gcloud.datastore.key.Key` set on the
          entity. That means that if you have no key set, the dataset might
          be `None`. It also means that if you change the key on the entity,
          this will refer to that key's dataset.

        :rtype: :class:`gcloud.datastore.dataset.Dataset`
        :returns: The Dataset containing the entity if there is a key,
                  else None.
        """
        return self._dataset

    def key(self, key=None):
        """Get or set the :class:`.datastore.key.Key` on the current entity.

        :type key: :class:`glcouddatastore.key.Key`
        :param key: The key you want to set on the entity.

        :rtype: :class:`gcloud.datastore.key.Key` or :class:`Entity`.
        :returns: Either the current key (on get) or the current
                  object (on set).

        >>> entity.key(my_other_key)  # This returns the original entity.
        <Entity[{'kind': 'OtherKeyKind', 'id': 1234}] {'property': 'value'}>
        >>> entity.key()  # This returns the key.
        <Key[{'kind': 'OtherKeyKind', 'id': 1234}]>
        """

        if key is not None:
            self._key = key
            return self
        else:
            return self._key

    def kind(self):
        """Get the kind of the current entity.

        .. note::
          This relies entirely on the :class:`gcloud.datastore.key.Key`
          set on the entity.  That means that we're not storing the kind
          of the entity at all, just the properties and a pointer to a
          Key which knows its Kind.
        """

        if self._key:
            return self._key.kind()

    def exclude_from_indexes(self):
        """Names of fields which are *not* to be indexed for this entity.

        :rtype: sequence of field names
        """
        return frozenset(self._exclude_from_indexes)

    @classmethod
    def from_key(cls, key, dataset=None):
        """Create entity based on :class:`.datastore.key.Key`.

        .. note:: This is a factory method.

        :type key: :class:`gcloud.datastore.key.Key`
        :param key: The key for the entity.

        :returns: The :class:`Entity` derived from the
                  :class:`gcloud.datastore.key.Key`.
        """

        return cls(dataset).key(key)

    @property
    def _must_key(self):
        """Return our key, or raise NoKey if not set.

        :rtype: :class:`gcloud.datastore.key.Key`.
        :returns: our key
        :raises: NoKey if key is None
        """
        if self._key is None:
            raise NoKey()
        return self._key

    @property
    def _must_dataset(self):
        """Return our dataset, or raise NoDataset if not set.

        :rtype: :class:`gcloud.datastore.key.Key`.
        :returns: our key
        :raises: NoDataset if key is None
        """
        if self._dataset is None:
            raise NoDataset()
        return self._dataset

    def reload(self):
        """Reloads the contents of this entity from the datastore.

        This method takes the :class:`gcloud.datastore.key.Key`, loads all
        properties from the Cloud Datastore, and sets the updated properties on
        the current object.

        .. warning::
          This will override any existing properties if a different value
          exists remotely, however it will *not* override any properties that
          exist only locally.
        """
        key = self._must_key
        dataset = self._must_dataset
        entity = dataset.get_entity(key.to_protobuf())

        if entity:
            self.update_properties(entity.to_dict())
        return self

    def save(self):
        """Save the entity in the Cloud Datastore.

        .. note::
           Any existing properties for the entity will be replaced by those
           currently set on this instance.  Already-stored properties which do
           not correspond to keys set on this instance will be removed from
           the datastore.

        .. note::
           Property values which are "text" ('unicode' in Python2, 'str' in
           Python3) map to 'string_value' in the datastore;  values which are
           "bytes" ('str' in Python2, 'bytes' in Python3) map to 'blob_value'.

        :rtype: :class:`gcloud.datastore.entity.Entity`
        :returns: The entity with a possibly updated Key.
        """
        key = self._must_key
        dataset = self._must_dataset
        connection = dataset.connection()
        key_pb = connection.save_entity(
            dataset_id=dataset.id(),
            key_pb=key.to_protobuf(),
            properties=self._data,
            exclude_from_indexes=self.exclude_from_indexes())

        # If we are in a transaction and the current entity needs an
        # automatically assigned ID, tell the transaction where to put that.
        transaction = connection.transaction()
        if transaction and key.is_partial():
            transaction.add_auto_id_entity(self)

        if isinstance(key_pb, datastore_pb.Key):
            # Update the path (which may have been altered).
            # NOTE: The underlying namespace can't have changed in a save().
            #       The value of the dataset ID may have changed from implicit
            #       (i.e. None, with the ID implied from the dataset.Dataset
            #       object associated with the Entity/Key), but if it was
            #       implicit before the save() we leave it as implicit.
            path = []
            for element in key_pb.path_element:
                key_part = {}
                for descriptor, value in element._fields.items():
                    key_part[descriptor.name] = value
                path.append(key_part)
            self._key = key.path(path)

        return self

    def delete(self):
        """Delete the entity in the Cloud Datastore.

        .. note::
          This is based entirely off of the :class:`gcloud.datastore.key.Key`
          set on the entity. Whatever is stored remotely using the key on the
          entity will be deleted.
        """
        key = self._must_key
        dataset = self._must_dataset
        dataset.connection().delete_entities(
            dataset_id=dataset.id(),
            key_pbs=[key.to_protobuf()],
            )

    def __repr__(self):
        if self._key:
            return '<Entity%s %r>' % (self._key.path(), self._data)
        else:
            return '<Entity %r>' % (self._data,)
