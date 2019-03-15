import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser

class UserProfile(AbstractUser):
    name = models.CharField(max_length=20, verbose_name="昵称", default="客户")
    mobile = models.CharField(max_length=11, verbose_name="手机号码")
    image = models.ImageField(upload_to="image/user",default="images/default.png", max_length=100)

    class Meta:
        verbose_name = "用户列表"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.username


class UserAddr(models.Model):
    id = models.AutoField(primary_key=True)
    list = (('M', '先生'), ('F', '女士'), ('S', '保密'))
    name = models.CharField(max_length=20, verbose_name="联系人")
    user = models.ForeignKey('UserProfile', on_delete=models.CASCADE, verbose_name='用户名')
    gender = models.CharField(max_length=2, blank=True, null=True, choices=list, default='S',verbose_name='性别')
    mobilephone = models.CharField(max_length=11,verbose_name='联系电话')
    address = models.CharField(max_length=255,verbose_name='门牌号')
    business = models.CharField(max_length=255, verbose_name='地址')
    tags = models.CharField(max_length=20, blank=True, null=True,verbose_name='标签')
    class Meta:
        db_table = 'user_addr'
        verbose_name = '用户详情'
        verbose_name_plural = verbose_name
    def __str__(self):
        return str(self.id)

class Resetpwd(models.Model):
    email = models.EmailField()
    resetStatus = models.BooleanField(default=False)
    class Meta:
        db_table='resetpwd'

class EmailVerifyRecord(models.Model):
    """邮箱激活码"""
    code = models.CharField(max_length=20, verbose_name='验证码')
    email = models.EmailField(max_length=50, verbose_name='邮箱')
    send_type = models.CharField(verbose_name='验证码类型', choices=(('register', '注册'), ('forget', '忘记密码')),max_length=20)
    send_time = models.DateTimeField(verbose_name='发送时间', default=datetime.datetime.now)
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name = '邮箱验证码'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{0}({1})'.format(self.code, self.email)
# Create your models here.
