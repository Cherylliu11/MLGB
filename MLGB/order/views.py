from django.shortcuts import render
from django.views.generic import View
from django.db import transaction
from django.http import JsonResponse, request,HttpResponseRedirect
from django_redis import get_redis_connection
from django.http import HttpResponse
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import login_required
from .models import ProductDetail,OrderInfo,OrderDetail
from users.models import UserAddr
from datetime import datetime
from .api import WeChatSendMsg
from address.api import BaiDuMap
import json
import time
from django.views.decorators.csrf import csrf_exempt

# 访问首页时传递所有商品列表、购物车商品总数及总价
class ProductView(View):
    def get(self,request):
        #从mysql获取商品列表
        all_product = ProductDetail.objects.values('product_id','name', 'price', 'image', 'groups')
        # 获取登录的用户
        user = request.user
         # 从redis获取用户购物车中商品的信息
        conn = get_redis_connection('default')
        total_count = 0
        total_price = 0
        #判断用户是否登录
        if not user.is_authenticated:
            pass
        else:
            cart_key = 'cart_%d'%user.id
            # {'商品id':商品数量, ...}
            cart_dict = conn.hgetall(cart_key)
            # 遍历获取购物车商品的信息
            for cart_product_id, count in cart_dict.items():
                # 根据商品的id获取商品的信息
                product_detail = ProductDetail.objects.get(product_id=cart_product_id)
                # 计算购物车商品的总数和总价
                amount = product_detail.price*int(count)
                total_count += int(count)
                total_price += amount
        context = {'product_list':all_product,'total_count': total_count,'total_price': total_price,}

        #返回所有商品列表、购物车商品总数及总价
        return  render(request, "index.html", context)

class CartView(View):
    def get(self,request):
        # 获取登录的用户
        user = request.user
        if not user.is_authenticated:
            return render(request, "login.html", {})
        # 从redis获取用户购物车中商品的信息
        conn = get_redis_connection('default')
        cart_key = 'cart_%d'%user.id
        # {'商品id':商品数量, ...}
        cart_dict = conn.hgetall(cart_key)
        json_list = []
        cart = {}

        # 遍历获取商品的信息
        for cart_product_id, count in cart_dict.items():
            if count == 0:
                print('删除为0数据')
                conn.delete(cart_key,cart_product_id)
            # 根据商品的id获取商品的信息
            product_detail = ProductDetail.objects.get(product_id=cart_product_id)
            cart['name'] = product_detail.name
            # 计算商品的小计
            amount = product_detail.price*int(count)
            cart['amount'] = amount
            cart['id'] = cart_product_id.decode()
            cart['count'] = int(count)
            cart['price'] =product_detail.price
            #拼接购物车中商品信息字典至json_list中
            json_list.append(cart.copy())
            #以json格式返回购物车中商品名字、总价、id、数量、价格
        return HttpResponse(json.dumps(json_list), content_type="application/json")

# 更新购物车记录
# 采用ajax post请求
# 前端需要传递的参数:商品id(sku_id) 更新的商品数量(count)
# /cart/update
class CartUpdateView(View):
    '''购物车记录更新'''
    def post(self, request):
        user = request.user
        if not user.is_authenticated:
            return render(request, "login.html", {})
        # 接收数据
        product_id = request.POST.get('product_id')
        count = request.POST.get('count')
        # print(product_id,count)
        # 数据校验
        if not all([product_id, count]):
            return JsonResponse({'res': 1, 'errmsg': '数据不完整'})
        # 校验添加的商品数量
        try:
            count = int(count)
        except Exception as e:
            # 数目出错
            return JsonResponse({'res': 2, 'errmsg': '商品数目出错'})

        # 校验商品是否存在
        try:
            product = ProductDetail.objects.get(product_id=product_id)
        except  ProductDetail.DoesNotExist:
            return JsonResponse({'res':3, 'errmsg':'商品不存在'})

        # 业务处理:更新购物车记录
        conn = get_redis_connection('default')
        cart_key = 'cart_%d'%user.id
        conn.hincrby(cart_key, product_id, count)
        # 计算用户购物车中商品的总件数 {'1':5, '2':3}
        cart_dict = conn.hgetall(cart_key)
        for cart_product_id, count in cart_dict.items():
            #数量为0的商品不显示
            if int(count) == 0:
                conn.hdel(cart_key,cart_product_id)
        total_count = 0
        vals = conn.hvals(cart_key)
        for val in vals:
            total_count += int(val)
        # 返回应答
        return JsonResponse({'res':4, 'total_count':total_count, 'message':'添加成功'})

