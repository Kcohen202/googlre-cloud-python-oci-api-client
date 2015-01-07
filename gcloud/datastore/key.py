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

"""Create / interact with gcloud datastore keys."""

import copy
from itertools import izip
import six

from gcloud.datastore import _implicit_environ
from gcloud.datastore import datastore_v1_pb2 as datastore_pb


class Key(object):
    """An immutable representation of a datastore Key.

    To create a basic key:

      >>> Key('EntityKind', 1234)
      <Key[{'kind': 'EntityKind', 'id': 1234}]>
      >>> Key('EntityKind', 'foo')
      <Key[{'kind': 'EntityKind', 'name': 'foo'}]>

    To create a key with a parent:

      >>> Key('Parent', 'foo', 'Child', 1234)
      <Key[{'kind': 'Parent', 'name': 'foo'}, {'kind': 'Child', 'id': 1234}]>

    To create a paritial key:

      >>> Key('Parent', 'foo', 'Child')
      <Key[{'kind': 'Parent', 'name': 'foo'}, {'kind': 'Child'}]>

    .. automethod:: __init__
    """

    def __init__(self, *path_args, **kwargs):
        """Constructor / initializer for a key.

        :type path_args: tuple of strings and ints
        :param path_args: May represent a partial (odd length) or full (even
                          length) key path.

        :type namespace: :class:`str`
        :param namespace: A namespace identifier for the key. Can only be
                          passed as a keyword argument.

        :type dataset_id: string
        :param dataset_id: The dataset ID associated with the key. Required,
                           unless the implicit dataset ID has been set. Can
                           only be passed as a keyword argument.

        :type parent: :class:`gcloud.datastore.key.Key`
        :param parent: The parent of the key. Can only be passed as a
                       keyword argument.
        """
        self._flat_path = path_args
        parent = self._parent = kwargs.get('parent')
        self._namespace = kwargs.get('namespace')
        dataset_id = kwargs.get('dataset_id')
        self._dataset_id = _validate_dataset_id(dataset_id, parent)
        # _flat_path, _parent, _namespace and _dataset_id must be set before
        # _combine_args() is called.
        self._path = self._combine_args()

    @staticmethod
    def _parse_path(path_args):
        """Parses positional arguments into key path with kinds and IDs.

        :type path_args: :class:`tuple`
        :param path_args: A tuple from positional arguments. Should be
                          alternating list of kinds (string) and id/name
                          parts (int or string).

        :rtype: list of dict
        :returns: A list of key parts with kind and id or name set.
        :raises: `ValueError` if there are no `path_args`, if one of the
                 kinds is not a string or if one of the IDs/names is not
                 a string or an integer.
        """
        if len(path_args) == 0:
            raise ValueError('Key path must not be empty.')

        kind_list = path_args[::2]
        id_or_name_list = path_args[1::2]
        # Dummy sentinel value to pad incomplete key to even length path.
        partial_ending = object()
        if len(path_args) % 2 == 1:
            id_or_name_list += (partial_ending,)

        result = []
        for kind, id_or_name in izip(kind_list, id_or_name_list):
            curr_key_part = {}
            if isinstance(kind, six.string_types):
                curr_key_part['kind'] = kind
            else:
                raise ValueError(kind, 'Kind was not a string.')

            if isinstance(id_or_name, six.string_types):
                curr_key_part['name'] = id_or_name
            elif isinstance(id_or_name, six.integer_types):
                curr_key_part['id'] = id_or_name
            elif id_or_name is not partial_ending:
                raise ValueError(id_or_name,
                                 'ID/name was not a string or integer.')

            result.append(curr_key_part)

        return result

    def _combine_args(self):
        """Sets protected data by combining raw data set from the constructor.

        If a _parent is set, updates the _flat_path and sets the
        _namespace and _dataset_id if not already set.

        :rtype: list of dict
        :returns: A list of key parts with kind and id or name set.
        :raises: `ValueError` if the parent key is not complete.
        """
        child_path = self._parse_path(self._flat_path)

        if self._parent is not None:
            if self._parent.is_partial:
                raise ValueError('Parent key must be complete.')

            # We know that _parent.path() will return a copy.
            child_path = self._parent.path + child_path
            self._flat_path = self._parent.flat_path + self._flat_path
            if (self._namespace is not None and
                    self._namespace != self._parent.namespace):
                raise ValueError('Child namespace must agree with parent\'s.')
            self._namespace = self._parent.namespace
            if (self._dataset_id is not None and
                    self._dataset_id != self._parent.dataset_id):
                raise ValueError('Child dataset ID must agree with parent\'s.')
            self._dataset_id = self._parent.dataset_id

        return child_path

    def _clone(self):
        """Duplicates the Key.

        Most attributes are simple types, so don't require copying. Other
        attributes like `parent` are long-lived and so we re-use them rather
        than creating copies.

        :rtype: :class:`gcloud.datastore.key.Key`
        :returns: A new `Key` instance with the same data as the current one.
        """
        return self.__class__(*self.flat_path, parent=self.parent,
                              dataset_id=self.dataset_id,
                              namespace=self.namespace)

    def completed_key(self, id_or_name):
        """Creates new key from existing partial key by adding final ID/name.

        :rtype: :class:`gcloud.datastore.key.Key`
        :returns: A new `Key` instance with the same data as the current one
                  and an extra ID or name added.
        :raises: `ValueError` if the current key is not partial or if
                 `id_or_name` is not a string or integer.
        """
        if not self.is_partial:
            raise ValueError('Only a partial key can be completed.')

        id_or_name_key = None
        if isinstance(id_or_name, six.string_types):
            id_or_name_key = 'name'
        elif isinstance(id_or_name, six.integer_types):
            id_or_name_key = 'id'
        else:
            raise ValueError(id_or_name,
                             'ID/name was not a string or integer.')

        new_key = self._clone()
        new_key._path[-1][id_or_name_key] = id_or_name
        new_key._flat_path += (id_or_name,)
        return new_key

    def to_protobuf(self):
        """Return a protobuf corresponding to the key.

        :rtype: :class:`gcloud.datastore.datastore_v1_pb2.Key`
        :returns: The Protobuf representing the key.
        """
        key = datastore_pb.Key()
        key.partition_id.dataset_id = self.dataset_id

        if self.namespace:
            key.partition_id.namespace = self.namespace

        for item in self.path:
            element = key.path_element.add()
            if 'kind' in item:
                element.kind = item['kind']
            if 'id' in item:
                element.id = item['id']
            if 'name' in item:
                element.name = item['name']

        return key

    def get(self, connection=None):
        """Retrieve entity corresponding to the curretn key.

        :type connection: :class:`gcloud.datastore.connection.Connection`
        :param connection: Optional connection used to connect to datastore.

        :rtype: :class:`gcloud.datastore.entity.Entity` or `NoneType`
        :returns: The requested entity, or ``None`` if there was no
                  match found.
        """
        # Temporary import hack until Dataset is removed in #477.
        from gcloud import datastore

        # We allow partial keys to attempt a get, the backend will fail.
        connection = connection or _implicit_environ.CONNECTION
        entities = datastore.get_entities(
            [self], connection=connection, dataset_id=self.dataset_id)

        if entities:
            result = entities[0]
            # We assume that the backend has not changed the key.
            result.key = self
            return result

    def delete(self, connection=None):
        """Delete the key in the Cloud Datastore.

        :type connection: :class:`gcloud.datastore.connection.Connection`
        :param connection: Optional connection used to connect to datastore.
        """
        # We allow partial keys to attempt a delete, the backend will fail.
        connection = connection or _implicit_environ.CONNECTION
        connection.delete_entities(
            dataset_id=self.dataset_id,
            key_pbs=[self.to_protobuf()],
        )

    @property
    def is_partial(self):
        """Boolean indicating if the key has an ID (or name).

        :rtype: :class:`bool`
        :returns: True if the last element of the key's path does not have
                  an 'id' or a 'name'.
        """
        return self.id_or_name is None

    @property
    def namespace(self):
        """Namespace getter.

        :rtype: :class:`str`
        :returns: The namespace of the current key.
        """
        return self._namespace

    @property
    def path(self):
        """Path getter.

        Returns a copy so that the key remains immutable.

        :rtype: :class:`str`
        :returns: The (key) path of the current key.
        """
        return copy.deepcopy(self._path)

    @property
    def flat_path(self):
        """Getter for the key path as a tuple.

        :rtype: :class:`tuple` of string and int
        :returns: The tuple of elements in the path.
        """
        return self._flat_path

    @property
    def kind(self):
        """Kind getter. Based on the last element of path.

        :rtype: :class:`str`
        :returns: The kind of the current key.
        """
        return self.path[-1]['kind']

    @property
    def id(self):
        """ID getter. Based on the last element of path.

        :rtype: :class:`int`
        :returns: The (integer) ID of the key.
        """
        return self.path[-1].get('id')

    @property
    def name(self):
        """Name getter. Based on the last element of path.

        :rtype: :class:`str`
        :returns: The (string) name of the key.
        """
        return self.path[-1].get('name')

    @property
    def id_or_name(self):
        """Getter. Based on the last element of path.

        :rtype: :class:`int` (if 'id') or :class:`str` (if 'name')
        :returns: The last element of the key's path if it is either an 'id'
                  or a 'name'.
        """
        return self.id or self.name

    @property
    def dataset_id(self):
        """Dataset ID getter.

        :rtype: :class:`str`
        :returns: The key's dataset ID.
        """
        return self._dataset_id

    def _make_parent(self):
        """Creates a parent key for the current path.

        Extracts all but the last element in the key path and creates a new
        key, while still matching the namespace and the dataset ID.

        :rtype: :class:`gcloud.datastore.key.Key` or `NoneType`
        :returns: a new `Key` instance, whose path consists of all but the last
                  element of self's path. If self has only one path element,
                  returns None.
        """
        if self.is_partial:
            parent_args = self.flat_path[:-1]
        else:
            parent_args = self.flat_path[:-2]
        if parent_args:
            return self.__class__(*parent_args, dataset_id=self.dataset_id,
                                  namespace=self.namespace)

    @property
    def parent(self):
        """The parent of the current key.

        :rtype: :class:`gcloud.datastore.key.Key` or `NoneType`
        :returns: a new `Key` instance, whose path consists of all but the last
                  element of self's path.  If self has only one path element,
                  returns None.
        """
        if self._parent is None:
            self._parent = self._make_parent()

        return self._parent

    def __repr__(self):
        return '<Key%s, dataset=%s>' % (self.path, self.dataset_id)


def _validate_dataset_id(dataset_id, parent):
    """Ensure the dataset ID is set appropriately.

    If ``parent`` is passed, skip the test (it will be checked / fixed up
    later).

    If ``dataset_id`` is unset, attempt to infer the ID from the environment.

    :raises: `ValueError` if ``dataset_id`` is None and none can be inferred.
    """
    if parent is None:

        if dataset_id is None:

            if _implicit_environ.DATASET_ID is None:
                raise ValueError("A Key must have a dataset ID set.")

            dataset_id = _implicit_environ.DATASET_ID

    return dataset_id
