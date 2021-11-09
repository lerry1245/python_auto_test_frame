# coding: utf-8

import requests
import json
import re
import inspect

from keywords.httpkeywords import HTTP
from common.Excel import Reader
from common.Excel import Writer
from common import logger
from common import config
from common.excelresult import Res
from common.mysql import Mysql
from common.mail import Mail


# 反射获取关键字
def getfunc(obj,line):
	func = None
	try:
		func = getattr(obj, line[3])
	except Exception as e:
		logger.logger.exception(e)

	return func


# 反射获取方法的形参
def getargs(func):
	if func:
		args = inspect.getfullargspec(func).__str__()
		# print(args)
		args = args[args.find("args=") + 5:args.find(", varargs=None")]
		args = eval(args)
		args.remove("self")
		l = len(args)
		return l
	else:
		return 0


# 运行一条用例
def run(func, lenargs, line):
	if func is None:
		return
	if lenargs < 1:
		func()
		return
	if lenargs < 2:
		func(line[4])
		return
	if lenargs < 3:
		func(line[4], line[5])
		return
	if lenargs < 4:
		func(line[4], line[5], line[4])
		return
	logger.logger.error("error: 目前只支持3个参数的关键字")


# 运行用例
def runCase():
	reader = Reader()
	writer = Writer()
	http = HTTP(writer)
	reader.open_excel("../lib/cases/HTTP接口用例.xls")
	writer.copy_open('../lib/cases/HTTP接口用例.xls', '../lib/results/results-HTTP接口用例.xls')
	sheetname = reader.get_sheets()
	for sheet in sheetname:
		# 设置当前读取的sheet页面
		reader.set_sheet(sheet)
		writer.set_sheet(sheet)
		writer.clo = 7
		for i in range(reader.rows):
			line = reader.readline()
			# print(line)
			# 如果第一列或者第二列有内容，就是分组信息，不运行
			if len(line[0])>0 or len(line[1])>0:
				pass
			else:
				print(line)
				writer.row = i
				func = getfunc(http,line)
				lenargs = getargs(func)
				run(func,lenargs,line)

	writer.save_close()

if __name__ == "__main__":
	config.get_config("../lib/conf/conf.txt")
	logger.info(config.config)
	# 初始化数据库，如果非必要可以不用执行
	# mysql = Mysql()
	# mysql.init_mysql("C:\\Users\\007\\Desktop\\huobi\\userinfo.sql")
	runCase()
	res = Res()
	r = res.get_res("../lib/results/results-HTTP接口用例.xls")
	text = config.config['mailtext']
	mailtitle = config.config["mailtitle"]
	if r["status"] == "PASS":
		text = text.replace("status",r['status'])
	else:
		text = text.replace('<font style="font-weight: bold;font-size: 14px;color: #00d800;">status</font>','<font style="font-weight: bold;font-size: 14px;color: red;">Fail</font>')
	text = text.replace("passrate", r["passrate"] + "%")
	text = text.replace("casecount", r["casecount"])
	text = text.replace("title", mailtitle)
	print(text)
	# logger.info(text)
	# mail = Mail()
	# mail.send(text)