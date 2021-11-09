# conding: uft-8

import requests
import json


from common import logger


# 创建已http接口请求关键字类
class HTTP:


	# 构造函数，实例化实例变量
	def __init__(self, writer):
		# 创建session对象，模拟浏览器的cookie管理
		self.session = requests.session()
		# 存放json解析后的结果
		self.json_res = {}
		self.params = {}
		# 全局的url
		self.baseurl = ''

		# 写入结果的excel
		self.writer = writer


	def seturl(self, url):
		"""
		设置一个url后面只需给接口路径
		:param url:
		:return:
		"""

		if url.startswith("http"):
			self.baseurl =url
			# print("baseurl: ",self.baseurl)
			self.writer.write(self.writer.row, self.writer.clo, "PASS")
		else:
			logger.error("error: utl地址不合法")
			self.writer.write(self.writer.row, self.writer.clo, "FAIL")
			self.writer.write(self.writer.row, self.writer.clo+1, "error: utl地址不合法")

	def post(self, path, data=""):
		"""
		定义post实例方法，用来发送post请求
		:param path: post的访问接口路径
		:param data: 接口需要传入的参数类型为str
		:return:
		"""
		try:
			if not path.startswith('http'):
				path = self.baseurl + '/' + path
				# print("self.url:",self.baseurl)
				# print(path)
			# 如果需要传参数，就调用post，传递data
			if data is None or data == "":
				res = self.session.post(path)
			else:
				# 替换参数
				data = self.__getparams(data)
				# 替换后的参数转换为字典
				data = self.__todict(data)
				res = self.session.post(path, data=data)
			print(res.text)

			self.json_res = json.loads(res.text)
			self.writer.write(self.writer.row, self.writer.clo, "PASS")
			self.writer.write(self.writer.row, self.writer.clo + 1, str(self.json_res))
		except Exception as e:
			self.writer.write(self.writer.row, self.writer.clo, "FAIL")
			self.writer.write(self.writer.row, self.writer.clo + 1, str(self.json_res))
			logger.exception(e)

	# 定义断言相等的关键字，用来判断接送的可以对应的值和期望值相等
	def assertequals(self, key, value):
		"""
		:param key: 需要断言self.json_res的key值
		:param value: 断言的预期结果值
		:return:
		"""
		res = ''
		try:
			res = str(self.json_res[key])
		except Exception as e:
			logger.logger.exception(e)
		if res == str(value):
			self.writer.write(self.writer.row, self.writer.clo, "PASS")
			self.writer.write(self.writer.row, self.writer.clo + 1, str(res))
			logger.logger.info("PASS")
		else:
			self.writer.write(self.writer.row, self.writer.clo, "FAIL")
			self.writer.write(self.writer.row, self.writer.clo + 1, str(res))
			logger.logger.info("FAIL")

	# 给头添加一个键值对关键字
	def addheader(self, key, value):
		"""
		:param key: 添请求加头的键
		:param value: 添加请求头的值
		:return:
		http.savejson("t","token")
		http.addheaders("token",'{t}')
		"""
		value = self.__getparams(value)
		self.session.headers[key] = value
		self.writer.write(self.writer.row, self.writer.clo, "PASS")
		self.writer.write(self.writer.row, self.writer.clo + 1, str(value))

	def removeheader(self, key):
		"""
		从表头里面删除一个键值对
		:return:
		"""
		self.session.headers.pop(key)
		self.writer.write(self.writer.row, self.writer.clo, "PASS")
		self.writer.write(self.writer.row, self.writer.clo + 1, str(key))


	def savejson(self, p, key):
		"""
		定义保存一个接送值为参数的关键字
		:param p:
		:param key:
		:return:
		"""
		res = ''
		try:
			res = self.json_res[key]
		except Exception as e:
			logger.logger.exception(e)
		self.params[p] = res
		self.writer.write(self.writer.row, self.writer.clo, "PASS")
		self.writer.write(self.writer.row, self.writer.clo + 1, str(res))

		# print("savejson: ", self.params)


	def __getparams(self, data):
		"""
		私有方法，获取参数里面的值
		:param data:
		:return:
		"""
		for key in self.params:
			# print(self.params)
			data = data.replace('{' + key + '}', self.params[key])
			# print("self.params[key]: " ,self.params[key])
			# print("__getparams:", data)
		return data


	def __todict(self, data):
		"""
		 将一个标准的URL地址参数转换为一个dict
		:param data:
		:return:
		"""
		# 分割参数个数
		# print("data: ", data)
		httpparam = {}
		param = data.split("&")
		print("param: ", param)
		for item in param:
			# print("item: ", item)
			p = item.split("=")
			if len(p) > 1:
				httpparam[p[0]] = p[1]
			else:
				httpparam[p[0]] = ""
		# print("httpparam: ", httpparam)
		return httpparam
