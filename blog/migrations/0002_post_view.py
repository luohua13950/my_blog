# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-07-03 12:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='view',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
