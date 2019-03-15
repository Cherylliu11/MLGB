from django.shortcuts import render,redirect
from django.views.generic.base import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from .forms import LoginForm, RegisterForm,UserInfoForm,ForgetForm, ResetForm
from .models import UserProfile,EmailVerifyRecord
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from utils.mixin_utils import LoginRequiredMixin
from utils.email_send import send_register_email

#用户登录
class LoginView(View):
    def get(self, request):
        return render(request, "login.html", {})
    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect("/")
                else:
                    return render(request, "login.html", {"msg":"用户未激活!","username":user_name, "password":pass_word})
            else:
                return render(request, "login.html", {"msg":"用户名或密码错误!", "username":user_name, "password":pass_word})
        else:
            return render(request, "login.html", {"login_form":login_form})

class LogoutView(View):
    def get(self,request):
        logout(request)
        return render(request, 'index.html')

class UserinfoView(LoginRequiredMixin, View):
    """
    用户个人信息
    """
    def get(self, request):
        user = request.user
        if not user.is_authenticated:
            return render(request, "login.html", {})
        user_list = UserProfile.objects.get(id=user.id)
        return render(request, 'userinfo.html', {'user_list':user_list})
    def post(self, request):
        userinfo_form = UserInfoForm(request.POST)
        if userinfo_form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = request.user
            user = UserProfile.objects.get(id=user.id)
            if password != '':
                user.set_password(password)
            user.name = username
            user.save()
            return JsonResponse({'res':5, 'message':'保存成功'})
        else:
            message = userinfo_form.errors.as_json()
            return JsonResponse({'res':4, 'message':message})

class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, "register.html", {'register_form': register_form})
    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get("phonenum", "")
            if UserProfile.objects.filter(username=user_name):
                msg1 = "此手机号码已被注册！"
                return render(request, "register.html", {"register_form": register_form, "msg1": msg1})
            pass_word = request.POST.get("password", "")
            email = request.POST.get("email", "")
            if UserProfile.objects.filter(email=email):
                msg2 = "此邮箱已被注册，请换个邮箱重试！"
                return render(request, "register.html",
                              {"register_form": register_form, "msg2": msg2, "phonenum": user_name})
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.mobile = user_name
            user_profile.email = email
            user_profile.is_active = False
            user_profile.password = make_password(pass_word)
            user_profile.save()
            # 发送邮件代码start
            send_register_email(email, "register")
            return render(request, "register.html", {'register_form': register_form, "message": "　注册成功！ 请去邮箱激活"})
        else:
            return render(request, "register.html", {"register_form": register_form})

class ActiveUserView(View):
    """激活账户"""
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        return render(request, 'login.html')

class ForgetPwdView(View):
    def get(self, request):
        forget_form=ForgetForm()
        return render(request,"forgetPwd.html",{"forget_form":forget_form})
    def post(self, request):
        forget_form=ForgetForm(request.POST)
        if forget_form.is_valid():
            email=request.POST.get("email","")
            user = UserProfile.objects.filter(email=email)
            if user:
                send_register_email(email,"forget")
                return render(request,"forgetPwd.html",{"forget_form":forget_form,"message":" 重置密码邮件 已发送！" })
            else:
                return render(request,"forgetPwd.html", {"forget_form":forget_form, "msg":"此邮箱未注册！"})
        else:
            return render(request,"forgetPwd.html",{"forget_form":forget_form})

class ResetView(View):
    def get(self, request, active_code):
        record = EmailVerifyRecord.objects.filter(code=active_code)
        if record:
            for i in record:
                email=i.email
                is_register=UserProfile.objects.filter(email=email)
                status = i.status
                if status:
                    return HttpResponse("<h1>此密码重置链接已失效，请重新申请重置密码！</h1>")
                else:
                    if is_register:
                        i.status = True
                        i.save()
                        return render(request, "resetPwd.html", {"email": email})
                    else:
                        return HttpResponseRedirect("/forget")
        return HttpResponseRedirect("/forget")

class ModifyView(View):
    def post(self, request):
        reset_form=ResetForm(request.POST)
        print(reset_form)
        if reset_form.is_valid():
            pwd1 = request.POST.get("newpwd1","")
            print(pwd1)
            pwd2 = request.POST.get("newpwd2","")
            email = request.POST.get("email","")
            print(email)
            if pwd1 != pwd2:
                return render(request, "resetPwd.html", {"msg":"两次密码不一致!"})
            else:
                user=UserProfile.objects.get(email=email)
                user.password=make_password(pwd2)
                user.save()
                print("ok")
                return render(request, "resetPwd.html",{"message":"修改密码成功！请再次登录"})
        else:
            email=request.POST.get("email","")
            return render(request, "resetPwd.html", {"msg":reset_form.errors})



