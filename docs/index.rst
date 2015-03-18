.. toctree::
  :maxdepth: 0
  :hidden:

  gcloud-api
  datastore-api
  datastore-entities
  datastore-keys
  datastore-queries
  datastore-transactions
  datastore-batches
  datastore-dataset
  storage-api
  storage-blobs
  storage-buckets
  storage-acl
  pubsub-api


Getting started
---------------

.. include:: _components/getting-started.rst

Cloud Datastore
~~~~~~~~~~~~~~~

`Google Cloud Datastore`_ is a fully managed, schemaless database for storing non-relational data.

.. _Google Cloud Datastore: https://developers.google.com/datastore/

.. code-block:: python

  from gcloud import datastore

  entity = datastore.Entity(key=datastore.Key('Person'))
  entity['name'] = 'Your name'
  entity['age'] = 25
  datastore.put([entity])

Cloud Storage
~~~~~~~~~~~~~

`Google Cloud Storage`_ allows you to store data on Google infrastructure.

.. _Google Cloud Storage: https://developers.google.com/storage/

.. code-block:: python

  from gcloud import storage
  storage.set_defaults()
  bucket = storage.get_bucket('<your-bucket-name>')
  blob = storage.Blob('my-test-file.txt', bucket=bucket)
  blob = blob.upload_contents_from_string('this is test content!')
