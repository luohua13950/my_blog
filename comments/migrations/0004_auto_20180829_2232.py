# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-08-29 14:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0003_auto_20180730_2216'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='email',
            field=models.EmailField(blank=True, max_length=255),
        ),
    ]
