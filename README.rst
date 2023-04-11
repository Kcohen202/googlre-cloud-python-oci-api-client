Google Cloud Python Client
==========================

Python idiomatic clients for `Google Cloud Platform`_ services.

.. _Google Cloud Platform: https://cloud.google.com/


Stability levels
*******************

The `development status classifier`_ on PyPI indicates the current stability
of a package.

.. _development status classifier: https://pypi.org/classifiers/

General Availability
--------------------

**GA** (general availability) indicates that the client library for a
particular service is stable, and that the code surface will not change in
backwards-incompatible ways unless either absolutely necessary (e.g. because
of critical security issues) or with an extensive deprecation period.
Issues and requests against GA libraries are addressed with the highest
priority.

GA libraries have development status classifier ``Development Status :: 5 - Production/Stable``.

.. note::

    Sub-components of GA libraries explicitly marked as beta in the
    import path (e.g. ``google.cloud.language_v1beta2``) should be considered
    to be beta.

Beta Support
------------

**Beta** indicates that the client library for a particular service is
mostly stable and is being prepared for release. Issues and requests
against beta libraries are addressed with a higher priority.

Beta libraries have development status classifier ``Development Status :: 4 - Beta``.

Alpha Support
-------------

**Alpha** indicates that the client library for a particular service is
still a work-in-progress and is more likely to get backwards-incompatible
updates. See `versioning`_ for more details.


Alpha libraries have development status classifier ``Development Status :: 3 - Alpha``.

If you need support for other Google APIs, check out the
`Google APIs Python Client library`_.

.. _Google APIs Python Client library: https://github.com/google/google-api-python-client


Libraries
*********

.. This table is generated, see synth.py for details.

.. API_TABLE_START

