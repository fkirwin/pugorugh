from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from rest_framework import permissions
from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.views import APIView, Response
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin

from . import serializers
from . import models


class UserRegisterView(CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    model = get_user_model()
    serializer_class = serializers.UserSerializer


class UserPreferenceSaveView(APIView):
    #permission_classes = (permissions.IsAuthenticated,)
    #model = models.UserPref
    #serializer_class = serializers.UserPrefSerializer

    def put(self, request, format=None):
        pref, status = models.UserPref.objects.get_or_create(user=self.request.user)
        incoming = serializers.UserPrefSerializer(pref, data=request.data)
        if incoming.is_valid():
            incoming.save()
        return Response(incoming.data)

