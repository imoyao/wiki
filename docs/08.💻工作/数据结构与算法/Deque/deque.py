#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by imoyao at 2019/6/10 18:57


class Deque:
    """模拟双端队列"""

    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def addFront(self, item):
        """
        队首添加
        :param item:
        :return:
        """
        self.items.append(item)

    def addRear(self, item):
        """
        队尾添加
        :param item:
        :return:
        """
        self.items.insert(0, item)

    def removeFront(self):
        """
        队首移除
        :return:
        """
        if not self.isEmpty():
            return self.items.pop()

    def removeRear(self):
        """
        队尾移除
        :return:
        """
        if not self.isEmpty():
            return self.items.pop(0)

    def size(self):
        return len(self.items)


if __name__ == '__main__':
    d = Deque()
    print(d.isEmpty())
    d.addRear(4)
    d.addRear('dog')
    d.addFront('cat')
    d.addFront(True)
    print(d.size())
    print(d.isEmpty())
    d.addRear(8.4)
    print(d.removeRear())
    print(d.removeFront())