.. list-table::
   :header-rows: 1

   * - Client
     - Release Level
     - Version
   * - `AI Platform <https://github.com/googleapis/python-aiplatform>`_
     - |stable|
     - |PyPI-google-cloud-aiplatform|
   * - `AI Platform Notebooks <https://github.com/googleapis/python-notebooks>`_
     - |stable|
     - |PyPI-google-cloud-notebooks|
   * - `Access Approval <https://github.com/googleapis/python-access-approval>`_
     - |stable|
     - |PyPI-google-cloud-access-approval|
   * - `Artifact Registry <https://github.com/googleapis/python-artifact-registry>`_
     - |stable|
     - |PyPI-google-cloud-artifact-registry|
   * - `Asset Inventory <https://github.com/googleapis/python-asset>`_
     - |stable|
     - |PyPI-google-cloud-asset|
   * - `AutoML <https://github.com/googleapis/python-automl>`_
     - |stable|
     - |PyPI-google-cloud-automl|
   * - `BigQuery <https://github.com/googleapis/python-bigquery>`_
     - |stable|
     - |PyPI-google-cloud-bigquery|
   * - `BigQuery Connection <https://github.com/googleapis/python-bigquery-connection>`_
     - |stable|
     - |PyPI-google-cloud-bigquery-connection|
   * - `BigQuery Data Transfer <https://github.com/googleapis/python-bigquery-datatransfer>`_
     - |stable|
     - |PyPI-google-cloud-bigquery-datatransfer|
   * - `BigQuery Logging Protos <https://github.com/googleapis/python-bigquery-logging>`_
     - |stable|
     - |PyPI-google-cloud-bigquery-logging|
   * - `BigQuery Reservation <https://github.com/googleapis/python-bigquery-reservation>`_
     - |stable|
     - |PyPI-google-cloud-bigquery-reservation|
   * - `BigQuery Storage <https://github.com/googleapis/python-bigquery-storage>`_
     - |stable|
     - |PyPI-google-cloud-bigquery-storage|
   * - `Bigtable <https://github.com/googleapis/python-bigtable>`_
     - |stable|
     - |PyPI-google-cloud-bigtable|
   * - `Billing <https://github.com/googleapis/python-billing>`_
     - |stable|
     - |PyPI-google-cloud-billing|
   * - `Billing Budget <https://github.com/googleapis/python-billingbudgets>`_
     - |stable|
     - |PyPI-google-cloud-billing-budgets|
   * - `Build <https://github.com/googleapis/python-cloudbuild>`_
     - |stable|
     - |PyPI-google-cloud-build|
   * - `Compute Engine <https://github.com/googleapis/python-compute>`_
     - |stable|
     - |PyPI-google-cloud-compute|
   * - `Contact Center AI Insights <https://github.com/googleapis/python-contact-center-insights>`_
     - |stable|
     - |PyPI-google-cloud-contact-center-insights|
   * - `Container Analysis <https://github.com/googleapis/python-containeranalysis>`_
     - |stable|
     - |PyPI-google-cloud-containeranalysis|
   * - `Data Catalog <https://github.com/googleapis/python-datacatalog>`_
     - |stable|
     - |PyPI-google-cloud-datacatalog|
   * - `Data Loss Prevention <https://github.com/googleapis/python-dlp>`_
     - |stable|
     - |PyPI-google-cloud-dlp|
   * - `Database Migration Service <https://github.com/googleapis/python-dms>`_
     - |stable|
     - |PyPI-google-cloud-dms|
   * - `Dataproc <https://github.com/googleapis/python-dataproc>`_
     - |stable|
     - |PyPI-google-cloud-dataproc|
   * - `Datastore <https://github.com/googleapis/python-datastore>`_
     - |stable|
     - |PyPI-google-cloud-datastore|
   * - `Deploy <https://github.com/googleapis/python-deploy>`_
     - |stable|
     - |PyPI-google-cloud-deploy|
   * - `Dialogflow <https://github.com/googleapis/python-dialogflow>`_
     - |stable|
     - |PyPI-google-cloud-dialogflow|
   * - `Dialogflow CX <https://github.com/googleapis/python-dialogflow-cx>`_
     - |stable|
     - |PyPI-google-cloud-dialogflow-cx|
   * - `Document AI <https://github.com/googleapis/python-documentai>`_
     - |stable|
     - |PyPI-google-cloud-documentai|
   * - `Firestore <https://github.com/googleapis/python-firestore>`_
     - |stable|
     - |PyPI-google-cloud-firestore|
   * - `Functions <https://github.com/googleapis/python-functions>`_
     - |stable|
     - |PyPI-google-cloud-functions|
   * - `Game Servers <https://github.com/googleapis/python-game-servers>`_
     - |stable|
     - |PyPI-google-cloud-game-servers|
   * - `Grafeas <https://github.com/googleapis/python-grafeas>`_
     - |stable|
     - |PyPI-grafeas|
   * - `Identity and Access Management <https://github.com/googleapis/python-iam>`_
     - |stable|
     - |PyPI-google-cloud-iam|
   * - `Internet of Things (IoT) Core <https://github.com/googleapis/python-iot>`_
     - |stable|
     - |PyPI-google-cloud-iot|
   * - `Key Management Service <https://github.com/googleapis/python-kms>`_
     - |stable|
     - |PyPI-google-cloud-kms|
   * - `Kubernetes Engine <https://github.com/googleapis/python-container>`_
     - |stable|
     - |PyPI-google-cloud-container|
   * - `Logging <https://github.com/googleapis/python-logging>`_
     - |stable|
     - |PyPI-google-cloud-logging|
   * - `Memorystore for Memcached <https://github.com/googleapis/python-memcache>`_
     - |stable|
     - |PyPI-google-cloud-memcache|
   * - `Monitoring Dashboards <https://github.com/googleapis/python-monitoring-dashboards>`_
     - |stable|
     - |PyPI-google-cloud-monitoring-dashboards|
   * - `NDB Client Library for Datastore <https://github.com/googleapis/python-ndb>`_
     - |stable|
     - |PyPI-google-cloud-ndb|
   * - `Natural Language <https://github.com/googleapis/python-language>`_
     - |stable|
     - |PyPI-google-cloud-language|
   * - `OS Login <https://github.com/googleapis/python-oslogin>`_
     - |stable|
     - |PyPI-google-cloud-os-login|
   * - `Private Certificate Authority <https://github.com/googleapis/python-security-private-ca>`_
     - |stable|
     - |PyPI-google-cloud-private-ca|
   * - `Pub/Sub <https://github.com/googleapis/python-pubsub>`_
     - |stable|
     - |PyPI-google-cloud-pubsub|
   * - `Pub/Sub Lite <https://github.com/googleapis/python-pubsublite>`_
     - |stable|
     - |PyPI-google-cloud-pubsublite|
   * - `Recommender <https://github.com/googleapis/python-recommender>`_
     - |stable|
     - |PyPI-google-cloud-recommender|
   * - `Redis <https://github.com/googleapis/python-redis>`_
     - |stable|
     - |PyPI-google-cloud-redis|
   * - `Resource Manager <https://github.com/googleapis/python-resource-manager>`_
     - |stable|
     - |PyPI-google-cloud-resource-manager|
   * - `Retail <https://github.com/googleapis/python-retail>`_
     - |stable|
     - |PyPI-google-cloud-retail|
   * - `Scheduler <https://github.com/googleapis/python-scheduler>`_
     - |stable|
     - |PyPI-google-cloud-scheduler|
   * - `Secret Manager <https://github.com/googleapis/python-secret-manager>`_
     - |stable|
     - |PyPI-google-cloud-secret-manager|
   * - `Security Command Center <https://github.com/googleapis/python-securitycenter>`_
     - |stable|
     - |PyPI-google-cloud-securitycenter|
   * - `Security Scanner <https://github.com/googleapis/python-websecurityscanner>`_
     - |stable|
     - |PyPI-google-cloud-websecurityscanner|
   * - `Service Management <https://github.com/googleapis/python-service-management>`_
     - |stable|
     - |PyPI-google-cloud-service-management|
   * - `Spanner <https://github.com/googleapis/python-spanner>`_
     - |stable|
     - |PyPI-google-cloud-spanner|
   * - `Spanner Django <https://github.com/googleapis/python-spanner-django>`_
     - |stable|
     - |PyPI-django-google-spanner|
   * - `Speech <https://github.com/googleapis/python-speech>`_
     - |stable|
     - |PyPI-google-cloud-speech|
   * - `Stackdriver Monitoring <https://github.com/googleapis/python-monitoring>`_
     - |stable|
     - |PyPI-google-cloud-monitoring|
   * - `Storage <https://github.com/googleapis/python-storage>`_
     - |stable|
     - |PyPI-google-cloud-storage|
   * - `Talent Solution <https://github.com/googleapis/python-talent>`_
     - |stable|
     - |PyPI-google-cloud-talent|
   * - `Tasks <https://github.com/googleapis/python-tasks>`_
     - |stable|
     - |PyPI-google-cloud-tasks|
   * - `Text-to-Speech <https://github.com/googleapis/python-texttospeech>`_
     - |stable|
     - |PyPI-google-cloud-texttospeech|
   * - `Trace <https://github.com/googleapis/python-trace>`_
     - |stable|
     - |PyPI-google-cloud-trace|
   * - `Translation <https://github.com/googleapis/python-translate>`_
     - |stable|
     - |PyPI-google-cloud-translate|
   * - `Video Intelligence <https://github.com/googleapis/python-videointelligence>`_
     - |stable|
     - |PyPI-google-cloud-videointelligence|
   * - `Vision <https://github.com/googleapis/python-vision>`_
     - |stable|
     - |PyPI-google-cloud-vision|
   * - `Web Risk <https://github.com/googleapis/python-webrisk>`_
     - |stable|
     - |PyPI-google-cloud-webrisk|
   * - `Workflows <https://github.com/googleapis/python-workflows>`_
     - |stable|
     - |PyPI-google-cloud-workflows|
   * - `reCAPTCHA Enterprise <https://github.com/googleapis/python-recaptcha-enterprise>`_
     - |stable|
     - |PyPI-google-cloud-recaptcha-enterprise|
   * - `Analytics Admin <https://github.com/googleapis/python-analytics-admin>`_
     - |preview|
     - |PyPI-google-analytics-admin|
   * - `Analytics Data <https://github.com/googleapis/python-analytics-data>`_
     - |preview|
     - |PyPI-google-analytics-data|
   * - `Area 120 Tables <https://github.com/googleapis/python-area120-tables>`_
     - |preview|
     - |PyPI-google-area120-tables|
   * - `BigQuery Migration <https://github.com/googleapis/python-bigquery-migration>`_
     - |preview|
     - |PyPI-google-cloud-bigquery-migration|
   * - `BigQuery connector for pandas <https://github.com/googleapis/python-bigquery-pandas>`_
     - |preview|
     - |PyPI-pandas-gbq|
   * - `DNS <https://github.com/googleapis/python-dns>`_
     - |preview|
     - |PyPI-google-cloud-dns|
   * - `Data Labeling <https://github.com/googleapis/python-datalabeling>`_
     - |preview|
     - |PyPI-google-cloud-datalabeling|
   * - `Dataflow <https://github.com/googleapis/python-dataflow-client>`_
     - |preview|
     - |PyPI-google-cloud-dataflow-client|
   * - `Error Reporting <https://github.com/googleapis/python-error-reporting>`_
     - |preview|
     - |PyPI-google-cloud-error-reporting|
   * - `Media Translation <https://github.com/googleapis/python-media-translation>`_
     - |preview|
     - |PyPI-google-cloud-media-translation|
   * - `Phishing Protection <https://github.com/googleapis/python-phishingprotection>`_
     - |preview|
     - |PyPI-google-cloud-phishing-protection|
   * - `Recommendations AI <https://github.com/googleapis/python-recommendations-ai>`_
     - |preview|
     - |PyPI-google-cloud-recommendations-ai|
   * - `Runtime Configurator <https://github.com/googleapis/python-runtimeconfig>`_
     - |preview|
     - |PyPI-google-cloud-runtimeconfig|
   * - `SQLAlchemy dialect for BigQuery <https://github.com/googleapis/python-bigquery-sqlalchemy>`_
     - |preview|
     - |PyPI-sqlalchemy-bigquery|

