#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by imoyao at 2019/5/13 18:33

import pathlib
import sys

util_p = pathlib.Path('../..').resolve()

sys.path.append(str(util_p))
from util import utils


def insertion_sort(unsorted_collection):
    """
    插入排序
    从未排序序列中，拿出一个元素，与已经排序的序列比较，对于有序序列中大于该元素的元素，则后移一位腾出空间，其他不变，直到整个序列循环完成
    :param unsorted_collection:待排序序列
    :return:排序后序列
    """
    length = len(unsorted_collection)
    for index in range(1, length):
        while index > 0 and unsorted_collection[index - 1] > unsorted_collection[index]:  # 前一个元素大于后一个元素
            unsorted_collection[index], unsorted_collection[index - 1] = unsorted_collection[index - 1], \
                                                                         unsorted_collection[index]
            index -= 1  # 只保持前面已经排列的有序，这点和冒泡相反，冒泡每次排序都保证末端有序
    return unsorted_collection


if __name__ == '__main__':
    unsorted_li = utils.rand_list(100)
    print('Before sorted:', unsorted_li)
    print('After sorted:', insertion_sort(unsorted_li))
