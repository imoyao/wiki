#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by imoyao at 2019/5/14 14:16
import time
import random


def show_time(func):
    def wrap_func(*args, **kwargs):
        start_time = time.time()
        ret_result = func(*args, **kwargs)
        end_time = time.time()
        print('The function **{0}** takes {1} time.'.format(func.__name__, end_time - start_time))
        return ret_result

    return wrap_func


@show_time
def foo(n):
    for _ in list(range(n)):
        pass


def rand_list(n=10):
    """
    生成长度为 n 的 1000 以内随机数组
    :param n:int,希望生成的数组长度
    :return: 随机生成的乱序数组
    """
    random_list = []
    for i in range(n):
        num = random.randint(1, 1000)
        random_list.append(num)
    return random_list


if __name__ == '__main__':

    foo(100)
