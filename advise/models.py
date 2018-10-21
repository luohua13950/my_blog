# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Advise(models.Model):
    advise = models.TextField()
    user = models.ForeignKey(User)
    sub_time = models.DateTimeField()