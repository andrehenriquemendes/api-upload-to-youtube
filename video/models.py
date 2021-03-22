from django.db import models
from django.contrib.postgres.fields import ArrayField

from .constants import *


class Video(models.Model):
    file = models.CharField(max_length=255)
    title = models.CharField(max_length=80)
    description = models.TextField(null=True)
    category = models.IntegerField()
    keywords = ArrayField(models.CharField(max_length=30))
    privacy_status = models.CharField(
        max_length=20, choices=PRIVACY_STATUS, default=PRIVACY_STATUS_PRIVATE)

    id_youtube = models.CharField(max_length=50, null=True)
    is_uploaded = models.BooleanField(default=False)

    origin_channel = models.CharField(max_length=50)
    origin_video_url = models.URLField(max_length=250)

    def __str__(self):
        return self.title
