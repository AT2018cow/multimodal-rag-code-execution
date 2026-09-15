import os
from dotenv import load_dotenv
load_dotenv()

DI_ENDPOINT = os.environ.get('DI_ENDPOINT', '')
DI_KEY = os.environ.get('DI_KEY', '')
DI_API_VERSION  = os.environ.get('DI_API_VERSION', '')

AZURE_OPENAI_RESOURCE = os.environ.get('AZURE_OPENAI_RESOURCE', '')
AZURE_OPENAI_KEY = os.environ.get('AZURE_OPENAI_KEY', "2024-02-29-preview")

AZURE_OPENAI_RESOURCE_1 = os.environ.get('AZURE_OPENAI_RESOURCE_1', '')
AZURE_OPENAI_KEY_1 = os.environ.get('AZURE_OPENAI_KEY_1', '')

AZURE_OPENAI_RESOURCE_2 = os.environ.get('AZURE_OPENAI_RESOURCE_2', '')
AZURE_OPENAI_KEY_2 = os.environ.get('AZURE_OPENAI_KEY_2', '')

AZURE_OPENAI_RESOURCE_3 = os.environ.get('AZURE_OPENAI_RESOURCE_3', '')
AZURE_OPENAI_KEY_3 = os.environ.get('AZURE_OPENAI_KEY_3', '')

AZURE_OPENAI_RESOURCE_4 = os.environ.get('AZURE_OPENAI_RESOURCE_4', '')
AZURE_OPENAI_KEY_4 = os.environ.get('AZURE_OPENAI_KEY_4', '')

AZURE_OPENAI_RESOURCE_5 = os.environ.get('AZURE_OPENAI_RESOURCE_5', '')
AZURE_OPENAI_KEY_5 = os.environ.get('AZURE_OPENAI_KEY_5', '')

AZURE_OPENAI_RESOURCE_6 = os.environ.get('AZURE_OPENAI_RESOURCE_6', '')
AZURE_OPENAI_KEY_6 = os.environ.get('AZURE_OPENAI_KEY_6', '')

AZURE_OPENAI_EMBEDDING_MODEL_RESOURCE = os.environ.get('AZURE_OPENAI_EMBEDDING_MODEL_RESOURCE', '')
AZURE_OPENAI_EMBEDDING_MODEL_RESOURCE_KEY = os.environ.get('AZURE_OPENAI_EMBEDDING_MODEL_RESOURCE_KEY', '')
AZURE_OPENAI_EMBEDDING_MODEL_API_VERSION = os.environ.get('AZURE_OPENAI_EMBEDDING_MODEL_API_VERSION', '2023-12-01-preview')


AZURE_OPENAI_MODEL = os.environ.get('AZURE_OPENAI_MODEL', '')
AZURE_OPENAI_EMBEDDING_MODEL = os.environ.get('AZURE_OPENAI_EMBEDDING_MODEL', 'text-embedding-ada-002')
AZURE_OPENAI_MODEL_VISION = os.environ.get('AZURE_OPENAI_MODEL_VISION', '')
AZURE_OPENAI_VISION_API_VERSION = os.environ.get('AZURE_OPENAI_VISION_API_VERSION', '2023-12-01-preview')

AZURE_OPENAI_API_VERSION = os.environ.get('AZURE_OPENAI_API_VERSION', '')

# Full custom endpoint override for Azure OpenAI-compatible accounts
# (e.g. Azure AI Foundry / kind=AIServices resources whose domain is
# *.cognitiveservices.azure.com instead of *.openai.azure.com).
# When set, it replaces the classic https://<resource>.openai.azure.com
# construction in every endpoint-building code path.
AZURE_OPENAI_ENDPOINT = os.environ.get('AZURE_OPENAI_ENDPOINT', '')

def get_openai_endpoint(resource_name):
    return AZURE_OPENAI_ENDPOINT if AZURE_OPENAI_ENDPOINT else f"https://{resource_name}.openai.azure.com"
AZURE_OPENAI_TEMPERATURE = os.environ.get('AZURE_OPENAI_TEMPERATURE', '')
AZURE_OPENAI_TOP_P = os.environ.get('AZURE_OPENAI_TOP_P', '')
AZURE_OPENAI_MAX_TOKENS = os.environ.get('AZURE_OPENAI_MAX_TOKENS', '')
AZURE_OPENAI_STOP_SEQUENCE = os.environ.get('AZURE_OPENAI_STOP_SEQUENCE', '')

