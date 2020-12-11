#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by imoyao at 2020/6/28 16:19

import logging
import threading
import time


def wait_for_event(e):
    """
    等待event被设置之后才会执行
    一直等，等到发出event信号，开始做
    :return:
    """
    logging.debug('wait_for_event starting')
    until_event_is_set = e.wait()
    logging.debug('event set: %s', until_event_is_set)


def wait_for_event_timeout(e, t):
    """
    等超时时间之后，如果没有接受到set，则先去做别的事；
    然后回来接着等，等到event之后，开始做设置好的事情，做完退出
    :param e:
    :param t:
    :return:
    """
    while not e.is_set():
        logging.debug('wait_for_event_timeout starting')
        event_is_set = e.wait(t)
        logging.debug('event set: %s', event_is_set)
        if event_is_set:
            logging.debug('processing event')
        else:
            logging.debug('doing other work')


logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-10s) %(message)s', )

e = threading.Event()

t1 = threading.Thread(name='block thread', target=wait_for_event, args=(e,))
t1.start()

t2 = threading.Thread(name='noblock thread', target=wait_for_event_timeout, args=(e, 1))
t2.start()

logging.debug('Waiting before calling Event.set()')
time.sleep(5)
e.set()  # 设置event为True
logging.debug('Event is set')

'''
(block thread) wait_for_event starting
(noblock thread) wait_for_event_timeout starting
(MainThread) Waiting before calling Event.set()
(noblock thread) event set: False
(noblock thread) doing other work
(noblock thread) wait_for_event_timeout starting
(noblock thread) event set: False
(noblock thread) doing other work
(noblock thread) wait_for_event_timeout starting
(noblock thread) event set: False
(noblock thread) doing other work
(noblock thread) wait_for_event_timeout starting
(noblock thread) event set: False
(noblock thread) doing other work
(noblock thread) wait_for_event_timeout starting
(MainThread) Event is set
(block thread) event set: True
(noblock thread) event set: True
(noblock thread) processing event

Process finished with exit code 0
'''
