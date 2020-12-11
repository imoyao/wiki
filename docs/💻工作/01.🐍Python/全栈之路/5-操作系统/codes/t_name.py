#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by imoyao at 2020/6/28 15:09
import sys
import threading
import time


def work():
    print('this is {},name is {}'.format(sys._getframe().f_code.co_name, threading.current_thread().name))
    time.sleep(2)


def service():
    print('this is {},name is {}'.format(sys._getframe().f_code.co_name, threading.current_thread().name))
    time.sleep(.3)


def main():
    print(threading.current_thread().name)
    w = threading.Thread(target=work, name='my_work', daemon=True)
    s = threading.Thread(target=service, name='my_server')
    w.start()
    s.start()


if __name__ == '__main__':
    main()
