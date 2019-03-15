from django.db import models
from django.utils import timezone

class OrderDetail(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey('OrderInfo', on_delete=models.CASCADE, verbose_name='订单ID')
    product = models.ForeignKey('ProductDetail', on_delete=models.DO_NOTHING, verbose_name='商品名称')
    count = models.IntegerField(verbose_name='商品数量')
    price = models.FloatField(blank=True, null=True, verbose_name='商品价格')

    class Meta:
        db_table = 'order_detail'
        verbose_name = '订单详情'
        verbose_name_plural = verbose_name
    def __str__(self):
        return str(self.order)

class OrderInfo(models.Model):
    list = (('1','等待商家接单'),('2','订单配送中'),('3','订单已送达'),('4','订单已取消'))
    order_id = models.CharField(max_length=128, primary_key=True, verbose_name='订单id')
    user = models.ForeignKey('users.UserProfile', on_delete=models.CASCADE, verbose_name='用户ID')
    order_time = models.DateTimeField(default=timezone.now, blank=True, null=True, verbose_name='下单时间')
    total_count = models.IntegerField(default=1, verbose_name='商品数量')
    total_price = models.FloatField(default=0,verbose_name='商品总价')
    coupon_id = models.IntegerField(blank=True, null=True, verbose_name='优惠券ID')
    name = models.CharField(max_length=20, null=True, verbose_name="联系人")
    mobilephone = models.CharField(max_length=11,null=True,verbose_name='联系电话')
    address = models.CharField(max_length=255,null=True,verbose_name='门牌号')
    business = models.CharField(max_length=255,null=True, verbose_name='地址')
    status = models.CharField(max_length=1, blank=True, null=True, choices=list, default='1', verbose_name='订单状态')
    class Meta:
        db_table = 'order_info'
        verbose_name = '订单列表'
        verbose_name_plural = verbose_name
    def __str__(self):
        return str(self.order_id)

class ProductDetail(models.Model):
    product_id = models.AutoField(primary_key=True, verbose_name='商品ID')
    name = models.CharField(max_length=30, verbose_name='商品名称')
    price = models.FloatField(blank=True, null=True, verbose_name='商品价格')
    groups = models.CharField(max_length=20, verbose_name='商品分类')
    description = models.CharField(max_length=255, blank=True, null=True, verbose_name='商品描述')
    image = models.ImageField(upload_to="product",default="default.png", max_length=100, verbose_name='产品图片')
    class Meta:
        db_table = 'product_detail'
        verbose_name = '商品列表'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name

# Create your models here.
