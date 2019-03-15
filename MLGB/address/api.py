import json
from urllib import request
from urllib.request import quote

class BaiDuMap():
    def __init__(self,origin_addr):
        self.origin_addr = origin_addr
        self.AK = "iAFRLmGl6E4o0DGT0zGmpq7IBpwKnh55"
    def getlnglat(self):
        url_geocoder = 'http://api.map.baidu.com/geocoder/v2/'
        url = url_geocoder + '?address=' + quote(self.origin_addr) + '&output=json' + '&ak=' + self.AK
        respponse = request.urlopen(url).read()
        result = json.loads(respponse.decode())
        status = result['status']
        if status == 0:
            lng = float('%.6f' % result['result']['location']['lng'])
            lat = float('%.6f' % result['result']['location']['lat'])
        origin=str(lat)+','+str(lng)
        return origin

    def ride_distance(self):
        destination="31.246997,121.445875"
        # destination = "31.214636,121.462323"
        origin = self.getlnglat()
        url_ride = "http://api.map.baidu.com/direction/v2/riding"
        url = url_ride + '?origin=' + origin + '&destination=' + destination + '&ak=' + self.AK
        response = request.urlopen(url).read()
        result_ride = json.loads(response.decode())
        status = result_ride['status']
        if status == 0:
            m_drive = result_ride['result']['routes'][0]['distance']
            timesec_drive = result_ride['result']['routes'][0]['duration']
            return {'m_drive':m_drive,'timesec_drive':timesec_drive}
        else:
            message=result_ride['message']
            return message

#
# map = BaiDuMap("长寿路-地铁站")
# res = map.ride_distance()
# print(res)