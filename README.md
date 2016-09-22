# Python-SDK 说明

## 1 简介

Python-SDK 是用于服务器端点播上传的软件开发工具包，提供简单、便捷的方法，方便用户开发上传视频或图片文件的功能。

## 2 功能特性

- 文件上传
- 获取进度
- 断点续传
- 查询视频
- 设置回调

## 3 开发准备

### 3.1 下载地址

[python sdk 的源码地址](https://github.com/vcloud163/python-sdk.git "python sdk 的源码地址")


### 3.2 环境准备

- 适用于 Python2 和 Python 3版本。
- 通过管理控制台->账户信息获取AppKey和AppSecret；
- 下载 python sdk，如果安装了git命令行，执行 git clone https://github.com/vcloud/python-sdk.git或者直接在github下载zip包，通过执行 python setup.py install 安装。
- 参照 API 说明和 sdk 中提供的 demo，开发代码。

**注：SDK 依赖 requests 包，需自行安装。**

### 3.2 https支持

默认使用https协议，如需修改为http协议，请在sdk包中Config目录修改。

## 4 使用说明

### 4.1 初始化

接入视频云点播，需要拥有一对有效的 AppKey 和 AppSecret 进行签名认证，可通过如下步骤获得：

- 开通视频云点播服务；
- 登陆视频云开发者平台，通过管理控制台->账户信息获取 AppKey 和 AppSecret。

在获取到 AppKey 和 AppSecret 之后，可按照如下方式进行初始化：

	from vcloud import Client
	client = Client(AppKey, AppSecret)

### 4.2 文件上传

视频云点播在全国各地覆盖大量上传节点，会选择适合用户的最优节点进行文件上传，并根据用户传入的参数做不同处理，具体详见点播服务端 API 文档。

以下是使用示例：

	from vcloud import Client
	client = Client(appKey, secretKey)
	
	#上传初始化的请求包体参数
	body = {"originFileName":"beauty.mp4"}
	
	#要上传文件的本地路径
	localfile = '/Users/Royen/Documents/video/beauty.mp4'

	res = client.upload_file(body, localfile)

**注：具体使用示例详见 sdk 包中 examples 目录下的 upload.py 文件。**

### 4.2 查询进度

视频云点播文件上传采用分片处理，可通过以下方法查询上传完成的文件进度。SDK 提供回调函数接收文件上传进度。

以下是使用示例：
	
	#负责接收进度的回调函数
	def upload_progress(offset, size):
		if size == 0:
			print "upload process ... {0}".format("%5.1f%%" % (100 * 0))
		else:
			ratio = float(offset) / size
			print "upload process ... {0}".format("%5.1f%%" % (100 * ratio))

	from vcloud import Client
	client = Client(appKey, secretKey)
		
	#上传初始化的请求包体参数
	body = {"originFileName":"beauty.mp4"}
		
	#要上传文件的本地路径
	localfile = '/Users/Royen/Documents/video/beauty.mp4'
	
	res = client.upload_file(body, localfile, upload_progress)


**注：具体使用示例详见 sdk 包中 examples 目录下的 upload.py 文件。**

### 4.3 断点续传

在上传文件中，视频云点播通过唯一标识 context 标识正在上传的文件，可通过此标识获取到已经上传视频云的文件字节数。通过此方法可实现文件的断点续传。

为防止服务中止造成文件上传信息丢失，可通过在本地存储文件信息来记录断点信息，当服务重启启动，可根据文件继续上传文件。临时文件会在上传完成后删除记录。记录断点的临时文件在配置文件 config.py 中配置。

使用示例如 4.2 所示。

### 4.4 查询视频

视频上传成功后，可通过主动查询的方式获取到视频唯一标识，支持批量查询。

以下是使用示例：

	from vcloud import Client
	client = Client(appKey, secretKey)
	#查询视频的请求包体参数
	body = {"objectNames":["sdfs.mp4"]}
		
	res = client.query_id(body)
	if res != None:
		print "client.query_id res : {0}".format(vars(res))
	else:
		print "query video error!"

**注：具体使用示例详见 sdk 包中 examples 目录下的 upload_query.py 文件。**

### 4.5 设置回调

如果设置回调，视频上传成功后会发送相关视频信息给回调接口。

以下是使用示例：

	from vcloud import Client
	client = Client(appKey, secretKey)
	
	#设置回调地址的请求包体参数
	body = {"callbackUrl":"http://1.111.11.1"}
	
	res = client.set_callback(body)
	if res != None:
		print "client.set_callback res : {0}".format(res)
	else:
		print "set callback error!"

**注：具体使用示例详见 sdk 包中 examples 目录下的 upload_set_callback.py 文件。**

## 5 版本更新记录

**v1.0.0**

1. Python SDK 的初始版本，提供点播上传的基本功能。包括：文件上传、获取进度、断点续传、查询视频、设置回调。
