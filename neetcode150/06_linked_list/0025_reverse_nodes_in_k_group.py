"""
LeetCode 25: Reverse Nodes in k-Group - Hard
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
# Time: O(n)   Space: O(1)
class Solution_v1:
    def reverseKGroup(self, head, k):
        dummy = ListNode(0, head); group_prev = dummy
        while True:
            kth = group_prev
            for _ in range(k):
                kth = kth.next
                if not kth: return dummy.next
            group_next = kth.next
            prev, cur = kth.next, group_prev.next
            while cur != group_next:
                nxt = cur.next; cur.next = prev; prev = cur; cur = nxt
            tmp = group_prev.next; group_prev.next = kth; group_prev = tmp
        return dummy.next

if __name__ == "__main__":
    tracemalloc.start(); t0 = time.perf_counter()
    result = to_list(Solution_v1().reverseKGroup(build([1,2,3,4,5]), 2))
    t1 = time.perf_counter(); mem = tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
    print(f"var1: result={result}, mem = {mem} bytes, time = {(t1-t0)*1e6:.2f} us")
# var1 mem = {} and time = {}
