# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
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
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired
from django.core.mail import send_mail
from django.conf import settings
from untils.celery_task import send_register_active_email
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import cache_page
# import sys
# reload(sys)
# sys.setdefaultencoding('utf8')
# Create your views here.
app_name = 'blog'

class Index(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    #post_list = Post.objects.all().order_by("-create_time")
    #return render(request,"blog/index.html",context={"title":"欢迎你","post_list":post_list})
    paginate_by =  6
    # def get(self, request, *args, **kwargs):
    #     if request.META.get('HTTP_X_FORWARDED_FOR'):
    #         ip = request.META['HTTP_X_FORWARDED_FOR']
    #     else:
    #         ip = request.META['REMOTE_ADDR']
    #     print(ip)
    #     return render(request,'blog/index.html')

@cache_page(10*60)
def detail(request,pk):
    post = get_object_or_404(Post,pk=pk)
    post.auto_increase_view()
    form = CommentForm()
    comment_list = post.comment_set.all()
    user = request.user
    try:
        #uu = User.objects.get(post__user_store=request.user)
        uu = user.post_store.get(pk=pk)

        msg = '已收藏'
    except:
        msg='收藏'
        print(msg)
    post.body = markdown.markdown(post.body,
                                  extensions=[
                                      'markdown.extensions.extra',
                                      'markdown.extensions.codehilite',
                                      'markdown.extensions.toc',]
                                  )
    context = {"form":form,"post":post,"comment_list":comment_list,"comment_count":post.comment_set.count(),'msg':msg}
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
@login_required(login_url='/login/')
def user_space(request):
    post_list = Post.objects.filter(author = request.user).order_by('-create_time')
    active = request.user.is_active
    return render(request,"blog/userspace.html",{'post_list':post_list,'active':active})
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
        uf = Login()
        return render(request,'blog/login.html',context={"uf":uf})

def register(request):
    if request.method == 'POST':
        user_form = Register(request.POST)
        user_profile = Users()
        if user_form.is_valid():
            username = request.POST.get('username')
            email =request.POST.get('email')
            password = request.POST.get('password')
            user = User.objects.create_user(username,email,password)
            user.is_active=0

            user.save()
            user_profile.user = user
            user_profile.nick_name = request.POST.get('nickname',None)
            user_profile.level = 0
            user_profile.save()
            #user = user_form.save(commit = False)
            #user.set_password(user_form.cleaned_data['password'])
            #user.save()
            ser = Serializer(settings.SECRET_KEY,7200)
            info = {'confirm':user.id}
            res = ser.dumps(info)
            res = res.decode()
            #发邮件
            subject = '从今天开始种树激活邮件'
            msg = ''
            html_msg ='<h1>%s,欢迎您成为今天开始种树会员</h1>请点击链接激活您的用户，激活后可任意下载资源<br/><a href = "http://127.0.0.1:8000/active/%s">http://127.0.0.1:8000/active/%s</a>' %(username,res,res)
            sender = settings.EMAIL_FROM
            emails = [email]
            #send_mail(subject,msg,sender,email,html_message=html_msg)
            send_register_active_email.delay(emails,username,res)
            return HttpResponseRedirect(reverse("blog:login"))
        else:
            return HttpResponse("注册失败")
    else:
        user_form = Register()
        return render(request,"blog/register.html",{"form":user_form})

def user_active(request,token):
    #token = token.decode()
    ser = Serializer(settings.SECRET_KEY,7200)
    try:
        res = ser.loads(token)
        id = res['confirm']
        user = User.objects.get(id =id)
        user.is_active = 1
        user.save()
        return redirect(reverse('blog:login'))
    except SignatureExpired as e:
        return HttpResponse('激活链接已过期')

def send_mail_to_active(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        user = User.objects.get(username=username)
        if user.is_active ==1:
            err_msg = '此账号已激活，请直接登录'
            return render(request,'blog/active.html',{'err_msg':err_msg})
        ser = Serializer(settings.SECRET_KEY,7200)
        info = {'confirm':user.id}
        res = ser.dumps(info)
        res = res.decode()
        #发邮件
        # subject = '从今天开始种树激活邮件'
        # msg = ''
        # html_msg ='<h1>%s,欢迎您成为今天开始种树会员</h1>请点击链接激活您的用户，激活后可任意下载资源<br/><a href = "http://127.0.0.1:8000/active/%s">http://127.0.0.1:8000/active/%s</a>' %(user.username,res,res)
        # sender = settings.EMAIL_FROM
        email = [user.email]
        # send_mail(subject,msg,sender,email,html_message=html_msg)
        send_register_active_email.delay(email,username,res)
        return HttpResponse('激活邮件已发送，请到邮箱激活！')
    else:
        return render(request,'blog/active.html')