ROOT_PATH_INGESTION = os.environ.get('ROOT_PATH_INGESTION', '')

COG_SERV_ENDPOINT = os.environ.get('COG_SERV_ENDPOINT', '')
COG_SERV_KEY = os.environ.get('COG_SERV_KEY', '')
COG_SERV_LOCATION = os.environ.get('COG_SERV_LOCATION', '')

COG_SEARCH_ENDPOINT = os.environ.get('COG_SEARCH_ENDPOINT', '')
COG_SEARCH_ADMIN_KEY = os.environ.get('COG_SEARCH_ADMIN_KEY', '')
COG_VEC_SEARCH_API_VERSION = os.environ.get('COG_VEC_SEARCH_API_VERSION', '')

COG_SEARCH_ENDPOINT_PROD = os.environ.get('COG_SEARCH_ENDPOINT_PROD', '')
COG_SEARCH_ADMIN_KEY_PROD = os.environ.get('COG_SEARCH_ADMIN_KEY_PROD', '')

BLOB_CONN_STR = os.environ.get('BLOB_CONN_STR', '')

TRANSLATION_ENDPOINT = os.environ.get('TRANSLATION_ENDPOINT', 'https://api.cognitive.microsofttranslator.com')

SEM_INDEX_NAME = os.environ.get('SEM_INDEX_NAME', 'sc-sem')
COG_VECSEARCH_VECTOR_INDEX = os.environ.get('COG_VECSEARCH_VECTOR_INDEX', 'vec-index')

KB_INDEX_NAME = os.environ.get('KB_INDEX_NAME', 'sc')
KB_SEM_INDEX_NAME = os.environ.get('KB_SEM_INDEX_NAME', 'sc_1')
KB_INDEXER_NAME = os.environ.get('KB_INDEXER_NAME', 'sc-indexer')
KB_DATA_SOURCE_NAME = os.environ.get('KB_DATA_SOURCE_NAME', 'sc-docs')
KB_SKILLSET_NAME = os.environ.get('KB_SKILLSET_NAME', 'sc-skills')
KB_BLOB_CONTAINER = os.environ.get('KB_BLOB_CONTAINER', 'search')
OVERLAP_TEXT = int(os.environ.get('OVERLAP_TEXT', '250'))

AZURE_VISION_ENDPOINT = os.environ.get('AZURE_VISION_ENDPOINT', '')
AZURE_VISION_KEY = os.environ.get('AZURE_VISION_KEY', '')

AZURE_OPENAI_ASSISTANTSAPI_ENDPOINT = os.environ.get('AZURE_OPENAI_ASSISTANTSAPI_ENDPOINT', '')
AZURE_OPENAI_ASSISTANTSAPI_KEY = os.environ.get('AZURE_OPENAI_ASSISTANTSAPI_KEY', '')

TEXT_CHUNK_SIZE = int(os.environ.get('TEXT_CHUNK_SIZE', '512'))
TEXT_CHUNK_OVERLAP = int(os.environ.get('TEXT_CHUNK_OVERLAP', '128'))

CHAINLIT_APP = os.environ.get('CHAINLIT_APP', '')

TENACITY_STOP_AFTER_DELAY = int(os.environ.get('TENACITY_STOP_AFTER_DELAY', '300'))
TENACITY_TIMEOUT = int(os.environ.get('TENACITY_TIMEOUT', '200'))

## AML
AML_SUBSCRIPTION_ID=os.environ.get('AML_SUBSCRIPTION_ID', '')
AML_RESOURCE_GROUP=os.environ.get('AML_RESOURCE_GROUP', '')
AML_WORKSPACE_NAME=os.environ.get('AML_WORKSPACE_NAME', '')

## Azure File Share
AZURE_FILE_SHARE_ACCOUNT=os.environ.get('AZURE_FILE_SHARE_ACCOUNT', '')
AZURE_FILE_SHARE_NAME=os.environ.get('AZURE_FILE_SHARE_NAME', '')
AZURE_FILE_SHARE_KEY=os.environ.get('AZURE_FILE_SHARE_KEY', '')

