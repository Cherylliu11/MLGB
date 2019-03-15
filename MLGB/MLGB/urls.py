
"""MLGB URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import xadmin
from django.urls import path
from django.conf.urls import url, include
from django.views.static import serve
from django.views.generic import RedirectView
from users.views import LoginView, RegisterView,ActiveUserView, ForgetPwdView, ResetView, ModifyView
from order.views import ProductView
from MLGB.settings import MEDIA_ROOT


urlpatterns = [
    url(r'xadmin/', xadmin.site.urls),
    url(r'^favicon.ico$', RedirectView.as_view(url=r'static/images/favicon.ico')),
    url('^$', ProductView.as_view(), name="index"),
    url('^login/$', LoginView.as_view(), name="login"),
    url('^register/$', RegisterView.as_view(), name="register"),
    url(r'^upload/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
    url(r'^users/', include('users.urls', namespace="users")),
    url(r'^order/', include('order.urls', namespace="order")),
    url(r'^address/', include('address.urls', namespace="address")),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^active/(?P<active_code>.*)/$', ActiveUserView.as_view(), name="user_active"),
    url(r'^forget/', ForgetPwdView.as_view(), name='forget_pwd'),
    url(r'^reset/(?P<active_code>.*)/$', ResetView.as_view(), name='reset'),
    url(r'^modify/', ModifyView.as_view(), name='modify'),
]