.. |PyPI-google-cloud-aiplatform| image:: https://img.shields.io/pypi/v/google-cloud-aiplatform.svg
     :target: https://pypi.org/project/google-cloud-aiplatform
.. |PyPI-google-cloud-notebooks| image:: https://img.shields.io/pypi/v/google-cloud-notebooks.svg
     :target: https://pypi.org/project/google-cloud-notebooks
.. |PyPI-google-cloud-access-approval| image:: https://img.shields.io/pypi/v/google-cloud-access-approval.svg
     :target: https://pypi.org/project/google-cloud-access-approval
.. |PyPI-google-cloud-artifact-registry| image:: https://img.shields.io/pypi/v/google-cloud-artifact-registry.svg
     :target: https://pypi.org/project/google-cloud-artifact-registry
.. |PyPI-google-cloud-asset| image:: https://img.shields.io/pypi/v/google-cloud-asset.svg
     :target: https://pypi.org/project/google-cloud-asset
.. |PyPI-google-cloud-automl| image:: https://img.shields.io/pypi/v/google-cloud-automl.svg
     :target: https://pypi.org/project/google-cloud-automl
.. |PyPI-google-cloud-bigquery| image:: https://img.shields.io/pypi/v/google-cloud-bigquery.svg
     :target: https://pypi.org/project/google-cloud-bigquery
