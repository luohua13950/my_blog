#-*- coding:utf-8 -*-
__author__ = 'luohua139'
from ..models import Post,Category,Tag
from resource.models import Resource,Cate
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

@register.simple_tag
def hot_article(num=5):
    return Post.objects.all().order_by('-view')[:num]

@register.simple_tag
def get_recent_res(num=5):
    return Resource.objects.all().order_by('-create_time')[:num]
@register.simple_tag
def hot_resoucre(num=5):
    return Resource.objects.all().order_by('-download')[:num]

@register.filter
def div(value):
    size = ''
    if value/1000 >1000:
        return str(float(value/1000000))+'M'
    else:
        return str(value/1000)+'K'
@register.simple_tag
def res_cateforys():
    return Cate.objects.annotate(num_count = Count('resource')).filter(num_count__gt=0)#resource即为模型Resource，这里的小写

@register.filter()
def user_upload(user):
    count = Resource.objects.filter(upload_user=user).count()
    return count

@register.filter()
def user_post_article(user):
    count = Post.objects.filter(author=user).count()
    return count