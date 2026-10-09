"""_why.py --- derive a one-line complexity justification when none was authored."""
import re
RULES = [
    ("brute", "nested enumeration dominates: O(n^k) pairs, no pruning"),
    ("brute force", "nested enumeration dominates: O(n^k) pairs, no pruning"),
    ("hash", "one O(1) hash probe per element, no rescans"),
    ("set", "each element is probed once; pairs cancel or are recorded"),
    ("counter", "one O(1) counter update per element"),
    ("counter", "one O(1) counter update per element"),
    ("sort", "the sort dominates; the post-sort scan is linear"),
    ("stack", "each element is pushed once and popped at most once"),
    ("monotonic", "each index enters and leaves the stack once: amortised O(1)"),
    ("deque", "each index is pushed once and popped at most once"),
    ("heap", "one push (and at most one pop) per element"),
    ("binary search", "the interval halves each iteration: O(log n) probes"),
    ("lower bound", "the interval halves each iteration: O(log n) probes"),
    ("bisect", "the interval halves each iteration: O(log n) probes"),
    ("dfs", "every node is visited once and returns O(1) state"),
    ("bfs", "every node is enqueued and dequeued once"),
    ("top-down", "each (i, j) state is solved once and cached"),
    ("memo", "each state is solved once; the rest are cached lookups"),
    ("tabulation", "each state is computed once from already-known states"),
    ("bottom-up", "each state is computed once from already-known states"),
    ("rolling", "each row is read once and discarded: two arrays at most"),
    ("in-place", "the output array doubles as the state store"),
    ("greedy", "one pass; the greedy argument bounds the choice"),
    ("math formula", "constant time after one counting pass"),
    ("union-find", "O(alpha(n)) amortised per union with path compression"),
    ("union", "O(alpha(n)) amortised per union with path compression"),
    ("kahn", "each node enters the queue once; each edge decremented once"),
    ("dijkstra", "each edge relaxes once; heap ops are O(log V)"),
    ("bellman", "k+1 full passes over the edge list"),
    ("twist", "one pass per direction"),
    ("sweep", "each interval enters and leaves the frontier once"),
    ("prefix", "two linear passes; the suffix is carried in a scalar"),
    ("suffix", "two linear passes; the prefix is carried in a scalar"),
    ("xor", "one accumulator pass, O(1) space"),
    ("bit", "constant passes over the bits of the value"),
    ("shift", "one shift-and-mask per bit position"),
    ("kadane", "one pass, two running scalars"),
    ("divide", "the recursion splits the work; the bound is the sum over levels"),
    ("multi-source", "each cell is flooded once per source layer"),
    ("bidirectional", "each word is expanded from at most two frontiers"),
]


def why_for(name: str, time: str, space: str) -> str:
    """Purpose: a defensible one-line justification for the stated bounds."""
    low = name.lower()
    for needle, reason in RULES:
        if needle in low:
            return f"{reason}; hence the stated bounds."
    return f"Follows directly from the traversal count: {time} time, {space} space."


