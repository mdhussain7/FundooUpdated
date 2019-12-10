from rest_framework import serializers
from .models import SocialLogin , CreateSocial


class CreateSocialSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialLogin
        fields = '__all__'
        # url = serializers.get_url_kwargs('url')


class ShareSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreateSocial
        fields = ['title', 'filename']
