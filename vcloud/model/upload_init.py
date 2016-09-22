# -*- coding:utf8 -*-

class UploadInit(object):
	"""上传初始化信息封装类

	该类主要封装了上传初始化信息

	Attributes:
		bucket:		存储上传文件的桶
		objectName:	上传文件存储的名称
		xNosToken:	访问上传加速节点的上传凭证
	"""
	def __init__(self, bucket, objectName, xNosToken):
		self.bucket = bucket
		self.objectName = objectName
		self.xNosToken = xNosToken

