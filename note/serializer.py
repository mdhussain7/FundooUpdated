from rest_framework import serializers
from .models import File, ImageTable


class ImageUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['file']


class ImageTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageTable
        fields = ['path', 'date', 'filename', 'directory']