.. |PyPI-google-cloud-bigquery-connection| image:: https://img.shields.io/pypi/v/google-cloud-bigquery-connection.svg
     :target: https://pypi.org/project/google-cloud-bigquery-connection
.. |PyPI-google-cloud-bigquery-datatransfer| image:: https://img.shields.io/pypi/v/google-cloud-bigquery-datatransfer.svg
     :target: https://pypi.org/project/google-cloud-bigquery-datatransfer
.. |PyPI-google-cloud-bigquery-logging| image:: https://img.shields.io/pypi/v/google-cloud-bigquery-logging.svg
     :target: https://pypi.org/project/google-cloud-bigquery-logging
.. |PyPI-google-cloud-bigquery-reservation| image:: https://img.shields.io/pypi/v/google-cloud-bigquery-reservation.svg
     :target: https://pypi.org/project/google-cloud-bigquery-reservation
.. |PyPI-google-cloud-bigquery-storage| image:: https://img.shields.io/pypi/v/google-cloud-bigquery-storage.svg
     :target: https://pypi.org/project/google-cloud-bigquery-storage
.. |PyPI-google-cloud-bigtable| image:: https://img.shields.io/pypi/v/google-cloud-bigtable.svg
     :target: https://pypi.org/project/google-cloud-bigtable
