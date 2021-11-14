# coding: utf-8

import os
import time
import traceback

from selenium import  webdriver
from selenium.webdriver.common.by import  By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select


from common import logger


class WEB:
	""""
		创建一个web自动化关键字类
	"""
	# 构造函数，用来创建实例变量，初始化一些代码
	def __init__(self, writer):
		# 初始化浏览器对象的实例变量
		# 实例变量用来保存打开的浏览器
		self.driver = None
		# 写入excel执行结果
		self.writer = writer
		# 保存参数
		self.params = {}


	def openbrowser(self,browser = "gg", dpath='', t=''):
		"""
		   定义函数，专门用来打开浏览器
		:param browser:浏览器类型：gg、ff、ie
		:param dpath: webdriver的地址
		:param t: 隐式等待的时间
		:return: 返回操作浏览器的driver
		"""
		if t == '':
			t = 10
		try:
			t = int(t)
		except:
			t = 10

		if dpath == '':
			# 使用相对路径
			# dpath = '../lib/drivers/'
			# 使用绝对路径
			dpath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
			print(dpath +  "\\lib\\drivers\\chromedriver.exe")
		if browser == "gg" or browser =="":
			# 创建一个ChromeOptions的对象
			chrom_options = webdriver.ChromeOptions()
			# 去掉提示条的配置
			chrom_options.add_experimental_option("excludeSwitches", ['enable-automation'])

			# 获取浏览器用户数据目录
			try:
				# 异常处理，如果获取到，就是用获取到的路径
				base_dir =  os.environ["USERPROFILE"]
			except Exception as e:
				# 如果没有获取到，就默认使用Administrator路径
				base_dir = "C:\\Users\\007"

			user_data = base_dir + "\\AppData\\Local\\Google\\Chrome\\User Data"
			userdir = "user-data-dir=" + user_data
			# 添加用户目录数据
			chrom_options.add_argument(userdir)

			# path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
			# 调用google浏览器
			self.driver = webdriver.Chrome(executable_path= dpath+"\\lib\\drivers\\chromedriver.exe", options=chrom_options)
			self.driver.maximize_window()
			self.writer.write(self.writer.row, self.writer.clo, 'PASS')
			# 设置默认等待时间
			self.driver.implicitly_wait(t)

			return self.driver

		if browser == "ie":
			self.driver = webdriver.Ie(executable_path=dpath + "\\lib\\drivers\\IEDriver.exe")
			# 设置默认等待时间
			self.driver.implicitly_wait(t)
			self.writer.write(self.writer.row, self.writer.clo, 'PASS')
			return self.driver

		if browser == "ff":
			self.driver = webdriver.Firefox(executable_path= dpath+"\\lib\\drivers\\geckodriver.exe")
			self.driver.maximize_window()
			self.writer.write(self.writer.row, self.writer.clo, 'PASS')
			# 设置默认等待时间
			self.driver.implicitly_wait(t)
			return self.driver

	# 打开url
	def openurl(self, url):
		self.driver.get(url)
		self.writer.write(self.writer.row, self.writer.clo, 'PASS')
		return  True

	# 点击关键字，根据Xpath定位
	def click(self, xpath):
		try:
			self.driver.find_element(By.XPATH, xpath).click()
			self.writer.write(self.writer.row, self.writer.clo, 'PASS')
			return True
		except Exception as e:
			# 定位失败，则写入失败信息
			logger.exception(e)
			self.writer.write(self.writer.row, self.writer.clo, 'FAIL')
			self.writer.write(self.writer.row, self.writer.clo + 1, str(traceback.format_exc()))
			return False

	def clickbyid(self, id):
		try:
			self.driver.find_element(By.ID, id).click()
			self.writer.write(self.writer.row, self.writer.clo, 'PASS')
			return True
		except Exception as e:
			# 定位失败，则写入失败信息
			logger.exception(e)
			self.writer.write(self.writer.row, self.writer.clo, 'FAIL')
			self.writer.write(self.writer.row, self.writer.clo + 1, str(traceback.format_exc()))
			return False

	def input(self, xpath,value):
		"""
			向输入框输入的关键字，根据xpath定位
		:param xpath:
		:param value: 输入框输入的值
		:return:
		"""
		try:
			self.driver.find_element(By.XPATH, xpath).send_keys(value)
			self.writer.write(self.writer.row, self.writer.clo, 'PASS')
			return True
		except Exception as e:
			logger.exception(e)
			self.writer.write(self.writer.row, self.writer.clo, 'FAIL')
			self.writer.write(self.writer.row, self.writer.clo + 1, str(traceback.format_exc()))
			return False

	def quit(self):
		""""
			关闭浏览器
		"""
		self.driver.quit()
		self.writer.write(self.writer.row, self.writer.clo, 'PASS')
		return True

	def sleep(self, t):
		"""
			强制等待
		:param t:
		:return:
		"""
		try:
			t = int(t)
		except:
			t = 1
			self.writer.write(self.writer.row, self.writer.clo, 'FAIL')
			self.writer.write(self.writer.row, self.writer.clo + 1, str(traceback.format_exc()))
		time.sleep(t)
		self.writer.write(self.writer.row, self.writer.clo, 'PASS')

	def switchwindow(self, idx):
		"""
			切换窗口句柄
		:param idx: 窗口的id从0开始
		:return:
		"""
		try:
			idx = int(idx)
		except Exception as e:
			idx = 0
			logger.warn('switchwindow参数错误：')
			logger.exception(e)

		# 获取打开的多个窗口句柄
		windows =self.driver.window_handles
		# 关闭当前在操作的页面
		# self.driver.close()
		try:
			#切换到idx的窗口
			self.driver.switch_to.window(windows[idx])
			self.writer.write(self.writer.row, self.writer.clo, 'PASS')
			return True
		except Exception as e:
			logger.exception(e)
			self.writer.write(self.writer.row, self.writer.clo, 'FAIL')
			self.writer.write(self.writer.row, self.writer.clo + 1, str(traceback.format_exc()))
			return False

	def closewindow(self, cidx, oidx):
		"""
			根据窗口的id，关闭窗口，并切换到将要操作的窗口
		:param cidx: 需要关闭的窗口id
		:param oidx: 需要切换到的窗口id
		:return:
		"""
		try:
			# 如果需要关闭的id输入错误，则直接结束
			cidx = int(cidx)
		except:
			cidx = 0
			self.writer.write(self.writer.row, self.writer.clo, 'FAIL')
			self.writer.write(self.writer.row, self.writer.clo + 1, str(traceback.format_exc()))
			return False
		# 默认切回第一个参数
		try:
			oidx = int(oidx)
		except Exception as e:
			oidx = 0
			logger.warn("closewindow参数错误：")
			logger.exception(e)
		windows = self.driver.window_handles
		try:
			# 切换到需要关闭的窗口
			self.driver.switch_to.window(windows[cidx])
			# 关闭窗口
			self.driver.close()
			self.writer.write(self.writer.row, self.writer.clo, 'PASS')
			# 切换到关闭后，需要操作的窗口
			self.driver.switch_to.window(windows[oidx])
			return True
		except Exception as e:
			logger.exception(e)
			self.writer.write(self.writer.row, self.writer.clo, 'FAIL')
			self.writer.write(self.writer.row, self.writer.clo + 1, str(traceback.format_exc()))
			return False

	def __find_elemnet(self, locator):
		"""
		内部用来查找元素的方法
		支持三种主流的查找方式
		:param locator: 支持输入xpath，id ， cotent-desc
		:return:
		"""
		try:
			if locator.startswith('/'):
				ele = self.driver.find_element(By.XPATH, locator)
			else:
				try:
					# 尝试用id定位
					ele = self.driver.find_element(By.ID, locator)
				except:
					try:
						# 尝试用name定位
						ele = self.driver.find_element(By.NAME,locator)
					except:
						return None
		except Exception as e:
			logger.exception(e)
			return None
		return ele

	def intoiframe(self, locator):
		"""
		通过定位到iframe，在进入ifram， 改关键字提供了一种多定位方式的实例
		:param locator: 元素的定位器（支持id，name，xpath）
		:return:
		"""
		ele = self.__find_elemnet(locator)
		try:
			# 根据定位，切换iframe
			self.driver.switch_to.frame(ele)
			self.writer.write(self.writer.row, self.writer.clo, 'PASS')
			return True
		except Exception as e:
			# 定位失败，则写入失败信息
			logger.exception(e)
			self.writer.write(self.writer.row, self.writer.clo, 'FAIL')
			self.writer.write(self.writer.row, self.writer.clo + 1, str(traceback.format_exc()))
			return False

	def outiframe(self):
		"""
		切回默认页面
		:return:
		"""
		# 切到frame中之后，便不能继续操作主文档的元素，如果想操作主文档内容，则需切回主文档
		self.driver.switch_to.default_content()
		self.writer.write(self.writer.row, self.writer.clo, 'PASS')
		return True

	def selectbyindex(self,locator,index):
		"""
		根据下拉框的index选择
		:param locator: 元素的定位器（支持id，name，xpath）
		:param index: 选择框的index值
		:return:
		"""
		ele = self.__find_elemnet(locator)
		try:
			index = int(index)
			Select(ele).select_by_index(index)
			self.writer.write(self.writer.row, self.writer.clo, 'PASS')
			return True
		except Exception as e:
			# 定位失败，则写入失败信息
			logger.exception(e)
			self.writer.write(self.writer.row, self.writer.clo, 'FAIL')
			self.writer.write(self.writer.row, self.writer.clo + 1, str(traceback.format_exc()))
			return False

	def selectbyvalue(self,locator,value):
		"""
		根据下拉框的value选择
		:param locator: 元素的定位器（支持id，name，xpath）
		:param value: 选择框的value值
		:return:
		"""
		ele = self.__find_elemnet(locator)
		try:
			Select(ele).select_by_value(value)
			self.writer.write(self.writer.row, self.writer.clo, 'PASS')
			return True
		except Exception as e:
			# 定位失败，则写入失败信息
			logger.exception(e)
			self.writer.write(self.writer.row, self.writer.clo, 'FAIL')
			self.writer.write(self.writer.row, self.writer.clo + 1, str(traceback.format_exc()))
			return False

	def selectbytext(self,locator,text):
		"""
		根据下拉框的index选择
		:param locator: 元素的定位器（支持id，name，xpath）
		:param text: 选择框的text值
		:return:
		"""
		ele = self.__find_elemnet(locator)
		try:
			Select(ele).select_by_visible_text(text)
			self.writer.write(self.writer.row, self.writer.clo, 'PASS')
			return True
		except Exception as e:
			# 定位失败，则写入失败信息
			logger.exception(e)
			self.writer.write(self.writer.row, self.writer.clo, 'FAIL')
			self.writer.write(self.writer.row, self.writer.clo + 1, str(traceback.format_exc()))
			return False

	def hover(self, xpath):
		"""
		根据xpath，找到元素，并将鼠标悬停到元素
		该关键字在自动化过程中，如果认为移动了鼠标可能导致悬停失败
		改关键字也可以用于页面滚动，但不一定能滚动成功
		:param xpath: 元素的xpath
		:return:
		"""
		try:
			ele = self.driver.find_element(By.XPATH, xpath)
		except Exception as e:
			logger.exception(e)
			self.writer.write(self.writer.row, self.writer.clo, 'FAIL')
			self.writer.write(self.writer.row, self.writer.clo + 1, str(traceback.format_exc()))
			# 定位失败，则直接返回
			return  False
		try:
			actions = ActionChains(self.driver)
			actions.move_to_element(ele).perform()
			self.writer.write(self.writer.row, self.writer.clo, 'PASS')
			return True
		except Exception as e:
			logger.exception(e)
			self.writer.write(self.writer.row, self.writer.clo, 'FAIL')
			self.writer.write(self.writer.row, self.writer.clo + 1, str(traceback.format_exc()))
			# 定位失败，则直接返回

	def scroll(self, x, y):
		"""
		使用js滚动，既可以横向，也可以纵向滚动
		该方法使用的是scrollBy，增量式滚动
		:param self:
		:param x:  横向滚动距离
		:param y:  纵向滚动距离
		:return:
		"""
		# 此处坐标直接使用字符串，因为js需要拼接成字符串
		js = 'window。scrollBy(' + str(x) + ',' + str(y) + ');'
		try:
			self.driver.execute_script(js)
		except Exception as e:
			logger.exception(e)
			self.writer.write(self.writer.row, self.writer.clo, 'FAIL')
			self.writer.write(self.writer.row, self.writer.clo + 1, str(traceback.format_exc()))
			return False

	def excutejs(self, js):
		"""
		封装了默认执行js的方法
		:param js: 需要执行的标准js语句
		:return: 无
		"""
		try:
			self.driver.execute_script(js)
			self.writer.write(self.writer.row, self.writer.clo, 'PASS')
			return True
		except Exception as e:
			logger.exception(e)
			self.writer.write(self.writer.row, self.writer.clo, 'FAIL')
			self.writer.write(self.writer.row, self.writer.clo + 1, str(traceback.format_exc()))
			# 定位失败，则直接返回
			return False



	def uploadfile(self, xpath, filepath):
		"""
		根据xpath，找到元素
		使用send_keys上传文件
		:param xpath:  元素的xpath
		:param filepath: 需要上传文件的全路径
		:return:
		"""
		try:
			ele = self.driver.find_element(By.XPATH, xpath)
		except Exception as e:
			logger.exception(e)
			self.writer.write(self.writer.row, self.writer.clo, 'FAIL')
			self.writer.write(self.writer.row, self.writer.clo + 1, str(traceback.format_exc()))
			# 定位失败，则直接返回
			return  False
		try:
			ele.send_keys(filepath)
			self.writer.write(self.writer.row, self.writer.clo, 'PASS')
			return True
		except Exception as e:
			logger.exception(e)
			self.writer.write(self.writer.row, self.writer.clo, 'FAIL')
			self.writer.write(self.writer.row, self.writer.clo + 1, str(traceback.format_exc()))
			return False

	def gettitle(self):
		"""
		获取当前窗口的title，并在系统中保存一个名加title的变量
		在支持关联的关键字中，可以是用{title},来调用它的值
		:return: 无
		"""
		title = self.driver.title
		self.params['title'] = title
		self.writer.write(self.writer.row, self.writer.clo, 'PASS')
		return True

	def gettext(self, xpath):
		"""
		获取当前xpath定位元素的文本， 并在系统中保存一个名叫text的变量
		在支持关联的关键字中，可以使用{text}, 来调用它的值
		:param xpath: 元素的xpath
		:return:无
		"""
		self.params['text'] = ''
		try:
			text = self.driver.find_element(By.XPATH, xpath).text
			self.params['text'] = text
			self.writer.write(self.writer.row, self.writer.clo, 'PASS')
			return True
		except Exception as e:
			logger.exception(e)
			self.writer.write(self.writer.row, self.writer.clo, 'FAIL')
			self.writer.write(self.writer.row, self.writer.clo + 1, str(traceback.format_exc()))
			return  False

	def assertequals(self, param, value):
		"""
		定义断言相等的关键字，用来判断前后的值是否一致
		:param param: 需要校验的参数
		:param vlue: 需要校验的值
		:return:
		"""
		param = self._getparams(param)
		value = self._getparams(value)
		if str(param) == str(value):
			self.writer.write(self.writer.row, self.writer.clo, 'PASS')
			self.writer.write(self.writer.row, self.writer.clo + 1, str(param))
			return True
		else:
			self.writer.write(self.writer.row, self.writer.clo, 'FAIL')
			self.writer.write(self.writer.row, self.writer.clo + 1, str(param))
			return False


	# 获取参数里面的值
	def _getparams(self, s):
		logger.info(self.params)
		for key in self.params:
			s = s.replace('{' + key + '}', self.params[key])
		return s


	def isElementExist(self,element):
		flag = True
		try:
			self.driver.find_element(By.XPATH, element)
			return flag
		except:
			flag = False
			return flag

	def browserback(self):
		self.driver.back()
		self.writer.write(self.writer.row, self.writer.clo, 'PASS')

if __name__ == "__main__":
	path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	print(path)