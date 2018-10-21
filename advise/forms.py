__author__ = 'luohua139'
from django import forms
from .models import Advise
class MessageForm(forms.ModelForm):
    class Meta:
        model = Advise
        fields = ['advise']