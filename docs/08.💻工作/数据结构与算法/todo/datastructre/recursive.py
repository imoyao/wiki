"""


递归
编程实现斐波那契数列求值 f(n)=f(n-1)+f(n-2)
编程实现求阶乘 n!
编程实现一组数据集合的全排列

https://www.cnblogs.com/panlq/p/9307203.html

"""

def fib_recur(n):
  assert n >= 0, "n > 0"
  if n <= 1:
    return n
  return fib_recur(n-1) + fib_recur(n-2)

for i in range(1, 20):
    print(fib_recur(i), end=' ')


def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)


def permutations(arr, position, end):
    if position == end:
        print(arr)

    else:
        for index in range(position, end):
            arr[index], arr[position] = arr[position], arr[index]
            permutations(arr, position + 1, end)
            arr[index], arr[position] = arr[position], arr[index]

#
# arr = ["a", "b", "c"]
# permutations(arr, 0, len(arr))


# https://leetcode-cn.com/problems/climbing-stairs/

###递推法
class Solution:
    def climbStairs(self, n: int) -> int:
        nums = [0,1,2]
        if n == 1:
            return nums[1]
        elif n == 2:
            return nums[2]
        else:
            for i in range(3,n+1):
                nums.append(nums[i-1] + nums[i-2])
        return nums[n]


