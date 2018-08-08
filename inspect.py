#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
# =============================================================================
#      FileName: inspect.py
#          Desc: send the data from hwopenapi to redis
#        Author: Dong Wei Chao
#         Email: 435904632@qq.com
#      HomePage: https://github.com/hyperwd
#       Version: 0.0.1
#    LastChange: 2018-08-08 03:15:30
#       History:
# =============================================================================
'''
import configparser

conf = configparser.ConfigParser()
conf.read('/etc/.hwzabbix/config.ini')

ak = conf.get('hw', 'ak')
sk = conf.get('hw', 'sk')
region = conf.get('hw', 'region')
project_id = conf.get('hw', 'project_id')
x_project_id = conf.get('hw', 'x_project_id')

print(ak, sk, region, project_id, x_project_id)
