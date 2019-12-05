from rest_framework import serializers
from .models import CreateSocial


class CreateSocialSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreateSocial
        fields = ['title', 'content', 'filename']
        # url = serializers.get_url_kwargs('url')
