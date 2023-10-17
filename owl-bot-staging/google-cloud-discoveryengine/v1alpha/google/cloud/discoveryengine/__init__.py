# -*- coding: utf-8 -*-
# Copyright 2023 Google LLC
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
#
from google.cloud.discoveryengine import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.discoveryengine_v1alpha.services.completion_service.client import CompletionServiceClient
from google.cloud.discoveryengine_v1alpha.services.completion_service.async_client import CompletionServiceAsyncClient
from google.cloud.discoveryengine_v1alpha.services.conversational_search_service.client import ConversationalSearchServiceClient
from google.cloud.discoveryengine_v1alpha.services.conversational_search_service.async_client import ConversationalSearchServiceAsyncClient
from google.cloud.discoveryengine_v1alpha.services.document_service.client import DocumentServiceClient
from google.cloud.discoveryengine_v1alpha.services.document_service.async_client import DocumentServiceAsyncClient
from google.cloud.discoveryengine_v1alpha.services.recommendation_service.client import RecommendationServiceClient
from google.cloud.discoveryengine_v1alpha.services.recommendation_service.async_client import RecommendationServiceAsyncClient
from google.cloud.discoveryengine_v1alpha.services.schema_service.client import SchemaServiceClient
from google.cloud.discoveryengine_v1alpha.services.schema_service.async_client import SchemaServiceAsyncClient
from google.cloud.discoveryengine_v1alpha.services.search_service.client import SearchServiceClient
from google.cloud.discoveryengine_v1alpha.services.search_service.async_client import SearchServiceAsyncClient
from google.cloud.discoveryengine_v1alpha.services.site_search_engine_service.client import SiteSearchEngineServiceClient
from google.cloud.discoveryengine_v1alpha.services.site_search_engine_service.async_client import SiteSearchEngineServiceAsyncClient
from google.cloud.discoveryengine_v1alpha.services.user_event_service.client import UserEventServiceClient
from google.cloud.discoveryengine_v1alpha.services.user_event_service.async_client import UserEventServiceAsyncClient

from google.cloud.discoveryengine_v1alpha.types.common import CustomAttribute
from google.cloud.discoveryengine_v1alpha.types.common import DoubleList
from google.cloud.discoveryengine_v1alpha.types.common import Interval
from google.cloud.discoveryengine_v1alpha.types.common import UserInfo
from google.cloud.discoveryengine_v1alpha.types.common import SolutionType
from google.cloud.discoveryengine_v1alpha.types.completion_service import CompleteQueryRequest
from google.cloud.discoveryengine_v1alpha.types.completion_service import CompleteQueryResponse
from google.cloud.discoveryengine_v1alpha.types.conversation import Conversation
from google.cloud.discoveryengine_v1alpha.types.conversation import ConversationContext
from google.cloud.discoveryengine_v1alpha.types.conversation import ConversationMessage
from google.cloud.discoveryengine_v1alpha.types.conversation import Reply
from google.cloud.discoveryengine_v1alpha.types.conversation import TextInput
from google.cloud.discoveryengine_v1alpha.types.conversational_search_service import ConverseConversationRequest
from google.cloud.discoveryengine_v1alpha.types.conversational_search_service import ConverseConversationResponse
from google.cloud.discoveryengine_v1alpha.types.conversational_search_service import CreateConversationRequest
from google.cloud.discoveryengine_v1alpha.types.conversational_search_service import DeleteConversationRequest
from google.cloud.discoveryengine_v1alpha.types.conversational_search_service import GetConversationRequest
from google.cloud.discoveryengine_v1alpha.types.conversational_search_service import ListConversationsRequest
from google.cloud.discoveryengine_v1alpha.types.conversational_search_service import ListConversationsResponse
from google.cloud.discoveryengine_v1alpha.types.conversational_search_service import UpdateConversationRequest
from google.cloud.discoveryengine_v1alpha.types.document import Document
from google.cloud.discoveryengine_v1alpha.types.document_service import CreateDocumentRequest
from google.cloud.discoveryengine_v1alpha.types.document_service import DeleteDocumentRequest
from google.cloud.discoveryengine_v1alpha.types.document_service import GetDocumentRequest
from google.cloud.discoveryengine_v1alpha.types.document_service import ListDocumentsRequest
from google.cloud.discoveryengine_v1alpha.types.document_service import ListDocumentsResponse
from google.cloud.discoveryengine_v1alpha.types.document_service import UpdateDocumentRequest
from google.cloud.discoveryengine_v1alpha.types.import_config import BigQuerySource
from google.cloud.discoveryengine_v1alpha.types.import_config import GcsSource
from google.cloud.discoveryengine_v1alpha.types.import_config import ImportDocumentsMetadata
from google.cloud.discoveryengine_v1alpha.types.import_config import ImportDocumentsRequest
from google.cloud.discoveryengine_v1alpha.types.import_config import ImportDocumentsResponse
from google.cloud.discoveryengine_v1alpha.types.import_config import ImportErrorConfig
from google.cloud.discoveryengine_v1alpha.types.import_config import ImportUserEventsMetadata
from google.cloud.discoveryengine_v1alpha.types.import_config import ImportUserEventsRequest
from google.cloud.discoveryengine_v1alpha.types.import_config import ImportUserEventsResponse
from google.cloud.discoveryengine_v1alpha.types.purge_config import PurgeDocumentsMetadata
from google.cloud.discoveryengine_v1alpha.types.purge_config import PurgeDocumentsRequest
from google.cloud.discoveryengine_v1alpha.types.purge_config import PurgeDocumentsResponse
from google.cloud.discoveryengine_v1alpha.types.purge_config import PurgeUserEventsMetadata
from google.cloud.discoveryengine_v1alpha.types.purge_config import PurgeUserEventsRequest
from google.cloud.discoveryengine_v1alpha.types.purge_config import PurgeUserEventsResponse
from google.cloud.discoveryengine_v1alpha.types.recommendation_service import RecommendRequest
from google.cloud.discoveryengine_v1alpha.types.recommendation_service import RecommendResponse
from google.cloud.discoveryengine_v1alpha.types.schema import FieldConfig
from google.cloud.discoveryengine_v1alpha.types.schema import Schema
from google.cloud.discoveryengine_v1alpha.types.schema_service import CreateSchemaMetadata
from google.cloud.discoveryengine_v1alpha.types.schema_service import CreateSchemaRequest
from google.cloud.discoveryengine_v1alpha.types.schema_service import DeleteSchemaMetadata
from google.cloud.discoveryengine_v1alpha.types.schema_service import DeleteSchemaRequest
from google.cloud.discoveryengine_v1alpha.types.schema_service import GetSchemaRequest
from google.cloud.discoveryengine_v1alpha.types.schema_service import ListSchemasRequest
from google.cloud.discoveryengine_v1alpha.types.schema_service import ListSchemasResponse
from google.cloud.discoveryengine_v1alpha.types.schema_service import UpdateSchemaMetadata
from google.cloud.discoveryengine_v1alpha.types.schema_service import UpdateSchemaRequest
from google.cloud.discoveryengine_v1alpha.types.search_service import SearchRequest
from google.cloud.discoveryengine_v1alpha.types.search_service import SearchResponse
from google.cloud.discoveryengine_v1alpha.types.site_search_engine_service import RecrawlUrisMetadata
from google.cloud.discoveryengine_v1alpha.types.site_search_engine_service import RecrawlUrisRequest
from google.cloud.discoveryengine_v1alpha.types.site_search_engine_service import RecrawlUrisResponse
from google.cloud.discoveryengine_v1alpha.types.user_event import CompletionInfo
from google.cloud.discoveryengine_v1alpha.types.user_event import DocumentInfo
from google.cloud.discoveryengine_v1alpha.types.user_event import MediaInfo
from google.cloud.discoveryengine_v1alpha.types.user_event import PageInfo
from google.cloud.discoveryengine_v1alpha.types.user_event import PanelInfo
from google.cloud.discoveryengine_v1alpha.types.user_event import SearchInfo
from google.cloud.discoveryengine_v1alpha.types.user_event import TransactionInfo
from google.cloud.discoveryengine_v1alpha.types.user_event import UserEvent
from google.cloud.discoveryengine_v1alpha.types.user_event_service import CollectUserEventRequest
from google.cloud.discoveryengine_v1alpha.types.user_event_service import WriteUserEventRequest

