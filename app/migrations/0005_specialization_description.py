# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2019-04-27 14:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20190427_1714'),
    ]

    operations = [
        migrations.AddField(
            model_name='specialization',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
