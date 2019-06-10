# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2019-04-24 10:31
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('performance', '0016_auto_20190423_2123'),
    ]

    operations = [
        migrations.AddField(
            model_name='basicevaluation',
            name='other_expectation',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='basicevaluation',
            name='training',
            field=models.CharField(default=1, max_length=500, verbose_name='List the Trainings you attended during the PDTP programme?'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='basicevaluation',
            name='training_expectection',
            field=models.CharField(default=1, max_length=200, verbose_name='List professional Certifications you successfully undertook during your PDTP progamme period. '),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='innovationevaluation',
            name='evaluation',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=5, validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(0)], verbose_name='First Evaluation'),
        ),
        migrations.AlterField(
            model_name='innovationevaluation',
            name='final',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=5, verbose_name='Final Evaluation'),
        ),
        migrations.AlterField(
            model_name='innovationevaluation',
            name='initiative',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=5, validators=[django.core.validators.MaxValueValidator(2), django.core.validators.MinValueValidator(0)], verbose_name='Submission/Initiative'),
        ),
        migrations.AlterField(
            model_name='innovationevaluation',
            name='presentation',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=5, validators=[django.core.validators.MaxValueValidator(3), django.core.validators.MinValueValidator(0)], verbose_name='Shortlisted'),
        ),
        migrations.AlterField(
            model_name='innovationevaluation',
            name='total',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
    ]