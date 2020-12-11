"""


循环比较两个有序数组头位元素的大小，并把头元素放到新数组中，从老数组中删掉，直到其中一个数组长度为0。
然后再把不为空的老数组中剩下的部分加到新数组的结尾

"""


def merge_sort(a, b):
    result = []
    while len(a)>0 and len(b)>0:

        if a[0] <= b[0]:
            result.append(a[0])
            a.remove(a[0])
        else:                        #  第一次在这里判断了a【0】和b【0】导致indexOutOf报错
            result.append(b[0])
            b.remove(b[0])
    if len(a) == 0:
        result += b
    if len(b) == 0:
        result += a
    return result


if __name__ == '__main__':
    a = [1,3,5]
    b = [2,5,6]
    print(merge_sort(a, b))