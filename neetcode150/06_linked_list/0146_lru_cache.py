"""
=====================================================================
LeetCode 146 : LRU Cache                                     (Medium)
https://leetcode.com/problems/lru-cache/
Category   : Linked List
---------------------------------------------------------------------
PROBLEM
    Design a cache with capacity C supporting O(1) average:
      get(key) → value, or −1 if absent. Access marks key RECENT.
      put(k,v) → insert/overwrite; if full, EVICT the LEAST
                 RECENTLY USED entry first.
---------------------------------------------------------------------
INTUITION
    A hash map alone gives O(1) get/put but no "which key is least
    recently used?" — that needs an ORDER updatable in O(1). A
    doubly linked list (LRU ⇔ MRU) delivers: moving a node to the
    MRU end is O(1). Map key → list node. Two structures, one job.
---------------------------------------------------------------------
APPROACH 1 — Hash map key → node + doubly linked list (BEST)
    DLL keeps recency order: head = LRU (victim), tail = MRU.
    get: hit → move node to tail. put: exists → update + move to
    tail; new → append at tail; if full → unlink head + erase map.
    Time  Complexity : O(1) average per op   Space : O(C)
---------------------------------------------------------------------
APPROACH 2 — Naive: key → (value, lastUsedTick)
    Every op stamps a global tick. Eviction scans ALL entries for
    the smallest tick — O(C) per eviction.
    Time  Complexity : O(1) get, O(C) put-when-full   Space : O(C)
---------------------------------------------------------------------
REAL LIFE
    • Browser back/forward + tab caches, CDN edge caches, Redis
      allkeys-lru, memcached, the Linux page cache — all are the
      hash-map + doubly-linked-list marriage.
    • LRU = the default cache policy because locality of reference
      is a law of real workloads.
=====================================================================
"""

from __future__ import annotations
import time
import tracemalloc
from typing import Optional


class _DNode:
    """Doubly linked list node: key, value, prev, next."""

    __slots__ = ("key", "value", "prev", "next")

    def __init__(self, key: int = 0, value: int = 0) -> None:
        self.key = key
        self.value = value
        self.prev: Optional[_DNode] = None
        self.next: Optional[_DNode] = None


# =====================================================================
# APPROACH 1 : Hash map + doubly linked list (best)
# =====================================================================
class LRUCache_List:
    """
    Purpose : An LRU cache with O(1) average get/put.
    Inputs  : capacity — maximum entries before eviction.
    Output  : get returns the value or −1; put stores/evicts in place.
    """

    def __init__(self, capacity: int) -> None:
        self.capacity = capacity
        self.map: dict[int, _DNode] = {}    # key → list node (O(1) find)
        self.head: Optional[_DNode] = None  # LRU end — victim lives here
        self.tail: Optional[_DNode] = None  # MRU end — most recent here

    def _move_to_tail(self, node: _DNode) -> None:
        """Refresh recency: unlink node, re-attach at the MRU end."""
        if node is self.tail:
            return                          # already most recent
        # Unlink: bridge prev <-> next around the node.
        if node.prev is not None:
            node.prev.next = node.next
        if node.next is not None:
            node.next.prev = node.prev
        if node is self.head:
            self.head = node.next           # node was the victim end
        # Re-attach at the tail.
        node.prev = self.tail
        node.next = None
        if self.tail is not None:
            self.tail.next = node
        self.tail = node

    def _push_back(self, key: int, value: int) -> None:
        """Append a brand-new node at the MRU end."""
        node = _DNode(key, value)
        self.map[key] = node
        if self.tail is None:
            self.head = self.tail = node    # first node ever
        else:
            node.prev = self.tail
            self.tail.next = node
            self.tail = node

    def _pop_front(self) -> None:
        """Evict the LRU (head) — O(1)."""
        victim = self.head
        if victim is None:
            return
        self.head = victim.next
        if self.head is not None:
            self.head.prev = None
        else:
            self.tail = None
        del self.map[victim.key]            # forget the key too

    def get(self, key: int) -> int:
        """Return the value of key, or −1; a hit refreshes recency."""
        node = self.map.get(key)
        if node is None:
            return -1
        self._move_to_tail(node)            # hit ⇒ now the MOST recent
        return node.value

    def put(self, key: int, value: int) -> None:
        """Insert/overwrite key→value; evict LRU if the cache is full."""
        node = self.map.get(key)
        if node is not None:
            node.value = value              # overwrite in place
            self._move_to_tail(node)
            return
        if len(self.map) == self.capacity:
            self._pop_front()               # full → evict least recent
        self._push_back(key, value)


