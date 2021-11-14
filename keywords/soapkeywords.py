# coding:utf-8
import json
import jsonpath
from suds.client import Client
from suds.xsd.doctor import ImportDoctor, Import

from common import logger


class SOAP:
	def __init__(self, writer):
		# 文档标准
		self.doctor = None
		# client 请求
		self.client = None
		# 保存wsdl文档地址
		self.wsdlurl = ""
		# 请求头
		self.header = {}
		# 保存的参数
		self.params = {}
		# 返回的结果
		self.result = ""
		# 解析后的json字典
		self.jsoners = None
		#实际结果
		self.actualresult = ""
		# 写入结果的Excel
		self.writer = writer

	def adddoctor(self,targetNamespace, XMLSchema="", localtion=""):
		if XMLSchema == "":
			XMLSchema = 'http://www.w3.org/2001/XMLSchema'
		if localtion =="":
			localtion = 'http://www.w3.org/2001/XMLSchema.xsd'

		imp = Import(XMLSchema, location = localtion)
		# 添加命名空间，
		imp.filter.add(targetNamespace)
		self.doctor = ImportDoctor(imp)
		self.writer.write(self.writer.row, self.writer.clo, "PASS")

	# 设置描述文档地址
	def setwsdl(self,url):
		self.wsdlurl = url
		try:
			self.client = Client(url, doctor=self.doctor, headers=self.header)
			self.writer.write(self.writer.row, self.writer.clo, "PASS")
			self.writer.write(self.writer.row, self.writer.clo + 1, str(self.jsoners))
		except Exception as e:
			self.writer.write(self.writer.row, self.writer.clo, "FAIL")
			self.writer.write(self.writer.row, self.writer.clo + 1, str(self.jsoners))

	def addheader(self, key, value):
		value = self.__getparams(value)
		self.header[key] = value
		try:
			self.client = Client(self.wsdlurl, doctor=self.doctor, headers=self.header)
			self.writer.write(self.writer.row, self.writer.clo, "PASS")
			self.writer.write(self.writer.row, self.writer.clo + 1, str(self.jsoners))
		except Exception as e:
			self.writer.write(self.writer.row, self.writer.clo, "FAIL")
			self.writer.write(self.writer.row, self.writer.clo + 1, str(self.jsoners))
			logger.exception(e)


	def removeheader(self, key):
		try:
			self.header.pop(key)
			self.client = Client(self.wsdlurl, doctor=self.doctor, headers=self.header)
			self.writer.write(self.writer.row, self.writer.clo, "PASS")
			self.writer.write(self.writer.row, self.writer.clo + 1, str(self.jsoners))
		except Exception as e:
			self.writer.write(self.writer.row, self.writer.clo, "FAIL")
			self.writer.write(self.writer.row, self.writer.clo + 1, str(self.jsoners))
			logger.exception(e)


	def callmethod(self, method, param=""):
		try:
			param = self.__getparams(param)
			if not param =="":
				p = param.split('、')
			if param =="":
				self.result = self.client.service.__getattr__(method)()

			else:
				self.result = self.client.service.__getattr__(method)(*p)

			self.jsoners = json.loads(self.result)
			self.writer.write(self.writer.row, self.writer.clo, "PASS")
			self.writer.write(self.writer.row, self.writer.clo + 1, str(self.jsoners))
			logger.info("self.result: ",self.result)
		except Exception as e:
			self.writer.write(self.writer.row, self.writer.clo, "FAIL")
			self.writer.write(self.writer.row, self.writer.clo + 1, str(self.jsoners))
			logger.exception(e)

		# 定义断言相等的关键字，用来判断接送的可以对应的值和期望值相等
		def assertequals(self, jsonpaths, value):
			"""
			:param key: 需要断言self.json_res的key值
			:param value: 断言的预期结果值
			:return:
			"""
			res = 'None'
			try:
				res = str(jsonpath.jsonpath(self.json_res, jsonpaths)[0])
			except Exception as e:
				logger.exception(e)
			if res == str(value):
				self.writer.write(self.writer.row, self.writer.clo, "PASS")
				self.writer.write(self.writer.row, self.writer.clo + 1, str(res))
				logger.info("PASS")
			else:
				self.writer.write(self.writer.row, self.writer.clo, "FAIL")
				self.writer.write(self.writer.row, self.writer.clo + 1, str(res))
				logger.info("FAIL")

	def savejson(self, p, key):
		"""
		定义保存一个接送值为参数的关键字
		:param p:
		:param key:
		:return:
		"""
		res = ''
		try:
			res = self.jsoners[key]
		except Exception as e:
			logger.exception(e)
		self.params[p] = res
		self.writer.write(self.writer.row, self.writer.clo, "PASS")
		self.writer.write(self.writer.row, self.writer.clo + 1, str(res))

		print("savejson: ", self.params)


	def __getparams(self, data):
		"""
		私有方法，获取参数里面的值
		:param data:
		:return:
		"""
		for key in self.params:
			print(self.params)
			data = data.replace('{' + key + '}', self.params[key])
			print("self.params[key]: " ,self.params[key])
			print("__getparams:", data)
		return data
