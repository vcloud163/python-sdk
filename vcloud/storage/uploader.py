# -*- coding: utf-8 -*-

import os
import time
import json

from vcloud import config
from vcloud import http
from vcloud.utils import _file_iter
from .upload_progress_recorder import UploadProgressRecorder

def put_file(upload_init, upload_host, file_name, file_path, file_size, modify_time, offset, context, upload_progress_recorder, mime_type='application/octet-stream', progress_handler=None):
	"""上传文件
	Args:
		upload_init:				上传初始化信息
		upload_host:				上传加速节点列表
		file_name:					上传文件名
		file_path:					上传文件的路径
		file_size:					上传文件大小
		modify_time:				上传文件最后修改时间
		offset:						文件下一次上传的起始偏移量
		context:					标示断点的上下文
		upload_progress_recorder:	记录上传进度，用于断点续传
		mime_type:					上传数据的mimeType
		progress_handler:			上传进度

	Returns:
		一个dict变量，类似 {"code": "<code>", "ret": {"<ret>"}}
		一个ResponseInfo对象
	"""
	ret = {}
	info = None
	with open(file_path, 'rb') as input_stream:
		ret, info = put_stream(upload_init, upload_host, file_name, file_size, modify_time, offset, context, input_stream, upload_progress_recorder, mime_type, progress_handler)
	return ret, info

def put_stream(upload_init, upload_host, file_name, size, modify_time, offset, context, input_stream, upload_progress_recorder, mime_type, progress_handler=None):
	task = _Resume(upload_init, upload_host, file_name, size, modify_time, offset, context, input_stream, upload_progress_recorder, mime_type, progress_handler)
	return task.upload()

class _Resume(object):
	"""断点续上传类

	该类主要实现了分块上传，断点续上

	Attributes:
		upload_init:				上传初始化信息
		upload_host:				上传加速节点列表
		file_name:					上传文件名
		size:						上传文件大小
		modify_time:				上传文件最后修改时间
		offset:						文件下一次上传的起始偏移量
		context:					标示断点的上下文
		input_stream:				上传二进制流
		upload_progress_recorder:	记录上传进度，用于断点续传
		mime_type:					上传数据的mimeType
		progress_handler:			上传进度
	"""

	def __init__(self, upload_init, upload_host, file_name, size, modify_time, offset, context, input_stream, upload_progress_recorder, mime_type, progress_handler):
		"""初始化断点续上传"""
		self.upload_init = upload_init
		self.upload_host = upload_host
		self.file_name = file_name
		self.offset = offset
		self.context = context
		self.size = size
		self.modify_time = modify_time
		self.input_stream = input_stream
		self.mime_type = mime_type
		self.upload_progress_recorder = upload_progress_recorder
		self.progress_handler = progress_handler

	def upload(self):
		"""上传操作"""
		ret = None
		info = None

		host = self.upload_host.upload_host
		offset = self.offset
		context = self.context
		record = False

		for block in _file_iter(self.input_stream, config._BLOCK_SIZE, offset):
			url = self.block_url(host, offset, context)
			ret_inner, info_inner = self.block_upload(url, block)

			if ret_inner is None and not info_inner.need_retry():
				return ret_inner, info_inner
			if info_inner.connect_failed():
				host_backup = self.upload_host.upload_host_backup
				url_backup = self.block_url(host_backup, offset, context)
				if info_inner.need_retry():
					ret_inner, info_inner = self.block_upload(url_backup, block)
					if ret_inner is None:
						return ret_inner, info_inner

			data = json.loads(info_inner.text_body)
			if data.has_key("offset"):
				offset = data["offset"]
			if data.has_key("context"):
				context = data["context"]

			if record == False:
				self.record_upload_progress(context)
				record = True

			ret = ret_inner
			info = info_inner
			if(callable(self.progress_handler)):
				self.progress_handler(offset, self.size)
			#进度显示
			#print "upload process ... {0}".format(self.as_parent(offset, self.size))
		self.upload_progress_recorder.delete_upload_record(self.file_name, self.modify_time)
		return ret, info	

	def block_upload(self, url, block):
		"""上传块"""
		headers = {}
		headers['x-nos-token'] = self.upload_init.xNosToken
		return http._post(url, headers, block)

	def block_url(self, host, offset, context):
		"""获取上传块的URL"""
		if self.size - offset < config._BLOCK_SIZE:
			if offset == 0:
				return '{0}/{1}/{2}?offset={3}&complete={4}&version=1.0'.format(host, self.upload_init.bucket, self.upload_init.objectName, offset, 'true')
			else:
				return '{0}/{1}/{2}?offset={3}&complete={4}&context={5}&version=1.0'.format(host, self.upload_init.bucket, self.upload_init.objectName, offset, 'true', context)
		else:
			return '{0}/{1}/{2}?offset={3}&complete={4}&context={5}&version=1.0'.format(host, self.upload_init.bucket, self.upload_init.objectName, offset, 'false', context)

	def record_upload_progress(self, context):
		"""记录上传的断点信息"""
		record_data = {
			'bucket' : self.upload_init.bucket,
			'object' : self.upload_init.objectName,
			'xNosToken': self.upload_init.xNosToken,
			'size': self.size,
			'context': context,
			'host': vars(self.upload_host)
		}
		self.upload_progress_recorder.set_upload_record(self.file_name, self.modify_time, record_data)

	def as_parent(self, num, den):
		if den == 0:
			ratio = 0
		else:
			ratio = float(num) / den
		return "%5.1f%%" % (100 * ratio)







