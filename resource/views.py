# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import  redirect,render,get_object_or_404
from  django.http import HttpResponse,FileResponse
from forms import  UploadForm
from mypro import settings
from models import Resource
import os,datetime
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.utils.encoding import escape_uri_path
from django.db.models import Q
from .models import Cate
# Create your views here.
@login_required(login_url='/login/')
def upload_file(request):
    username = request.user
    user=User.objects.get(username=username)
    now_time = timezone.localtime(timezone.now()).strftime("%Y-%m-%d %H:%M:%S")
    if request.method == "POST":
        form = UploadForm(request.POST,request.FILES)
        cate = Cate()
        cate.cate_name = request.POST['cate']
        cate.save()
        if form.is_valid:
            ff=request.FILES['file']
            try:
                path = os.path.join('upload',ff.name)
                if not os.path.isfile(path):
                    #os.mkdir(settings.MEDIA_ROOT)
                    with open(path,'wb+') as f:
                        for chunk in ff.chunks():
                            f.write(chunk)
                    Resource.objects.create(res_name=ff.name,upload_url=path,upload_user=user,create_time=now_time,size=ff.size,cate=cate)
                else:
                    err_msg = '此文件名的文件已被其它用户上传，如继续上传请更改文件名！'
                    form = UploadForm()
                    return render(request,'resoucre/upload.html',{'err_msg':err_msg,'form':form})
            except Exception as e:
                print(e)
            return redirect('/resoucre/')
    else:
        form = UploadForm()
    return render(request,"resoucre/upload.html",{"form":form})

@login_required(login_url='/login/')
def download_file(resquest,pk):
    try:
        res =Resource.objects.get(id=pk)
        res.downlaod_count()
        file = open(res.upload_url,'rb')
        response = FileResponse(file)
        filename = os.path.basename(res.upload_url)
        response['Content-Type']='application/octet-stream'
        response['Content-Disposition']="attachment;filename*=utf-8''{0}".format(escape_uri_path(filename))
        return response
    except Exception as e:
        return HttpResponse('文件不存在或被删除，如需继续下载请在优化建议留言！')

def dislpay_all_resource(request):
    res_list = Resource.objects.all()
    return render(request,'resoucre/display.html',{'res_list':res_list})

def search_res(request):
    search = request.GET.get('q')
    post_list = Resource.objects.filter(res_name__icontains=search)
    err_msg = ''
    post_msg = ''
    if not post_list:
        err_msg='未找到%s相关资源' %search
        return render(request,'blog/index.html',{'err_msg':err_msg})
    return render(request,'blog/index.html',{'post_list':post_list,'err_msg':err_msg,'post_msg':post_msg})

def categry(request,pk):
    post_list = Resource.objects.filter(id=pk).order_by('-create_time')
    return render(request,'resoucre/src.html',{'post_list':post_list})
