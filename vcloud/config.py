# -*- coding: utf-8 -*-

VCLOUD_API_HOST = 'http://106.2.44.248'  # 视频云API Host

WANPROXY_HOST = 'http://wanproxy.127.net'  # 获取上传加速节点 Host

_BLOCK_SIZE = 1024 * 1024 * 4  		# 断点续上传分块大小，该参数为接口规格，暂不支持修改

POOL_CONNECTIONS = 10          		# 链接池个数为10
CONNECTION_TIMEOUT = 30        		# 链接超时为时间为30s
CONNECTION_RETRIES = 3        		# 链接重试次数为3次

TMP_FILE = '/tmp/test'	# 用于存储断点的临时文件目录，一个上传文件会对应一个临时文件，上传完成会清除临时文件，应保证对此目录有读写权限
