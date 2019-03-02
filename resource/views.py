# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import  redirect,render,get_object_or_404
from  django.http import HttpResponse,FileResponse
from .forms import  UploadForm
from mypro import settings
from .models import Resource
from blog.models import Users
import os,datetime
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.utils.encoding import escape_uri_path
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Cate
#from untils.celery_task import upload
# Create your views here.
PATH = "/home/luohua/upload/"
@login_required(login_url='/login/')
def upload_file(request):
    username = request.user
    user_prof=Users.objects.get(user=username)
    user=User.objects.get(username=username)
    now_time = timezone.localtime(timezone.now()).strftime("%Y-%m-%d %H:%M:%S")
    err_msg = ''
    #print(request.POST['cate'])
    if request.method == "POST":
        form = UploadForm(request.POST,request.FILES)
        if form.is_valid():
            tt = form.cleaned_data['cate']
            cate = Cate.objects.get(cate_name=tt)
            ff=request.FILES['file']
            name = ff.name
            try:
                #path = os.path.join('upload',name)
                path = os.path.join(PATH,name)
                if not os.path.isfile(path):
                    os.mkdir(settings.MEDIA_ROOT)
                    with open(path,'wb+') as f:
                        for chunk in ff.chunks():
                            f.write(chunk)
                    #upload.delay(ff,path)
                    Resource.objects.create(res_name=ff.name,upload_url=path,upload_user=user,create_time=now_time,size=ff.size,cate=cate)
                else:
                    err_msg = '此文件名的文件已被其它用户上传，如继续上传请更改文件名！'
                    form = UploadForm()

            except Exception as e:
                print(e)
            return redirect('/resoucre/')
    else:
        form = UploadForm()
    return render(request, 'resoucre/upload.html', {'err_msg': err_msg, 'form': form,'user_prof':user_prof})

#@login_required(login_url='/login/')
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

def dislpay_all_resource(request,pindex):
    res = Resource.objects.all()
    paginator = Paginator(res,6)
    if pindex=='':
        pindex=1
    res_list = paginator.page(int(pindex))
    return render(request,'resoucre/display.html',{'res_list':res_list,'paginator':paginator})

def search_res(request):
    search = request.GET.get('q')
    res_list = Resource.objects.filter(res_name__icontains=search)
    err_msg = ''
    if not res_list:
        err_msg='未找到%s相关资源' %search
        return render(request,'resoucre/display.html',{'err_msg':err_msg})
    post_msg = '找到了吗'
    return render(request,'resoucre/display.html',{'res_list':res_list,'err_msg':err_msg,'post_msg':post_msg})

def categry(request,pk):
    cate = Cate.objects.get(id=pk)
    general = cate.cate_name
    res_list = Resource.objects.filter(cate=cate).order_by('-create_time')
    return render(request,'resoucre/display.html',{'res_list':res_list,'general':general})

def recent_resource(request,pindex):
    res = Resource.objects.all().order_by("-create_time")
    general = "按发布时间排序"
    paginator = Paginator(res,6)
    if pindex=='':
        pindex=1
    res_list = paginator.page(int(pindex))
    return render(request,'resoucre/display.html',{"res_list":res_list,'general':general,"paginator":paginator})
def hot_resource(request,pindex):
    res = Resource.objects.all().order_by("-download")
    general = "按下载量排序"
    paginator = Paginator(res,6)
    if pindex=='':
        pindex=1
    res_list = paginator.page(int(pindex))
    return render(request,'resoucre/display.html',{"res_list":res_list,'general':general,"paginator":paginator})