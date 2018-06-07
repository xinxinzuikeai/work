# coding:utf8
from __future__ import absolute_import
import time
from celery import shared_task

@shared_task
def celeryTask():
    print 'previous test'
    time.sleep(3)
    print 'next test'