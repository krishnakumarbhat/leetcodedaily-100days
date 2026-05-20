"""
LeetCode 138: Copy List with Random Pointer - Medium
"""
import time, tracemalloc
class Node:
    def __init__(self, x, next=None, random=None):
        self.val = x; self.next = next; self.random = random

# ============= Variation 1: HashMap =============
# Time: O(n)   Space: O(n)
class Solution_v1:
    def copyRandomList(self, head):
        if not head: return None
        old_to_new = {}
        cur = head
        while cur: old_to_new[cur] = Node(cur.val); cur = cur.next
        cur = head
        while cur:
            old_to_new[cur].next = old_to_new.get(cur.next)
            old_to_new[cur].random = old_to_new.get(cur.random)
            cur = cur.next
        return old_to_new[head]

# ============= Variation 2: Interleaving =============
# Time: O(n)   Space: O(1)
class Solution_v2:
    def copyRandomList(self, head):
        if not head: return None
        cur = head
        while cur:
            new_node = Node(cur.val, cur.next); cur.next = new_node; cur = new_node.next
        cur = head
        while cur:
            if cur.random: cur.next.random = cur.random.next
            cur = cur.next.next
        old, new_head = head, head.next
        cur_new = new_head
        while old:
            old.next = old.next.next
            cur_new.next = cur_new.next.next if cur_new.next else None
            old = old.next; cur_new = cur_new.next
        return new_head

if __name__ == "__main__":
    n1 = Node(7); n2 = Node(13); n3 = Node(11)
    n1.next = n2; n2.next = n3; n2.random = n1; n3.random = n1
    for i, (Sol, name) in enumerate(zip([Solution_v1, Solution_v2], ["HashMap", "Interleave"]), 1):
        tracemalloc.start(); t0 = time.perf_counter()
        n1c = Node(7); n2c = Node(13); n3c = Node(11)
        n1c.next = n2c; n2c.next = n3c; n2c.random = n1c; n3c.random = n1c
        result = Sol().copyRandomList(n1c)
        t1 = time.perf_counter(); mem = tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{i} ({name}): mem = {mem} bytes, time = {(t1-t0)*1e6:.2f} us")
# var1 mem = {} and time = {}
# var2 mem = {} and time = {}
