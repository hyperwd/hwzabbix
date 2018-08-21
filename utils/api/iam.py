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
import datetime
import time
from utils.redis import conn
from utils.auth import signer
from utils.log import log


class Iam(object):
    """Docstring for zeus. """

    def __init__(self, path_config):
        """TODO: to be defined1.

        :path_config: TODO

        """
        self._path_config = path_config
        self._redis_pool = conn.redis_pool()
        self._account_key = 'account'
        self._d_account = self._redis_pool.hgetall(self._account_key)
        self._date_today = datetime.date.today()
        self._date_tommorrow = self._date_today + datetime.timedelta(days=1)
        self._extime = datetime.datetime.strptime(
            str(self._date_tommorrow),
            '%Y-%m-%d') + datetime.timedelta(hours=1)

    def account_to_redis(self):
        """TODO: Docstring for account_to_redis.
        :returns: TODO

        """
        try:
            #get ak,sk from config.ini
            conf = configparser.ConfigParser()
            conf.read(self._path_config)
            d_account = {
                'ak': conf.get('hw', 'ak'),
                'sk': conf.get('hw', 'sk'),
            }
            #push ak,sk to redis,field is account
            self._redis_pool.hmset(self._account_key, d_account)
            return None
        except Exception as error:
            log.logging.error(error)

    def pid_to_redis(self, region):
        """TODO: Docstring for pid_to_redis.

        :region: TODO
        :returns: TODO

        """
        try:
            dpid = {}
            pid_key = 'pid_' + region + '_' + self._date_today.strftime(
                '%Y-%m-%d')
            #get ak,sk from redis
            #get the porject info from huaweicloud openapi
            l_resp_pid = signer.Sign(self._d_account['ak'],
                                     self._d_account['sk'], 'GET',
                                     'iam.' + region + '.myhuaweicloud.com',
                                     '/v3/auth/projects').sign()['projects']
            for proj in l_resp_pid:
                if region in proj['name']:
                    dpid[proj['name']] = proj['id']
            #push ak,sk to redis,field is account and set expire time
            self._redis_pool.hmset(pid_key, dpid)
            self._redis_pool.expireat(pid_key, self._extime)
            return None
        except Exception as error:
            log.logging.error(error)
