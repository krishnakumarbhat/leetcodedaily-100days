"""
LeetCode 143: Reorder List - Medium
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

# ============= Variation 1: Array =============
# Time: O(n)   Space: O(n)
class Solution_v1:
    def reorderList(self, head):
        if not head: return
        nodes = []
        cur = head
        while cur: nodes.append(cur); cur = cur.next
        l, r = 0, len(nodes) - 1
        while l < r:
            nodes[l].next = nodes[r]; l += 1
            if l == r: break
            nodes[r].next = nodes[l]; r -= 1
        nodes[l].next = None

# ============= Variation 2: Find Mid + Reverse + Merge =============
# Time: O(n)   Space: O(1)
class Solution_v2:
    def reorderList(self, head):
        if not head or not head.next: return
        slow = fast = head
        while fast.next and fast.next.next: slow = slow.next; fast = fast.next
        prev, cur = None, slow.next; slow.next = None
        while cur: nxt = cur.next; cur.next = prev; prev = cur; cur = nxt
        first, second = head, prev
        while second:
            t1, t2 = first.next, second.next
            first.next = second; second.next = t1
            first, second = t1, t2

if __name__ == "__main__":
    for i, (Sol, name) in enumerate(zip([Solution_v1, Solution_v2], ["Array", "In-Place"]), 1):
        tracemalloc.start(); t0 = time.perf_counter()
        h = build([1,2,3,4,5]); Sol().reorderList(h); result = to_list(h)
        t1 = time.perf_counter(); mem = tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{i} ({name}): result={result}, mem = {mem} bytes, time = {(t1-t0)*1e6:.2f} us")
# var1 mem = {} and time = {}
# var2 mem = {} and time = {}
