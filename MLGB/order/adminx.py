import xadmin
from xadmin import views
from .models import ProductDetail, OrderInfo, OrderDetail

class OrderInline(object):
    model = OrderDetail
    extra = 0

class ProductAdmin(object):
    list_display = ['product_id', 'name', 'price', 'groups', 'description']
    search_fields = ['product_id', 'name']
    list_filter = ['groups']
    readonly_fields = ['product_id']
    model_icon = 'fa fa-shopping-cart'

#订单详情
class OrderDetailAdmin(object):
    list_display = ['order', 'product', 'count']
    search_fields = ['order', 'product']
    list_filter = ['order', 'product']
    model_icon = 'fa fa-list-ol'

#订单信息
class OrderInfoAdmin(object):
    list_display = ['order_id', 'user', 'total_count', 'total_price', 'status']
    search_fields = ['order_id', 'user']
    list_filter = ['status','user']
    readonly_fields = ['order_id']
    inlines = [OrderInline]
    model_icon = 'fa fa-list'

xadmin.site.register(ProductDetail, ProductAdmin)
xadmin.site.register(OrderInfo, OrderInfoAdmin)
xadmin.site.register(OrderDetail, OrderDetailAdmin)