.. |PyPI-google-cloud-billing| image:: https://img.shields.io/pypi/v/google-cloud-billing.svg
     :target: https://pypi.org/project/google-cloud-billing
.. |PyPI-google-cloud-billing-budgets| image:: https://img.shields.io/pypi/v/google-cloud-billing-budgets.svg
     :target: https://pypi.org/project/google-cloud-billing-budgets
.. |PyPI-google-cloud-build| image:: https://img.shields.io/pypi/v/google-cloud-build.svg
     :target: https://pypi.org/project/google-cloud-build
.. |PyPI-google-cloud-compute| image:: https://img.shields.io/pypi/v/google-cloud-compute.svg
     :target: https://pypi.org/project/google-cloud-compute
.. |PyPI-google-cloud-contact-center-insights| image:: https://img.shields.io/pypi/v/google-cloud-contact-center-insights.svg
     :target: https://pypi.org/project/google-cloud-contact-center-insights
.. |PyPI-google-cloud-containeranalysis| image:: https://img.shields.io/pypi/v/google-cloud-containeranalysis.svg
     :target: https://pypi.org/project/google-cloud-containeranalysis
.. |PyPI-google-cloud-datacatalog| image:: https://img.shields.io/pypi/v/google-cloud-datacatalog.svg
     :target: https://pypi.org/project/google-cloud-datacatalog
.. |PyPI-google-cloud-dlp| image:: https://img.shields.io/pypi/v/google-cloud-dlp.svg
     :target: https://pypi.org/project/google-cloud-dlp
.. |PyPI-google-cloud-dms| image:: https://img.shields.io/pypi/v/google-cloud-dms.svg
     :target: https://pypi.org/project/google-cloud-dms
.. |PyPI-google-cloud-dataproc| image:: https://img.shields.io/pypi/v/google-cloud-dataproc.svg
     :target: https://pypi.org/project/google-cloud-dataproc
.. |PyPI-google-cloud-datastore| image:: https://img.shields.io/pypi/v/google-cloud-datastore.svg
     :target: https://pypi.org/project/google-cloud-datastore
.. |PyPI-google-cloud-deploy| image:: https://img.shields.io/pypi/v/google-cloud-deploy.svg
     :target: https://pypi.org/project/google-cloud-deploy
.. |PyPI-google-cloud-dialogflow| image:: https://img.shields.io/pypi/v/google-cloud-dialogflow.svg
     :target: https://pypi.org/project/google-cloud-dialogflow
.. |PyPI-google-cloud-dialogflow-cx| image:: https://img.shields.io/pypi/v/google-cloud-dialogflow-cx.svg
     :target: https://pypi.org/project/google-cloud-dialogflow-cx
.. |PyPI-google-cloud-documentai| image:: https://img.shields.io/pypi/v/google-cloud-documentai.svg
     :target: https://pypi.org/project/google-cloud-documentai
