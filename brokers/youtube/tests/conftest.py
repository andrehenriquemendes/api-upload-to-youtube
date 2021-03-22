import pytest

from video.models import Video


@pytest.fixture
def video_data():
    data = {
        'id': 61,
        'file': 'static_files/video/canal_test/convidado_test/video_test.mp4',
        'title': 'Title example',
        'description': 'Marcio Donato no PodPah \n\n Episodio completo: www.youtube.com/watch?id-do-video',
        'category': 24,
        'keywords': ['marcio donato', 'podpah', 'podcast'],
        'privacy_status': 'private',
        'id_youtube': 'abc1234',
        'is_uploaded': True,
        'origin_channel': 'PodPah',
        'origin_video_url': 'https://www.youtube.com/watch?v=id-do-video&ab_channel=Podpah'
    }
    return data
