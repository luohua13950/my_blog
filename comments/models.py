# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from blog.models import User
# Create your models here.
class Comment(models.Model):
    name = models.ManyToManyField(User)
    email = models.EmailField(max_length=255,blank=True)
    url = models.URLField(blank=True)
    text = models.TextField()
    create_time = models.DateTimeField(auto_now_add=True)

    post = models.ForeignKey('blog.Post')

    def __str__(self):
        return self.text[:20]