# -*- coding:utf8 -*-

class VcloudResp(object):
	"""视频云API返回结果封装类

	该类主要封装了视频云API放回结果

	Attributes:
		code:	视频云API返回码
		ret:	视频云API返回结果
		msg:	视频云API返回错误信息
	"""
	def __init__(self, code, ret, msg):
		self.code = code
		self.ret = ret
		self.msg = msg

