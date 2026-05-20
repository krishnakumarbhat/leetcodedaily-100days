"""LeetCode 53: Maximum Subarray - Medium"""
import time, tracemalloc
from typing import List
# Variation 1: Kadane's O(n)
class Solution_v1:
    def maxSubArray(self, nums: List[int]) -> int:
        cur=mx=nums[0]
        for n in nums[1:]: cur=max(n,cur+n); mx=max(mx,cur)
        return mx
# Variation 2: Divide and conquer O(n log n)
class Solution_v2:
    def maxSubArray(self, nums: List[int]) -> int:
        def dc(l,r):
            if l==r: return nums[l]
            m=(l+r)//2
            left_max=right_max=0; cur=0
            for i in range(m,l-1,-1): cur+=nums[i]; left_max=max(left_max,cur)
            cur=0
            for i in range(m+1,r+1): cur+=nums[i]; right_max=max(right_max,cur)
            return max(dc(l,m),dc(m+1,r),left_max+right_max)
        return dc(0,len(nums)-1)
if __name__ == "__main__":
    nums=[-2,1,-3,4,-1,2,1,-5,4]
    for Vi,Cls in enumerate([Solution_v1,Solution_v2],1):
        tracemalloc.start(); t0=time.perf_counter()
        r=Cls().maxSubArray(nums[:])
        t1=time.perf_counter(); mem=tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{Vi}: max={r}, mem={mem}bytes, time={(t1-t0)*1e6:.2f}us")
# var1 mem = {} and time = {}
# var2 mem = {} and time = {}
