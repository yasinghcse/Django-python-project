# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-25 14:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_auto_20170518_1406'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='title',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