class SettlementView(View):
    def get(self,request):
        user = request.user
        if not user.is_authenticated:
            return render(request, "login.html", {})
        # 从redis获取用户购物车中商品的信息
        addr_id = request.GET.get("addrid")
        conn = get_redis_connection('default')
        cart_key = 'cart_%d' % user.id
        # {'商品id':商品数量, ...}
        cart_dict = conn.hgetall(cart_key)
        cart_list = []
        cart = {}

        # 遍历获取购物车商品的信息
        total_amount = 0
        for cart_product_id, count in cart_dict.items():
            if count == 0:
                print('删除为0数据')
                conn.delete(cart_key,cart_product_id)
            # 根据商品的id获取商品的信息
            product_detail = ProductDetail.objects.get(product_id=cart_product_id)
            cart['name'] = product_detail.name
            # 计算商品的小计
            amount = product_detail.price*int(count)
            cart['price'] = product_detail.price
            cart['amount'] = amount
            cart['id'] = cart_product_id.decode()
            cart['count'] = int(count)
            total_amount += amount
            cart_list.append(cart.copy())
        if addr_id:
            addr = UserAddr.objects.filter(user=user.id,id=addr_id).first()
            try:
                map = BaiDuMap(addr.business)
                res = map.ride_distance()
                addr_dict = model_to_dict(addr)
                time_now = time.time()
                estimate_timeStamp = time_now + res['timesec_drive'] + 900
                st = time.localtime(estimate_timeStamp)
                estimate = time.strftime('%H:%M', st)
                addr_dict['estimate'] = estimate
            except Exception as e:
                print(e)
                addr_dict= {}
        else:
            #显示距离最近的地址
            addr_list = UserAddr.objects.filter(user=user.id)
            nearest_addr = 5000
            for addr in addr_list:
                try:
                    map = BaiDuMap(addr.business)
                    res = map.ride_distance()
                    if res['m_drive'] < nearest_addr:
                        nearest_addr = res['m_drive']
                        addr_dict  = model_to_dict(addr)
                        time_now = time.time()
                        estimate_timeStamp  = time_now + res['timesec_drive'] + 900
                        st = time.localtime(estimate_timeStamp)
                        estimate = time.strftime('%H:%M', st)
                        addr_dict['estimate'] = estimate
                except Exception as e:
                    print(e)
            if nearest_addr == 5000:
                addr_dict= {}
        params={'list': cart_list,'total_amount':total_amount,'addr':addr_dict}
        return  render(request, "settlement.html", params)

