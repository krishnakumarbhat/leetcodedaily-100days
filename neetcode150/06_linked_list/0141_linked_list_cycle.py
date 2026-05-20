"""
LeetCode 141: Linked List Cycle - Easy
"""
import time, tracemalloc
class ListNode:
    def __init__(self, val=0, next=None): self.val = val; self.next = next

# ============= Variation 1: HashSet =============
# Time: O(n)   Space: O(n)
class Solution_v1:
    def hasCycle(self, head):
        seen = set()
        while head:
            if id(head) in seen: return True
            seen.add(id(head)); head = head.next
        return False

# ============= Variation 2: Fast & Slow Pointers =============
# Time: O(n)   Space: O(1)
class Solution_v2:
    def hasCycle(self, head):
        slow = fast = head
        while fast and fast.next:
            slow = slow.next; fast = fast.next.next
            if slow == fast: return True
        return False

if __name__ == "__main__":
    n1 = ListNode(3); n2 = ListNode(2); n3 = ListNode(0); n4 = ListNode(-4)
    n1.next = n2; n2.next = n3; n3.next = n4; n4.next = n2
    for i, (Sol, name) in enumerate(zip([Solution_v1, Solution_v2], ["HashSet", "Floyd"]), 1):
        tracemalloc.start(); t0 = time.perf_counter()
        result = Sol().hasCycle(n1)
        t1 = time.perf_counter(); mem = tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{i} ({name}): result={result}, mem = {mem} bytes, time = {(t1-t0)*1e6:.2f} us")
# var1 mem = {} and time = {}
# var2 mem = {} and time = {}
