"""
LeetCode 19: Remove Nth Node From End of List - Medium
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

# ============= Variation 1: Two Pass =============
# Time: O(n)   Space: O(1)
class Solution_v1:
    def removeNthFromEnd(self, head, n):
        length = 0; cur = head
        while cur: length += 1; cur = cur.next
        if length == n: return head.next
        cur = head
        for _ in range(length - n - 1): cur = cur.next
        cur.next = cur.next.next
        return head

# ============= Variation 2: One Pass (Two Pointers) =============
# Time: O(n)   Space: O(1)
class Solution_v2:
    def removeNthFromEnd(self, head, n):
        dummy = ListNode(0, head); fast = slow = dummy
        for _ in range(n + 1): fast = fast.next
        while fast: fast = fast.next; slow = slow.next
        slow.next = slow.next.next
        return dummy.next

if __name__ == "__main__":
    for i, (Sol, name) in enumerate(zip([Solution_v1, Solution_v2], ["Two Pass", "One Pass"]), 1):
        tracemalloc.start(); t0 = time.perf_counter()
        result = to_list(Sol().removeNthFromEnd(build([1,2,3,4,5]), 2))
        t1 = time.perf_counter(); mem = tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{i} ({name}): result={result}, mem = {mem} bytes, time = {(t1-t0)*1e6:.2f} us")
# var1 mem = {} and time = {}
# var2 mem = {} and time = {}