class CommitView(View):
    #处理提交订单
    @transaction.atomic
    def post(self,request):
        # 判断用户是否登录
        user = request.user
        addr_id = request.POST.get("addr_id")
        if not user.is_authenticated:
            return render(request, "login.html", {})
        if not all([addr_id]):
            return JsonResponse({'res':1, 'errmsg':'参数不完整'})
        order_id = datetime.now().strftime('%Y%m%d%H%M%S')+str(user.id)
        total_count = 0
        total_price = 0
        try:
            addr = UserAddr.objects.get(id=addr_id)
        except UserAddr.DoesNotExist:
            # 地址不存在
            return JsonResponse({'res':3, 'errmsg':'收货地址错误'})
        save_id = transaction.savepoint()
        try:
            order = OrderInfo.objects.create(order_id = order_id,
                                             user = user,
                                             name = addr.name,
                                             mobilephone = addr.mobilephone,
                                             address = addr.address,
                                             business = addr.business,
                                             total_count = total_count,
                                             total_price = total_price)
            conn = get_redis_connection('default')
            cart_key = 'cart_%d' % user.id
            cart_dict = conn.hgetall(cart_key)
            if not cart_dict:
                return JsonResponse({'res': 6, 'errmsg': '购物车里没有商品'})
            for product_id in cart_dict:
                try:
                    product = ProductDetail.objects.select_for_update().get(product_id=product_id)
                except:
                    # 商品不存在
                    transaction.savepoint_rollback(save_id)
                    return JsonResponse({'res':4, 'errmsg':'商品不存在'})
                count = conn.hget(cart_key, product_id)
                OrderDetail.objects.create(order = order,
                                           product = product,
                                           count = count,
                                           price = product.price)

                amount = product.price * int(count)
                total_count += int(count)
                total_price += amount
            order.total_count = total_count
            order.total_price = total_price
            order.save()
        except Exception as e:
            print(e)
            transaction.savepoint_rollback(save_id)
            return JsonResponse({'res':7, 'errmsg':'下单失败'})

        # 提交事务
        transaction.savepoint_commit(save_id)
        #发送微信通知
        keyword5 = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        data_dict = '{"touser": "oozmb1TMBks6dACCBMOmazezP7JM",' \
                    ' "template_id": "DB60TlrDc7w1buT395LR_kawVmV3GWJdP16kwvS-N20",' \
                    ' "data": {"first": {"value": "您有新订单了!", "color": "#173177"}, ' \
                    '"productType": {"value": "产品类型", "color": "#173177"}, ' \
                    '"keyword1": {"value": "' + order_id + '", "color": "#173177"}, ' \
                    '"keyword2": {"value": "' + addr.name + '", "color": "#173177"}, ' \
                    '"keyword3": {"value": "等待商家接单", "color": "#173177"}, ' \
                    '"keyword4": {"value": "无", "color": "#173177"}, ' \
                    '"keyword5": {"value": "' + keyword5 + '", "color": "#173177"}, ' \
                    '"remark": {"value": "", "color": "#173177"}}}'
        my_wechat = WeChatSendMsg()
        my_wechat.post_data(data_dict)

        # 清除用户购物车中对应的记录
        conn.delete(cart_key,cart_dict.keys())

        # 返回应答
        return JsonResponse({'res':5, 'message':'下单成功','orderid':order_id})


class OrderInfoView(View):
    def get(self,request):
        user = request.user
        orderid = request.GET.get("orderid")
        if orderid:
            order_info = OrderInfo.objects.filter(order_id=orderid,user=user.id)
            order_list = OrderDetail.objects.select_related('product').filter(order_id=orderid)
            product_dict_list=[]
            for product_info in order_list:
                product_dict={}
                product_dict['name']=product_info.product.name
                product_dict['count']=product_info.count
                product_dict['amount']=product_info.price*product_info.count
                product_dict_list.append(product_dict.copy())
            return render(request, "order_info.html",{'order_info': order_info[0], 'order_list': product_dict_list,'order_id':orderid})
        else:
            return HttpResponseRedirect('/order/order_list')

class OrderListView(View):
    def get(self,request):
        user = request.user
        current_order = OrderInfo.objects.filter(user=user.id,status__in=[1,2]).order_by('-order_id')
        history_order = OrderInfo.objects.filter(user=user.id,status__in=[3,4]).order_by('-order_id')[:10]
        return render(request,"order_list.html",{'current_order':current_order,'history_order':history_order})


class OrderCancelView(View):
    def post(self,request):
        orderid = request.POST.get("order_id")
        order = OrderInfo.objects.get(order_id=orderid)
        if order:
            order.status = '4'
            order.save()
            return JsonResponse({'res':5, 'message':'取消成功'})
        else:
            return JsonResponse({'res':3, 'errmsg':'取消失败'})

class ClearCartView(View):
    def get(self,request):
        user = request.user
        if not user.is_authenticated:
            return render(request, "login.html", {})
        # 从redis获取用户购物车中商品的信息
        conn = get_redis_connection('default')
        cart_key = 'cart_%d'%user.id
        conn.delete(cart_key)
        return JsonResponse({'res':5, 'message':'清空成功'})
