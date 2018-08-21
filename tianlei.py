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
import time
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from utils.log import log
from utils.api import iam
from utils.api import vpc

SCHED = BackgroundScheduler()
ACCOUNT_TRIGGER = IntervalTrigger(seconds=3)
PID_TRIGGER = IntervalTrigger(seconds=5)
EIP_TRIGGER = IntervalTrigger(seconds=10)

FUNC_IAM = iam.Iam('/etc/.hwzabbix/config.ini')
FUNC_ACCOUNT = FUNC_IAM.account_to_redis
FUNC_PID = FUNC_IAM.pid_to_redis

FUNC_VPC = vpc.Vpc()
FUNC_EIP = FUNC_VPC.eip_to_redis

SCHED.add_job(func=FUNC_ACCOUNT, trigger=ACCOUNT_TRIGGER)
SCHED.add_job(func=FUNC_PID, args=('cn-north-1',),trigger=PID_TRIGGER)
SCHED.add_job(func=FUNC_PID, args=('cn-east-2',),trigger=PID_TRIGGER)
SCHED.add_job(func=FUNC_PID, args=('cn-south-1',),trigger=PID_TRIGGER)
SCHED.add_job(func=FUNC_EIP, args=('cn-north-1',),trigger=EIP_TRIGGER)
SCHED.add_job(func=FUNC_EIP, args=('cn-east-2',),trigger=EIP_TRIGGER)
SCHED.add_job(func=FUNC_EIP, args=('cn-south-1',),trigger=EIP_TRIGGER)

SCHED.start()
while True:
    time.sleep(100)
