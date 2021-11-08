# coding:utf-8


import requests
import json
import re
import inspect

from keywords.httpkeywords import HTTP


#post请求测试代码
http = HTTP()
#鉴权
url = "http://47.105.110.138:8081/inter/HTTP/auth"
http.post(url)
http.savejson("t","token")
http.addheaders("token",'{t}')
print(http.session.headers)
#登录
url = "http://47.105.110.138:8081/inter/HTTP/login"
data = "username=Will666&password=123456"
http.post(url, data=data)
http.assertequals('status',200)

http.savejson("id", "userid")
url = "http://47.105.110.138:8081/inter/HTTP/getUserInfo"
data = "id={id}"

http.post(url, data =data)
http.assertequals("status", 200)

http.post("http://47.105.110.138:8081/inter/HTTP/logout")
http.assertequals("status", 200)




#反射测试代码
a= 'post'
http = HTTP()
func = getattr(http, a)
print(func)

func("http://47.105.110.138:8081/inter/HTTP/auth")
args = inspect.getfullargspec(func).__str__()
print(args)
args = args[args.find("args=")+5:args.find(", varargs=None")]
print(args)
b = ['', '', '设置地址', 'seturl', 'http://47.105.110.138:8081/inter/HTTP/auth', '', '', '', '']
args = eval(args)
args.remove("self")
l = len(args)

# args = re.findall("\(args=(.*?), varargs",args)
print(l)

if l < 1:
	func()

if l < 2:
	func(b[4])

if l < 3:
	func(b[4], b[5])