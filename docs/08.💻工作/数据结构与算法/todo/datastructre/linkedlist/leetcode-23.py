"""
23. Merge k Sorted Lists

Merge k sorted linked lists and return it as one sorted list. Analyze and describe its complexity.

Example:

Input:
[
  1->4->5,
  1->3->4,
  2->6
]
Output: 1->1->2->3->4->4->5->6

solution
对于这个问题，有这样两种主要的思路：

从这k个链表中找出最小的连接到dummy node上，知道所有链表为空。
把merge k简化成merge 2，也就是每次只merge两个链表，知道lists中只剩下一个链表。

参考 https://blog.csdn.net/PKU_Jade/article/details/78105723


"""


# Definition for singly-linked list.
from typing import List


class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None

class Solution:
    def mergeKLists(self, lists: List[ListNode]) -> ListNode:
        if len(lists) < 1: return []
        head = ListNode(0)
        head.next = lists[0]
        for lst in lists[1:]:
            node = head
            item = lst
            while item and node.next:
                if node.next.val > item.val:
                    nodebak = node.next
                    node.next = ListNode(item.val)
                    node = node.next
                    node.next = nodebak
                    item = item.next
                else:
                    node = node.next
            if item:
                node.next = item
        return head.next