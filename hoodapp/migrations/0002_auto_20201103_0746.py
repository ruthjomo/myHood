# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-11-03 04:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hoodapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='neighborhood',
            name='locality',
            field=models.CharField(default='', max_length=30),
        ),
    ]
