"""
=====================================================================
LeetCode 136 : Single Number                                       (Easy)
https://leetcode.com/problems/single-number/
Category   : Bit Manipulation
---------------------------------------------------------------------
PROBLEM
    Given a non-empty array of integers where EVERY element appears
    EXACTLY TWICE except ONE which appears exactly ONCE, find the
    single one. Must run in O(n) time and O(1) extra space.
    Example: [4,1,2,1,2] → 4.
---------------------------------------------------------------------
INTUITION
    XOR is its own inverse: applying it twice returns the original
    value. "Xor everything together" annihilates every pair and
    leaves exactly the unpaired element — no counting, no memory.
    The bitwise view is clearest: a pair of 1-bits at the same
    position cancels to 0, so only the singleton's bits survive.
---------------------------------------------------------------------
APPROACH 1 — XOR everything (BEST)
    acc = 0; for num in nums: acc ^= num. Pairs vanish (x ^ x = 0,
    x ^ 0 = x); order is irrelevant (commutative + associative).
    Time  Complexity : O(n)   Space Complexity : O(1)
    WHY it works — the cancellation law, derived from the truth table:
        0^0=0  0^1=1  1^0=1  1^1=0   →  x ^ 0 = x  and  x ^ x = 0
        Group the array: (v1^v1) ^ (v2^v2) ^ ... ^ s = 0 ^ ... ^ s = s
---------------------------------------------------------------------
APPROACH 2 — Hash set toggle (O(n) space baseline)
    Add on first sight, remove on second. The only key left when the
    array ends is the singleton. Correct but fails the O(1)-space
    requirement — shown as the baseline XOR defeats.
    Time  Complexity : O(n)   Space Complexity : O(n)
---------------------------------------------------------------------
REAL LIFE
    • Parity/checksums: every 2-disk RAID array stores parity as the
      XOR of the data disks — the parity block can REBUILD a failed
      disk because XOR undoes itself (x ^ x = 0 kills the survivor).
    • Checksum fields in network packets: xor-ing the whole packet
      yields zero when the packet is intact (the 'accumulator' above).
=====================================================================
"""

from __future__ import annotations
import time
import tracemalloc
from typing import List


# =====================================================================
# APPROACH 1 : XOR everything — pairs cancel, singleton survives (best)
# =====================================================================
class Solution_1:
    """
    Purpose : Find the element that appears exactly once, given every
              other element appears exactly twice.
    Inputs  : nums — the array to scan (must satisfy the guarantee).
    Output  : int — the single non-paired element.
    """

    def singleNumber(self, nums: List[int]) -> int:
        # Accumulator: 0 is the XOR identity, so the first element
        # passes through unchanged (x ^ 0 == x).
        acc = 0

        # One pass. XOR is commutative and associative, so visit order
        # is irrelevant: every pair cancels itself wherever it lives.
        for num in nums:
            acc ^= num
        return acc


# =====================================================================
# APPROACH 2 : Hash set toggle — add once, remove on the second sight
# =====================================================================
class Solution_2:
    """
    Purpose : Find the unique element via add/remove toggling in a
              hash set — the O(n)-space baseline XOR beats.
    Inputs  : nums — the array to scan (satisfies the guarantee).
    Output  : int — the single non-paired element.
    """

    def singleNumber(self, nums: List[int]) -> int:
        # seen : values currently holding an ODD number of visits.
        seen: set[int] = set()

        # Toggle membership: first sight inserts, second sight erases.
        # After the loop, the only remaining key is the singleton —
        # every other value was toggled out by its own second copy.
        for num in nums:
            if num in seen:
                seen.remove(num)   # second occurrence → pair complete
            else:
                seen.add(num)      # first occurrence → remember it

        # Exactly one key survives the toggling.
        return next(iter(seen))


# =====================================================================
# BENCHMARK — run both approaches and compare time + peak memory
# =====================================================================
if __name__ == "__main__":
    # Test table: {array, expected singleton}.
    tests: List[tuple] = [
        ([2, 2, 1], 1),
        ([4, 1, 2, 1, 2], 4),
        ([1], 1),
        ([-2**31, 7, 7, -2**31, 42], 42),
    ]

    # --- Approach 1: time + peak memory (tracemalloc snapshot) ---
    tracemalloc.start()
    t0 = time.perf_counter()
    ok_1 = True
    for arr, exp in tests:
        got = Solution_1().singleNumber(arr)
        pass_ = got == exp
        ok_1 = ok_1 and pass_
        print(f"  A1 singleNumber({len(arr)} elems) = {got}  expected {exp}  {'PASS' if pass_ else 'FAIL'}")
    t1 = time.perf_counter()
    _, peak_1 = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    # --- Approach 2: time + peak memory ---
    tracemalloc.start()
    t0b = time.perf_counter()
    ok_2 = True
    for arr, exp in tests:
        got = Solution_2().singleNumber(arr)
        pass_ = got == exp
        ok_2 = ok_2 and pass_
        print(f"  A2 singleNumber({len(arr)} elems) = {got}  expected {exp}  {'PASS' if pass_ else 'FAIL'}")
    t1b = time.perf_counter()
    _, peak_2 = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    # Summary lines: time in µs, peak memory in KB.
    print(f"Approach 1 (XOR, O(1) space) : time = {(t1 - t0) * 1e6:.2f} µs  peak-mem = {peak_1 / 1024:.2f} KB")
    print(f"Approach 2 (hash set toggle) : time = {(t1b - t0b) * 1e6:.2f} µs  peak-mem = {peak_2 / 1024:.2f} KB")

    print("PASS : both approaches find the singleton in every test."
          if ok_1 and ok_2
          else "FAIL : at least one test mismatched.")