.. |PyPI-google-cloud-firestore| image:: https://img.shields.io/pypi/v/google-cloud-firestore.svg
     :target: https://pypi.org/project/google-cloud-firestore
.. |PyPI-google-cloud-functions| image:: https://img.shields.io/pypi/v/google-cloud-functions.svg
     :target: https://pypi.org/project/google-cloud-functions
.. |PyPI-google-cloud-game-servers| image:: https://img.shields.io/pypi/v/google-cloud-game-servers.svg
     :target: https://pypi.org/project/google-cloud-game-servers
.. |PyPI-grafeas| image:: https://img.shields.io/pypi/v/grafeas.svg
     :target: https://pypi.org/project/grafeas
.. |PyPI-google-cloud-iam| image:: https://img.shields.io/pypi/v/google-cloud-iam.svg
     :target: https://pypi.org/project/google-cloud-iam
.. |PyPI-google-cloud-iot| image:: https://img.shields.io/pypi/v/google-cloud-iot.svg
     :target: https://pypi.org/project/google-cloud-iot
.. |PyPI-google-cloud-kms| image:: https://img.shields.io/pypi/v/google-cloud-kms.svg
     :target: https://pypi.org/project/google-cloud-kms
.. |PyPI-google-cloud-container| image:: https://img.shields.io/pypi/v/google-cloud-container.svg
     :target: https://pypi.org/project/google-cloud-container
.. |PyPI-google-cloud-logging| image:: https://img.shields.io/pypi/v/google-cloud-logging.svg
     :target: https://pypi.org/project/google-cloud-logging
.. |PyPI-google-cloud-memcache| image:: https://img.shields.io/pypi/v/google-cloud-memcache.svg
     :target: https://pypi.org/project/google-cloud-memcache
.. |PyPI-google-cloud-monitoring-dashboards| image:: https://img.shields.io/pypi/v/google-cloud-monitoring-dashboards.svg
     :target: https://pypi.org/project/google-cloud-monitoring-dashboards
.. |PyPI-google-cloud-ndb| image:: https://img.shields.io/pypi/v/google-cloud-ndb.svg
     :target: https://pypi.org/project/google-cloud-ndb
.. |PyPI-google-cloud-language| image:: https://img.shields.io/pypi/v/google-cloud-language.svg
     :target: https://pypi.org/project/google-cloud-language
.. |PyPI-google-cloud-os-login| image:: https://img.shields.io/pypi/v/google-cloud-os-login.svg
     :target: https://pypi.org/project/google-cloud-os-login
.. |PyPI-google-cloud-private-ca| image:: https://img.shields.io/pypi/v/google-cloud-private-ca.svg
     :target: https://pypi.org/project/google-cloud-private-ca
.. |PyPI-google-cloud-pubsub| image:: https://img.shields.io/pypi/v/google-cloud-pubsub.svg
     :target: https://pypi.org/project/google-cloud-pubsub
.. |PyPI-google-cloud-pubsublite| image:: https://img.shields.io/pypi/v/google-cloud-pubsublite.svg
     :target: https://pypi.org/project/google-cloud-pubsublite
.. |PyPI-google-cloud-recommender| image:: https://img.shields.io/pypi/v/google-cloud-recommender.svg
     :target: https://pypi.org/project/google-cloud-recommender
.. |PyPI-google-cloud-redis| image:: https://img.shields.io/pypi/v/google-cloud-redis.svg
     :target: https://pypi.org/project/google-cloud-redis
.. |PyPI-google-cloud-resource-manager| image:: https://img.shields.io/pypi/v/google-cloud-resource-manager.svg
     :target: https://pypi.org/project/google-cloud-resource-manager
.. |PyPI-google-cloud-retail| image:: https://img.shields.io/pypi/v/google-cloud-retail.svg
     :target: https://pypi.org/project/google-cloud-retail
.. |PyPI-google-cloud-scheduler| image:: https://img.shields.io/pypi/v/google-cloud-scheduler.svg
     :target: https://pypi.org/project/google-cloud-scheduler
