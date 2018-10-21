# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Advise
# Register your models here.
import sys
reload(sys)
class AdviseAdmin(admin.ModelAdmin):
    list_display = ['advise','user','sub_time']
admin.site.register(Advise,AdviseAdmin)