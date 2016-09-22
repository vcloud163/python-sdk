# -*- coding:utf8 -*-

class UploadHost(object):
	"""查询上传加速节点返回信息类

	该类主要封装了上传加速节点列表

	Attributes:
		upload_host:		上传加速节点首选节点
		upload_host_backup:	上传加速节点备用节点
	"""
	def __init__(self, upload_host, upload_host_backup):
		self.upload_host = upload_host
		self.upload_host_backup = upload_host_backup

