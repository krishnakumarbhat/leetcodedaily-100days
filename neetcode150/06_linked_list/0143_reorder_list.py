"""
=====================================================================
LeetCode 143 : Reorder List                                   (Medium)
https://leetcode.com/problems/reorder-list/
Category   : Linked List
---------------------------------------------------------------------
PROBLEM
    Reorder  L0→L1→…→Ln−1→Ln  into  L0→Ln→L1→Ln−1→L2→…  in place.
        1→2→3→4  →  1→4→2→3       1→2→3→4→5 → 1→5→2→4→3
---------------------------------------------------------------------
INTUITION
    The target order pulls alternately from front and back. A singly
    linked list cannot walk BACKWARD → split in half, REVERSE the
    second half (0206), then WEAVE the halves together.
---------------------------------------------------------------------
APPROACH 1 — Split + reverse + weave (BEST)
    (a) fast/slow finds the middle; (b) prev/cur flip reverses the
    second half; (c) weave with cached successors.
    Time  Complexity : O(n)   Space Complexity : O(1)
---------------------------------------------------------------------
APPROACH 2 — Vector weave
    Collect all node pointers into an array, weave l from 0, r from
    n−1 inward.
    Time  Complexity : O(n)   Space Complexity : O(n)
---------------------------------------------------------------------
REAL LIFE
    • Playlist shuffling / "interleave" UI features.
    • Any alternation merge: de-interleaving a doubled stream,
      cache-optimized pairing of records.
=====================================================================
"""

from __future__ import annotations
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
# APPROACH 1 : Split at middle (fast/slow) + reverse + weave (best)
# =====================================================================
class Solution_SplitReverseWeave:
    """
    Purpose : Reorder L0→L1→…→Ln into L0→Ln→L1→Ln−1→… in place.
    Inputs  : head — first node of the list to reorder.
    Output  : Returns None; the input list is reordered in place.
    """

    def reorderList(self, head: Optional[ListNode]) -> None:
        if head is None or head.next is None:
            return                        # 0 or 1 node: nothing to do

        # (a) Find the middle: fast hops 2 per slow hop → when fast
        # ends, slow is the center.
        slow = head
        fast = head.next
        while fast is not None and fast.next is not None:
            slow = slow.next
            fast = fast.next.next

        # (b) Reverse the SECOND half (0206 flip: save/flip/slide).
        prev: Optional[ListNode] = None
        cur: Optional[ListNode] = slow.next
        slow.next = None                  # sever the halves!
        while cur is not None:
            nxt = cur.next
            cur.next = prev
            prev = cur
            cur = nxt
        second = prev                     # head of reversed half

        # (c) Weave: one from first half, one from second, alternately.
        first = head
        while second is not None:
            next1 = first.next if first else None   # CACHE survivors
            next2 = second.next
            if first is not None:
                first.next = second       # first → second
            second.next = next1           # second → rest of first
            first = next1
            second = next2


# =====================================================================
# APPROACH 2 : Flatten to a list of nodes, then weave
# =====================================================================
class Solution_VectorWeave:
    """
    Purpose : Reorder the list using an auxiliary array of nodes.
    Inputs  : head — first node of the list to reorder.
    Output  : Returns None; the input list is reordered in place.
    Note    : Simpler logic, but O(n) extra memory.
    """

    def reorderList(self, head: Optional[ListNode]) -> None:
        if head is None or head.next is None:
            return

        nodes: list[ListNode] = []        # contiguous pointer array
        cur = head
        while cur is not None:
            nodes.append(cur)
            cur = cur.next

        l, r = 0, len(nodes) - 1
        while l < r:
            nodes[l].next = nodes[r]      # left node → right node
            l += 1
            if l == r:                    # odd count: middle closes
                nodes[r].next = None
                break
            nodes[r].next = nodes[l]      # right node → next left
            r -= 1
        nodes[r].next = None              # last node closes the chain


# =====================================================================
# BENCHMARK — 3 tests, both approaches, time + peak memory
# =====================================================================
if __name__ == "__main__":
    tests: list[list[int]] = [[1, 2, 3, 4], [1, 2, 3, 4, 5], [1]]
    expected: list[list[int]] = [[1, 4, 2, 3], [1, 5, 2, 4, 3], [1]]

    # --- Approach 1 ---
    tracemalloc.start()
    t0 = time.perf_counter()
    ok1 = True
    for v, e in zip(tests, expected):
        head = build_list(v)
        Solution_SplitReverseWeave().reorderList(head)
        if to_list(head) != e:
            ok1 = False
    t1 = time.perf_counter()
    _, peak1 = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    # --- Approach 2 ---
    tracemalloc.start()
    t0b = time.perf_counter()
    ok2 = True
    for v, e in zip(tests, expected):
        head = build_list(v)
        Solution_VectorWeave().reorderList(head)
        if to_list(head) != e:
            ok2 = False
    t1b = time.perf_counter()
    _, peak2 = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print("0143 Reorder List")
    print(f"Approach 1 (split+reverse+weave) : time = {(t1 - t0) * 1e6:.2f} µs  peak-mem = {peak1} bytes")
    print(f"Approach 2 (vector weave)         : time = {(t1b - t0b) * 1e6:.2f} µs  peak-mem = {peak2} bytes")
    print("PASS : both approaches reordered all 3 tests correctly."
          if ok1 and ok2 else "FAIL : at least one test produced a wrong order.")
