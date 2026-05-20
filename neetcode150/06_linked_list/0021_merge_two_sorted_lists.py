"""
LeetCode 21: Merge Two Sorted Lists - Easy
"""
import time, tracemalloc
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

# ============= Variation 1: Iterative =============
# Time: O(n+m)   Space: O(1)
class Solution_v1:
    def mergeTwoLists(self, l1, l2):
        dummy = ListNode(0); cur = dummy
        while l1 and l2:
            if l1.val <= l2.val: cur.next = l1; l1 = l1.next
            else: cur.next = l2; l2 = l2.next
            cur = cur.next
        cur.next = l1 or l2
        return dummy.next

# ============= Variation 2: Recursive =============
# Time: O(n+m)   Space: O(n+m)
class Solution_v2:
    def mergeTwoLists(self, l1, l2):
        if not l1: return l2
        if not l2: return l1
        if l1.val <= l2.val: l1.next = self.mergeTwoLists(l1.next, l2); return l1
        else: l2.next = self.mergeTwoLists(l1, l2.next); return l2

if __name__ == "__main__":
    for i, (Sol, name) in enumerate(zip([Solution_v1, Solution_v2], ["Iterative", "Recursive"]), 1):
        tracemalloc.start(); t0 = time.perf_counter()
        result = to_list(Sol().mergeTwoLists(build([1,2,4]), build([1,3,4])))
        t1 = time.perf_counter(); mem = tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{i} ({name}): result={result}, mem = {mem} bytes, time = {(t1-t0)*1e6:.2f} us")
# var1 mem = {} and time = {}
# var2 mem = {} and time = {}
