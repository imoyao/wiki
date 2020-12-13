#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by imoyao at 2020/6/28 17:21
import logging
import threading
import time


def consumer(con):
    """
    先启动消费者，不然生产者发出之后也收不到了
    :param con:
    :return:
    """
    logging.debug('Starting consumer thread,just waiting……')
    with con:
        con.wait()
        time.sleep(.8)
        logging.debug('Resource is available to consumer')


def producer(con):
    logging.debug('Starting producer thread')
    with con:
        logging.debug('notifyAll working……')
        time.sleep(.1)
        con.notifyAll()


logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s (%(threadName)-2s) %(message)s',
)


def main():
    con = threading.Condition()
    for i in range(5):
        c = threading.Thread(name='c' + str(i), target=consumer, args=(con,))
        c.start()

    for i in range(3):
        c = threading.Thread(name='p' + str(i), target=producer, args=(con,))
        c.start()


main()
