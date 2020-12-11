def gen_power_set(L):
    power_set = []
    for i in range(2**len(L)):
        bin_str = get_binary_rep(i, len(L))

        sub_set = []
        for j in range(len(L)):
            if bin_str[j] == '1':
                sub_set.append(L[j])
        power_set.append(sub_set)

    return power_set

# 物品转化为二进制表示

## 我们可以把输入集合当做一个元素的列表，任意一个子集合看成是一个只包含了0,1的字符串，0表示不包含指定元素，1表示包含指定元素，那么全0就表示空集，全1就表示包括所有元素的集合（输入集合）。因此0–2727所有的数的2进制就代表了输入集合的所有子集，也就是找到了问题的全部子空间。
def get_binary_rep(n, num_digital):
    result = ''
    while n > 0:
        result = str(n % 2) + result
        n = n // 2

    if len(result) > num_digital:
        raise ValueError("not enough digits")

    for i in range(num_digital - len(result)):
        result = '0' + result

    return result

if __name__ == '__main__':
   print( gen_power_set(['a','b','c']))