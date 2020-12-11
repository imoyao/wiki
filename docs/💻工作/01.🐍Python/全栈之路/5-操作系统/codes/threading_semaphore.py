#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by imoyao at 2020/6/29 14:42
"""
限制并发访问
模拟餐厅翻台：
一个餐厅只有
"""
import threading
import time
import random
import logging


class ActivePool:
    def __init__(self):
        super(ActivePool, self).__init__()
        self.active = []
        self.lock = threading.Lock()

    def make_active(self, name):
        with self.lock:
            self.active.append(name)
            logging.debug('Running: %s', self.active)

    def make_inactive(self, name):
        with self.lock:
            logging.debug('Removing: %s from %s', name, self.active)
            self.active.remove(name)


def worker(s, pool):
    logging.debug('Waiting to join the pool')
    with s:
        name = threading.current_thread().name
        pool.make_active(name)
        pause_time = random.randint(1, 5) / 10
        logging.debug('sleeping %0.2f', pause_time)
        time.sleep(pause_time)
        pool.make_inactive(name)


def main(tables, users):
    pool = ActivePool()
    s = threading.Semaphore(tables)
    for i in range(users):
        t = threading.Thread(
            target=worker,
            name='thread' + str(i),
            args=(s, pool),
        )
        t.start()


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s (%(threadName)-2s) %(message)s',
    )
    TABLES = 10
    USERS = 55
    main(TABLES, USERS)
    '''
    打印返回结果，我们可以看到，当不够时，会往里加，满额时，停止加入，消耗之后，继续加入
    '''
