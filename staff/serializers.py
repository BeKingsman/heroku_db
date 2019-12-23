from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import *




class user_profile_serializer(serializers.ModelSerializer):
    # snippets = serializers.PrimaryKeyRelatedField(many=True, queryset=Snippet.objects.all())

    class Meta:
        model = user_profile
        fields = '__all__'


class user_profile_serializer(serializers.ModelSerializer):
    # snippets = serializers.PrimaryKeyRelatedField(many=True, queryset=Snippet.objects.all())

    class Meta:
        model = user_profile
        fields = '__all__'
