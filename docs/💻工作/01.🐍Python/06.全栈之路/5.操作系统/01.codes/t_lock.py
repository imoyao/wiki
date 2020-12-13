#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by imoyao at 2020/6/28 16:52
import logging
import random
import threading
import time

logging.basicConfig(
    level=logging.DEBUG,
    format='(%(threadName)-10s) %(message)s',
)


class Counter:

    def __init__(self, start=0):
        self.lock = threading.Lock()
        self.count = start

    def increment(self):
        logging.debug('Waiting for lock……')
        logging.debug('Acquire lock……')
        self.count += 1
        # self.lock.acquire()
        # try:
        #     logging.debug('Acquire lock……')
        #     self.count += 1
        # finally:
        #     self.lock.release()
        with self.lock:
            logging.debug('Acquire lock……')
            self.count += 1


c = Counter()


def worker(c):
    for i in range(10):
        pause_time = random.randint(1, 5) / 10
        logging.debug('Sleeping %0.2f', pause_time)
        time.sleep(pause_time)
        c.increment()
    logging.debug('This is worker thread done.')


def main():
    for i in range(3):
        t = threading.Thread(target=worker, args=(c,))
        t.start()

    logging.debug('Waiting for worker threads')
    main_thread = threading.main_thread()
    for t in threading.enumerate():
        if t is not main_thread:
            t.join()
    logging.debug('Counter: %d', c.count)


if __name__ == '__main__':
    main()
