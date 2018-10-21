__author__ = 'luohua139'
from django.conf.urls import url
from .import views
from  django.contrib.auth import  views as auth_views
app_name = 'blog'
urlpatterns = [
    url(r'^$',views.Index.as_view(),name='index'),
    url(r'^post/(?P<pk>[0-9]+)/$',views.detail,name='detail'),
    url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', views.archives, name='archives'),
    url(r'^category/(?P<pk>[0-9]+)/$', views.category, name='category'),
    url(r'^sub_article/$', views.sub_article, name='sub_article'),
    #url(r'^login/$',views.login_blog,name = 'login'),
    url(r'^login/$',auth_views.login,name = 'login'),
    url(r'^login/$',auth_views.login,{"template_name": "registration/login.html"}),
    url(r'^register/$',views.register,name = 'register'),
    url(r'logout/$',auth_views.logout,name = 'user_logout'),
    url(r'^userspace/$',views.user_space,name = 'user_space'),
    url(r'^search/$',views.search,name='search'),
    url(r'^allhot/$',views.all_hot,name='all_hot'),
    url(r'^recent/$',views.recent_post,name='recent_post')
]