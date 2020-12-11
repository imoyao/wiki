"""


15. 3Sum

Given an array nums of n integers, are there elements a, b, c in nums such that a + b + c = 0? Find all unique triplets in the array which gives the sum of zero.

Note:

The solution set must not contain duplicate triplets.

Example:

Given array nums = [-1, 0, 1, 2, -1, -4],

A solution set is:
[
  [-1, 0, 1],
  [-1, -1, 2]
]


"""


# 思路：先排序，再用两个指针遍历

class Solution(object):
    def threeSum(self, nums):
        solution=[]
        nums.sort()
        for i in range(len(nums)-1):
            left=i+1
            right=len(nums)-1
            while left<right:
                val=nums[i]+nums[left]+nums[right]
                if val==0 and [nums[i],nums[left],nums[right]] not in solution:
                    solution.append([nums[i],nums[left],nums[right]])
                    left+=1
                    right-=1
                elif val<0:
                    left+=1
                else:
                    right-=1
        return solution