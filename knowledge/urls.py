__author__ = 'luohua139'
from. import views
from django.conf.urls import url
app_name = 'knowledge'
urlpatterns = [
    url(r'^knowledge/(?P<pindex>[0-9]+)/$', views.knowledge_forum, name='knowledge'),
    url(r'^details/(?P<pk>[0-9]+)/$',views.post_detail,name='details'),
    url(r'^author_recommend/$',views.author_recommend,name='recommend'),
    url(r'^most_view/$',views.most_view,name='most_view'),
    url(r'^like_article/$',views.like_article,name='like_article'),
    url(r'^knsearch/$',views.knsearch,name="knsearch"),
]