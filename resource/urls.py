__author__ = 'luohua139'
from. import views
from django.conf.urls import url
app_name = 'resource'
urlpatterns = [
    #url(r'^comment/post/(?P<post_pk>[0-9]+)/$', views.post_comment, name='post_comment'),
    url(r'^upload/$',views.upload_file,name='upload'),
    url(r'^resoucre/$',views.dislpay_all_resource,name='all_resoucre'),
    url(r'^download/(?P<pk>[0-9]+)/$',views.download_file,name='download'),
    url(r'^searchresoucre/$',views.search_res,name='search_res'),
    url(r'^resoucer_cate/(?P<pk>[0-9]+)/$',views.categry,name='resoucer_cate')
]