# =====================================================================
# APPROACH 2 : Naive tick counter + linear eviction scan (contrast)
# =====================================================================
class LRUCache_Naive:
    """
    Purpose : An LRU cache using timestamps and a linear eviction scan.
    Inputs  : capacity — maximum entries before eviction.
    Output  : get returns the value or −1; put stores/evicts in place.
    Note    : get is O(1); put can be O(C) — the contrast to A1.
    """

    def __init__(self, capacity: int) -> None:
        self.capacity = capacity
        self.tick = 0
        self.store: dict[int, tuple[int, int]] = {}   # key → (value, tick)

    def get(self, key: int) -> int:
        """Return the value of key, or −1; a hit refreshes recency."""
        entry = self.store.get(key)
        if entry is None:
            return -1
        self.tick += 1
        self.store[key] = (entry[0], self.tick)       # stamp access time
        return entry[0]

    def put(self, key: int, value: int) -> None:
        """Insert/overwrite key→value; evict LRU if the cache is full."""
        if key in self.store:
            self.tick += 1
            self.store[key] = (value, self.tick)
            return
        if len(self.store) == self.capacity:
            # Eviction needs the OLDEST stamp — scan everything (O(C)).
            victim_key = min(self.store, key=lambda k: self.store[k][1])
            del self.store[victim_key]
        self.tick += 1
        self.store[key] = (value, self.tick)


# =====================================================================
# BENCHMARK — official example, both approaches, time + peak memory
# =====================================================================
if __name__ == "__main__":
    # Official example: cap 2, ops
    # put(1,1) put(2,2) get(1) put(3,3) get(2) put(4,4) get(1) get(3) get(4)
    # → [1, -1, -1, 3, 4]
    expected = [1, -1, -1, 3, 4]

    def run_example(cache) -> bool:
        out: list[int] = []
        cache.put(1, 1)
        cache.put(2, 2)
        out.append(cache.get(1))    # 1  (2 is now least recent)
        cache.put(3, 3)             # evicts 2
        out.append(cache.get(2))    # -1 (gone)
        cache.put(4, 4)             # evicts 1
        out.append(cache.get(1))    # -1 (gone)
        out.append(cache.get(3))    # 3
        out.append(cache.get(4))    # 4
        return out == expected

    # --- Approach 1 ---
    tracemalloc.start()
    t0 = time.perf_counter()
    ok1 = run_example(LRUCache_List(2))
    t1 = time.perf_counter()
    _, peak1 = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    # --- Approach 2 ---
    tracemalloc.start()
    t0b = time.perf_counter()
    ok2 = run_example(LRUCache_Naive(2))
    t1b = time.perf_counter()
    _, peak2 = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print("0146 LRU Cache")
    print(f"Approach 1 (map + DLL)  : time = {(t1 - t0) * 1e6:.2f} µs  peak-mem = {peak1} bytes")
    print(f"Approach 2 (naive tick) : time = {(t1b - t0b) * 1e6:.2f} µs  peak-mem = {peak2} bytes")
    print("PASS : both caches reproduced the official example (1, -1, -1, 3, 4)."
          if ok1 and ok2 else "FAIL : at least one cache deviated from the expected outputs.")
