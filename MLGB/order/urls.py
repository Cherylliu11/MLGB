from django.conf.urls import url, include
from .views import CartUpdateView,CartView,SettlementView,CommitView,OrderInfoView,OrderListView,OrderCancelView,ClearCartView
urlpatterns = [
    #首页添加/减少商品按钮
    url(r'^add/$', CartUpdateView.as_view(), name="add"),
    #footer购物车
    url(r'^cart_list/$', CartView.as_view(), name="cart_add"),
    # 订单支付页面
    url(r'^settlement/$', SettlementView.as_view(), name="settlement"),
    url(r'^commit/$', CommitView.as_view(), name="commit"),
    url(r'^order_info/$', OrderInfoView.as_view(), name="order_info"),
    url(r'^order_list/$', OrderListView.as_view(), name="order_list"),
    url(r'^cancel/$', OrderCancelView.as_view(),name="cancel"),
    url(r'^clearcart/$', ClearCartView.as_view(), name="clearcart"),

]
app_name = 'order'
