from django.contrib.auth.models import User
from django.db import models

GENDERS = (("m", "male"), ("f", "female"), ("u", "unknown"))
SIZES = (("s", "small"), ("m", "medium"), ("l", "large"), ("xl", "extra large"), ("u", "unknown"))
STATUSES = (("l", "liked"), ("d", "disliked"))
AGES = (("b", "baby"), ("y", "young"), ("a", "adult"), ("s", "senior"))

#GENDERS = ("m", "f", "u",)
#SIZES = ("s", "m", "l", "xl", "u",)
#STATUSES = ("l", "d",)
#AGES = ("b", "y", "a", "s",)


class Dog(models.Model):
    name = models.CharField(max_length=500,)
    image_filename = models.ImageField()
    breed = models.CharField(max_length=500,)
    age = models.IntegerField()
    gender = models.CharField(max_length=500, choices=GENDERS)
    size = models.CharField(max_length=500, choices=SIZES)


class UserDog(models.Model):
    user = models.ForeignKey(User, related_name='dogs', on_delete='cascade')
    dog = models.OneToOneField(Dog, on_delete='cascade')
    status = models.CharField(max_length=500, choices=STATUSES)


class UserPref(models.Model):
    user = models.OneToOneField(User, on_delete='cascade')
    age = models.CharField(max_length=500, choices=AGES)
    gender = models.CharField(max_length=500, choices=GENDERS)
    size = models.CharField(max_length=500, choices=SIZES)