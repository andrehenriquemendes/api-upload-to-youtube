from types import SimpleNamespace
import httplib2
import os
import json

from googleapiclient.discovery import build
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run_flow
from decouple import config

# Always retry when an apiclient.errors.HttpError with one of these status codes is raised.
RETRIABLE_STATUS_CODES = [500, 502, 503, 504]

# File that contains the OAuth 2.0 information for this application,
# including its client_id and client_secret.
CLIENT_SECRETS_FILE = 'brokers/youtube/client_secrets.json'

MISSING_CLIENT_SECRETS_MESSAGE = 'WARNING: Please configure OAuth 2.0 (client_secrets.json)'

YOUTUBE_UPLOAD_SCOPE = 'https://www.googleapis.com/auth/youtube.upload'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'


def data_simplenamespace(data):
    data.pop('id', None)
    data.pop('id_youtube', None)
    data.pop('is_uploaded', None)
    data.pop('origin_channel', None)
    data.pop('origin_video_url', None)
    data['logging_level'] = 'ERROR'
    data['noauth_local_webserver'] = config('NOAUTH_LOCAL_WEBSERVER') == 'True'
    data['auth_host_name'] = config('AUTH_HOST_NAME')
    data['auth_host_port'] = [8080, 8090]
    return SimpleNamespace(**data)


def setup_client_secrets(client_secret_path, action):
    file = open(client_secret_path, "r")
    json_object = json.load(file)
    file.close()

    if action == 'fill':
        json_object['web']['client_id'] = os.environ['API_GOOGLE_CLIENT_ID']
        json_object['web']['client_secret'] = os.environ['API_GOOGLE_CLIENT_SECRET']
    elif action == 'delete':
        json_object['web']['client_id'] = ""
        json_object['web']['client_secret'] = ""

    file = open(client_secret_path, "w")
    json.dump(json_object, file, indent=4)
    file.close()


def get_authenticated_service(data):
    setup_client_secrets(CLIENT_SECRETS_FILE, 'fill')
    flow = flow_from_clientsecrets(
        CLIENT_SECRETS_FILE,
        scope=YOUTUBE_UPLOAD_SCOPE,
        message=MISSING_CLIENT_SECRETS_MESSAGE
    )
    setup_client_secrets(CLIENT_SECRETS_FILE, 'delete')

    storage = Storage(f'brokers/youtube/credentials-oauth2.json')
    credentials = storage.get()

    if credentials is None or credentials.invalid:
        credentials = run_flow(flow, storage, data_simplenamespace(data))

    return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, http=credentials.authorize(httplib2.Http()))
