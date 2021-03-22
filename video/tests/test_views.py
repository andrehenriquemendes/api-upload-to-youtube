import pytest

from django import urls

from video.models import Video


def test_post_video(client, video_data, db):
    response = client.post('/video/', video_data, content_type='application/json')
    res_json = response.json()

    video_db = Video.objects.get(id=res_json.get('id'))

    assert response.status_code == 201
    assert res_json.get('file') == video_data.get('file')
    assert video_db.file == video_data.get('file')


def test_list_videos(client, video):
    response = client.get('/video/')
    res_json = response.json()

    assert len(res_json) == 1
    assert response.status_code == 200


def test_retrieve_video(client, video):
    response = client.get(f'/video/{video.id}/')
    res_json = response.json()

    assert response.status_code == 200
    assert res_json.get('id') == video.id


def test_delete_video(client, video):
    response = client.delete(f'/video/{video.id}/')

    video_in_db = Video.objects.filter(id=video.id).exists()

    assert response.status_code == 204
    assert not video_in_db


def test_patch_video(client, video):
    payload = {'title': 'Updated Title'}

    response = client.patch(f'/video/{video.id}/', payload, content_type='application/json')
    res_json = response.json()

    video_db = Video.objects.get(id=video.id)

    assert response.status_code == 200
    assert res_json.get('title') == 'Updated Title'
    assert video_db.title == 'Updated Title'
