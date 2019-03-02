from django.conf.urls import url
from .import views
app_name = 'onlinetools'
urlpatterns = [
    url(r'^pdfsplit/$',views.split_pdf,name="split_pdf"),

]