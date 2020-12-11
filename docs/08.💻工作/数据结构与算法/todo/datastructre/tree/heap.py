# parent(i) = floor((i - 1)/2)
# left(i)   = 2i + 1
# right(i)  = 2i + 2
class MaxHeap:
    def __init__(self):
        self.list = []
        self.size = 0

    def insert(self, data):
        self.list.append(data)
        self.size += 1
        self.shift_up(self.size - 1)

    def shift_up(self, index):
        if (index - 1) // 2 >= 0 and self.list[(index - 1) // 2] < self.list[index]:
            self.list[(index - 1) // 2], self.list[index] = self.list[index], self.list[(index - 1) // 2]
            self.shift_up((index - 1) // 2)

    def shift_down(self, index):
        if index * 2 + 1 <= self.size - 1:
            child = index * 2 + 1
            if child + 1 <= self.size - 1:
                if self.list[child] < self.list[child + 1]:
                    child += 1
            if self.list[child] > self.list[index]:
                self.list[child], self.list[index] = self.list[index], self.list[child]
                self.shift_down(child)

    def pop(self):
        if self.size == 0:
            return None
        self.list[0], self.list[self.size - 1] = self.list[self.size - 1], self.list[0]
        item = self.list.pop()
        self.size -= 1
        self.shift_down(0)
        return item


from heapq import heappush, heappop


class PriorityQueue:
    def __init__(self):
        self._queue = []

    def put(self, item, priority):
        heappush(self._queue, (-priority, item))

    def get(self):
        if len(self._queue) == 0:
            return None
        return heappop(self._queue)[-1]

    def is_empty(self):
        return len(self._queue) == 0


def combine_k_sorted_arr(lists):
    queue = PriorityQueue()
    result = []
    for i in range(len(lists)):
        queue.put(lists[i], -lists[i][0])

    while not queue.is_empty():
        current = queue.get()
        result.append(current.pop(0))
        if len(current) != 0:
            queue.put(current, -current[0])  ###优先级高的先出
    return result


if __name__ == '__main__':
    lists = [
        [1, 3, 4], [2, 5, 6], [7, 8, 9]
    ]
    print(combine_k_sorted_arr(lists))
