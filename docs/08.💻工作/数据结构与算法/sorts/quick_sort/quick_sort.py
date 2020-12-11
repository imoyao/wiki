#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by imoyao at 2019/5/13 18:33

import pathlib
import sys

util_p = pathlib.Path('../..').resolve()

sys.path.append(str(util_p))
from util import utils


def quick_sort(unsorted_collection):
    """
    快速排序
    先找到一个比较基准，然后将列表中剩余元素与这个基准进行比较，如果小于，则放在左边的序列；大于则放在右边；最后把三个序列按顺序连接起来
    :param unsorted_collection:待排序序列
    :return:排序后序列
    """
    if len(unsorted_collection) <= 1:  # 在序列中只有一个元素时，我们不用比较元素大小，本身就是有序序列
        return unsorted_collection
    cmp_base = unsorted_collection[0]  # 取出第一个作为比较基准
    left_col = [item for item in unsorted_collection[1:] if item <= cmp_base]  # 如果希望降序排列，只需分治点两边调换即可
    right_col = [item for item in unsorted_collection[1:] if item > cmp_base]
    '''
    left_col = []
    right_col = []
    for item in unsorted_collection[1:]:
        left_col.append(item) if item <= cmp_base else right_col.append(item)
    '''
    return quick_sort(left_col) + [cmp_base] + quick_sort(right_col)  # 对左右两边的序列使用递归，之后拼接；注意中间的元素要“还原”


@utils.show_time
def compute_time(unsorted_collection):
    return quick_sort(unsorted_collection)


if __name__ == '__main__':
    unsorted_li = utils.rand_list(100)
    print('Before sorted:', unsorted_li)
    print('After sorted:', quick_sort(unsorted_li))
