from django.shortcuts import render,redirect,reverse
from django.views.generic import View
from django.http import HttpResponseRedirect,JsonResponse
from django.forms.models import model_to_dict
from users.models import UserAddr
from .api import BaiDuMap

# Create your views here.
class LocationView(View):
    def get(self,request):
        url = request.path_info
        return render(request, "location.html")

class ModifityAddrView(View):
    def get(self,request):
        user = request.user
        addr_id = request.GET.get("addrid")
        addr_info = UserAddr.objects.filter(id=addr_id,user=user.id).values('name','mobilephone','address','business')
        addr_list = list(addr_info)
        if not addr_info:
            return HttpResponseRedirect('addr_list')
        else:
            return render(request, "modifity_addr.html",{'addr_info_dict':addr_list[0],'addr_id':addr_id})
    def post(self,request):
        id = request.POST.get("addr_id")
        name = request.POST.get("name")
        mobilephone = request.POST.get("mobilephone")
        business = request.POST.get("business")
        address = request.POST.get("address")
        if not all([id,name,mobilephone,business,address]):
            return JsonResponse({'res': 1, 'errmsg': '请填写完整'})
        UserAddr.objects.filter(id = id).update(name = name, mobilephone = mobilephone,business = business,address = address)
        return JsonResponse({'res':5, 'message':'保存成功'})

class AddrListView(View):
    def get(self,request):
        user = request.user
        range_check = request.GET.get("range_check")
        addr_list = UserAddr.objects.filter(user=user.id)
        in_range_list = []
        outof_range_list = []
        if range_check == '1':
            for addr in addr_list:
                try:
                    map = BaiDuMap(str(addr.business))
                    res = map.ride_distance()
                    if res['m_drive'] < 5000:
                        in_range_list.append(addr)
                    else:
                        outof_range_list.append(addr)
                except Exception as e:
                    print(e)
                    outof_range_list.append(addr)

            return  render(request, "addr_list.html", {'in_range_list':in_range_list,'outof_range_list':outof_range_list})
        else:

            return render(request, "addr_list.html", {'in_range_list':addr_list})

class AddAddrView(View):
    def get(self,request):
        return render(request,"add_addr.html")
    def post(self,request):
        user = request.user
        name = request.POST.get("name")
        mobilephone = request.POST.get("mobilephone")
        business = request.POST.get("business")
        address = request.POST.get("address")
        if not all([name,mobilephone,business,address]):
            return JsonResponse({'res': 1, 'errmsg': '请填写完整'})
        UserAddr.objects.create(user_id = user.id,name = name, mobilephone = mobilephone,business = business,address = address)
        return JsonResponse({'res':5, 'message':'新增成功'})

class DelAddrView(View):
    def post(self,request):
        user = request.user
        addr_id = request.POST.get("addr_id")
        try:
            UserAddr.objects.filter(id=addr_id,user=user.id).delete()
            return JsonResponse({'res': 5, 'message': '删除成功'})
        except Exception as e:
            print(e)
            return JsonResponse({'res': 1, 'errmsg': '删除失败'})