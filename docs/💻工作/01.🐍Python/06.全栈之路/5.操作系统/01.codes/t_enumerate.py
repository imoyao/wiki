#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by imoyao at 2020/6/28 15:40
import threading
import time
import random
import logging


def worker():
    pause_time = random.randint(1, 5) / 10
    logging.debug('sleeping %0.2f', pause_time)
    time.sleep(pause_time)
    print('this is worker thread.')


logging.basicConfig(
    level=logging.DEBUG,
    format='(%(threadName)-10s) %(message)s',
)


def main():
    for i in range(3):
        t = threading.Thread(target=worker, daemon=True)
        t.start()

    main_thread = threading.main_thread()
    for t in threading.enumerate():
        if t is not main_thread:

            logging.debug('joining %s', t.getName())
            t.join()


if __name__ == '__main__':
    main()
