from django.shortcuts import render
from blog.models import Post,Users,Category,Tag
from django.contrib.auth.views import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse

import markdown
from untils.get_ip import ip_belong,get_ip
from django.views.decorators.cache import cache_page
# Create your views here.
@login_required(login_url='/login/')
def my_space(request):
    user = request.user
    try:
        user_prof = Users.objects.get(user=user)

    except Exception as e:
        user_prof = Users(user=user,nick_name='游客',level=0)
        user_prof.save()
    return render(request,"my_space.html",{"user":user,"user_prof":user_prof,})


@login_required(login_url='/login/')
@csrf_exempt
def store_post(request):
    user = request.user
    msg = "收藏"
    id = request.POST.get("id")
    if id:
        post = Post.objects.get(id=id)
        try:
            #ret = User.objects.get(post__user_store=user)
            uu = user.post_store.get(pk=id)
            post.user_store.remove(user)
            msg = "收藏"
            return JsonResponse({'status': 'cancel','msg':msg })
        except Exception as e:
            msg = "已收藏"
            post.user_store.add(user)
    return JsonResponse({'status':'ok','msg':msg })

@cache_page(10*60)
@login_required(login_url='/login/')
def my_store(request):
    user = request.user
    user_prof = Users.objects.get(user=user)
    try:
        post_list = user.post_store.all()
    except Exception as e:
        post=''
    return render(request,"myspace/mystore.html",{"user":user,"post_list":post_list,'user_prof':user_prof})

@cache_page(10*60)
@login_required(login_url='/login/')
def my_info(request):
    user = request.user
    ip = get_ip(request)
    region = ip_belong(ip)
    save_region = ''
    try:
        user_prof = Users.objects.get(user=user)
    except Exception as e:
        user_prof = Users(nick_name='游客',level=0)
        user_prof.save()
    try:
        last_login_ip = user_prof.last_login_ip
    except Exception as e:
        last_login_ip = ''
    last_region = ip_belong(last_login_ip)
    if last_login_ip:
        if ip == last_login_ip:
            save_region = region
        else:
            #last_region = ip_belong(last_login_ip)
            user_prof.last_login_ip = ip
            if last_region != region:
                save_region = region + '上次登录为:（%s）' % last_region
            else:
                save_region = region
    else:
        user_prof.last_login_ip = ip
        save_region = last_region

    msg = ""
    nickname = request.POST.get("nickname", None)
    email = request.POST.get("email", None)
    if request.method == "POST":
        if nickname and email:
            user_prof.nick_name=nickname
            user.email = email
            user.save()
            user_prof.save()
            msg = "修改成功"
        else:
            msg = "修改不成功，请稍后再试！"
    return render(request,"myspace/myinfo.html",{"user":user,"user_prof":user_prof,"msg":msg,"region":save_region})

@cache_page(10*60)
def my_post(request):
    user=request.user
    user_prof = Users.objects.get(user=user)
    post_list = Post.objects.filter(author=user)

    return render(request,'myspace/mystore.html',{'post_list':post_list,"user_prof":user_prof})

def post_detail(request):
    pass