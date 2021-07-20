# -*- coding:utf8 -*-

import requests

from vcloud import config

_session = None

def _return_wrapper(resp):
	if resp.status_code != 200:
		return None, ResponseInfo(resp)
	ret = resp.json() if resp.text != '' else {}
	return ret, ResponseInfo(resp)

def _init():
	session = requests.Session()
	adapter = requests.adapters.HTTPAdapter(pool_connections=config.POOL_CONNECTIONS, pool_maxsize=config.POOL_CONNECTIONS, max_retries=config.CONNECTION_RETRIES)
	session.mount('http://', adapter)
	global _session
	_session = session

def _get(url, body=None, headers={}):
	if _session is None:
		_init()
	try:
		r = _session.get(url, headers=headers)
	except Exception as e:
		return None, ResponseInfo(None, e)
	return _return_wrapper(r)

def _post_json(url, body=None, headers={}):
	if _session is None:
		_init()
	try:
		r = _session.post(url, json=body, headers=headers, timeout=config.CONNECTION_TIMEOUT)
	except Exception as e:
		return None, ResponseInfo(None, e)
	return _return_wrapper(r)

def _post(url, headers, stream):
	if _session is None:
		_init()
	try:
		r = _session.post(url, headers=headers, data=stream)
	except Exception as e:
		return None, ResponseInfo(None, e)
	return _return_wrapper(r)

def _post_file(url, headers, stream):
	return _post(url, headers, stream)

class ResponseInfo(object):
	"""HTTP请求返回信息类

	该类主要是用于获取和解析对视频云发起各种请求后的响应包的header和body。

	Attributes:
		status_code: 整数变量，响应状态码
		text_body:   字符串变量，响应的body
		error:       字符串变量，响应的错误内容
    """
	def __init__(self, response, exception=None):
		"""用响应包和异常信息初始化ResponseInfo类"""
		self.response = response
		self.exception = exception
		if response is None:
			self.status_code = -1
			self.text_body = None
			self.error = str(exception)
		else:
			self.status_code = response.status_code
			self.text_body = response.text
			
	def ok(self):
		return self.status_code == 200

	def need_retry(self):
		if self.response is None:
			return True
		code = self.status_code
		if code // 100 == 5:
			return True
		return False

	def connect_failed(self):
		return self.response is None

	def __str__(self):
		return ', '.join(['%s:%s' % item for item in self.__dict__.items()])

	def __repr__(self):
		return self.__str__()

