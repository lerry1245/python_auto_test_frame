# conding: uft-8

import requests
import json

# 创建已http接口请求关键字类
class HTTP:

	# 构造函数，实例化实例变量
	def __init__(self):
		#创建session对象，模拟浏览器的cookie管理
		self.session = requests.session()
		#存放json解析后的结果
		self.json_res = {}
		self.params = {}

	# 定义post实例方法，用来发送post请求
	def post(self, path, data=None):
		"""

		:param path: post的访问接口路径
		:param data: 接口需要传入的参数类型为str
		:return:
		"""
		if data is None:
			res = self.session.post(path)
		else:
			# 替换参数
			data = self.__getparams(data)
			# 替换后的参数转换为字典
			data = self.__todict(data)
			res = self.session.post(path, data=data)
		print(res.text)
		self.json_res = json.loads(res.text)

	# 定义断言相等的关键字，用来判断接送的可以对应的值和期望值相等
	def assertequals(self,key,value):
		"""
		:param key: 需要断言self.json_res的key值
		:param value: 断言的预期结果值
		:return:
		"""
		if str(self.json_res[key]) == str(value):
			print("PASS")
		else:
			print("FAIL")

	# 给头添加一个键值对关键字
	def addheaders(self, key, value):
		"""
		:param key: 添请求加头的键
		:param value: 添加请求头的值
		:return:
		http.savejson("t","token")
		http.addheaders("token",'{t}')
		"""
		value = self.__getparams(value)
		self.session.headers[key] = value

	def savejson(self, p, key):
		"""
		:param p:
		:param key:
		:return:
		"""
		self.params[p] = self.json_res[key]
		print("savejson: ",self.params)

	# 获取参数里面的值
	def __getparams(self, data):
		"""
		:param data:
		:return:
		"""
		for key in self.params:
			print(self.params)
			data = data.replace('{' + key + '}', self.params[key])
			# print("self.params[key]: " ,self.params[key])
			print("__getparams:",data)
		return data

	# 将一个标准的URL地址参数转换为一个dict
	def __todict(self, data):
		"""
		:param data:
		:return:
		"""
		# 分割参数个数
		print("data: ", data)
		httpparam = {}
		param = data.split("&")
		print("param: ", param)
		for item  in param:
			print("item: ",item)
			p = item.split("=")
			print("p: ",p)
			httpparam[p[0]] = p[1]
		print("httpparam: ",httpparam)
		return httpparam
