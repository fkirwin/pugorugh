from django.contrib.auth import get_user_model, get_user
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework import permissions, viewsets
from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveAPIView, UpdateAPIView, GenericAPIView, ListAPIView, RetrieveUpdateAPIView
from rest_framework.views import APIView, Response
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, RetrieveModelMixin

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


class AllDogs(viewsets.ModelViewSet):
    """
    This utilizes a modelviewset which is registered with a router.  Lots of alchemy,
    but automatic gets are happening for all dogs and for each dog.  Saves a lot of code.
    """
    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.DogSerializer
    queryset = models.Dog.objects.all()


class NextLikedDog(RetrieveAPIView):
    """
    It looks like RetrieveAPIView isn't as concerned with queryset and likes to have get_object used.
    Here is one way to handle getting resources from the DB based on some logic.
    """
    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.DogSerializer
    queryset = models.Dog.objects.prefetch_related('userdog').order_by('id').all()

    def get_queryset(self):
        return self.queryset.select_related('userdog').filter(userdog__status__icontains='l')\
                                                      .filter(userdog__user=self.request.user.id).all()

    def get_object(self):
        target = self.kwargs.get('pk')
        next_record = target + 1
        try:
            next_dog = self.get_queryset().get(id=next_record)
            return next_dog
        except:
            next_dog = self.get_queryset().first()
            if next_dog:
                return next_dog
            else:
                raise NotFound


class NextDislikedDog(APIView):
    '''
    Using generic view.  Also used the associative table to handle the dog getting.
    '''
    permission_classes = (permissions.AllowAny,)

    def get(self, request, pk, format=None):
        next_record = pk + 1
        dogs = models.UserDog.objects.filter(status__icontains='d').filter(user_id=self.request.user.id).order_by('id').all()
        try:
            next_pref = dogs.get(dog_id=next_record)
        except:
            next_pref = dogs.first()
            if next_pref:
                return next_pref.dog
            else:
                raise NotFound
        else:
            serializer = serializers.DogSerializer(next_pref.dog, many=True)
            return Response(serializer.data)


class NextUndecidedDog(RetrieveModelMixin, GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.DogSerializer
    queryset = models.Dog.objects.order_by('id').all()

    def get_queryset(self):
        return self.queryset.exclude(id__in=models.UserDog.objects.filter(user_id=self.request.user.id).all())

    def get_object(self):
        next_record = self.kwargs.get('pk')+1
        try:
            next_dog = self.queryset.get(id=next_record)
            return next_dog
        except:
            next_dog = self.queryset.first()
            if next_dog:
                return next_dog
            else:
                raise NotFound

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


##And now for some clean inheritance

class CoreDogs(RetrieveUpdateAPIView, CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.DogSerializer
    queryset = models.Dog.objects.order_by('id').all()


class ChangeUndecidedDog(CoreDogs):

    def get_object(self):
        return get_object_or_404(self.get_queryset())

    def get_queryset(self):
        try:
            self.queryset.exclude(id__in=models.UserDog.objects.filter(user_id=self.request.user.id).get(id=self.kwargs.get('pk')))
        except:
            raise NotFound

    def post(self, request, *args, **kwargs):
        decision = models.UserDog(dog=self.queryset.get(id=self.kwargs.get('pk')), user_id=self.request.user.id, status=request.data['status'])
        decision.save()
        serializer = serializers.UserDog(decision)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
