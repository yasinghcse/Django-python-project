# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-28 18:05
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_auto_20170613_2120'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='numpages',
            field=models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(1000), django.core.validators.MinValueValidator(50)]),
        ),
    ]
