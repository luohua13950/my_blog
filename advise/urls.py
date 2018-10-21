__author__ = 'luohua139'
from django.conf.urls import url,include
from django.contrib import admin
from . import views
app_name='advise'
urlpatterns = [
    url(r'^advise/$',views.message_info,name='advise')
]