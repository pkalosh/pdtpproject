# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2019-04-05 12:40
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('performance', '0004_auto_20190405_1531'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mentorshipreport',
            name='pdtp',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