#COSMOS DB
COSMOS_URI = os.environ.get('COSMOS_URI', '')
COSMOS_KEY = os.environ.get('COSMOS_KEY', '')
COSMOS_DB_NAME = os.environ.get('COSMOS_DB_NAME', 'mmdoc')
COSMOS_CONTAINER_NAME = os.environ.get('COSMOS_CONTAINER_NAME', 'prompts')
COSMOS_CATEGORYID = os.environ.get('COSMOS_CATEGORYID', 'prompts')
COSMOS_LOG_CONTAINER = os.environ.get('COSMOS_LOG_CONTAINER', 'logs')


INITIAL_INDEX = os.environ.get('INITIAL_INDEX', 'rag-data')


BUILD_ID = os.getenv('BUILD_ID', '0.0.0')

AML_TENANT_ID = os.environ.get('AML_TENANT_ID', '')
AML_SERVICE_PRINCIPAL_ID = os.environ.get('AML_SERVICE_PRINCIPAL_ID', '')
AML_PASSWORD = os.environ.get('AML_PASSWORD', '')
AML_VMSIZE = os.environ.get('AML_VMSIZE', 'Standard_DS3_v2')
AML_CLUSTER_NAME = os.environ.get('AML_CLUSTER_NAME','mm-doc-cpu-cluster')

FULL_TEXT_TOKEN_LIMIT = int(os.environ.get('FULL_TEXT_TOKEN_LIMIT', '100000'))


AZURE_SQL_SERVER_NAME = os.environ.get('AZURE_SQL_SERVER_NAME', '')
AZURE_SQL_DATABASE_NAME = os.environ.get('AZURE_SQL_DATABASE_NAME', '')
AZURE_SQL_USERNAME = os.environ.get('AZURE_SQL_USERNAME', '')
AZURE_SQL_PASSWORD = os.environ.get('AZURE_SQL_PASSWORD', '')
AZURE_SQL_SCHEMA_NAME = os.environ.get('AZURE_SQL_SCHEMA_NAME', 'dbo')
AZURE_SQL_DRIVER = os.environ.get('AZURE_SQL_DRIVER', 'ODBC Driver 18 for SQL Server')


SEARCH_TOP_N =  int(os.environ.get('SEARCH_TOP_N', '4'))


AZURE_NEO4J_URI = os.environ.get('AZURE_NEO4J_URI', '')
AZURE_NEO4J_USERNAME = os.environ.get('AZURE_NEO4J_USERNAME', '')
AZURE_NEO4J_PASSWORD = os.environ.get('AZURE_NEO4J_PASSWORD', '')
AZURE_NEO4J_DATABASE = os.environ.get('AZURE_NEO4J_DATABASE', '')

APPLICATIONINSIGHTS_CONNECTION_STRING = os.environ.get('APPLICATIONINSIGHTS_CONNECTION_STRING', '')
# --- Entra ID (keyless) auth helpers ---------------------------------------
# AZURE_CLIENT_ID is the user-assigned managed identity's client id. It is
# already set in the deployed app settings (originally for the AML SDK v1
# MSI trick) and doubles as the switch for keyless data-service access:
# when set, all data-plane calls use Entra tokens (DefaultAzureCredential
# reads AZURE_CLIENT_ID for user-assigned managed identity); when unset
# (local dev), the classic key-based auth is used.
AZURE_CLIENT_ID = os.environ.get('AZURE_CLIENT_ID', '')

COGNITIVE_SERVICES_SCOPE = 'https://cognitiveservices.azure.com/.default'
AZURE_SEARCH_SCOPE = 'https://search.azure.com/.default'

_entra_credential = None
_entra_token_cache = {}

def use_entra_auth():
    return bool(AZURE_CLIENT_ID)

def get_entra_credential():
    global _entra_credential
    if _entra_credential is None:
        from azure.identity import DefaultAzureCredential
        _entra_credential = DefaultAzureCredential()
    return _entra_credential

def get_entra_token(scope=COGNITIVE_SERVICES_SCOPE):
    import time as _time
    entry = _entra_token_cache.get(scope)
    if entry and entry[1] > _time.time():
        return entry[0]
    token = get_entra_credential().get_token(scope).token
    # refresh ~5 minutes before the typical 3600s expiry
    _entra_token_cache[scope] = (token, _time.time() + 3000)
    return token

def search_auth_headers(api_key):
    headers = {'Content-Type': 'application/json'}
    if use_entra_auth():
        headers['Authorization'] = 'Bearer ' + get_entra_token(AZURE_SEARCH_SCOPE)
    else:
        headers['api-key'] = api_key
    return headers
