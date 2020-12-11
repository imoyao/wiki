class Node:
    def __init__(self, elem):
        self.elem = elem
        self.next = None

    def __repr__(self):  # 这个函数将内容‘友好’地显示出来，否则会显示对象的内存地址
        return str(self.elem)


class CycleLinkedList:
    def __init__(self):
        self.head = None

    def is_empty(self):
        """
        判断该链表是否为空
        :return: boolean
        """
        return self.head is None

    def length(self):
        if self.is_empty():
            return 0
        cur = self.head
        count = 1
        while cur.next != self.head:
            count += 1
            cur = cur.next  # 游标移动
        return count

    def traversal(self):
        if self.is_empty():
            return
        cur = self.__head
        while cur.next != self.__head:
            print(cur.value)
            cur = cur.next
        print(cur.value)

    def add(self, value):
        """头插法"""
        node = Node(value)
        if self.is_empty():
            self.head = node
            self.head.next = self.head
            return
        cur = self.head
        while cur.next != self.head:
            cur = cur.next
        # 新节点的next指针指向原头节点
        node.next = self.head
        # 将新节点指向头节点
        self.head = node
        # 尾节点next指针指向新头节点
        cur.next = self.head

    def append(self, value):
        node = Node(value)
        cur = self.head
        if self.is_empty():
            self.head = node
            self.head.next = self.head
            return
        while cur.next != self.head:
            cur = cur.next
        node.next = cur.next
        cur.next = node

    def insert(self, pos, value):
        if pos <= 0:
            self.add(value)
        elif pos > len(self) - 1:
            self.append(value)
        else:
            node = Node(value)
            cur = self.head
            count = 0
            while count < pos - 1:
                count += 1
                cur = cur.next
            node.next = cur.next
            cur.next = node

    def search(self, value):
        if self.is_empty():
            return False
        cur = self.head
        while cur.next != self.head:
            if cur.value == value:
                return True
            else:
                cur = cur.next
        if cur.value == value:
            return True
        return False

    def remove(self, value):
        cur = self.head
        prior = None
        if self.is_empty():
            return
        while cur.next != self.head:
            if cur.value == value:
                # 待删除节点在头部
                if cur == self.head:
                    rear = self.head
                    while rear.next != self.head:
                        rear = rear.next
                    self.head = cur.next
                    rear.next = self.head
                # 待删除节点在中间
                else:
                    prior.next = cur.next
                    return
            else:
                prior = cur
                cur = cur.next
                # 待删除节点在尾部
                if cur.value == value:
                    # 如果链表中只有一个元素，则此时prior为None，Next属性就会报错
                    # 此时直接使其头部元素为None即可
                    if cur == self.head:
                        self.head = None
                        return
                    prior.next = cur.next
