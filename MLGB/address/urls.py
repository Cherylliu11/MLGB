from django.conf.urls import url, include
from .views import LocationView,ModifityAddrView,AddrListView,AddAddrView,DelAddrView

urlpatterns = [
    url(r'^location$', LocationView.as_view(), name="location"),
    url(r'^modifity_addr$', ModifityAddrView.as_view(), name="modifty_addr"),
    url(r'^addr_list$', AddrListView.as_view(), name="addr_list"),
    url(r'^add_addr$', AddAddrView.as_view(), name="add_addr"),
    url(r'^del_addr$', DelAddrView.as_view(), name="del_addr"),
]
app_name = 'address'
