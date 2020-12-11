#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by imoyao at 2019/9/19 16:02

class Link:
    """
    定义单个节点
    """
    next = None
    prev = None

    def __init__(self, val):
        self.val = val

    def display_link(self):
        print(f'{self.val}', end=' ')


class DoublyLinkedList:
    """
    定义双链表类
    """

    def __init__(self):
        self.head = None
        self.tail = None

    def __iter__(self):
        _temp = self.head
        while _temp is not None:
            yield _temp.val
            _temp = _temp.next

    def is_empty(self):
        return self.head is None

    def insert_head(self, val):
        """
        从头插入值
        :param val:
        :return:
        """
        new_node = Link(val)  # 初始化
        if self.is_empty():
            self.tail = new_node  # 第一个的尾指向新节点
        else:
            self.head.prev = new_node  # 原来的链表头的前驱指向新节点

        new_node.next = self.head  # 新节点指向原来的链表头
        self.head = new_node  # 新节点作为链表头

    def insert_tail(self, val):
        """
        从尾部插入值
        :param val:
        :return:
        """
        new_node = Link(val)  # 初始化节点
        new_node.next = None  # 新节点的后域指向空
        self.tail.next = new_node  # 原来的尾的后域指向新节点
        new_node.prev = self.tail  # 新节点的前驱指向原来的尾
        self.tail = new_node  # 改节点成为链表的尾

    def delete_head(self):
        """
        从头部删除
        :return:
        """
        _temp = self.head
        self.head = self.head.next  # 原来的头指向的变成新头
        self.head.prev = None  # 原来头的前驱指向空
        if self.head is None:  # 如果头是空
            self.tail = None  # 则尾变空
        return _temp  # 返回删除节点

    def delete_tail(self):
        """
        从尾部删除
        :return:
        """
        _temp = self.tail  # 拿到原来的尾
        self.tail = self.tail.prev  # 现在的尾是原来的尾前驱所指
        self.tail.next = None  # 现在的尾的后域指向空
        return _temp  # 返回原来的尾

    def delete(self, data):
        """
        删除指定值
        :param data:
        :return:
        """
        # 先找到要删除的节点的位置
        current = self.head  # 拿到链表的头
        try:
            while current.val != data:  # 头不等于要删除值继续向后找
                current = current.next
        except AttributeError:
            print(f'The linked list has not data equals {data}')
            return

        if current == self.head:  # 如值等于链表头，则删除值就是删除头
            self.delete_head()
        elif current == self.tail:  # 如果头等于链表尾，则是删除尾
            self.delete_tail()
        else:  # 否则删除中间值
            current.prev.next = current.next  # 删除中间某节点，就是该值的前一个节点的后域指向当前节点的下一个节点
            current.next.prev = current.prev  # 当前节点的后面一个节点的前驱指向当前节点的前驱

    def show_data_of_link(self):
        """
        显示节点值
        :return:
        """
        _temp = self.head
        while _temp is not None:
            _temp.display_link()
            _temp = _temp.next
        print('\n')

    def reverse(self):
        """
        翻转链表
        :return:
        """
        current = self.head
        prev_node = None
        while current is not None:
            _temp = current.next
            current.next = prev_node
            prev_node = current
            current = _temp

        self.head = self.tail
        self.tail = current


def main():
    link = DoublyLinkedList()
    for i in range(5):
        link.insert_head(i)

    link.show_data_of_link()

    for i in range(5):
        link.insert_tail(i)

    link.show_data_of_link()

    link.delete(3)
    link.delete(3)
    link.show_data_of_link()
    link.delete(1)
    link.show_data_of_link()
    link.delete_head()
    link.show_data_of_link()
    link.delete_tail()
    link.show_data_of_link()
    print('===before reverse===')
    link.insert_head('haha')
    link.insert_tail('hehe')
    link.reverse()
    link.show_data_of_link()


if __name__ == '__main__':
    main()
