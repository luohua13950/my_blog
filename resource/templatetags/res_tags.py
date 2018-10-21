__author__ = 'luohua139'
from django import template
from django.db.models.aggregates import Count
from ..models import Resource
register = template.Library()
@register.simple_tag
def get_recent_res(num=5):
    return Resource.objects.all().order_by('-create_time')[0:5]
@register.simple_tag
def hot_resoucre(num=5):
    return Resource.objects.all.order_by('-download')[0:5]