# Generated by Django 2.1.5 on 2019-02-13 01:22

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pugorugh', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userpref',
            name='user',
            field=models.OneToOneField(on_delete='protect', to=settings.AUTH_USER_MODEL),
        ),
    ]
