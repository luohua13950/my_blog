# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2019-03-01 14:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='last_login_ip',
            field=models.CharField(blank=True, max_length=120),
        ),
    ]