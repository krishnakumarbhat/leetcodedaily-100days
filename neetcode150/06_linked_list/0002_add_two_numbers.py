"""
LeetCode 2: Add Two Numbers - Medium
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
# Time: O(max(m,n))   Space: O(max(m,n))
class Solution_v1:
    def addTwoNumbers(self, l1, l2):
        dummy = ListNode(0); cur = dummy; carry = 0
        while l1 or l2 or carry:
            v1 = l1.val if l1 else 0
            v2 = l2.val if l2 else 0
            s = v1 + v2 + carry
            carry = s // 10
            cur.next = ListNode(s % 10); cur = cur.next
            if l1: l1 = l1.next
            if l2: l2 = l2.next
        return dummy.next

if __name__ == "__main__":
    tracemalloc.start(); t0 = time.perf_counter()
    result = to_list(Solution_v1().addTwoNumbers(build([2,4,3]), build([5,6,4])))
    t1 = time.perf_counter(); mem = tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
    print(f"var1: result={result}, mem = {mem} bytes, time = {(t1-t0)*1e6:.2f} us")
# var1 mem = {} and time = {}
