# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
import datetime
# Create your models here.
class Cate(models.Model):
    cate_name = models.CharField(max_length=100)
    def __str__(self):
        return self.cate_name
class Resource(models.Model):
    res_name = models.CharField(max_length=200)
    upload_url = models.CharField(max_length=100)
    upload_user = models.ForeignKey(User)
    create_time=models.DateTimeField()
    download=models.PositiveIntegerField(default=0)
    size = models.PositiveIntegerField(default=0)
    cate = models.ForeignKey(Cate)
    def downlaod_count(self):
        self.download +=1
        self.save(update_fields=['download'])
    def __unicode__(self):
        return self.res_name