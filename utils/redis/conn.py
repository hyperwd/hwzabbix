#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
# =============================================================================
#      FileName: conn.py
#          Desc: redis pool
#        Author: Dong Wei Chao
#         Email: 435904632@qq.com
#      HomePage: https://github.com/hyperwd
#       Version: 0.0.1
#    LastChange: 2018-08-08 03:14:25
#       History:
# =============================================================================
'''
import configparser

conf = configparser.ConfigParser()
conf.read('/etc/.hwzabbix/config.ini')

redis_host = conf.get('redis', 'host')
redis_port = conf.get('redis', 'port')
redis_password = conf.get('redis', 'password')
redis_db = conf.get('redis', 'db')


def pool():
    try:
        pool = redis.ConnectionPool(
            host=redis_host,
            password=redis_password,
            port=redis_port,
            db=redis_db,
            decode_responses=True)
        r = redis.Redis(connection_pool=pool)
        return r
    except Exception as e:
        return 'could not connect to redis'
