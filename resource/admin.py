# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Resource
import  sys
# Register your models here.
reload(sys)
class ResoucreAdmin(admin.ModelAdmin):
    list_display = ['res_name','upload_url','upload_user','create_time']
admin.site.register(Resource,ResoucreAdmin)