.. |PyPI-google-cloud-secret-manager| image:: https://img.shields.io/pypi/v/google-cloud-secret-manager.svg
     :target: https://pypi.org/project/google-cloud-secret-manager
.. |PyPI-google-cloud-securitycenter| image:: https://img.shields.io/pypi/v/google-cloud-securitycenter.svg
     :target: https://pypi.org/project/google-cloud-securitycenter
.. |PyPI-google-cloud-websecurityscanner| image:: https://img.shields.io/pypi/v/google-cloud-websecurityscanner.svg
     :target: https://pypi.org/project/google-cloud-websecurityscanner
.. |PyPI-google-cloud-service-management| image:: https://img.shields.io/pypi/v/google-cloud-service-management.svg
     :target: https://pypi.org/project/google-cloud-service-management
.. |PyPI-google-cloud-spanner| image:: https://img.shields.io/pypi/v/google-cloud-spanner.svg
     :target: https://pypi.org/project/google-cloud-spanner
.. |PyPI-django-google-spanner| image:: https://img.shields.io/pypi/v/django-google-spanner.svg
     :target: https://pypi.org/project/django-google-spanner
.. |PyPI-google-cloud-speech| image:: https://img.shields.io/pypi/v/google-cloud-speech.svg
     :target: https://pypi.org/project/google-cloud-speech
.. |PyPI-google-cloud-monitoring| image:: https://img.shields.io/pypi/v/google-cloud-monitoring.svg
     :target: https://pypi.org/project/google-cloud-monitoring
.. |PyPI-google-cloud-storage| image:: https://img.shields.io/pypi/v/google-cloud-storage.svg
     :target: https://pypi.org/project/google-cloud-storage
.. |PyPI-google-cloud-talent| image:: https://img.shields.io/pypi/v/google-cloud-talent.svg
     :target: https://pypi.org/project/google-cloud-talent
.. |PyPI-google-cloud-tasks| image:: https://img.shields.io/pypi/v/google-cloud-tasks.svg
     :target: https://pypi.org/project/google-cloud-tasks
.. |PyPI-google-cloud-texttospeech| image:: https://img.shields.io/pypi/v/google-cloud-texttospeech.svg
     :target: https://pypi.org/project/google-cloud-texttospeech
.. |PyPI-google-cloud-trace| image:: https://img.shields.io/pypi/v/google-cloud-trace.svg
     :target: https://pypi.org/project/google-cloud-trace
.. |PyPI-google-cloud-translate| image:: https://img.shields.io/pypi/v/google-cloud-translate.svg
     :target: https://pypi.org/project/google-cloud-translate
.. |PyPI-google-cloud-videointelligence| image:: https://img.shields.io/pypi/v/google-cloud-videointelligence.svg
     :target: https://pypi.org/project/google-cloud-videointelligence
.. |PyPI-google-cloud-vision| image:: https://img.shields.io/pypi/v/google-cloud-vision.svg
     :target: https://pypi.org/project/google-cloud-vision
.. |PyPI-google-cloud-webrisk| image:: https://img.shields.io/pypi/v/google-cloud-webrisk.svg
     :target: https://pypi.org/project/google-cloud-webrisk
.. |PyPI-google-cloud-workflows| image:: https://img.shields.io/pypi/v/google-cloud-workflows.svg
     :target: https://pypi.org/project/google-cloud-workflows
.. |PyPI-google-cloud-recaptcha-enterprise| image:: https://img.shields.io/pypi/v/google-cloud-recaptcha-enterprise.svg
     :target: https://pypi.org/project/google-cloud-recaptcha-enterprise
.. |PyPI-google-analytics-admin| image:: https://img.shields.io/pypi/v/google-analytics-admin.svg
     :target: https://pypi.org/project/google-analytics-admin
.. |PyPI-google-analytics-data| image:: https://img.shields.io/pypi/v/google-analytics-data.svg
     :target: https://pypi.org/project/google-analytics-data
