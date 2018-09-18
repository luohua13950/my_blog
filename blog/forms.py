#-*-coding:utf-8 -*-
__author__ = 'luohua139'
from django import forms
from .models import Post,Users
from django.contrib.auth.models import User
class Subarticle(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title','body','category','tags']
        widgets = {'body':forms.Textarea(attrs={'class':'form-control','placeholder':u'正文'}),'title':forms.TextInput(attrs={'class':'form-control','placeholder':u'标题'
        }),}
class Login(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','password']
        widgets = {'password':forms.PasswordInput}
class Register(forms.ModelForm):
    password = forms.CharField(label="密码", widget=forms.PasswordInput)
    password2 = forms.CharField(label="重输密码", widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ["username", "email"]
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError("passwords do not match.")
        return cd['password2']