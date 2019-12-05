from rest_framework import serializers
from .models import File, ImageTable
from .models import Notes, Label


class ImageUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['file']


class ImageTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageTable
        fields = ['path', 'date', 'filename', 'directory']


# Serializers define the API representation.
# class NoteSerializer(serializers.ModelSerializer):
#     class Meta:
#
#         model = Notes
#         fields = ['id', 'title', 'description', 'is_archived', 'is_pinned', 'image', 'color', 'is_trash', 'collaborate',
#                   'remainder', 'created_time', 'user']

class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = ['label']


class CreateNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notes
        # fields = ['title', 'description', 'is_archived', 'is_pinned', 'image', 'color', 'is_trash',
        #           'reminder', 'user']
        fields = ['title', 'description', 'is_archived', 'is_pinned', 'color', 'is_trash',
                  'reminder', 'user']


class UpdateNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notes
        fields = '__all__'


class ArchieveNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notes
        fields = 'is_archived'


class TrashNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notes
        fields = 'is_trash'


class PinnedNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notes
        fields = ['title', 'description','is_pinned']


class SearchNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notes
        fields = ['title', 'description']