.. |PyPI-google-area120-tables| image:: https://img.shields.io/pypi/v/google-area120-tables.svg
     :target: https://pypi.org/project/google-area120-tables
.. |PyPI-google-cloud-bigquery-migration| image:: https://img.shields.io/pypi/v/google-cloud-bigquery-migration.svg
     :target: https://pypi.org/project/google-cloud-bigquery-migration
.. |PyPI-pandas-gbq| image:: https://img.shields.io/pypi/v/pandas-gbq.svg
     :target: https://pypi.org/project/pandas-gbq
.. |PyPI-google-cloud-dns| image:: https://img.shields.io/pypi/v/google-cloud-dns.svg
     :target: https://pypi.org/project/google-cloud-dns
.. |PyPI-google-cloud-datalabeling| image:: https://img.shields.io/pypi/v/google-cloud-datalabeling.svg
     :target: https://pypi.org/project/google-cloud-datalabeling
.. |PyPI-google-cloud-dataflow-client| image:: https://img.shields.io/pypi/v/google-cloud-dataflow-client.svg
     :target: https://pypi.org/project/google-cloud-dataflow-client
.. |PyPI-google-cloud-error-reporting| image:: https://img.shields.io/pypi/v/google-cloud-error-reporting.svg
     :target: https://pypi.org/project/google-cloud-error-reporting
.. |PyPI-google-cloud-media-translation| image:: https://img.shields.io/pypi/v/google-cloud-media-translation.svg
     :target: https://pypi.org/project/google-cloud-media-translation
.. |PyPI-google-cloud-phishing-protection| image:: https://img.shields.io/pypi/v/google-cloud-phishing-protection.svg
     :target: https://pypi.org/project/google-cloud-phishing-protection
.. |PyPI-google-cloud-recommendations-ai| image:: https://img.shields.io/pypi/v/google-cloud-recommendations-ai.svg
     :target: https://pypi.org/project/google-cloud-recommendations-ai
.. |PyPI-google-cloud-runtimeconfig| image:: https://img.shields.io/pypi/v/google-cloud-runtimeconfig.svg
     :target: https://pypi.org/project/google-cloud-runtimeconfig
.. |PyPI-sqlalchemy-bigquery| image:: https://img.shields.io/pypi/v/sqlalchemy-bigquery.svg
     :target: https://pypi.org/project/sqlalchemy-bigquery

.. API_TABLE_END

.. |ga| image:: https://img.shields.io/badge/support-GA-gold.svg
   :target: https://github.com/googleapis/google-cloud-python/blob/main/README.rst#general-availability

.. |beta| image:: https://img.shields.io/badge/support-beta-orange.svg
   :target: https://github.com/googleapis/google-cloud-python/blob/main/README.rst#beta-support


.. |alpha| image:: https://img.shields.io/badge/support-alpha-orange.svg
   :target: https://github.com/googleapis/google-cloud-python/blob/main/README.rst#alpha-support


Example Applications
********************

-  `getting-started-python`_ - A sample and `tutorial`_ that demonstrates how to build a complete web application using Cloud Datastore, Cloud Storage, and Cloud Pub/Sub and deploy it to Google App Engine or Google Compute Engine.
-  `google-cloud-python-expenses-demo`_ - A sample expenses demo using Cloud Datastore and Cloud Storage.

.. _getting-started-python: https://github.com/GoogleCloudPlatform/getting-started-python
.. _tutorial: https://cloud.google.com/python
.. _google-cloud-python-expenses-demo: https://github.com/GoogleCloudPlatform/google-cloud-python-expenses-demo


Authentication
********************


With ``google-cloud-python`` we try to make authentication as painless as possible.
Check out the `Getting started with authentication`_ in our documentation to learn more.

.. _Getting started with authentication: https://cloud.google.com/docs/authentication/getting-started



License
********************


Apache 2.0 - See `the LICENSE`_ for more information.

.. _the LICENSE: https://github.com/googleapis/google-cloud-python/blob/main/LICENSE
