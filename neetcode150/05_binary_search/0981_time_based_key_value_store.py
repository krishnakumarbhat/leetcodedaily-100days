"""
=====================================================================
LeetCode 0981 : Time Based Key-Value Store                        (Medium)
https://leetcode.com/problems/time-based-key-value-store/
Category   : Binary Search (over a per-key timestamp vector)
---------------------------------------------------------------------
PROBLEM
    Design a key-value store where every set(key, value, timestamp)
    call is logged, and get(key, timestamp) returns the value whose
    timestamp is the LARGEST one <= the query timestamp (or "" if
    the key has no such record). Timestamps only ever INCREASE per
    key (callers set them in ascending order).

---------------------------------------------------------------------
INTUITION
    Each key owns a chronologically ordered list of (timestamp,value)
    records. get() is then a LOWER-BOUND query on that sorted list:
    "last record with ts <= query" is the predecessor of the first
    record with ts > query. Sorted list → binary search answers each
    get() in O(log n) instead of a linear scan.

---------------------------------------------------------------------
APPROACH 1 — dict[str, list[(ts,val)]] + bisect (BEST)
    Python : dict maps the key to a list of (timestamp, value) pairs
    appended in order. get() uses bisect_right on a parallel list of
    timestamps — returns the INSERTION POINT after any equal entries,
    i.e. the first index with ts > query; the element before it is
    the answer. If the insertion point is 0, every record is too new.
    (C++ equivalent: std::map<string, vector<pair<int,string>>> +
     std::upper_bound — identical semantics.)
    Time  Complexity : set O(1) amortized, get O(log n)
    Space Complexity : O(records) total across all keys

---------------------------------------------------------------------
APPROACH 2 — Linear scan of the per-key list (contrast)
    Same storage, but get() walks the list from the END backward and
    returns the first record with ts <= query. Correct, zero binary
    search machinery — but O(n) per get; a hot key queried a million
    times becomes a billion comparisons.
    Time  Complexity : set O(1), get O(n)
    Space Complexity : O(records)

---------------------------------------------------------------------
DEEP DIVE — bisect_right vs bisect_left (lower_bound vs upper_bound)
    bisect_left(ts)  → first index where list[idx] >= ts  (lower bound).
    bisect_right(ts) → first index where list[idx] >  ts  (upper bound).
    Here we want "last ts <= query": the predecessor of the UPPER
    bound. For an exact hit bisect_left would land ON the record, but
    the query usually falls BETWEEN timestamps, and only
    bisect_right's "strictly greater" boundary points at the first
    record that overshoots. Both run O(log n); the off-by-one is
    purely which boundary you take. Same pattern as C++
    std::lower_bound / std::upper_bound — and how time-series
    databases answer "most recent value at or before time T"
    (versioned configs, event replay, audit trails).
=====================================================================
"""

from __future__ import annotations

import time
import tracemalloc
from bisect import bisect_right
from typing import Dict, List, Tuple

# =====================================================================
# APPROACH 1 : dict of lists + bisect_right (upper bound)
# =====================================================================
class TimeMap_BinarySearch:
    """
    Purpose : Time-based key-value store with O(log n) reads.
    Inputs  : none (constructor).
    Output  : get(key, ts) returns the newest value at or before ts.
    """

    def __init__(self) -> None:
        # key → chronologically ordered (timestamp, value) records.
        self.store: Dict[str, List[Tuple[int, str]]] = {}

    def set(self, key: str, value: str, timestamp: int) -> None:
        """Purpose: store a (timestamp, value) record for a key."""
        # Timestamps arrive ascending → append keeps the list sorted.
        self.store.setdefault(key, []).append((timestamp, value))

    def get(self, key: str, timestamp: int) -> str:
        """Purpose: newest value with record timestamp <= query."""
        vals = self.store.get(key)
        if not vals:
            return ""                        # unknown key → no records.

        # bisect_right on the timestamps = first index with ts > query.
        # (C++ std::upper_bound does exactly this.)
        i = bisect_right([t for t, _ in vals], timestamp)

        if i == 0:
            return ""                        # every record is too new.
        return vals[i - 1][1]                # predecessor of the boundary.

# =====================================================================
# APPROACH 2 : Same storage, linear scan from the newest record
# =====================================================================
class TimeMap_LinearScan:
    """
    Purpose : Time-based key-value store with O(n) reads (contrast).
    Inputs  : none (constructor).
    Output  : get(key, ts) returns the newest value at or before ts.
    """

    def __init__(self) -> None:
        self.store: Dict[str, List[Tuple[int, str]]] = {}

    def set(self, key: str, value: str, timestamp: int) -> None:
        """Purpose: store a (timestamp, value) record for a key."""
        self.store.setdefault(key, []).append((timestamp, value))

    def get(self, key: str, timestamp: int) -> str:
        """Purpose: newest value with record timestamp <= query."""
        vals = self.store.get(key)
        if not vals:
            return ""

        # Scan newest → oldest; first record that qualifies wins.
        for t, v in reversed(vals):
            if t <= timestamp:
                return v
        return ""                            # all records too new.


# =====================================================================
# BENCHMARK — run both approaches, time + peak memory
# =====================================================================
if __name__ == "__main__":
    # --- Approach 1: the official example script ---
    tracemalloc.start()
    t0 = time.perf_counter()
    tm1 = TimeMap_BinarySearch()
    tm1.set("foo", "bar", 1)
    tm1.set("foo", "bar2", 4)
    a1 = tm1.get("foo", 1)                   # "bar"
    a2 = tm1.get("foo", 3)                   # "bar"
    a3 = tm1.get("foo", 5)                   # "bar2"
    t1 = time.perf_counter()
    _, peak1 = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    # --- Approach 2: the same script ---
    tracemalloc.start()
    t0b = time.perf_counter()
    tm2 = TimeMap_LinearScan()
    tm2.set("foo", "bar", 1)
    tm2.set("foo", "bar2", 4)
    b1 = tm2.get("foo", 1)
    b2 = tm2.get("foo", 3)
    b3 = tm2.get("foo", 5)
    t1b = time.perf_counter()
    _, peak2 = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    ok1 = (a1, a2, a3) == ("bar", "bar", "bar2") and (b1, b2, b3) == (a1, a2, a3)
    print(f"A1 BS (bisect_right): get(1)={a1} get(3)={a2} get(5)={a3}  "
          f"time = {(t1-t0)*1e6:.2f} µs  peak-mem = {peak1} B")
    print(f"A2 linear scan      : get(1)={b1} get(3)={b2} get(5)={b3}  "
          f"time = {(t1b-t0b)*1e6:.2f} µs  peak-mem = {peak2} B")
    print("PASS : both approaches return the expected values."
          if ok1 else "FAIL : at least one answer is wrong.")

    # --- Edge cases: queries before the first record and exact hits ---
    tm1.set("love", "high", 10)
    tm1.set("love", "low", 20)
    e1 = tm1.get("love", 5)                  # ""
    e2 = tm1.get("love", 10)                 # "high"
    e3 = tm1.get("love", 15)                 # "high"
    e4 = tm1.get("love", 20)                 # "low"
    ok2 = e1 == "" and e2 == "high" and e3 == "high" and e4 == "low"
    print(f"Edge cases: get(5)='{e1}' get(10)={e2} get(15)={e3} get(20)={e4}"
          f" | {'PASS' if ok2 else 'FAIL'}")