CAT_NOTES = {
 "Arrays & Hashing": "Both languages do the same number of hash probes, so the difference is constant factor and memory layout. C++ `std::unordered_map` allocates a node per entry plus a bucket array, so every probe is a pointer chase into a scattered allocation; Python's `dict` is one flat open-addressed array of PyObject* slots, which is denser but requires boxing every small int on the way in. CPython caches ints -5..256, so small-int keys allocate nothing, but larger keys allocate a PyLong per distinct key. The arrays themselves behave identically in both: contiguous ints, unit stride, perfect prefetch.",
 "Two Pointers": "Two-pointer loops are branch-dominated in both languages. The C++ compiler can often turn the pointer update into a conditional move, eliminating the hard-to-predict branch entirely; CPython cannot, so every comparison dispatches through the bytecode loop. Both read the array sequentially or inward from two ends, which the prefetcher handles well, so the difference is interpreter overhead rather than memory behaviour.",
 "Sliding Window": "Sliding windows stream the input once, so both languages get perfect cache behaviour on the array itself. The work per element is a handful of array or dict operations, and that is where they diverge: C++ does them in registers against a fixed-size counter array that never leaves L1, while CPython performs list indexing with per-element int arithmetic and allocates a fresh int for every accumulated sum or comparison result.",
 "Stack": "Stack pushes and pops are register-cheap in C++ when the stack is a preallocated vector with an index, and the comparisons against the top element are L1 hits. CPython's `list` and `collections.deque` are efficient block structures with amortised O(1) ends, so the structural cost is comparable; the difference is the interpreted dispatch around each of those operations.",
 "Binary Search": "At 20 to 30 iterations per call, both languages finish in microseconds and the asymptotic bound is identical, so this category is about correctness rather than speed. C++ must use `lo + (hi - lo) / 2` to avoid overflow and must guard sentinel sentinels explicitly; CPython has arbitrary precision and unbounded indices, so the same expressions are safe without ceremony.",
 "Linked List": "Linked lists are the worst case for both languages because every node access is a dependent pointer chase that the CPU cannot prefetch. C++ makes that one cache miss per node; CPython makes it a cache miss plus a PyObject header read plus a type check. The larger constant is why C++ linked-list code is genuinely faster here rather than merely tidier -- and why an array-based representation can beat both.",
 "Trees": "Recursion dominates. Each C++ call is a fixed-size stack frame pushed by a single instruction, so a 1e4-deep tree is a few hundred KB of stack. CPython frames are heap objects costing roughly 500 bytes plus the interpreter state per call, so deep trees risk the recursion limit and cost far more memory. An explicit stack in both languages removes the difference.",
 "Tries": "Trie nodes are pointer-heavy in C++ (children vectors or maps with per-node allocations) and object-heavy in Python (one dict per node, at ~64 bytes empty). Python's `defaultdict(dict)` per node is surprisingly compact but every lookup is a Python-level dict access; C++ with a fixed 26-array gives one cache line per node but wastes 104 bytes per node on sparse tries.",
 "Heap / Priority Queue": "Heap operations are sift loops with $O(\log k)$ dependent loads. C++ `std::priority_queue` over a `std::vector` keeps the array contiguous, so the sift path touches predictable cache lines. CPython's `heapq` is implemented in C and also operates on a contiguous list, so the structural performance is nearly identical -- the difference is the surrounding Python loop and any per-element tuple allocation the element type requires.",
 "Backtracking": "Backtracking is dominated by the cost of copying the current path at each node. Python's `path + ch` allocates and copies at every node, giving $O(n \cdot \text{output})$ where $O(\text{output})$ suffices; mutating one list with append and pop fixes that. C++ has exactly the same trap with `std::string`, and the same fix with `push_back` and `pop_back`.",
 "Graphs": "Graph traversal is memory-latency bound: each neighbour fetch is a pointer chase into an adjacency structure. C++ `vector<vector<int>>` gives per-node contiguous vectors, so a node's neighbours are one cache line. CPython's `list` of lists is comparable in structure but each inner list is a separate object, and the loop around the deque adds dispatch cost. Union-Find shifts the trade-off entirely toward $O(1)$ space with no adjacency structure at all.",
 "Advanced Graphs": "Shortest-path work is dominated by heap operations and by the priority-queue entry size. C++ stores `pair<int,int>` values inline, so a heap entry is 8 bytes and the sift path is tight. Python must heapify tuples, so each entry is a 56-byte object plus two pointers, and comparisons go through tuple `__lt__`. That 7x memory difference is the dominant factor when a relaxation fires many times.",
 "1-D Dynamic Programming": "DP tables are contiguous arrays, so memory behaviour is the same in both languages. The divergence is the inner loop: C++ reads two integers, adds, and compares -- a few instructions that the compiler vectorises or at least pipelines; CPython performs list indexing, int addition, and a comparison, allocating a new int for each intermediate sum. At 1e5 to 1e6 cells that difference is one to two orders of magnitude.",
 "2-D Dynamic Programming": "A 2-D table in C++ can be a single contiguous allocation indexed by `r * n + c`, giving perfect locality on the row-major traversal order that DP naturally uses. Python's `list` of lists costs one object per row plus indirection per access. Rolling-row reduction removes the difference almost entirely, since a single row fits in L1 in both languages.",
 "Greedy": "Greedy algorithms are one linear pass with a comparison and an update, so they are the cheapest category to execute and the most expensive to get right. C++ emits the update as a cmov, removing the branch; CPython performs the same comparison in bytecode. Because the pass is so cheap, the interview weight is entirely on the correctness argument rather than the implementation.",
 "Intervals": "Interval algorithms are sort-dominated, so the languages differ in how they sort. C++ `std::sort` on `pair<int,int>` compares two registers, giving $O(n \log n)$ comparisons with no allocation. CPython's `list.sort()` is Timsort, which is faster on nearly-sorted data but compares tuples through a generic rich-comparison slot -- an indirect call per comparison. Both then sweep linearly.",
 "Math & Geometry": "These problems are arithmetic on small integers, so both languages are fast. The C++ concern is overflow -- intermediate products in multiply-strings, reverse-integer, and pow can exceed 32 bits -- while Python's arbitrary precision removes that class of bug entirely. Matrix rotations differ more meaningfully: both work in place on the same memory, but C++ gets in-register swaps where Python writes through list indirection.",
 "Bit Manipulation": "Bit operations map almost directly onto single machine instructions in C++, so this category shows the largest per-operation gap. Python's integers are arbitrary-precision objects, so `&`, `|`, `^` and `>>` allocate a new object per operation unless CPython's small-int cache applies -- and Python's `~x` yields a negative number because integers are infinite two's complement. For pure bit work C++ is the natural home.",
}


def cpp_vs_py_default(h: dict, m: dict) -> str:
    """Purpose: language-mechanics paragraph when neither authored nor harvested."""
    cat = m.get("category", "")
    return CAT_NOTES.get(cat, "C++ stores the working set in contiguous, unboxed memory while CPython boxes every "
                              "intermediate, so the same algorithm differs by a large constant factor while sharing "
                              "an identical asymptotic bound.")


def main() -> None:
    import json
    from pathlib import Path
    here = Path(__file__).resolve().parent
    total = 0
    for f in sorted((here / "content").glob("[0-9]*.json")):
        data = json.loads(f.read_text())
        for p in data["problems"]:
            for a in p["approaches"]:
                if not a.get("why"):
                    a["why"] = why_for(a.get("name", ""), a.get("time", "?"), a.get("space", "?"))
                    total += 1
        f.write_text(json.dumps(data, indent=1))
    print(f"filled {total} complexity justifications")


if __name__ == "__main__":
    main()
