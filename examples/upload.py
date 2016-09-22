# -*- coding: utf-8 -*-

from vcloud import Client
from vcloud import UploadInit
from vcloud import put_file


def upload_progress(offset, size):
	if size == 0:
		print "upload process ... {0}".format("%5.1f%%" % (100 * 0))
	else:
		ratio = float(offset) / size
		print "upload process ... {0}".format("%5.1f%%" % (100 * ratio))

if __name__ == '__main__':
	appKey = "027338bf05cc4a65b5d44bc9d6af80b3"
	secretKey = "a2d9c5a47d86470ca7182457191ebf79"
	client = Client(appKey, secretKey)
	
	#上传初始化的请求包体参数
	body = {"originFileName":"beauty.mp4"}
	
	#要上传文件的本地路径
	localfile = '/Users/Royen/Documents/video/beauty.mp4'

	res = client.upload_file(body, localfile, upload_progress)
	if res != None:
		print "client.upload_file res : {0}".format(vars(res))
	else:
		print "upload error!"



