__author__ = 'luohua139'
from django import forms
from .models import Post,User

class Subarticle(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title','body','category','tags','author']
        forms.Textarea
        widgets = {
            'body': forms.Textarea(attrs={'cols': 80, 'rows': 20}),
        }
class Login(forms.ModelForm):
    class Meta:
        model = User
        fields = ['user_name','pass_wd']
class Register(forms.ModelForm):
    class Meta:
        model = User
        fields = ['user_name','pass_wd']

