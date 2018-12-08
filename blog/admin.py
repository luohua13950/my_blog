# -*- coding: utf-8 -*-


from __future__ import unicode_literals
import sys
from django.contrib import admin
from .models import Post,Category,Tag
# Register your models here.
#import importlib
#importlib.reload(sys)
#sys.setdefaultencoding('utf-8')
class PostAdmin(admin.ModelAdmin):
    list_display = ['title','create_time','modify_time','category','author']
admin.site.register(Post,PostAdmin)
admin.site.register(Category)
admin.site.register(Tag)