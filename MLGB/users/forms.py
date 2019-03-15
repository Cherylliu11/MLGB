from django import forms
from captcha.fields import CaptchaField
from django.core import validators
from .models import UserProfile


class LoginForm(forms.Form):
    username = forms.CharField(label="用户名", error_messages={"required": u"手机号必填"})
    password = forms.CharField(label="密码", error_messages={"required": u"密码必填"}, min_length=6)


class RegisterForm(forms.Form):
    phonenum = forms.CharField(validators=[validators.RegexValidator(r'1[345678]\d{9}', message="请输入正确的手机号码")], label="用户名", error_messages={"required": u"手机号必填"})
    password = forms.CharField(label="密码", error_messages={"required": u"密码必填"}, min_length=6)
    email = forms.EmailField(error_messages={"required":u"邮箱必填"})
    captcha = CaptchaField(error_messages={"invalid":u"验证码错误"})

class UserInfoForm(forms.Form):
    username =  forms.CharField(max_length=5)
    password = forms.CharField(required=False,min_length=6)


class ModifyPwdForm(forms.Form):
    password1 = forms.CharField(required=True, min_length=6)
    password2 = forms.CharField(required=True, min_length=6)


class UploadImageForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image']



# forgetpwd中验证手机和验证码
class ForgetForm(forms.Form):
    email = forms.EmailField(required=True)
    captcha = CaptchaField(error_messages={"invalid": u"验证码错误"})


#reset.html中，用于验证新设的密码长度是否达标
class ResetForm(forms.Form):
    newpwd1=forms.CharField(required=True,min_length=6,error_messages={'required': '密码不能为空.', 'min_length': "至少6位"})
    newpwd2 = forms.CharField(required=True, min_length=6, error_messages={'required': '密码不能为空.', 'min_length': "至少6位"})
