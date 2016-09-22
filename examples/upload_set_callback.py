# -*- coding: utf-8 -*-

from vcloud import Client
from vcloud import UploadInit
from vcloud import put_file

if __name__ == '__main__':
	appKey = "027338bf05ee4a65b5d98bc9d6af80b3"
	secretKey = "a2d9c5a47d86ee0ca71823a7191ebf79"
	client = Client(appKey, secretKey)
	
	#设置回调地址的请求包体参数
	body = {"callbackUrl":"http://1.111.11.1"}
	
	res = client.set_callback(body)
	if res != None:
		print "client.set_callback res : {0}".format(res)
	else:
		print "set callback error!"
