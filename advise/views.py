# -*- coding: utf-8 -*-
from __future__ import unicode_literals



# Create your views here.
from django.shortcuts import render
from advise.models import Advise
from advise.forms import MessageForm
from django.utils import timezone
# Create your views here.
def message_info(request):
    message_list = Advise.objects.all()
    if request.method == "POST":
        time = timezone.localtime(timezone.now()).strftime("%Y-%m-%d %H:%M:%S")
        form = MessageForm(request.POST)
        print(request.POST['advise'])
        if  form.is_valid():
            ad = Advise(advise = request.POST['advise'],user=request.user,sub_time=time)
            ad.save()
            return render(request,'advise/advise.html',{'form':form,'message_list':message_list})
    else:
        form  = MessageForm()
    return render(request,'advise/advise.html',{'form':form,'message_list':message_list})