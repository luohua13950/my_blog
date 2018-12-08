# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from blog.models import Post,Category,Tag,Users
from django.shortcuts import render,redirect,reverse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
import markdown
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
# Create your views here.
def knowledge_forum(request,pindex):
    cate = get_object_or_404(Category,name = "知识图谱")
    post = Post.objects.filter(category =cate).order_by('-create_time')
    paginator = Paginator(post,5)
    if pindex == "":
        pindex = 1
    page = paginator.page(int(pindex))
    return render(request,'knowledge/lis.html',{'post':post,'page':page,'paginator':paginator})

def post_detail(requset,pk):
    post = Post.objects.get(pk=pk)
    next_post = post.next_article()
    pre_post =  post.pre_article()
    post.auto_increase_view()
    comment_list = post.comment_set.all()
    post.body = markdown.markdown(post.body,
                                  extensions=[
                                      'markdown.extensions.extra',
                                      'markdown.extensions.codehilite',
                                      'markdown.extensions.toc',]
                                  )
    if pre_post and not next_post:
        next_post = '没有下一篇了'
    elif not pre_post and next_post:
        pre_post = '没有上一篇了'
    return render(requset,'knowledge/info.html',{'post':post,'next_post':next_post,'pre_post':pre_post,'comment_list':comment_list})
def author_recommend(requset):
    pass

def most_view(request):
    cate = get_object_or_404(Category, name="知识图谱")
    post_list = Post.objects.filter(category=cate).order_by('-view')
    return render(request,'knowledge/lis.html',{'post_list':post_list})

@csrf_exempt
@require_POST
@login_required(login_url='/login/')
def like_article(request):
    post_id = request.POST.get("id")
    action = request.POST.get("action")
    if post_id and action:
        try:
            post = Post.objects.get(id = post_id)
            if action == "like":
                post.user_like.add(request.user)
                return HttpResponse("1")
            else:
                post.user_like.remove(request.user)
                return HttpResponse("2")
        except Exception as e:
            return HttpResponse("no")

from django.db.models import Q
@require_POST
def knsearch(request):
    content = request.POST.get("keyboard")
    msg ,page= "",""
    try:
        page = Post.objects.filter(Q(body__icontains=content)|Q(title__icontains=content))
        msg = "共找到{}篇关于{}的文章".format(page.count(),content)
    except:
        msg = "没有找到关于{}的内容".format(content)
    return render(request,'knowledge/lis.html',{"err_msg":msg,"page":page})