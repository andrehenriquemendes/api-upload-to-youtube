import httplib2
import random
import time
import http.client
import logging
import json

from rest_framework import status
from rest_framework.response import Response

from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

from .authentication import get_authenticated_service

# Explicitly tell the underlying HTTP transport library not to retry, since
# we are handling retry logic ourselves.
from video.models import Video

httplib2.RETRIES = 1
MAX_RETRIES = 5

# Always retry when these exceptions are raised.
RETRIABLE_EXCEPTIONS = (
    httplib2.HttpLib2Error, IOError, http.client.NotConnected,
    http.client.IncompleteRead, http.client.ImproperConnectionState,
    http.client.CannotSendRequest, http.client.CannotSendHeader,
    http.client.ResponseNotReady, http.client.BadStatusLine
)

RETRIABLE_STATUS_CODES = [500, 502, 503, 504]


def initialize_upload(youtube, data):
    body = dict(
        snippet=dict(
            title=data.get('title'),
            description=data.get('description'),
            categoryId=data.get('category'),
            tags=data.get('keywords')
        ),
        status=dict(
            privacy_status=data.get('privacy_status')
        )
    )

    insert_request = youtube.videos().insert(
        part=','.join(body.keys()),
        body=body,
        media_body=MediaFileUpload(data.get('file'), chunksize=-1, resumable=True)
        # Setting "chunksize" equal to -1 in the code below means that the entire
        # file will be uploaded in a single HTTP request. (If the upload fails,
        # it will still be retried where it left off.)
    )
    response = resumable_upload(insert_request)
    return response


def resumable_upload(insert_request):
    response = None
    error = None
    retry = 0
    while response is None:
        try:
            print('Uploading file...')
            status, response = insert_request.next_chunk()
            if response is not None:
                if 'id' in response:
                    print(f'Video id {response["id"]} was successfully uploaded.')
                else:
                    exit(f'The upload failed an unexpected response: {response}')
        except HttpError as e:
            if e.resp.status in RETRIABLE_STATUS_CODES:
                error = f'A retriable HTTP error {e.resp.status} occurred:\n{e.content}'
            else:
                raise
        except RETRIABLE_EXCEPTIONS as e:
            error = f'A retriable error occurred: {e}'

        if error is not None:
            print(error)
            retry += 1
            if retry > MAX_RETRIES:
                exit('No longer attempting to retry.')

            max_sleep = 2 ** retry
            sleep_seconds = random.random() * max_sleep
            print(f'Sleeping {sleep_seconds} seconds and then retrying...')
            time.sleep(sleep_seconds)
    return response


def upload_to_youtube(data):
    video_instance = Video.objects.get(id=data['id'])
    youtube = get_authenticated_service(data)

    logger = logging.getLogger(__name__)
    try:
        response = initialize_upload(youtube, data)
    except HttpError as e:
        logging.error('Failed to upload to ftp: ' + str(e))
        raise

    if video_instance:
        video_instance.is_uploaded = True
        video_instance.id_youtube = response.get('id')
        video_instance.save()
