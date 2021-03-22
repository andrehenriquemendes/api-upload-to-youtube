from types import SimpleNamespace

import pytest

from django import urls

from video.models import Video

from brokers.youtube.authentication import data_simplenamespace


def test_data_simplenamespace(client, video_data, db):
    response = data_simplenamespace(video_data)
    assert isinstance(response, SimpleNamespace)
    assert hasattr(response, 'auth_host_name')
    assert hasattr(response, 'auth_host_port')
    assert hasattr(response, 'logging_level')
    assert hasattr(response, 'noauth_local_webserver')





