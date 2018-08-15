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
import time
import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from utils.redis import conn
from utils.auth import signer

REDIS_POOL = conn.redis_pool()
SCHED = BackgroundScheduler()
DATE_TODAY = datetime.date.today()
DATE_TOMMORROW = DATE_TODAY + datetime.timedelta(days=1)
ACCOUNT_KEY = 'account'
PID_KEY = 'project' + '_' + DATE_TODAY.strftime('%Y-%m-%d')
EIP_KEY = 'eipinfo' + '_' + DATE_TODAY.strftime('%Y-%m-%d')
EXTIME = datetime.datetime.strptime(str(DATE_TOMMORROW),
                                    '%Y-%m-%d') + datetime.timedelta(hours=1)


@SCHED.scheduled_job('interval', seconds=3)
def account_to_redis():
    """set ak,sk to redis
    :returns: None

    """
    try:
        #get ak,sk from config.ini
        conf = configparser.ConfigParser()
        conf.read('/etc/.hwzabbix/config.ini')
        d_account = {
            'ak': conf.get('hw', 'ak'),
            'sk': conf.get('hw', 'sk'),
        }
        #push ak,sk to redis,field is account
        REDIS_POOL.hmset(ACCOUNT_KEY, d_account)
        print('account')
    except Exception as error:
        raise error


@SCHED.scheduled_job('interval', seconds=5)
def pid_to_redis():
    """set the all project id to redis
    :returns: None

    """
    try:
        d_project = {}
        #get ak,sk from config.ini
        conf = configparser.ConfigParser()
        conf.read('/etc/.hwzabbix/config.ini')
        d_account = {
            'ak': conf.get('hw', 'ak'),
            'sk': conf.get('hw', 'sk'),
        }
        #get the porject info from huaweicloud openapi
        respon = signer.Sign(d_account['ak'], d_account['sk'], 'GET',
                             'iam.cn-north-1.myhuaweicloud.com',
                             '/v3/auth/projects')
        for proj in respon.sign()['projects']:
            d_project[proj['name']] = proj['id']
        #push ak,sk to redis,field is account and set expire time
        REDIS_POOL.hmset(PID_KEY, d_project)
        REDIS_POOL.expireat(PID_KEY, EXTIME)
        print('pid')
    except Exception as error:
        raise error


@SCHED.scheduled_job('interval', seconds=30)
def eip_info():
    """TODO: Docstring for eip_info.
    :returns: TODO

    """
    try:
        d_eipinfo = {}
        #get ak,sk from config.ini
        conf = configparser.ConfigParser()
        conf.read('/etc/.hwzabbix/config.ini')
        d_account = {
            'ak': conf.get('hw', 'ak'),
            'sk': conf.get('hw', 'sk'),
        }
        #get the porject info from redis
        d_project = REDIS_POOL.hgetall(PID_KEY)
        #get the eip info from huaweicloud openapi
        for key in d_project.keys():
            if 'cn-north-' in key:
                d_eiptmp = {}
                d_eiptmp['project_name'] = key
                respon = signer.Sign(
                    d_account['ak'],
                    d_account['sk'],
                    'GET',
                    'vpc.cn-north-1.myhuaweicloud.com',
                    '/v1/' + d_project[key] + '/publicips',
                    x_project_id=d_project[key])
                for eip in respon.sign()['publicips']:
                    d_eiptmp['project_id'] = eip['tenant_id']
                    d_eiptmp['id'] = eip['id']
                    d_eipinfo[eip['public_ip_address']] = d_eiptmp
            if 'cn-east-' in key:
                d_eiptmp = {}
                d_eiptmp['project_name'] = key
                respon = signer.Sign(
                    d_account['ak'],
                    d_account['sk'],
                    'GET',
                    'vpc.cn-east-2.myhuaweicloud.com',
                    '/v1/' + d_project[key] + '/publicips',
                    x_project_id=d_project[key])
                for eip in respon.sign()['publicips']:
                    d_eiptmp['project_id'] = eip['tenant_id']
                    d_eiptmp['id'] = eip['id']
                    d_eipinfo[eip['public_ip_address']] = d_eiptmp
            if 'cn-south-' in key:
                d_eiptmp = {}
                d_eiptmp['project_name'] = key
                respon = signer.Sign(
                    d_account['ak'],
                    d_account['sk'],
                    'GET',
                    'vpc.cn-south-1.myhuaweicloud.com',
                    '/v1/' + d_project[key] + '/publicips',
                    x_project_id=d_project[key])
                for eip in respon.sign()['publicips']:
                    d_eiptmp['project_id'] = eip['tenant_id']
                    d_eiptmp['id'] = eip['id']
                    d_eipinfo[eip['public_ip_address']] = d_eiptmp
            if 'cn-northeast-' in key:
                d_eiptmp = {}
                d_eiptmp['project_name'] = key
                respon = signer.Sign(
                    d_account['ak'],
                    d_account['sk'],
                    'GET',
                    'vpc.cn-northeast-1.myhuaweicloud.com',
                    '/v1/' + d_project[key] + '/publicips',
                    x_project_id=d_project[key])
                for eip in respon.sign()['publicips']:
                    d_eiptmp['project_id'] = eip['tenant_id']
                    d_eiptmp['id'] = eip['id']
                    d_eipinfo[eip['public_ip_address']] = d_eiptmp
            if 'ap-southeast-' in key:
                d_eiptmp = {}
                d_eiptmp['project_name'] = key
                respon = signer.Sign(
                    d_account['ak'],
                    d_account['sk'],
                    'GET',
                    'vpc.ap-southeast-1.myhuaweicloud.com',
                    '/v1/' + d_project[key] + '/publicips',
                    x_project_id=d_project[key])
                for eip in respon.sign()['publicips']:
                    d_eiptmp['project_id'] = eip['tenant_id']
                    d_eiptmp['id'] = eip['id']
                    d_eipinfo[eip['public_ip_address']] = d_eiptmp
        #push ak,sk to redis,field is account and set expirt time
        REDIS_POOL.hmset(EIP_KEY, d_eipinfo)
        REDIS_POOL.expireat(EIP_KEY, EXTIME)
        #delete the not exist eip info from redis
        print('eip_info')
    except Exception as error:
        raise error


SCHED.start()
while True:
    time.sleep(100)
