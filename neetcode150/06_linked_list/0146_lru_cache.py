"""
LeetCode 146: LRU Cache - Medium
"""
import time, tracemalloc
from collections import OrderedDict

# ============= Variation 1: OrderedDict =============
# Time: O(1) all ops   Space: O(capacity)
class LRUCache_v1:
    def __init__(self, capacity: int):
        self.cache = OrderedDict(); self.cap = capacity
    def get(self, key: int) -> int:
        if key not in self.cache: return -1
        self.cache.move_to_end(key); return self.cache[key]
    def put(self, key: int, value: int) -> None:
        if key in self.cache: self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.cap: self.cache.popitem(last=False)

# ============= Variation 2: Doubly Linked List + HashMap =============
# Time: O(1) all ops   Space: O(capacity)
class DNode:
    def __init__(self, k=0, v=0): self.key=k; self.val=v; self.prev=None; self.next=None
class LRUCache_v2:
    def __init__(self, capacity: int):
        self.cap = capacity; self.cache = {}
        self.head, self.tail = DNode(), DNode()
        self.head.next = self.tail; self.tail.prev = self.head
    def _remove(self, node):
        node.prev.next = node.next; node.next.prev = node.prev
    def _add(self, node):
        node.prev = self.tail.prev; node.next = self.tail
        self.tail.prev.next = node; self.tail.prev = node
    def get(self, key):
        if key not in self.cache: return -1
        node = self.cache[key]; self._remove(node); self._add(node); return node.val
    def put(self, key, value):
        if key in self.cache: self._remove(self.cache[key])
        node = DNode(key, value); self._add(node); self.cache[key] = node
        if len(self.cache) > self.cap:
            lru = self.head.next; self._remove(lru); del self.cache[lru.key]

if __name__ == "__main__":
    for i, (Cls, name) in enumerate(zip([LRUCache_v1, LRUCache_v2], ["OrderedDict", "DLL+Map"]), 1):
        tracemalloc.start(); t0 = time.perf_counter()
        c = Cls(2); c.put(1,1); c.put(2,2); r1=c.get(1); c.put(3,3); r2=c.get(2); c.put(4,4); r3=c.get(1); r4=c.get(3); r5=c.get(4)
        t1 = time.perf_counter(); mem = tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{i} ({name}): gets={r1},{r2},{r3},{r4},{r5}, mem = {mem} bytes, time = {(t1-t0)*1e6:.2f} us")
# var1 mem = {} and time = {}
# var2 mem = {} and time = {}
