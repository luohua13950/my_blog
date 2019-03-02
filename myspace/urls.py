from django.conf.urls import url
from .import views
app_name = 'myspace'
urlpatterns = [
    url(r'^myspace/$', views.my_space, name="my_space"),
    url(r'^mystore/$', views.my_store, name="my_store"),
    url(r'^myinfo/$', views.my_info, name="my_info"),
    url(r'^store/$', views.store_post, name="store_post"),
    url(r'^mypost/$', views.my_post, name='my_post'),
    url(r'^postdetail/$',views.post_detail,name='post_detail')
]