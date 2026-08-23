"""
=====================================================================
LeetCode 2 : Add Two Numbers                                   (Medium)
https://leetcode.com/problems/add-two-numbers/
Category   : Linked List
---------------------------------------------------------------------
PROBLEM
    Two linked lists store non-negative integers in REVERSE order
    (head = least significant digit). Return the sum as a linked
    list in the same format.
        2→4→3 (342) + 5→6→4 (465) = 7→0→8 (807)
---------------------------------------------------------------------
INTUITION
    Heads are the ones digits → grade-school column addition from
    the head:  digit = (a + b + carry) % 10, carry = (a+b+carry)//10.
    A missing node contributes 0; no padding needed.
---------------------------------------------------------------------
APPROACH 1 — Iterative with dummy head + carry (BEST)
    Walk both lists while either lives OR carry is non-zero; append
    digit, keep carry.
    Time  Complexity : O(max(n, m))   Space Complexity : O(1)
---------------------------------------------------------------------
APPROACH 2 — Recursive
    Same column arithmetic on the call stack. Base case: both lists
    empty and carry == 0 → None.
    Time  Complexity : O(max(n, m))   Space Complexity : O(max(n, m))
---------------------------------------------------------------------
REAL LIFE
    • Arbitrary-precision integers (Python int, Java BigInteger)
      add digit-chunks with exactly this carry loop.
    • Linked-digit streams in calculators / payment-splitting math.
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
# APPROACH 1 : Iterative column addition with a dummy head (best)
# =====================================================================
class Solution_Iterative:
    """
    Purpose : Sum two reverse-ordered digit lists into a new list.
    Inputs  : l1, l2 — heads of two digit lists (head = ones digit).
    Output  : Head of the sum list (same reverse digit order).
    """

    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        dummy = ListNode()                # sentinel: no first-append case
        tail = dummy
        carry = 0

        # Loop while digits remain OR the carry is still live:
        # 5 + 5 → digit 0, carry 1 → one extra result node.
        while l1 is not None or l2 is not None or carry != 0:
            total = carry
            if l1 is not None:
                total += l1.val
                l1 = l1.next
            if l2 is not None:
                total += l2.val
                l2 = l2.next

            carry = total // 10           # overflow → next column
            tail.next = ListNode(total % 10)   # one result digit
            tail = tail.next

        return dummy.next


# =====================================================================
# APPROACH 2 : Recursive column addition
# =====================================================================
class Solution_Recursive:
    """
    Purpose : Sum two digit lists recursively.
    Inputs  : l1, l2 — heads of two reverse-ordered digit lists.
    Output  : Head of the sum list.
    Note    : O(max(n, m)) time and stack space.
    """

    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        return self._add(l1, l2, 0)

    def _add(self, a: Optional[ListNode], b: Optional[ListNode], carry: int) -> Optional[ListNode]:
        # Base case: nothing left and no carry → chain ends here.
        if a is None and b is None and carry == 0:
            return None

        total = carry                      # null nodes contribute 0
        if a is not None:
            total += a.val
        if b is not None:
            total += b.val

        # This column's digit leads; recursion builds the rest.
        node = ListNode(total % 10)
        node.next = self._add(a.next if a is not None else None,
                              b.next if b is not None else None,
                              total // 10)
        return node


# =====================================================================
# BENCHMARK — 3 tests, both approaches, time + peak memory
# =====================================================================
if __name__ == "__main__":
    tests_a: list[list[int]] = [[2, 4, 3], [0], [9, 9, 9, 9, 9]]
    tests_b: list[list[int]] = [[5, 6, 4], [0], [1]]
    expected: list[list[int]] = [[7, 0, 8], [0], [0, 0, 0, 0, 0, 1]]

    # --- Approach 1 ---
    tracemalloc.start()
    t0 = time.perf_counter()
    ok1 = all(
        to_list(Solution_Iterative().addTwoNumbers(build_list(a), build_list(b))) == e
        for a, b, e in zip(tests_a, tests_b, expected)
    )
    t1 = time.perf_counter()
    _, peak1 = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    # --- Approach 2 ---
    tracemalloc.start()
    t0b = time.perf_counter()
    ok2 = all(
        to_list(Solution_Recursive().addTwoNumbers(build_list(a), build_list(b))) == e
        for a, b, e in zip(tests_a, tests_b, expected)
    )
    t1b = time.perf_counter()
    _, peak2 = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print("0002 Add Two Numbers")
    print(f"Approach 1 (iterative) : time = {(t1 - t0) * 1e6:.2f} µs  peak-mem = {peak1} bytes")
    print(f"Approach 2 (recursive) : time = {(t1b - t0b) * 1e6:.2f} µs  peak-mem = {peak2} bytes")
    print("PASS : both approaches produced correct sums on all 3 tests."
          if ok1 and ok2 else "FAIL : at least one test produced a wrong sum.")
