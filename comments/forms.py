__author__ = 'luohua139'
from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        #fields = ['name','email','url','text']
        #fields = ['name','email','text']
        fields = ['text']
