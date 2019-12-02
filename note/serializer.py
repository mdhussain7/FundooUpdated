from rest_framework import serializers
from .models import File, ImageTable
from .models import Notes


class ImageUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['file']


class ImageTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageTable
        fields = ['path', 'date', 'filename', 'directory']


# Serializers define the API representation.
class NoteSerializer(serializers.ModelSerializer):
    class Meta:

        model = Notes
        fields = ['id', 'title', 'description', 'is_archived', 'pinned', 'image', 'color', 'trash', 'collaborate',
                  'remainder', 'created_time', 'user']


class CreateNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notes
        fields = ['title', 'description', 'is_archived', 'is_pinned', 'image', 'color', 'is_trash',
                  'reminder', 'user']


class UpdateNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notes
        fields = '__all__'


class SearchNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notes
        fields = ['title', 'description']
