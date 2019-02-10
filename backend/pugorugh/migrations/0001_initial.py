# Generated by Django 2.1.5 on 2019-02-10 21:04

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Dog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
                ('image_filename', models.ImageField(upload_to='')),
                ('breed', models.CharField(max_length=500)),
                ('age', models.IntegerField()),
                ('gender', models.CharField(choices=[('m', 'male'), ('f', 'female'), ('u', 'unknown')], max_length=500)),
                ('size', models.CharField(choices=[('s', 'small'), ('m', 'medium'), ('l', 'large'), ('xl', 'extra large'), ('u', 'unknown')], max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='UserDog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('l', 'liked'), ('d', 'disliked')], max_length=500)),
                ('dog', models.OneToOneField(on_delete='cascade', to='pugorugh.Dog')),
                ('user', models.ForeignKey(on_delete='cascade', related_name='dogs', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserPref',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('age', models.CharField(choices=[('b', 'baby'), ('y', 'young'), ('a', 'adult'), ('s', 'senior')], max_length=500)),
                ('gender', models.CharField(choices=[('m', 'male'), ('f', 'female'), ('u', 'unknown')], max_length=500)),
                ('size', models.CharField(choices=[('s', 'small'), ('m', 'medium'), ('l', 'large'), ('xl', 'extra large'), ('u', 'unknown')], max_length=500)),
                ('user', models.OneToOneField(on_delete='cascade', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
