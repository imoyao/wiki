#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by imoyao at 2019/5/21 11:32

import pathlib
import sys

util_p = pathlib.Path('..').resolve()
sys.path.append(str(util_p))

from util import utils


class TailRecurseException(Exception):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs


def tail_call_optimized(g):
    """
    参见:https://segmentfault.com/a/1190000007641519
    当递归函数被该装饰器修饰后, 递归调用在装饰器while循环内部进行,
    每当产生新的递归调用栈帧时: f.f_back.f_back.f_code == f.f_code:, 就捕获当前尾调用函数的参数, 并抛出异常,
    从而销毁递归栈并使用捕获的参数手动调用递归函数. 所以递归的过程中始终只存在一个栈帧对象, 达到优化的目的。
    :param g:
    :return:
    """

    def func(*args, **kwargs):
        f = sys._getframe()
        '''
        import sys
        help(sys._getframe)
        
        _getframe(...)
        
        _getframe([depth]) -> frameobject
        
        Return a frame object from the call stack.  If optional integer depth is
        given, return the frame object that many calls below the top of the stack.
        If that is deeper than the call stack, ValueError is raised.  The default
        for depth is zero, returning the frame at the top of the call stack.
        
        This function should be used for internal and specialized
        purposes only.
        从调用堆栈返回一个框架对象。如果给定可选的整数深度，则返回多重调用栈顶部下方的框架对象；
        如果比调用栈更深，捕获 ValueError，对于默认深度零，返回调用堆栈的顶部帧。

        '''
        if f.f_back and f.f_back.f_back and f.f_back.f_back.f_code == f.f_code:
            raise TailRecurseException(*args, **kwargs)
        while True:
            try:
                return g(*args, **kwargs)
            except TailRecurseException as e:
                args = e.args
                kwargs = e.kwargs

    func.__doc__ = g.__doc__
    return func


def factorial(n):
    """
    阶乘运算
    :param n:
    :return:
    """
    if n < 0:
        raise Exception('Factorial num should be a natural number.')
    elif n <= 1:  # 基线条件（base case）
        return 1
    else:
        return n * factorial(n - 1)  # 递归条件（recursive case）


def tail_recursion_fact(n):
    """
    阶乘的尾递归实现
    :param n:
    :return:
    """
    return fact_iter(n, 1)


# @tail_call_optimized            # 该装饰器开启 Python 尾递归优化
def fact_iter(num, result=1):
    if num == 1:
        return result
    return fact_iter(num - 1, num * result)


def get_fib_item_recursion(n):
    """
    递归方式获取斐波那契数列第 n 项
    :param n:
    :return:
    """
    if n <= 1:
        return n
    return get_fib_item_recursion(n - 1) + get_fib_item_recursion(n - 2)


def get_fib_item_tail_recursion(num, result=0, temp=1):
    if num == 0:
        return result
    return get_fib_item_tail_recursion(num - 1, temp, result + temp)


@utils.show_time
def fib_tail_recursion(num):
    fib_li = []
    for i in range(num + 1):  # 注意：0不是第一项，而是第零项，第一项为1
        fib_item = get_fib_item_tail_recursion(i)
        fib_li.append(fib_item)
    return fib_li[1:]


@utils.show_time
def fib_recursion(num):
    """
    获取Fibonacci数列前 n 项
    该函数内部没有使用递归，只是其中的函数调用 get_fib_item_recursion() 实现了递归
    :param num:
    :return:
    """
    fib_li = []
    for i in range(num + 1):  # 注意：0不是第一项，而是第零项，第一项为1
        fib_item = get_fib_item_recursion(i)
        fib_li.append(fib_item)
    return fib_li[1:]


def get_fib_item_normal(n):
    """
    使用迭代方式获取斐波那契数列第 n 项
    :param n:
    :return:
    """
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


@utils.show_time
def fib_normal(num):
    """
    获取Fibonacci数列前 n 项
    :param num: num,自然数
    :return: list
    """
    fib_li = []
    for i in range(num + 1):
        fib_li.append(get_fib_item_normal(i))
    return fib_li[1:]


if __name__ == '__main__':
    test_num = 30
    print(factorial(test_num))
    print(tail_recursion_fact(test_num))
    print(get_fib_item_recursion(test_num))
    print(get_fib_item_normal(test_num))
    print(fib_normal(test_num))
    print(fib_recursion(test_num))
    print(get_fib_item_tail_recursion(test_num))
    print(fib_tail_recursion(test_num))
