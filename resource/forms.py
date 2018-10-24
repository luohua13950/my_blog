#-*- coding:utf-8 -*-
__author__ = 'luohua139'
from django import forms
from .models import Resource,Cate
class UploadForm(forms.Form):
    #title = forms.CharField(max_length=200)
    CATE=Cate.objects.all()
    file = forms.FileField()
    cate = forms.ModelChoiceField(queryset=CATE,empty_label='请选择分类')

