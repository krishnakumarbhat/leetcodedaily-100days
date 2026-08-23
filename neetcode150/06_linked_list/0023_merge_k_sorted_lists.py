"""
=====================================================================
LeetCode 23 : Merge K Sorted Lists                             (Hard)
https://leetcode.com/problems/merge-k-sorted-lists/
Category   : Linked List
---------------------------------------------------------------------
PROBLEM
    Merge k sorted linked lists into one sorted list.
        [[1→4→5], [1→3→4], [2→6]]  →  1→1→2→3→4→4→5→6
---------------------------------------------------------------------
INTUITION
    With two lists the winner is min of the two heads (0021). With k
    lists the winner is the smallest of the k heads — a MIN-HEAP
    answers "which head is smallest?" in O(log k).
---------------------------------------------------------------------
APPROACH 1 — Min-heap of k heads (BEST)
    Push all k heads (value, list index). Pop the smallest, append,
    push its successor back. Heap never exceeds k entries.
    Time  Complexity : O(n·log k)   Space Complexity : O(k)
---------------------------------------------------------------------
APPROACH 2 — Sequential two-list merges
    result = lists[0]; fold each later list in with the 0021 merge.
    A node from list i is re-merged i times.
    Time  Complexity : O(n·k)   Space Complexity : O(1)
---------------------------------------------------------------------
REAL LIFE
    • k-way merge powers external sorting, database merge joins
      and log-shard aggregation.
    • Any "best next candidate from many streams" (top-k feeds).
=====================================================================
"""

from __future__ import annotations
import heapq
import time
import tracemalloc
from typing import Optional


class ListNode:
    """Minimal singly linked list node used by every test below."""

    def __init__(self, val: int = 0, next: Optional["ListNode"] = None) -> None:
        self.val = val
        self.next = next


def build_list(values: list[int]) -> Optional[ListNode]:
    """Turn a Python list into a linked list; returns the head."""
    dummy = ListNode()
    tail = dummy
    for v in values:
        tail.next = ListNode(v)
        tail = tail.next
    return dummy.next


def to_list(head: Optional[ListNode]) -> list[int]:
    """Walk a linked list back into a Python list (for verification)."""
    out: list[int] = []
    while head is not None:
        out.append(head.val)
        head = head.next
    return out


# =====================================================================
# APPROACH 1 : Min-heap over the k current heads (best)
# =====================================================================
class Solution_MinHeap:
    """
    Purpose : Merge k sorted lists into one sorted list with a heap.
    Inputs  : lists — list of heads of sorted lists (may be None).
    Output  : Head of the merged sorted list.
    """

    def mergeKLists(self, lists: list[Optional[ListNode]]) -> Optional[ListNode]:
        # Min-heap entries: (value, list index, node).
        # Index breaks ties so nodes with equal values are distinct.
        heap: list[tuple[int, int, ListNode]] = []
        for i, head in enumerate(lists):
            if head is not None:
                heapq.heappush(heap, (head.val, i, head))

        dummy = ListNode()                # result chain sentinel
        tail = dummy

        while heap:
            _, i, node = heapq.heappop(heap)   # smallest head wins
            # That list advances; its new head re-enters the heap.
            nxt = node.next
            if nxt is not None:
                heapq.heappush(heap, (nxt.val, i, nxt))

            tail.next = node              # append winner to result
            tail = tail.next

        return dummy.next


# =====================================================================
# APPROACH 2 : Sequential two-list merges (reuse 0021's merge)
# =====================================================================
class Solution_Sequential:
    """
    Purpose : Merge k sorted lists by folding them in one by one.
    Inputs  : lists — list of heads of sorted lists (may be None).
    Output  : Head of the merged sorted list.
    Note    : O(n·k) worst case — late lists get re-merged k times.
    """

    def mergeKLists(self, lists: list[Optional[ListNode]]) -> Optional[ListNode]:
        result: Optional[ListNode] = None
        for head in lists:
            result = self._merge_two(result, head)   # fold one in
        return result

    def _merge_two(self, a: Optional[ListNode], b: Optional[ListNode]) -> Optional[ListNode]:
        """The 0021 two-list merge (iterative, dummy head)."""
        dummy = ListNode()
        tail = dummy
        while a is not None and b is not None:
            if a.val <= b.val:
                tail.next = a
                a = a.next
            else:
                tail.next = b
                b = b.next
            tail = tail.next
        tail.next = a if a is not None else b
        return dummy.next


# =====================================================================
# BENCHMARK — 3 test sets, both approaches, time + peak memory
# =====================================================================
if __name__ == "__main__":
    test_sets: list[list[list[int]]] = [
        [[1, 4, 5], [1, 3, 4], [2, 6]],
        [[], [1, 3], [2]],
        [[1]],
    ]
    expected: list[list[int]] = [
        [1, 1, 2, 3, 4, 4, 5, 6],
        [1, 2, 3],
        [1],
    ]

    # --- Approach 1 ---
    tracemalloc.start()
    t0 = time.perf_counter()
    ok1 = True
    for vv, e in zip(test_sets, expected):
        lists = [build_list(v) for v in vv]
        merged = Solution_MinHeap().mergeKLists(lists)
        if to_list(merged) != e:
            ok1 = False
    t1 = time.perf_counter()
    _, peak1 = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    # --- Approach 2 ---
    tracemalloc.start()
    t0b = time.perf_counter()
    ok2 = True
    for vv, e in zip(test_sets, expected):
        lists = [build_list(v) for v in vv]
        merged = Solution_Sequential().mergeKLists(lists)
        if to_list(merged) != e:
            ok2 = False
    t1b = time.perf_counter()
    _, peak2 = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print("0023 Merge K Sorted Lists")
    print(f"Approach 1 (min-heap)   : time = {(t1 - t0) * 1e6:.2f} µs  peak-mem = {peak1} bytes")
    print(f"Approach 2 (sequential) : time = {(t1b - t0b) * 1e6:.2f} µs  peak-mem = {peak2} bytes")
    print("PASS : both approaches merged all 3 test sets correctly."
          if ok1 and ok2 else "FAIL : at least one test set produced a wrong list.")
