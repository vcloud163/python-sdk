# -*- coding: utf-8 -*-
'''
Vcloud upload SDK for Python
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For detailed document, please see:
<https://vcloud.163.com>
'''

__version__ = '1.0.0'

from .transport import Transport

from .client.auth import Auth
from .model.upload_init import UploadInit
from .model.upload_host import UploadHost
from .model.query_result import QueryResult
from .model.vcloud_response import VcloudResp
from .storage.uploader import put_file
from .storage.upload_progress_recorder import UploadProgressRecorder
from .client.vcloud_client import Client

