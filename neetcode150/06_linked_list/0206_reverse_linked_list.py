"""
LeetCode 206: Reverse Linked List - Easy
"""
import time, tracemalloc
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val; self.next = next
def build(arr):
    dummy = ListNode(0)
    cur = dummy
    for v in arr: cur.next = ListNode(v); cur = cur.next
    return dummy.next
def to_list(node):
    res = []
    while node: res.append(node.val); node = node.next
    return res

# ============= Variation 1: Iterative =============
# Time: O(n)   Space: O(1)
class Solution_v1:
    def reverseList(self, head):
        prev, cur = None, head
        while cur:
            nxt = cur.next; cur.next = prev; prev = cur; cur = nxt
        return prev

# ============= Variation 2: Recursive =============
# Time: O(n)   Space: O(n)
class Solution_v2:
    def reverseList(self, head):
        if not head or not head.next: return head
        new_head = self.reverseList(head.next)
        head.next.next = head; head.next = None
        return new_head

if __name__ == "__main__":
    data = [1, 2, 3, 4, 5]
    for i, (Sol, name) in enumerate(zip([Solution_v1, Solution_v2], ["Iterative", "Recursive"]), 1):
        tracemalloc.start(); t0 = time.perf_counter()
        result = to_list(Sol().reverseList(build(data)))
        t1 = time.perf_counter(); mem = tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{i} ({name}): result={result}, mem = {mem} bytes, time = {(t1-t0)*1e6:.2f} us")
# var1 mem = {} and time = {}
# var2 mem = {} and time = {}
