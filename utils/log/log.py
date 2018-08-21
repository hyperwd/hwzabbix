#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
# =============================================================================
#      FileName: log.py
#          Desc: log
#        Author: Dong Wei Chao
#         Email: 435904632@qq.com
#      HomePage: https://github.com/hyperwd
#       Version: 0.0.1
#    LastChange: 2018-08-20 17:46:08
#       History:
# =============================================================================
'''
import os
import logging
from logging.handlers import RotatingFileHandler

if not os.path.exists('/var/log/hwzabbix'):
    os.makedirs('/var/log/hwzabbix', 0o755)

#logging.basicConfig(level=logging.DEBUG,format='%(asctime)s %(filename)s %(module)s %(funcName)s %(process)d %(thread)d %(levelname)s %(message)s',filename='/var/log/hwcram/hwcram.log',filemode='a')
logging.basicConfig(
    level=logging.INFO,
    format=
    '%(asctime)s %(filename)s %(module)s %(funcName)s %(process)d %(thread)d %(levelname)s %(message)s',
    filename='/var/log/hwzabbix/hwzabbix.log',
    filemode='a')

#定义一个RotatingFileHandler，最多备份5个日志文件，每个日志文件最大10M
Rthandler = RotatingFileHandler(
    '/var/log/hwzabbix/hwzabbix.log', maxBytes=10 * 1024 * 1024, backupCount=5)
#Rthandler.setLevel(logging.DEBUG)
Rthandler.setLevel(logging.INFO)
formatter = logging.Formatter(
    '%(asctime)s %(filename)s %(module)s %(funcName)s %(process)d %(thread)d %(levelname)s %(message)s'
)
Rthandler.setFormatter(formatter)
logging.getLogger('').addHandler(Rthandler)
