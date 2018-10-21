__author__ = 'luohua139'
from django import forms
class UploadForm(forms.Form):
    #title = forms.CharField(max_length=200)
    file = forms.FileField()
    cate = forms.CharField(max_length=100)