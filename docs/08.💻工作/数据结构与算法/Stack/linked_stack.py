#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by imoyao at 2019/9/17 15:58

"""
基于链表实现的栈
"""


class Node:

    def __init__(self, data, next_node=None):
        self.data = data
        self.next_node = next_node


class LinkedStack:
    """A stack based upon singly-linked list.
    """

    def __init__(self):
        self._head = None
        self._size = 0

    def __repr__(self):
        current = self._head
        nums = []
        while current:
            nums.append(current.data)
            current = current.next_node
        ret = ','.join([repr(num) for num in nums])
        return f'[{ret}]'

    def is_empty(self):
        return self._size == 0

    def size(self):
        return self._size

    def push(self, item):
        new_head = Node(item)
        new_head.next_node = self._head
        self._head = new_head
        self._size += 1

    def pop(self):
        if not self._size:
            print('StackOverflow')
        else:
            item = self._head.data
            self._head = self._head.next_node
            return item

    def top(self):
        """
        返回栈顶元素
        :return: 
        """
        if not self._size:
            print('StackOverflow.')
        else:
            return self._head.data


if __name__ == '__main__':
    s = LinkedStack()
    print(s.is_empty())
    s.push(4)
    print(s)
    s.push('dog')
    print(s)
    print(s.top())
    s.push(True)
    print(s)
    print(s.size())
    print(s.is_empty())
    print(s.pop())
