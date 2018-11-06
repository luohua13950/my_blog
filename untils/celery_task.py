import redis
from celery import Celery
from django.conf import  settings
from django.core.mail import send_mail
import  os
import django
#初始化，不加celery会报错
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mypro.settings")
django.setup()
app = Celery('untils.celery_task',broker="redis://118.25.181.239:6379/1")

@app.task
def send_register_active_email(to_email,username,token):
    # 发邮件
    subject = '从今天开始种树激活邮件'
    msg = ''
    html_msg = '<h1>%s,欢迎您成为今天开始种树会员</h1>请点击链接激活您的用户，激活后可任意下载资源<br/><a href = "http://127.0.0.1:8000/active/%s">http://127.0.0.1:8000/active/%s</a>' % (
    username, token, token)
    sender = settings.EMAIL_FROM
    email = [to_email]
    send_mail(subject, msg, sender, email, html_message=html_msg)