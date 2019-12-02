from rest_framework import serializers
from .models import CreateNotes


class CreateNotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreateNotes
        fields = ['title', 'content', 'filename']
        # url = serializers.get_url_kwargs('url')
