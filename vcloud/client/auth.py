# -*- coding:utf8 -*-

import random,time,hashlib

class Auth(object):
	"""视频云权限类

	该类主要实现了视频云的请求权限获取

	Attributes:
		AppKey:		用户的访问密钥公钥
		AppSecret:	用户的访问密钥私钥
	"""
	def __init__(self, AppKey, AppSecret):
		self.AppKey = AppKey
		self.AppSecret = AppSecret
		charHex = '0123456789abcdef';
		self.Nonce = '';                    #随机字符串最大128个字符，也可以小于该数
		for i in range(0,128):
			index = int(15*random.random());
			self.Nonce = self.Nonce + charHex[index];

		self.CurTime = int(time.time());    #当前UTC时间戳，从1970年1月1日0点0 分0 秒开始到现在的秒数(String)

	def checkSumBuilder(self):
		"""获取CheckSum
		"""
		join_string = self.AppSecret + self.Nonce + str(self.CurTime);
		self.CheckSum = hashlib.sha1(join_string.encode("utf-8")).hexdigest(); #SHA1(AppSecret + Nonce + CurTime),三个参数拼接的字符串，进行SHA1哈希计算，转化成16进制字符(String，小写)

	def getVcloudHeaders(self):
		"""获取视频云API的请求头
		Returns:
			 一个dict变量，视频云请求头
		"""
		self.checkSumBuilder()
		headers = {}
		headers['Content-Type'] = 'application/json;charset=utf-8'
		headers['AppKey'] = self.AppKey
		headers['Nonce'] = self.Nonce
		headers['CurTime'] = str(self.CurTime)
		headers['CheckSum'] = self.CheckSum
		return	headers


