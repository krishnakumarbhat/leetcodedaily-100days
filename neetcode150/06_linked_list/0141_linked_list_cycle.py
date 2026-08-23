"""
=====================================================================
LeetCode 141 : Linked List Cycle                                (Easy)
https://leetcode.com/problems/linked-list-cycle/
Category   : Linked List
---------------------------------------------------------------------
PROBLEM
    Given the head of a linked list, determine whether the list has
    a CYCLE (some node's next points back into the list). Walking
    next forever must never reach null for a cyclic list.
---------------------------------------------------------------------
INTUITION
    Two runners on a circular track always meet: a 2×-fast runner
    shrinks the gap by one step per round until collision. In a
    straight corridor they never meet. → slow=1×, fast=2×:
    collision ⇔ cycle. This is FLOYD'S CYCLE DETECTION.
---------------------------------------------------------------------
APPROACH 1 — Floyd's tortoise and hare (BEST)
    slow += 1 hop, fast += 2 hops per round. Same node → cycle.
    fast hits null → acyclic.
    Time  Complexity : O(n)   Space Complexity : O(1)
---------------------------------------------------------------------
APPROACH 2 — Hash set of visited nodes
    Insert every node pointer into a set; first repeat → cycle.
    Time  Complexity : O(n)   Space Complexity : O(n)
---------------------------------------------------------------------
REAL LIFE
    • git fsck detects loops in the object graph with this trick.
    • Deadlock/loop detection in linked allocators, free lists and
      browser DOM traversal guards.
    • 0287 (Find the Duplicate Number) reuses the same math on an
      array interpreted as a linked list.
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


# =====================================================================
# APPROACH 1 : Floyd's tortoise and hare — O(1) space (best)
# =====================================================================
class Solution_Floyd:
    """
    Purpose : Detect a cycle with two pointers moving at 1× and 2×.
    Inputs  : head — first node of the list (may be None).
    Output  : True if the list contains a cycle, False otherwise.
    """

    def hasCycle(self, head: Optional[ListNode]) -> bool:
        slow = head                       # tortoise: 1 hop per round
        fast = head                       # hare: 2 hops per round

        # fast->next guard: the hare must survive two hops.
        while fast is not None and fast.next is not None:
            slow = slow.next              # 1 hop
            fast = fast.next.next         # 2 hops
            if slow is fast:              # lapped inside a loop → cycle
                return True

        return False                      # ran off the end → acyclic


# =====================================================================
# APPROACH 2 : Hash set of visited node addresses
# =====================================================================
class Solution_HashSet:
    """
    Purpose : Detect a cycle by remembering every visited address.
    Inputs  : head — first node of the list (may be None).
    Output  : True if the list contains a cycle, False otherwise.
    """

    def hasCycle(self, head: Optional[ListNode]) -> bool:
        seen: set[ListNode] = set()       # Python set = open addressing

        cur = head
        while cur is not None:
            if cur in seen:               # O(1) probe → second visit
                return True               # some node points back → cycle
            seen.add(cur)
            cur = cur.next
        return False                      # reached None → acyclic


# =====================================================================
# BENCHMARK — 4 tests (incl. cycle cases), time + peak memory
# =====================================================================
if __name__ == "__main__":
    # (values, position the tail loops back to, -1 = no cycle)
    tests: list[tuple[list[int], int]] = [
        ([3, 2, 0, -4], 1),
        ([1, 2], 0),
        ([1], -1),
        ([], -1),
    ]
    expected = [True, True, False, False]

    def make_list(values: list[int], pos: int) -> Optional[ListNode]:
        """Build the list and wire the cycle if pos >= 0."""
        head = build_list(values)
        if pos >= 0 and head is not None:
            entry: Optional[ListNode] = head
            for _ in range(pos):
                entry = entry.next if entry else None
            tail = head
            while tail.next is not None:
                tail = tail.next
            tail.next = entry             # THE CYCLE
        return head

    # --- Approach 1 ---
    tracemalloc.start()
    t0 = time.perf_counter()
    ok1 = all(
        Solution_Floyd().hasCycle(make_list(v, p)) == e
        for (v, p), e in zip(tests, expected)
    )
    t1 = time.perf_counter()
    _, peak1 = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    # --- Approach 2 ---
    tracemalloc.start()
    t0b = time.perf_counter()
    ok2 = all(
        Solution_HashSet().hasCycle(make_list(v, p)) == e
        for (v, p), e in zip(tests, expected)
    )
    t1b = time.perf_counter()
    _, peak2 = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print("0141 Linked List Cycle")
    print(f"Approach 1 (Floyd 2-ptr) : time = {(t1 - t0) * 1e6:.2f} µs  peak-mem = {peak1} bytes")
    print(f"Approach 2 (hash set)    : time = {(t1b - t0b) * 1e6:.2f} µs  peak-mem = {peak2} bytes")
    print("PASS : both approaches detected cycles on all 4 tests."
          if ok1 and ok2 else "FAIL : at least one test returned the wrong verdict.")
