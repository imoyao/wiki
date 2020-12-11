#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by imoyao at 2019/6/10 17:18
"""
此为使用Python的list模拟栈
"""


class Stack:
    """
    使用Python内建的list直接实现栈
    """

    def __init__(self):
        self.__items = []

    def __str__(self):
        """
        打印测试
        :return:
        """
        return str(self.__items)

    def is_empty(self):
        return self.size() == 0

    def peek(self):
        if not self.is_empty():
            return self.__items[-1]

    def push(self, new_item):
        self.__items.append(new_item)

    def pop(self):
        if not self.is_empty():
            self.__items.pop()
        else:
            return

    def size(self):
        return len(self.__items)


if __name__ == '__main__':
    s = Stack()
    print(s.is_empty())
    s.push(4)
    print(s)
    s.push('dog')
    print(s)
    print(s.peek())
    s.push(True)
    print(s)
    print(s.size())
    print(s.is_empty())
    print(s)
