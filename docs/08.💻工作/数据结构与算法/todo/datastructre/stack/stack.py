"""
https://zhuanlan.zhihu.com/p/37840774
栈
用数组实现一个顺序栈
用链表实现一个链式栈
编程模拟实现一个浏览器的前进、后退功能

"""


# import datastructre.linkedlist.linkedlist as linkedlistfile
class Stack(object):
    # 初始化栈为空列表
    def __init__(self):
        self.items = []

    # 判断栈是否为空，返回布尔值
    def is_empty(self):
        return self.items == []

    # 返回栈顶元素
    def peek(self):
        return self.items[-1]

    # 返回栈的大小
    def size(self):
        return len(self.items)

    # 压栈
    def push(self, item):
        self.items.append(item)

    # 出栈
    def pop(self):
        return self.items.pop()

    def clear(self):
        del self.items[:]


class LinkedListStack(object):
    """
    """

    def __init__(self):
        self._data = LinkedList()

    def get_size(self):
        return self._data.size()

    def is_empty(self):
        return self._data.is_empty()

    def push(self, e):
        self._data.prepend(e)

    def pop(self):
        if self._data.is_empty():
            return None
        return self._data.remove_first()

    def peek(self):
        if self._data.is_empty():  # 以后在写链表的时候要注意边界情况
            return None
        return self._data.get_first()

    def __str__(self):

        return str(self._data)


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

    def remove_first(self):
        tmp = self.head.data
        self.head = self.head.next
        return tmp

    def get_first(self):
        return self.head.data

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


# 我们使用两个栈X和Y，我们把首次浏览的页面依次压入栈X，当点击后退按钮时，再依次从栈X中出栈，并将出栈的数据一次放入Y栈。
# 当点击前进按钮时，我们依次从栈Y中取出数据，放入栈X中。当栈X中没有数据时，说明没有页面可以继续后退浏览了。
# 当Y栈没有数据，那就说明没有页面可以点击前进浏览了。

class WebViewList(object):
    def __init__(self):
        self._stackA = Stack()
        self._stackB = Stack()

    def forward(self):
        if self._stackB.size() == 0:  # 此处是0，原因是
            return None
        url = self._stackB.pop()
        self._stackA.push(url)
        return self._stackA.peek()

    def back(self):
        if self._stackA.size() == 1:  # 此处是1 ，原因是退到最后一个页面无法再退
            return None
        url = self._stackA.pop()
        self._stackB.push(url)
        return self._stackA.peek()

    def load(self, url):
        self._stackA.push(url)
        return url


if __name__ == '__main__':
    # linkedStack = LinkedListStack()
    # linkedStack.push(5)
    # linkedStack.push(3)
    # print(linkedStack.pop())
    # print(linkedStack.get_size())
    # print(linkedStack.pop())
    # print(linkedStack.pop())

    weblist = WebViewList()
    weblist.load("test1")
    weblist.load("test2")
    weblist.load("test3")
    weblist.load("test4")
    print(weblist.back())
    print(weblist.back())
    print(weblist.back())
    print(weblist.back())

    print(weblist.forward())
    print(weblist.forward())
    print(weblist.forward())
    print(weblist.forward())
