# coding: utf8

# import requests

# session = requests.session()
# session.headers["user-agent"] ="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"
# # session.headers[]
# res = session.post("https://www.zhihu.com/udid")
# print(res.text)
""""
# sopa 测试代码
from suds.client import Client
from suds.xsd.doctor import ImportDoctor,Import

# 添加默认的XMLSchema
imp = Import('http://www.w3.org/2001/XMLSchema', location='http://www.w3.org/2001/XMLSchema.xsd')
# 添加命名空间
imp.filter.add('http://WebXml.com.cn/')
doctor = ImportDoctor(imp)
# 用来发送webservice请求对象
# url是wsdl文档的全路径
client1 = Client('http://www.webxml.com.cn/WebServices/WeatherWebService.asmx?wsdl', doctor = doctor)
# 已函数的形式发送webservice接口请求
res = client1.service.getWeatherbyCityName('西安')
print(res)

# client = Client('http://47.105.110.138:8081/inter/SOAP?wsdl')
# res = client.service.auth()
# print(res)

header = {}
header["token"] = "a14d9124875948448f5041b0f56fdb7a"
client = Client('http://47.105.110.138:8081/inter/SOAP?wsdl',doctor=doctor, headers = header)
s = 'Tester、123456'
s = s.split('、')
res = client.service.login(*s)
print(res)
res = client.service.logout()
print(res)


from keywords.soapkeywords import SOAP
soap = SOAP()
soap.adddoctor("")
soap.setwsdl('http://47.105.110.138:8081/inter/SOAP?wsdl')
soap.callmethod('auth')
soap.savejson('token', 'token')
soap.addheader('token', '{token}')
soap.callmethod('login', 'Tester、123456')
soap.callmethod('logout')

"""
# import threading
# import os
# import time
#
# def run(cmd):
# 	res = os.system(cmd)
# 	print("子线程")
# 	return res
#
# c = "node C:/Users/007/AppData/Local/Programs/Appium/resources/app/node_modules/appium/build/lib/main.js"
# cmd = 'netstat -aon | findstr ' + '4723' + ' | findstr LISTENING'
#
# # 创建一个线程
# th = threading.Thread(target=run, args=(c,))
# th.start()
# print("主线程")
# time.sleep(6)
# res = run(cmd)
# print(res)
# print("启动完成")

from keywords.appkeywords import APP

app = APP()
app.runappium("C:/Users/007/AppData/Local/Programs/Appium", "4777",6)
config = '''{"platformName": "Android","platformVersion": "6.0.1","deviceName": "127.0.0.1:7555","appPackage": "com.provident.haocai","appActivity": "com.spring.table.main.SplashActivity","noReset": "true","unicodeKeyboard": "true",
            "resetKeyboard":"true"}'''
app.runapp(config,10)

app.click("com.provident.haocai:id/bt_cancel")

app.click("com.provident.haocai:id/tv_login")
app.input("com.provident.haocai:id/et_name", "hcfox")
app.input("com.provident.haocai:id/et_password", "qwe123")
app.click("com.provident.haocai:id/btn_login")

app.sleep(5)

app.click("com.provident.haocai:id/bt_cancel")
app.click("com.provident.haocai:id/ibn_home_menu")
app.click("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.support.v4.widget.DrawerLayout/android.widget.FrameLayout/android.support.v7.widget.RecyclerView/android.widget.LinearLayout/android.widget.LinearLayout/android.support.v7.widget.RecyclerView/android.widget.LinearLayout[10]")
app.click("com.provident.haocai:id/tvLeft")

app.colse()
