import pytest

from video.models import Video


@pytest.fixture
def video_data():
    data = {
        "file": "static/video.mp4",
        "title": "Title Example",
        "description": "Description example: \n\nContinue description...",
        "category": 2,
        "keywords": [
            "keyword1",
            "keyword2",
            "keyword3"
        ],
        "privacy_status": "private",
        "id_youtube": None,
        "origin_channel": "Origin Channel",
        "origin_video_url": "https://www.youtube.com/watch?v=id-do-video"
    }
    return data


@pytest.fixture
def video(video_data, db):
    return Video.objects.create(**video_data)
