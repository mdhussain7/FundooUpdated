from rest_framework import serializers
from .models import File, ImageTable
from .models import Notes, Label
from django.contrib.auth.models import User


class ImageUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['file']


class ImageTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageTable
        fields = ['path', 'date', 'filename', 'directory']


class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = ['label']


class CollaboratorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email']


# Serializers define the API representation.
class NotesSerializer(serializers.ModelSerializer):
    label = LabelSerializer(many=True, read_only=True)
    collaborators = CollaboratorsSerializer(many=True, read_only=True)

    class Meta:
        model = Notes
        fields = ['title', 'note', 'label', 'url', 'is_archive', 'collaborators', 'image', 'reminder', 'color']


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
        fields = ['title', 'description', 'is_pinned']


class ShareSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notes
        fields = ['title', 'label']


class SearchNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notes
        fields = ['title', 'description']
