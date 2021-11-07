# coding:utf-8

from keywords.httpkeywords import HTTP

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