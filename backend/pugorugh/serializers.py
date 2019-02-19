from django.contrib.auth import get_user_model

from rest_framework import serializers

from . import models

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = get_user_model().objects.create(
            username=validated_data['username'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = get_user_model()
        fields = (
             'password',
             'username',
        )


class DogSerializer(serializers.ModelSerializer):

    class Meta:
        fields = (
            'name',
            'image_filename',
            'breed',
            'age',
            'gender',
            'size',
        )
        model = models.Dog

class UserPrefSerializer(serializers.ModelSerializer):
    age = serializers.CharField()
    gender = serializers.CharField()
    size = serializers.CharField()

    class Meta:
        fields = (
            'age',
            'gender',
            'size',
        )
        model = models.UserPref


class UserDogSerializer(serializers.ModelSerializer):

    class Meta:
        fields = (
            'dog',
            'user',
            'status',
        )
        model = models.UserDog
