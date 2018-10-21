# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse,HttpResponseRedirect
from blog.models import Category,Post,Tag,Users
from comments.forms import CommentForm
from django.views.generic import ListView
from .forms import Subarticle,Login,Register
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
import markdown
# Create your views here.
app_name = 'blog'
class Index(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    #post_list = Post.objects.all().order_by("-create_time")
    #return render(request,"blog/index.html",context={"title":"欢迎你","post_list":post_list})
    paginate_by =  6
def detail(request,pk):
    post = get_object_or_404(Post,pk=pk)
    post.auto_increase_view()
    form = CommentForm()
    comment_list = post.comment_set.all()
    post.body = markdown.markdown(post.body,
                                  extensions=[
                                      'markdown.extensions.extra',
                                      'markdown.extensions.codehilite',
                                      'markdown.extensions.toc',]
                                  )
    context = {"form":form,"post":post,"comment_list":comment_list,"comment_count":post.comment_set.count()}
    return render(request,'blog/detail.html', context =context)

def archives(requset,year,month):
    post_list = Post.objects.filter(create_time__year = year,create_time__month = month).order_by('-create_time')
    return  render(requset,'blog/index.html',context={"post_list":post_list})
def category(request,pk):
    cate = get_object_or_404(Category,pk=pk)
    post_list = Post.objects.filter(category = cate).order_by('-create_time')
    return render(request,'blog/index.html',context={'post_list':post_list})

@login_required(login_url='/login/')
def sub_article(request):
    #这里需要保存用户名
    time = timezone.localtime(timezone.now()).strftime("%Y-%m-%d %H:%M:%S")
    super = User.objects.get(username=request.user)
    if super.is_superuser ==1:
        if request.method == "POST":
            form = Subarticle(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.author =request.user
                post.create_time = time
                post.modify_time = time
                post.save()
                return redirect(post.absolute_url())
            else:
                return render(request,'blog/subarticle.html',context={"form":form})
        else:
            form = Subarticle()
            return render(request,'blog/subarticle.html',context={"form":form})
    else:
        err_msg='你没有权限发布文章，如需发布，请联系管理员添加权限!'
        post_msg = ''
        return render(request,'blog/index.html',{'err_msg':err_msg,'post_msg':post_msg})
def user_space(request):
    post_list = Post.objects.filter(author = request.user).order_by('-create_time')
    return render(request,"blog/userspace.html",{'post_list':post_list})
from django.db.models import Q
def search(request):
    req = request.GET.get('q')
    err_msg = ''
    if not req:
        err_msg='未找到%s相关文章' %req
        return render(request,'blog/index.html',{'err_msg':err_msg})
    post_list = Post.objects.filter(Q(title__icontains=req)|Q(body__icontains=req))
    return render(request,'blog/index.html',{'post_list':post_list,'err_msg':err_msg})

def all_hot(request):
    post_list = Post.objects.all().order_by('-view')
    msg = '按阅读量排序'
    return render(request,'blog/index.html',{'post_list':post_list,'msg':msg})
def recent_post(request):
    post_list = Post.objects.all().order_by('-create_time')
    msg = '按发布时间排序'
    pagin= Paginator(post_list,6)
    page_obj = pagin.page(1)
    return render(request,'blog/index.html',{'post_list':post_list,'msg':msg,'page_obj':page_obj})









def login_blog(request):
    if request.method == "POST":
        uf = Login(request.POST)
        if uf.is_valid():
            username = uf.cleaned_data['username']
            passwd = uf.cleaned_data['password']
            user = authenticate(username=username, password=passwd)
            #user = User.objects.filter(username = username)
            if user:
                #passwd = User.objects.filter(username = username,passorwd = passwd)
                login(request,user)
                url = reverse('blog:user_space')
                return redirect(url)
            else:
                info = '登录失败，请检查用户名和密码！'
                messages.add_message(request,messages.WARNING,info)
                return render(request,'blog/login.html',context={"uf":uf})
        else:
            info = '登录失败'
            messages.add_message(request,messages.WARNING,info)
            return render(request,'blog/login.html',context={"uf":uf})
        #return HttpResponseRedirect(reverse("blog:login"))
    else:
        login = Login()
        return render(request,'blog/login.html',context={"login":login})

def register(request):
    if request.method == 'POST':
        user_form = Register(request.POST)
        if user_form.is_valid():
            user = user_form.save(commit = False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            return HttpResponseRedirect(reverse("blog:login"))
        else:
            return HttpResponse("注册失败")
    else:
        user_form = Register()
        return render(request,"blog/register.html",{"form":user_form})


