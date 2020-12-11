class DoubleNode(object):
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None


class DoubleLinkedList(object):
    def __init__(self):
        self.head = None

    def is_empty(self):
        # 链表是否为空
        return self.head is None

    def length(self):
        # 链表长度
        cur = self.head
        count = 0
        while cur is not None:
            count += 1
            cur = cur.next
        return count

    def add(self, data):
        node = DoubleNode(data)
        if self.is_empty():
            self.head = node
        else:
            node.next = self.head
            self.head.prev = node
            self.head = node

    def append(self, data):
        node = DoubleNode(data)
        if self.is_empty():
            self.head = node
        else:
            cur = self.head
            while cur.next is not None:
                cur = cur.next
            cur.next = node
            node.prev = cur

    def insert(self, pos, data):
        if pos <= 0:
            self.add(data)
        elif pos > self.length() - 1:
            self.append(data)
        else:
            node = DoubleNode(data)
            cur = self.head
            count = 0
            # 把cur移动到指定位置的前一个位置
            while count < (pos - 1):
                count += 1
                cur = cur.next
            # node的prev指向cur
            node.prev = cur
            # node的next指向cur的next
            node.next = cur.next
            cur.next.prev = node
            cur.next = node

    def remove(self, data):
        if self.is_empty():
            return
        else:
            cur = self.head
            if cur.data == data:
                # 首节点是要删除的节点
                if cur.next is None:
                    # 说明链表中只有一个节点
                    self.head = None
                else:
                    # 链表多于一个节点的情况
                    cur.next.prev = None
                    self.head = cur.next
            else:
                # 首节点不是要删除的节点
                while cur is not None:
                    if cur.data == data:
                        cur.prev.next = cur.next
                        cur.next.prev = cur.prev
                        break
                    cur = cur.next

    def search(self, item):
        cur = self.head
        while cur is not None:
            if cur.item == item:
                return True
            cur = cur.next
        return False