__all__ = ('CompletionServiceClient',
    'CompletionServiceAsyncClient',
    'ConversationalSearchServiceClient',
    'ConversationalSearchServiceAsyncClient',
    'DocumentServiceClient',
    'DocumentServiceAsyncClient',
    'RecommendationServiceClient',
    'RecommendationServiceAsyncClient',
    'SchemaServiceClient',
    'SchemaServiceAsyncClient',
    'SearchServiceClient',
    'SearchServiceAsyncClient',
    'SiteSearchEngineServiceClient',
    'SiteSearchEngineServiceAsyncClient',
    'UserEventServiceClient',
    'UserEventServiceAsyncClient',
    'CustomAttribute',
    'DoubleList',
    'Interval',
    'UserInfo',
    'SolutionType',
    'CompleteQueryRequest',
    'CompleteQueryResponse',
    'Conversation',
    'ConversationContext',
    'ConversationMessage',
    'Reply',
    'TextInput',
    'ConverseConversationRequest',
    'ConverseConversationResponse',
    'CreateConversationRequest',
    'DeleteConversationRequest',
    'GetConversationRequest',
    'ListConversationsRequest',
    'ListConversationsResponse',
    'UpdateConversationRequest',
    'Document',
    'CreateDocumentRequest',
    'DeleteDocumentRequest',
    'GetDocumentRequest',
    'ListDocumentsRequest',
    'ListDocumentsResponse',
    'UpdateDocumentRequest',
    'BigQuerySource',
    'GcsSource',
    'ImportDocumentsMetadata',
    'ImportDocumentsRequest',
    'ImportDocumentsResponse',
    'ImportErrorConfig',
    'ImportUserEventsMetadata',
    'ImportUserEventsRequest',
    'ImportUserEventsResponse',
    'PurgeDocumentsMetadata',
    'PurgeDocumentsRequest',
    'PurgeDocumentsResponse',
    'PurgeUserEventsMetadata',
    'PurgeUserEventsRequest',
    'PurgeUserEventsResponse',
    'RecommendRequest',
    'RecommendResponse',
    'FieldConfig',
    'Schema',
    'CreateSchemaMetadata',
    'CreateSchemaRequest',
    'DeleteSchemaMetadata',
    'DeleteSchemaRequest',
    'GetSchemaRequest',
    'ListSchemasRequest',
    'ListSchemasResponse',
    'UpdateSchemaMetadata',
    'UpdateSchemaRequest',
    'SearchRequest',
    'SearchResponse',
    'RecrawlUrisMetadata',
    'RecrawlUrisRequest',
    'RecrawlUrisResponse',
    'CompletionInfo',
    'DocumentInfo',
    'MediaInfo',
    'PageInfo',
    'PanelInfo',
    'SearchInfo',
    'TransactionInfo',
    'UserEvent',
    'CollectUserEventRequest',
    'WriteUserEventRequest',
)
