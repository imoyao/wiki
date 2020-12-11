#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by imoyao at 2019/6/10 17:58


class Queue:
    """
    我们设定队列的队尾在列表的 0 位置。
    这使得我们能够利用列表的 insert 功能来向队列的队尾添加新的元素。而 pop 操作则可以用来移除队首的元素（也就是列表的最后一个元素）。
    这也意味着 enqueue 的复杂度是 O(n)，而 dequeue 的复杂度是 O(1)。
    """

    def __init__(self):
        self.__items = list()

    def __str__(self):
        """
        打印测试
        :return:
        """
        return str(self.__items)

    def isEmpty(self):
        return self.__items == []

    def enqueue(self, new_item):
        """
        入队
        :param new_item:
        :return:
        """
        self.__items.insert(0, new_item)

    def dequeue(self):
        """
        出队
        :return:
        """
        if not self.isEmpty():
            return self.__items.pop()
        return

    def size(self):
        return len(self.__items)


if __name__ == '__main__':
    q = Queue()
    q.enqueue(4)
    q.enqueue('dog')
    print(q)
    q.enqueue(True)
    print(q.size())
    print(q)
