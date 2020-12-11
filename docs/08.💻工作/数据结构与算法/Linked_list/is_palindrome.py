#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by imoyao at 2019/9/24 15:31


def reverse(head):
    """
    反转链表
    :param head:
    :return:
    """
    prev = None
    while head:
        new_next = head.next_node
        head.next_node = prev
        prev = head
        head = new_next
    return prev


def is_palindrome(linked_list):
    """
    https://www.jianshu.com/p/22b934f351ef
    :param linked_list:
    :return:
    """
    slow = linked_list.head
    fast = linked_list.head
    index_position = 0
    while fast and fast.next_node:
        slow = slow.next_node
        fast = fast.next_node.next_node

        index_position += 1

    reverse_nodes = reverse(slow)
    head_node = linked_list.head
    is_palin = True
    while head_node and reverse_nodes:
        if head_node.data == reverse_nodes.data:
            head_node = head_node.next_node
            reverse_nodes = reverse_nodes.next_node
        else:
            is_palin = False
            break
    return is_palin

# def is_palindrome(head):
#     """
#     判断回文（链表实现）
#     :param head:
#     :return:
#     """
#     if not head:
#         return True
#     fast, slow = head.next, head
#     # 快慢指针
#     while fast and fast.next_node:
#         fast = fast.next_node.next_node
#         slow = slow.next_node
#     second = slow.next_node
#     slow.next_node = None
#     node = None
#     while second:
#         nxt = second.next_node
#         second.next_node = node
#         node = second
#         second = nxt
#     while node:
#         if node.data != head.data:
#             return False
#         node = node.next_node
#         head = head.next
#     return True
