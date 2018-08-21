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


class Vpc(object):
    """Docstring for zeus. """

    def __init__(self):
        """TODO: to be defined1.

        """
        self._redis_pool = conn.redis_pool()
        self._account_key = 'account'
        self._d_account = self._redis_pool.hgetall(self._account_key)
        self._date_today = datetime.date.today()
        self._date_tommorrow = self._date_today + datetime.timedelta(days=1)
        self._extime = datetime.datetime.strptime(
            str(self._date_tommorrow),
            '%Y-%m-%d') + datetime.timedelta(hours=1)


    def eip_to_redis(self, region):
        """TODO: Docstring for eip_to_redis.

        :region: TODO
        :returns: TODO

        """
        try:
            deip = {}
            pid_key = 'pid_' + region + '_' + self._date_today.strftime(
                '%Y-%m-%d')
            eip_key = 'eip_' + region + '_' + self._date_today.strftime(
                '%Y-%m-%d')
            #get ak,sk from redis
            #get the porject info from redis
            lpid = (i for i in self._redis_pool.hgetall(pid_key).values())
            #get the eip info from huaweicloud openapi
            for pid in lpid:
                l_res = signer.Sign(
                    self._d_account['ak'],
                    self._d_account['sk'],
                    'GET',
                    'vpc.' + region + '.myhuaweicloud.com',
                    '/v1/' + pid + '/publicips',
                    x_project_id=pid).sign()['publicips']
                for eip in l_res:
                    eip['region'] = region
                    deip[eip['public_ip_address']] = eip
            #push ak,sk to redis,field is account and set expirt time
            self._redis_pool.hmset(eip_key, deip)
            self._redis_pool.expireat(eip_key, self._extime)
            return None
        except Exception as error:
            log.logging.error(error)
