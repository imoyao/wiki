#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Administrator at 2019/9/17 21:43


class Node:
    """
    节点类
    """

    def __init__(self, data, next_node=None):
        self.data = data
        self.next_node = next_node

    def __repr__(self):
        return str(self.data)


class LinkedList:
    """
    单链表类
    """

    def __init__(self):
        self.head = None

    def __iter__(self):
        node = self.head
        while node:
            yield node.data
            node = node.next_node

    def is_empty(self):
        """
        链表头是None，则为空
        :return:
        """
        return self.head is None

    def insert_head(self, data):
        """
        头部插入
        :param data:
        :return:
        """
        new_node = Node(data)  # 初始化节点
        if self.head is not None:
            new_node.next_node = self.head  # 节点指向原来的头
        self.head = new_node  # 该节点作为节点头

    def insert_tail(self, data):
        """
        节点尾部插入
        :param data:
        :return:
        """
        if self.head is None:  # 没有头，直接调用插入头的方法
            self.insert_head(data)
        else:
            temp = self.head  # 有头，顺着链表一直往下找，找到最后，将该节点作为最后节点
            while temp.next_node:
                temp = temp.next_node
            temp.next_node = Node(data)

    def show_node_data(self):
        """
        打印每个节点的数据
        开始指向节点头，直到节点的next指向空，每一次打印节点data
        :return:
        """
        _temp = self.head
        while _temp is not None:
            print(_temp.data)
            _temp = _temp.next_node

    def delete_head(self):
        """
        从链表头部删除
        先拿到旧的链表头，然后链表头指向原来链表头的下一个，原来的头的next指向空
        :return:
        """
        _temp = self.head
        if self.head is not None:
            self.head = self.head.next_node
            _temp.next_node = None
        return _temp

    def delete_tail(self):
        """
        删除链表尾
        :return:
        """
        _temp = self.head
        if self.head is not None:  # 如果头不是None,如果头的指向为空，则删除尾即为将头指向None
            if self.head.next_node is None:
                self.head = None

            else:
                while _temp.next_node.next_node is not None:  # 当头的next的next不为空，则继续往下找，直到找到倒数第二个节点
                    _temp = _temp.next_node

                _temp.next_node, _temp = None, _temp.next_node  # 将倒数第二个节点的next指向None,该节点变为最后一个节点（a,b = b,a）
        return _temp

    def reverse(self):
        """
        反转链表
        :return:
        """
        prev = None
        current = self.head
        while current:
            # _temp = current.next_node  # 对当前节点的下一个节点赋值
            # current.next_node = prev  # 反转当前节点的下一个节点指向前一节点
            # prev = current  # 前一个节点变成当前节点
            # current = _temp  # 节点偏移/迭代
            '''The above code equate to the follow.'''
            current.next_node, prev, current = prev, current, current.next_node
        self.head = prev  # 原来的链表头指向新的链表头

    @staticmethod
    def find_middle_node(head):
        """
        查找链表中间节点（必须保证节点的数量最少是1，否则如果初始化是空的话fast.next会报错。）
        定义快慢两个指针，快的走两步，慢的走一步；如果是奇数项，快的走到头，慢的刚好走到中间；
        如果是偶数项，快的指向空，慢的刚好指向中间两项的后一项
        :param head: 链表头
        :return:
        """
        slow, fast = head, head
        fast = fast.next_node if fast else None
        while fast and fast.next_node:
            slow, fast = slow.next_node, fast.next_node.next_node
        return slow


def main():
    link_list = LinkedList()
    for i in range(10):
        link_list.insert_tail(i)
    link_list.show_node_data()
    print('==before===insert head======')
    for i in range(10, 20):
        link_list.insert_head(str(i))
    link_list.show_node_data()
    link_list.delete_head()
    print('==before===reverse it======')
    link_list.reverse()
    link_list.delete_tail()
    link_list.show_node_data()
    ########################
    # print("Inserting 1st at Head")
    # a1 = input()
    # link_list.insert_head(a1)
    # print("Inserting 2nd at Head")
    # a2 = input()
    # link_list.insert_head(a2)
    # print("\nPrint List : ")
    # link_list.show_node_data()
    # print("\nInserting 1st at Tail")
    # a3 = input()
    # link_list.insert_tail(a3)
    # print("Inserting 2nd at Tail")
    # a4 = input()
    # link_list.insert_tail(a4)
    # print("\nPrint List : ")
    # link_list.show_node_data()
    # print("\nDelete Head")
    # link_list.delete_head()
    # print("Delete Tail")
    # link_list.delete_tail()
    # print("\nPrint List : ")
    # link_list.show_node_data()
    # print("\nReverse Linked List")
    # link_list.reverse()
    # print("\nPrint List : ")
    # link_list.show_node_data()


def find_mid():
    link = LinkedList()
    n1 = Node(1)
    n2 = Node(2, n1)
    n3 = Node(3, n2)
    n4 = Node(4, n3)
    n5 = Node(5, n4)
    print(link.find_middle_node(n5))


if __name__ == '__main__':
    main()
    # find_mid()
