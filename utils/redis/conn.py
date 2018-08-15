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
import redis

CONF = configparser.ConfigParser()
CONF.read('/etc/.hwzabbix/config.ini')

REDIS_HOST = CONF.get('redis', 'host')
REDIS_PORT = CONF.get('redis', 'port')
REDIS_PASSWORD = CONF.get('redis', 'password')
REDIS_DB = CONF.get('redis', 'db')


def redis_pool():
    """redis conn pool
    :returns: TODO

    """
    try:
        r_p = redis.ConnectionPool(
            host=REDIS_HOST,
            password=REDIS_PASSWORD,
            port=REDIS_PORT,
            db=REDIS_DB,
            decode_responses=True)
        redis_conn = redis.Redis(connection_pool=r_p)
        return redis_conn
    except Exception as error:
        raise error
