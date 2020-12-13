#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by imoyao at 2020/6/28 14:02
# -*- coding:utf-8 -*-
import threading
import time


def worker(i):
    time.sleep(3)
    print('this is the worker {}\n'.format(i))


def main():
    t1 = threading.Thread(target=worker, args=('Daemon is True',), daemon=True)
    t1.start()
    t1.join()   # 阻塞，t1执行完，再终止
    # t2 = threading.Thread(target=worker, args=('Daemon is False',))
    # t2.start()
    print('main done')


if __name__ == '__main__':
    main()
