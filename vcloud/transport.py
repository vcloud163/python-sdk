# -*- coding:utf8 -*-

from vcloud import http
from vcloud import config
from vcloud.storage.uploader import put_file
from vcloud.model.vcloud_response import VcloudResp

import json

class Transport(object):
	"""视频云请求实体类

	该类主要实现了视频云的相关请求

	Attributes:
		access_key_id:		用户的访问密钥公钥
		access_key_secret:	用户的访问密钥私钥
	"""
	def __init__(self, access_key_id=None, access_key_secret=None):
		self.access_key_id = access_key_id
		self.access_key_secret = access_key_secret

	def vcloud_api_request(self, operator, headers={}, body=None):
		"""视频云API访问
		Args:
			operator:	API方法
			headers:	请求头
			body:		请求包体

		Returns:
			一个dict变量，类似 {"code": "<code>", "ret": {"<ret>"}}
			一个ResponseInfo对象
		"""
		url = config.VCLOUD_API_HOST + operator
		r, info = http._post_json(url, body, headers) 
		
		if info.status_code == 200:
			data = json.loads(info.text_body)
			if data["code"] != 200:
				return	r, VcloudResp(data["code"], None, data["msg"])
			else:
				return	r, VcloudResp(data["code"], data["ret"], None)
		return	r, None

	def upload_host_get(self):
		"""获取上传加速节点
		Returns:
			一个dict变量
			一个ResponseInfo对象
		"""
		url = config.WANPROXY_HOST + "/lbs?version=1.0"
		ret, info = http._get(url)

		return	ret, info

	def get_offset(self, upload_host, upload_init, context):
		"""获取断点
		Args:
			upload_host:	上传加速节点列表
			upload_init:	上传初始化信息
			context:		标示断点的上下文

		Returns:
			文件下一次上传的起始偏移量
		"""
		url = upload_host.upload_host + "/" + upload_init.bucket + "/" + upload_init.objectName + "?uploadContext&context=" + context + "&version=1.0"
		headers = {}
		headers['x-nos-token'] = upload_init.xNosToken
		ret, info = http._get(url, None, headers)

		if ret is None and not info.need_retry():
				return 0
		if info.connect_failed():
			host_backup = upload_host.upload_host_backup
			url_backup = host_backup + "/" + upload_init.bucket + "/" + upload_init.objectName + "?uploadContext&context=" + context + "&version=1.0"
			if info.need_retry():
				ret, info = http._get(url_backup, None, headers)
				if ret is None:
					return 0 

		if info.status_code == 200:
			data = json.loads(info.text_body)
			return int(data["offset"])
		else:
			return 0

	def upload_file(self, upload_init, upload_host, file_name, file_path, file_size, modify_time, offset, context, upload_progress_recorder, mime_type='application/octet-stream', progress_handler=None):
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
		return put_file(upload_init, upload_host, file_name, file_path, file_size, modify_time, offset, context, upload_progress_recorder, mime_type, progress_handler)





