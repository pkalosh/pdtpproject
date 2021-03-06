# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2019-04-10 17:58
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('performance', '0011_supervisorapprovalcomment_award_marks'),
    ]

    operations = [
        migrations.AddField(
            model_name='buddyapprovalcomment',
            name='award_marks',
            field=models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(12), django.core.validators.MinValueValidator(0)], verbose_name='Award the intern marks as per his/her performance in your ourgnization and based on the report above(max 12)'),
        ),
        migrations.AlterField(
            model_name='supervisorapprovalcomment',
            name='award_marks',
            field=models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(12), django.core.validators.MinValueValidator(0)], verbose_name='Award the intern marks as per his/her performance in your ourgnization and based on the report above(max 12)'),
        ),
    ]
