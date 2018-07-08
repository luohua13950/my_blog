__author__ = 'luohua139'
from ..models import Post,Category,Tag
from django import template
from django.db.models.aggregates import Count
register = template.Library()
@register.simple_tag
def get_recent_psots(num=5):
    return Post.objects.all().order_by('-create_time')[:num]
@register.simple_tag
def archives():
    return Post.objects.dates('create_time','month',order = 'DESC')
@register.simple_tag
def get_categorys():
    return Category.objects.annotate(num_count = Count('post')).filter(num_count__gt=0)
@register.simple_tag
def get_tag():
    return Tag.objects.annotate(num_count=Count('post')).filter(num_count__gt=0)