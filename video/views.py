from django.shortcuts import render
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404

from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.response import Response

from video.models import Video
from video.serializers import VideoSerializer

from brokers.youtube.integrations import upload_to_youtube


class VideoViewSet(ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(methods=['post'], detail=True)
    def upload(self, request, pk=None):
        instance = get_object_or_404(Video, pk=pk)

        upload_to_youtube(VideoSerializer(instance).data)

        return Response(
            {'messagem': f'Video was successfully uploaded.'}, status=status.HTTP_200_OK)
