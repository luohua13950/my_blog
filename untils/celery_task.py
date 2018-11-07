import redis
from celery import Celery
from django.conf import  settings
from django.core.mail import send_mail
import  os
import django
#初始化，不加celery会报错
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mypro.settings")
django.setup()
app = Celery('untils.celery_task',broker="redis://:123456@118.25.181.239:6379/1")

@app.task
def send_register_active_email(to_email,username,token):
    # 发邮件
    subject = '从今天开始种树激活邮件'
    msg = ''
    html_msg = '<h1>%s,欢迎您成为今天开始种树会员</h1>请点击链接激活您的用户，激活后可任意下载资源<br/><a href = "http://www.happyhong.cn/active/%s">http://www.happyhong.cn/active/%s</a>' % (
    username, token, token)
    sender = settings.EMAIL_FROM
    send_mail(subject, msg, sender, to_email, html_message=html_msg)
    
@app.task
def upload(ff,path):
     with open(path, 'wb+') as f:
        for chunk in ff.chunks():
            f.write(chunk)
