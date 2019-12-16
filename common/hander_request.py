"""
============================
Author  : XiaoLei.Du
Time    : 2019/12/3 16:34
E-mail  : 506615839@qq.com
File    : hander_request.py
============================
"""
'''
封装的目的：
    为了使用的时候更方便，提高代码的重用率

封装的需求：
    发送post请求，，发送get请求，发送patch请求，
    代码中如何做到不同请求方式的接口去发送不同的请求
    加判断
'''
import requests
class HanderRequest:

    def send(self,url,method,data=None,json=None,params=None,headers=None):
        method=method.lower()
        if method=='post':
            return requests.post(url=url,json=json,data=data,headers=headers)
        elif method=='patch':
            return requests.patch(url=url,json=json,data=data,headers=headers)
        elif method=='get':
            return requests.get(url=url,params=params)

class handerSessionRequest:
    def __init__(self):
        self.se=requests.session()

    def send(self,url,method,data=None,json=None,params=None,headers=None):
        method=method.lower()
        if method=='post':
            return self.se.post(url=url,json=json,data=data,headers=headers)
        elif method=='patch':
            return self.se.patch(url=url,json=json,data=data,headers=headers)
        elif method=='get':
            return self.se.get(url=url,params=params)

if __name__ == '__main__':
    login_url = 'http://api.lemonban.com/futureloan/member/login'
    login_data = {
        "mobile_phone": "13641878111",
        "pwd": "12345678",
    }
    login_header = {
        "X-Lemonban-Media-Type": "lemonban.v1"
    }

    res=HanderRequest()
    r=res.send(login_url,method='post',json=login_data,headers=login_header)
    print(r.json())
