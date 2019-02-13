from django.contrib.auth import get_user_model, get_user
from django.shortcuts import get_object_or_404

from rest_framework import permissions
from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveAPIView, UpdateAPIView, GenericAPIView, ListAPIView, RetrieveUpdateAPIView
from rest_framework.views import APIView, Response
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin

from . import serializers
from . import models


class UserRegisterView(CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    model = get_user_model()
    serializer_class = serializers.UserSerializer

    def create(self, request, *args, **kwargs):
        user = super().create(request, *args, **kwargs)
        pref_shell = models.UserPref(user=models.User.objects.get_by_natural_key(request.data['username']))
        pref_shell.save()
        return user


class UserPreferenceSaveView(RetrieveUpdateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.UserPrefSerializer
    queryset = models.UserPref.objects.all()

    def get_object(self):
        prefs = models.UserPref.objects.get(user=self.request.user)
        return prefs


    '''
    pref, status = models.UserPref.objects.get_or_create(user=self.request.user)
    incoming = serializers.UserPrefSerializer(pref, data=request.data)
    if incoming.is_valid():
        incoming.save()
    return Response(incoming.data)
    '''


class ListAllDogs(ListAPIView):
    serializer_class = serializers.DogSerializer
    queryset = models.Dog.objects.all()

class ListNextUndecidedDog(ListAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.DogSerializer
    queryset = models.Dog.objects.all()