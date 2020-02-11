from django.contrib.auth.models import User
from rest_framework import serializers

from users.models import Profile


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=200)
    username = serializers.CharField(max_length=200, read_only=True)

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password"]


class ProfileSerializer(serializers.ModelSerializer):
    xp_points = serializers.IntegerField(read_only=True)
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = ["user", "avatar", "xp_points"]
