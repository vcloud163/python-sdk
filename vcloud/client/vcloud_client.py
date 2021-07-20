# -*- coding:utf8 -*-

from vcloud import put_file
from vcloud import config
from vcloud.transport import Transport
from vcloud.client.auth import Auth
from vcloud.model.upload_init import UploadInit
from vcloud.model.upload_host import UploadHost
from vcloud.model.query_result import QueryResult
from vcloud.storage.upload_progress_recorder import UploadProgressRecorder

import json, os

class Client(object):
	"""视频云请求实体类

	该类主要实现了视频云的相关请求

	Attributes:
		access_key_id:		用户的访问密钥公钥
		access_key_secret:	用户的访问密钥私钥
		transport_class:	http请求处理类
	"""
	def __init__(self, access_key_id, access_key_secret, transport_class=Transport):
		self.transport = transport_class()
		self.auth = Auth(access_key_id, access_key_secret)

	def upload_init(self, body):
		"""上传初始化
		Args:
			body:	请求包体

		Returns:
			一个UploadInit对象
		"""
		headers = self.auth.getVcloudHeaders()
		r, vResp = self.transport.vcloud_api_request("/app/vod/upload/init", headers, body)
		if vResp != None:
			if vResp.msg == None:
				return	UploadInit(vResp.ret['bucket'], vResp.ret['object'], vResp.ret['xNosToken'])
			else:
				return	None
		else:
			return	None

	def get_upload_host(self):
		"""获取上传加速节点地址
		Returns:
			一个UploadHost对象
		"""
		ret, info = self.transport.upload_host_get()
		if info != None:
			if info.status_code == 200:
				data = json.loads(info.text_body)
				return	UploadHost(data['upload'][0], data['upload'][1])
			else:
				return None
		else:
			return None

	def upload_file(self, body, file_path, progress_handler=None, mime_type='application/octet-stream'):
		"""上传文件
		Args:
			body:		请求包体
			file_path:	上传文件路径

		Returns:
			一个QueryResult对象
		"""
		file_name = os.path.basename(file_path)
		modify_time= os.path.getmtime(file_path)
		file_size = os.stat(file_path).st_size
		
		upload_init = None
		upload_host = None
		offset = 0
		context = ""

		upload_progress_recorder = UploadProgressRecorder(config.TMP_FILE)
		record = upload_progress_recorder.get_upload_record(file_name, modify_time)
		if record == None:
			upload_init = self.upload_init(body)
			upload_host = self.get_upload_host()
		else:
			upload_init = UploadInit(record['bucket'], record['object'], record['xNosToken'])
			upload_host = UploadHost(record['host']['upload_host'], record['host']['upload_host_backup'])
			context = record['context']
			offset = self.transport.get_offset(upload_host, upload_init, context)

		if upload_init == None or upload_host == None:
			return	None

		ret, info = self.transport.upload_file(upload_init, upload_host, file_name, file_path, file_size, modify_time, offset, context, upload_progress_recorder, mime_type, progress_handler)

		if info.status_code == 200:
			body = {"objectNames":[upload_init.objectName]}
			return self.query_id(body)
		else:
			return None

	def query_id(self, body):
		"""根据对象名查询uid或imgId
		Args:
			body:	请求包体

		Returns:
			一个QueryResult对象
		"""
		headers = self.auth.getVcloudHeaders()
		r, vResp = self.transport.vcloud_api_request("/app/vod/video/query", headers, body)
		if vResp != None:
			if vResp.msg == None:
				result = vResp.ret['list'][0]
				if 'vid' in result:
					return	QueryResult(result['objectName'], result['vid'], None)
				else:
					return	QueryResult(result['objectName'], None, result['imgId'])
			else:
				return	vResp.msg.encode('utf-8')
		else:
			return	"请求异常"

	def set_callback(self, body):
		"""设置上传回调
		Args:
			body:	请求包体

		Returns:
			字符串，表示请求结果
		"""
		headers = self.auth.getVcloudHeaders()
		r, vResp = self.transport.vcloud_api_request("/app/vod/upload/setcallback", headers, body)

		if vResp != None:
			if vResp.code == 200:
				return "设置成功"
			else:
				return	vResp.msg.encode('utf-8')
		else:
			return	"请求异常"



