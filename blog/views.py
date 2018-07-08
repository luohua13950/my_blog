# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse
from blog.models import Category,Post,Tag,User
from comments.forms import CommentForm
from django.views.generic import ListView
from .forms import Subarticle,Login,Register
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
# Create your views here.
app_name = 'blog'
class Index(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    #post_list = Post.objects.all().order_by("-create_time")
    #return render(request,"blog/index.html",context={"title":"欢迎你","post_list":post_list})
def detail(request,pk):
    post = get_object_or_404(Post,pk=pk)
    post.auto_increase_view()
    form = CommentForm()
    comment_list = post.comment_set.all()
    context = {"form":form,"post":post,"comment_list":comment_list,"comment_count":post.comment_set.count()}
    return render(request,'blog/detail.html', context =context)

def archives(requset,year,month):
    post_list = Post.objects.filter(create_time__year = year,create_time__month = month).order_by('-create_time')
    return  render(requset,'blog/index.html',context={"post_list":post_list})
def category(request,pk):
    cate = get_object_or_404(Category,pk=pk)
    post_list = Post.objects.filter(category = cate).order_by('-create_time')
    return render(request,'blog/index.html',context={'post_list':post_list})

def sub_article(request):

    return render(request,'blog/subarticle.html')
def login(request):
    print 111
    if request.method == "POST":
        print 222222
        uf = Login(request.POST)
        print uf
        if uf.is_valid():
            print "dfafafafaa"
            username = uf.cleaned_data['user_name']
            passwd = uf.cleaned_data['pass_wd']
            user = User.objects.filter(user_name = username)
            print user
            if user:
                passwd = User.objects.filter(user_name = username,pass_wd = passwd)
                if passwd:
                    return redirect('/blog/')
            else:
                info = '登录失败，请检查用户名和密码！'
                messages.add_message(request,messages.WARNING,info)
                return render(request,'blog/login.html',context={"info":info})
        else:
            info = '登录失败，请检查用户名和密码！'
            messages.add_message(request,messages.WARNING,info)
            return render(request,'blog/login.html',context={"info":info})
    else:
        log = Login()
        info = '登录失败，请检查用户名和密码！'
        return render(request,'blog/login.html',context={"info":info})

def register(request):
    if request.method == "POST":
        res = Register(request.POST)
        if res.is_valid():
            username = res.cleaned_data['user_name']
            passwd = res.cleaned_data['pass_wd']
            user = User.objects.filter(user_name=username)
            if len(user) == 1:
                info = "用户已经存在！"
                messages.add_message(request,messages.WARNING,info)
                return render(request,'blog/register.html',{'info':info})
            else:
                user = User.objects.create(user_name = username,pass_wd = passwd)
                user.save()
                return redirect('/blog/')
    else:
        res = Register()
        info = "注册失败，请重新注册"
    return render(request,"blog/register.html",{"res":res})


