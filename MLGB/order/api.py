import datetime
import json
import requests

class WeChatSendMsg():
    def __init__(self):
        self.date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    def get_token(self):
        try:
            with open('/MLGB/access_token.txt', 'r') as f:
                content = f.read()
                print(content)
                data_dict = eval(content)
                time = datetime.datetime.strptime(data_dict["time"], '%Y-%m-%d %H:%M:%S')
            if (datetime.datetime.now() - time).seconds < 7000:
                print("未到两小时，从文件读取")
                return data_dict["access_token"]
            else:
                # 超过两小时，重新获取
                print("超过两小时，重新获取")
                payload = {
                    'grant_type': 'client_credential',
                    'appid': 'wx970cfc916de7fa67',
                    'secret': '21117902fe6ba659c1d05d59c7f6785f',
                }
                url = "https://api.weixin.qq.com/cgi-bin/token?"
                try:
                    respone = requests.get(url, params=payload, timeout=50)
                    access_token = respone.json().get("access_token")
                    content = "{'access_token':'" + str(access_token) + "','time':'" + str(
                        datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + "'}"
                    # 写入文件
                    with open('/MLGB/access_token.txt', 'w') as f:
                        f.write(content)
                    print("get_token", access_token)
                    return access_token
                except Exception as e:
                    print(e)
        except Exception as e:
            print("get_token,file", e)


    def post_data(self, data):
        # json_template = json.loads(data)
        # json_template = json.dumps(json_template)
        json_template = data.encode('utf-8')
        print('post微信接口数据:', json_template)
        access_token = self.get_token()
        url = "https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=" + access_token
        try:
            respone = requests.post(url, data=json_template, timeout=50)
            # 拿到返回值
            errcode = respone.json().get("errcode")
            if (errcode == 0):
                print("模板消息发送成功")
            else:
                print("模板消息发送失败")
        except Exception as e:
            print("微信返回报错:", e)