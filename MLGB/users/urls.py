from django.conf.urls import url, include
from .views import UserinfoView,LogoutView
urlpatterns = [
    #用户信息
    url(r'^userinfo/$', UserinfoView.as_view(), name="user_info"),
    url(r'^logout/$', LogoutView.as_view(), name='logout')
    ]
app_name = 'users'
