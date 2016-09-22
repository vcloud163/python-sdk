# -*- coding:utf8 -*-

class QueryResult(object):
	"""查询上传文件ID返回信息类

	该类主要封装了上传文件完成后返回的ID信息

	Attributes:
		objectName:		上传文件的保存名称，即objectName
		vid:			上传视频文件返回的ID
		imgId:			上传图片文件返回的ID
	"""
	def __init__(self, objectName, vid, imgId):
		self.objectName = objectName
		self.vid = vid
		self.imgId = imgId

