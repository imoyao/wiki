#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by imoyao at 2019/5/13 18:33

import pathlib
import sys

util_p = pathlib.Path('../..').resolve()

sys.path.append(str(util_p))
from util import utils


def merge_sorted_col(left_col, right_col):
    """
    对两个已排序序列进行归并
    :param left_col:
    :param right_col:
    :return: 归并之后的序列
    """
    sorted_col = list()
    while left_col and right_col:
        '''
        注意此处pop()操作，将两个序列中小的元素直接append到最终列表中。
        >>> a = list(range(5))
        >>> a
        [0, 1, 2, 3, 4]
        >>> a.pop(0)
        0
        >>> a
        [1, 2, 3, 4]
        '''
        sorted_col.append(left_col.pop(0) if left_col[0] <= right_col[0] else right_col.pop(0))
    # 最终将长的列表剩余元素和已排序的列表连接起来
    return sorted_col + left_col + right_col


def merge_sort(unsorted_collection):
    """
    归并排序
    :param unsorted_collection:待排序序列
    :return:排序后序列
    """
    length = len(unsorted_collection)
    if length <= 1:
        return unsorted_collection
    mid_index = length // 2  # 从中间分割
    left_col = unsorted_collection[:mid_index]
    right_col = unsorted_collection[mid_index:]
    # 注意merge_sorted_col内部使用递归对左右两边继续进行排序
    sorted_col = merge_sorted_col(merge_sort(left_col), merge_sort(right_col))  # 调用合并方法，将左右两边排序过的序列合并
    return sorted_col


if __name__ == '__main__':
    unsorted_li = utils.rand_list(100)
    print('Before sorted:', unsorted_li)
    print('After sorted:', merge_sort(unsorted_li))
