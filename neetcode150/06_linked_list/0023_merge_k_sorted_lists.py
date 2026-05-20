"""
LeetCode 23: Merge k Sorted Lists - Hard
"""
import time, tracemalloc, heapq
from typing import List
class ListNode:
    def __init__(self, val=0, next=None): self.val = val; self.next = next
def build(arr):
    dummy = ListNode(0); cur = dummy
    for v in arr: cur.next = ListNode(v); cur = cur.next
    return dummy.next
def to_list(node):
    res = []
    while node: res.append(node.val); node = node.next
    return res

# ============= Variation 1: Merge All + Sort =============
# Time: O(N log N)   Space: O(N)
class Solution_v1:
    def mergeKLists(self, lists):
        vals = []
        for l in lists:
            while l: vals.append(l.val); l = l.next
        dummy = ListNode(0); cur = dummy
        for v in sorted(vals): cur.next = ListNode(v); cur = cur.next
        return dummy.next

# ============= Variation 2: Min Heap =============
# Time: O(N log k)   Space: O(k)
class Solution_v2:
    def mergeKLists(self, lists):
        heap = []; dummy = ListNode(0); cur = dummy
        for i, l in enumerate(lists):
            if l: heapq.heappush(heap, (l.val, i, l))
        while heap:
            val, i, node = heapq.heappop(heap)
            cur.next = node; cur = cur.next
            if node.next: heapq.heappush(heap, (node.next.val, i, node.next))
        return dummy.next

# ============= Variation 3: Divide and Conquer =============
# Time: O(N log k)   Space: O(log k)
class Solution_v3:
    def mergeKLists(self, lists):
        if not lists: return None
        def merge2(l1, l2):
            d = ListNode(0); c = d
            while l1 and l2:
                if l1.val <= l2.val: c.next = l1; l1 = l1.next
                else: c.next = l2; l2 = l2.next
                c = c.next
            c.next = l1 or l2; return d.next
        while len(lists) > 1:
            merged = []
            for i in range(0, len(lists), 2):
                l1 = lists[i]; l2 = lists[i+1] if i+1 < len(lists) else None
                merged.append(merge2(l1, l2))
            lists = merged
        return lists[0]

if __name__ == "__main__":
    for i, (Sol, name) in enumerate(zip([Solution_v1, Solution_v2, Solution_v3], ["Sort", "Heap", "D&C"]), 1):
        tracemalloc.start(); t0 = time.perf_counter()
        lists = [build([1,4,5]), build([1,3,4]), build([2,6])]
        result = to_list(Sol().mergeKLists(lists))
        t1 = time.perf_counter(); mem = tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{i} ({name}): result={result}, mem = {mem} bytes, time = {(t1-t0)*1e6:.2f} us")
# var1 mem = {} and time = {}
# var2 mem = {} and time = {}
# var3 mem = {} and time = {}
