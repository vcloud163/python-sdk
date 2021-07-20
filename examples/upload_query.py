# -*- coding: utf-8 -*-

from vcloud import Client
from vcloud import UploadInit
from vcloud import put_file

if __name__ == '__main__':
	appKey = "027338bf05cc4afdb5d98bc9d6af80b3"
	secretKey = "a2d9c5a47d86470c341823a7191ebf79"
	client = Client(appKey, secretKey)
	
	#查询视频的请求包体参数
	body = {"objectNames":["sdfs.mp4"]}
	
	res = client.query_id(body)
	if res != None:
		print ("client.query_id res : {0}".format(vars(res)))
	else:
		print ("query video error!")
