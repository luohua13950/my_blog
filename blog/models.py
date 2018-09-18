# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.six import python_2_unicode_compatible

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
class Tag(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
class Post(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    create_time = models.DateTimeField()
    modify_time = models.DateTimeField()
    excerpt = models.CharField(max_length=200,blank=True)
    category = models.ForeignKey(Category)
    tags = models.ManyToManyField(Tag,blank=True)
    author = models.ForeignKey(User)
    view = models.PositiveIntegerField(default=0)
    def __str__(self):
        return self.title
    def absolute_url(self):
        return reverse('blog:detail',kwargs={'pk':self.pk})
    #这里使用了update——field：只更新指定字段
    def auto_increase_view(self):
        self.view +=1
        self.save(update_fields=['view'])
class Users(models.Model):
    user_name = models.CharField(max_length=60,unique=True)
    pass_wd = models.CharField(max_length=60)
    def __str__(self):
        return self.user_name