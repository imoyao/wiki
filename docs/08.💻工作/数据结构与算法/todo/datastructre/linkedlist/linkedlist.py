"""
实现单链表、循环链表、双向链表，支持增删操作
实现单链表反转
实现两个有序的链表合并为一个有序链表
实现求链表的中间结点
"""
import math


class Node(object):
    def __init__(self, value):
        self.data = value
        self.next = None


class LinkedList:
    # 初始化，头结点为空
    def __init__(self):
        self.head = None

    # 添加节点，添加的新节点作为新的头结点
    def prepend(self, data):
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def append(self, data):
        if not self.head:
            self.head = Node(data)
            return
        p = self.head
        while p.next:
            p = p.next
        p.next = Node(data)

    def insert(self, data, key):
        tmp = Node(data)
        p = self.head
        for i in range(key - 1):
            p = p.next
        tmp.next = p.next
        p.next = tmp

    def search(self, data):
        current = self.head
        while current is not None:
            if current.data == data:
                return True
            current = current.next
        return False

    def remove(self, data):
        current = self.head
        pre = None
        while current is not None:
            if current.data == data:
                if current == self.head:
                    self.head = self.head.next
                    return
                pre.next = current.next
                return
            pre = current
            current = current.next

    # 判断链表是否为空
    def is_empty(self):
        return not self.head

    # 返回链表长度
    def size(self):
        count = 0
        counting = self.head  # 从头结点开始计数
        while counting is not None:
            count += 1
            counting = counting.next
        return count

    # 翻转链表
    def reverse(self):
        p = self.head
        q = self.head.next
        p.next = None
        while q:
            r = q.next
            q.next = p
            p = q
            q = r
        return p


#  实现两个有序的链表合并为一个有序链表

def combine(l1, l2):
    if l1 is None and l2 is None:
        return None
    pre = Node(0)
    while l1 is not None and l2 is not None:
        if l1.val < l2.val:
            pre.next = l1
            l1 = l1.next
        else:
            pre.next = l2
            l2 = l2.next
        pre = pre.next
    if l1 is not None:
        pre.next = l1
    else:
        pre.next = l2
    return pre.next


# leetcode 876 链表的中间结点 python实现
class Solution:
    def middleNode(self, head):
        # 首先要知道链表一共有多少个结点
        count = 0
        res = {}
        while head != None:
            count += 1
            res[count] = head
            head = head.next
        j = math.ceil((count - 1) / 2) + 1
        return res[j]
