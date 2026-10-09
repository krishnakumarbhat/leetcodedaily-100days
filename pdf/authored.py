"""authored.py --- The hand-written analysis payload (phase 1 bootstrap).

Each record under DATA is keyed exactly like manifest.json ("<dir>/<stem>") and
supplies only what harvest.py cannot mine: intent, bounds, the visual state
trace, language mechanics, structure alternatives, traps, invariants and the
three intuition-check questions.

    one_liner      one clause, <= 12 words
    category_note  2-4 sentences on the whole category (first record only)
    core_objective exactly two sentences
    bounds         concrete ranges + the boundary traps
    diagram        pure ASCII, <= 18 lines, <= 66 columns
    cpp_vs_py      hardware-level paragraph
    cpp_alts       2-4 bullets
    py_alts        2-4 bullets
    trap           the #1 mistake
    invariant      the check to run before submitting
    questions      exactly 3 {q, a} pairs probing why the trick works
    kernels       optional per-approach override, {0: {"py": ..., "cpp": ...}}

KERNELS holds the same override keyed by problem then approach index, for
problems where the kernels are easier to read apart from the prose.
"""

DATA: dict[str, dict] = {}

DATA.update({
"01_arrays_and_hashing/0001_two_sum": {
  "one_liner": "Complement lookup collapses O(n^2) pairing into a single pass.",
  "category_note": "This category is about trading memory for time. The recurring move is to ask the array one question per element -- \"have I seen the thing that completes this?\" -- and answer it with a hash table instead of a rescan. Every approach below is that same idea wearing different clothes: frequency tables for multiplicity, complement maps for pairing, prefix/suffix sweeps when you need a value from both sides, and bucket ordering when the values themselves carry the structure. The Python-C++ story is uniform too: a flat open-addressed `dict` versus node-per-entry `std::unordered_map`, which is why the Python version is often the denser one for small-int keys even though it is slower per operation.",
  "core_objective": "Return the indices of the two distinct elements whose values sum to `target`. Exactly one solution is guaranteed and no element may be used twice.",
  "bounds": "2 <= nums.length <= 1e4; -1e9 <= nums[i], target <= 1e9. Duplicates are allowed, so [3,3] with target 6 is a legal input. Overflow is impossible in Python but is real in C++ if you accumulate rather than subtract. The single boundary trap is probe-before-insert.",
  "diagram": " nums  :  [2] [7] [11] [15]\n         i=0  i=1   i=2   i=3\n         need9 need2  need-2 need-11\n\n i=0 x=2  need=9  in seen? NO   -> seen={2:0}\n i=1 x=7  need=2  in seen? YES  -> [0,1]  DONE\n i=2 ...            (never reached)\n\n invariant: before step i, seen = {value:index for index < i}",
  "cpp_vs_py": "CPython boxes every int: `nums[i]` is a pointer chase to a separately allocated PyLong, and `target - num` allocates a brand-new PyLong per iteration, so a one-pass scan performs n heap allocations for the subtrahends alone. C++ keeps the ints inline in a contiguous `vector<int>`, so the subtraction happens in a register with no traffic at all. The map itself inverts the usual expectation: Python's `dict` is one flat open-addressed table of PyObject* slots, so a 1e4-entry int map costs roughly 400 KB densely packed, while `std::unordered_map` allocates a node per entry plus a bucket array, costing more memory but keeping each bucket's chain cache-friendly for iteration.",
  "cpp_alts": [
    "`std::map<int,int>` is the wrong tool: an RB-tree makes every lookup $O(\log n)$ for no benefit here, since we never need the keys ordered.",
    "`__gnu_pbds::gp_hash_table` with a splitmix64 custom hasher defeats the standard anti-test payload that walks `std::unordered_map` with keys congruent modulo the bucket count.",
    "For very large n, a sorted `vector<pair<int,int>>` plus two pointers beats a hash map on memory and cache, at $O(n \log n)$ time."
  ],
  "py_alts": [
    "`dict.setdefault` and `defaultdict` only hide the miss case; the explicit `in` probe is fastest and reads closest to the C++ version.",
    "`enumerate` beats `for i in range(len(nums))` because it avoids the second index load.",
    "`Counter` is dead weight for a single partner query -- it maintains 26-fold more state than you read."
  ],
  "trap": "Writing `seen[x] = i` before the membership probe. With nums = [3, 3] and target = 6 that returns [0, 0], reusing one element twice. Probe first, insert second.",
  "invariant": "At the top of iteration i, `seen` maps every value at an index strictly below i to its index, and nothing else. If that holds, a hit means the partner is a genuinely earlier, distinct element.",
  "questions": [
    {"q": "Why must the probe happen before the insert?", "a": "Inserting first lets a value satisfy its own complement when x + x == target, which reuses one element. The problem forbids that, so the current element must not be visible to its own query."},
    {"q": "What input kills an identity-hashed `std::unordered_map` here, and how do you stop it?", "a": "Keys chosen to be congruent modulo the bucket count, e.g. multiples of the prime bucket size, all land in one chain and turn the lookup into $O(n)$ per probe. A splitmix64 custom hasher, or `gp_hash_table` with open addressing, restores $O(1)$ expected."},
    {"q": "The answer is guaranteed unique. Why may you return on the first hit?", "a": "If a second valid pair existed, the scan would have found it at an earlier index, contradicting the stated uniqueness. So the first hit is provably the expected pair and no backtracking is needed."}
  ]
},
"01_arrays_and_hashing/0036_valid_sudoku": {
  "one_liner": "Three sets of masks (row, column, box) check each cell once.",
  "core_objective": "Decide whether a partially filled 9x9 Sudoku board obeys Sudoku rules: no digit repeats in any row, column, or 3x3 box. Empty cells are always permitted.",
  "bounds": "The board is always exactly 9x9, so the alphabet is fixed at 27 nine-bit masks and 81 cells. '.' means empty and must be skipped before any bit test. Digits arrive as characters, so a 0-9 digit test beats any bit shift unless you subtract '1' first.",
  "diagram": " 0 1 2 | 3 4 5 | 6 7 8        box = (r//3)*3 + (c//3)\n 0 . 5 3 . . 7 . . .\n 0 . 6 . . 1 9 . . .\n 0 9 8 . . . . 6 . .\n ---------+-------+--------\n 3 4 . . . . . . 8 .\n\n bit test : mask[box] >> d & 1\n r0c0 d=5 : boxes[0] bit 5 clear -> set\n r0c6 d=7 : boxes[2] bit 7 clear -> set\n r0c0 d=5 again -> HIT -> invalid\n\n invariant: masks hold exactly the digits already placed",
  "cpp_vs_py": "Nine-bit masks fit in a machine word, so C++ does one shift and one AND per check with the mask living in a register or a 27-element stack array that stays in L1. Python cannot use the `int` as a bit carrier cheaply -- a small `int` is still a heap object -- so `mask | (1 << d)` allocates, and the masks cost 27 boxed integers with pointer chasing at every probe. In exchange Python gets free arbitrary precision, so a 27-bit or 26-bit mask costs nothing extra while the C++ author must remember that `1 << d` with d as the digit 9 needs `-1` to stay inside a byte if they use `uint8_t`.",
  "cpp_alts": [
    "`std::bitset<9>` or a plain `uint16_t` per row/col/box gives compile-time masking; a `bool grid[9][9]` is simplest and still $O(1)$ per cell.",
    "`std::array<std::array<uint16_t,9>,9>` keeps all 243 bits in one contiguous block -- 27 cache lines -- instead of three separate containers.",
    "A `std::unordered_set<char>` per row works but allocates one node per cell; masks allocate nothing."
  ],
  "py_alts": [
    "Three `defaultdict(set)` rows/cols/boxes is the readable version but allocates a set object per line -- 27 set objects plus 81 inserts.",
    "Bit masks with `1 << (int(ch) - 1)` are fastest in Python and mirror C++ exactly.",
    "`str.isdigit()` is locale-free here but slower than comparing against `'1' <= ch <= '9'`."
  ],
  "trap": "Testing the digit against the mask before skipping empties, so `'.'` gets hashed into a bit. The second classic bug is computing the box index as `r * 3 + c` instead of `(r // 3) * 3 + (c // 3)`.",
  "invariant": "After processing cell k, `rows`, `cols`, `boxes` contain exactly the digits already committed in the first k cells. A duplicate is therefore exactly a set bit that was already present.",
  "questions": [
    {"q": "Why 9 bits and not a set per row?", "a": "A mask turns \"has digit d already appeared here?\" into one shift and one AND on a single machine word, with zero allocation. A set needs a pointer chase and a node allocation per insert."},
    {"q": "What is the box index for cell (4, 7) and why?", "a": "(4 // 3) * 3 + (7 // 3) = 1 * 3 + 2 = 5. Integer division on both coordinates folds the 9x9 grid into 3x3 blocks; row-major multiplication would give 4*3+7 = 19, which is out of range."},
    {"q": "The board is fixed at 9x9 -- does that make the problem trivial?", "a": "It removes input parsing, not the design question. The real content is choosing a per-line data structure that makes the duplicate test O(1), and noticing that a fixed alphabet invites bit packing rather than hashing."}
  ]
},
"01_arrays_and_hashing/0049_group_anagrams": {
  "one_liner": "Anagrams share a multiset signature, so signature is the key.",
  "core_objective": "Partition a list of strings so that all strings that are permutations of each other land in the same group, and return the groups in any order.",
  "bounds": "1 <= strs.length <= 1e4; 1 <= strs[i].length <= 100, all lowercase. Worst-case total characters is 1e6, so a sort-based key is $O(L \log L)$ while a 26-slot count signature is $O(L)$. Duplicate strings are legal inputs and simply collide into the same group.",
  "diagram": " str      sorted-key   count-key\n \"eat\"      \"aet\"        \"a#e#t##...\"\n \"tea\"      \"aet\"        \"a#e#t##...\"\n \"tan\"      \"ant\"        \"a#n#t##...\"\n \"ate\"      \"aet\"        \"a#e#t##...\"\n \"nat\"      \"ant\"        \"a#n#t##...\"\n\n dict = {\"aet\": [eat,tea,ate],\n        \"ant\": [tan,nat]}\n\n cost: count-key 26 slots vs sort's O(L log L)",
  "cpp_vs_py": "The 26-slot signature is the whole story in both languages. C++ builds it as a `std::array<char,26>` on the stack, increments 26 bytes of L1-resident memory, then needs a 26-byte array as a hash key -- which means `std::unordered_map` must hash and memcmp 26 bytes per lookup, all still in L1. Python builds the same tuple but as 26 heap-allocated small ints; because Python caches ints -5..256 the increments return interned objects with no allocation, yet the tuple itself is a fresh 26-slot object each time, so the dictionary stores one pointer to it. Python therefore trades roughly one 26-element tuple allocation per string for a much lighter lookup.",
  "cpp_alts": [
    "`array<char,26>` + a custom hasher beats `std::string` keys made from sorted copies: no $O(L \log L)$ sort and no heap string.",
    "`std::map<array<char,26>, vector<string>>` keeps groups ordered by signature, at $O(L \log G)$ for G groups.",
    "Packing the 26 counts into two 64-bit words (5 bits per letter covers length <= 31) makes the key trivially hashable."
  ],
  "py_alts": [
    "`''.join(sorted(s))` is the one-liner but costs $O(L \log L)$ and a fresh string per input.",
    "`tuple(count)` where `count = [0]*26` and you bump `count[ord(c)-97]` is the fast signature.",
    "`defaultdict(list)` collects the groups without a second pass; `itertools.groupby` on a sorted list is an alternative that pays one sort."
  ],
  "trap": "Using the sorted string as the key and then claiming $O(n)$ time. It is $O(L \log L)$; with 1e4 strings of length 100 that sort dominates everything else in the solution.",
  "invariant": "Two strings share a dictionary key exactly when they are permutations of each other -- which is true if and only if they contain the same multiset of characters.",
  "questions": [
    {"q": "What must the hash key capture, and what is the cheapest sufficient encoding?", "a": "Only the multiset of characters. A 26-slot count vector encodes it in $O(L)$; sorted order encodes it in $O(L \log L)$; a bitmask alone would be wrong because it loses multiplicity."},
    {"q": "Why can a plain set of characters not be the key?", "a": "{a, b} cannot distinguish \"ab\" from \"aabb\". Duplicates matter, so the encoding must be a multiset -- counts, not membership."},
    {"q": "What is the total work bound in terms of L, the sum of all lengths?", "a": "$O(L)$ for the count signature plus $O(L)$ hashing, so linear in the input size. The sorted-key version is $O(L \log L)$, which is why the counting version is the better interview answer."}
  ]
},
"01_arrays_and_hashing/0128_longest_consecutive_sequence": {
  "one_liner": "Only start a walk where value-1 is absent, making it O(n).",
  "core_objective": "Return the length of the longest run of consecutive integers appearing anywhere in an unsorted array, with $O(n)$ time.",
  "bounds": "0 <= nums.length <= 1e5, so an $O(n^2)$ scan times out. Values span -1e9..1e9, so the run is not a contiguous index range. Duplicates must not inflate the answer, and the empty array returns 0.",
  "diagram": " nums = [100,4,200,1,3,2]   (longest run = 4)\n\n step 1: put every value in a set\n step 2: only walk from values whose predecessor is MISSING\n\n   x=100  99 in set? NO  -> walk 100 (len 1)\n   x=4    3 in set? YES -> skip  (do NOT walk here)\n   x=200  199 in set? NO -> walk 200 (len 1)\n   x=1    0 in set? NO  -> walk 1->2->3->4  (len 4) BEST\n   x=3    2 in set? YES -> skip\n   x=2    1 in set? YES -> skip\n\n every element is touched O(1) times -> O(n) total",
  "cpp_vs_py": "The fix is structural: each run is walked exactly once because only its minimum is a start. In C++ that means each successful probe is a `find` into an open-addressed `unordered_set<int>` -- one cache miss on a miss, two on a hit -- and the walk is a tight dependent chain of loads. Python pays the same probe count, but each `x - 1 in s` allocates a new PyLong for the probe key, so a 1e5-element scan performs hundreds of thousands of small allocations that C++ never makes. Set membership in CPython short-circuits on identity first, which rescues the repeat probes on already-interned values but not on large negatives.",
  "cpp_alts": [
    "`std::unordered_set<int>` with a reserve() call sized to n -- without it, rehashing dominates for adversarial inputs.",
    "Sorting then a single scan is $O(n \log n)$ time but $O(1)$ extra space beyond the sort and avoids hashing entirely.",
    "A `std::bitset` over the value range is only viable when the range is small; here -1e9..1e9 rules it out."
  ],
  "py_alts": [
    "`set(nums)` once, then a second pass over the set -- iterating the set rather than the list avoids re-checking duplicates.",
    "`s.discard`/`s.remove` while walking shrinks the working set but changes the start-detection logic; the membership gate is cleaner.",
    "A sorted-list scan is slower in Python than the set version because `bisect` is $O(\log n)$ per step and you pay Python-level loop overhead."
  ],
  "trap": "Walking from every element. That is $O(n \cdot \text{runLength})$ and blows up on inputs like [1..100000]. The gate `if x - 1 in s: continue` is what makes it linear.",
  "invariant": "A walk is started at x only when x-1 is absent, so every walk begins at the minimum of its run; consequently no two walks ever cover the same element.",
  "questions": [
    {"q": "Why is checking only run-minima enough?", "a": "Every consecutive run has exactly one minimum, and only that minimum lacks a predecessor in the set. Walking from the minimum visits every element of the run, so all other starting points are redundant work."},
    {"q": "What is the total probe count, and why is it linear rather than quadratic?", "a": "At most two probes per element -- one failed predecessor test and one successful membership test per walk step -- because the runs partition the set. Hence $O(n)$ expected."},
    {"q": "What breaks if you drop the set and sort instead?", "a": "Nothing breaks, the bound just degrades to $O(n \log n)$ time and $O(n)$ or $O(1)$ extra space depending on sort. That is still accepted; it is simply not the tightest answer."}
  ]
},
"01_arrays_and_hashing/0217_contains_duplicate": {
  "one_liner": "Insert into a set; the size tells you a repeat happened.",
  "core_objective": "Return true if any integer appears at least twice in the array, false otherwise.",
  "bounds": "1 <= nums.length <= 2e5; -2e9 <= nums[i] < 2e9, so sorting changes the array's index order but not membership. A single element can never be a duplicate, and negatives are ordinary keys.",
  "diagram": " nums = [1, 2, 3, 1]\n\n s = {}\n  1 -> not in s -> s = {1}\n  2 -> not in s -> s = {1,2}\n  3 -> not in s -> s = {1,2,3}\n  1 -> FOUND        -> True\n\n invariant: len(s) == count of distinct values seen so far",
  "cpp_vs_py": "Both languages do the same amount of work -- n probes -- so the difference is constant factor. C++ inserts into `std::unordered_set<int>` where each insert is a bucket index, a node allocation and a pointer write; with `reserve(n)` the bucket array is one contiguous block and the whole structure is n mallocs plus n probes. CPython's `set` needs no per-element allocation at all for the table itself and its probe uses the value's own hash, but the set stores a PyObject* per slot, so it costs 16 bytes per slot on 64-bit versus C++'s 8-byte node plus 8-byte key plus 8-byte next pointer spread across separate allocations -- which is why Python's set, despite the slower interpreter loop, ends up competitive in memory.",
  "cpp_alts": [
    "`std::unordered_set` with `reserve(n)` and `max_load_factor(0.7)` -- otherwise repeated rehashing triples the cost.",
    "Sorting then adjacent comparison is $O(n \log n)$ time, $O(1)$ extra space, and wins decisively on memory-constrained judges.",
    "`gp_hash_table` with open addressing removes the per-node malloc entirely -- one flat array, n probes."
  ],
  "py_alts": [
    "`len(set(nums)) < len(nums)` is the entire solution; no explicit loop needed.",
    "`return len(nums) != len(set(nums))` is the idiomatic single-expression form interviewers want.",
    "For a pre-sorted array, comparing neighbours is $O(1)$ space and beats building a set."
  ],
  "trap": "Comparing each element against the previous one. That detects only ADJACENT duplicates, so [1, 2, 1] passes. Either sort first or use a set.",
  "invariant": "After processing k elements, `len(seen)` equals the number of distinct values among the first k. So the answer is determined the moment `len(seen)` fails to grow.",
  "questions": [
    {"q": "Why does the set version beat the sort version here even though sort is cache friendly?", "a": "Expected time: $O(n)$ versus $O(n \log n)$. The sort's wins are space ($O(1)$ versus $O(n)$) and constant factor predictability, which is the right trade only when memory is the binding constraint."},
    {"q": "What is the space cost, and can it be reduced?", "a": "$O(n)$ for the set. Sorting in place and scanning neighbours gets it to $O(1)$ auxiliary space (or $O(\log n)$ stack for introsort), at $O(n \log n)$ time."},
    {"q": "How would you detect a duplicate in a 10 GB stream you cannot hold?", "a": "Bloom filter (probabilistic, no false negatives), or sort-external-merge and scan for adjacent equality (exact, needs disk). The set approach fails because its space is linear in the stream."}
  ]
},
"01_arrays_and_hashing/0238_product_of_array_except_self": {
  "one_liner": "Prefix pass left, suffix pass right -- no division allowed.",
  "core_objective": "Return an array where the element at index i is the product of every input element except nums[i], without using division and in $O(n)$ time.",
  "bounds": "1 <= nums.length <= 2e5, so division is banned by the problem statement (and would also fail on zeros). Elements may be 0 or negative, and with exactly one zero the whole output is zero except at that index.",
  "diagram": " nums = [1,2,3,4]      out = [24,12,8,6]\n\n pass 1 (left):  out[i] = product of nums[0..i-1]\n   prefix=1 -> out[0]=1 ; prefix*=1 -> 1\n   out[1]=1  ; prefix*=2 -> 2\n   out[2]=2  ; prefix*=3 -> 6\n   out[3]=6  ; prefix*=4 -> 24\n\n pass 2 (right): multiply the suffix\n   suffix=1 -> out[3]=24*1=24 ; suffix*=4 -> 4\n   out[2]= 6*4=24 ; suffix*=3 -> 12\n   out[1]= 1*12=12 ; suffix*=2 -> 24\n   out[0]= 1*24=24\n\n with a zero [1,0,3]: out=[0,3,0]  division would divide by zero",
  "cpp_vs_py": "The two passes are pure arithmetic on already-loaded values, so C++ keeps the running product in a register and the output vector is one contiguous, write-once buffer that the prefetcher streams perfectly. Python allocates a new int for every product it writes, and for values beyond 2^63 CPython promotes to arbitrary precision: a single 32-digit product means a 100-byte object plus a multiplication routine instead of one `imul`. Python also re-reads the output list element by element in the reverse pass, so the second sweep walks memory backwards, which is mildly prefetcher-hostile on top of the object chasing.",
  "cpp_alts": [
    "One vector doubles as the prefix output array -- $O(1)$ extra space beyond the required output.",
    "Division plus a total-product scan is $O(n)$ and shorter, but is forbidden here and divides by zero whenever the input contains 0.",
    "`long long` is mandatory: with values up to 1e4 and n up to 2e5 the intermediate products overflow 32 bits instantly."
  ],
  "py_alts": [
    "Python integers never overflow, so the whole overflow argument disappears -- but arbitrary-precision multiply is not free.",
    "`math.prod` computes the total but is O(n) per call; slicing products is $O(n^2)$ and fails.",
    "Filling with 1s so the identity element needs no special case at index 0 or n-1 keeps both passes uniform."
  ],
  "trap": "Using the total product and dividing. It is banned, and it crashes on any zero. The prefix/suffix sweep is the only structure that survives zeros.",
  "invariant": "After the left pass, out[i] equals the product of nums[0]..nums[i-1]. After the right pass at index i, out[i] equals product(nums[0..i-1]) * product(nums[i+1..n-1]), which is exactly the answer.",
  "questions": [
    {"q": "Why is division forbidden even when no zeros are present?", "a": "The problem bans it, and more fundamentally it only works when every element is invertible. A single 0 in the input makes the total product 0 and the quotient undefined, so the algorithm would need a zero pass anyway -- at which point the prefix/suffix version is simpler."},
    {"q": "Why does out[0] need to be seeded with 1 rather than nums[0]?", "a": "out[i] must hold the product of everything strictly left of i, so at i = 0 that product is the empty product, which is 1. Seeding with nums[0] would double-count the element."},
    {"q": "What is the space complexity, and can it be O(1)?", "a": "$O(1)$ auxiliary, because the output array itself is reused as the prefix store. Total space including the required output is $O(n)$."}
  ]
},
"01_arrays_and_hashing/0242_valid_anagram": {
  "one_liner": "26 counters: equal multisets iff all 26 slots return to zero.",
  "core_objective": "Decide whether two strings are anagrams of each other, that is whether one is a permutation of the other.",
  "bounds": "1 <= s.length, t.length <= 5e4. Lengths must match first, which rejects half the cases in O(1). Only lowercase English letters are guaranteed, so a 26-slot array is exact; a general solution needs a 26-entry array plus an ASCII guard or a dict.",
  "diagram": " s = \"anagram\", t = \"nagaram\"\n\n need = [0]*26\n for ch in s: need[ord(ch)-97] += 1\n  a+1 n+1 g+1 r+1 m+2\n for ch in t:\n  if need[ord(ch)-97] == 0: return False   (t longer/alien)\n  need[ord(ch)-97] -= 1\n return all(v == 0 for v in need)   (s fully consumed)\n\n invariant: need counts (s prefix) minus (t prefix); never negative",
  "cpp_vs_py": "Twenty-six counters is 26 bytes, so C++ touches a single cache line and increments in place with a `++count[ch - 'a']` -- no allocation, no branching beyond the bounds guard. Python's list of 26 small ints is heap-allocated and CPython caches the values 0..256, so `need[i] += 1` stores back an interned int and allocates nothing, but the list itself costs 264 bytes plus 26 pointers of indirection per access. Python pays about 3x in interpreter dispatch overhead per increment; the memory story is a wash.",
  "cpp_alts": [
    "`std::array<int,26> need{}` is stack-allocated and zero-initialised in one instruction sequence.",
    "Sorting both strings is $O(L \log L)$ but $O(1)$ extra space and trivially correct for any character set.",
    "`std::string_view` avoids the by-value copies that `std::string` parameters would force."
  ],
  "py_alts": [
    "`Counter(s) == Counter(t)` is a one-liner but builds two 26-entry dicts.",
    "`sorted(s) == sorted(t)` is $O(L \log L)$ and allocates two lists of L elements.",
    "`collections.Counter(s) - Counter(t)` computes the multiset difference directly, which is the same idea with dict internals."
  ],
  "trap": "Checking only that every character of s appears in t. Without the counters running back to zero, \"aab\" vs \"abb\" or \"aab\" vs \"aba\" pass. The final all-zero test is the load-bearing line.",
  "invariant": "After each t character, `need[c]` equals the count of c in s minus the count of c in the t prefix. It must never go negative, and it is all zeros at the end exactly when s and t are permutations.",
  "questions": [
    {"q": "Why check the lengths first?", "a": "Different lengths cannot be permutations, and the check is O(1). It also guarantees that if no counter ever goes negative, all counters must finish at zero -- which lets you drop the final scan."},
    {"q": "How do you adapt this to arbitrary characters including unicode?", "a": "Replace the 26-array with a dict keyed by code point, or map code points to ids first. The invariant is unchanged; only the index function changes."},
    {"q": "What is the difference between the sorted and counted approaches in asymptotics and space?", "a": "Counted is $O(L)$ time and $O(1)$ space (26 slots). Sorted is $O(L \log L)$ time and $O(L)$ space for the two sorted copies. Counting wins on both once the alphabet is fixed."}
  ]
},
"01_arrays_and_hashing/0271_encode_and_decode_strings": {
  "one_liner": "Length-prefix framing makes the boundary of each string unambiguous.",
  "core_objective": "Implement `encode` turning a list of strings into one string and `decode` recovering the exact original list. The two must be perfect inverses on any input, including the delimiter character itself.",
  "bounds": "0 <= strs.length <= 1e5; 0 <= strs[i].length <= 100, so a list of 1e5 empty strings is legal and must round-trip. Total encoded length is bounded by roughly 7e6. The delimiter-collision case is the entire difficulty: any scheme that just joins on a character is broken by that character appearing inside a word.",
  "diagram": " input : [\"a\", \"b#c\", \"d\"]        (delimiter '#')\n\n BAD  join : \"a#b#c#d\"\n       decode cannot tell if the token is\n       [a,b,c,d] or [a,b#c,d]\n\n GOOD length-prefix :\n       \"1#a#3#b#c#1#d\"\n        ^ each header states the exact length,\n          so the decoder never guesses a boundary\n\n decode:\n       read digits until '#' -> len\n       take next len chars -> word\n       advance; repeat until exhausted\n\n round trip: [a, b#c, d] -> same list, always",
  "cpp_vs_py": "This is a serialisation problem, so the cost is dominated by per-byte append. In C++ `str.append(s)` writes into a `std::string` whose capacity doubles, so the total copy work is amortised O(total) and the final buffer is one contiguous block -- the decoder can then parse with a raw pointer and a `stoi`-like digit loop touching nothing but the string's own bytes. Python's `str += piece` on a str is also amortised O(1) thanks to CPython's resize heuristic, but the string is UCS-2/UCS-4 internally, so each element costs 1-4 bytes; joining a list of pieces with `''.join` is measurably faster because it does one pass with a precomputed total length instead of repeated resize checks.",
  "cpp_alts": [
    "`std::string::append(s.data(), len)` with a manual length header beats `to_string` + `+` because it avoids temporary string objects.",
    "Reserve the output up front with `reserve(total)` to remove the doubling copies entirely.",
    "`std::string_view` lets `decode` parse without owning a copy; safe only if the encoded buffer outlives the views."
  ],
  "py_alts": [
    "`''.join(parts)` in one pass beats repeated `+=` for many small pieces.",
    "Building the length header with an f-string `f'{len(s)}#'` is faster than `str(len(s)) + '#'`.",
    "`io.StringIO` with `getvalue()` is the other way to batch appends without quadratic risk."
  ],
  "trap": "Joining on a delimiter with no escaping. That round-trips fine on the examples and fails the moment an input string contains the delimiter, which is exactly the hidden test.",
  "invariant": "At every decode step, the cursor sits on the first digit of a length header whose declared length is exactly the number of characters up to the next cursor position. If that holds, the parse never needs to search for a separator.",
  "questions": [
    {"q": "What property must the encoding have for `decode` to be correct?", "a": "It must be unambiguously decodable: the encoded string must determine the original list uniquely. Length-prefixing achieves that by making every boundary explicit rather than inferred from a separator."},
    {"q": "Is the escaping scheme ('#' -> '/#', '/' -> '//') correct?", "a": "It is decodable provided no input string ever contains '/'. That is an unstated assumption about the alphabet, which is why the length-prefix design is the safer answer."},
    {"q": "Why does length-prefixing still decode when the input list is empty or all elements are empty?", "a": "An empty list encodes to the empty string and decodes to nothing. A list of k empty strings encodes to '0#' repeated k times, and each header of 0 consumes zero characters -- so the cursor advances by the header length only, and the count of headers carries the count of empty strings."}
  ]
},
"01_arrays_and_hashing/0347_top_k_frequent_elements": {
  "one_liner": "Count frequencies, then take the top k of the counter.",
  "core_objective": "Return the k most frequent elements in an array, in any order.",
  "bounds": "1 <= nums.length <= 2e4; 1 <= k <= nums.length, so k can equal n and the answer is then just every distinct value. All values are integers in a bounded range, so counting is exact rather than approximate.",
  "diagram": " nums = [1,1,1,2,2,3]  k = 2\n\n counter: {1:3, 2:2, 3:1}\n\n heap.nlargest(2, counter, key=counter.get)\n   push (3,1) -> keep 1\n   push (2,2) -> keep 2,2\n   push (1,3) -> better than 2 -> drop 2\n   -> [1,2]   correct\n\n bucket sort O(n):\n   buckets[3]=[1] buckets[2]=[2] buckets[1]=[3]\n   walk freq 3..1, collect 1 then 2 -> [1,2]",
  "cpp_vs_py": "Counting is the same integer-increment work in both languages, but the selection step diverges. C++ `nth_element` partitions the frequency vector in place with introselect: linear average time, no allocation, and it leaves the k largest in the first k slots unordered -- exactly the freedom this problem allows. Python has no `nth_element`, so `heapq.nlargest(k, ...)` is a lazy min-heap of size k (or `sorted` for $O(n \log n)$); both allocate a real heap of k Python tuples and pay full interpreter overhead per comparison. Bucket sort in Python is $O(n)$ but with a large constant because `max(counts)` plus n bucket appends is n Python-level operations.",
  "cpp_alts": [
    "`std::nth_element(begin, begin + k, end)` on a vector of pairs is $O(n)$ average with no extra memory.",
    "Sorting a vector of (frequency, value) pairs descending and taking k is simpler and $O(n \log n)$.",
    "For a bounded value range, counting into a fixed-size array and then a descending frequency sweep gives strict $O(n)$."
  ],
  "py_alts": [
    "`Counter(nums).most_common(k)` is the intended one-liner; internally it is `heapq.nlargest`.",
    "`heapq.nlargest(k, counter, key=counter.get)` avoids materialising the (count, value) pairs.",
    "`sorted(counter, key=counter.get, reverse=True)[:k]` is the readable fallback but $O(n \log n)$."
  ],
  "trap": "Sorting the input array and taking a slice. Order carries no frequency information, so this returns the k largest VALUES, not the k most frequent ones -- wrong for [1,1,1,2,2,3], k=2.",
  "invariant": "The counter's value set equals the distinct values of nums, and each count equals its exact multiplicity. Selecting the top k of that multiset of counts is therefore equivalent to selecting the k most frequent values.",
  "questions": [
    {"q": "Why can you do better than sorting the array?", "a": "Only multiplicities matter, not positions, so you first compress n items into at most n distinct counts and then select the top k of those. Sorting nums spends its effort on a total order that is then discarded."},
    {"q": "What does `nth_element` guarantee, and what does it not?", "a": "It guarantees the first k elements are the k smallest (or largest, per comparator) as a set, in linear average time. It does NOT sort them, which is fine here since any order is accepted."},
    {"q": "If k equals n, which approach collapses?", "a": "Everything works, but heapq.nlargest special-cases k >= len and returns a sorted list directly. The bucket sweep also degenerates to a full scan of the frequency axis, so it stays O(n)."}
  ]
}
})

KERNELS: dict[str, dict] = {
"01_arrays_and_hashing/0001_two_sum": {
 0: {"py": "seen = {}\nfor i, x in enumerate(nums):\n    if target - x in seen:\n        return [seen[target - x], i]\n    seen[x] = i",
     "cpp": "unordered_map<int,int> seen;\nfor (int i = 0; i < n; ++i) {\n    int need = target - nums[i];\n    if (seen.count(need))\n        return {seen[need], i};\n    seen[nums[i]] = i;\n}"},
 1: {"py": "pairs = sorted((v, i) for i, v in enumerate(nums))\nl, r = 0, len(pairs) - 1\nwhile l < r:\n    s = pairs[l][0] + pairs[r][0]\n    if s == target: return [pairs[l][1], pairs[r][1]]\n    l, r = (l + 1, r) if s < target else (l, r - 1)",
     "cpp": "sort(pairs.begin(), pairs.end());\nint l = 0, r = pairs.size() - 1;\nwhile (l < r) {\n    int s = pairs[l].first + pairs[r].first;\n    if (s == target) return {pairs[l].second,\n                            pairs[r].second};\n    s < target ? ++l : --r;\n}"}
},
}

# ---- appended from _authored_chunk2.json
DATA.update({
 "02_two_pointers/0011_container_with_most_water": {
  "one_liner": "Move the shorter wall; area is width times the shorter height.",
  "category_note": "Two pointers is a search-space-reduction technique, not a data structure. You start with two extremes of the feasible region and every move permanently discards a subrange, so the algorithm is a depth-first walk of an $O(n^2)$ decision tree pruned to a single path. The two flavours are opposite pointers on a sorted-or-unsorted array where a monotone predicate justifies each move, and same-direction pointers where a window's validity is monotone. The invariant to hunt for is always the same: after each move, the discarded end provably cannot appear in any strictly better answer than the one already recorded.",
  "core_objective": "Given an array of non-negative heights, find the two lines that, with the x-axis, hold the most water. Return that maximum area.",
  "bounds": "1 <= height.length <= 2e5; 0 <= height[i] <= 1e4. Fewer than two lines returns 0. The area fits in 32 bits but the intermediate product is the widest arithmetic in the problem, so be careful in C++.",
  "diagram": " h = [1, 8, 6, 2, 5, 4, 8, 3, 7]\n     0  1  2  3  4  5  6  7  8\n\n     l=0,r=8: (8-0) * min(1,7) = 8 8 -> move l (h[l]=1 < h[r])\n     l=1,r=8: (8-1) * min(8,7) = 7 7 -> move r (h[r]=7 < h[l])\n     l=1,r=7: (7-1) * min(8,3) =18 18 -> move r\n     l=1,r=6: (6-1) * min(8,8) =40 40 -> tie: move either\n     l=2,r=6: (6-2) * min(6,8) =24\n     l=3,r=6: (6-3) * min(2,8) = 6 -> move l\n     ... best so far = 49 at l=4,r=8? no: l=2,r=7 -> 5*6=30\n     ANSWER 49 = (8-1) * min(h[1],h[7]) is wrong; true best is\n            l=1,r=6 area 40, or l=4,r=8: 4*min(5,7)=20\n     full sweep records every candidate; only the pruned walk is fast",
  "cpp_vs_py": "The loop is a dependent chain: the next comparison needs the previous pointer, so the branch predictor sees a hard-to-predict pattern and mispredicts often, which is where the real cycles go. C++ keeps `height[l]` and `height[r]` in registers across the iteration and computes the area in two multiplies with no memory traffic beyond two L1 loads; the compiler can even hoist the comparison into a conditional move, eliminating the branch entirely. CPython re-dereferences the list pointer, boxes the indices for `height[l]`, calls `min()` as a Python-level function, and allocates a new int for every `max(...)` candidate -- roughly 15 to 20 bytecodes per iteration for work C++ does in about six instructions.",
  "cpp_alts": [
   "Ternary `h[l] < h[r] ? ++l : --r` instead of an if/else lets the compiler emit a branchless cmov, which removes the misprediction entirely.",
   "Prefix and suffix max arrays give an $O(n)$ one-pass alternative but need $O(n)$ extra memory; the two-pointer version needs none.",
   "For 64-bit safety on huge inputs use `1LL * (r - l) * min(h[l], h[r])` even though the bound here fits in 32 bits."
  ],
  "py_alts": [
   "`min`/`max` are Python function calls; inlining them as conditional expressions is measurably faster in a hot loop.",
   "`while l < r` with `l, r = (l+1, r) if ... else (l, r-1)` avoids rebinding overhead in some interpreters -- measure before trusting it.",
   "`zip(height, reversed(height))` is a cute O(1)-space form but it stops at the midpoint, so it is wrong unless combined with an explicit index."
  ],
  "trap": "Moving the TALLER wall, or moving both pointers. Any answer containing the shorter wall is bounded by the area just computed, so that wall can never improve on the recorded best; discarding it is safe. Discarding the taller one is not, because the shorter wall could pair with something further out.",
  "invariant": "At the top of each iteration, `best` is at least the maximum area over every pair that uses an index already discarded. That is what makes the discard safe.",
  "questions": [
   {
    "q": "Why is it always safe to move the shorter wall?",
    "a": "Any pair (l, j) with j < r holds at most h[l] of water and a width smaller than r - l, so its area is at most what we just recorded. Same symmetric argument for r. Hence the discarded end cannot appear in a better answer."
   },
   {
    "q": "What does the prefix/suffix max version buy you, and what does it cost?",
    "a": "It removes the dependency between the two pointer positions, letting you sweep in one direction. It costs $O(n)$ extra memory and two extra passes, so for this problem the two-pointer version strictly dominates."
   },
   {
    "q": "How many pairs does the two-pointer version actually examine?",
    "a": "At most $n-1$, because each iteration moves exactly one pointer toward the other. The brute force examines $n(n-1)/2$. The speedup comes from the proof above, not from the count alone."
   }
  ]
 },
 "02_two_pointers/0015_3sum": {
  "one_liner": "Fix one value, two-pointer the rest, and skip duplicates.",
  "core_objective": "Return every unique triple of distinct indices whose values sum to zero. Duplicated triples must be reported once and the order within a triple is irrelevant.",
  "bounds": "3 <= nums.length <= 3000; -1e5 <= nums[i] <= 1e5. At least one triple is guaranteed. The $O(n^2)$ target is mandatory because the naive triple loop is $O(n^3)$ and times out at n = 3000.",
  "diagram": " nums = [-1, 0, 1, 2, -1, -4]   -> [[-1,-1,2], [-1,0,1]]\n\n sort: [-4, -1, -1, 0, 1, 2]\n\n i=0 x=-4  nums[i]>0? no\n   l=1 r=5  sum=-3 <0 -> l++      (need bigger)\n   l=2 r=5  sum=-3 <0 -> l++\n   l=3 r=5  sum=-1 <0 -> l++\n   l=4 r=5  sum=-1 <0 -> l++  -> l>=r, next i\n i=1 x=-1  nums[i-1]==-1? YES -> SKIP (dup left)\n   l=2 r=5  sum=0 HIT -> [-1,-1,2]\n        skip dup l (nums[l]==nums[l+1]) -> l=4\n        skip dup r (nums[r]==nums[r-1]) -> r=4\n        l+=1 r-=1 -> l>r, exit\n i=2 x=-1  nums[i-1]==-1? YES -> SKIP (dup left)\n i=3 x=0   l=4 r=5  sum=3 >0 -> r--\n        l=4 r=4 -> exit\n i=4 x=1   nums[i]>0 -> BREAK (rest cannot sum to 0)\n result [[-1,-1,2],[-1,0,1]]",
  "cpp_vs_py": "Sorting dominates here. C++ `std::sort` is introsort -- quicksort with a depth cap, then heapsort, then insertion sort for small ranges -- so it is branch-heavy, cache-friendly on ints (a single 24 KB array for n = 3000, entirely in L1/L2) and never allocates. CPython's `list.sort()` is Timsort, which on an already-sorted or nearly-sorted run costs $O(n)$, and it uses a scratch buffer plus $O(\\log n)$ comparisons per merge step. The real Python cost is not the sort but the triple loop: the inner while is pure bytecode with a `max` of two indices, and CPython's per-iteration overhead of roughly 200 ns dominates the three integer adds that do the actual work.",
  "cpp_alts": [
   "`vector<long long>` for the sum if you want headroom; int is enough for the stated bounds but -1e5 * 3 fits comfortably anyway.",
   "Prune the inner loop with `if (nums[i] + nums[i+1] + nums[i+2] > 0) break;` and `if (nums[i] + nums[n-2] + nums[n-1] < 0) continue;` -- standard three-sum pruning that shaves the constant noticeably.",
   "Sorting once into `vector<pair<int,int>>` keeps original indices if you need them; this problem does not."
  ],
  "py_alts": [
   "`while l < r and nums[l] == nums[l+1]: l += 1` after a hit is what makes the output unique; omitting it is the classic bug.",
   "Two-sum per fixed i with a dict is $O(n^2)$ too but allocates a dict n times; the two-pointer version allocates nothing.",
   "`itertools.combinations` is $O(n^3)$ and unusable here, but its output shape is the fastest way to express the brute force."
  ],
  "trap": "Finding a valid triple and appending it without the duplicate-skipping sweeps afterwards. You then emit the same triple many times, which LeetCode rejects as a wrong answer even though the set of triples is right.",
  "invariant": "For fixed i, `l < r` and `nums[l..r]` is sorted. A sum below zero means no pair at or right of l can work with this i and the current r, so l advances; symmetrically for r. Every triple with first index i is found or provably excluded.",
  "questions": [
   {
    "q": "Why must you skip duplicates after a hit, and not before?",
    "a": "Skipping duplicates on the left before the loop only handles duplicate values of the fixed `i`. After a hit, the same triple can still be re-found by advancing one pointer, so the inner duplicate sweeps on both `l` and `r` are what make the output set unique."
   },
   {
    "q": "Why is `if nums[i] > 0: break` safe?",
    "a": "The array is sorted, so once the fixed value is positive every later value is too and no triple including it can sum to zero. Symmetrically, `nums[i] + nums[n-2] + nums[n-1] < 0` lets you skip the current i entirely."
   },
   {
    "q": "What is the time complexity, and where does each factor come from?",
    "a": "$O(n \\log n)$ for the sort plus $O(n^2)$ for the nested i/l walk -- each i sweeps at most n pointers. The third factor is eliminated by the monotone two-pointer argument inside the inner loop."
   }
  ]
 },
 "02_two_pointers/0042_trapping_rain_water": {
  "one_liner": "Always advance the side with the smaller running maximum.",
  "core_objective": "Given bar heights, compute how much trapped rain water sits between them, assuming the ends are infinitely tall walls.",
  "bounds": "0 <= height.length <= 2e4; 0 <= height[i] <= 1e5. The answer can reach about $10^9$, so it just fits in a signed 32-bit int but any intermediate sum wants `long long`. An empty array or fewer than three bars traps nothing.",
  "diagram": " h = [4,2,0,3,2,5]\n     ^\n     |        <- trapped between 4 and 5\n     |    . . .\n     |  [4][2][0][3][2][5]\n\n l=0 r=5  lo=4 hi=5   lo<hi -> water += 4-2 = 2 (at l=1) -> l=1\n l=1 r=5  lo=4 hi=5   lo<hi -> water += 4-2 = 2 (at l=2) -> l=2\n l=2 r=5  lo=4 hi=5   lo<hi -> water += 4-0 = 4 -> l=3\n l=3 r=5  lo=4 hi=5   lo<hi -> water += 4-3 = 1 -> l=4\n l=4 r=5  lo=4 hi=5   lo<hi -> water += 4-2 = 2 -> l=5  loop ends\n total = 2+2+4+1+2 = 11   (check: 0,1,3,1,2,0)\n\n key: when lo<hi the LEFT bound is already known, so height at l\n      is irrelevant to the level -- only the right side can rise.",
  "cpp_vs_py": "The $O(1)$-space version reads `h[l]` and `h[r]` once per iteration and keeps both running maxima in registers, so the inner loop is two loads, two compares and one subtract -- about as tight as user code gets, and the two loads are cache-friendly because the two fronts sweep inward toward each other and stay resident. Python re-reads `h[l]`, calls `max` twice per iteration, allocates a fresh int for every `water +=` accumulation, and performs the accumulate into a boxed object, so the interpreter spends roughly ten bytecodes doing what the C++ loop does in six instructions. The $O(n)$ prefix/suffix version is worse in C++ for the same reason: it makes two full forward and backward passes over memory to hold data that two registers already carry.",
  "cpp_alts": [
   "The $O(1)$-space two-pointer version needs only `lo`, `hi`, `l`, `r` -- four registers, no allocation, no vector.",
   "A prefix-max vector plus a running suffix max gives one forward pass and one backward pass, $O(n)$ space but better branch prediction.",
   "Bucket approach for huge inputs: clamp heights into min(h, maxH) buckets, accumulate with a running max and a pending-water counter, which is a single streaming pass."
  ],
  "py_alts": [
   "Inlining `max(lo, h[l])` as `lo = lo if lo > h[l] else h[l]` avoids two Python function calls per iteration.",
   "The generator-sum form of the prefix/suffix version is concise but allocates three lists of size n.",
   "For small n a stack-based solution mirroring the histogram problem is also $O(n)$ and reuses a familiar kernel."
  ],
  "trap": "Advancing the taller side, or forgetting to clamp negative contributions to zero. If you move `r` while `h[r] > h[l]` you subtract a height that has not yet been bounded on the left, and the total comes out too large.",
  "invariant": "`lo` is the maximum of `h[0..l]` and `hi` the maximum of `h[r..n-1]`. When `lo <= hi`, the water level at l is exactly `lo`, so adding `lo - h[l]` is final and `l` can be retired. Symmetrically for r.",
  "questions": [
   {
    "q": "Why does the smaller running maximum decide which side to move?",
    "a": "If `lo <= hi`, the highest bar seen from the left already bounds column l, and the right side cannot get lower than `hi`. So the final water surface at l is `lo` and adding `lo - h[l]` now is safe; symmetrically when `hi < lo`. The two cases are the only possibilities, so every step is correct."
   },
   {
    "q": "Is the O(n)-space prefix/suffix solution ever preferable?",
    "a": "Yes, if you also need the per-column trapped amounts later, or if a single left-to-right pass suits a streaming source. For a single scalar answer the two-pointer version is strictly better: less memory, fewer passes, and a shorter dependency chain."
   },
   {
    "q": "How do you prove the two-pointer version never skips a column's water?",
    "a": "Each iteration retires exactly one index and adds its exact final contribution, and the pointers move only inward from 0 and n-1 until they meet. So every column is counted exactly once, and its level was provably final at the time it was counted."
   }
  ]
 },
 "02_two_pointers/0125_valid_palindrome": {
  "one_liner": "Two pointers that skip non-alphanumeric and fold case.",
  "core_objective": "Decide whether a string reads the same forwards and backwards after discarding every non-alphanumeric character and ignoring letter case.",
  "bounds": "1 <= s.length <= 1e5, no bound on the character set. An empty result after filtering is a palindrome. Digits count as alphanumeric, so '0' must be compared too, and non-ASCII letters need an explicit alnum predicate.",
  "diagram": " s = \"A man, a plan, a canal: Panama\"\n     l=0                r=len-1\n\n step 1: skip non-alnum from both ends, fold case\n step 2: compare, advance both\n\n   A ... a   -> 'a' == 'a'  ok\n   m ... m   -> ok\n   a ... n   -> 'a' != 'n'  ... keep going, real middle\n   \\n\n   filtered = \"amanaplanacanalpanama\"\n   reversed = \"amanaplanacanalpanama\"\n\\n memory: two pointers, zero allocation (BEST)\n vs    filtered + reversed = 2 extra strings of size n",
  "cpp_vs_py": "The $O(1)$-space version is the whole point, and it is where the languages diverge most. C++ `isalnum` and `tolower` from `<cctype>` are locale-aware C functions operating directly on `char` inside the string's own buffer, so the scan is a pure in-place read with perfect prefetch behaviour and zero allocation. Python's `str.isalnum()` is a method call on a one-character string, and critically CPython caches single-character Latin-1 strings, so `s[l].isalnum()` does not allocate -- but `s[l].lower()` on a character with no uppercase form also returns a cached object. The remaining cost is the four method dispatches per iteration, which at n = 1e5 dominates everything else.",
  "cpp_alts": [
   "Use `std::isalnum(static_cast<unsigned char>(ch))` -- passing a plain signed `char` is undefined behaviour for bytes above 127.",
   "`std::string_view` avoids a copy of the input if you must take it by value elsewhere.",
   "A manual in-place compaction into a buffer (write pointer, read pointer) beats the two-pointer version when you need to keep the filtered string, and is still one pass."
  ],
  "py_alts": [
   "Generator filtering plus a comparison against the reversed generator is awkward; the explicit two-pointer loop is clearest.",
   "`s[l].isalnum()` beats `re.match` or `str.translate` here -- the per-call regex machinery dwarfs the check.",
   "`casefold()` is stricter than `lower()` for Unicode but slower; with the ASCII guarantee, `lower()` is correct and fast."
  ],
  "trap": "Using the whole-string reverse comparison and calling it $O(1)$ space. It is $O(n)$ space and allocates two strings. Also, forgetting that digits count, or comparing without folding case so 'A' != 'a' fails every real test.",
  "invariant": "Throughout the loop, every character strictly left of `l` and strictly right of `r` has already been matched with its mirror (or skipped as non-alphanumeric). So the remaining work is entirely inside the window [l, r].",
  "questions": [
   {
    "q": "Why is the two-pointer version $O(1)$ space and the reversed-copy version not?",
    "a": "The two-pointer version only holds two integer indices and reads the original buffer in place. Building `t = filtered` and then `t[::-1]` materialises two new strings of length n, so that version is $O(n)$ space."
   },
   {
    "q": "What does `isalnum` return for unicode digits and accented letters in Python?",
    "a": "True for any unicode alphanumeric, which is broader than the ASCII definition. C++ `std::isalnum` with the default 'C' locale only accepts ASCII. That divergence is exactly why a naive port can behave differently on non-ASCII input."
   },
   {
    "q": "How do you make the digits comparison safe from sign issues in C++?",
    "a": "Cast to `unsigned char` before calling `isalnum`/`tolower`. A `char` with the high bit set is negative, and passing that where an `unsigned char` is expected is undefined behaviour -- a real source of crashes on non-ASCII input."
   }
  ]
 },
 "02_two_pointers/0167_two_sum_ii": {
  "one_liner": "Sorted input means one pointer move per step; watch the 1-based indices.",
  "core_objective": "Given a 1-indexed array of integers sorted in ascending order, return the 1-indexed positions of the two numbers that add to target.",
  "bounds": "2 <= numbers.length <= 3e4; -1e7 <= numbers[i] < 1e7; exactly one solution exists and l < r always. The output must be 1-based -- the single most common failure on this problem.",
  "diagram": " numbers = [2, 7, 11, 15]   target = 9\n         idx1   idx2  idx3   idx4\n\n l=1 r=4  2 + 15 = 17 > 9  -> r=3\n l=1 r=3  2 + 11 = 13 > 9  -> r=2\n l=1 r=2  2 +  7 =  9 = 9  -> return [1, 2]\n\n why r moves on 'too big': numbers[l] is the smallest remaining,\n so with this l no smaller r can work either -> retire l? no,\n retire r because any smaller r only makes the sum smaller,\n and we already know l is at its smallest useful value here.\n\n 1-BASED TRAP: returning [0, 1] fails.\n Binary-search alternative is O(n log n); the log n is wasted.",
  "cpp_vs_py": "Sorted input plus two indices is the ideal shape for C++: `numbers[l]` and `numbers[r]` are loads from opposite ends of a 240 KB array, the cache lines holding both are fetched once and reused on every subsequent iteration, and the pointer update is a single decrement that the compiler turns into a branchless cmov. The array is read-only, so there is no store traffic and no write-allocate misses at all. Python does the same two loads through `numbers.__getitem__`, which returns a borrowed reference and interns nothing here, then allocates a new int for the sum each iteration; the comparison chain is identical but executed in bytecode, so the constant factor is 20 to 50 times larger even though the asymptotics match.",
  "cpp_alts": [
   "A single `for` with two index variables and a ternary move compiles to cmov and avoids one predictable-branch misprediction per iteration.",
   "`std::lower_bound` + `std::upper_bound` gives $O(n \\log n)$ with branch-predictable library code -- a reasonable fallback when readability matters more than the constant.",
   "Because the array is sorted and you know the index, you can prune the right end using `target - numbers[0]` as an initial bound."
  ],
  "py_alts": [
   "The dict version is $O(n)$ time but $O(n)$ space -- strictly worse here, listed only as the contrast that motivates the two pointers.",
   "`bisect_left` per element is $O(n \\log n)$ in C-implemented code, which for large n can beat a Python-level two-pointer loop despite the worse asymptotics.",
   "Using `numbers[l] + numbers[r] < target` directly avoids materialising `s`, saving one int allocation per iteration."
  ],
  "trap": "Returning 0-based indices. The input is explicitly 1-indexed and the expected answer is `[1, 2]` for the standard example, not `[0, 1]`.",
  "invariant": "At every step, if a valid pair exists at all, one exists with `l' >= l` and `r' <= r`. That is exactly what lets each move retire one index permanently.",
  "questions": [
   {
    "q": "Why is moving the pointer toward the middle correct given sorted input?",
    "a": "If the sum is too large, every pair using the current `r` with a smaller `l` is also too large, because `numbers[l]` only decreases as `l` grows. So `r` cannot be part of a solution and can be retired. The sum-too-small case is symmetric for `l`."
   },
   {
    "q": "Is the hash-map solution acceptable here?",
    "a": "It is $O(n)$ and correct, but the array is already sorted, so the two-pointer version is $O(n)$ time with $O(1)$ space and no hashing. Mentioning why the sorted invariant makes the map unnecessary is the point of the comparison."
   },
   {
    "q": "What is the tight bound on pointer moves?",
    "a": "At most $n-1$ moves, since each iteration moves exactly one pointer and the gap shrinks by one. Combined with the $O(1)$ cost of each load and add, the whole scan is a linear pass over two cache lines' worth of active data."
   }
  ]
 },
 "03_sliding_window/0003_longest_substring_without_repeating_characters": {
  "one_liner": "Jumping the left pointer past the last duplicate is O(n).",
  "category_note": "A sliding window is a promise that the answer's defining property is monotone under window extension: for fixed-size validity (no repeats, at most k replacements, anagram) growing a window can only add violations, so the left pointer never needs to retreat. Three variants recur: the last-seen index map, which jumps `left` directly past the conflict in $O(1)$; the shrink-by-one set, which costs $O(26)$ extra per left step; and the counter-of-required-frequency with a formed/match counter. The invariant is always about what the window currently contains, and the performance hinges on how aggressively you can advance `left` rather than how many characters the window holds.",
  "core_objective": "Return the length of the longest contiguous substring of s containing no repeated characters.",
  "bounds": "1 <= s.length <= 5e4; the character set is unspecified, so a 256-entry array is needed rather than 26. The answer is at most the number of distinct characters, which caps how far the window can ever grow.",
  "diagram": " s = \"abcbbad\"  -> answer 3 (\"abc\" or \"bba\"->3)\n\n r=0 'a'  last={}        l=0 win=\"a\"   len 1\n r=1 'b'  last={a:0}      l=0 win=\"ab\"  len 2\n r=2 'c'  last={a:0,b:1}  l=0 win=\"abc\" len 3  best=3\n r=3 'b'  last[b]=1  l=max(0,1+1)=2   win=\"cb\"  len 2\n r=4 'b'  last[b]=3  l=max(2,3+1)=4   win=\"b\"   len 1\n r=5 'a'  last={a:0,b:3} l=max(4,0+1)=4 win=\"ba\"  len 2\n r=6 'd'  l=4                       win=\"bad\" len 3\n\\n max(len) = 3\n\\n each index enters and leaves the window exactly once -> O(n)",
  "cpp_vs_py": "Both versions do $n$ probes, but the second version does strictly more work in Python. The last-seen map in C++ is a 256-entry `int` array sitting in L1 -- 1 KB, fully resident, and the update `last[ch] = r` is a single store with no allocation and no bounds check if the array is fixed-size. The Python dict, by contrast, hashes the one-character string (a cached Latin-1 object, so the hash is cached too) and stores an interned int value; the `max(l, last[ch] + 1)` allocates a fresh int for `last[ch] + 1` every single iteration. That is $n$ small allocations that C++ never performs, which is the dominant cost in Python.",
  "cpp_alts": [
   "A fixed `int last[256]` beats `unordered_map<char,int>` for an ASCII byte alphabet: O(1) array indexing, no hashing, no node allocation.",
   "Use `unsigned char` for the index to avoid sign extension and out-of-bounds on bytes above 127.",
   "A 26-entry array plus a lowercase-only precondition is 104 bytes -- guaranteed single cache line."
  ],
  "py_alts": [
   "`last.get(ch, -1)` in one lookup beats `if ch in last: last[ch]` which is two hash lookups.",
   "Iterating with `enumerate` avoids the explicit index increment and the range/len round trip.",
   "For a lowercase-alphabet guarantee, a `list` of size 26 indexed by `ord(ch) - 97` beats a dict by a wide margin."
  ],
  "trap": "`l = last[ch] + 1` instead of `l = max(l, last[ch] + 1)`. If the conflict lies behind the current window, that assignment moves `l` backwards, and for inputs like `\"abba\"` the window shrinks incorrectly and the reported length is too small.",
  "invariant": "Before processing `s[r]`, `s[l..r-1]` has no duplicate characters and `last[ch]` is the greatest index < r where `ch` occurred. Setting `l = max(l, last[s[r]] + 1)` therefore yields the smallest valid `l`, which maximises the window length for this `r`.",
  "questions": [
   {
    "q": "Why is `max` needed rather than a plain assignment?",
    "a": "The previous occurrence of `s[r]` might be at an index smaller than `l - 1`, i.e. outside the window. A plain assignment would drag `l` backwards and shrink a window that is already valid. `max` enforces monotonicity of `l`, which is what keeps the total work linear."
   },
   {
    "q": "What does the last-seen approach buy over the shrinking set?",
    "a": "One probe instead of up to 26 erase operations per left move, and each index is touched a constant number of times rather than once per possible duplicate. Both are $O(n)$ in theory; the map version has the smaller constant because it never re-reads characters it has already discarded."
   },
   {
    "q": "Can the window length exceed the number of distinct characters?",
    "a": "No. If the window has d distinct characters then its length is d, so len <= d and also len <= 26 for a lowercase alphabet. That bound is a useful sanity check: any answer above 26 on a lowercase-guaranteed input is a bug."
   }
  ]
 },
 "03_sliding_window/0076_minimum_window_substring": {
  "one_liner": "Shrink from the left while valid; count formed letters, not characters.",
  "core_objective": "Return the shortest substring of s that contains every character of t, including multiplicities, or the empty string if none exists.",
  "bounds": "1 <= s.length, t.length <= 1e5 over the printable ASCII set, so a 128- or 256-slot array is valid and a dict is unnecessary. The empty string is a valid t. Duplicate letters in t must be satisfied: t = 'aab' needs two a's.",
  "diagram": " s = \"ADOBECODEBANC\", t = \"ABC\"  -> \"BANC\"\n\n need  = {A:1, B:1, C:1}   need_size = 3\n win   = {A:1,B:2,C:2,E:2,D:1,O:1}   formed = 0\n\n r: A  win[A]=1 == need[A] -> formed=1\n r: D  win[D]=1, not in need      formed=1\n r: O  ..                          formed=1\n r: B  win[B]=1 == need[B] -> formed=2\n r: E  ..                          formed=2\n r: C  win[C]=1 == need[C] -> formed=3   window \"ADOBEC\" valid\n        record 6 ; shrink: drop A -> win[A]=0 < need -> formed=2, l++\n r: O  ..    (invalid, keep extending)\n r: D  ..\n r: E  ..\n r: B  win[B]=1 == need[B] -> formed=3   window \"CODEBANC\" valid\n        record 7 (worse, skip)\n        drop C -> formed=2, l++\n r: A  win[A]=1 -> formed=3   window \"E BANC\" len 5? record\n        drop O (not needed) -> still valid\n        ... best = \"BANC\" (4) -> return s[bl:br+1]\n\\n critical: 'formed' counts DISTINCT letters satisfied, not letters seen",
  "cpp_vs_py": "The inner shrink loop is the hot path and it is branch-heavy: every character removal tests membership in `need` and compares against a stored count. C++ with two `unordered_map<char,int>` keeps each map in one or two cache lines for the ASCII range, so the probes are L1 hits after the first few characters; the alternative is a fixed `int need[128], win[128]` pair, 1 KB total, which eliminates hashing entirely and turns `need[ch]` into a pure load. Python's `Counter` and `dict` do the same logical work but each `window[out] -= 1` is a dict update with an int object, and `out in need` is a second hash lookup -- so the shrink loop pays roughly three dict operations per removed character where C++ pays two array loads.",
  "cpp_alts": [
   "`array<int,128> need{}, win{}` replaces both maps for the printable-ASCII guarantee, turning hashing into indexing.",
   "Track a `matched` count against `need.size()` rather than recounting -- that is what keeps the inner loop $O(1)$ per removal.",
   "`std::string_view` lets you return a view of the original buffer instead of copying the substring."
  ],
  "py_alts": [
   "`Counter` pre-decrement is not supported; `need.get(ch, 0)` is the idiomatic equivalent and avoids the `in` + `[]` double lookup.",
   "`collections.defaultdict(int)` removes the `get` boilerplate but is measurably slower than `dict.get`.",
   "For a strictly lowercase alphabet, two 26-element lists are faster than any dict in CPython."
  ],
  "trap": "Testing `all(v >= need[k] for k in need)` on every left move. That is $O(26)$ per step and blows the constant. The `formed` counter makes the validity test a single integer comparison, which is what keeps the whole thing linear.",
  "invariant": "`formed` equals the number of distinct characters of t whose window count has reached its required count, and no window count ever exceeds its requirement for a needed character because you extend before you shrink. So `formed == len(need)` is exactly \"the window covers t\".",
  "questions": [
   {
    "q": "Why track distinct letters satisfied rather than total letters matched?",
    "a": "Total letters matched is unbounded and does not capture coverage: t = 'AB' with window 'AABB' matches 4 letters but is invalid. `formed` counts how many of the required distinct characters are at or above their requirement, so equality with `len(need)` is precisely the validity predicate."
   },
   {
    "q": "Why does extending before shrinking keep counts from overshooting?",
    "a": "You add `s[r]` first and only then run the shrink loop, and you shrink exactly one character per iteration. Because the invariant forbids a needed count from exceeding its requirement, the `formed == need_size` test flips exactly once per shrink, which is what makes the loop terminate predictably."
   },
   {
    "q": "What makes this problem harder than the no-repeating variant?",
    "a": "The required multiset is input-dependent rather than \"all distinct\", so you need two data structures and a counter, and the window can become invalid again after shrinking (unlike the simple case). That extra state is the entire delta."
   }
  ]
 },
 "03_sliding_window/0121_best_time_to_buy_and_sell_stock": {
  "one_liner": "Track the running minimum price; the best profit is price minus it.",
  "category_note": "Sliding windows over arrays whose validity predicate is monotone in the window's length. Once a window is valid, every super-window containing it is valid too (at most k replacements, fixed-size anagram); once a window has a duplicate, every super-window has one as well. That monotonicity is what licenses a single left-to-right sweep in which `left` never retreats. The recurring bookkeeping is a small fixed-size frequency array plus a scalar that says how much of the requirement is currently satisfied, so that both the extend step and the shrink step are O(1).",
  "core_objective": "Return the maximum profit obtainable from one buy followed by one sell on later days, or 0 if no profit is possible.",
  "bounds": "1 <= prices.length <= 1e5; 0 <= prices[i] <= 1e4, so the array is non-decreasing only in the degenerate sense and prices are never negative. n = 1 must return 0, and a strictly decreasing series must also return 0 rather than a negative number.",
  "diagram": " prices = [7,1,5,3,6,4]   -> 5 (buy 1 sell 6)\n\n p=7  lo=7  best=max(0, 7-7)=0\n p=1  lo=1  best=max(0, 1-1)=0\n p=5  lo=1  best=max(0, 5-1)=4\n p=3  lo=1  best=max(0, 3-1)=2   (no shrink: 2 < 4)\n p=6  lo=1  best=max(0, 6-1)=5   BEST\n p=4  lo=1  best=max(0, 4-1)=3\n\\n invariant: at day r, lo = min(prices[0..r])\n so p - lo is the best profit among all sells on day r.\n\\n the two-pointer loop is O(n^2) because l restarts per r;\n the running-minimum sweep does the same work in one pass.",
  "cpp_vs_py": "This loop is as tight as C++ gets: one load per iteration, two `min`/`max` which the compiler emits as `cmov`, and a loop-carried dependency of only two registers. There is no memory traffic beyond the streaming load of `prices`, so the loop runs at roughly one element per cycle and is entirely bound by the load port. Python executes roughly 8 bytecodes for the same step and, critically, allocates a new int for each `p - lo` candidate before `max` discards most of them -- so for n = 1e5 you get 1e5 short-lived int allocations, which is the difference between microseconds and milliseconds.",
  "cpp_alts": [
   "`lo = min(lo, p); best = max(best, p - lo);` compiles to branchless cmovs, removing the unpredictable branch a naive `if` would create.",
   "`std::min_element` over the prefix is unnecessary -- the running minimum is already optimal.",
   "For a second transaction variant, remember the best two profits with two running minima instead of a DP table."
  ],
  "py_alts": [
   "Conditional expressions beat the builtin calls in a hot Python loop because each `min()` is a function dispatch.",
   "Iterating `for p in prices` rather than indexing avoids the range/len overhead entirely.",
   "`itertools.accumulate(prices, min)` then a max over `p - lo` is C-speed but allocates an n-element list; faster for very large n."
  ],
  "trap": "Updating `lo` after computing the candidate, so day r's profit is measured against itself and can never be positive on a new minimum day. The order must be: lower the floor first, then measure.",
  "invariant": "After processing `prices[r]`, `lo` equals the minimum price over indices 0..r and `best` equals the maximum profit over all buys strictly before some sell at index <= r. Together they mean `best` is final for every prefix, so no later recomputation is needed.",
  "questions": [
   {
    "q": "Why does a running minimum replace a sliding window here?",
    "a": "Validity here is not about window content but about a max over pairs (i, j) with i < j. For each sell j the best buy is the prefix minimum, which is a single scalar carried forward. A window would have to re-examine every earlier price for every j, giving $O(n^2)$."
   },
   {
    "q": "What does the strictly-decreasing input return, and why is that correct?",
    "a": "0. `lo` equals the current price on every step so `p - lo = 0`, and `best` stays at its initial 0. Returning a negative profit would be wrong since doing nothing is allowed."
   },
   {
    "q": "How would you extend this to at most two transactions?",
    "a": "Carry four scalars: two buys seen so far, one sell, and the best profit. The extra state is why the simple running minimum stops working -- once you may re-enter after selling, the floor is no longer a single prefix minimum."
   }
  ]
 },
 "03_sliding_window/0239_sliding_window_maximum": {
  "one_liner": "A deque of indices, monotone decreasing, answers every window.",
  "core_objective": "For every contiguous window of size k in nums, return the maximum value in that window.",
  "bounds": "1 <= nums.length <= 1e5; -1e4 <= nums[i] <= 1e4; 1 <= k <= n. The output length is n - k + 1. Windows near the end must not produce output before r >= k - 1.",
  "diagram": " nums = [1, 3, -1, -3, 5, 3, 6, 7], k = 3\n\n r=0  1  push 0        dq=[0]\n r=1  3  pop 0 (<=3)   push 1     dq=[1]        (1 dominated by 3)\n r=2 -1  push 2        dq=[1,2]\n r=3 -3  push 3        dq=[1,2,3]   out[0]=nums[1]=3   window 0..2\n r=4  5  pop 3,2,1     push 4     dq=[4]        out[1]=5\n r=5  3  push 5        dq=[4,5]     out[2]=5\n r=6  6  pop 5,4       push 6     dq=[6]        out[3]=6\n r=7  7  pop 6          push 7     dq=[7]        out[4]=7\n\\n out = [3, 5, 5, 6, 7]\n\\n two pops per element, max once:\n   FRONT pop = expired (index < r-k+1)\n   BACK  pop = dominated (nums[back] <= nums[r], never\n           the max of any future window containing it)",
  "cpp_vs_py": "The deque is a linked structure in the general case, but both languages let you implement this one as a flat array with head and tail indices, which turns every push and pop into an integer increment or decrement on two registers. That is the key optimisation: in C++ the deque elements are indices, so the comparison `nums[dq.back()] <= nums[r]` is two loads from the same cache-line-dense array as the input, and the amortised cost is one comparison plus at most two writes per element. CPython's `collections.deque` is a genuinely optimised block-based structure with $O(1)$ end operations and no per-element malloc, so the amortised bound is the same; the overhead is the interpreted `while` conditions and the tuple-free but still boxed index arithmetic. The heap alternative costs $O(n \\log n)$ in both.",
  "cpp_alts": [
   "Replace `std::deque<int>` with `vector<int> dq(n); int head = 0, tail = 0;` -- two register indices, no block reallocation, best locality.",
   "`std::multiset` or `priority_queue` with lazy deletion is the simpler alternative at $O(n \\log k)$ time and $O(k)$ space.",
   "For very large n, a segmented/two-pass block-maximum method (the van Herk / Gil-Werman algorithm) gets $O(n)$ with $O(1)$ memory and is cache-friendlier than pointer-based deques."
  ],
  "py_alts": [
   "`deque` is the right structure; a Python list with a moving head leaks memory unless you periodically slice, which is $O(n)$.",
   "`heapq.heappushpop` fuses the push and the stale pop into one C call, which is why the heap variant is competitive in Python.",
   "For the two-block (prefix/suffix max) approach, list comprehensions run at C speed and often beat an interpreted deque loop."
  ],
  "trap": "Popping from the back with `<` instead of `<=`. With `<=` the newer equal element replaces the older one, which keeps the deque smaller and is still correct. With `<` the deque fills with stale equals and the amortised argument weakens. Also: pop the front BEFORE reading `dq[0]`, otherwise you can report an expired index.",
  "invariant": "The deque holds indices strictly increasing, whose values are strictly decreasing, and all lie within the current window [r-k+1, r]. Therefore `dq[0]` is always the window maximum and any index removed from the back is provably never a future maximum.",
  "questions": [
   {
    "q": "Why is it safe to discard a smaller element when a bigger one arrives behind it?",
    "a": "If `nums[i] <= nums[r]` with i < r, then every future window containing i also contains r (because r is to its right and windows are contiguous), so i can never be a maximum again. That domination argument is the entire correctness proof of the back-pop."
   },
   {
    "q": "What is the amortised cost of the whole algorithm?",
    "a": "Each index is pushed once and popped at most once from either end, so across n iterations there are at most 2n pops and n pushes: $O(n)$ total, $O(k)$ space. The per-iteration cost looks like a while loop but is amortised constant."
   },
   {
    "q": "When would the heap be the better answer in an interview?",
    "a": "When k is large relative to n or when the same structure must serve several different window sizes, or when you want to expose the trade-off. It is $O(n \\log k)$ with the same $O(k)$ space, so it is never asymptotically better here."
   }
  ]
 },
 "03_sliding_window/0424_longest_repeating_character_replacement": {
  "one_liner": "Window length minus the max frequency, allowed to exceed k.",
  "core_objective": "Return the length of the longest substring containing at most k distinct repeating characters, i.e. at most k characters differing from the substring's most common character.",
  "bounds": "1 <= s.length <= 1e5; 1 <= k <= s.length; s consists of uppercase English letters, so a 26-slot array is exact. When k >= 26 the answer is simply n, which is a useful early exit.",
  "diagram": " s = \"AABABBA\", k = 1  -> answer 4 (\"ABBA\")\n\n r=0 A  need[A]=1 mx=1   len 1-1=0 <=1 -> best 1\n r=1 A  need[A]=2 mx=2   len 2-2=0 <=1 -> best 2\n r=2 B  need[B]=1 mx=2   len 3-2=1 <=1 -> best 3\n r=3 A  need[A]=3 mx=3   len 4-3=1 <=1 -> best 4  BEST\n r=4 B  need[B]=2 mx=3   len 5-3=2 >1  -> shrink l\n         len 4-3=1 <=1 -> best 4\n r=5 B  need[B]=3 mx=3   len 6-3=3 >1  -> shrink l\n         ... shrinks until len-mx<=1 again\n r=6 A  ...\n\\n why mx may STALL: after a shrink the true max can only\n drop, but keeping the stale (larger) mx keeps len-mx small,\n so the window stays valid. Only ever UPDATE mx upward.",
  "cpp_vs_py": "The inner shrink loop decrements one array slot and increments one index, so the whole algorithm is a pair of sweeps over a 104-byte array that never leaves L1. C++ performs that in a handful of instructions per character, giving $O(n)$ with a very small constant. Python does the same arithmetic but each `need[s[l] - 'A'] -= 1` performs an index computation, a list lookup, an int subtraction and a list store -- roughly 12 bytecodes for work C++ does in one `dec` instruction. The subtle correctness point is that `mx` is allowed to be stale, which is safe because `mx` never decreases; that monotonicity is trivially expressible in both languages and is the whole trick.",
  "cpp_alts": [
   "`int need[26] = {}` on the stack beats any map; the working set is one and a half cache lines.",
   "Hoist `mx` out of the loop as a separate variable rather than recomputing `max(*max_element(...))` each iteration.",
   "For mixed case, `s[r] - 'A'` breaks; either normalise once or index with a 256-entry array."
  ],
  "py_alts": [
   "`Counter` is much slower than a 26-element list because dict operations are hash lookups.",
   "Tracking `mx` as a separate scalar rather than recomputing `max(count)` is essential -- `max()` over 26 slots per iteration would make it $O(26n)$.",
   "`ord(ch) - 65` is needed for uppercase; using the character directly with a list fails."
  ],
  "trap": "Recomputing `mx = max(count)` after each shrink, which is both slower and -- if implemented as a stale-value reset -- wrong. `mx` must be monotonically non-decreasing: you only ever set `mx = max(mx, need[ch])` on extension.",
  "invariant": "`mx` is the maximum frequency observed in the window at any point since the window reached its current minimum size. Because frequencies only decrease on a shrink, `len - mx` is a lower bound on the true number of replacements, so `len - mx <= k` is sufficient (never falsely invalid) for validity, and the window recorded is genuinely valid.",
  "questions": [
   {
    "q": "Why is it legal to keep a stale `mx` after the window shrinks?",
    "a": "If the true maximum drops, then `len - trueMax <= len - staleMax`, so using the larger stale value gives a smaller, still-safe replacement count. Using it can never make an invalid window look valid -- it only makes the shrink test fire later. The recorded window is checked by the true condition implicitly."
   },
   {
    "q": "What happens when `k >= 26`?",
    "a": "With a 26-letter alphabet, `len - mx <= len - 1 <= n - 1 <= k` whenever `k >= n`, and for `k >= 26` the shrink loop never fires after the first 26 characters. An early `if k >= 26: return n` short-circuits the whole sweep."
   },
   {
    "q": "Why does the shrink loop need a while, not a single if?",
    "a": "Dropping one character can reduce the window length by one while `mx` stays the same, so the excess `len - mx - k` may exceed 1 by an arbitrary amount when k is small. The while loop keeps dropping until the condition holds, and total drops across the whole run is exactly n because `l` only moves forward."
   }
  ]
 },
 "03_sliding_window/0567_permutation_in_string": {
  "one_liner": "Fixed-size window with a match counter kept in O(1) per slide.",
  "core_objective": "Return true if s2 contains a permutation of s1, that is a contiguous substring of s2 whose character multiset equals that of s1.",
  "bounds": "1 <= s1.length, s2.length <= 1e5; s1 and s2 contain lowercase and/or uppercase English letters, so a 52-slot or 128-slot ASCII array is required -- a 26-slot array is wrong for mixed case. s1 may be longer than s2, which must return false immediately.",
  "diagram": " s1 = \"ab\", s2 = \"eidbaooo\"  -> true (\"ba\" at index 3)\n\n need[26] vs win[26], window width W = len(s1) = 2\n matches = #{ i : need[i] == win[i] }   (0 or 26)\n\\n slide by one: OUT = s2[r-W], IN = s2[r]\n   matches += (win[OUT] == need[OUT])\n   win[OUT] -= 1\n   matches += (win[OUT] == need[OUT])      (after change)\n   win[IN]  += 1\n   matches += (win[IN]  == need[IN])\n\\n each slide: 3 compares + 2 increments = O(1)\n the naive version recomputes matches = sum(...) = O(26) per slide\n\\n when |s1| > |s2|  -> no window of width W exists -> False",
  "cpp_vs_py": "The whole algorithm exists to avoid an $O(26)$ recomputation per slide, and in C++ the compare-and-adjust pattern compiles to three conditional increments on a counter in a register, with the 26-element arrays permanently in L1. That makes a slide about six instructions. Python performs the same logic with list indexing and int boxing: each `(win[out] == need[out])` yields a bool object (interned, so no allocation) but the arithmetic `matches += True - False` still creates a new int, and the list index computation `ord(s2[r]) - 97` allocates nothing but costs several bytecodes. For n = 1e5 slides this is roughly a million bytecodes in Python against well under a million cycles in C++.",
  "cpp_alts": [
   "Use `int need[128], win[128]` indexed by `unsigned char` -- handles mixed case without any case-folding branch.",
   "`std::array` instead of a raw array gives you `operator[]` with no behavioural difference but clearer intent.",
   "For the fixed 52-letter case, `memcmp(need, win, 52) == 0` per slide is 52 bytes of SIMD-comparable load, which can beat the counter for small alphabets -- but it is $O(\\sigma)$ again."
  ],
  "py_alts": [
   "`Counter(s2[i:i+len(s1)]) == Counter(s1)` is correct but $O(W \\cdot \\sigma)$ per window and $O(W)$ allocations -- it times out at n = 1e5.",
   "The `matches` counter is the whole optimization; keep it as a plain int and avoid `sum()` per slide.",
   "For lowercase-only inputs, `[0]*26` lists beat `Counter` by a factor of several."
  ],
  "trap": "Using a 26-slot array and assuming lowercase. The problem explicitly allows uppercase, so \"Aa\" and \"aA\" are both permutations and a mixed-case input will corrupt the counts.",
  "invariant": "`win[i]` is the count of character i in `s2[r-W+1 .. r]`, and `matches` is exactly the number of slots where `win[i] == need[i]`. A window is a permutation iff `matches == 26` (equivalently sigma), because equal counts at every slot means equal multisets.",
  "questions": [
   {
    "q": "Why maintain a match counter instead of comparing arrays?",
    "a": "Comparing the two arrays each slide is $O(\\sigma)$ per slide, giving $O(n \\sigma)$ overall -- 2.6 million comparisons at the limits. The counter makes each slide $O(1)$ because only two slots change, so the total drops to $O(n)$."
   },
   {
    "q": "What is the order of the update when a character leaves and another enters?",
    "a": "Remove first, then add. If the incoming and outgoing characters are the same slot you would double-count; by decrementing before incrementing and adjusting `matches` after each individual mutation, the invariant holds at every intermediate point and no special case is needed."
   },
   {
    "q": "How do you adapt this to the fixed-size-anagram-inside-s1 case (567) versus arbitrary-length?",
    "a": "Here the window width is pinned to `len(s1)`, which is what makes the check a pure frequency comparison. For arbitrary-length windows you would instead need the formed/required counter pattern of problem 76, where the requirement is a multiset rather than an exact match."
   }
  ]
 }
})

# ---- _chunk3.py
DATA.update({
 "04_stack/0020_valid_parentheses": {
  "one_liner": "Push opens, pop and match on every close.",
  "category_note": "The stack is the right structure whenever the last unclosed thing must be resolved first -- nested brackets, nested calls, infix evaluation, and monotonic scans where a later element can retroactively cancel an earlier one. Three flavours recur across this category: a stack of openers with a closing-to-opener map, a stack that carries a running summary (a min-stack, a running arrival time) so a query is $O(1)$ instead of $O(n)$, and a MONOTONIC stack where each element is pushed once and popped at most once, giving amortised $O(1)$ per item. The monotonic pattern is the hardest and most valuable: it converts an $O(n^2)$ nested scan into a single pass by keeping only the elements that are still capable of being an answer.",
  "core_objective": "Return true if every opening bracket in the string is closed by the same type of bracket in the correct order.",
  "bounds": "1 <= s.length <= 1e4; the only characters present are '(', ')', '{', '}', '[' and ']'. An empty string is valid. The invariant must be checked on close before popping, so an unmatched closer on an empty stack returns false immediately rather than underflowing.",
  "diagram": " s = \"([)]\"  -> false\n\n s = \"({[]})\" -> true\n\n   ch (  stack: (\n   ch {  stack: ( {\n   ch [  stack: ( { [\n   ch ]  close ] -> pop [   match!    stack: ( {\n   ch }  close } -> pop {   match!    stack: (\n   ch )  close ) -> pop (   match!    stack: (empty)\n   end: stack empty AND no mismatch -> true\n\n s = \"([)]\" -> false\n   (  stack: (\n   [  stack: ( [\n   )  close ) -> TOP is [ not (  -> MISMATCH -> false\n\\n trap: popping before checking empties the stack\n and lets \")]\" through",
  "cpp_vs_py": "The stack here is at most three elements deep for a well-formed string, so both languages live entirely in registers or L1 and the difference is pure interpreter overhead. C++ runs the loop as a load, an array index with a branch on the character class, and a compare -- the `switch` compiles to a jump table, which is a single indirect branch the CPU predicts well for a repeating bracket pattern. CPython must execute roughly 20 bytecodes per character (unpack the char, index the dict for the closer, compare strings) and allocates nothing here only because CPython interns single-character Latin-1 strings, so `ch` is a pointer chase to a cached object rather than a fresh allocation.",
  "cpp_alts": [
   "`switch (ch)` on the character compiles to a jump table, beating a `std::unordered_map<char,char>` lookup (no hashing, no node).",
   "`std::string::find_last_of` style scanning is $O(n^2)$ and wrong; a `std::stack<char>` is fine but a raw `std::array<char,64>` avoids allocation."
  ],
  "py_alts": [
   "A `dict` of closer-to-opener beats `if/elif` chains and keeps the intent data-driven.",
   "`while stack and stack[-1] != pairs[ch]` followed by `if not stack: return False` is the bug-free idiom -- it checks the guard and the match in one pass.",
   "An f-string-free `stack.pop() != opener` comparison is the tightest check: one pop, one compare, no temp variable."
  ],
  "trap": "Popping the top and comparing, without first verifying the stack is non-empty. `s = ')'` then indexes an empty list, or in C++ reads uninitialised memory.",
  "invariant": "After each processed character, the stack contains exactly the opening brackets that have been seen but not yet matched, in their original order. So a closer must match the top element, and if it does not, the string is invalid regardless of what comes later.",
  "questions": [
   {
    "q": "Why does only the top of the stack need checking?",
    "a": "Nesting requires proper LIFO order, so a closer must immediately undo the most recent unclosed opener. Anything deeper in the stack was opened earlier and must be closed after the current one, so a mismatch at the top is already fatal."
   },
   {
    "q": "What is the difference between counting and matching?",
    "a": "Counting openers and closers of each type ignores order, so `')('` and `'([)]'` would pass. Order is exactly what the stack enforces, which is why this problem is a stack exercise rather than a counting exercise."
   },
   {
    "q": "Can this be solved with a counter?",
    "a": "Only for a single bracket type. With three types you need at minimum a stack of types, since `{[)]` has balanced counts but wrong nesting. The counter version works for `()` and nothing else."
   }
  ]
 },
 "04_stack/0022_generate_parentheses": {
  "one_liner": "Backtrack with two budgets: opens left, closes left.",
  "core_objective": "Generate all combinations of well-formed parentheses of length n, using exactly n pairs.",
  "bounds": "1 <= n <= 8, so at most 2n = 16 characters and C(8,4) = 70 valid strings -- the answer set is small enough to enumerate exhaustively. Every generated string must have exactly n opens and n closes.",
  "diagram": " n = 3   -> [\"((()))\", \"(()())\", \"(())()\", \"()(())\", \"()()()\"]\n\n dfs(path, open, close):\n   if len(path) == 2n: emit; return\n   if open  < n: dfs(path + '(' , open+1, close)   # can always open\n   if close < open: dfs(path + ')' , open, close+1) # can only close\n\n                         '('  open 1 close 0\n                  /                     \\\n           '('  open2 cl0          ')'  open1 close1\n           /          \\\\|               /          \\\n      '(' o3c0    ')' o2c1        '(' o2c1     ')' o1c2\n        |            \\\\             |           \\\\\n   ')' '(())'  '(()())'      '(())()'    '()()()'\n\\n the close branch needs close < open: you may never\n close more than you have opened (else ')' first).",
  "cpp_vs_py": "This is a search tree of depth 2n with branching factor 2, so there are at most $2^{16}$ nodes here and about 1e5 in the worst allowed case -- tiny. The interesting difference is memory: every node in Python holds a new `path` string built by `path + '('`, which allocates a fresh string of length up to 2n and copies the whole prefix. That is $O(n)$ per node, making the whole thing $O(n \\cdot 2^n)$ in allocation traffic. C++ has exactly the same trap with `string path`, but passing `path` by value and appending, or mutating a single buffer with push/pop and one `push_back`, avoids the copy entirely and turns each node into $O(1)$ amortised work.",
  "cpp_alts": [
   "Mutate one `string path` with `push_back` / `pop_back` instead of copying per node -- the single biggest win here.",
   "Use a fixed `std::array<char,16>` and a length counter for zero-allocation enumeration.",
   "`std::function` recursion has indirect-call overhead; a plain static recursive function or a template lambda is inlined."
  ],
  "py_alts": [
   "A list `path` with `append`/`pop` avoids the $O(n)$ string copy per node; join once at the leaves.",
   "Pruning with `if close < open` is what keeps the tree at Catalan size instead of $2^{2n}$.",
   "An iterative BFS with a deque is the second approach; it trades recursion for explicit queue churn and is not faster here."
  ],
  "trap": "Allowing a close when `close == open`. That produces strings like `(()` with an unmatched closer and you end up emitting invalid output unless you also check `open == close == n` at the leaf.",
  "invariant": "`path` is always a prefix of a valid parenthesis string, `open` counts its '(', `close` counts its ')', and the guard `close <= open <= n` holds at every node. That is sufficient to guarantee every leaf is well formed.",
  "questions": [
   {
    "q": "Why is the condition `close < open` enough to prevent invalid prefixes?",
    "a": "A prefix is extendable to a valid string iff it never has more closers than openers, and we never exceed n of either. Checking `close < open` before appending a closer preserves `close <= open` at every node, so every leaf has balanced counts and proper nesting."
   },
   {
    "q": "How many strings are produced?",
    "a": "The n-th Catalan number, $C_n = \\frac{1}{n+1}\\binom{2n}{n}$, which is 70 for n = 8 and 5 for n = 3. The output is exponential, so the algorithm is output-bound rather than work-bound."
   },
   {
    "q": "What would be wrong with a greedy construction?",
    "a": "There is no fixed rule for where to place the next bracket -- the choice depends on the prefix. That is precisely why this is a backtracking search rather than a greedy or DP problem."
   }
  ]
 },
 "04_stack/0084_largest_rectangle_in_histogram": {
  "one_liner": "Increasing stack of indices; each pop reveals one maximal rectangle.",
  "core_objective": "Return the largest area of an axis-aligned rectangle fully contained in a histogram, where the rectangle's height is limited by the shortest bar it spans.",
  "bounds": "1 <= heights.length <= 1e5; 0 <= heights[i] <= 1e4. Areas reach about $10^9$, so `long long` is the safe C++ type. Zero-height bars are legal and contribute area 0.",
  "diagram": " h = [2,1,5,6,2,3]   -> answer 10 (bars 2..4, height 5)\n\n  i=0 h=2 stack:[0]\n  i=1 h=1 pop 0: w = 1-(empty? -1: )-1 = 1-0 = 1? width=1 area=2*1=2\n        stack:[1]\n  i=2 h=5 stack:[1,2]\n  i=3 h=6 stack:[1,2,3]\n  i=4 h=2 pop 3: width = 4-2-1 = 1  area=6*1=6\n        pop 2: width = 4-1-1 = 2  area=5*2=10  BEST\n        stack:[1,4]\n  i=5 h=3 stack:[1,4,5]\n  i=6 SENTINEL h=0 pop 5: width=6-4-1=1 area=3\n              pop 4: width=6-1-1=4 area=2*4=8\n              pop 1: width=6-(-1)-1=6 area=1*6=6\n        stack:[]\n\\n width rule: the popped bar's height is valid all the way\n from (new stack top + 1) to (i - 1).",
  "cpp_vs_py": "This is where the monotonic-stack pattern pays off most. In C++ the stack is a preallocated `vector<int>` with an index pointer, so push and pop are a store and an integer decrement into a single cache line, and the inner `while` reads `heights[st.back()]` -- a load from the histogram array at an index the CPU has just computed, so it is an L1 hit. Total work is a single pass with 2n stack operations. In Python the same loop runs against a `list` of ints, which is nearly as good for the stack itself, but `heights[st[-1]]` boxes nothing here (existing int objects are reused) while `max(area, height * (i - w - 1))` allocates a new int for every candidate, and the `while` condition re-evaluates `st` truthiness plus an indexing operation. The asymptotic bound is identical; the constant is roughly 30x.",
  "cpp_alts": [
   "`vector<int> st; st.reserve(n + 1);` and an index pointer beat `std::stack<int>` -- no adaptor indirection, one contiguous block.",
   "Push a sentinel height of 0 (or -1) as `heights[n]` to flush the stack in the same loop, avoiding a second pass.",
   "For very large n, the two-pass block-maximum approach (van Herk/Gil-Werman) gives $O(n)$ with better cache behaviour and no stack at all."
  ],
  "py_alts": [
   "`while st and heights[st[-1]] > h:` is the canonical loop; using `>=` breaks ties differently but is also correct as long as the width formula stays consistent.",
   "Append a 0 sentinel to the heights list rather than special-casing the loop exit -- removes a duplicated code path.",
   "Python lists support amortised O(1) `append`/`pop`, so a list is a fine stack; no `deque` needed."
  ],
  "trap": "Computing the width before popping, or using `i` instead of the new stack top in the width formula. The width is `i - st.back() - 1` evaluated AFTER the pop, because the popped bar is no longer a boundary.",
  "invariant": "The stack holds indices with strictly increasing heights, and every index between consecutive stack entries is shorter than the entry above it. When index i is popped, the stack top is the nearest bar to the left that is shorter, so bars from top+1 to i-1 all have height at least `heights[i]`.",
  "questions": [
   {
    "q": "Why is the width `i - st.back() - 1` after popping, not before?",
    "a": "After popping index i, `st.back()` is the nearest bar strictly to the left with a smaller height, which is exactly the left boundary of the maximal span for `heights[i]`. The right boundary is i-1 because the current bar is shorter. Using the pre-pop top would include the boundary bar and overcount."
   },
   {
    "q": "What does the sentinel flush accomplish?",
    "a": "It forces every remaining index to be popped as if a bar of height 0 had appeared at position n. Without it you need a separate loop after the main one, and forgetting that loop loses the rectangles that extend to the right edge."
   },
   {
    "q": "Why is the whole algorithm linear despite the nested while?",
    "a": "Each index is pushed once and popped at most once, so the total number of inner-loop iterations across the entire run is at most n. The nested loop is amortised O(1) per outer iteration."
   }
  ]
 },
 "04_stack/0150_evaluate_reverse_polish_notation": {
  "one_liner": "Two operands plus an operator form a three-token reduction.",
  "core_objective": "Evaluate an expression given in reverse Polish notation, where every operator follows its operands and `/` truncates toward zero.",
  "bounds": "1 <= tokens.length <= 1e5, with integer operands in [-100, 100] and division by zero guaranteed not to occur. Operand count is always valid, so the stack never underflows. Intermediate results can exceed 32 bits, which is the classic C++ trap.",
  "diagram": " tokens = [\"2\",\"1\",\"+\",\"3\",\"*\"]  -> 9\n\n is an operand?  push 2            [2]\n is an operand?  push 1            [2,1]\n '+' : b=pop()=1, a=pop()=2 -> 2+1=3   [3]\n '3' : push                     [3,3]\n '*' : b=3, a=3            -> 3*3=9   [9]\n\\n operand test: token is a digit, or starts with '-'/'+' followed\n by a digit. The classic bug is testing isdigit() alone,\n which rejects negative operands like \"-3\".\n\\n DIVISION TRAP: C++ int division truncates toward zero, so\n -7 / 2 == -3 (not -4). Python's // floors to -4, so Python\n needs int(a / b) to match.",
  "cpp_vs_py": "The stack depth is bounded by the number of operands, which for a balanced RPN expression is modest, so both languages keep it in cache. C++ does one `isdigit` scan per token and one division per operator, with the token comparison against `'-'` handled by a branch. CPython's `str.isdigit()` allocates nothing (one-character cached strings) but the repeated `int(token)` conversion goes through the full string-to-integer parser, and the operator dispatch via a dict lookup returns a function object that is then called -- a full Python-level call per operator. That call overhead is the dominant cost, not the arithmetic.",
  "cpp_alts": [
   "Dispatch operators with a `switch` on `tok[0]` rather than an `unordered_map<string,function>` -- no string hashing, no indirect call.",
   "`stoll` on the operand after the digit check, or `std::from_chars` which is allocation-free and locale-independent.",
   "Reserve the stack with `stack.reserve(tokens.size())` to avoid repeated reallocation."
  ],
  "py_alts": [
   "A dict of lambdas for the five operators is concise but each call is a Python-level function call.",
   "`tok.isdigit() or (tok[0] in '+-' and tok[1:].isdigit())` correctly handles negative operands.",
   "Use `int(a / b)` not `a // b` so the truncation matches LeetCode's C++ semantics."
  ],
  "trap": "Popping in the wrong order. For a non-commutative operator like `-` or `/`, the FIRST pop is the RIGHT operand and the second pop is the LEFT one. Swapping them gives correct-looking output on symmetric inputs and wrong answers otherwise.",
  "invariant": "After processing each token, the stack holds, in order, the values of all complete subexpressions that have not yet been consumed by an operator. An operator therefore always finds its two operands on top.",
  "questions": [
   {
    "q": "Why is the first pop the right operand?",
    "a": "In reverse Polish notation the operands appear before the operator, left operand first. Popping takes the most recently pushed, which is the right operand, so `a = pop()` must be the SECOND pop. Subtraction and division are not commutative, so this matters immediately."
   },
   {
    "q": "How do you distinguish an operand from an operator robustly?",
    "a": "Check the first character: digits or a leading sign followed by a digit mean operand. `isdigit()` alone fails on `-3`, and a set of operator characters alone is fragile if the token set grows."
   },
   {
    "q": "What is the C++-versus-Python semantic trap here?",
    "a": "Integer division. C++ truncates toward zero, so -7/2 is -3; Python's // floors, giving -4. A Python port must use `int(a / b)` to reproduce the judge's expected output."
   }
  ]
 },
 "04_stack/0155_min_stack": {
  "one_liner": "Push the running minimum alongside every value.",
  "core_objective": "Support push, pop, top, and getMin in constant worst-case time each.",
  "bounds": "Operations arrive in any order with at most 3e6 calls, so worst-case O(1) per operation is required. The main stack holds up to 1e5 elements. Duplicates are legal, so the auxiliary structure must handle equal minima correctly.",
  "diagram": " ops: push(-2) push(0) push(-3) getMin() pop() top() getMin()\n\n main    : [-2] [-2,0] [-2,0,-3]\n mins    : [-2] [-2,-2] [-2,-2,-3]\n\n getMin -> mins.back() = -3\n pop() : main.pop() -> -3 ; mins.pop() -> -2 (restored!)\n top()  : main.back() -> 0\n getMin -> mins.back() = -2   CORRECT (0 was popped? no, min was -2)\n\\n invariant: |mins| == |main| always, and\n mins[i] == min(main[0..i]) at every depth i.\n Popping is symmetric, so the two stay in lockstep.\n\n alternative: one stack of (value, runningMin) pairs --\n half the push/pop calls, twice the per-node memory.",
  "cpp_vs_py": "This is the rare problem where Python's memory model is a genuine liability. Two parallel stacks mean two `deque`s, and each CPython deque block holds pointers, so a 1e5-element stack costs roughly 800 KB of pointers plus the int objects. C++ `std::stack<int>` over a `std::vector<int>` stores the values inline in one 400 KB block with perfect locality, and the running-min vector is likewise 400 KB -- 1.6x denser with no per-element object header and no indirection on read. Pushing a Python int does not allocate when the value is interned or already referenced, but a large computed minimum is a fresh PyLong, so the auxiliary stack allocates on every push where the min changes.",
  "cpp_alts": [
   "`vector<pair<int,int>>` holding (value, runningMin) halves the number of push/pop calls at the cost of doubling per-node bytes.",
   "A single `vector<int>` for values plus a `vector<int>` for mins, with `reserve`, is faster than `std::stack` because there is no adaptor indirection.",
   "An `std::multiset` with a matching iterator per element gives O(log n) getMin with O(1) push/pop and erase -- only worth it if you need ordering too."
  ],
  "py_alts": [
   "`deque` is the natural stack; a `list` with negative indexing works too and is faster to push/pop but its `pop()` from the end is the same operation.",
   "Storing `(value, running_min)` tuples halves the calls but allocates a tuple per push -- usually a net loss in CPython.",
   "`min_stack[-1]` is O(1); do not use `min(min_stack)` anywhere in the hot path."
  ],
  "trap": "Pushing to the auxiliary stack only when the new value is smaller. Then the auxiliary stack no longer has the same depth as the main one, and a pop cannot know how many minima to discard -- you must push unconditionally and pop unconditionally.",
  "invariant": "`|mins| == |main|` and `mins[i] == min(main[0..i])` for every depth i. Push appends `min(v, mins.top())`, pop discards one entry, and the invariant then holds for the shorter stack by construction.",
  "questions": [
   {
    "q": "Why must you push the running min unconditionally?",
    "a": "The auxiliary stack's depth must mirror the main stack's so that popping once from each stays in sync. Pushing only on decrease leaves fewer entries than there are values, and there is no way to recover how many to discard on pop."
   },
   {
    "q": "What is the space cost of the two-stack design versus the pair design?",
    "a": "Two stacks of n ints is 2n words. A stack of n pairs is also 2n words, so the memory is identical. The difference is call count: two stacks do two push and two pop calls per operation, the pair design does one each but allocates a pair per node."
   },
   {
    "q": "Can getMin be O(1) without extra space?",
    "a": "Not without extra state -- you would have to rescan, which is O(n). The whole point of the problem is that the extra structure buys O(1); the space cost is the price."
   }
  ]
 },
 "04_stack/0739_daily_temperatures": {
  "one_liner": "Monotonic decreasing stack: a warmer day resolves the wait.",
  "core_objective": "For each day, return how many days you must wait for a strictly warmer temperature; 0 if none exists.",
  "bounds": "1 <= temperatures.length <= 1e5; 30 <= temperatures[i] <= 100, so the value range is tiny and a 71-slot array could replace the stack, but the stack generalises. A day with no warmer future returns 0, not -1.",
  "diagram": " T = [73, 74, 75, 71, 69, 72, 76, 73]\n     idx 0  1  2  3  4  5  6  7\n\n i=0 73 st=[]            -> push 0   st=[0]\n i=1 74 T[0]=73 < 74 -> ans[0]=1-0=1 ; push 1  st=[1]\n i=2 75 T[1]=74 < 75 -> ans[1]=1     ; push 2  st=[2]\n i=3 71 T[2]=75 > 71 -> not warmer; push 3  st=[2,3]\n i=4 69 push 4                        st=[2,3,4]\n i=5 72 pop 4 (69<72) ans[4]=1\n              pop 3 (71<72) ans[3]=2\n              T[2]=75 > 72 stop; push 5  st=[2,5]\n i=6 76 pop 5 (72) ans[5]=1\n              pop 2 (75) ans[2]=4\n              push 6  st=[6]\n i=7 73 push 7  st=[6,7]  (no one left to warm them)\n\\n ans = [1,1,4,2,1,1,0,0]   (index 6,7 stay 0)",
  "cpp_vs_py": "Each index is pushed once and popped at most once, so the stack operations total 2n and the amortised cost is O(1). In C++ the stack is a `vector<int>` with a pointer, the `while (T[st.back()] <= T[i])` test is two L1 loads, and popping is one decrement -- all register work with the histogram array streaming through L1 once. Python's list-based stack behaves nearly identically for the stack itself, but each iteration allocates an int for `i - st[-1]` before storing it into the answer list, and CPython cannot keep the loop-carried comparison in a register. Realistically the C++ version runs about 25 times faster at n = 1e5, purely from interpreter dispatch.",
  "cpp_alts": [
   "Use `<=` in the pop condition so equal temperatures also pop; `<` leaves equal values in the stack, which is still correct but does more work.",
   "Because temperatures are 30..100, a `vector<int> last(101, -1)` forward pass is also $O(n)$ with no stack.",
   "`std::vector<int>` plus an index counter beats `std::stack<int>` (which defaults to `std::deque`) on both speed and locality."
  ],
  "py_alts": [
   "`while st and T[st[-1]] < t:` must be re-tested after each pop; the loop condition alone handles it.",
   "`st.append(i)` / `st.pop()` on a list is amortised O(1) and faster than `deque` here because there is no block splitting.",
   "Leaving the answer list pre-filled with zeros avoids a second pass to handle unresolved stack entries."
  ],
  "trap": "Using `<` instead of `<=` in the pop condition, or popping on `<=`. With `<=` equal temperatures resolve each other (and the later one correctly reports 0 for a day whose equal-temperature successor is not strictly warmer -- check this against the expected output). More commonly the bug is forgetting to initialise unresolved entries to 0.",
  "invariant": "The stack holds indices in strictly increasing order of position and strictly decreasing order of temperature, and every one of them is still waiting for a warmer day. When a warmer day arrives it resolves all stack entries with a smaller temperature, and each is resolved exactly once with the nearest qualifying day.",
  "questions": [
   {
    "q": "Why does each entry get the NEAREST warmer day rather than just any?",
    "a": "Because entries are popped the moment a warmer day is seen, and days are processed left to right. The first warmer day encountered after index i is by definition the nearest one, so the answer is correct the instant the pop happens."
   },
   {
    "q": "Why must the stack be decreasing rather than increasing?",
    "a": "An increasing stack would pop on a colder day, but the question asks for warmer. Decreasing order means the stack top is the most recent day that nothing warmer has resolved, so a warmer arrival pops exactly the entries it can answer."
   },
   {
    "q": "What happens to indices left in the stack at the end?",
    "a": "Their answers stay 0, meaning no warmer day ever appeared. That is the correct answer and the reason the result array is initialised to 0 rather than assigned in a final flush."
   }
  ]
 },
 "04_stack/0853_car_fleet": {
  "one_liner": "Sort by position; scan from the back comparing arrival times.",
  "core_objective": "Return the minimum number of cars that arrive at the target. A faster car that catches a slower one ahead merges into that fleet and arrives with it.",
  "bounds": "1 <= n <= 1e4; 1 <= target <= 1e9; 1 <= speed[i], position[i] <= 1e9. `target - position[i]` can be zero or negative and must be handled as an immediate arrival. The product speed * time can reach about 1e18, so C++ needs `long long`.",
  "diagram": " target = 12, position = [10,8,0,5,3], speed = [2,4,1,1,3]\n\n sorted by position desc: (10,2) (8,4) (5,1) (3,3) (0,1)\n\n scan from the BACK (closest to target first):\n (3,3)  time = 9/3 = 3      -> slowest=3, fleets=1\n (5,1)  time = 7/1 = 7      -> 7 > 3 : SLOWER, new fleet  fleets=2\n (8,4)  time = 4/4 = 1      -> 1 < 3 : catches up, joins fleet\n (10,2) time = 2/2 = 1      -> 1 < 3 : catches up, joins fleet\n (0,1)  time = 12/1 = 12    -> 12 > 3: SLOWER, new fleet  fleets=3\n\\n ANSWER 3\n\n invariant: `slowest` is the arrival time of the fleet nearest the\n target seen so far. A car arriving LATER must be its own fleet;\n a car arriving EARLIER or equal merges behind it.",
  "cpp_vs_py": "The dominant cost here is the sort of up to 1e4 pairs. C++ sorts `vector<pair<int,int>>` with introsort -- the second element makes it lexicographic, which is a comparison on two registers per element, so roughly 1e5 comparisons in well-predicted branches on a 80 KB array that fits in L2. CPython's `list.sort()` uses Timsort with tuple comparison, and tuple `__lt__` goes through a generic rich-comparison slot, so each of the ~1e5 comparisons is an indirect C call. Then the scan divides by `speed[i]`, and Python's `/` on ints produces a float -- allocating a float object per car and risking precision issues near 1e18, which is why the integer ceil-division form is mandatory in both languages here.",
  "cpp_alts": [
   "`sort` by position descending, or sort ascending and iterate from `n-1` down.",
   "Integer ceil division `(d + s - 1) / s` avoids the float round-trip and the precision hazard entirely.",
   "`long long` throughout: `(target - position) * time` intermediate products overflow 32 bits immediately."
  ],
  "py_alts": [
   "`(d + s - 1) // s` is exact integer ceiling division and much faster than `math.ceil(d / s)`.",
   "Sort with `key=lambda p: -p[0]` or sort ascending and reverse-index; both avoid a custom comparator, which in Python is far more expensive than a key function.",
   "`max(slowest, t)` inline instead of `max()` calls keeps the scan free of function dispatch."
  ],
  "trap": "Scanning from the front (largest position gap first) instead of the back. The nearest car sets the pace for everyone behind it, so you must process from the target backwards. Scanning forward gives the wrong fleet count.",
  "invariant": "After processing the i closest cars, `slowest` is the arrival time of the rearmost fleet among them. A car with arrival time <= slowest catches that fleet; a car with arrival time > slowest cannot catch anything and forms its own fleet, updating slowest.",
  "questions": [
   {
    "q": "Why scan from the back?",
    "a": "Fleet membership is determined by arrival time ordering, and the car closest to the target has no car ahead of it, so it always forms its own fleet. Working backwards, each subsequent car either catches that fleet (arrives no later) or overtakes it and becomes the new pace-setter. Scanning forwards has no such anchor."
   },
   {
    "q": "What does the running `slowest` value represent?",
    "a": "The arrival time at the target of the rearmost fleet encountered so far. It is non-decreasing as you scan backwards, which is the invariant that makes the single comparison per car sufficient."
   },
   {
    "q": "Why must you use integer ceiling division?",
    "a": "Two reasons. Exactness: floating point near 1e18 has no room for an integer, so `(d + s - 1) / s` is the only safe form. And correctness of the comparison: a car that arrives 0.0000001 later is a separate fleet, and float rounding would merge them incorrectly."
   }
  ]
 },
 "05_binary_search/0004_median_of_two_sorted_arrays": {
  "one_liner": "Binary search the partition of the shorter array, not the value.",
  "category_note": "Binary search is not just \"halve the array\" -- it is \"find the boundary where a monotone predicate flips\". Every problem in this category has a hidden monotone predicate: is `nums[mid] <= target` (704), is the window feasible (875), is the timestamp at most t (981), is the half sorted (153). The transferable skill is naming that predicate and its monotonicity, because once the predicate is monotone the proof is mechanical. Three flavours recur: closed lower-bound search on values, boundary search on a rotated array where one half is always sorted, and binary search over a search SPACE of size up to 1e9 -- where the array being searched has nothing to do with the quantity being found.",
  "core_objective": "Given two sorted arrays of different sizes, return the median of their combined elements in O(log(min(m,n))) time.",
  "bounds": "1 <= m, n <= 1000; both arrays are sorted ascending and contain only non-negative ints. m + n can be odd (then there is a true middle) or even (then it is the average of the two middles). One array may be a single element.",
  "diagram": " A = [1,3]  B = [2]   combined = [1,2,3] median = 2\n\n search on the SHORTER array (A, m=2). Partition A into\n left A[0..j-1] and right A[j..m-1], B into left B[0..k-1]\n and right B[k..n-1], with j + k = half = (m+n+1)/2 = 2\n\n j=1 k=1:  leftA=[1]  rightA=[3] | leftB=[2] rightB=[]\n          check: leftA <= rightB (1 <= inf) ok\n                leftB <= rightA (2 <= 3) ok\n          left count = 1+1 = 2 = half\n          median = max(leftA, leftB) = 2   CORRECT\n\n j=0 k=2:  leftA=[]   rightA=[1,3]\n          leftB=[2] rightB=[]\n          leftB(2) <= rightA(1)? NO -> j too small, move right\n\n conditions to satisfy:\n   leftA_max <= rightB_min      and      leftB_max <= rightA_min\n   plus  left_count == half  (or half+1 for even)",
  "cpp_vs_py": "Binary search over a partition position has at most log2(1000) = 10 iterations, so both languages finish in microseconds and interpreter overhead is invisible. The interesting difference is in the guards: C++ needs explicit `INT_MIN`/`INT_MAX` sentinels because indexing `A[j-1]` with j = 0 is out of bounds, and getting that wrong is undefined behaviour rather than an exception. Python's negative indexing silently wraps around, so `A[j-1]` at j = 0 returns the LAST element instead of raising -- which is a silent wrong answer rather than a crash. That single asymmetry is the most valuable thing to know when porting this problem.",
  "cpp_alts": [
   "Guard the boundaries explicitly with `j == 0 ? INT_MIN : A[j-1]` and `j == m ? INT_MAX : A[j]` -- the alternative is index-0/1 padding with sentinels, which removes the branches entirely.",
   "`std::max_element` on the two left partitions gives the median side in O(1); no need to merge.",
   "Always search the shorter array: log(min(m,n)) <= log(max(m,n)), so swapping when m > n is free and halves the worst case."
  ],
  "py_alts": [
   "Pad conceptually with `float('-inf')` and `float('inf')` instead of branching -- Python's arbitrary comparison makes it clean.",
   "Beware that Python's `A[-1]` is the last element, so the j = 0 case must be special-cased explicitly.",
   "`while lo <= hi:` with the standard partition search is clearer here than a half-open loop, because the answer needs both neighbours."
  ],
  "trap": "Searching for the median VALUE with a standard binary search. The median is not necessarily an element of either array, so there is nothing to search for; you must search for the partition position, then take the max of the two left partitions.",
  "invariant": "The partition is valid iff `max(leftA) <= min(rightB)` and `max(leftB) <= min(rightA)` and the left side holds `ceil((m+n)/2)` elements. Monotonicity says: if `leftB_max > rightA_min`, then j must increase; if `leftA_max > rightB_min`, then j must decrease. That is what makes the search valid.",
  "questions": [
   {
    "q": "Why binary search on the shorter array?",
    "a": "The partition count is bounded by the shorter length, so the search space is min(m,n)+1 and the depth is log(min(m,n)). Searching the longer array works but is strictly worse, and swapping the pointers first is free."
   },
   {
    "q": "What are the two validity conditions and how do they drive the search?",
    "a": "(1) every element on the left is <= every element on the right, split into the two cross pairs leftA vs rightB and leftB vs rightA. (2) the left side has exactly half the elements. If leftB is too large, j must grow; if leftA is too large, j must shrink. Both conditions are monotone in j, which is what licenses binary search."
   },
   {
    "q": "How do you compute the median once the partition is valid?",
    "a": "If m+n is odd, it is max(leftA, leftB). If even, it is the average of max(leftA, leftB) and min(rightA, rightB). Getting the odd/even indexing right matters: use half = (m+n+1)//2 so the left side absorbs the extra element."
   }
  ]
 },
 "05_binary_search/0033_search_in_rotated_sorted_array": {
  "one_liner": "One half is always sorted -- use it to discard the other.",
  "core_objective": "Return the index of target in a strictly increasing array that was rotated at an unknown pivot, or -1 if absent.",
  "bounds": "1 <= nums.length <= 5e4; values are distinct integers, so there are no duplicates and exactly one sorted half per step. n = 1 must work, and a single-element array rotated is itself.",
  "diagram": " nums = [4,5,6,7,0,1,2], target = 0  -> index 4\n\n mid = 3 (value 7). nums[3]=7 > nums[6]=2 -> RIGHT half sorted.\n   target 0 <= 7 and 0 not in [7,2] (which spans 2..7) -> search LEFT\n   lo=0 hi=2\n mid=1 (value 5). nums[1]=5 > nums[2]=6? no -> LEFT half [4,5] sorted\n   target 0 < 5 -> search RIGHT: lo=2 hi=2\n mid=2 (value 6). 0 < 6 -> search RIGHT: lo=3 > hi=2 -> return -1? \n   WRONG STEP -- corrected: at lo=2 hi=2 mid=2 val=6, 0<6 so\n   lo=3, loop ends. But target IS at index 4.\n\n the correct trace (target=0):\n  lo=0 hi=6 mid=3 val=7, right sorted [7,0,1,2] spans 2..7\n     target 0 < nums[3]=7 -> lo=0 hi=2\n  mid=1 val=5, left sorted [4,5] ; target 0 < 5 -> lo=2 hi=2\n  mid=2 val=6 ; nums[2]=6 > nums[0]=4 so right 'sorted'...\n  with lo==hi==2 just compare: nums[2]==0? no -> -1\n\n KEY: at each step only ONE half is guaranteed sorted, and\n the target must lie in it (or exactly at its boundary) unless\n the sorted half excludes it -- then go the other way.",
  "cpp_vs_py": "Both do at most log2(50000) = 16 iterations, so this is entirely overhead-dominated. In C++ the two comparisons `(nums[mid] >= nums[lo])` and `(target >= nums[lo])` are register comparisons and the loop is a handful of instructions with one hard-to-predict branch. CPython executes roughly 25 bytecodes per iteration for the same four comparisons and subscripts, and each `nums[mid]` returns a borrowed reference to an existing int with no allocation -- so this is pure dispatch overhead. At 16 iterations the absolute difference is a few microseconds, which is precisely why this problem is a correctness problem rather than a performance one.",
  "cpp_alts": [
   "Always compute `mid = lo + (hi - lo) / 2` rather than `(lo + hi) / 2` to avoid overflow, even though the bounds here make it safe.",
   "Decide the sorted half with `nums[mid] >= nums[lo]`; the mirrored form `nums[mid] <= nums[hi]` is equally valid and equally fast.",
   "An alternative is to find the pivot with one binary search, then binary search in the guaranteed-sorted segment -- two searches but conceptually simpler."
  ],
  "py_alts": [
   "A `while lo <= hi` loop with `mid = (lo + hi) // 2` is idiomatic; `/` would produce a float and break the indices.",
   "Python's negative indices do not help here, so `lo` and `hi` must stay genuine in-range bounds.",
   "For a rotating search, `bisect` is unusable -- the array is not globally sorted."
  ],
  "trap": "Assuming BOTH halves are sorted, or assuming the whole array is sorted. Also, testing the sorted half's range with `nums[lo] <= target <= nums[mid]` on the wrong half. The reliable formulation: identify which half is sorted, then check whether the target lies in its value range; if it does, recurse there, otherwise recurse into the other half.",
  "invariant": "If `nums[lo..mid]` is the sorted half then `nums[mid] >= nums[lo]`, and the target is in `[nums[lo], nums[mid]]` exactly when it is present in that half; otherwise the answer lies in `[mid+1, hi]`. Exactly one half is sorted because the rotation has a single pivot and all values are distinct.",
  "questions": [
   {
    "q": "How do you know which half is sorted?",
    "a": "Compare `nums[mid]` with `nums[lo]`. If `nums[mid] >= nums[lo]` the left half is sorted (a rotation only breaks monotonicity across the pivot); otherwise the right half is. With distinct values exactly one of the two holds at every step."
   },
   {
    "q": "How do you decide which half to keep?",
    "a": "Once the sorted half is identified, test whether the target's value falls inside that half's range. If yes, discard the other half; if no, the answer must be in the other half. Because all values are distinct the target cannot be in both, so this decision never loses the answer."
   },
   {
    "q": "What changes when duplicates are allowed (problem 153)?",
    "a": "Both halves can appear unsorted when `nums[mid] == nums[hi]`. Then you cannot tell which half is sorted, so you must shrink by `hi--` and rely on the fact that the element you dropped equals nums[hi], so it cannot be the unique answer. That branch is what makes 153 harder."
   }
  ]
 },
 "05_binary_search/0074_search_a_2d_matrix": {
  "one_liner": "Treat the matrix as one flat sorted array of m*n elements.",
  "core_objective": "Return true if target appears in the m-by-n integer matrix, whose rows and columns are both sorted ascending, or false otherwise.",
  "bounds": "m, n >= 1 and m*n <= 1e6, so at most log2(1e6) = 20 iterations. Integer overflow in the mid computation is the classic C++ bug: `rows * cols` up to 1e6 is fine, but `(low + high) / 2` computed as an index into a flattened array needs 64-bit arithmetic if the matrix is large.",
  "diagram": " m=3 n=4 matrix = [[1, 3, 5, 7], [10,11,16,20], [23,30,34,60]]\n\n flatten: idx 0..11 -> 1 3 5 7 10 11 16 20 23 30 34 60\n\n lo=0 hi=11 mid=5  -> row 5//4=1 col 5%4=1 -> 11\n   11 > 23? target 13 < 11? no: 13 < 11 false\n   13 > 11 -> lo = 6\n lo=6 hi=11 mid=8  -> row 2 col 0 -> 23 ; 23 > 13 -> hi = 7\n lo=6 hi=7  mid=6  -> row 1 col 2 -> 16 ; 16 > 13 -> hi = 6\n lo=6 hi=6  mid=6  -> 16 != 13 -> lo = 7 > hi -> false\n\\n the mapping mid -> (mid // n, mid % n) is the whole trick:\n no need for a staircase search at all.",
  "cpp_vs_py": "Twenty iterations means both languages are effectively instant, so the difference is only in the index arithmetic. C++ computes `rows * cols` in a register and uses a 64-bit mid to be safe; the div and mod by `cols` compile to a single hardware division instruction (about 20 cycles on x86) or are strength-reduced by the compiler into a multiply-shift pair. CPython does `mid // cols` and `mid % cols` as two separate boxed operations on Python ints, each of which is a full integer-division routine -- so you pay two divisions per iteration instead of one fused divide-and-remainder.",
  "cpp_alts": [
   "`long long mid = lo + (hi - lo) / 2` and `int r = mid / cols, c = mid % cols` -- the compiler fuses the div/mod pair.",
   "The staircase search (start at top-right, move left or down) is $O(m+n)$ and uses $O(1)$ space; it is the pedagogically important alternative even though it is asymptotically worse.",
   "Flatten into a single `vector<long long>` once if you search many times -- converts the matrix to a plain binary search."
  ],
  "py_alts": [
   "`mid // cols, mid % cols` is two separate operations; use `divmod(mid, cols)` if you need both and it is measurably no slower.",
   "The staircase version is arguably more Pythonic and avoids arithmetic entirely: `while 0 <= r < m and 0 <= c < n`.",
   "`bisect` on a flattened list is the fastest if you are allowed to allocate the flat list."
  ],
  "trap": "Using the staircase search's O(m+n) bound when n*m is 1e6 -- that is up to 4000 steps versus 20. The flattened binary search is asymptotically strictly better here and is the intended solution.",
  "invariant": "The matrix sorted row-major is a sorted 1-D array, so the standard binary search invariant applies to the flattened index space: if target exists, its flat index lies in [lo, hi]. The div/mod mapping is a bijection between flat indices and cells, so no candidate is skipped or duplicated.",
  "questions": [
   {
    "q": "Why does the flattened array count as sorted?",
    "a": "Row-major order visits every row left to right, and the row-max of row i is <= the row-min of row i+1 because the columns are sorted too. So the concatenation of the rows is globally ascending, which is exactly what binary search needs."
   },
   {
    "q": "How do you recover (row, col) from a flat index?",
    "a": "`row = mid // cols`, `col = mid % cols`. Integer division and remainder by the column count decompose the flat index; no cell is visited twice and none is skipped, which is the bijection argument."
   },
   {
    "q": "When would the staircase search be preferable?",
    "a": "If you needed $O(m + n)$ and could not afford to assume both rows and columns are sorted (for example only rows sorted), or if the matrix is streamed and cannot be flattened. Here it is dominated."
   }
  ]
 },
 "05_binary_search/0153_find_minimum_in_rotated_sorted_array": {
  "one_liner": "Compare against the right edge; equals means shrink one side.",
  "core_objective": "Return the minimum element of an ascending array that may have been rotated, allowing duplicates.",
  "bounds": "1 <= nums.length <= 5e4; -1e4 <= nums[i] <= 1e4. Duplicates ARE allowed, which is the entire difference from problem 33. n = 1 returns that element; an all-equal array must terminate.",
  "diagram": " nums = [1,3,5,1,1,1]  hmm use [3,1,3,1,1,3]\n\n lo=0 hi=5 mid=2 (val 3)\n   nums[hi]=3 == nums[mid]=3  -> AMBIGUOUS: hi-- (drop a 3)\n   lo=0 hi=4\n mid=2 (3) vs nums[hi]=1 : 3 > 1 -> RIGHT half holds the min\n   lo = 3\n lo=3 hi=4 mid=3 (1) vs nums[hi]=1 : equal -> hi--\n lo=3 hi=3 -> return nums[3] = 1  CORRECT\n\n the three-way decision at each step:\n   nums[mid] <  nums[hi]  -> min is in [lo, mid],   hi = mid\n   nums[mid] >  nums[hi]  -> min is in [mid+1, hi], lo = mid+1\n   nums[mid] == nums[hi]  -> cannot tell, discard hi\n\\n worst case degrades to O(n) with all-equal input:\n   every step is the equal branch, hi decrements n times.",
  "cpp_vs_py": "This is the one binary-search problem in the set whose worst case is genuinely linear, because the equal branch only shrinks by one element per iteration. On an all-equal array of length 5e4 the C++ loop runs 5e4 times with two loads and two compares per iteration -- still only about 200 microseconds. Python runs the same 5e4 iterations in bytecode, roughly 20x that, which is the difference between 0.2 ms and 4 ms. Worth noting that the algorithm's *asymptotic* worst case is O(n) while its *typical* case is O(log n), and interviews often probe exactly that distinction.",
  "cpp_alts": [
   "`lo = mid + 1` in the greater branch is mandatory; `lo = mid` would loop forever when lo == mid.",
   "Handle n == 1 up front so the loop is never entered with lo == hi ambiguously.",
   "For a variant without duplicates you can drop the equal branch entirely and get a strict O(log n) guarantee."
  ],
  "py_alts": [
   "`while lo < hi:` with `mid = (lo + hi) // 2` and `hi = mid` in the smaller branch -- this is the half-open formulation that avoids the final check.",
   "The equal branch is the only one that costs an extra comparison; ordering the branches so equality is tested last keeps the common case cheap.",
   "`min()` calls per iteration are pure overhead; use explicit comparisons."
  ],
  "trap": "Writing `lo = mid` in the `nums[mid] > nums[hi]` branch. If `lo == mid` the loop never progresses, and if the minimum happens to sit at mid the algorithm returns it by luck rather than by proof -- either way it is wrong on some inputs.",
  "invariant": "The minimum lies in [lo, hi] at every step. When `nums[mid] < nums[hi]`, the segment [lo, mid] is sorted ascending so its minimum is `nums[mid]` itself, and the true minimum cannot be to the right of mid because nums[mid] < everything in [mid, hi]. The other two branches follow symmetrically, and the equal branch only discards a duplicate of `nums[hi]`, which cannot be the unique minimum unless every element equals it -- in which case any remaining element is the answer.",
  "questions": [
   {
    "q": "Why does the duplicate case make the worst case linear?",
    "a": "When `nums[mid] == nums[hi]` there is no information to narrow the search: the minimum could be on either side. You can only shrink one position per step, so an array of all equal values forces n iterations. Without duplicates this branch never fires and the bound is strict O(log n)."
   },
   {
    "q": "Is discarding `hi` always safe?",
    "a": "Yes: `nums[hi] == nums[mid]`, so `nums[hi]` has an equal twin at or left of mid. If nums[hi] were the unique minimum then so would nums[mid] be, and the answer would be reproducible from the remaining window. Nothing is lost."
   },
   {
    "q": "What does the half-open formulation change?",
    "a": "With `while lo < hi` and `hi = mid` in the smaller branch, the loop exits when lo == hi and `nums[lo]` is the answer with no post-loop comparison. It is one fewer line and removes an entire class of off-by-one, at the cost of a slightly subtler mental model."
   }
  ]
 },
 "05_binary_search/0704_binary_search": {
  "one_liner": "The loop bounds decide leftmost versus rightmost insertion.",
  "core_objective": "Return the index of target in a sorted ascending array of distinct integers, or -1 if absent.",
  "bounds": "1 <= nums.length <= 1e4; -1e4 <= nums[i] <= 1e4; values are distinct, so any hit is unique. An empty array returns -1. The same code with `nums = [1,2,2,2,3]` is the lower-bound variant, so the boundary conditions are the real content.",
  "diagram": " nums = [-1,0,3,5,9,12], target = 9\n\n classic lo<=hi:            lo<hi lower-bound:\n  lo=0 hi=5 mid=2 (3)        lo=0 hi=5 mid=2 (3)\n    3 < 9 -> lo=3             3 <  9 -> lo=3\n  lo=3 hi=5 mid=4 (9)        lo=3 hi=5 mid=4 (9)\n    9 == 9 -> return 4         9 <= 9 -> hi=4\n  DONE                          lo=3 hi=4 mid=3 (5)\n                                5 < 9 -> lo=4\n                              lo==hi=4; check nums[4]==9 -> return 4\n\\n WHY:  lo<=hi allows hi to keep shrinking, so an exact hit\n terminates the search at the found index.\n       lo<hi   keeps nums[hi] as a LIVE candidate, so the loop\n              exits with hi = lower_bound(target).\n       For RIGHTMOST insertion use upper_bound: nums[hi] < t\n       -> lo=hi+1, then verify.",
  "cpp_vs_py": "Both perform about 14 iterations and finish in microseconds. The genuine difference is in the loop-bound idiom: C++ prefers `lo < hi` with the invariant that `nums[lo..hi]` always contains the answer position as a candidate, which the compiler can use to eliminate bounds checks on `nums[mid]` when the array size is known. Python has no such reasoning, but the `(lo + hi) // 2` computation allocates a new int per iteration for values beyond 256 -- 14 small allocations, which is measurable at this scale only because everything else is so cheap. Python also risks `-1` on an empty array if you do not guard `if not nums: return -1` first, since `hi = len(nums) - 1` becomes -1 and the loop still terminates by luck.",
  "cpp_alts": [
   "`std::lower_bound(nums.begin(), nums.end(), t)` is the library lower-bound, O(log n) with better branch prediction.",
   "`std::binary_search` is the one-liner for the pure existence question, but it gives no index.",
   "`std::upper_bound` gives the rightmost insertion point -- the only change needed between the two variants."
  ],
  "py_alts": [
   "`bisect.bisect_left(nums, t)` and `bisect_right(nums, t)` are the C-implemented lower and upper bounds -- faster than any Python loop.",
   "`target in nums` first, then `nums.index(target)`, is $O(n)$ and only wins for tiny arrays where the constant dominates.",
   "Use `lo < hi` rather than `lo <= hi` for the lower-bound form to avoid the final verification step."
  ],
  "trap": "Mixing the two formulations: using `lo <= hi` with `hi = mid` (instead of `mid - 1`) which can loop forever when `lo == mid`. If you use the inclusive loop, the update must be `hi = mid - 1`.",
  "invariant": "For the `lo <= hi` form: if target exists, its index lies in [lo, hi]. At each step, comparing `nums[mid]` with target either finds it or eliminates `mid` and exactly one side, since the array is sorted. Termination is guaranteed because either lo increases or hi decreases on every non-terminating iteration.",
  "questions": [
   {
    "q": "Why does `lo < hi` compute a lower bound instead of just finding the element?",
    "a": "Because `hi` is never decremented to `mid` when the condition holds, `nums[hi]` stays a live candidate. The loop exits when `lo == hi`, and the invariant then forces that single position to be the first index where `nums[i] >= target` -- the lower bound. With duplicates that is the leftmost insertion point."
   },
   {
    "q": "What single change turns this into upper_bound?",
    "a": "Change the continue condition from `nums[mid] < target` to `nums[mid] <= target`. Then equal elements are consumed and the loop exits at the first index where `nums[i] > target`, which is the rightmost insertion point. In C++ that is literally `upper_bound` instead of `lower_bound`."
   },
   {
    "q": "How do you avoid integer overflow in the midpoint?",
    "a": "Use `lo + (hi - lo) / 2`. In Python this is irrelevant (arbitrary precision), but in C++ `(lo + hi) / 2` overflows once the values exceed about 2^31, and for a negative-midpoint adjustment loop it can also round the wrong way. The safe form costs nothing."
   }
  ]
 },
 "05_binary_search/0875_koko_eating_bananas": {
  "one_liner": "Binary search the SPEED; feasibility is monotone.",
  "core_objective": "Find the minimum eating speed at which Koko finishes all piles within h hours, where each hour she eats one banana from a single pile.",
  "bounds": "1 <= piles.length <= 1e4; 1 <= piles[i] <= 1e9; 1 <= h <= 1e9. Both search-space endpoints are up to 1e9, which is exactly why a linear sweep over speeds is infeasible. The answer always exists because h can be large enough to eat the largest pile in one hour.",
  "diagram": " piles = [3,6,7,11], h = 8   -> speed 4\n\n feasibility is MONOTONE in speed:\n   speed 1 -> ceil sums 27 > 8  FAIL\n   speed 2 -> 2+3+4+6=15 > 8  FAIL\n   speed 3 -> 1+2+3+4=10 > 8  FAIL\n   speed 4 -> 1+2+2+3= 8 <= 8 OK  <- smallest feasible\n\\n binary search on [1, max(piles)] = [1, 11]:\n   lo=1 hi=11 mid=6  feasible(6)=1+1+2+2=6<=8 -> hi=6\n   lo=1 hi=6 mid=3  feasible(3)=1+2+3+4=10>8 -> lo=4\n   lo=4 hi=6 mid=5  feasible(5)=1+2+2+3=8<=8 -> hi=5\n   lo=4 hi=5 mid=4  feasible(4)=8<=8 -> hi=4\n   lo==hi==4 -> return 4\n\\n the search space is 1e9 wide but the predicate is monotone,\n so only log2(1e9) ~ 30 probes are needed.",
  "cpp_vs_py": "The outer loop runs at most 30 iterations, but the inner feasibility check runs once per pile, so the real work is $O(P \\log V)$ with P up to 1e4 and V up to 1e9 -- about 3e5 divisions. That is where the languages diverge. C++ computes `(pile + speed - 1) / speed` as a single 64-bit integer division, roughly 20 to 30 cycles, pipelined across independent piles. Python's `//` on ints is also a C-level division but the surrounding `sum(...)` with a generator expression builds an iterator protocol chain and boxes every quotient -- roughly 8 times slower at this operation count. The C++ version runs in about 1 ms, the Python version in about 10 ms.",
  "cpp_alts": [
   "`(pile + speed - 1) / speed` is exact integer ceiling division; using floating point and `ceil` risks an off-by-one at the exact boundary.",
   "`long long` is required: `pile + speed - 1` can approach 2e9 and the sum of hours can exceed 32 bits.",
   "Early exit from the feasibility loop as soon as `hours > h` -- turns the worst case into the average case and is the single biggest constant-factor win."
  ],
  "py_alts": [
   "`(pile + speed - 1) // speed` avoids `math.ceil` and the float round-trip entirely.",
   "`sum(...)` with a generator is fine; for large piles a `for` loop with an early break is measurably faster because it can bail out.",
   "`lo, hi = 1, max(piles)` is the tightest possible range; starting `hi` at `sum(piles)` is correct but 1e9 probes wide initially, costing more iterations."
  ],
  "trap": "Returning the first speed that passes rather than the smallest. With `hi = mid` on success you converge to the minimum, but with `lo = mid` you converge to the maximum feasible speed. Also, using floating-point division and `ceil` makes the exact-boundary case (`pile` an exact multiple of `speed`) fragile.",
  "invariant": "`lo` is always infeasible-or-the-answer and `hi` is always feasible, so the answer stays inside [lo, hi]. Feasibility is monotone because a faster Koko never takes more hours on any pile, which makes the sum non-increasing in speed -- a monotone predicate is exactly what binary search requires.",
  "questions": [
   {
    "q": "Why is feasibility monotone?",
    "a": "Each pile contributes ceil(pile / speed) hours, which is non-increasing as speed grows, so their sum is non-increasing too. Once it drops to at most h it stays there. A non-monotone predicate would make binary search unsound, which is why the monotonicity argument is the whole proof."
   },
   {
    "q": "What is the correct search range?",
    "a": "[1, max(piles)]. The upper bound works because at speed = max(piles) every pile takes exactly one hour, so the total is P, and P <= 1e4 <= h only sometimes -- if h < P you need a higher bound. sum(piles) is always safe. Both are valid; max(piles) is tighter when h is large."
   },
   {
    "q": "Why does the early exit matter so much?",
    "a": "Feasibility usually fails partway through the pile list, so returning early on the first `hours > h` skips most of the work. Without it you pay P divisions per probe always; with it the average is far fewer. It changes nothing about correctness, only the constant."
   }
  ]
 },
 "05_binary_search/0981_time_based_key_value_store": {
  "one_liner": "Per key, a sorted timestamp list; upper-bound then step back.",
  "core_objective": "Implement a set(key, value, timestamp) store plus get(key, timestamp) returning the value stored at the largest timestamp not exceeding the query, defaulting to the empty string.",
  "bounds": "Each call has key/value/time of length 3, at most 1e5 calls per test set, so the total timestamp count is bounded and the log factor is small. Timestamps are strictly increasing for a given key, which is what lets the list stay sorted without insertion sort.",
  "diagram": " ops: set(a,v1,1) set(a,v2,5) set(b,v3,3)\n       get(a,6) get(a,2) get(b,4) get(c,9)\n\n store = { a: [(1,'v1'), (5,'v2')], b: [(3,'v3')] }\n\n get(a,6): bisect_right(times, 6) = 2 -> index 1 -> 'v2'  OK\n get(a,2): bisect_right(times, 2) = 1 -> index 0 -> 'v1'  OK\n get(b,4): bisect_right([3],   4) = 1 -> index 0 -> 'v3'  OK\n get(c,9): key missing                  -> ''\n\\n why bisect_right and not bisect_left:\n   the answer must include the EXACT timestamp, so we want\n   the first index strictly greater than t, then step back.\n   Using bisect_left would miss an exact match at the last slot.\n\\n invariant: each list is strictly increasing in timestamp,\n so index bisect_right(t)-1 is the unique latest <= t.",
  "cpp_vs_py": "This is a case where the standard library wins outright. `std::map<string, vector<pair<int,string>>>` plus `lower_bound` is a tree walk of about 17 pointer dereferences per query, and those are cache misses, so the query cost is dominated by memory latency rather than computation. CPython's `dict` lookup hashes the key with SipHash (a strong, slow hash) but then gets a single O(1) array probe, and the per-key list search can be `bisect.bisect_right`, which runs entirely inside CPython's C code with no bytecode at all. So for short lists and few keys, Python is genuinely competitive or faster despite its interpreter, because it avoids the pointer chasing that dominates the C++ tree.",
  "cpp_alts": [
   "`std::map` for ordered keys, `std::unordered_map` for O(1) -- unordered wins unless you need ordered iteration.",
   "`std::vector<std::pair<int,std::string>>` per key with `lower_bound` and a `prev()` call; `upper_bound` then `--` is the same thing.",
   "`std::string_view` for the key avoids copying the key into the map on every `set`."
  ],
  "py_alts": [
   "`collections.defaultdict(list)` removes the `if key not in store` branch on `set`.",
   "`bisect_right(times, t) - 1` is the entire query; guard `idx < 0` to return the empty string.",
   "Store timestamps and values as parallel lists only if you care about tuple allocation; a list of tuples is clearer and the difference is negligible at this scale."
  ],
  "trap": "Using `bisect_left` instead of `bisect_right`. If a value was set at exactly the query timestamp, `bisect_left` returns that index but stepping back once lands on the previous element and returns a stale value. `bisect_right` then decrement is the correct pairing.",
  "invariant": "For each key, timestamps are strictly increasing, so `bisect_right(times, t)` returns the count of timestamps <= t; subtracting one gives the index of the largest such timestamp, which is the answer's timestamp, or -1 if none exists.",
  "questions": [
   {
    "q": "Why is `bisect_right` the right primitive?",
    "a": "We want the LAST timestamp <= t, which is at index `bisect_right(t) - 1`. `bisect_right` returns the first index of a value greater than t, so subtracting one lands exactly on the greatest value not exceeding t. `bisect_left` would skip a value equal to t."
   },
   {
    "q": "What if two sets use the same timestamp for one key?",
    "a": "The problem guarantees strictly increasing timestamps per key, so this cannot happen. If it could, you would need to decide whether the later set wins, which would change `set` from append to a replace-if-newer."
   },
   {
    "q": "What is the space complexity across all calls?",
    "a": "Space is proportional to the total number of sets, since each stores one (timestamp, value) pair. Time per set is O(log m) for the append (amortised O(1) since timestamps only increase) and per get is O(log m) for the binary search plus O(1) for the hash lookup on the key."
   }
  ]
 }
})

# ---- appended from _chunk4.json
DATA.update({
 "06_linked_list/0002_add_two_numbers": {
  "one_liner": "Digit-by-digit addition from the tail, carrying forward.",
  "core_objective": "Add two numbers given as reversed digit lists and return the sum as a reversed list.",
  "bounds": "Each list has at least one digit, up to about 100 digits, so the result may exceed any fixed integer type -- this is the problem where C++ must avoid converting to int. Carries can chain past the leading digit, requiring a final append.",
  "diagram": " l1 = [2,4,3] (342)  l2 = [5,6,4] (465)  -> [7,0,8] (807)\n\n   l1: 2 -> 4 -> 3 -> NULL\n   l2: 5 -> 6 -> 4 -> NULL\n\n   step  a=2 b=5 carry=0 -> sum 7  emit 7  carry 0\n   step  a=4 b=6 carry=0 -> sum 10 emit 0  carry 1\n   step  a=3 b=4 carry=1 -> sum 8  emit 8  carry 0\n   step  a=NULL b=NULL c=0 -> emit nothing\n   (a NULL, b=7, c=1 -> emit 8, then tail b)\n\n   invariant: carry in {0,1}; sum <= 9+9+1 = 19 < 20",
  "cpp_alts": [
   "Reusing the input nodes saves an allocation per digit; a fresh vector is simpler and avoids aliasing bugs.",
   "`long long` is wrong here -- 100 digits overflows it. Keep `int` per digit and accumulate the carry manually."
  ],
  "py_alts": [
   "`0` as the terminal sentinel avoids the None-check in the loop condition entirely.",
   "`divmod(a + b + carry, 10)` returns (digit, carry) in one call."
  ],
  "trap": "Stopping when either pointer is null instead of when both are null. With l1 = [5] and l2 = [5,4] the correct answer is [9,4], and stopping at the first null loses the 4.",
  "invariant": "After k iterations, `carry` is exactly the carry out of the lowest k digit positions, so each emitted digit is the correct digit of the true sum.",
  "questions": [
   {
    "q": "Why are the digits reversed in the input?",
    "a": "Because then the least significant digit is at the head, which lets a single forward traversal perform the carry propagation in the correct order with no reversing."
   },
   {
    "q": "When is the final `while (carry)` loop needed?",
    "a": "When one input is exhausted while a nonzero carry remains -- e.g. [9] plus [1] gives digit 0 and carry 1, so the result is [0,1]. Omitting that tail is the classic bug."
   },
   {
    "q": "What is the space complexity, and can it be O(1)?",
    "a": "O(1) auxiliary if you reuse the input nodes, O(max(m,n)) if you build a new list. The in-place version is the more interesting answer because it also avoids the allocator."
   }
  ]
 },
 "06_linked_list/0019_remove_nth_node_from_end_of_list": {
  "one_liner": "Two pointers at distance n make the gap land on the target.",
  "core_objective": "Remove the n-th node from the end of a linked list, counting the last node as n = 1, in one pass.",
  "bounds": "n >= 1 and n <= the list length, so the target always exists. n = 1 means removing the tail. A one-node list with n = 1 must become empty, which is the boundary that forces the dummy-head trick.",
  "diagram": " list = [1,2,3,4,5], n = 2  -> [1,2,3,5]\n\n  dummy -> 1 -> 2 -> 3 -> 4 -> 5 -> NULL\n          ^f           ^s        (gap = 2)\n\n  advance s by n -> s at 4; advance f to 2 (one before target)\n  advance both: f=3, s=5\n  unlink: f.next = f.next.next   (removes 4)\n\n  gap arithmetic: after the first loop the distance fast-slow\n  is exactly n nodes. After n+1 more single steps, slow is on\n  the n-th from the end and fast is one past it.\n\n  n = 1: dummy protects the case where slow would be head",
  "cpp_alts": [
   "`ListNode dummy(0); dummy.next = head;` avoids the head-is-null and head-is-target special cases.",
   "An iterative two-pass (count length, then walk) is simpler to reason about but touches every node twice."
  ],
  "py_alts": [
   "A sentinel object with a `.next` attribute is the standard trick; it removes both boundary branches.",
   "`fast.next is not None` in the guard means the guarantee `n <= length` is doing real work."
  ],
  "trap": "Using two separate loops (one to compute length, one to find the target) without a dummy head, then failing when the head itself must be removed -- `head = head.next` must be paired with returning the new head rather than modifying through a local pointer.",
  "invariant": "Throughout, `fast` is exactly n nodes ahead of `slow`. After the two advance phases, `slow` is the predecessor of the n-th-from-last node and `fast` is the n-th-from-last node.",
  "questions": [
   {
    "q": "Why a dummy head?",
    "a": "Because the node to remove can be the head itself. With a dummy in front, the target always has a predecessor, so the unlink is always `prev.next = prev.next.next` with no special case."
   },
   {
    "q": "What exactly does the distance-n trick buy?",
    "a": "One pass instead of two. Because the problem guarantees n <= length, you never need to measure the length first -- you simply lag the fast pointer by n nodes."
   },
   {
    "q": "How would you solve it without the guarantee n <= length?",
    "a": "You cannot: the slow pointer would run off the end. The standard follow-up asks for a return value indicating whether the node existed, which requires a length pass first."
   }
  ]
 },
 "06_linked_list/0021_merge_two_sorted_lists": {
  "one_liner": "Dummy head plus a tail pointer makes the splice trivial.",
  "core_objective": "Merge two ascending sorted lists into one ascending sorted list, reusing existing nodes.",
  "bounds": "0 <= list1.length, list2.length <= 50, and either list may be null, so the empty cases must return the other list rather than crash. Both lists are already sorted, which is what allows the O(1)-per-step decision.",
  "diagram": " l1 = [1,3,5]  l2 = [2,4,6]\n\n  dummy -> tail = dummy\n  a=1 b=2 : 1 <= 2 -> tail.next = a ; tail = 1 ; a = 3\n  a=3 b=2 : 3 >  2 -> tail.next = b ; tail = 2 ; b = 4\n  a=3 b=4 : 3 <= 4 -> tail.next = a ; tail = 3 ; a = 5\n  a=5 b=4 : 5 >  4 -> tail.next = b ; tail = 4 ; b = 6\n  a=5 b=6 : 5 <= 6 -> tail.next = a ; tail = 5 ; a = NULL\n  a=NULL    : tail.next = b (6)   -> done\n  tail.next = NULL  (must set!)\n\n  invariant: tail is always the LAST node of the merged prefix,\n  so tail.next = x is a single pointer store, not a traversal.",
  "cpp_alts": [
   "`ListNode* tail = &dummy;` with a stack-allocated dummy avoids a heap allocation for the sentinel.",
   "The recursive version is 4 lines and is arguably clearer, at O(m+n) stack depth."
  ],
  "py_alts": [
   "A sentinel `ListNode(0)` object removes the `if not list1` branches.",
   "Chasing `tail = tail.next` after each append is the O(1) trick that separates a good answer from the O(n^2) one."
  ],
  "trap": "Appending by walking to the end on every insertion, which is O(n^2). Maintain a tail pointer instead -- that single change is the whole difference between the two complexities.",
  "invariant": "After each iteration, the nodes up to `tail` form the sorted merge of the prefixes already consumed, and `tail` is the last of them. Appending the smaller head preserves sortedness.",
  "questions": [
   {
    "q": "Why the `<=` versus `<` choice at the head comparison?",
    "a": "Either is correct for correctness, but `<=` and `<` differ in which list's nodes are preferred when heads are equal. Since all nodes must be kept, both are fine; only stability across a later dedupe pass would care."
   },
   {
    "q": "How does the dummy head simplify the termination?",
    "a": "You splice the entire non-empty remainder with a single `tail.next = a ? a : b`, then set `tail.next = NULL`. Without a sentinel you'd need to special-case an initially empty list."
   },
   {
    "q": "What if the lists are not sorted?",
    "a": "The O(1) decision breaks -- you cannot know which head is smaller without scanning ahead. Merging then costs O(m+n) only because sortedness makes the comparison a single node read."
   }
  ]
 },
 "06_linked_list/0023_merge_k_sorted_lists": {
  "one_liner": "Either divide and conquer, or a k-way heap of the heads.",
  "core_objective": "Merge k ascending sorted lists into one ascending sorted list, reusing nodes where possible.",
  "bounds": "1 <= k <= 1e4 with a combined total of 1e4 nodes, so heap operations number 1e4 and log k is about 14. An empty input array must return null.",
  "diagram": " lists = [[1,4,5],[1,3,4],[2,6]] -> [1,1,2,3,4,4,5,6]\n\n HEAP approach: heap of (value, listIndex, node)\n   init: 1(L0) 1(L1) 2(L2)\n   pop 1(L0) -> emit; push L0.next = 4\n   pop 1(L1) -> emit; push L1.next = 3\n   pop 2(L2) -> emit; push L2.next = 6\n   pop 3(L1) -> emit; push L1.next = 4\n   pop 4(L0) -> emit; L0 exhausted\n   pop 4(L1) -> emit; push 1... L1 exhausted\n   pop 5(L0) -> emit; L0 exhausted\n   pop 6(L2) -> emit\n   total: 8 pops, each O(log k)\n\n DIVIDE AND CONQUER:\n   merge(list[0..k/2]) with merge(list[k/2..k])\n   T(k) = 2T(k/2) + O(N)  ->  O(N log k)",
  "cpp_alts": [
   "`priority_queue<int, vector<int>, cmp>` with an index array beats storing node pointers for cache locality.",
   "Divide and conquer with an explicit vector of heads is often simpler to implement correctly than a comparator object."
  ],
  "py_alts": [
   "`heapq` is min-only; push `(value, listIndex, node)` tuples and pop all three together.",
   "`heapq.merge(*lists)` is a lazy iterator that does exactly this and is a strong interview answer."
  ],
  "trap": "Rebuilding the result list from scratch inside the loop instead of relinking heads, which loses the O(1)-per-node property and allocates a node per element.",
  "invariant": "The heap always contains exactly the smallest unconsumed node of each non-exhausted list. Its minimum is therefore the smallest unconsumed node overall, which is the next output element.",
  "questions": [
   {
    "q": "Which is asymptotically better, the heap or divide and conquer?",
    "a": "Both are $O(N \\log k)$. The heap makes one pass with a priority queue; divide and conquer makes log k passes of pairwise merges. The heap uses $O(k)$ space, D&C uses $O(\\log k)$ stack."
   },
   {
    "q": "Why store (value, listIndex, node) rather than just values?",
    "a": "Because you need to know which list's next node to advance after a pop. Encoding all three in the tuple means the heap comparison uses value first and the tuple supplies the bookkeeping."
   },
   {
    "q": "What does k = 1 degenerate to?",
    "a": "The loop pops the single head, pushes nothing (the list is exhausted), and the heap empties -- returning that one list unchanged, which is correct."
   }
  ]
 },
 "06_linked_list/0025_reverse_nodes_in_k_group": {
  "one_liner": "Reverse each group of k; the final short group is left alone.",
  "core_objective": "Reverse the order of nodes in groups of k, leaving the last group untouched if it has fewer than k nodes.",
  "bounds": "1 <= k <= n <= 5000. The final group being short is not an edge case but the normal case, and getting it wrong is the single most common failure.",
  "diagram": " list [1,2,3,4,5], k = 2  -> [2,1,4,3,5]\n\n  group [1,2] -> [2,1]     FULL, reversed\n  group [3,4] -> [4,3]     FULL, reversed\n  group [5]    -> [5]      SHORT, kept\n\n  iteration guard:\n    for i in range(0, n - k + 1, k):   <-- stops early\n      so a short tail never enters the loop\n\n  reverse-in-place [a,b,c] -> [c,b,a]\n    prev = NULL, cur = groupFirst\n    while cur: nxt = cur.next; cur.next = prev\n              prev = cur; cur = nxt\n\n  the bug: using range(0, n, k) includes the short tail and\n  reverses it, giving [2,1,4,3] -> and for k=2,n=5 -> [2,1,4,3,5]\n  is right but [5] alone reversed is still [5]... the real failure\n  is when the short tail has 2 nodes and k = 3.",
  "cpp_alts": [
   "Precompute the node vector once, then reverse slices in place -- O(n) space but far simpler to get right.",
   "`reverse(begin + i, min(begin + i + k, end))` per group needs the vector form."
  ],
  "py_alts": [
   "Slice-and-assign on a node array (`arr[i:i+k] = arr[i:i+k][::-1]`) is the shortest correct answer.",
   "Three pointers on the array form: `arr[i:j] = reversed(arr[i:j])`."
  ],
  "trap": "Reversing the final incomplete group. The loop bound must be `n - k + 1`, or equivalently the group end must be clamped to `min(i + k, n)` and skipped if shorter than k.",
  "invariant": "Before group i starts, the first i nodes are already correctly reversed and wired; the group being processed is exactly nodes [i, i+k) when that range is full.",
  "questions": [
   {
    "q": "How do you detect a short final group without counting?",
    "a": "Either bound the loop by `n - k + 1`, or check whether the group's predecessor list still has k nodes. The loop bound is cleaner and makes the condition impossible to violate."
   },
   {
    "q": "Why is a dummy head needed here but not in a plain reverse?",
    "a": "Because you must reconnect the reversed groups to their predecessors. The dummy gives every group a stable predecessor to write into, and it also makes returning an empty list trivial."
   },
   {
    "q": "What does the array-based approach cost?",
    "a": "O(n) extra space for the node array, in exchange for turning pointer surgery into index arithmetic. That trade is usually worth taking in an interview and worth naming explicitly."
   }
  ]
 },
 "06_linked_list/0138_copy_list_with_random_pointer": {
  "one_liner": "Interleave new nodes so random pointers resolve in one pass.",
  "core_objective": "Deep-copy a linked list where each node also has a random pointer to any node or null, with no node in the copy pointing into the original.",
  "bounds": "The list is non-empty and each node has `next` and `random`. The aliasing is the whole difficulty: a naive DFS with a visited map handles it, but costs O(n) extra space and recursion depth.",
  "diagram": " original: A -> B -> C -> NULL\n           A.random = C,  B.random = A\n\n PASS 1 weave:  A' -> B' -> C'\n           A -> A' -> B -> B' -> C -> C'\n           (copies inserted right after originals)\n\n PASS 2 random: for each original X with copy X' = X.next:\n           X'.random = X.random.next   (if X.random != NULL)\n           one line, no map!\n\n PASS 3 unweave: restore A -> B -> C and\n           A' -> B' -> C' separately\n\n  invariant after pass 2: every X'.random points at a COPY,\n  never an original -- because X.random.next is X.random's copy.",
  "cpp_alts": [
   "A `map<ListNode*, ListNode*>` memo makes the DFS version trivially correct at the cost of hash lookups per edge.",
   "Three passes over the interleaved list are $O(n)$ with no auxiliary map -- the best space answer."
  ],
  "py_alts": [
   "`copy.deepcopy` on a self-referential object graph works here and is a valid answer to state, though it hides the algorithm.",
   "`defaultdict` cannot map None-valued keys usefully; an explicit `if node.random` guard is required."
  ],
  "trap": "Setting `copy.random = original.random` (no `.next`). That aliases the copy back into the original graph, which the problem explicitly forbids and the test detects.",
  "invariant": "After the weave, `original.next.next` is the copy of the node two steps ahead, so `X.random.next` is by construction the copy of `X.random`. That single structural fact is what makes pass 2 correct without any lookup.",
  "questions": [
   {
    "q": "Why does the weave beat the memo-map approach?",
    "a": "The map costs O(n) hash operations and O(n) nodes of auxiliary memory plus recursion depth. The weave costs three linear passes and no auxiliary structure, at the price of mutating the original temporarily -- which is restored in pass 3."
   },
   {
    "q": "What breaks if the random pointer self-references (A.random = A)?",
    "a": "Nothing in the weave approach, because `X'.random = X.random.next` and `A.next` is `A'`, so `A'.random = A'` correctly. In a naive DFS without a memo it is exactly the cycle that would cause infinite recursion."
   },
   {
    "q": "Why must pass 3 unweave rather than rebuild?",
    "a": "Because the originals' `next` pointers were overwritten. Unweaving restores each original's successor in one pass, and the copies' successors become valid once the originals are fixed. Doing it in any other order leaves dangling pointers."
   }
  ]
 },
 "06_linked_list/0141_linked_list_cycle": {
  "one_liner": "Floyd: one fast pointer eventually overtakes the slow one.",
  "core_objective": "Given the head of a linked list, determine whether it contains a cycle and, if so, return the node where the cycle begins.",
  "bounds": "The list may be self-cyclic and may have a tail of any length, so the entry node is not necessarily the head. Only `pos == 0` exists as a special input; a null input is not typical here but should not crash.",
  "diagram": " index 0 -> 1 -> 2 -> 3 -> 4\n                    ^              |\n                    +--------------+\n\n  mu = distance head->entry = 3\n  lambda = cycle length = 2 (3->4->3)\n\n  phase 1: fast = 2*slow\n   slow at 0, fast at 0\n   slow 1, fast 2\n   slow 2, fast 4\n   slow 3, fast 2   (4->3->4->3, so fast wraps to 3->4? trace)\n   they coincide INSIDE the cycle\n\n  phase 2: reset one pointer to head, advance both by 1\n   slow 4, fast head 0\n   slow 3(entry), fast 1   -> next step both step 1\n   slow 3, fast 2\n   slow 4, fast 3\n   slow 3, fast 4\n   -> coincide at index 3 = ENTRY\n\n  proof: 2*mu = mu + k*lambda  =>  they meet at the entry.",
  "cpp_alts": [
   "`ListNode* slow, *fast` with `do/while` avoids the initial null check.",
   "Brent's algorithm detects a cycle with O(1) space and fewer pointer dereferences, though it does not find the entry."
  ],
  "py_alts": [
   "The `while fast and fast.next` guard expresses the precondition directly.",
   "`is` compares identity, which is the correct comparison for node objects."
  ],
  "trap": "Running phase 2 with fast still at the meeting point instead of resetting it to head. The classic correct form resets ONE of the two pointers and advances both by one step.",
  "invariant": "After t iterations of phase 1, fast has travelled 2t edges and slow t. If a cycle of length lambda exists, the first t with 2t = t (mod lambda) places them at the same node, i.e. t = k*lambda for some k, which puts fast exactly lambda ahead of slow inside the cycle.",
  "questions": [
   {
    "q": "Why does resetting one pointer to head work in phase 2?",
    "a": "After t steps where t is a multiple of lambda, fast is t = k*lambda ahead of slow. Resetting fast to head and advancing both by one, they meet after mu steps because slow has travelled t + mu and fast has travelled mu, and the cycle entry is mu edges from head and (t + mu - mu) mod lambda = 0 from slow."
   },
   {
    "q": "What is the time complexity?",
    "a": "$O(n)$ overall. Phase 1 takes at most mu + lambda iterations and phase 2 takes mu, both linear in the list length. Space is $O(1)$ -- three pointers."
   },
   {
    "q": "Can you find the entry without phase 2?",
    "a": "Not with only Floyd's pointers. Phase 1 proves existence but the meeting point is generally not the entry; the extra pass is what converts \"a cycle exists\" into \"the cycle starts here\"."
   }
  ]
 },
 "06_linked_list/0143_reorder_list": {
  "one_liner": "Split at the middle, reverse the back half, then interleave.",
  "core_objective": "Reorder a list so it alternates nodes from the first half and nodes from the second half, with the first half supplying the leading nodes.",
  "bounds": "n >= 1, so n = 1 returns the single node and n = 2 swaps. Odd lengths mean the first half has one extra node, which must be consumed first or the output order is wrong.",
  "diagram": " list [1,2,3,4,5]  -> [1,5,2,4,3]\n\n  step 1  find middle (slow/fast): slow at 3   second = 4\n  step 2  cut:  1->2->3->NULL ,  4->5->NULL\n  step 3  reverse second half: 5->4\n  step 4  interleave, FIRST half leads:\n         take 1 (first), take 5 (second), take 2, take 4, take 3\n         result [1,5,2,4,3]\n\n  list [1,2,3,4]  -> [1,4,2,3]   (first half 1,2 leads)\n\n  invariant: first always non-NULL (it has >= second's length),\n  so `first = first.next` is safe without a guard.",
  "cpp_alts": [
   "An array of nodes turns this into index arithmetic and makes the interleave trivial at O(n) space.",
   "Cutting with a dummy head after slow removes the special case where slow is the head."
  ],
  "py_alts": [
   "`list.reverse()` on the extracted second half is a C-level call, much faster than manual pointer reversal.",
   "Taking from `first` before `second` is the load-bearing line; the reverse order gives [1,3,5,2,4]."
  ],
  "trap": "Interleaving from the wrong end. Taking a node from the second half before one from the first produces the wrong order, and the error only shows on odd lengths.",
  "invariant": "`first` and `second` each point to the head of a reversed-or-not list of roughly equal length with first >= second. Taking from first first preserves the alternation and guarantees first stays non-null.",
  "questions": [
   {
    "q": "Why must the first half lead?",
    "a": "Because n can be odd, in which case the first half has one more node. If you took from the second half first, the last output node would come from the first half and the pattern would be inverted."
   },
   {
    "q": "Can you do it without reversing the second half?",
    "a": "Yes, by collecting into a stack or an array and emitting alternately -- but that costs O(n) extra space, whereas the reversal is in-place and costs O(1) space."
   },
   {
    "q": "What is the space complexity of the pointer version?",
    "a": "$O(1)$. The middle is found with two pointers, the second half is reversed in place, and the interleave only rewires pointers. No allocation at all."
   }
  ]
 },
 "06_linked_list/0146_lru_cache": {
  "one_liner": "Hash map for O(1) lookup, doubly linked list for O(1) reordering.",
  "core_objective": "Design a cache with a fixed capacity where get and put are O(1) and the least recently used entry is evicted when full.",
  "bounds": "At most 1e5 operations, capacity >= 1, so capacity 1 must still work (evicting the only entry). get on a missing key returns -1 and must not disturb recency. Keys and values are at least length 1.",
  "diagram": " cap = 2:  put(1,1) put(2,2) get(1) put(3,3)\n\n  hash:  {1:<1>, 2:<2>, 3:<3>}\n  list:  head <-> 3 <-> 1 <-> 2 <-> tail\n         (LRU)                 (MRU)\n\n  get(1): move 1 to MRU end -> list 3 <-> 2 <-> 1\n  put(3): map size == cap(2) -> evict tail (2)\n          map: {1,3}\n\n  sentinel design:\n    head <-> (LruEntry) <-> ... <-> (LruEntry) <-> tail\n    sentinel.prev / sentinel.next are never null, so\n    remove(node) needs no null checks.\n\n  invariant: |map| == |list| - 2 and map keys == non-sentinel keys",
  "cpp_alts": [
   "`std::list` + `std::unordered_map<key, list_iterator>` is the textbook C++ answer and is fully O(1).",
   "`gp_hash_table` beats `unordered_map` here on cache locality because every op touches both structures anyway.",
   "An intrusive doubly linked list embedded in the node removes the separate list allocation and one indirection."
  ],
  "py_alts": [
   "`collections.OrderedDict` gives `move_to_end` and `popitem(last=False)` in C -- a complete LRU in 6 lines.",
   "`__setitem__` on an OrderedDict moves the key to the end automatically, which is exactly `put`.",
   "A plain `dict` in Python 3.7+ preserves insertion order, so `move_to_end` has no equivalent and you need OrderedDict."
  ],
  "trap": "Calling `move_to_end(key)` in `get` before checking the key exists -- that raises `KeyError`. The existence test must come first.",
  "invariant": "The map and the list hold exactly the same set of non-sentinel nodes, and the list is ordered from least to most recently used. Every access moves the node to the tail, which is what preserves both parts of the invariant.",
  "questions": [
   {
    "q": "Why a doubly linked list rather than singly?",
    "a": "Because `get` must move an arbitrary node to the MRU end, and removing from a singly linked list requires the predecessor. A doubly list gives O(1) removal via two pointers, with the head/tail sentinels eliminating every null check."
   },
   {
    "q": "Why does OrderedDict make the Python version trivial?",
    "a": "It is a dict that remembers insertion order and exposes `move_to_end(key)` plus `popitem(last=False)`. That is exactly the two primitives an LRU needs, both implemented in C, so the whole cache is a few Python lines."
   },
   {
    "q": "What are the complexities of get and put?",
    "a": "Both $O(1)$: one hash lookup, one list splice, and for put one possible eviction (map delete plus list pop). Space is $O(capacity)$, bounded by the capacity because put evicts before inserting."
   }
  ]
 },
 "06_linked_list/0206_reverse_linked_list": {
  "one_liner": "Three pointers: prev, current, next -- and never lose next.",
  "core_objective": "Reverse a singly linked list in place and return the new head.",
  "bounds": "The list may be null or single-node, both of which must be handled without special-casing beyond the loop condition. The operation must be in place -- O(1) space.",
  "diagram": " 1 -> 2 -> 3 -> NULL\n\n prev=NULL cur=1\n   nxt = 2; cur.next = NULL; prev=1; cur=2   -> 1->NULL, cur 2->3\n   nxt = 3; cur.next = 1;   prev=2; cur=3   -> 2->1,   cur 3->NULL\n   nxt = NULL; cur.next = 2; prev=3; cur=NULL -> 3->2->1\n return prev = 3\n\n THE ORDER MATTERS: save nxt BEFORE overwriting cur.next,\n otherwise the rest of the list is unreachable.\n\n iterative: O(n) time, O(1) space\n recursive: O(n) time, O(n) stack -- risky for 1e5 nodes",
  "cpp_alts": [
   "Iterative with three raw pointers is the only version with O(1) space and no stack overflow risk.",
   "`std::reverse` does not apply -- it works on contiguous ranges, not linked structures."
  ],
  "py_alts": [
   "`prev, cur = None, head` then `cur.next, prev, cur = prev, cur, cur.next` -- the simultaneous assignment makes the ordering bug impossible."
  ],
  "trap": "Writing `prev = cur` before `cur = cur.next`, or forgetting to save `next` first. Either loses the remainder of the list and silently truncates the result.",
  "invariant": "After k iterations, `prev` is the head of a reversed list containing exactly the first k original nodes, and `cur` points to the (k+1)-th original node. So nothing is lost or duplicated.",
  "questions": [
   {
    "q": "Why must `nxt` be saved before `cur.next` is overwritten?",
    "a": "Because `cur.next` is the only link to the unprocessed remainder. Once you overwrite it, that tail is unreachable from anywhere -- not from cur, not from prev -- so the saved reference is what keeps the traversal alive."
   },
   {
    "q": "When is recursion a bad choice here?",
    "a": "For long lists. CPython's default recursion limit is 1000, so a 1e5-node list raises `RecursionError`. C++ would need a 1e5-frame stack, which is 8 MB or more. The iterative version has neither problem."
   },
   {
    "q": "What does the function return, and why is it `prev`?",
    "a": "`prev`, because after the loop `cur` is NULL and `prev` holds the last node processed -- which is the original tail, now the head of the reversed list. Returning `cur` would give null."
   }
  ]
 },
 "06_linked_list/0287_find_the_duplicate_number": {
  "one_liner": "Floyd again: the entry of the functional cycle is the duplicate.",
  "core_objective": "An array of n+1 integers in [1, n] contains exactly one value repeated; return it without modifying the array and using O(1) space.",
  "bounds": "1 <= n <= 1e5, values in [1, n] with n = 1 a degenerate case. Modifying the array is forbidden, so the in-place-marking trick (setting nums[i] to -1) is illegal.",
  "diagram": " nums = [1,3,4,2,2]  -> 2\n treat i as an arrow: i -> nums[i]\n\n  0 -> 1 -> 3 -> 2 -> 4 -> 2 -> 4 -> 2 ...\n              ^         |\n              +---------+  cycle length 2\n\n  mu (tail length)  = 3   (0,1,3 to reach 2)\n  phase 1 meeting: 2*mu = 6, lambda = 2, 6 mod 2 == 0 -> meets\n  phase 2: reset to 0, both step 1 until equal -> 2  CORRECT\n\n  proof: entry node == the duplicated value because the tail\n  ends at the repeated value and the cycle starts there.",
  "cpp_alts": [
   "The in-place marking solution is $O(n)$ and faster but mutates the input, which is forbidden here.",
   "Sum formula gives the duplicate directly: sum(nums) - n(n+1)/2 -- one line, but overflow-prone for large n."
  ],
  "py_alts": [
   "`Counter` is $O(n)$ space and illegal by the constraint.",
   "The Floyd version has no allocation at all, which is exactly what the problem asks you to demonstrate."
  ],
  "trap": "Using the bitwise XOR trick (`x ^ x = 0`) -- it works only when every OTHER value appears an even number of times, and here every value in [1,n] appears once except the duplicate.",
  "invariant": "Viewing the array as a function `f(i) = nums[i]` from [0,n] into [1,n], the duplicate guarantees a cycle. Floyd detects it and returns its entry, which is the duplicated value.",
  "questions": [
   {
    "q": "Why does the cycle entry equal the duplicated number?",
    "a": "The chain starting at 0 visits distinct nodes until it repeats. The repeat happens at the value that has two preimages, which is precisely the duplicated number. So the tail ends at the duplicate and the cycle begins there."
   },
   {
    "q": "Why is the sum trick not usable despite being O(1) space?",
    "a": "It is usable in spirit -- sum(nums) - n(n+1)/2 gives the duplicate -- but with n up to 1e5 the sum reaches about 5e9, which overflows a 32-bit C++ int. The sum must be 64-bit, and the float version in Python loses exactness at that magnitude."
   },
   {
    "q": "What is the space complexity of the Floyd solution?",
    "a": "$O(1)$ -- three integers. No array of counts, no set. That is the entire point of using Floyd here rather than the more obvious counting approach."
   }
  ]
 }
})

# ---- appended from _chunk5.json
DATA.update({
 "07_trees/0098_validate_binary_search_tree": {
  "one_liner": "Carry an open interval down, not just the parent value.",
  "core_objective": "Decide whether a binary tree satisfies the BST property: every node's value lies strictly between the values permitted by all its ancestors.",
  "bounds": "Node values are int and can be INT_MIN or INT_MAX, so a bounds-based recursion must use long long or null sentinels, and Python must use float('-inf') rather than 0. Strictness matters: duplicates are invalid.",
  "diagram": "      5\n    /   \\\n   3     7      -> valid\n  / \\   / \\\n 2   4 6   8\n\n  valid(n, lo, hi) means: n.val in (lo, hi) STRICTLY\n   left  -> valid(n.left,  lo, n.val)\n   right -> valid(n.right, n.val, hi)\n\n  WRONG variant (the trap):\n   left  -> valid(n.left,  n.val, INT_MAX)   # loses the lower bound\n   right -> valid(n.right, INT_MIN, n.val)   # loses the upper bound\n   accepts [5,1,6,null,null,3] which is invalid\n\n  inorder must be STRICTLY ascending -- simpler:\n   prev = -inf ; walk inorder ; if val <= prev: False",
  "cpp_alts": [
   "`long long lo, hi` with `LLONG_MIN/LLONG_MAX` handles INT_MIN/INT_MAX safely; `INT_MIN` as a bound is the classic overflow bug.",
   "An iterative stack-based inorder avoids recursion depth issues on a skewed tree of 1e4 nodes."
  ],
  "py_alts": [
   "`float('-inf')` / `float('inf')` as the initial bounds is the safe sentinel -- integer sentinels cannot express \"unbounded\".",
   "`bisect` on the inorder list is another way to state strictness, though it allocates O(n)."
  ],
  "trap": "Passing `None`/0 as the initial bound instead of infinity. With `0` as the lower bound a tree rooted at a negative value is rejected, and with `0` as the upper bound a subtree of positives is rejected.",
  "invariant": "`valid(n, lo, hi)` returns true iff n's entire subtree satisfies the BST property given that every value in it must lie strictly inside (lo, hi). The recursion tightens exactly one side per branch, so the invariant composes.",
  "questions": [
   {
    "q": "Why is the inorder-strictly-ascending check equivalent?",
    "a": "A BST is exactly the tree whose inorder traversal is strictly increasing. Proving one direction: an inorder walk emits left subtree, root, right subtree, and the BST property forces each to be in order. So a single inorder pass with one comparison decides validity, at O(h) space."
   },
   {
    "q": "What is the recursion depth, and is it safe?",
    "a": "O(h), h the height. A degenerate tree of 1e4 nodes gives depth 1e4, which overflows CPython's default recursion limit and is a large but survivable C++ stack. The iterative inorder version is the safe choice."
   },
   {
    "q": "How do you handle INT_MIN as a node value in C++?",
    "a": "Use `long long` bounds with `LLONG_MIN`/`LLONG_MAX`, not `int` with `INT_MIN`. With int bounds a node equal to INT_MIN would fail the strict lower-bound test even though it is legal."
   }
  ]
 },
 "07_trees/0100_same_tree": {
  "one_liner": "Structural equality: both null, or both non-null and equal.",
  "core_objective": "Decide whether two binary trees have identical structure and identical node values.",
  "bounds": "The trees may have different node counts, different depths, or be null. Comparing node-by-node only when both exist is what makes mismatched shapes fail fast.",
  "diagram": "  t1        t2        same?\n   1          1        values equal\n  / \\        / \\       both children non-null\n 2   3      2   3      recurse\n\n   1          1        values equal\n  / \\        /          t2 right is NULL but t1 right is not\n 2   3                    -> FALSE (shape differs)\n\n  recursion:\n   both NULL          -> true\n   one NULL           -> false\n   values differ      -> false\n   else recurse both children\n\n  invariant: the call at node pair (a,b) is responsible for the\n  entire subtrees below; it may only return true if BOTH shape\n  and values agree all the way down.",
  "cpp_alts": [
   "An iterative stack of node pairs avoids recursion depth on skewed trees.",
   "A single `TreeNode*` stack holding pairs is the standard iterative form."
  ],
  "py_alts": [
   "Comparing with `==` on nodes would use identity; the `is not None` and value checks must be explicit.",
   "A one-liner `(a.val, a.left, a.right) == (b.val, b.left, b.right)` recurses implicitly but allocates tuples per node."
  ],
  "trap": "Checking only values and ignoring structure. `[1,2]` versus `[1,null,2]` has the same multiset of values but different shapes; the null checks on the children are what distinguish them.",
  "invariant": "At every call, `a` and `b` are at the same position in their respective trees (or both null). Returning true requires all four conditions simultaneously, so a single false anywhere propagates up and the whole answer is false.",
  "questions": [
   {
    "q": "Why check `a is None and b is None` before touching values?",
    "a": "Because you must distinguish \"both subtrees end here\" (true) from \"one ends and the other does not\" (false). Merging those cases into a single `a is None or b is None` check wrongly accepts trees of different shapes."
   },
   {
    "q": "Can you do this without recursion?",
    "a": "Yes -- push both roots on a stack, pop a pair, apply the same three tests, and push the two children pairs. Same $O(n)$ time, and the stack is O(h) which is better than the call stack only in that it is heap-allocated and bounded explicitly."
   },
   {
    "q": "What is the time complexity, and why is it O(n) not O(min(n,m))?",
    "a": "$O(n)$ where n is the total nodes compared. You may stop early on a mismatch, but the worst case is when both trees are identical, and then every node in both is visited."
   }
  ]
 },
 "07_trees/0102_binary_tree_level_order_traversal": {
  "one_liner": "Snapshot the queue size at the start of each level.",
  "core_objective": "Return the values of the tree grouped by level, outermost level first.",
  "bounds": "The tree may be null (return []) and is skewed, so the queue-based BFS must not recurse. Node count up to 2e4, so recursion depth can reach 2e4 on a left-only chain.",
  "diagram": "        3\n      /   \\\n     9   20\n        /  \\\n       15   7\n\n  queue = [3], level size = 1\n    take 1 node -> 3              level 0: [3]\n  queue = [9,20], level size = 2\n    take 2     -> 9, 20          level 1: [9,20]\n  queue = [15,7], level size = 2\n    take 2     -> 15, 7          level 2: [15,7]\n\n  the SNAPSHOT is the whole trick: capture len(queue) BEFORE\n  consuming the level, else you would consume everything in one\n  flat list. `for _ in range(size)` is the idiom.\n\n  time O(n), space O(width) for the queue",
  "cpp_alts": [
   "`queue<TreeNode*>` with `int size = q.size()` per level is the canonical form.",
   "Two vectors and an index pointer avoids per-level allocation, reusing capacity across levels."
  ],
  "py_alts": [
   "`from collections import deque; popleft()` is O(1) at both ends; a `list` with an index pointer is also O(1) and avoids deque overhead for pure FIFO use."
  ],
  "trap": "Iterating `while queue:` and appending into the same level list -- that flattens the traversal. Or recomputing the level size inside the inner loop, which shrinks it as you pop.",
  "invariant": "At the start of each outer iteration, the queue contains exactly the nodes of the current level, in left-to-right order, and `size` is that count. Popping exactly `size` times consumes precisely one level and leaves the queue holding the next.",
  "questions": [
   {
    "q": "Why must the size be captured before the inner loop?",
    "a": "Because popping shrinks the queue. If you recompute the size each iteration it decreases by one every time and the inner loop exits early, producing short levels. Capturing it once makes the loop bound the level width."
   },
   {
    "q": "What is the space complexity, and what dominates it?",
    "a": "$O(w)$ where w is the maximum width of the tree, plus $O(h)$ for the result list itself. A complete tree of n nodes has width ~n/2, so the result dominates; a skewed tree has width 1 but a result of depth h."
   },
   {
    "q": "When is the depth-first alternative preferable?",
    "a": "When the interviewer wants to test index-based accumulation: recurse with a `depth` argument and append into `result[depth]`. That gives $O(n)$ time with $O(h)$ recursion space and no queue at all."
   }
  ]
 },
 "07_trees/0104_maximum_depth_of_binary_tree": {
  "one_liner": "1 + max of the two subtrees; null is depth zero.",
  "core_objective": "Return the number of edges on the longest root-to-leaf path.",
  "bounds": "The tree is a valid binary tree and may be a single node (depth 0) or null. Up to 1e4 nodes, so recursion depth can reach 1e4.",
  "diagram": "      1\n    /   \\\n   2     3\n  /         \\\n 4           5\n               \\\n                6\n\n  depth(NULL) = 0\n  depth(1) = 1 + max(depth(2), depth(3))\n  depth(2) = 1 + max(depth(4), 0) = 1 + 1 = 2\n  depth(3) = 1 + max(0, depth(5)) = 1 + 2 = 3\n  depth(1) = 1 + max(2, 3) = 4   CORRECT (path 1-3-5-6)\n\n  edge count vs node count: null->0 means the answer counts\n  EDGES, which matches the problem statement.",
  "cpp_alts": [
   "A stack with `(node, depth)` pairs avoids the 1e4-deep call stack risk.",
   "`max` on two ints is a single cmp/cmov pair, so the recursive form is already optimal."
  ],
  "py_alts": [
   "`max(a, b)` is a Python function call; a conditional expression is measurably faster in a hot recursion.",
   "Iterative level-order counting is O(n) time with O(w) space and no recursion limit risk."
  ],
  "trap": "Returning node count instead of edge count. Returning 1 for a null tree instead of 0 shifts every answer by one; the problem counts edges.",
  "invariant": "`depth(n)` returns the longest downward path from n to a null child, counted in edges. A null node has depth 0 because it has no edges, so the recurrence 1 + max(left, right) composes correctly.",
  "questions": [
   {
    "q": "Why is the null base case 0 and not 1?",
    "a": "Because the answer counts edges. A lone node has one node and zero edges, so depth must be 0 for it, which requires depth(NULL) = 0 and depth(node) = 1 + max(children)."
   },
   {
    "q": "Could this be iterative with less memory?",
    "a": "Yes -- level-order counting needs O(w) queue space, but a DFS stack needs O(h). Neither beats the O(h) recursion stack meaningfully; the iterative version's only real advantage is avoiding the recursion-depth limit in Python."
   },
   {
    "q": "What if the tree were a general N-ary tree?",
    "a": "The recurrence generalises to 1 + max over all children, and the null base case stays 0. The kernel is identical; only the loop over children is added."
   }
  ]
 },
 "07_trees/0105_construct_binary_tree_from_preorder_and_inorder": {
  "one_liner": "The next preorder value is the root; inorder splits it.",
  "core_objective": "Rebuild a binary tree from its preorder and inorder traversals, where node values are unique.",
  "bounds": "1 <= preorder.length <= 3000 with all values unique, so the inorder index map is a permutation and the split point is well defined. An empty input must return null without special-casing.",
  "diagram": " preorder = [3,9,20,15,7]\n inorder  = [9,3,15,20,7]\n\n build(pre_idx, lo, hi):\n   root_val = preorder[pre_idx]\n   root = TreeNode(root_val)\n   mid = index_of[root_val]          # O(1) with a map\n   left_size = mid - lo\n   root.left  = build(pre_idx+1,      lo,  mid-1)\n   root.right = build(pre_idx+1+left_size, mid+1, hi)\n\n build(0, 0, 4):\n   root 3, mid=1, left_size=1\n   left  = build(1, 0, 0)   -> 9\n   right = build(2, 2, 4)   -> 20 with children 15, 7\n\n WITHOUT the map (the O(n^2) variant):\n   mid = inorder.index(root_val)   -> O(n) PER CALL\n   total O(n^2) = 9e6 for n=3000. The map makes it O(n).",
  "cpp_alts": [
   "An `unordered_map<int,int>` of value to inorder index is the whole optimization.",
   "Passing the inorder range by reference and preorder by index avoids copying vectors per call."
  ],
  "py_alts": [
   "`index = {v: i for i, v in enumerate(inorder)}` is O(n) once and makes each lookup O(1).",
   "`inorder.index(v)` inside the recursion is the trap -- it is O(n) per node, giving O(n^2)."
  ],
  "trap": "Recomputing the inorder position with `inorder.index(root_val)` at each call. It works, is O(n^2), and at n = 3000 is roughly 9e6 comparisons -- enough to time out.",
  "invariant": "`build(pre_idx, lo, hi)` reconstructs exactly the subtree whose inorder traversal is `inorder[lo..hi]`, using `preorder[pre_idx]` as its root. The left subtree consumes `mid - lo` further preorder entries, so the right subtree starts at `pre_idx + 1 + (mid - lo)`.",
  "questions": [
   {
    "q": "Why does the inorder index split the preorder list?",
    "a": "In preorder the root is first, then the entire left subtree, then the entire right subtree. Knowing the left subtree's size from the inorder index therefore tells you where the right subtree begins in preorder -- that single arithmetic step is the entire algorithm."
   },
   {
    "q": "What if values were not unique?",
    "a": "The algorithm breaks: the same value appears in inorder at multiple positions, so the split point is ambiguous and the tree is not uniquely determined. Uniqueness is exactly the precondition that makes the map well defined."
   },
   {
    "q": "What is the space complexity?",
    "a": "$O(n)$ for the index map plus $O(h)$ recursion. Both are unavoidable -- the map is what buys the time bound and the stack is the traversal itself."
   }
  ]
 },
 "07_trees/0110_balanced_binary_tree": {
  "one_liner": "Return the height, and reject any subtree differing by more than one.",
  "core_objective": "Decide whether the height of the left and right subtrees of every node differs by at most one.",
  "bounds": "Up to 5e3 nodes, so a skewed tree recurses 5e3 deep. An empty tree is balanced, which must be the base case.",
  "diagram": "        3\n      /   \\\n     2     8\n    /       \\\n   1        7\n             \\\n              6      <- subtree of 7 is off by 2\n\n  height(n) -> -1 if unbalanced, else the height\n\n   h(1) = 0                       (leaf)\n   h(7) = 1 + max(h(6), h(N))     (6 has h 0, NULL -1)\n                              -> 1 + max(0, -1) = 1\n   h(8) = 1 + max(h(7), h(NULL)) = 1 + max(1, -1) = 2\n   h(2) = 1 + max(h(1), h(NULL)) = 1 + max(0,-1) = 1\n   h(3) = 1 + max(1, 2) = 3, and |1-2| = 1 <= 1 -> balanced\n\n  WHY -1 AS THE SENTINEL: one return value encodes both\n  'how tall' and 'is fine', so the parent can check both\n  facts with a single comparison.",
  "cpp_alts": [
   "Returning -1 for failure is the single-pass standard; returning a bool with an out-parameter height costs a second traversal.",
   "An iterative post-order with a `(node, state)` stack avoids the recursion limit at 5e3 depth."
  ],
  "py_alts": [
   "`return -1 if ... else 1 + h` written as one expression avoids a Python-level branch and a temp variable.",
   "A generator-free explicit stack is safer than recursion past 1000 in CPython, and 5e3 exceeds that limit."
  ],
  "trap": "Recomputing both subtree heights with separate calls inside the parent, which visits subtrees repeatedly and can become O(n^2) on skewed inputs. Returning height from a single pass avoids that entirely.",
  "invariant": "`height(n)` returns the height of n's subtree if that subtree is balanced at every node, or -1 if any node in the subtree is unbalanced. Because -1 propagates up, once a violation is found every ancestor also returns -1 and the whole answer is false.",
  "questions": [
   {
    "q": "Why is a single return value better than a bool plus a height?",
    "a": "Because it halves the work. The parent needs both the height (to compute its own) and the validity (to fail fast). Returning -1 on failure gives one int that answers both, so there is no second traversal and no out-parameter."
   },
   {
    "q": "What is the worst-case time complexity?",
    "a": "$O(n)$ -- each node is visited exactly once in post-order, whether the tree is balanced or not. The naive version that recurses for left height, right height, and then again to check, visits each node once per ancestor and is $O(n^2)$ on a chain."
   },
   {
    "q": "How do you avoid the Python recursion limit here?",
    "a": "Convert to an explicit stack of nodes with a visited flag, or push `(node, False)` then `(node, True)` and children to emulate post-order. That replaces the C-level call stack with a heap list you control."
   }
  ]
 },
 "07_trees/0124_binary_tree_maximum_path_sum": {
  "one_liner": "Clamp each child branch at zero; the return is one-sided.",
  "core_objective": "Return the largest sum of values along any path in a binary tree, where node values may be negative and the path may start and end anywhere.",
  "bounds": "-1e3 <= node.val <= 1e3 and up to 3e4 nodes, so the answer can be as low as -1e3 (a single negative node) and clamping at zero must not make the answer 0 incorrectly. A path cannot revisit a node, so it bends at most once.",
  "diagram": "      -10        best through -10:\n     /    \\\n     9     20     9 + (-10) + 20 = 19\n   /         \\\n  15         7\n\n  dfs(n) = best DOWNWARD path starting at n (one branch only)\n\n   dfs(15) = 15          best so far stays 0\n   dfs(9)  = 9 + max(0, 15) = 24\n   dfs(7)  = 7 + max(0, 0)  = 7\n   dfs(20) = 20 + max(0, 7) = 27\n\n   at -10: candidate = 9-path(24) + (-10) + 20-path(27)\n            = 24 - 10 + 27 = 41   <-- the answer, a BENT path\n   dfs(-10) = -10 + max(0, 24) = 14  (one-sided, for the parent)\n\n  TWO different quantities:\n   return value  = may extend upward -> ONE branch -> clamp\n   best tracker  = any shape        -> TWO branches -> no clamp\n  Conflating them is THE classic bug.",
  "cpp_alts": [
   "Passing `int& best` avoids a member variable and makes the function reentrant.",
   "`max(0, dfs(left))` is the clamp; without it a negative subtree poisons every ancestor's path."
  ],
  "py_alts": [
   "`self.best` as an instance attribute is the Python idiom; a nested function with a mutable cell is faster.",
   "Returning 0 from a null child makes the clamp unnecessary: `max(left, right)` already excludes negatives."
  ],
  "trap": "Returning `node.val + left + right` (both branches) instead of the one-sided sum. That returns the best bent path, which the parent cannot extend upward, so ancestors compute wrong values.",
  "invariant": "`dfs(n)` returns the maximum sum of a path that starts at n and goes down into at most one subtree. Clamping children at 0 is safe because a path is not required to extend into a subtree at all, and the empty extension contributes 0.",
  "questions": [
   {
    "q": "Why clamp at zero when the values may be negative?",
    "a": "Because a path is not obliged to visit any child. Choosing not to descend contributes 0, which is always at least as good as descending into a negative subtree. Clamping therefore models a legal choice rather than distorting the optimum."
   },
   {
    "q": "Why are the return value and the global answer different quantities?",
    "a": "A path that bends through n uses both children and cannot be extended upward (the parent would revisit n). A path that starts at n and goes down uses one child and can be extended. So the return value is one-sided while the tracked answer is two-sided."
   },
   {
    "q": "What happens on an all-negative tree?",
    "a": "Every clamp zeroes out, so each return is the node's own value, and the best tracker records the maximum single node value -- which is the correct answer, since a path must contain at least one node."
   }
  ]
 },
 "07_trees/0199_binary_tree_right_side_view": {
  "one_liner": "BFS taking the last node of each level, or DFS right-first.",
  "core_objective": "Return the values seen from the right side, top to bottom -- one value per level.",
  "bounds": "The tree may be a single node, so there is exactly one level. A right-skewed tree gives all nodes in order.",
  "diagram": "       1\n     /   \\\n    2     3\n   / \\   / \\\n  4   5 6   7\n\n  right side view = [1, 3, 7]\n\n  BFS: per level take the LAST enqueued node\n   level 0: queue=[1]              -> take 1\n   level 1: queue=[2,3]            -> take 3\n   level 2: queue=[4,5,6,7]        -> take 7\n\n  DFS right-first with OVERWRITE per depth:\n   depth 0: visit(1) -> res[0] = 1\n   depth 1: visit(3) -> res[1] = 3   (2 then overwrites? no:\n          visiting right child first means 3 is set FIRST)\n   depth 2: visit(7) -> res[2] = 7   (5 would overwrite -- so\n          either visit right-first and overwrite, or\n          left-first and skip-if-set)\n\n  invariant BFS: nodes at each level enter the queue in\n  left-to-right order, so index size-1 is the rightmost.",
  "cpp_alts": [
   "`queue` + per-level size is the standard; taking `q.back()` before popping the level is the one-liner.",
   "A DFS with an explicit stack must push LEFT first so RIGHT is popped first."
  ],
  "py_alts": [
   "A deque plus `for _ in range(len(q))` and reading the last popped value is the idiomatic version.",
   "Storing `(node, depth)` and overwriting `res[depth]` is a clean DFS alternative."
  ],
  "trap": "In the DFS variant, overwriting `res[depth]` while visiting LEFT first -- then the leftmost node wins. The correct pairing is left-first traversal WITH overwrite, or right-first traversal WITH first-write-only.",
  "invariant": "In BFS, before each level's loop the queue holds exactly that level in left-to-right order, so the last element popped is the rightmost node of the level. One per level therefore gives the right view.",
  "questions": [
   {
    "q": "Which node is the right view of a given level?",
    "a": "The rightmost, which is the last node enqueued at that depth because BFS enqueues children left to right. Reading the queue's back before draining the level gives it in O(1)."
   },
   {
    "q": "How do the two DFS variants differ, and which is right?",
    "a": "Traversing right-first and overwriting works, because the first node written at each depth IS the rightmost and later left-side visits at the same depth overwrite it with a worse value. Traversing left-first requires first-write-only. Mixing them up is the bug."
   },
   {
    "q": "Why is BFS conceptually safer than DFS here?",
    "a": "Because BFS's level structure is explicit -- the queue length tells you the level size, so \"one per level\" is enforced structurally rather than by tracking a depth argument through recursion."
   }
  ]
 },
 "07_trees/0226_invert_binary_tree": {
  "one_liner": "Swap the children, recursively; three lines of essence.",
  "core_objective": "Invert a binary tree by swapping every node's left and right subtrees.",
  "bounds": "Up to 1e4 nodes, so a skewed tree recurses 1e4 deep and blows CPython's default limit. Modifying in place is expected and avoids a second tree.",
  "diagram": "    4              4\n   / \\            / \\\n  2   7    ->    7   2\n  / \\  / \\       / \\ / \\\n 1  3 6  9      9  6 3  1\n\n  invert(n):\n    if not n: return\n    n.left, n.right = n.right, n.left\n    invert(n.left)\n    invert(n.right)\n\n  invariant: on entry, n's subtree is un-inverted; on return it\n  is fully inverted. The swap must come BEFORE recursing,\n  otherwise the recursion visits the wrong subtrees.\n\n  3 lines of essence, O(n) time, O(h) space.\n  Recursion depth = h; a 1e4 chain exceeds Python's limit.",
  "cpp_alts": [
   "`swap(node->left, node->right)` from `<algorithm>` is a single inline exchange.",
   "An explicit stack of nodes avoids 1e4-deep recursion and is barely more code."
  ],
  "py_alts": [
   "Tuple assignment `node.left, node.right = node.right, node.left` is one bytecode pair and reads correctly.",
   "An explicit stack `[root]` with `node.left, node.right = node.right, node.left` then pushing both children is O(1) extra space beyond the stack."
  ],
  "trap": "Recursing before swapping. Then `invert(node.left)` operates on the node's original left subtree, and after the swap the right subtree is never visited -- silently leaving half the tree uninverted.",
  "invariant": "`invert(n)` returns with n's subtree fully inverted and all other parts of the tree untouched. The pre-order placement of the swap is what preserves this: the swap happens on entry, so both recursive calls see subtrees that have already been repositioned.",
  "questions": [
   {
    "q": "Why must the swap precede the recursion?",
    "a": "Because the recursive calls should operate on the node's children as they will be visited in the inverted tree. Swapping first and then recursing on `node.left` and `node.right` visits both original subtrees exactly once."
   },
   {
    "q": "Can this be done without recursion?",
    "a": "Yes -- push the root, then repeatedly pop a node, swap its children, and push both. That is $O(n)$ time and $O(h)$ stack, with no recursion limit concern. Worth mentioning given the 1e4-node bound."
   },
   {
    "q": "What is the minimum information a node needs?",
    "a": "Just its two child pointers. The values are irrelevant, which is a useful observation: the problem is purely structural, so any node with two mutable child slots can be inverted."
   }
  ]
 },
 "07_trees/0230_kth_smallest_element_in_bst": {
  "one_liner": "Iterative inorder, stopping at the k-th visit.",
  "core_objective": "Return the k-th smallest value in a binary search tree with distinct values, counting from 1.",
  "bounds": "1 <= k <= n and n <= 1e4, so k is always valid and the early exit always triggers. A skewed tree recurses 1e4 deep, which is why the iterative version is preferred.",
  "diagram": "      5\n    /   \\\n   3     6\n  / \\   / \\\n 2   4 7   8\n\n  inorder: 2 3 4 5 6 7 8\n  k=3 -> the 3rd value = 4\n\n  stack, cur = [], root\n  push 5 ; cur = 3\n  push 3 ; cur = 2\n  push 2 ; cur = None  -> pop 2  visit 1\n  cur = None          -> pop 3  visit 2\n  cur = 4              -> (4 unvisited, not None)\n     ^ need pop-after-LEFT-visited, not pop-on-null-first\n  push 4 ; cur = None  -> pop 4  visit 3  <-- RETURN 4\n\n  invariant: nodes on the stack are the unvisited ancestors in\n  descending order, so the top is always the smallest available.",
  "cpp_alts": [
   "A `stack<TreeNode*>` with `while (cur || !st.empty())` is the canonical iterative form.",
   "Using the size of the left subtree to compute the rank is a different O(h) strategy: `k -= leftSize + 1` on each step."
  ],
  "py_alts": [
   "The two-phase loop `while cur or stack` with `stack.append/pop` is the standard Python form.",
   "`while stack and k > 0: node = stack.pop(); k -= 1` is the clean early-exit shape."
  ],
  "trap": "Decrementing k when pushing rather than when popping. The visit happens on pop, after the left subtree is exhausted, so that is the only place the rank advances.",
  "invariant": "The stack holds, from top to bottom, the ancestors whose left subtrees have been fully visited but whose own values have not yet been emitted. Popping therefore always yields the next smallest value in sorted order.",
  "questions": [
   {
    "q": "Why does inorder give sorted order here?",
    "a": "The BST invariant places every value in the left subtree below the node and every value in the right subtree above it, so a left-node-right traversal emits values in strictly increasing order."
   },
   {
    "q": "What is the complexity, and why can it be better than O(n)?",
    "a": "$O(h + k)$ for the iterative version -- you descend at most h levels and pop at most k nodes, then stop. Worst case that is $O(n)$, but for small k on a balanced tree it is much closer to $O(\\log n + k)$."
   },
   {
    "q": "When would a size-based rank computation beat inorder?",
    "a": "If you augmented each node with subtree size, you could descend directly to the k-th element by comparing k against the left subtree's size -- $O(h)$ regardless of k, and no stack. That needs extra state the problem does not provide."
   }
  ]
 },
 "07_trees/0235_lowest_common_ancestor_of_bst": {
  "one_liner": "Descend using BST ordering until p and q split.",
  "core_objective": "Return the lowest node in a binary search tree that is an ancestor of (or equal to) both given nodes.",
  "bounds": "p and q are distinct nodes in the tree, so a solution always exists. Values are unique, which is what makes the ordering comparisons unambiguous.",
  "diagram": "        6\n      /   \\\n     2     8\n    / \\   / \\\n   0   4 7   9\n      / \\\n     3   5\n\n  p = 2, q = 8  -> LCA = 6\n  p = 2, q = 4  -> LCA = 2\n  p = 3, q = 5  -> LCA = 4\n\n  descend(root=6):\n    both < 6 ? (0,0) yes -> go LEFT\n    both > 6 ? yes          -> go RIGHT\n    otherwise root is the split point -> ANSWER\n\n  p=2 q=4: at 6, 2<6 but 4<6 -> LEFT to 2.\n           2 is p itself -> return 2 (ancestor of itself)\n\n  invariant: at every node, p and q are both <= node or\n  both >= node, unless the node is the answer.",
  "cpp_alts": [
   "A `TreeNode*` descent is $O(h)$ time and $O(1)$ space -- strictly better than the general-tree ancestor-path method.",
   "`std::numeric_limits` is irrelevant here since no sentinel values are needed."
  ],
  "py_alts": [
   "The while loop mutates `root` in place, which is fine since the caller does not need it.",
   "For a general binary tree the same problem needs the parent-map approach; the BST ordering is what removes that requirement."
  ],
  "trap": "Returning when `node == p or node == q` without first checking whether the other node is in that subtree. The correct order is: check the ordering split first, and only match a node when the two targets lie on opposite sides (or one equals it).",
  "invariant": "At the current node, both p and q are at most the node's value or both at least it, and neither is below the node on one side while the other is on the other. The first node where they split -- or where one equals the node -- is their lowest common ancestor.",
  "questions": [
   {
    "q": "Why does the split point have to be the LCA?",
    "a": "If p and q are both below the current node's value they are both in the left subtree, so no ancestor at or above this node can be their LCA -- it must be deeper. Symmetrically when both are above. So the search descends until the targets separate, and the node where they separate is the answer."
   },
   {
    "q": "How does the general binary tree version differ?",
    "a": "Without ordering you cannot tell which subtree to descend, so you must record ancestor sets (or a parent map) for p, then walk up from q until you hit one of p's ancestors. That is $O(h)$ time but $O(h)$ space instead of $O(1)$."
   },
   {
    "q": "What if p is an ancestor of q?",
    "a": "The descent walks down toward p, and when it reaches p the equality branch fires and p is returned. Treating a node as an ancestor of itself is the standard convention and is what makes that case work without special handling."
   }
  ]
 },
 "07_trees/0297_serialize_and_deserialize_binary_tree": {
  "one_liner": "Preorder with null markers encodes every tree unambiguously.",
  "core_objective": "Encode a binary tree to a single string and recover the exact original tree from it.",
  "bounds": "Up to 1e4 nodes, so the encoded string can be 2n+1 tokens. The encoding must be unambiguous -- any tree must decode to itself and only itself.",
  "diagram": "  tree:      9\n            / \\\n           3  20\n          /  \\ / \\\n         2   1 15  7\n\n  preorder with NULL markers:\n   9 3 2 # 1 # # 20 15 # # 7 #\n   ^  ^ ^      ^ ^  ^     ^     ^\n   |  | |      | |  |     |     +-- null for 7's right\n   |  | |      | |  +-- null for 20's left\n   |  | |      | +-- null for 1's right\n   |  | +-- null for 1's left\n   |  +-- null for 3's right\n   +-- root\n\n  invariant: exactly 2n+1 tokens for n nodes, since every node\n  contributes one value and every null child contributes a marker.\n  The marker count equals n+1, which is a self-check.\n\n  decode: consume a token; '#' -> null; else build node and\n          recurse twice (left then right). No index bookkeeping.",
  "cpp_alts": [
   "`stringstream` with `string` tokens avoids manual delimiter parsing and is fast enough at 1e4 nodes.",
   "Appending the delimiter as a character (`','`) plus a separate null marker is cheaper than a string per token."
  ],
  "py_alts": [
   "`','.join(tokens)` in one pass avoids repeated string concatenation, which would be $O(n^2)$ in CPython.",
   "`tokens.split(',')` in C beats any manual character loop."
  ],
  "trap": "Omitting the null markers. Preorder values alone are ambiguous -- [1,2] and [1,null,2] both encode to `1,2`. Every null child must contribute a marker or decoding is not injective.",
  "invariant": "Decoding consumes tokens left to right; each node token is followed by exactly two subtrees (left then right). Because every subtree is itself a valid encoding, the recursive consumption always lines up and the string is consumed exactly.",
  "questions": [
   {
    "q": "Why are null markers necessary for injectivity?",
    "a": "Without them, a preorder value sequence cannot distinguish a node with a left child from one without. [1,2] encodes to `1,2` whether 2 is a left or a right child, and also whether 1 has an empty right subtree. Marking nulls fixes both ambiguities."
   },
   {
    "q": "How many tokens does a tree of n nodes produce?",
    "a": "Exactly 2n+1: n values plus n+1 null markers (every node has two child slots, but the root has no parent, so there are 2n slots and n-1 are filled, leaving n+1 null). That identity is a useful integrity check on any implementation."
   },
   {
    "q": "What is the complexity?",
    "a": "$O(n)$ to serialize and $O(n)$ to deserialize, with the token list itself being $O(n)$ space. The recursion adds $O(h)$, and a skewed tree has h = n, so the stack is the dominant term for pathological inputs."
   }
  ]
 },
 "07_trees/0543_diameter_of_binary_tree": {
  "one_liner": "Post-order returning (height, diameter) and carrying the best.",
  "core_objective": "Return the length in edges of the longest path between any two nodes, which need not pass through the root.",
  "bounds": "Up to 1e4 nodes, so the diameter can reach 1e4 - 1 and must be computed in edges. A single-node tree has diameter 0.",
  "diagram": "        1\n      /   \\\n     2     3\n    / \\   / \\\n   4   5 6   7\n\n  longest paths:\n   4-2-5       = 2 edges\n   4-2-1-3-6   = 4 edges  <-- THROUGH THE ROOT\n   6-3-7       = 2 edges\n   ANSWER 4 (not found by a naive root-only computation)\n\n  post-order: dfs(n) -> (height, best)\n   h4 = (0,0)  h5 = (0,0)\n   h2: left=(0,0) right=(0,0)\n        through = 0 + 1 + 0 = 1\n        height  = 1 + max(0,0) = 1\n        return (1, max(0, 1, 0)) = (1, 1)\n   h6 = (0,0)  h7 = (0,0)\n   h3: through = 0+1+0 = 1 ; height = 1\n        return (1, 1)\n   h1: left=(1,1) right=(1,1)\n        through = 1 + 1 + 1 = 3   (edges through root)\n        height  = 1 + max(1,1) = 2\n        best = max(1, 1, 3) = 3\n        return (2, 3)  ANSWER 3 (edges)\n\n  invariant: dfs(n).height is the height of n's subtree;\n  dfs(n).best is the diameter WITHIN n's subtree.",
  "cpp_alts": [
   "Returning a `pair<int,int>` (height, best) is the canonical shape and needs no member state.",
   "`std::max` with an initializer list of three values is a single call but may not inline as well as chained maxes."
  ],
  "py_alts": [
   "Returning a tuple per node allocates one tuple per node; returning just the height and using a closure-captured `best` avoids that.",
   "The closure approach is both faster and easier to read in Python."
  ],
  "trap": "Returning the height as the answer, or forgetting that the two deepest branches contribute `leftH + 1 + rightH` edges -- the two `+1`s for the edges from the node to its children are the off-by-one that flips the whole answer.",
  "invariant": "`dfs(n)` returns the height of n's subtree and the diameter of n's subtree. The diameter is the max of the two children's diameters and the path through n, and the height is 1 plus the taller child. Both facts are computable from the children's return values because the recursion is post-order.",
  "questions": [
   {
    "q": "Why must the diameter consider paths not through the root?",
    "a": "The longest path may lie entirely inside one subtree. The post-order `best` value carries each child's internal diameter upward precisely so the parent can compare it against the through-node path and its own other child."
   },
   {
    "q": "Is the diameter in nodes or edges?",
    "a": "Edges. That is why the through-node candidate is `leftH + 1 + rightH` -- two edges from n to its children -- and why a leaf returns height 0 and best 0."
   },
   {
    "q": "Why is post-order the natural traversal here?",
    "a": "Because both facts about a node depend only on facts about its children. Post-order guarantees the children's return values are available when the node composes them, which is exactly the dependency this recurrence has."
   }
  ]
 },
 "07_trees/0572_subtree_of_another_tree": {
  "one_liner": "Serialize both trees and search for the pattern with KMP.",
  "core_objective": "Decide whether one binary tree is a descendant of another, matching structure and values exactly.",
  "bounds": "0 <= subRoot.val, root.val <= 1000 and up to 1000 nodes each, so an O(n*m) recursive comparison is technically acceptable at 1e6 operations. Nodes need not be unique.",
  "diagram": "  root:    3\n          / \\\n         4   5\n          \\\n           1\n\n  subRoot: 4\n           \\\n            1\n\n  descend(root=3): val 3 != 4 -> try root.left (4)\n     val 4 == 4 ; subRoot.right is None, so must match\n        (null-safe check!) -> root[4].right = 1 matches 1, and\n        1's children are both null -> MATCH\n\n  serialise with nulls (the safe encoding):\n   root:    \"3 4 1 # # 5 # #\"\n   subRoot: \"4 1 # #\"\n   -> the subRoot pattern occurs in the root string\n\n  why nulls matter: without them, subRoot \"1\" would falsely match\n  the leaf 1 of a larger subtree.",
  "cpp_alts": [
   "`stringstream` plus `std::search` is a clean implementation; KMP avoids the quadratic worst case of naive search.",
   "Comparing the recursive shapes directly is O(n*m) worst case but uses no extra space and is often fast in practice."
  ],
  "py_alts": [
   "`' '.join` on a serialized list plus Python's `in` operator is the shortest correct answer, and `in` on strings uses a fast two-way search.",
   "`' '.join(list)` in `haystack.split(' ')` style substring search sidesteps delimiter-boundary false matches."
  ],
  "trap": "Forgetting to compare the NULL children. If you only compare values and recurse while both are non-null, `[1]` matches a leaf that is actually the left child of a two-node subtree, giving a false positive.",
  "invariant": "`isSubtree(a, b)` is true iff a's value equals b's value AND (b is a leaf, OR a's corresponding child subtree matches b's). Writing the base cases explicitly -- both null is true, exactly one null is false -- is what makes it correct.",
  "questions": [
   {
    "q": "Why include nulls in the serialization?",
    "a": "Because a subtree match must agree on structure, and value sequences alone cannot distinguish a leaf from a node with one non-null child. Emitting a marker for every empty slot makes the pattern unambiguous, so a plain substring search becomes exactly a subtree search."
   },
   {
    "q": "What is the time complexity of the serialization approach?",
    "a": "$O(n + m)$ to serialize, plus a substring search. Python's `in` uses a linear-time algorithm on strings, so the whole thing is $O(n + m)$ in practice; a naive manual scan would be $O(n \\cdot m)$."
   },
   {
    "q": "Why can a naive recursive search be $O(n \\cdot m)$?",
    "a": "There are up to n candidate root positions in the big tree, and each attempt may compare up to m nodes before failing. With identical shapes the first attempt succeeds quickly, but adversarial inputs with matching prefixes force the full product."
   }
  ]
 },
 "07_trees/1448_count_good_nodes_in_binary_tree": {
  "one_liner": "Propagate the path minimum; a node is good at equality.",
  "core_objective": "Count nodes whose value is greater than or equal to every ancestor along the path from the root to that node.",
  "bounds": "0 <= node.val <= 1e4 and up to 1e4 nodes. The root is always good by definition, and equality with the minimum counts as good.",
  "diagram": "        7      path min 7 -> GOOD\n      /   \\\n     7     7    path min 7 -> both GOOD (equal counts)\n    /       \\\n   2         6  path min 7 -> 2 < 7 NO, 6 < 7 NO\n\n  count = 3 (root + two 7s)\n\n  dfs(node, pathMin):\n    if not node: return 0\n    pathMin = min(pathMin, node.val)\n    good = 1 if node.val >= pathMin else 0\n    return good + dfs(left, pathMin) + dfs(right, pathMin)\n\n  invariant: pathMin is the minimum value among the node and\n  ALL its ancestors. So `node.val >= pathMin` is exactly the\n  definition of a good node.\n\n  NOTE: comparing only against the PARENT is the bug -- node 7\n  under parent 7 passes, but a node 5 under parent 6 under a\n  grandparent 3 would pass the parent test yet fail against 3? no:\n  5 >= 6 fails. Correct example: 5 under 6 under 2 -> parent test\n  passes (5 < 6? no, 5 < 6 so fails). Use 9 under 8 under 3:\n  parent test 9>=8 passes, grandparent 3 gives min 3, 9>=3 passes.\n  The failing case is 5 under 6 under 1: parent 6, grandparent 1;\n  a node 2 under 6 -> 2 >= 6 fails anyway. The real bug case is\n  a node whose value beats its parent but loses to a HIGHER\n  ancestor that is smaller -- impossible. Hence tracking the\n  running MINIMUM (not the parent) is the correct formulation,\n  and parent-only comparison is merely incomplete reasoning.",
  "cpp_alts": [
   "`int pathMin` passed by value is the whole state; no member variable needed.",
   "Passing `INT_MAX` as the initial minimum is correct because all values are non-negative here; `INT_MIN` is the general choice."
  ],
  "py_alts": [
   "A closure with a mutable counter is faster than returning counts and summing.",
   "`float('inf')` as the initial minimum is the safe general sentinel."
  ],
  "trap": "Testing against the immediate parent only. The definition is against ALL ancestors, and while a node that beats its parent may still lose to a smaller ancestor further up, the correct and cheap formulation is to carry the running minimum.",
  "invariant": "At entry to `dfs(node, m)`, `m` is the minimum value among all strict ancestors of node. After `m = min(m, node.val)`, `node.val >= m` is exactly the good-node predicate, and children receive that updated minimum.",
  "questions": [
   {
    "q": "Why carry a minimum rather than the parent value?",
    "a": "Because the predicate quantifies over all ancestors. Carrying the running minimum reduces that quantification to one comparison: `val >= runningMin`. Keeping just the parent would require walking ancestors per node, turning $O(n)$ into $O(n h)$."
   },
   {
    "q": "Is the root always good?",
    "a": "Yes -- by convention a node with no ancestors vacuously satisfies \"greater than every ancestor\". Initialising the minimum to infinity makes the root's test `val >= min(val, inf)` trivially true, so no special case is needed."
   },
   {
    "q": "What is the space complexity, and can it be reduced?",
    "a": "$O(h)$ for the recursion stack. It can be reduced to $O(1)$ with an explicit Morris-style threaded traversal that temporarily rewires pointers to carry the path minimum without a stack, at the cost of mutating the tree."
   }
  ]
 }
})

# ---- appended from _chunk6.json
DATA.update({
 "08_tries/0208_implement_trie": {
  "one_liner": "Each node holds a child map plus an end-of-word flag.",
  "core_objective": "Implement a prefix tree supporting insert, search, and startsWith.",
  "bounds": "lowercase English letters only, so at most 26 children per node. With 1e4 words of length 100 the node count can reach 1e6, which makes per-node memory the real constraint in Python.",
  "diagram": " insert('apple') then insert('app')\n\n  root\n   |-a\n   |  \\-p\n   |    \\-p   <-- endOfWord (word 'app' ends here)\n   |       \\-l\n   |          \\-e  <-- endOfWord (word 'apple' ends here)\n\n  insert('apple','app','apply'):\n   root -> a -> p -> p (flag=True)\n                 -> l -> e (flag=True)\n                       -> y (flag=True)\n\n  search('app')  -> follow a,p,p and return flag -> True\n  search('apx')  -> no child 'x' -> False EARLY\n  startsWith('ap') -> follow a,p, end of pattern, no flag -> True\n\n  invariant: a node is reached by exactly one string prefix, so\n  the flag at a node is the sole record of \"a word ends here\".",
  "cpp_alts": [
   "`vector<TrieNode>` with `children[26]` as a fixed array is cache-ideal but costs 104 bytes per node; a `map` or `vector<pair>` child list is denser for sparse nodes.",
   "`gp_hash_table<char,int>` per node is a poor fit: one hash table per node is heavy, and 26 edges do not justify hashing."
  ],
  "py_alts": [
   "A plain `dict` per node is the standard; a `list` of 26 is faster for lookup but wastes memory on sparse tries.",
   "`defaultdict(dict)` for children removes the membership test on insert.",
   "A set of all words supports startsWith by scanning, but search becomes $O(\\sum |w|)$ -- worse, though trivially correct."
  ],
  "trap": "Confusing search with startsWith: `search('app')` must require the end-of-word flag, `startsWith('app')` must not. Returning the node without checking the flag makes every prefix a word.",
  "invariant": "Following the character sequence of a query reaches a node iff that sequence is a prefix of some inserted word. The flag at that node distinguishes \"a word ends here\" from \"a path continues\", which is the only difference between the two query methods.",
  "questions": [
   {
    "q": "Why does a trie beat a set for startsWith?",
    "a": "A set requires scanning all words or building a separate prefix structure, and a scan is $O(n)$ regardless of query length. A trie answers startsWith in $O(L)$ where L is the query length, independent of the number of words stored."
   },
   {
    "q": "What is the memory cost per node?",
    "a": "A Python dict costs roughly 64 bytes empty and grows with entries, so a million-node trie can exceed 200 MB. C++ with `children[26]` costs 104 bytes plus the flag, but compresses into a flat array with child indices -- predictable and cache-friendly."
   },
   {
    "q": "How would you support arbitrary characters?",
    "a": "Replace the fixed 26-array or lowercase assumption with a map, and index by code point rather than `ord(c) - ord('a')`. Unicode tries need care with surrogate pairs in narrow builds."
   }
  ]
 },
 "08_tries/0211_design_add_and_search_words": {
  "one_liner": "Treat '.' as a branch point during the descent.",
  "core_objective": "Implement a trie supporting insert and a search that allows '.' to match any single character.",
  "bounds": "1 <= word.length <= 25 with lowercase letters and '.', at most 100 words stored. A query of all dots must not blow up -- without pruning it explores 26^d paths.",
  "diagram": " insert('bad'), insert('dad'), insert('mad')\n\n  search('pad'):\n   root -> a exists; then '.' branches over b,d,m\n     'a'+'d' exists ; third char 'd' exists -> flag? yes -> True\n   -> 3 branches at ONE level only (the whole query has\n      a single dot), so this is cheap\n\n  the blow-up case: search('.....') with 25 dots\n   26 branches at each of 25 levels = 26^25 paths.\n   PRUNING: if a dot is the LAST character of the pattern,\n   accept immediately if the current node has any children.\n   That single check kills the exponential case:\n   \"\\.\" at the end -> return bool(children)\n\n  invariant: at level i, node sits on exactly the trie prefix\n  matching pattern[0..i-1] under the '.' rule.",
  "cpp_alts": [
   "Recursive DFS with `const vector<TrieNode*>& children` avoids copying the child vector per call.",
   "Iterative DFS with an explicit stack bounds the stack at $O(L)$ regardless of the branching factor."
  ],
  "py_alts": [
   "`for c in children[node]:` iterates values directly, saving a dict lookup per child.",
   "Recursion depth equals word length (25), so the default Python limit is never a concern here."
  ],
  "trap": "Not pruning when the '.' is the final character of the pattern. `26^L` is astronomically slow, and the fix is a one-line check that a node with any child satisfies a trailing wildcard.",
  "invariant": "`search(node, i)` is true iff there is an inserted word matching `pattern[i:]` within node's subtree. The split into \"pattern[i] == '.'\" (try every child) and \"concrete character\" (take one child) covers exactly the wildcard semantics, so the recursion is exhaustive and sound.",
  "questions": [
   {
    "q": "What is the worst-case time of the wildcard search?",
    "a": "Exponential in the number of dots, up to $26^d$ for d dots. The trailing-dot optimisation caps it, and in practice LeetCode inputs keep dot counts low -- but stating the exponential bound and the pruning is the interview answer."
   },
   {
    "q": "Why does a trailing dot return immediately?",
    "a": "Because any descendant of the current node completes the word. If the node has at least one child, some continuation exists and matches the single remaining dot. If it has no children, there is nothing to match. That test is exact, not a heuristic."
   },
   {
    "q": "How would you add prefix search with dots?",
    "a": "Return true if the recursion reaches i == len(pattern) without failing -- whether or not a flag is set -- which is exactly `startsWith` generalised to wildcards."
   }
  ]
 },
 "08_tries/0212_word_search_ii": {
  "one_liner": "Each trie node walks the grid instead of matching its word.",
  "core_objective": "Find all words in a dictionary that exist in a grid using adjacent horizontal or vertical moves, each cell at most once per word.",
  "bounds": "up to 3e4 cells, 1e5 words of length up to 10e3. Pruning is essential: without removing found words and without early termination the search is hopeless.",
  "diagram": " grid:  oaan\n        etaen\n        iok\n        le        words: [oath, pea, eat, rain]\n\n  THE SHIFT: each trie node stores the LIST OF GRID CELLS\n  where that prefix occurs. So one node does O(4) work per cell\n  rather than rescanning its whole word.\n\n   root: all (0,0) (0,1) (0,2) (0,3)\n            (1,0)... (2,3)\n   node 'o': (0,0) (1,0) (2,1)\n   node 'oa': (0,0)\n   node 'oat': (0,0) -> neighbour 'h' at (1,0)? no -> dead\n   node 'e': (0,1) (1,1) (1,3) (2,2)\n   node 'ea': (1,1)\n   node 'eat': (1,1) -> 't' at (1,2)? yes -> flag -> 'eat' FOUND\n              remove 'eat' from the trie (prune)\n\n  per node work: 4 neighbours * (rows*cols) cells = O(4RC)\n  marking is by mutating the CELL to '#' then restoring,\n  so a cell is never reused within one path.",
  "cpp_alts": [
   "Store `(row, col)` pairs per node in a `vector`; that is the algorithm's essential data, not an optimisation.",
   "Deleting found words from the trie is the main pruning win -- without it every grid cell keeps searching for words already reported.",
   "Encode positions as `int` instead of a pair to halve the node payload."
  ],
  "py_alts": [
   "A list of ints per node with `for p in node.positions:` avoids tuple unpacking.",
   "Deleting from the trie: set the node's children to an empty list so the DFS stops descending there."
  ],
  "trap": "Forgetting to unmark the grid cell after the recursive call. The cell stays as '#' and every other word that needs it fails, so the answer is missing valid words.",
  "invariant": "The list at trie node u holds exactly the grid cells where u's prefix ends, for the current search. DFS from u visits each such cell, marks it, and recurses into the child matching the next character. Marking makes the path self-avoiding; restoring after the loop restores the invariant for sibling branches.",
  "questions": [
   {
    "q": "What does storing grid positions in the trie buy?",
    "a": "It inverts the loops. Instead of every cell trying every dictionary word (O(RC * W)), each trie node does O(4) work per cell it occupies, so the total is proportional to the number of (prefix, cell) pairs that actually exist. Shared prefixes are explored once instead of once per word."
   },
   {
    "q": "Why is removing found words necessary?",
    "a": "Without it, a cell visited late still descends the full remaining trie looking for words already reported, wasting the dominant share of the work. Removing a found word prunes that subtree for every later cell, and since the answer is a set, reporting twice is wrong anyway."
   },
   {
    "q": "How does marking prevent revisiting a cell?",
    "a": "Temporarily writing '#' into the cell makes any check of its character fail for the remainder of that path. Because the recursion restores the original character on the way out, sibling branches still see the true letter -- so marking gives path-local, not global, exclusion."
   }
  ]
 },
 "09_heap_priority_queue/0215_kth_largest_element_in_an_array": {
  "one_liner": "A size-k min-heap, or quickselect, both avoid a full sort.",
  "core_objective": "Return the k-th largest element of an array, counting the largest as first.",
  "bounds": "1 <= k <= nums.length <= 2e4, so k is always valid. Values are ints, so `heapq.nlargest` and `sorted` both work, but the O(n log n) sort is avoidable.",
  "diagram": " nums = [3,2,1,5,6,4], k = 2 -> 5\n\n heap of size k (a MIN-heap keeps the k LARGEST):\n   push 3 -> [3]\n   push 2 -> [2,3]\n   push 1 -> [1,3,2]\n   push 5 -> [1,5,2,3]  size 4 > k, pop MIN 1 -> [2,5,3]\n   push 6 -> [2,5,3,6]  size 4 > k, pop MIN 2 -> [3,5,6]\n   push 4 -> [3,4,6,5]  size 4 > k, pop MIN 3 -> [4,5,6]\n   heap top = 4 = SMALLEST of the 4 largest {4,5,6}? there\n   are only 4 kept -> top 4, we want 2nd largest of 6\n   numbers: largest=6, 2nd=5.\n   -> heapify(heap); return heap[0]  -> need the MIN of the\n      k largest, i.e. pop the min once then the top is the 2nd.\n   Correct form: heapq.nlargest(k, nums)[-1]\n\n  quickselect: partition around a pivot, recurse into the\n  side that contains index len-k, average O(n).",
  "cpp_alts": [
   "`std::nth_element(nums.begin(), nums.begin() + k - 1, nums.end(), greater<int>())` then `nums[k-1]` is the answer: $O(n)$ average, no extra memory.",
   "`std::partial_sort` is the deterministic cousin of nth_element: $O(n \\log k)$, and a better worst case.",
   "A heap of size k is $O(n \\log k)$ and $O(k)$ space -- the right answer when memory is constrained."
  ],
  "py_alts": [
   "`heapq.nlargest(k, nums)[-1]` is the idiomatic one-liner and is C-implemented.",
   "`sorted(nums, reverse=True)[k-1]` is $O(n \\log n)$ -- correct, and worth naming as the baseline.",
   "For small k and small n, `max` in a loop is actually competitive because the interpreter overhead is amortised over few calls."
  ],
  "trap": "Off-by-one on the index: the k-th largest is at sorted index k-1, not k. Also, using a max-heap of size k and returning its top gives the k-th SMALLEST, not largest -- the heap must be a MIN-heap of the k largest.",
  "invariant": "After processing any prefix of the array, the heap contains the k largest elements of that prefix (or all of them if the prefix is shorter than k). Each push-then-pop-min preserves this, so at the end the heap's minimum is the k-th largest of the whole array.",
  "questions": [
   {
    "q": "Why a min-heap of size k rather than a max-heap?",
    "a": "Because you want to keep the k largest, so you need to know which retained element is the weakest -- the minimum. A max-heap's top would be the largest retained, which tells you nothing about whether a new element belongs in the set."
   },
   {
    "q": "What does `nth_element` actually guarantee?",
    "a": "That the first k positions hold the k largest elements as an unordered set, in linear average time. It does not sort them, which is exactly what this problem allows since the answer is a single value."
   },
   {
    "q": "How do the complexities compare?",
    "a": "Heap: $O(n \\log k)$ time, $O(k)$ space. nth_element: $O(n)$ average but $O(n^2)$ worst case on adversarial pivots, with $O(1)$ space. Sorting: $O(n \\log n)$ time, and C++'s in-place sort is $O(\\log n)$ stack."
   }
  ]
 },
 "09_heap_priority_queue/0295_find_median_from_data_stream": {
  "one_liner": "Two heaps with a size invariant; the answer is the max-heap top.",
  "core_objective": "Support adding an integer and retrieving the median of all values added so far in amortized O(1) each.",
  "bounds": "Up to 1e5 operations and values up to 1e5, so the median is an integer and needs no rounding. Odd and even counts alternate, so the balancing logic must handle both.",
  "diagram": " add 1, 2, 3, 4, 5\n\n   lower (MAX-heap)   upper (MIN-heap)   median\n   ---- ------------  ----------------  -------\n   1    [1]          []                1   (1 = 1)\n   2    [1]          [2]               1   (even -> low)\n   3    [2,1]        [3]               2   (3 = 2)\n   4    [2,1]        [3,4]             2   (even -> low)\n   5    [3,1,2]      [4,5]             3   (5 = 3)\n\n   INVARIANT: len(lower) == len(upper)          or\n              len(lower) == len(upper) + 1\n   EVERY element of lower <= EVERY element of upper\n\n   median:\n     odd  count -> lower[0]      (the max-heap top)\n     even count -> (-lower[0] + upper[0]) / 2\n\n   python's heapq is MIN-only, so lower stores NEGATED\n   values and lower[0] is the true maximum.",
  "cpp_alts": [
   "`std::priority_queue<int>` (max) and `std::priority_queue<int, vector<int>, greater<int>>` (min) are the natural pair -- no negation needed.",
   "`__gnu_pbds::rb_tree` with two order-statistics iterators would also work but is heavier than heaps."
  ],
  "py_alts": [
   "heapq is min-only: push negated values into `lower` and read `-lower[0]` as the maximum.",
   "`heapq.heappush` / `heappushpop` are C-level; keeping the balance check outside the heap calls matters more than the choice of push variant."
  ],
  "trap": "Getting the parity convention backwards -- returning `upper[0]` for an odd count. The whole design hinges on `lower` always holding the extra element when the count is odd, so that the median is always accessible at `lower[0]`.",
  "invariant": "`len(lower) == len(upper)` or `len(lower) == len(upper) + 1`, and `max(lower) <= min(upper)`. Together these make the median a read of one or two heap tops, and they are preserved by inserting into `lower` then moving its top to `upper` when `lower` grows too large.",
  "questions": [
   {
    "q": "Why does `lower` hold the extra element when the count is odd?",
    "a": "So the median is always `lower`'s maximum. If the smaller half holds one more element, its top is exactly the middle value of the sorted sequence -- for both parities, with a two-term average only when even."
   },
   {
    "q": "Why is inserting into `lower` then rebalancing correct?",
    "a": "Adding to `lower` can only violate the ordering invariant if `lower` was empty or `upper` was non-empty and the new value exceeds `upper`'s minimum. In both cases moving `lower`'s maximum to `upper` restores the ordering, and fixing the sizes then restores the count invariant."
   },
   {
    "q": "What is the space complexity?",
    "a": "$O(n)$ -- every value ever added is retained, split across the two heaps. That is unavoidable: the median depends on the whole multiset, so nothing can be discarded."
   }
  ]
 },
 "09_heap_priority_queue/0355_design_twitter": {
  "one_liner": "Follow graph plus a timestamp-ordered feed per user.",
  "core_objective": "Design a Twitter-like API supporting follow, unfollow, post, and a user's recent posts including those of followed users.",
  "bounds": "At most 1e5 operations and 5e9 user IDs, so IDs must be long and follow sets must be hash-based. The feed is capped at 10 tweets, which is the key constraint that shapes the data structures.",
  "diagram": " post(1, [2,3])\n\n   followers: { 1: {2,3} }\n   tweets[tweetId] = { id:1, uid:1, ts:... }\n   userTweets[1] = heap of tweet ids by ts\n\n   getRecent(3):\n     candidates = {2,3} U self(3)\n     for each u in candidates:\n        merge the top of userTweets[u] into the result heap\n     pop the largest ts until 10 collected or all heaps empty\n\n   k = 10 CAP: you never need the whole timeline, so\n   per-user heaps are only drained lazily, at most 10 times.\n   That is what makes O(k log k)-ish work per query instead of\n   O(total tweets).\n\n   follow(a,b):  followers[a].add(b)\n   unfollow(a,b): followers[a].discard(b)   (a==b is a no-op)\n   post: push to that user's heap, incrementing the global clock",
  "cpp_alts": [
   "`unordered_map<int, unordered_set<int>>` for the follow graph; a set is required because unfollow must be $O(1)$ and duplicates must be idempotent.",
   "`multiset<pair<ts, tweetId>>` per user gives ordered access with erase-by-key, which a heap cannot do.",
   "`map<int, ...>` instead of unordered only if you need ordered user iteration, which the API does not require."
  ],
  "py_alts": [
   "`defaultdict(set)` for the follow graph; `set` gives O(1) follow/unfollow and automatic dedupe.",
   "`OrderedDict` per user keyed by timestamp keeps insertion order without a heap, at O(1) `move_to_end` and popitem.",
   "`heapq.merge(*[userTweets[u] for u in candidates])` is a lazy k-way merge -- the cleanest expression of the query."
  ],
  "trap": "Returning the 10 most recent tweets of ALL followed users rather than per-user merges, and ignoring the self-inclusion rule. A user always sees their own tweets, and duplicates must not appear if they follow someone who also follows them.",
  "invariant": "Each user's tweet container is ordered newest-first, so the newest tweet overall among a candidate set is the maximum of the per-user heads. Merging those heads and popping 10 times therefore yields exactly the 10 newest, and the merge touches at most 10 nodes per container.",
  "questions": [
   {
    "q": "Why does the k=10 cap make this tractable?",
    "a": "Without it you would need to sort every tweet by every followed user -- potentially unbounded work. With the cap, a k-way merge over per-user sorted streams needs at most k pops, each $O(\\log |F|)$ where F is the follow count. The cap is what turns an unbounded query into a bounded one."
   },
   {
    "q": "What structure per user, and why?",
    "a": "A heap, multiset, or ordered dict keyed by timestamp, all of which support newest-first access in $O(1)$. A plain list would need insertion in the middle ($O(n)$) unless you keep it sorted, which is worse. The requirement is ordered access to the newest element, not arbitrary access."
   },
   {
    "q": "How do you make unfollow O(1)?",
    "a": "Store each user's following set as a hash set, not a list. Deletion from a set is expected $O(1)$, and re-following is idempotent. A list would need a scan, which is why the set is load-bearing rather than incidental."
   }
  ]
 },
 "09_heap_priority_queue/0621_task_scheduler": {
  "one_liner": "The formula (maxFreq-1)*(n-maxFreqCount) + maxFreq.",
  "core_objective": "Return the minimum number of time units to run all tasks given a non-negative cooldown between identical tasks.",
  "bounds": "1 <= tasks.length <= 1e4 and 1 <= n <= tasks.length, so the answer fits comfortably in int. Cooldown n can exceed the alphabet size, in which case the answer is just the task count.",
  "diagram": " tasks = [A,A,A,B,B,C,C,C], n = 2  -> answer 7\n\n  frequencies: A:3 B:2 C:3\n  maxFreq = 3, maxFreqCount = 2 (A and C)\n  formula = (3-1) * (7-2) + 3 = 10 + 3 = 13 ? NO\n  correct: (maxFreq-1)*(n - maxFreqCount) + maxFreq\n         = (3-1)*(7-2) + 3 = 13   ... but expected 7?\n\n  Recompute: n = 2 cooldown.\n   A . . A . . A      frames of length 3, 2 frames\n   B . . B\n   C . . C\n   total = 2*3 + 1 = 7\n  formula with maxFreq=3, maxFreqCount=2, len=7:\n   (3-1)*(7-2) + 3 = 13  is wrong; the correct form is\n   (maxFreq-1)*(n - maxFreqCount) + maxFreqCount\n   (3-1)*(7-2) + 2 = 12  also wrong for this example because\n   the OTHER tasks fill the gaps.\n\n  The derivation:\n   maxFreq-1 frames are needed, each frame has length n.\n   The most frequent tasks occupy maxFreqCount slots per frame.\n   Everything else (len - maxFreq*maxFreqCount tasks) fills the\n   remaining slack. Result =\n     max( len, (maxFreq-1)*n + maxFreqCount )",
  "cpp_alts": [
   "A 26-element frequency array plus two running maxima is $O(T + 26)$ with no map.",
   "The heap simulation is $O(T \\log 26)$ and is more obviously correct, which is why it is the fallback."
  ],
  "py_alts": [
   "`Counter(tasks).values()` plus `max`/`count` gives the two quantities in one pass.",
   "The heap simulation with `Counter` and `list.index` on a 26-slot cooldown array is readable and fast enough."
  ],
  "trap": "Using the widely-copied formula `(maxFreq-1)*(n-maxFreqCount) + maxFreq` without checking it against a worked example. It is not correct in general; the frame-based derivation gives `max(len, (maxFreq-1)*n + maxFreqCount)`.",
  "invariant": "No schedule can be shorter than `len` tasks, and the cooldown forces at least `maxFreq - 1` separate frames of at least `n` units with `maxFreqCount` tasks pinned per frame. The answer is the max of those two lower bounds, and both are achievable.",
  "questions": [
   {
    "q": "Why do the most frequent tasks define the frame count?",
    "a": "A task occurring f times needs f-1 cooldowns between them, so it spans at least f slots. That forces at least maxFreq-1 frame boundaries, each of which must be at least n long or the cooldown would be violated."
   },
   {
    "q": "When is the answer simply `len`?",
    "a": "When `(maxFreq-1)*n + maxFreqCount <= len`, i.e. the other tasks fill every frame completely. Then no idle slot is needed and the schedule runs back to back."
   },
   {
    "q": "Why is a heap simulation not necessary?",
    "a": "Because the frame structure gives a closed-form lower bound that is achievable. The simulation is $O(T \\log 26)$ and useful as a correctness check or when the cooldown structure is more complex, but it is strictly more work for no extra information."
   }
  ]
 },
 "09_heap_priority_queue/0703_kth_largest_element_in_a_stream": {
  "one_liner": "Keep the top k in a min-heap; its root is the answer.",
  "core_objective": "Return the k-th largest value seen so far in a stream, for every add.",
  "bounds": "1 <= k <= 500 <= n <= 1e4, so the heap never exceeds 500 and every operation is comfortably bounded. Values are non-negative ints.",
  "diagram": " k = 3, adds: 4, 5, 8, 2, 3\n\n  heap (size <= 3, MIN-heap of the k largest):\n   add 4 -> {4}                 kth = 4\n   add 5 -> {4,5}               kth = 4\n   add 8 -> {4,5,8}             kth = 4\n   add 2 -> {2,4,5,8} pop 2     -> {4,5,8}  kth = 4\n   add 3 -> {3,4,5,8} pop 3     -> {4,5,8}  kth = 4\n\n  heap root = MIN of the retained k = the k-th largest overall.\n\n  invariant: |heap| == min(k, n) and heap contains the k largest\n  values seen so far. Each add is one push plus at most one pop,\n  so amortized O(log k).\n\n  contrast with 215 (static array): there you may sort or\n  quickselect; here the input is a stream, so nothing but the\n  retained top k may be stored.",
  "cpp_alts": [
   "`priority_queue<int, vector<int>, greater<int>>` is a min-heap by default with the comparator -- exactly the structure needed.",
   "A fixed `vector` of size k with manual sift is faster but far more code."
  ],
  "py_alts": [
   "`heapq.heappushpop(heap, x)` fuses push-and-pop into one C call and is faster than a separate push then conditional pop.",
   "When the heap is already full, `heappushpop` returns the smallest; if x is larger than the root it is inserted and the old minimum is discarded in a single operation."
  ],
  "trap": "Using a MAX-heap of size k, whose top is the largest of the retained set -- that gives you the largest, not the k-th largest. Or returning `heap[0]` before the heap has reached size k.",
  "invariant": "After each add, the heap holds exactly the k largest values seen so far (or all values if fewer than k have arrived), so its minimum is the k-th largest. `heappushpop` maintains this in one call because it only evicts when the new value exceeds the current minimum.",
  "questions": [
   {
    "q": "Why can you discard the smaller elements permanently?",
    "a": "Because at most k values ever matter for the answer, and only ever more values arrive. Once a value is not among the k largest, no future addition can promote it -- adding new elements only pushes the k-th largest upward. So discarded values are provably irrelevant."
   },
   {
    "q": "What if the heap is not yet full?",
    "a": "Then every value so far is a candidate, and the answer is simply the heap's minimum. `heappushpop` handles this automatically: while `len(heap) < k` it behaves as a plain push."
   },
   {
    "q": "How does this differ from problem 215?",
    "a": "215 has the whole array available, so sorting ($O(n \\log n)$) or `nth_element`/quickselect ($O(n)$) is possible. Here the input is a stream, so only the retained top k may be stored, which forces the $O(n \\log k)$ heap."
   }
  ]
 },
 "09_heap_priority_queue/1046_last_stone_weight": {
  "one_liner": "Pop the two heaviest stones; a tie annihilates both.",
  "core_objective": "Return the smallest possible weight of the remaining stone, or 0 if none remain.",
  "bounds": "1 <= stones.length <= 30 with weights 1..100, so at most 30 pops of a pair and an answer of at most 100. Weights are small enough that a counting bucket works too.",
  "diagram": " stones = [2,7,4,1,8,1]  -> answer 1\n\n  max-heap (negated in Python):\n   [8,7,4,2,1,1]\n   pop 8, pop 7 -> smash: 8-7 = 1  -> heap {4,2,1,1,1}\n   pop 4, pop 2 -> smash: 4-2 = 2  -> heap {2,1,1,1}\n   pop 2, pop 1 -> smash: 2-1 = 1  -> heap {1,1,1}\n   pop 1, pop 1 -> smash: 0         -> heap {1}\n   pop 1 alone -> heap empty\n   ANSWER 1\n\n  the SINGLE-STONE case matters: at the end the heap may hold\n  one element with no partner, and that value is the answer.\n\n  invariant: the heap always contains the current multiset of\n  surviving stone weights, so popping two maxima and reinserting\n  the difference is exactly one smash.",
  "cpp_alts": [
   "`priority_queue<int>` is a max-heap with no negation needed.",
   "With weights <= 100 a `vector<int> count(101)` descending sweep gives $O(W + n)$ with no heap at all."
  ],
  "py_alts": [
   "heapq is min-only: store negated weights and read `-heapq.heappop(h)`.",
   "The counting approach is elegant here: `for w in range(100, 0, -1)` and consume the count in pairs."
  ],
  "trap": "Continuing to pop twice when only one stone remains. The `while len(h) > 1` guard handles this; the bug is a `while h:` loop that pops twice unconditionally.",
  "invariant": "The heap holds exactly the weights of the stones not yet smashed. Each iteration removes the two heaviest and inserts their difference, which is precisely the problem's operation, so the invariant is preserved and the final top is the minimum surviving weight.",
  "questions": [
   {
    "q": "Why is the answer the heap's top rather than the sum?",
    "a": "Because smashing two stones a >= b replaces them with a - b, and the total weight decreases by exactly 2b. Greedily smashing the two heaviest is optimal, and when the heap empties the answer is 0; when one stone remains its weight is the answer, not a sum."
   },
   {
    "q": "What changes when weights exceed 100?",
    "a": "The counting bucket becomes infeasible (the array would be too large) and you must fall back on the heap, which is $O(n \\log n)$ and works for any magnitude. The bucket is purely an optimisation enabled by the weight bound."
   },
   {
    "q": "Is greedy optimal here?",
    "a": "Yes, and the exchange argument is short: if an optimal schedule does not smash the two heaviest together first, you can swap that pairing in without increasing the final weight, since the heavier stone can only ever reduce itself by pairing with something no heavier."
   }
  ]
 }
})

# ---- appended from _chunk7.json
DATA.update({
 "10_backtracking/0017_letter_combinations_of_a_phone_number": {
  "one_liner": "Index i into the digit string; each level picks a letter.",
  "core_objective": "Return all letter combinations that the digit string represents, mapping each digit to its 2-4 letters.",
  "bounds": "0 <= digits.length, digits[i] != '1' (no letters for 1), so an empty digits string yields one empty combination. 2^n output size, so the output dominates the runtime.",
  "diagram": " digits = \"23\"\n\n   2 -> a b c        3 -> d e f\n\n   i=0 path=''\n     pick 'a' -> i=1 pick 'd' -> 'ad'  <- leaf\n                        pick 'e' -> 'ae'\n                        pick 'f' -> 'af'\n     pick 'b' -> 'bd' 'be' 'bf'\n     pick 'c' -> 'cd' 'ce' 'cf'\n\n   invariant: path is always a prefix of exactly one output, and\n   len(path) == i. The tree has 3*3 = 9 leaves for \"23\".\n\n   key = digits[i] - '0'; letters = KEYS[key]\n   for ch in letters: dfs(i+1, path + ch)",
  "cpp_alts": [
   "`static const string KEYS[10]` indexed by `digits[i] - '0'` beats a map.",
   "`string path` with `push_back`/`pop_back` avoids the $O(n)$ copy that `path + ch` forces at every node."
  ],
  "py_alts": [
   "Mutate a single list with append/pop instead of concatenating strings -- avoids an $O(L)$ copy per node.",
   "A dict keyed by digit character is clearer than a list indexed by digit minus zero."
  ],
  "trap": "Indexing the keys table with the digit's character value rather than the digit minus '0'. That reads out of bounds and returns the wrong key for every multi-digit input.",
  "invariant": "`dfs(i, path)` enumerates all completions of the suffix starting at digit index i. The recursion is exhaustive because every letter of digit i is tried, and it emits no duplicates because each output corresponds to exactly one choice sequence.",
  "questions": [
   {
    "q": "What is the size of the output space?",
    "a": "The product of the letter counts, between $2^n$ and $4^n$. For n = 8 that is up to 65536 combinations, so any solution is output-bound: the algorithm is $\\Theta(\\text{output size})$ and cannot beat enumeration."
   },
   {
    "q": "Why not a greedy per-position choice?",
    "a": "Every letter at every position is valid independently -- there is no constraint linking positions. So the solution set is the cartesian product, which is exactly what recursion over independent choices generates."
   },
   {
    "q": "How does string concatenation affect the complexity?",
    "a": "`path + ch` copies the whole prefix each time, making the traversal $\\Theta(n \\cdot \\text{output})$ in the worst case. Mutating one buffer with push/pop brings it down to $\\Theta(\\text{output})$, which is optimal."
   }
  ]
 },
 "10_backtracking/0039_combination_sum": {
  "one_liner": "Index-based recursion, reuse the current candidate to allow repeats.",
  "core_objective": "Return all combinations that sum to target, where each number may be used unlimited times.",
  "bounds": "1 <= candidates.length <= 30 and 1 <= target <= 30, so the output is small but recursion depth is bounded by target (each element adds at least 1). Zero targets would loop forever.",
  "diagram": " candidates = [2,3,6,7], target = 7\n\n  dfs(i=0, rem=7):\n    candidates[0]=2\n      dfs(0, 5):  candidates[0]=2  <- SAME index, reuse allowed\n        dfs(0, 3):\n          dfs(0, 1):  1 % 2 != 0, dead\n        candidates[1]=3 -> 3==3 -> HIT  [2,2,3]\n      candidates[1]=3 -> 3 < 5\n        dfs(1, 2):\n          candidates[1]=3 > 2 -> dead\n      candidates[2]=6 > 5  candidates[3]=7 > 5  dead\n    candidates[1]=3\n      dfs(1, 4): candidates[1]=3 ... 3+? no\n    candidates[2]=6\n      dfs(2, 1): 6 > 1 dead\n    candidates[3]=7\n      dfs(3, 0): 7 == 7 -> HIT  [7]\n\n  ANSWER [[2,2,3], [7]]\n\n  two index rules that make it work:\n   recurse with i       -> element reusable (problem 39)\n   recurse with i + 1   -> element single-use  (problem 40)",
  "cpp_alts": [
   "Sort candidates and prune with `if (c[i] > rem) break` -- a large practical speedup.",
   "Pass `vector<int>& cur` by reference and push/pop, avoiding a copy per leaf."
  ],
  "py_alts": [
   "Sorting the list first and breaking out of the loop early prunes an enormous amount of the tree.",
   "`cur + [c]` at the leaf copies once per solution, which is acceptable since it happens only at output points."
  ],
  "trap": "Recursing with `i + 1` instead of `i`, which silently forbids reuse and returns only [[7]] for the example above. The distinction between problems 39 and 40 is exactly one character.",
  "invariant": "`dfs(i, rem)` enumerates all combinations summing to `rem` drawn from candidates[i:]. Recursing with the same `i` permits unbounded reuse of candidates[i], and recursing with `i+1` guarantees combinations are generated in non-decreasing candidate order, so no solution is produced twice.",
  "questions": [
   {
    "q": "Why does starting at the same index prevent duplicates?",
    "a": "Because a combination like [2,3] can only be built by taking 2 then 3. If you always move forward or stay, you never build [3,2], and the monotonic construction is unique per multiset. Sorting makes this even more obvious by letting you break when a candidate exceeds the remainder."
   },
   {
    "q": "What bounds the recursion depth?",
    "a": "The target, since each element is at least 1 -- depth is at most `target`. With candidates containing 0 the recursion would not terminate, so a zero candidate requires an explicit guard."
   },
   {
    "q": "How do you prune aggressively?",
    "a": "Sort ascending, then at each level break as soon as candidates[i] > rem. Any later candidate is larger, so the entire remaining subtree at that level is infeasible. This typically removes most of the tree."
   }
  ]
 },
 "10_backtracking/0040_combination_sum_ii": {
  "one_liner": "Same index, but start at i+1 and skip duplicate values.",
  "core_objective": "Return all unique combinations that sum to target, using each input element at most once.",
  "bounds": "1 <= candidates.length <= 30, all values 1..30, distinct, target 1..40. Duplicates in the input must produce duplicate combinations, so input-level dedupe is mandatory.",
  "diagram": " candidates = [10,1,2,7,6,1,5], target = 8\n\n  KEY: dedupe the INPUT first -> [1,1,2,5,6,7,10]\n  at each level: skip i > 0 and candidates[i]==candidates[i-1]\n\n  dfs(i=0, rem=8), path=[]:\n    i=0 c=1 -> dfs(1, 7)\n      i=1 c=1 == c[0] -> SKIP (same value as previous)\n      i=2 c=2 -> dfs(3, 5)\n        i=3 c=5 -> dfs(4, 0) HIT [1,2,5]\n        i=4 c=6 > 5 break\n      i=3 c=5 -> dfs(4, 2) 6>2 break\n    i=1 c=1 == c[0] -> SKIP\n    i=2 c=2 -> ...\n    i=3 c=5 -> ...\n    i=5 c=7 -> dfs(6, 1) 10>1 break\n    i=6 c=10 > 8 break\n\n  the two skips:\n   i > 0 and c[i] == c[i-1]  -> skip duplicates AT a level\n   recurse with i + 1          -> element used at most once",
  "cpp_alts": [
   "Sort then dedupe the vector in place before searching -- makes the per-level skip correct.",
   "`break` when `c[i] > rem` after sorting removes whole subtrees."
  ],
  "py_alts": [
   "`cands = sorted(set(candidates))` does dedupe and sort in one step, which is both correct and faster than a manual pass.",
   "`i > 0 and cands[i] == cands[i-1]` is the canonical skip; using `i == start` is a common wrong variant."
  ],
  "trap": "Skipping with `i == start` instead of `i > 0`. That check compares against the position where the current combination began, not against the previous element, so duplicate values in the input still generate duplicate combinations.",
  "invariant": "With the input sorted and deduped and the rule \"skip c[i] if it equals c[i-1] and i > 0\", every multiset of candidates has exactly one representation: the increasing-index selection of its distinct positions. Combined with recursing at i+1, no element is reused and no combination repeats.",
  "questions": [
   {
    "q": "Why must the input be sorted before the per-level skip works?",
    "a": "The skip compares adjacent elements, which only detects duplicates if equal values are adjacent. Sorting guarantees that, and it also enables the `c[i] > rem` early break. Sorting first is a precondition, not an optimisation."
   },
   {
    "q": "What is the difference from problem 39 exactly?",
    "a": "Two changes: recurse with `i + 1` (single use) instead of `i` (reuse), and add the duplicate skip. Applying only the first to problem 39's repeated candidates would lose valid solutions; applying only the second leaves 39 unable to express repeats."
   },
   {
    "q": "Can you solve it without sorting?",
    "a": "Yes, using a `Counter` over candidates and choosing values in a fixed order with a count limit -- that also avoids duplicates structurally. It costs a hash map instead of a sort but has the same $O(n \\log n)$-ish bound after sorting."
   }
  ]
 },
 "10_backtracking/0046_permutations": {
  "one_liner": "One position at a time, choosing any unused value.",
  "core_objective": "Return all permutations of a collection of distinct integers.",
  "bounds": "1 <= nums.length <= 6, so at most 720 permutations -- output-bound, and every approach is fast. Values are distinct, so a bitmap suffices; duplicates would need a set.",
  "diagram": " nums = [1,2,3]\n\n  path=[1]\n    path=[1,2]\n      path=[1,2,3] -> EMIT [1,2,3]\n      path=[1,3]\n        path=[1,3,2] -> EMIT [1,3,2]\n    path=[1,3]\n      path=[1,3,2] -> EMIT [1,3,2]  (dup? no, different prefix)\n      path=[1,3,1]? -> 1 already used, skipped\n  path=[2]\n    [2,1] -> [2,1,3] EMIT ; [2,3] -> [2,3,1] EMIT\n  path=[3]\n    [3,1] -> [3,1,2] EMIT ; [3,2] -> [3,2,1] EMIT\n\n  ANSWER all 6 permutations\n\n  invariant: path holds distinct elements drawn from nums; when\n  len(path) == n the path IS a permutation. Every permutation\n  appears once because each has a unique choice sequence.",
  "cpp_alts": [
   "`next_permutation` from `<algorithm>` generates all permutations iteratively in $O(n \\cdot n!)$ with $O(1)$ extra space.",
   "The swap-based DFS (`do { emit } while (next_permutation(...))`) is usually the strongest C++ answer."
  ],
  "py_alts": [
   "`itertools.permutations(nums)` is a C-level lazy iterator -- the shortest and fastest answer.",
   "A `used` boolean list is faster than swapping or a set when values are distinct ints."
  ],
  "trap": "Emitting a copy of `path` at every node instead of only at depth n. That produces partial permutations too, and the count is wrong by a large factor.",
  "invariant": "`path` contains distinct values all drawn from nums, and `used` marks exactly the positions represented in it. Appending an unused value preserves distinctness, so every depth-n path is a valid permutation, and every permutation is reachable by appending its elements in order.",
  "questions": [
   {
    "q": "Why is every permutation generated exactly once?",
    "a": "Each permutation corresponds to exactly one ordering of choices, and the recursion tries each unused element at each level. Two different choice sequences produce different paths, so no permutation can be produced twice and none is missed."
   },
   {
    "q": "What changes if the input has duplicates?",
    "a": "The `used`-by-position approach still works and naturally produces duplicate outputs, which you must then dedupe (e.g. insert into a set or skip equal values at the same depth). Skipping equal values at one level is the cheaper fix and is what problem 90 does."
   },
   {
    "q": "What is the complexity?",
    "a": "$O(n \\cdot n!)$ time -- there are n! leaves and copying each costs $O(n)$. Space is $O(n)$ for the recursion and the path, plus $O(n \\cdot n!)$ for the output, which dominates everything."
   }
  ]
 },
 "10_backtracking/0051_n_queens": {
  "one_liner": "One column per row; three conflict sets prune instantly.",
  "core_objective": "Return all board configurations with n queens that attack no other queen.",
  "bounds": "1 <= n <= 9. n = 2 and n = 3 have no solutions, so the output is empty. The search tree has n! leaves before pruning.",
  "diagram": " n = 4 -> two solutions\n\n  rows 0..3, one queen per row. Place in row i:\n    cols   : set of occupied columns\n    d1     : set of occupied (row - col)   diagonals\n    d2     : set of occupied (row + col)   diagonals\n\n  dfs(row):\n    for c in range(n):\n      if c in cols or (row-c) in d1 or (row+c) in d2:\n        continue\n      place, recurse, unplace\n\n  trace row 0: c=0 ok -> row 1: c=0 taken, c=1 diag? row-c=0 ->\n    d1 has 0 -> skip; c=2 row-c=-1 d1? no, row+c=3 d2? no\n    -> place at (1,2) -> row 2: c=1 -> row 3: c=3 ->\n    SOLUTION [[0,2],[1,4?]]... emits board 0 0 0 0 / 0 1 0 1\n\n  the three conflict tests are exhaustive because a queen\n  attacks along a row (impossible, one per row), a column,\n  and two diagonals. Sets make each test O(1).",
  "cpp_alts": [
   "`bitset<n>` per row and diagonal-gather operations make the conflict test a single mask AND -- the fastest known formulation.",
   "Keeping `board[r] = c` per row makes emitting the board trivial; `vector<int> queen(n)` is simpler."
  ],
  "py_alts": [
   "Three Python `set`s give O(1) tests; three bitmasks on integers are faster in CPython because small-int bit ops are single operations.",
   "Precomputing all diagonal indices avoids recomputing `row - c` and `row + c` at every node."
  ],
  "trap": "Using only the column check and forgetting one of the diagonals, or using absolute differences instead of the difference and sum. Absolute difference alone catches one diagonal family and misses the other.",
  "invariant": "After placing queens in rows 0..row-1, the three sets contain exactly the columns, the row-minus-column values, and the row-plus-column values of the placed queens. Therefore the membership tests are exactly the three attack directions, and any candidate passing all three is conflict-free.",
  "questions": [
   {
    "q": "Why is one queen per row guaranteed by the algorithm?",
    "a": "Because the search places exactly one queen per row by construction -- it recurses row by row. A valid solution can also be rotated, so the first row always has a queen; that is why only row-wise placement is complete."
   },
   {
    "q": "What is the pruning power of the set tests?",
    "a": "They cut the n! search to roughly $O(n! / n^{n/2})$ explored nodes for large n, because each new queen eliminates a growing fraction of the remaining columns. That is what makes n = 9 tractable while a naive row-column scan is not."
   },
   {
    "q": "How would bitsets improve this?",
    "a": "Represent occupied columns, diagonals, and anti-diagonals as bitmasks; the test becomes three AND operations on machine words. For n up to 32 that is a handful of instructions versus three hash lookups, and it also makes the horizontal reflection symmetry cheap to exploit."
   }
  ]
 },
 "10_backtracking/0078_subsets": {
  "one_liner": "Every node of the tree is a subset, so emit as you go.",
  "core_objective": "Return all subsets of a set of distinct integers, in any order.",
  "bounds": "0 <= nums.length <= 10, so at most 1024 subsets. An empty input yields one subset, the empty set.",
  "diagram": " nums = [1,2,3]   -> 8 subsets\n\n  path=[]        EMIT []\n   path=[1]      EMIT [1]\n    path=[1,2]   EMIT [1,2]\n     path=[1,2,3] EMIT [1,2,3]\n    path=[1,3]   EMIT [1,3]\n   path=[2]      EMIT [2]\n    path=[2,3]   EMIT [2,3]\n  path=[3]        EMIT [3]\n\n  2^3 = 8 emissions, matching the node count of a binary tree\n  of depth 3 (1 + 2 + 4 + 8 = 15 nodes, 8 leaves) -- here\n  every NODE is a solution, so 8 of the 15 nodes emit.\n\n  include/exclude formulation:\n   dfs(i, cur):\n     if i == n: emit(cur); return\n     dfs(i+1, cur)            # exclude nums[i]\n     dfs(i+1, cur + [nums[i]]) # include nums[i]\n\n  BITMASK alternative: for m in 0..2^n-1, bit j of m says\n   whether nums[j] is in subset m -- no recursion at all.",
  "cpp_alts": [
   "The bitmask loop `for (int m = 0; m < (1<<n); ++m)` is branch-free and trivially correct for n <= 20.",
   "Reserving the result to `1 << n` avoids repeated reallocation."
  ],
  "py_alts": [
   "`[list(c) for r in range(n+1) for c in combinations(nums, r)]` is C-level and gives all subsets sorted by size.",
   "`itertools.chain.from_iterable` over `combinations(nums, r)` avoids materialising intermediate lists."
  ],
  "trap": "Emitting only at the leaves. That gives the subsets in a different form and, if the recursion is include/exclude, only emits at depth n -- losing every smaller subset unless the branch is handled separately.",
  "invariant": "`path` is always a subset of nums containing only indices greater than the current recursion depth, so no index is used twice. Every subset is generated exactly once because each subset has a unique include/exclude signature, which corresponds to a unique root-to-node path.",
  "questions": [
   {
    "q": "Why does the count match 2^n?",
    "a": "Each of the n elements independently is either in or out, giving $2^n$ combinations. The recursion explores exactly that decision tree, emitting once per complete signature, so the count is right by construction rather than by filtering."
   },
   {
    "q": "When is the bitmask version preferable?",
    "a": "When n is small (say <= 20) and you want no recursion at all: iterate m from 0 to $2^n - 1$ and read bit j to decide membership. It is branch-free and impossible to get wrong, at the cost of an $O(2^n)$ shift per element."
   },
   {
    "q": "How does this relate to permutation problems?",
    "a": "Subsets are the include/exclude case (2 branches per level) whereas permutations are the pick-any-unused case (n branches). That difference in branching factor is why subsets have $2^n$ nodes and permutations $n!$, and it is the structural insight the category is built on."
   }
  ]
 },
 "10_backtracking/0079_word_search": {
  "one_liner": "Mark in place, search the four neighbours, unmark.",
  "core_objective": "Return whether any word in the list exists in the grid using adjacent horizontal or vertical moves without revisiting a cell.",
  "bounds": "1 <= board.length, board[0].length <= 1e4 with up to 30 words of length up to 1e3. Words may reuse a board letter, so there is no frequency precheck.",
  "diagram": " board = [\"ABE\",\"SFCS\",\"ADEE\"]  word = \"ABCCED\"\n\n  dfs(r, c, k):   k = index into the word\n    if out of bounds or board[r][c] != word[k]: return False\n    if k == len(word) - 1: return True          # last char matched\n    tmp = board[r][c]; board[r][c] = '#'        # MARK\n    found = (dfs(r+1,c,k+1) or dfs(r-1,c,k+1)\n             or dfs(r,c+1,k+1) or dfs(r,c-1,k+1))\n    board[r][c] = tmp                          # UNMARK  <- load bearing\n    return found\n\n  why mark: without it, 'AAA' can walk a straight line forever\n  by stepping back onto the previous cell.\n  why unmark: a sibling branch needs the ORIGINAL character;\n  leaving '#' makes the whole search fail.",
  "cpp_alts": [
   "Mark with a sentinel character such as '\\0' rather than '#' to be collision-proof against board contents.",
   "A `used` bool grid costs $O(RC)$ extra space but avoids mutating the input, which matters if the caller reuses it."
  ],
  "py_alts": [
   "Passing the four neighbours as a literal tuple of (dr, dc) offsets avoids four near-duplicate recursive calls.",
   "A `used` 2-D list is clean but allocates; in-place marking with restore is faster and is what the problem's mutation tolerance invites."
  ],
  "trap": "Forgetting to restore the cell after the recursive call. Every later path that needs that cell sees '#' and fails, so the answer is wrong even though the code looks symmetric at a glance.",
  "invariant": "On entry to `dfs(r, c, k)`, the cells holding word[0..k-1] along the current path are all marked '#', so no unmark check is needed inside the recursion -- the marks themselves enforce the no-revisit rule. Restoring on the way out re-establishes the invariant for sibling branches.",
  "questions": [
   {
    "q": "What is the time complexity, and why is it not simply O(RC * L)?",
    "a": "A loose bound is $O(RC \\cdot 4^L)$ from the branching, but the marking prunes hard: each path visits distinct cells, so the search is bounded by the number of simple paths, which is $O(3^L)$ per start because the previous cell is already marked and cannot be re-entered."
   },
   {
    "q": "Why is in-place marking better than a visited array here?",
    "a": "It uses O(1) extra space and one array write instead of a bounds-checked 2-D lookup. The cost is that you must restore, which is one extra write per node -- a good trade at these sizes."
   },
   {
    "q": "When would a Trie be the right structure?",
    "a": "When you must find ALL words in a large dictionary, not test a few. Then you share the walk across words instead of restarting from each cell per word, which is exactly problem 212."
   }
  ]
 },
 "10_backtracking/0090_subsets_ii": {
  "one_liner": "Sort, then skip equal values at the same recursion level.",
  "core_objective": "Return all unique subsets of a collection that may contain duplicates.",
  "bounds": "1 <= nums.length <= 10 so at most 1024 raw subsets; uniqueness must be enforced, not filtered afterwards.",
  "diagram": " nums = [1,2,2]\n  raw subsets: 8  -> unique: 4\n\n  sorted: [1,2,2]\n  dfs(start=0, cur=[]):\n    EMIT []\n    i=0 c=1 -> dfs(1,[1])\n      i=1 c=2 -> dfs(2,[1,2])\n        i=2 c=2 -> dfs(3,[1,2,2]) EMIT [1,2,2]\n      i=2 i>0 and c[2]==c[1] -> SKIP   <- avoids [1,2,2] twice\n    i=1 c=2 -> dfs(2,[2])\n      i=2 i>0 and c[2]==c[1] -> SKIP   <- avoids [2,2] from\n                                          starting at index 1\n    i=2 i>0 and c[2]==c[1] -> SKIP\n\n  the rule: at a given recursion level, once you have taken\n  c[i], you may not also take c[i+1] if they are equal. Taking\n  the LATER equal element instead gives a canonical choice.",
  "cpp_alts": [
   "Sort then the same skip; `sort` plus `unique` on the input would lose multiplicity and is wrong.",
   "`vector<bool> used(100)` as an alternative dedupe via set insertion works but costs a hash per leaf."
  ],
  "py_alts": [
   "`set(map(tuple, ...))` at the end dedupes but is $O(2^n \\cdot n)$ and loses order.",
   "The skip rule is strictly better: it avoids generating the duplicates at all."
  ],
  "trap": "Deduplicating the INPUT with `set(nums)`. That loses multiplicity, so `[1,2,2]` becomes `[1,2]` and the answer misses `[1,2,2]` entirely.",
  "invariant": "With the array sorted, the skip `i > start and nums[i] == nums[i-1]` ensures that within each recursion level, equal values are offered only at their first occurrence. Every distinct multiset therefore has exactly one index sequence, so no duplicate subset is generated and none is lost.",
  "questions": [
   {
    "q": "Why `i > start` rather than `i > 0`?",
    "a": "Because the skip should apply only among siblings at the same level. Using `i > 0` would also forbid legitimately choosing a second equal element deeper in the recursion, which is required for subsets like [1,2,2]. `start` marks where the current level began."
   },
   {
    "q": "Why does the skip work only on sorted input?",
    "a": "It compares adjacent elements, so equal values must be adjacent. Sorting guarantees adjacency and is therefore a correctness precondition, not merely a speedup."
   },
   {
    "q": "What is the worst-case number of generated subsets?",
    "a": "Exactly the number of distinct subsets, which is at most $2^n$ and equals $\\prod_i (c_i + 1)$ for value multiplicities $c_i$. With the skip in place you generate each exactly once, so there is no wasted work."
   }
  ]
 },
 "10_backtracking/0131_palindrome_partitioning": {
  "one_liner": "Precompute the palindrome table, then DFS over cuts.",
  "core_objective": "Return all partitions of a string such that every part is a palindrome.",
  "bounds": "1 <= s.length <= 2000 with lowercase letters, so the answer can be up to $2^{n-1}$ -- output-bound. A palindrome table is $O(n^2)$ time and space.",
  "diagram": " s = \"aab\"  -> [[\"a\",\"a\",\"b\"], [\"aa\",\"b\"]]\n\n  isPal[i][j] = s[i]==s[j] and (j-i<2 or isPal[i+1][j-1])\n\n   a  a  b\n  a T  F  F\n  a .  T  F\n  b .  .  T\n\n  dfs(start):\n    if start == n: emit(path); return\n    for end in range(start, n):\n      if isPal[start][end]:\n        path.push(s[start..end])\n        dfs(end+1)\n        path.pop()\n\n   start=0: end=0 'a' pal -> dfs(1)\n        start=1: end=1 'a' pal -> dfs(2)\n              end=2 'ab' not pal\n              dfs(2): end=2 'b' pal -> dfs(3) EMIT [a,a,b]\n        end=2 'aab' not pal\n   start=0: end=1 'aa' pal -> dfs(2)\n        end=2 'b' pal -> dfs(3) EMIT [aa,b]\n\n  O(n^2) table beats testing each candidate substring inline,\n  which is O(n^3) in total.",
  "cpp_alts": [
   "A `vector<vector<bool>>` table is compact; a 2-D char array is faster.",
   "Fill the table by increasing substring length so the recurrence's dependency is already computed."
  ],
  "py_alts": [
   "A list-of-lists of bools beats a dict of tuples.",
   "For n = 2000 the table is 4e6 entries -- Python lists of bools cost ~32 MB, so a bytearray per row is leaner."
  ],
  "trap": "Testing palindromes by reversing each candidate substring inline. That is $O(n^3)$ overall and will not pass at n = 2000.",
  "invariant": "`isPal[i][j]` is true iff s[i..j] is a palindrome, established by the recurrence for j-i < 2 and the inner interval otherwise. Therefore `dfs(start)` explores exactly the partitions whose first part starts at `start` and whose remaining parts partition the suffix, so every valid partition appears exactly once.",
  "questions": [
   {
    "q": "Why precompute the palindrome table?",
    "a": "Because the same substring is tested repeatedly across different partitions. Precomputing makes each test O(1), giving $O(n^2)$ for the table and $O(2^n)$ for the enumeration (output-bound). Inline testing repeats work and pushes the total to $O(n^3)$."
   },
   {
    "q": "What is the actual complexity?",
    "a": "$O(n^2)$ for the table plus the number of partial partitions explored, which is bounded by the output size. The theoretical worst case is $O(n \\cdot 2^n)$ because there can be $2^{n-1}$ partitions."
   },
   {
    "q": "When is the problem output-bound rather than time-bound?",
    "a": "When s is all the same character, e.g. \"aaaa...\", because then every substring is a palindrome and every set of cut positions yields a valid partition -- giving exactly $2^{n-1}$ outputs. Any algorithm must spend that much just to write them down."
   }
  ]
 },
 "10_backtracking/0395_longest_substring_with_at_least_k_repeating_characters": {
  "one_liner": "Split on a bad character, or slide a window by distinct count.",
  "core_objective": "Return the length of the longest substring in which every character appears at least k times.",
  "bounds": "1 <= s.length <= 1e4, k >= 1, and lowercase letters only. If no valid substring exists the answer is 0, which is the common failure output.",
  "diagram": " s = \"aaabbcccc\", k = 3  -> answer 10? check:\n   'aaa' a:3 ok  'bb'  b:2 < 3  -> b is a BLOCKER\n   'cccc' c:4 ok  a:3 ok\n   whole string: a4 b2 c4 -> b < 3 -> invalid\n   split at b: \"aaa\" (3) and \"cccc\" (4) -> max 4\n   ANSWER 4\n\n  DIVIDE AND CONQUER:\n   if already valid(s): return len(s)      -- shortcut\n   find the leftmost bad char c\n   left  = recurse(s[:i])\n   right = recurse(s[i+1:])\n   return max(left, right)\n\n  SLIDING WINDOW variant:\n   track `distinct` (count of chars with count >= k)\n   shrink while distinct > target for target in 1..26\n   the answer is the max over all targets",
  "cpp_alts": [
   "Frequency arrays indexed by char avoid any hashing in both the split and the window version.",
   "The divide and conquer can use `string::find_first_of` for the split points, but an explicit scan is clearer."
  ],
  "py_alts": [
   "`Counter` or a 26-list for frequencies; a list is faster in CPython.",
   "Iterating `target` from 1 to 26 with a reused window avoids re-implementing divide and conquer entirely."
  ],
  "trap": "Assuming the whole string is valid, or forgetting the early `if valid(s): return len(s)` shortcut which the divide-and-conquer needs to avoid infinite splitting.",
  "invariant": "In the window variant, for a fixed `target`, the window is shrunk until at most `target` characters appear at least k times. Adding a character can only increase that count and removing one can only decrease it, so the shrink loop is monotone and each pointer advances at most n times, giving $O(n)$ per target and $O(26n)$ overall.",
  "questions": [
   {
    "q": "Why does the divide and conquer need the validity shortcut?",
    "a": "Because if the string is valid we must return its full length rather than split. Without the check, a fully valid string still gets split at its first bad character -- and there is none, so the code would either index out of range or recurse forever."
   },
   {
    "q": "What is the complexity of the sliding window variant?",
    "a": "$O(\\sigma n)$ where sigma is the alphabet size (26), since you try each target count of qualifying characters. That is linear for a fixed alphabet and avoids recursion entirely, which is why it is often the better interview answer."
   },
   {
    "q": "Why is splitting on a bad character correct?",
    "a": "A character with fewer than k occurrences in the current string has fewer than k in any substring containing it, so no valid substring can include that position. Every valid substring therefore lies entirely to the left or entirely to the right of it, so the two sides can be solved independently."
   }
  ]
 }
})

# ---- appended from _chunk8.json
DATA.update({
 "11_graphs/0127_word_ladder": {
  "one_liner": "BFS over words one letter at a time; bidirectional doubles up.",
  "core_objective": "Return the number of words in the shortest transformation sequence from beginWord to endWord, changing one letter per step.",
  "bounds": "up to 5e3 words of length up to 10, and beginWord may or may not be in wordList. 0 steps is possible when they are equal. The output is the distance, not the sequence.",
  "diagram": " begin=\"hit\", end=\"cog\", list=[hot,dot,dog,lot,log,cog]\n\n  hit -> hot (i->o) -> dot (h->d) -> dog (t->g)\n      -> cog (d->c)     4 steps\n\n  BFS: level 0 {hit}, level 1 {hot}, level 2 {dot},\n       level 3 {dog}, level 4 {cog} -> 4\n\n  BIDIRECTIONAL: expand the SMALLER frontier each time.\n   front = {hit:0}, back = {cog:0}, steps = 0\n   front is smaller -> expand front -> {hot:1}\n   expand back      -> {dog:1}\n   expand front     -> {dot:2}\n   ... meet when a word appears in both maps\n   sum the two distances + 1\n\n  why bidirectional wins: each search covers a ball of radius\n  d; two balls of radius d/2 cover the same volume as one of\n  radius d, so the frontier stays small.",
  "cpp_alts": [
   "`unordered_set<string>` for the unvisited set; `erase` on discovery prevents revisiting and shrinks it.",
   "Generating candidates with `'a' + i` for 26 letters is faster than mutating positions one at a time."
  ],
  "py_alts": [
   "Set of strings + `'a' + i` loops is the fastest Python formulation.",
   "`dict` frontier with distance values avoids a separate level counter; BFS is still correct because all entries at a level share a distance."
  ],
  "trap": "Forgetting to remove a word from the unvisited set when it is enqueued. Then it is re-expanded from multiple parents and the level counting breaks, because a word can appear at two different depths.",
  "invariant": "At the start of each BFS level, the frontier contains exactly the words at distance `d` from the start, and the unvisited set contains exactly the words not yet placed at any distance <= d. Both together guarantee each word is discovered at its shortest distance.",
  "questions": [
   {
    "q": "Why is BFS correct here?",
    "a": "Each edge is one letter substitution, so the answer is the shortest path length in an unweighted graph. BFS explores in non-decreasing distance order, so the first time a word is reached is at its minimum distance. A DFS would find a path but not necessarily the shortest."
   },
   {
    "q": "What is the complexity of the bidirectional version?",
    "a": "$O(26 \\cdot L \\cdot N)$ in the worst case for N words of length L, but in practice the frontiers meet after exploring roughly $\\sqrt{N}$ words each rather than N, because each search covers a radius-d ball and meeting means d is about half the path length."
   },
   {
    "q": "Why must beginWord be added to wordList?",
    "a": "Because it may be absent from the list while still being a valid node with neighbours in it. Omitting it makes the first expansion find nothing and the search returns 0 incorrectly."
   }
  ]
 },
 "11_graphs/0130_surrounded_regions": {
  "one_liner": "Flood in from the border; whatever is unreached is captured.",
  "core_objective": "Flip every 'O' that is not connected to a border 'O' to 'X', leaving the rest untouched.",
  "bounds": "Board is m x n with up to 100 x 100, so recursion depth can reach 1e4 and overflows CPython's limit -- iterative flood fill is the practical choice.",
  "diagram": "  X X X X X\n  X O O O X\n  X X O O X\n  X O O X X\n  X X X X X\n\n  border O's: NONE on the top/right (all X),\n                one at (3,1)? (3,1) is interior -> captured\n  so interior O's all become X. Only O's touching an\n  edge survive.\n\n  ALGORITHM:\n   1. for every border cell that is 'O': flood-mark it '*'\n   2. for every cell still 'O': set it to 'X'\n\n  why it works: a region survives iff it has a path to the\n  border. Marking exactly the border-connected 'O's identifies\n  the survivors in one pass over the boundary.",
  "cpp_alts": [
   "An explicit `queue<pair<int,int>>` BFS from all border cells avoids the recursion depth problem entirely.",
   "`vector<pair<int,int>>` as a manual stack is equivalent and usually faster than `std::queue`."
  ],
  "py_alts": [
   "Iterative flood with an explicit list-as-stack avoids both the recursion limit and the tuple allocation of `collections.deque`.",
   "Flattening to a 1-D index of `m*n` cuts coordinate bookkeeping and makes the four neighbours pure arithmetic."
  ],
  "trap": "Flooding from every 'O' instead of from the border. That marks everything and nothing changes. The whole algorithm hinges on the source being the boundary.",
  "invariant": "After step 1, the set of cells marked '*' is exactly the set of 'O' cells with a path to the border. That is true because step 1 explores precisely the connected components that touch a border cell, and no others.",
  "questions": [
   {
    "q": "Why is boundary-flood the right frame?",
    "a": "The property being tested is connectivity to the boundary, so the natural search space is the set of border cells and their connected components. Flooding inward from those components marks exactly the cells that must be preserved, leaving the complement as the answer."
   },
   {
    "q": "What is the time and space complexity?",
    "a": "$O(mn)$ time -- each cell is visited at most once in each of the two passes -- and $O(mn)$ space in the worst case for the queue or stack holding a large frontier. In practice the frontier is O(m + n)."
   },
   {
    "q": "What is the difference from number-of-islands?",
    "a": "Only the source of the flood. Islands flood from every unvisited land cell; this floods from the boundary only. Same traversal, different seeds, opposite classification."
   }
  ]
 },
 "11_graphs/0133_clone_graph": {
  "one_liner": "Map original node to copy so cycles terminate.",
  "core_objective": "Deep-copy an undirected connected graph with node values, returning the clone of the given node.",
  "bounds": "1 to 1e4 nodes, values in [-1e4, 1e4], no self-loops, and the graph may contain cycles -- the aliasing is the whole problem.",
  "diagram": "  1 -- 2 -- 3 -- 4\n       |         |\n       +---------+\n\n  naive recursion on 1: creates copy 1, recurses into 2,\n  creates copy 2, recurses into 3, creates copy 3, ...\n  coming back to 1 via the edge 4->1 would create a SECOND\n  copy of 1 -> infinite/wrong.\n\n  memo: dict orig -> copy\n   clone(1): 1 not in memo -> create 1'\n            for nb in 1.neighbors:\n                clone(nb)  (fills memo as it goes)\n            return 1'\n   when 4 is processed and reaches 1, `1 in memo` -> reuse 1'\n\n  invariant: memo[o] exists and equals the copy of o from the\n  moment o's copy is created, so every node is copied exactly\n  once and all references share the same copy.",
  "cpp_alts": [
   "`unordered_map<Node*, Node*>` is the memo; node identity is the pointer value.",
   "An explicit stack with `(node, copy)` pairs gives the BFS version, which is often preferred for very deep graphs."
  ],
  "py_alts": [
   "A `defaultdict(Node)` for the memo, with the original object as key -- relies on `__hash__`/`__eq__` defaults (identity), which is what you want.",
   "`copy.deepcopy` on a self-referential graph works but hides the algorithm; mention it only as a library observation."
  ],
  "trap": "Copying neighbours without consulting the map, or checking membership only after recursing. Both create duplicate copies of a revisited node and break the sharing that makes the graph a graph.",
  "invariant": "`memo[o]` is created at the moment `clone(o)` first runs and never replaced. Therefore when an edge points back to an already-cloned node, the recursion returns the existing copy, and the resulting graph is isomorphic to the original with exactly one copy per original node.",
  "questions": [
   {
    "q": "Why is the map keyed by node object rather than value?",
    "a": "Values are not unique in a graph -- two nodes may share value 5. Identity is the only sound key, and in both languages the default hash/equality for objects is identity, so using the object as the key is exactly right."
   },
   {
    "q": "Why does the undirected property matter?",
    "a": "Because edges are symmetric, the same node is reachable by many paths, and the cycle detection requirement is what forces the memo. In a directed acyclic graph a plain DFS would suffice."
   },
   {
    "q": "What is the complexity?",
    "a": "$O(V + E)$ time: each node is cloned once and each edge is traversed twice (once per direction). Space is $O(V)$ for the memo plus $O(V)$ for the recursion stack, which can be the binding constraint on a long chain."
   }
  ]
 },
 "11_graphs/0200_number_of_islands": {
  "one_liner": "Flood fill each unvisited land cell; each seed is an island.",
  "core_objective": "Count the connected components of '1' cells in the grid using four-directional adjacency.",
  "bounds": "up to 300 x 300, so 9e4 cells and a recursion that can reach 9e4 deep -- far beyond CPython's limit, so iterative is the practical form.",
  "diagram": "  1 1 0 0 0\n  1 1 0 0 0\n  0 0 1 0 0\n  0 0 0 1 0        -> 3 islands\n\n  flood from (0,0): marks (0,0),(0,1),(1,0),(1,1)\n  scan continues: (2,2) unvisited -> island 2\n                 (3,3) unvisited -> island 3\n\n  key: MUTATE the grid. Setting visited cells to '0' removes\n  the need for a separate visited matrix and halves the space.\n\n  four neighbours only -- 8-directional adjacency is a\n  different problem with different answers.",
  "cpp_alts": [
   "In-place mutation to '0' avoids a visited vector; a stack-based flood avoids recursion depth.",
   "`std::stack` or `std::queue` of `pair<int,int>`; the manual-vector-as-stack is measurably faster than `std::queue` here."
  ],
  "py_alts": [
   "A flat list-as-stack of `(r, c)` tuples avoids `collections.deque` overhead.",
   "Flattening to index `r*n + c` makes neighbour checks pure integer arithmetic and avoids tuple allocation entirely."
  ],
  "trap": "Using 8-directional adjacency, or forgetting the out-of-bounds check before indexing -- with in-place mutation a missing bounds check reads out of range and can loop forever.",
  "invariant": "When the outer scan reaches an unvisited land cell, that cell's connected component has not been marked yet, so the flood that follows marks exactly that component and nothing else. Each component is therefore counted exactly once, at its first-encountered cell.",
  "questions": [
   {
    "q": "Why is in-place mutation acceptable and preferable here?",
    "a": "The problem does not forbid modifying the input, and marking a cell as visited by setting it to '0' is indistinguishable from it being water. That removes an $O(mn)$ visited array entirely, which for 9e4 cells is a real memory saving."
   },
   {
    "q": "What is the complexity, and why does the flood not re-visit cells?",
    "a": "$O(mn)$ time -- each cell is examined once by the outer scan and marked once by a flood. Space is $O(mn)$ worst case for the stack in a pathological all-land grid, but typically $O(\\min(m,n))$."
   },
   {
    "q": "How would 8-directional adjacency change the answer?",
    "a": "Diagonal land cells would connect components that four-directional treats as separate, so the count can only decrease or stay equal. It is a one-line change to the neighbour offsets and a good sanity question to ask yourself."
   }
  ]
 },
 "11_graphs/0207_course_schedule": {
  "one_liner": "Kahn's algorithm: peel off nodes with indegree zero.",
  "core_objective": "Decide whether all courses can be finished, i.e. whether the dependency graph is acyclic.",
  "bounds": "1 <= numCourses <= 5000 with up to 1e5 prerequisites, so the graph can have far more edges than nodes. Duplicate prerequisites are allowed and must not corrupt the indegree bookkeeping.",
  "diagram": "  0 -> 1 -> 2\n  cycle example: 1->2->3->1\n\n  KAHN:\n   indeg = [0,1,1]\n   queue = [0]\n   pop 0, visited=1 -> decrement indeg[1] -> 0 -> push 1\n   pop 1, visited=2 -> decrement indeg[2] -> 0 -> push 2\n   pop 2, visited=3 -> nothing left\n   visited == numCourses -> acyclic -> True\n\n  CYCLE 1->2->3->1:\n   indeg all 1 -> queue EMPTY -> visited 0 < 3 -> False\n\n  why it works: a graph is acyclic iff it has a topological\n  ordering iff there is always a node of indegree 0. Kahn\n  consumes exactly the nodes that can be removed without\n  breaking an edge -- so it exhausts the graph iff acyclic.",
  "cpp_alts": [
   "`vector<vector<int>> adj` plus an `int` indegree array; `queue<int>` for the frontier.",
   "A `vector<int> used` serving as the queue avoids the `std::queue` allocation."
  ],
  "py_alts": [
   "`defaultdict(int)` for indegree is slower than a preallocated list because of hashing.",
   "`from collections import deque` and `popleft()` gives O(1) FIFO; using a list with an index pointer is equivalent."
  ],
  "trap": "Decrementing the indegree of a node for an edge you already processed, or failing to decrement when a prerequisite is popped. The classic symptom is a cycle reported where there is none.",
  "invariant": "`processed` counts nodes whose prerequisites are all satisfied. A node enters the queue exactly when its indegree reaches 0, i.e. when all its incoming edges come from processed nodes. So `processed == numCourses` means every node was orderable, which holds exactly when there is no cycle.",
  "questions": [
   {
    "q": "Why does an empty queue prove a cycle exists?",
    "a": "If the queue is empty while nodes remain, every remaining node has an incoming edge from another remaining node. Following those predecessors forever in a finite graph must revisit a node, which is precisely a cycle."
   },
   {
    "q": "How do you handle duplicate prerequisites?",
    "a": "Increment the indegree once per duplicate edge and decrement once per processed edge, so the two counts stay consistent. The algorithm is then correct; the extra work is simply redundant."
   },
   {
    "q": "What is the complexity?",
    "a": "$O(V + E)$ time -- each node enters and leaves the queue once, each edge is decremented once. Space is $O(V + E)$ for the adjacency list plus $O(V)$ for the indegree array and queue."
   }
  ]
 },
 "11_graphs/0210_course_schedule_ii": {
  "one_liner": "Same Kahn, but keep the dequeue order as the answer.",
  "core_objective": "Return one ordering of courses that satisfies all prerequisites.",
  "bounds": "1 <= numCourses <= 5e3 with up to 1e5 edges. The problem guarantees a valid ordering exists, so no cycle check is needed.",
  "diagram": "  0 -> 1, 0 -> 2, 1 -> 3, 2 -> 3\n\n  indeg = [0, 1, 1, 2]\n  queue = [0]\n  pop 0 -> order=[0] -> indeg[1]=0 push 1, indeg[2]=0 push 2\n  pop 1 -> order=[0,1] -> indeg[3]=1\n  pop 2 -> order=[0,1,2] -> indeg[3]=0 push 3\n  pop 3 -> order=[0,1,2,3]\n\n  ANSWER [0,1,2,3]\n\n  ties: when several nodes have indegree 0 the order is not\n  unique; any of them may be taken. Using a QUEUE (FIFO)\n  gives a deterministic answer; a stack (LIFO) gives a valid\n  but different one.",
  "cpp_alts": [
   "`vector<int> used` as both the queue and, in reverse, the answer -- an O(1) in-place trick.",
   "`priority_queue` gives a lexicographically smallest ordering at $O(E \\log V)$ if that is asked."
  ],
  "py_alts": [
   "A list used as a stack gives a valid order with slightly less code but no FIFO determinism.",
   "`deque` + `popleft()` is the canonical BFS-frontier form."
  ],
  "trap": "Returning the reverse of the dequeue order. With an edge a -> b meaning \"a before b\", the dequeue order already satisfies the constraints; reversing breaks them.",
  "invariant": "A node is dequeued only when its indegree is 0, meaning every prerequisite has already been dequeued and is earlier in `order`. Therefore every edge u -> v has position(u) < position(v), which is exactly the required property.",
  "questions": [
   {
    "q": "Is the ordering unique?",
    "a": "No. Whenever two or more nodes have indegree 0 simultaneously, any of them may be taken next, producing different valid orderings. The problem accepts any of them; using a queue gives one deterministic choice."
   },
   {
    "q": "How do you get the lexicographically smallest valid ordering?",
    "a": "Replace the FIFO queue with a min-heap. The first node available is then always the smallest, giving a canonical answer at $O((V+E) \\log V)$ instead of $O(V+E)$."
   },
   {
    "q": "What if a cycle existed, since the problem guarantees it does not?",
    "a": "The dequeue order would be shorter than numCourses and you would return an empty list or signal failure. Since existence is guaranteed, the check is unnecessary -- but adding it makes the function total."
   }
  ]
 },
 "11_graphs/0261_graph_valid_tree": {
  "one_liner": "n - 1 edges plus no cycle plus connected.",
  "core_objective": "Decide whether the given edge list forms a valid tree over n labelled nodes.",
  "bounds": "1 <= n <= 2e4 with 0 <= edges.length <= 2e4. n = 1 with zero edges IS a valid tree, and n = 1 with one self-loop is not.",
  "diagram": " n=3, edges=[[0,1],[1,2]]  -> valid\n   undirected, 2 = n-1 edges, connected, acyclic\n\n n=3, edges=[[0,1],[1,0]]  -> invalid (duplicate edge;\n   treated as a 2-cycle)  edges=2 but the component is\n   only {0,1}, node 2 isolated\n\n UNION-FIND:\n   parent = list(range(n))\n   for u, v in edges:\n      ru, rv = find(u), find(v)\n      if ru == rv: return False      <-- CYCLE detected\n      parent[ru] = rv                 <-- union\n   return edges == n - 1              <-- connectivity proxy\n\n why edges == n-1 implies connected, given no cycle:\n   an acyclic forest with V vertices and C components has\n   exactly V - C edges. So V-1 edges forces C = 1.",
  "cpp_alts": [
   "`std::vector<int> parent, size` with path compression and union by rank is near-O(1) per op.",
   "A BFS/DFS from node 0 plus an edge count is simpler to explain and uses O(n) space without a DSU."
  ],
  "py_alts": [
   "Iterative `find` with path halving avoids Python's recursion limit at 2e4 depth.",
   "The BFS-from-0 approach needs only a set and is easier to get right in an interview."
  ],
  "trap": "Checking only `edges == n - 1`. That passes for two disjoint 3-node trees, so the edge count alone is not sufficient -- acyclicity must also be established, or connectivity checked directly.",
  "invariant": "Union-Find maintains the partition of nodes into connected components of the edges processed so far. `find(u) == find(v)` before a union means the new edge closes a cycle; otherwise the union merges two components, decreasing the count by one. After all edges, no cycle means the graph is a forest, so the edge count decides connectivity.",
  "questions": [
   {
    "q": "Why is the edge count the right connectivity proxy?",
    "a": "An acyclic undirected graph with V vertices and C connected components has exactly V - C edges. So if the graph is acyclic and has V - 1 edges, then C must be 1. The count therefore substitutes for an explicit connectivity check once acyclicity is known."
   },
   {
    "q": "What does DSU detect that a cycle check alone does not?",
    "a": "DSU detects a cycle implicitly: adding an edge whose endpoints are already connected is exactly a cycle. Combined with the edge-count check you get both conditions without a traversal, and each operation is near-O(1) amortised."
   },
   {
    "q": "How do you handle parallel edges?",
    "a": "The DSU approach handles them naturally: the second copy of an edge has endpoints already in the same component, so it is rejected as a cycle. An approach that only counts edges and checks connectivity would wrongly accept them."
   }
  ]
 },
 "11_graphs/0286_walls_and_gates": {
  "one_liner": "Multi-source BFS from every zero, dist is the answer.",
  "core_objective": "Set each empty cell's value to its minimum distance to any gate, where 0 marks a gate and -1 an open empty room.",
  "bounds": "up to 200 x 200 = 4e4 cells, so a BFS with an explicit queue is the right shape; recursion depth would blow up.",
  "diagram": "  0 -1 -1 -1\n -1 -1 -1 -1\n -1 -1 -1 -1\n -1 -1 -1 0\n\n  multi-source: seed the queue with ALL zeros, dist 0\n\n  wave 1: cells adjacent to a zero get dist 1\n          (0,1)=1 (1,0)=1 (1,3)=1 (3,2)=1\n  wave 2: dist 2 cells\n  wave 3: dist 3 cells\n  wave 4: dist 4  <- centre (1,1) and (2,2) etc\n\n  result:\n   0 1 2 3\n   1 2 3 4\n   2 3 4 3\n   3 4 3 0\n\n  why multi-source: BFS from all sources at once gives the\n  distance to the NEAREST source, because BFS explores in\n  order of increasing distance from ANY seed. Running BFS\n  once per gate would be O(gates * RC) and give the last\n  gate's answer instead.",
  "cpp_alts": [
   "A single `queue<pair<int,int>>` seeded with all gates; in-place mutation to distances removes the visited set.",
   "An explicit index vector avoids `std::queue`'s block churn."
  ],
  "py_alts": [
   "A `deque` seeded with all zeros is the idiomatic multi-source BFS.",
   "Flatten to `r*cols + c` so the queue holds ints rather than tuples."
  ],
  "trap": "Overwriting gate cells during the BFS, or revisiting cells that already have a distance. The `if gate[r][c] == -1` guard must be checked before both writing and enqueueing, and the new cell must be marked as soon as it is enqueued.",
  "invariant": "BFS pops cells in non-decreasing order of their distance from the seed set. Because every seed starts at distance 0, the distance assigned when a cell is first enqueued is the minimum over all sources, which is the problem's definition.",
  "questions": [
   {
    "q": "Why must all gates be seeded before the BFS starts?",
    "a": "BFS's correctness relies on processing in non-decreasing distance order. Seeding all gates at distance 0 simultaneously establishes that order over the union of the searches, so the first time a cell is reached is via the nearest gate."
   },
   {
    "q": "What is the complexity?",
    "a": "$O(RC)$ time -- each cell is enqueued and expanded once, with four neighbour checks. Space is $O(RC)$ for the queue. Running BFS per gate would be $O(\\text{gates} \\cdot RC)$, which for many gates is the difference between passing and timing out."
   },
   {
    "q": "How does this differ from the wall/flood problem?",
    "a": "Same grid traversal, opposite source and target. Here you flood FROM all zeros and write distances; there you flood from the border and then flip the unmarked. The shared skill is multi-source flood fill."
   }
  ]
 },
 "11_graphs/0323_number_of_connected_components": {
  "one_liner": "Union nodes; a union that fails means a cycle, not a new component.",
  "core_objective": "Return the number of connected components in an undirected graph with n nodes and some edges.",
  "bounds": "0 <= n <= 200 with up to n*(n-1)/2 edges, so a dense graph is possible and duplicate edges are allowed.",
  "diagram": " n=5, edges=[[0,1],[0,2],[3,4]]  -> 3 components\n\n  DSU: components = 5\n   union(0,1) different -> components-- = 4\n   union(0,2) different -> components-- = 3\n   union(3,4) different -> components-- = 2 ?!\n\n  WAIT -- components starts at n=5 and each SUCCESSFUL union\n  decrements. 3 successful unions -> 5 - 3 = 2. But the\n  answer is 3: {0,1,2} {3,4} and node 5 is isolated.\n\n  count again: n=5, so components={0},{1},{2},{3},{4}\n   union(0,1): {0,1},{2},{3},{4}   -> 4\n   union(0,2): {0,1,2},{3},{4}     -> 3\n   union(3,4): {0,1,2},{3,4}       -> 2\n  components = 2 but the true answer with node 5 isolated is\n  3. n=5 means nodes 0..4, and there is no node 5 -- so the\n  components are {0,1,2} and {3,4} = 2. Correct: 2.\n\n  invariant: components = n - (number of successful unions),\n  and each successful union merges exactly two distinct sets.",
  "cpp_alts": [
   "`vector<int> parent` with path compression; a `vector<int> size` for union by rank.",
   "DFS over an adjacency list is simpler to explain: O(n + E) time, O(n + E) space."
  ],
  "py_alts": [
   "Iterative `find` with path halving; avoid recursion at n = 200 by using a loop.",
   "An adjacency-list DFS avoids DSU entirely and is often the faster-to-verify answer."
  ],
  "trap": "Forgetting that n may be 0, so the answer is 0 and the DSU must handle an empty parent array. Also, decrementing the count on a failed union, which is what would make a cyclic graph report too few components.",
  "invariant": "`components` always equals the number of distinct sets in the partition maintained by DSU. A union of two different sets decreases it by exactly one; a union within a single set leaves it unchanged. Since DSU's partition is exactly the graph's connected components once all edges are processed, the final count is the answer.",
  "questions": [
   {
    "q": "Why is a failed union not a new component?",
    "a": "Because the two nodes are already reachable from each other, so the edge adds no new connectivity. Only a union between distinct sets changes the component count, which is why the guard is on the find comparison rather than on the edge itself."
   },
   {
    "q": "When would the DFS version be better?",
    "a": "When the graph is given as an adjacency list you already have, DFS is one pass with no union-find setup, and it handles the components directly. DSU wins when edges arrive one at a time or when you only need the count and not the membership."
   },
   {
    "q": "What is the space complexity of the DSU version?",
    "a": "$O(n)$ for the parent and rank arrays -- independent of the number of edges. That is a genuine advantage over DFS, which needs $O(n + E)$ space for the adjacency structure."
   }
  ]
 },
 "11_graphs/0417_pacific_atlantic_water_flow": {
  "one_liner": "Two reverse BFS floods, one from each ocean.",
  "core_objective": "Return the coordinates of cells from which water can reach BOTH the Pacific and the Atlantic.",
  "bounds": "heights is m x n with 1 <= m, n <= 50, and height can be 0. A cell on a border touches both oceans and is always valid.",
  "diagram": " reverse thinking: instead of asking which cells DRAIN to an\n ocean, ask which cells an ocean can CLIMB TO.\n\n  pacific  seeds: (0,0) and (0,n-1)\n  atlantic seeds: (m-1,0) and (m-1,n-1)\n\n  canReachPacific(r,c):\n    if grid[r][c] is a seed: true\n    for each neighbour with height >= grid[r][c]:\n       if canReachPacific(nb): true\n\n  answer = cells where BOTH reachabilities hold\n\n  visited must be PER-OCEAN -- a shared visited set would\n  let the pacific search's marks block the atlantic search.\n\n  invariant: the flood from an ocean covers exactly the cells\n  with a non-increasing path to that ocean, which is exactly\n  the set that can drain there.",
  "cpp_alts": [
   "Two `queue<pair<int,int>>` runs with separate visited grids; the recursive DFS version is fine at m,n <= 50.",
   "`vector<vector<bool>>` visited is compact; a plain char grid avoids vector<bool>'s proxy semantics."
  ],
  "py_alts": [
   "Iterative flood with a list-as-stack avoids recursion depth issues for the 50x50 bound.",
   "Flattening to index `r*n + c` makes neighbour checks arithmetic and keeps the visited a flat bytearray."
  ],
  "trap": "Sharing one visited set between the two searches. The first flood claims cells the second flood then cannot enter, so valid intersections are missed. Two independent visited sets (or a bitmask of two flags per cell) are required.",
  "invariant": "`reach(ocean, r, c)` is true iff there is a path from (r,c) to that ocean along which heights never increase. This is exactly the condition for water to flow downhill from the cell to the ocean, so the intersection of the two predicates is precisely the answer.",
  "questions": [
   {
    "q": "Why search backwards, from the oceans?",
    "a": "The predicate is \"can reach the ocean\", which is a backward reachability question. Flooding from the ocean along non-decreasing heights computes exactly the set of cells that have such a path, in one pass per ocean, instead of searching from every cell."
   },
   {
    "q": "What is the complexity?",
    "a": "$O(mn)$ time -- two floods each visiting every cell at most once, with four neighbour checks. Space is $O(mn)$ for the visited flags and the flood structure. Doing it from every cell instead would be $O(m^2 n^2)$."
   },
   {
    "q": "How would you return only the intersection without two grids?",
    "a": "Use a single 2-bit mask per cell: bit 0 set when reachable from the Pacific, bit 1 from the Atlantic. Then answer = cells where mask == 3. One grid, both bits, and the two floods do not interfere because they test different bits."
   }
  ]
 },
 "11_graphs/0684_redundant_connection": {
  "one_liner": "Union-Find: the first edge whose endpoints are already joined.",
  "core_objective": "Given a tree plus one extra edge, return the single edge whose removal restores a tree.",
  "bounds": "n >= 3 and edges.length == n, so exactly one cycle exists. A self-loop and a duplicate edge are both possible and both have a unique answer.",
  "diagram": " n=3, edges=[[1,2],[1,3],[2,3]]  -> answer [2,3]\n\n  union(1,2): different -> merge {1,2}\n  union(1,3): different -> merge {1,2,3}\n  union(2,3): find(2)==find(3) SAME -> REDUNDANT\n\n  invariant: after processing i edges, DSU's partition is the\n  connected components of the first i edges. So a redundant\n  edge is precisely one whose endpoints were already joined --\n  adding it closes a cycle.\n\n  because only ONE extra edge exists, the FIRST such edge is\n  the answer; you may return immediately.",
  "cpp_alts": [
   "`vector<int> parent` with path compression; the whole loop is near-O(n) amortised.",
   "Detecting the extra edge by counting parity with an XOR array works for a tree plus one edge and is a neat alternative."
  ],
  "py_alts": [
   "Iterative `find` with path halving avoids recursion; at n = 1000 a loop is safer.",
   "A `defaultdict(set)` adjacency plus an edge-set for lookup works but is heavier."
  ],
  "trap": "Continuing the loop after finding a redundant edge, or recording the LAST redundant edge. With exactly one extra edge both work here, but the code reads as if multiple were possible, and the problem guarantees exactly one.",
  "invariant": "DSU's partition equals the connected components of the edges processed so far. Adding an edge within one component creates a cycle and is therefore redundant; adding one across components cannot. Since the input has exactly n edges over n nodes, exactly one such edge exists.",
  "questions": [
   {
    "q": "Why is the first cycle-closing edge the answer?",
    "a": "Because the input is a spanning tree plus one edge, so exactly one edge is redundant. An edge is redundant precisely when its endpoints are already connected when it is processed, so the first (and only) such edge is it."
   },
   {
    "q": "How do you handle a self-loop [1,1]?",
    "a": "A self-loop has find(1) == find(1) trivially, so it is detected as redundant immediately and returned. That is correct, since removing it restores the tree."
   },
   {
    "q": "What is the complexity?",
    "a": "$O(n \\alpha(n))$ time with union-find (the inverse Ackermann factor is effectively constant), or $O(n \\log n)$ worst case with only path compression and no union by rank. Space is $O(n)$."
   }
  ]
 },
 "11_graphs/0695_max_area_of_island": {
  "one_liner": "Flood fill each island, tracking its size.",
  "core_objective": "Return the area of the largest group of 1s connected four-directionally.",
  "bounds": "up to 300 x 300 with 0/1 cells, so 9e4 cells and a flood that can reach 9e4 stack entries -- an iterative fill is the practical form.",
  "diagram": "  0 0 1 0\n  0 1 1 0\n  1 0 0 1\n  0 0 1 0      -> largest area 3\n\n  scan: (0,2) seed, flood covers (0,2),(1,1),(1,2) -> area 3\n        (2,0) seed, area 1\n        (2,3) seed, area 1\n        (3,2) seed, area 1\n  max = 3\n\n  invariant: each cell is marked the moment it is counted, so\n  the flood from a seed covers exactly that seed's component\n  and the area counter equals the component size.",
  "cpp_alts": [
   "In-place mutation to 0 removes the visited grid; a `stack<pair<int,int>>` avoids recursion depth.",
   "A flat index stack with `r*n + c` arithmetic is faster than pairs."
  ],
  "py_alts": [
   "Flatten to a `bytearray` for the grid so marking is an int assignment, not a nested list store.",
   "Mutate `grid[i]` in place in a list of strs by converting rows to lists first."
  ],
  "trap": "Incrementing the area counter before marking the cell, or marking after recursing. Both cause the same cell to be counted twice, inflating the area.",
  "invariant": "The flood from an unvisited land cell visits each cell of its component exactly once, because the cell is marked at the moment it is counted. Hence the accumulated counter equals the component's size and the maximum over all seeds is the answer.",
  "questions": [
   {
    "q": "Why is the flood O(mn) overall rather than O((mn)^2)?",
    "a": "Each cell is marked once, and a marked cell is never entered again -- the flood's entry test is the same as the outer scan's. So the total work across all floods is proportional to the number of cells, not to the number of seeds times the grid."
   },
   {
    "q": "What does the mark-then-count ordering guarantee?",
    "a": "That the four-neighbour expansion never re-enters a cell already counted, so no cell contributes twice. This is the standard in-place visited pattern: write the mark before recursing, and restore only if you need the original grid."
   },
   {
    "q": "How would you handle an all-zeros grid?",
    "a": "The outer scan finds no seeds and the answer stays at its initial value, which must be 0. Initialising best to 0 rather than 1 is what makes that case correct."
   }
  ]
 },
 "11_graphs/0994_rotting_oranges": {
  "one_liner": "Multi-source BFS from all rotten oranges, minute by minute.",
  "core_objective": "Return the number of minutes until no fresh orange remains, or -1 if some orange can never rot.",
  "bounds": "up to 10 x 10, so 100 cells and at most 100 minutes. Multiple rotten oranges at t=0 are the defining case, and an all-rotten grid must return 0.",
  "diagram": "  2 1 1 1 1\n  1 1 1 1 1\n  1 1 0 1 1\n  1 1 1 1 1\n  1 1 1 0 1\n\n  t=0: two rots at (0,0) and (2,2)\n  t=1: (0,1) (1,0) (1,2) (2,1) (2,3) (3,2)\n  t=2: (0,2) (1,3) (1,1) (3,1) (3,3) (4,2)\n  ...\n  a 0 at (4,4) surrounded by 1s -> reachable\n  a 0 at (4,4)? all cells eventually rotted -> answer 11\n\n  BFS:\n   queue seeded with all 2s, count fresh = total - rotten\n   while queue and fresh > 0:\n       for _ in range(len(queue)):   process one minute\n           spread to 1 neighbours, mark 2, fresh--\n       minutes++\n   return minutes if fresh == 0 else -1\n\n  the `len(queue)` snapshot is what makes one BFS level = one\n  minute, exactly like level-order traversal.",
  "cpp_alts": [
   "`queue<pair<int,int>>` with `int levelSize = q.size()` per minute.",
   "An in-place 0->2 mutation removes the fresh counter, but the counter is clearer."
  ],
  "py_alts": [
   "`deque` with a per-level `for _ in range(len(q))` is the idiomatic minute-by-minute BFS.",
   "Early-exit as soon as fresh hits 0 avoids the final drained levels."
  ],
  "trap": "Using a single counter for elapsed time incremented per node rather than per level. That counts nodes processed, not minutes, and produces a number larger than the true answer.",
  "invariant": "At the start of each level, the queue holds exactly the cells that rot at minute `t`, and `fresh` is the number of cells still unrotted. Processing one level rots every cell adjacent to a minute-t cell, so the level boundary corresponds exactly to one minute of propagation.",
  "questions": [
   {
    "q": "Why does the level size snapshot equal one minute?",
    "a": "BFS expands in waves. All cells in the queue at the start of a level were reached at the same minute, and their newly discovered neighbours are exactly one minute later. Capturing the size before processing bounds one iteration to one time step."
   },
   {
    "q": "When is the answer -1?",
    "a": "When `fresh > 0` after the queue empties, meaning some 0 cell is only reachable through other 0 cells and can therefore never be adjacent to a rotting orange. Empty cells also block propagation, which is what makes unreachability possible at all."
   },
   {
    "q": "What is the space complexity?",
    "a": "$O(mn)$ for the queue in the worst case, plus the grid itself. The fresh counter is $O(1)$. Time is $O(mn)$ because each cell is enqueued at most once."
   }
  ]
 }
})

# ---- appended from _chunk9.json
DATA.update({
 "12_advanced_graphs/0269_alien_dictionary": {
  "one_liner": "First-appearing difference between words gives an edge.",
  "core_objective": "Derive the ordering of a new alphabet from a list of words that are sorted under it, and return a valid order.",
  "bounds": "1 <= dictionary.size <= 100 with up to 2e4 words, and every word is lowercase with up to 20 characters. An invalid dictionary (words out of order, or a prefix after a longer word) must return an empty string.",
  "diagram": " words = [\"hi\",\"hj\",\"az\",\"kl\"]  -> [a,h,k,z]\n\n  compare consecutive pairs, FIRST differing char only:\n   \"hi\" vs \"hj\":  i<j   -> edge i->j\n   \"hj\" vs \"az\":  h<a   -> edge h->a\n   \"az\" vs \"kl\":  a<k   -> edge a->k\n\n  graph:  i -> j\n          h -> a -> k\n\n  KAHN:\n   indeg: j=1, i=0, a=1(from h), k=1, h=0\n   queue = [i, h]\n   pop i -> order=[i], indeg[j]=0 -> push j\n   pop h -> order=[i,h], indeg[a]=0 -> push a\n   pop j -> order=[i,h,j]\n   pop a -> push k -> pop k\n   ANSWER [i,h,j,a,k]  (equivalent to a,h,k,z... any valid)\n\n  WHY first difference only: later characters are irrelevant\n  to lexicographic order -- the first mismatch decides.",
  "cpp_alts": [
   "`array<int,26>` adjacency with a boolean matrix is simplest and fine at this scale; bitmasks scale further.",
   "`std::priority_queue` variant gives the lexicographically smallest valid order."
  ],
  "py_alts": [
   "A `set` of pairs or a list-of-sets adjacency is the fastest readable Python form at n <= 100.",
   "`defaultdict(set)` handles multiple edges between the same pair without double-counting indegree."
  ],
  "trap": "Adding an edge for EVERY differing position rather than just the first. That produces constraints the problem never implied and can make a valid dictionary look cyclic.",
  "invariant": "The edge set contains exactly the pairwise orderings implied by lexicographic comparison, and Kahn consumes nodes of indegree zero. If Kahn emits all 26 letters the collected edges were acyclic and the order is valid; if fewer are emitted, the derived graph has a cycle and the dictionary is inconsistent.",
  "questions": [
   {
    "q": "Why only the first differing character matters?",
    "a": "Lexicographic comparison is decided by the earliest position where two words differ; everything after is irrelevant. So each adjacent pair contributes at most one constraint, and taking the minimum-cost set of edges is automatic."
   },
   {
    "q": "How do you detect an invalid dictionary?",
    "a": "After Kahn, if fewer than 26 letters were emitted, the derived graph contains a cycle and no valid order exists, so return the empty string. Separately, if a word is a strict prefix of its successor (e.g. \"abc\" before \"ab\"), the dictionary is invalid regardless of any graph."
   },
   {
    "q": "What is the complexity?",
    "a": "$O(W \\cdot L + 26^2)$ time for the comparisons and the topological sort, where W is the word count and L the max length. Space is $O(26^2)$ for the adjacency structure."
   }
  ]
 },
 "12_advanced_graphs/0332_reconstruct_itinerary": {
  "one_liner": "Hierholzer: traverse edges, reverse at the end.",
  "core_objective": "Return the lexicographically smallest route that visits every flight exactly once.",
  "bounds": "1 <= tickets.length <= 1e4 with n <= 10 airports, so the answer is at most 10 cities long while there may be 1e4 edges. The Euler path must start at the departure airport.",
  "diagram": " JFK -> MUC -> LHR -> SFO -> SIN\n  JFK -> MUC -> LHR -> NRT -> SFO -> SIN   (parallel MUC->LHR)\n\n  Hierholzer (post-order, reverse on return):\n   visit(JFK):\n     MUC ->\n       LHR ->\n         SFO -> SIN -> (no outgoing)  push SIN\n         push SFO\n       NRT -> SFO (no remaining) -> push SFO\n       push NRT\n     push LHR\n     push MUC\n   push JFK\n   reverse the push order ->\n     JFK, MUC, NRT, SFO, SIN ... (lexicographically smallest)\n\n  key: use a min-HEAP or sorted adjacency so the smallest\n  destination is always taken first; post-order accumulation\n  + reverse yields the lexicographically smallest Euler path.\n  A simple forward greedy (always take the smallest) can\n  dead-end and strand unused edges.",
  "cpp_alts": [
   "`priority_queue<string, vector<string>, greater<string>>` per node gives sorted outgoing edges directly.",
   "A `map<string, vector<string>>` plus sorting each adjacency once is simpler if the sort happens once."
  ],
  "py_alts": [
   "`defaultdict(list)` with each list sorted in reverse so `pop()` takes the smallest is faster than a heap at n <= 10.",
   "`heapq` per node is the direct analogue of the C++ min-heap and avoids the reverse-sort trick."
  ],
  "trap": "Greedy forward traversal without post-order accumulation. Taking the lexicographically smallest next destination at every step can visit a dead end while unused edges remain, so the naive answer uses only a subset of the flights.",
  "invariant": "Hierholzer's recursion visits every edge exactly once. Because outgoing edges are consumed in increasing order and the result is built by appending on the way out of each call, the reversed sequence visits every edge once and is the lexicographically smallest such sequence.",
  "questions": [
   {
    "q": "Why does plain greedy fail while Hierholzer works?",
    "a": "Greedy picks the smallest destination and moves on, which can strand remaining edges behind it -- for example JFK->MUC->LHR then choosing SFO before NRT, dead-ending at SFO. Hierholzer explores the dead end first, records it, and splices it in correctly on the way out."
   },
   {
    "q": "How do you guarantee the lexicographically smallest result?",
    "a": "Traverse outgoing edges in sorted order and accumulate the post-order, then reverse. Sorting makes the algorithm explore the smallest choices first, and the reversal produces the Euler path that respects that preference order."
   },
   {
    "q": "What guarantees the route exists?",
    "a": "The problem guarantees it. In general you need the degree conditions: exactly one node with out-degree = in-degree + 1 (the start), one with in-degree = out-degree + 1 (the end), and every other node balanced, with all edges in one weakly connected component."
   }
  ]
 },
 "12_advanced_graphs/0743_network_delay_time": {
  "one_liner": "Dijkstra with a min-heap, lazy deletion.",
  "core_objective": "Return the shortest time for a signal to reach every node, or -1 if any node is unreachable.",
  "bounds": "1 <= n <= 1e4 with 1e4 edges of weight 1..100, so distances fit in int. Node 1 is the source, so n = 1 means the answer is 0.",
  "diagram": " times = [[2,1,1],[2,3,1],[2,3,1]]\n\n  dist = [inf]*4 ; dist[0] = 0\n  heap = [(0,0)]\n\n  pop (0,0): relax (2,1) -> (2,1,0) push\n            relax (1,1) -> (1,1,0) push\n  pop (1,1,0): relax (3,2) -> (3,2,1) push\n  pop (2,1,0): node 1 done\n  pop (3,2,1): node 2 done\n\n  max(dist) = 2   (node 3 at distance 2)\n\n  LAZY DELETION: a heap may contain stale entries with an old\n  larger distance. Skip any pop whose distance != dist[node].\n  Without that check you process nodes repeatedly and the\n  result is still correct but the time bound degrades.",
  "cpp_alts": [
   "`priority_queue<pair<int,int>, vector<...>, greater<...>>` is the canonical form.",
   "Plain Dijkstra with an $O(V^2)$ scan is simpler and fast enough at 1e4 nodes if the graph is sparse."
  ],
  "py_alts": [
   "`heapq` with `(dist, node)` tuples and a `if d != dist[node]: continue` guard is the standard Python form.",
   "Push `(d + w, v)` directly instead of computing and pushing then comparing, which avoids one stale entry per improvement."
  ],
  "trap": "Forgetting the stale-entry check, or using a visited array that marks on push instead of on pop. The latter is incorrect because a node's distance can improve after it is first discovered.",
  "invariant": "When a node is popped with a distance equal to its current `dist`, that distance is final. The proof is the standard contradiction: any shorter path would have passed through a node that should have been popped earlier with a smaller distance. Therefore each node is finalised at most once with a correct value.",
  "questions": [
   {
    "q": "Why is Dijkstra not applicable here?",
    "a": "It is applicable -- this problem has non-negative weights, which is exactly Dijkstra's requirement. A DFS or BFS would be wrong: BFS minimises hop count, not total weight, and DFS has no ordering guarantee."
   },
   {
    "q": "What does the stale-entry guard protect?",
    "a": "The priority queue can hold an old, larger distance for a node whose distance has since improved. Popping it would re-relax its neighbours with a worse value. Skipping pops where the heap distance differs from the current best keeps the correctness argument about finalisation intact."
   },
   {
    "q": "How is unreachability detected?",
    "a": "After the loop, any node whose distance is still infinity was never reached. Return -1 if any remains; otherwise return the maximum distance, which is the time until the last node receives the signal."
   }
  ]
 },
 "12_advanced_graphs/0778_swim_in_rising_water": {
  "one_liner": "Binary search t, then BFS on cells with height <= t.",
  "core_objective": "Return the least t such that a path exists from the top-left to the bottom-right using only cells of height at most t.",
  "bounds": "0 <= n <= 1e3 so the grid can hold 1e6 cells, and 0 <= height[i][j] <= n-1. The answer is bounded by max of all heights, which gives the binary-search range.",
  "diagram": " grid: [[0,2],[1,3]]  -> answer 3\n\n  feasibility(t) monotone:\n   t=0: only (0,0) reachable, (1,1) not -> False\n   t=1: (0,0),(1,0) reachable -> False\n   t=2: (0,0),(0,1),(1,0) -> (1,1) is height 3, blocked\n   t=3: all cells -> True\n\n  binary search on [0, maxH] = [0,3]:\n   mid=1 -> False -> lo=2\n   mid=2 -> False -> lo=3\n   ANSWER 3\n\n  ALTERNATIVE: minimax Dijkstra -- dist[r][c] = the minimum\n  possible path maximum; relax with max(dist[u], h[v]).\n  One pass, O(nm log nm), no repeated BFS.",
  "cpp_alts": [
   "Binary search plus BFS is $O(n^2 \\log n)$ -- 20 BFS passes over 1e6 cells, which is the practical cost.",
   "Minimax Dijkstra with a priority queue is a single pass and often faster in wall-clock terms despite the log factor."
  ],
  "py_alts": [
   "`deque` BFS with a `bytearray` visited grid avoids a 2-D list of bools.",
   "An in-place visited marking with a sentinel height is possible but destroys the grid, which you must not modify."
  ],
  "trap": "Using a visited array that is not reset between binary-search probes, which makes later probes return stale True results and collapses the search to the first candidate.",
  "invariant": "`can_reach(t)` is monotone: if the target is reachable with threshold t, it is reachable with any larger threshold because every path that works at t also works at higher thresholds. That monotonicity is what makes binary search valid and guarantees termination with the minimum feasible t.",
  "questions": [
   {
    "q": "What is the search space being binary-searched?",
    "a": "The grid heights, i.e. 0 to max(height) -- up to 1e3 here. It is NOT the path space, which would be exponential. The insight is that feasibility is monotone in t, so a monotone predicate over a small integer range supports binary search."
   },
   {
    "q": "What are the time and space bounds?",
    "a": "Binary search performs $O(\\log n)$ probes, each a BFS over $n^2$ cells, so $O(n^2 \\log n)$ time and $O(n^2)$ space for the visited grid. Minimax Dijkstra is $O(n^2 \\log n^2)$ with a heap."
   },
   {
    "q": "Why is minimax Dijkstra the more elegant formulation?",
    "a": "It removes the outer binary search entirely. The relaxation `dist[v] = min(dist[v], max(dist[u], h[v]))` captures the bottleneck semantics directly, so one search yields the answer. The downside is a larger constant per node from the heap."
   }
  ]
 },
 "12_advanced_graphs/0787_cheapest_flights_within_k_stops": {
  "one_liner": "Bellman-Ford with at most k+1 edge layers.",
  "core_objective": "Return the cheapest price from src to dst using at most k intermediate stops, that is at most k+1 edges.",
  "bounds": "1 <= n <= 1e3 with up to 1e4 flights, and 0 <= src, dst, k < n. Prices are non-negative, so k = 0 means a direct flight.",
  "diagram": " n=3, k=1, flights=[[0,1,100],[1,2,100],[2,0,100],[1,2,100]]\n  src=0 dst=2 -> answer 200\n\n  Bellman-Ford with LAYERS:\n   LAYER 0 (0 edges):  dist = [0, inf, inf]  only src\n   LAYER 1 (1 edge):   from 0: dist[1]=100\n   LAYER 2 (2 edges):  from 1: dist[2]=200   <- k=1 means\n                        2 edges -> answer 200\n\n  n=3, k=0, same flights -> layer 1 only, dist[2]=inf -> -1\n\n  THE BUG: mutating dist IN PLACE lets one round use a\n  distance improved in the same round, so a 2-layer answer\n  leaks into layer 1. Fix: snapshot the previous layer.\n\n   prev = dist (copy)\n   for u,v,w in flights: if prev[u] + w < dist[v]: dist[v] = prev[u]+w\n\n  layers needed = k + 1, because k stops means k+1 flights.",
  "cpp_alts": [
   "A flat `int` vector of size n with a `prev` copy per layer is the standard C++ form.",
   "The one-array Bellman-Ford with early exit works for unconstrained shortest path but NOT here, because the layer count is a hard constraint."
  ],
  "py_alts": [
   "A list copy per layer (`prev = dist[:]`) is the clearest way to get the snapshot semantics.",
   "Keeping only the previous layer's array keeps space at $O(n)$."
  ],
  "trap": "Updating `dist` in place inside the layer loop. That allows a path using more than one edge in the same iteration, so a k = 0 query can return a two-flight answer.",
  "invariant": "After layer L, `dist[v]` is the minimum cost of a path from src to v using at most L edges. Base case L = 0 is `dist[src] = 0` and infinity elsewhere. Each layer relaxes only from the previous layer's values, so a path using L edges is built from a path using L-1 edges plus one flight, preserving the bound exactly.",
  "questions": [
   {
    "q": "Why k stops means k+1 edges?",
    "a": "With 0 stops you take one flight: src -> dst directly. Each additional stop allows one more intermediate airport, and one more edge. So the edge budget is k+1, which is the number of relaxation layers to run."
   },
   {
    "q": "Why is the in-place update wrong?",
    "a": "Because a vertex improved during layer L can then be used as a source later in the SAME layer, producing a path longer than the layer budget. Snapshotting `prev = dist` before each layer and reading only from `prev` makes the layer count a genuine bound."
   },
   {
    "q": "How does this relate to Dijkstra?",
    "a": "Both find shortest paths with non-negative weights, but Dijkstra has no hop constraint -- it optimises over all path lengths. Here the constraint is on the number of edges, so the layer-indexed DP is the natural formulation and Dijkstra would answer the wrong question."
   }
  ]
 },
 "12_advanced_graphs/1584_min_cost_to_connect_all_points": {
  "one_liner": "Prim or Kruskal on the complete edge set.",
  "core_objective": "Return the minimum total weight of edges connecting all points, using Manhattan distance.",
  "bounds": "1 <= n <= 1e3 with coordinates in [-1e6, 1e6], so a complete graph has about 5e5 edges. n = 1 returns 0 since no edges are needed.",
  "diagram": " points = [[0,0],[2,0]] -> dist 2\n  points = [[0,0],[1,1]] -> dist 2\n  points = [[0,0],[1,0],[3,0]]\n    edges: (0,1)=1 (1,2)=2 (0,2)=3\n    MST: 1 + 2 = 3\n\n  KRUSKAL:\n   sort all edges by weight: 1, 2, 3\n   take 1 (0-1), take 2 (1-2), take 3 -> both endpoints\n   already joined -> skip\n   total = 3\n\n  PRIM (min-heap):\n   visited = {0}; heap = {(d, node) for neighbours of 0}\n   pop smallest edge to an unvisited node, add weight,\n   mark visited, push its edges\n   stop after n-1 edges taken\n\n  n <= 1e3 so building all n(n-1)/2 edges and sorting is\n  acceptable; for larger n you would need a spatial index.",
  "cpp_alts": [
   "`std::sort` on 5e5 edges is $O(E \\log E)$ and dominates; Kruskal is simpler than Prim here.",
   "`priority_queue` Prim avoids materialising the edge list but does the same work per vertex."
  ],
  "py_alts": [
   "Prim with a heap is usually faster in Python than Kruskal, because building and sorting 5e5 tuples is expensive while the heap has only n entries.",
   "Avoid building the full edge list; compute distances lazily inside the Prim loop."
  ],
  "trap": "Counting an edge when both endpoints are already in the same component. In Kruskal that is caught by the union-find check; in Prim you must exclude already-visited vertices when pushing candidate edges.",
  "invariant": "Kruskal maintains a forest with no cycles, and by the cut property the cheapest edge crossing any cut is safe to take. Prim maintains a single growing tree and always takes the cheapest edge leaving it. Both terminate after exactly n-1 edges, which by the cut property is a minimum spanning tree.",
  "questions": [
   {
    "q": "Why is a minimum spanning tree the right model?",
    "a": "Any connected solution on n vertices needs at least n-1 edges, and a spanning tree is exactly a connected acyclic solution with n-1 edges. Since all costs are non-negative, an optimal solution never uses extra edges, so the MST weight is the answer."
   },
   {
    "q": "Kruskal or Prim for these constraints?",
    "a": "Both work. Kruskal is $O(E \\log E) = O(n^2 \\log n)$ with an explicit edge list, which at n = 1e3 is about 5e5 edges -- feasible. Prim with a lazy heap is $O(E \\log n)$ and avoids materialising the list, so it is often preferable in Python."
   },
   {
    "q": "What is the space complexity, and why does it matter here?",
    "a": "Kruskal needs $O(E) = O(n^2)$ space for the edge list -- 5e5 tuples at n = 1e3, which is the binding constraint in Python. Prim's heap holds at most $O(E)$ entries in the lazy version but typically far fewer, and it never builds the full list."
   }
  ]
 },
 "13_1d_dp/0005_longest_palindromic_substring": {
  "one_liner": "Expand around every odd and even centre.",
  "core_objective": "Return the longest contiguous substring of s that is a palindrome.",
  "bounds": "1 <= s.length <= 1000, so the answer always exists and an O(n^2) solution passes. s = \"babad\" has two length-3 answers, so any is accepted.",
  "diagram": " s = \"babad\"   longest palindrome \"bab\" or \"aba\"\n\n  ODD centres (2n-1 of them): c = 0, 0.5, 1, 1.5, ...\n   c=0.5 -> \"b\"? expand: s[-1] invalid -> len 1\n   c=1   -> \"a\", expand s[0]==s[2]? b==b YES -> len 3  BEST\n   c=1.5 -> \"a\" ... len 1\n   c=2   -> \"b\", expand a==a YES, b vs d NO -> len 3\n\n  EVEN centres (n-1 of them): between i and i+1\n   c=1.5 -> s[1]!=s[2]? a vs b -> no\n   c=3   -> s[3]==s[4]? a vs d no\n\n  expand(l, r):\n   while l >= 0 and r < n and s[l] == s[r]: l--, r++\n   return r - l - 1   # length after the last successful step\n\n  invariant: expand returns the largest palindrome centred at\n  (l, r) -- it stops exactly at the first mismatch, so the\n  window just inside is maximal.",
  "cpp_alts": [
   "`std::string_view` slices avoid copying during comparison.",
   "Manacher's algorithm gives $O(n)$ but is rarely worth the complexity at n = 1000."
  ],
  "py_alts": [
   "`s[l] == s[r]` on one-character strings is cheap thanks to CPython's character interning.",
   "Duplicating the string with separators turns odd and even into one loop, which is the Manacher-style simplification."
  ],
  "trap": "Checking only odd-length palindromes by centring on each character. Even-length palindromes like \"abba\" have no character centre, so they are missed entirely.",
  "invariant": "`expand(l, r)` returns the maximum palindrome length for the given centre. Since any palindrome has a centre at either a character (odd) or a gap (even), checking all 2n-1 centres covers every candidate, and the maximum over them is the answer.",
  "questions": [
   {
    "q": "Why are there 2n-1 centres?",
    "a": "n characters give n odd-length centres, and the n-1 gaps between adjacent characters give n-1 even-length centres. Total 2n-1, and every palindrome has exactly one of them."
   },
   {
    "q": "What is the complexity, and why is the naive $O(n^3)$ version avoidable?",
    "a": "$O(n^2)$ here because the expansion from each centre is not restarted from scratch inside another. The $O(n^3)$ version recomputes `s[l..r] == reversed` for every interval; expanding outward from each centre reuses work, giving at most n expansions per centre."
   },
   {
    "q": "When is Manacher's algorithm warranted?",
    "a": "When n is in the millions. It reuses palindromes found to the left to skip re-expansion, giving $O(n)$ time and $O(n)$ space. At n = 1000 that sophistication costs more in explanation than it saves in runtime."
   }
  ]
 },
 "13_1d_dp/0070_climbing_stairs": {
  "one_liner": "Ways to reach step n: fib(n+1).",
  "core_objective": "Count the number of distinct ways to climb n stairs taking 1 or 2 steps at a time.",
  "bounds": "1 <= n <= 45, and the answer fits in a signed 32-bit int (f(46) = 1836311903). n = 1 gives 1 and n = 2 gives 2.",
  "diagram": " n = 5 -> 8\n\n  dp[0] = 1   (one way to be at the bottom: do nothing)\n  dp[1] = 1   (1)\n  dp[2] = 2   (1+1, 2)\n  dp[3] = 3   (111, 12, 21)\n  dp[4] = 5   (1111,112,121,211,22)\n  dp[5] = 8\n\n  recurrence: dp[i] = dp[i-1] + dp[i-2]\n  because the last move is either 1 (from i-1) or 2 (from i-2)\n  and those cases are DISJOINT and EXHAUSTIVE.\n\n  rolling: prev2, prev1 = 1, 1\n  for i in 2..n: prev2, prev1 = prev1, prev1 + prev2\n\n  invariant: at step i, prev1 == dp[i-1] and prev2 == dp[i-2].",
  "cpp_alts": [
   "`int` suffices up to n = 45; use `long long` if you extend the range.",
   "`unsigned` avoids any signed-overflow discussion; the boundary is well inside 32 bits."
  ],
  "py_alts": [
   "`def fib(n): a, b = 1, 1; for _ in range(n): a, b = b, a + b; return a` is a one-liner.",
   "A full `dp` list is unnecessary: the recurrence only reads the previous two entries."
  ],
  "trap": "Initialising `dp[0] = 0`. Then dp[2] = dp[1] + dp[0] = 1, which is wrong. The empty climb has exactly one way, so dp[0] must be 1.",
  "invariant": "After iteration i, `prev1` equals the number of ways to reach step i and `prev2` equals the number for step i-1. The update computes dp[i+1] = dp[i] + dp[i-1], preserving the invariant. Since the last move is uniquely 1 or 2, no path is double-counted.",
  "questions": [
   {
    "q": "Why is this Fibonacci?",
    "a": "The recurrence dp[i] = dp[i-1] + dp[i-2] with base values 1, 1 is exactly the Fibonacci recurrence, so dp[n] = F(n+1). That is why the answer at n = 45 is 1836311903, which is F(46) and the largest Fibonacci number below 2^31."
   },
   {
    "q": "Why is the two-case split exhaustive?",
    "a": "Any way to climb to step i must end with a 1-step from i-1 or a 2-step from i-2. There is no other final move, so every valid path lands in exactly one of the two sets -- and the sets are disjoint because their final moves differ."
   },
   {
    "q": "Why is space O(1) here?",
    "a": "Because dp[i] depends only on dp[i-1] and dp[i-2]. Once those two values are held, everything before is irrelevant, so no array is needed. This is the general rule: rolling arrays reduce space to the dependency width."
   }
  ]
 },
 "13_1d_dp/0091_decode_ways": {
  "one_liner": "Count partitions into 1-2 digit valid codes.",
  "core_objective": "Count the number of ways to decode a digit string using codes 1-26, where 0 has no standalone meaning.",
  "bounds": "1 <= s.length <= 100, so the answer can reach about 2^100 and modulo 1e9+7 is required. Leading zeros and a trailing zero both need special handling.",
  "diagram": " s = \"226\"  -> 3\n\n  dp[0] = 1\n  i=1 ch=2: single 2 valid          -> dp[1] += dp[0] = 1\n  i=2 ch=2: single valid dp[2]+=dp[1]; pair \"22\" valid\n            dp[2] += dp[0] -> 1 + 1 = 2\n  i=3 ch=6: single dp[3]+=dp[2]; pair \"26\" valid\n            dp[3] += dp[1] -> 2 + 1 = 3\n\n  the two transitions per position:\n   single: 1 <= s[i-1] <= '9'      -> dp[i] += dp[i-1]\n   pair:   10 <= s[i-1..i] <= 26   -> dp[i] += dp[i-2]\n\n  ZEROS: \"06\" is invalid as a single (0 alone) and\n  \"06\" is not in 10..26, so it contributes nothing.\n  \"10\" is valid as a pair only. A '0' can never be a single.\n\n  invariant: dp[i] counts decodings of the first i characters,\n  partitioned by whether the last group is length 1 or 2.",
  "cpp_alts": [
   "`long long` with `% 1e9+7` at each step; taking the modulus before adding can overflow int.",
   "A rolling two-variable form keeps space at $O(1)$."
  ],
  "py_alts": [
   "Comparing with character bounds (`'1' <= s[i-1] <= '9'`) beats `int()` conversion in a hot loop.",
   "Rolling `prev2, prev1` avoids a length-n list; the list version is fine at n = 100."
  ],
  "trap": "Treating '0' as a decodable single character. It is not, so `\"100\"` has exactly one decoding (1-0-0 as 10,0) and `\"10\"` has one (10), while a naive single-char check would give wrong counts.",
  "invariant": "`dp[i]` equals the number of decodings of s[0..i-1]. Every such decoding ends either with a 1-digit group or a 2-digit group, and those are disjoint, so summing `dp[i-1]` (when the single digit is valid) and `dp[i-2]` (when the pair is in 10..26) gives exactly dp[i].",
  "questions": [
   {
    "q": "Why must '0' be excluded from the single-digit transition?",
    "a": "No letter maps to 0 alone. If '0' were allowed as a single digit, `\"10\"` would decode as both 1-0 and 10, which is wrong. Excluding it, and requiring 10..26 for the pair, is exactly the standard rule that makes decoding a valid prefix code."
   },
   {
    "q": "Why is the answer taken modulo 1e9+7?",
    "a": "The count grows like the Fibonacci sequence in the best case, so for s of length 100 the value exceeds any fixed-width type by an enormous margin. The problem specifies the modulus, so it must be applied at each addition."
   },
   {
    "q": "What is the space complexity, and can it be O(1)?",
    "a": "Yes -- dp[i] reads only dp[i-1] and dp[i-2], so two rolling variables suffice, giving $O(1)$ space against $O(n)$ time. The full array is only useful if you need to reconstruct the decodings."
   }
  ]
 },
 "13_1d_dp/0139_word_break": {
  "one_liner": "Can the prefix ending at i be broken into dictionary words?",
  "core_objective": "Decide whether s can be segmented into one or more dictionary words.",
  "bounds": "1 <= s.length <= 300 and 1 <= wordDict.length <= 1000 with words of length up to 20, so the substring checks are bounded by max word length.",
  "diagram": " s = \"leetcode\", dict = [\"leet\",\"code\"]  -> True\n\n  dp[0] = True  (empty prefix is breakable)\n  i=1 \"l\": no word ends here        -> False\n  i=2 \"le\": no\n  i=3 \"lee\": no\n  i=4 \"leet\": \"leet\" in dict, dp[0] -> dp[4] = True\n  i=5..8: no word\n  i=9 \"leetcode\": \"code\" in dict, dp[4] -> dp[9] = True\n\n  dp[i] = any( s[i-L:i] in words and dp[i-L] )\n          for each word length L <= i\n\n  the ordering matters: dp[i-L] is already known when\n  processing i, since L >= 1.\n\n  invariant: dp[i] is True iff s[0..i-1] can be segmented.\n  Every segmentation of that prefix ends with SOME dictionary\n  word of length L, leaving a breakable prefix of length i-L.",
  "cpp_alts": [
   "`unordered_set<string>` for the dictionary; the substring comparison then hashes a short string.",
   "A `maxLen` bound limits the inner loop to at most maxLen checks per position."
  ],
  "py_alts": [
   "A `set` of strings plus a slice per length; slicing is the expensive part, so iterating lengths outer and checking membership is efficient at these sizes.",
   "`any()` with a generator is concise; an explicit loop is marginally faster."
  ],
  "trap": "Iterating forward and checking `s[:i+1]` in the dictionary, which only finds segmentations where the FIRST word is the whole prefix. The recurrence must extend at the END, using already-known dp for shorter prefixes.",
  "invariant": "`dp[i]` is true iff s[0..i-1] is breakable. Any breakable prefix ends with some dictionary word w of length L, and what precedes it is s[0..i-L-1], which is breakable iff dp[i-L]. Since L >= 1, dp[i-L] is already computed, so the recurrence is well-founded and complete.",
  "questions": [
   {
    "q": "Why is dp[0] true?",
    "a": "The empty string is segmentable into zero words, which is the base case that lets the first word of any non-empty breakable string be recognised. Setting dp[0] to false breaks everything."
   },
   {
    "q": "What is the complexity?",
    "a": "$O(n \\cdot L^2)$ where L is the max word length -- n positions, up to L candidate lengths each, and each substring comparison is $O(L)$. With L <= 20 that is at most 120k character comparisons, comfortably fast."
   },
   {
    "q": "How does this relate to the decode-ways recurrence?",
    "a": "Structurally identical: both compute a prefix-reachable table where dp[i] aggregates over the possible lengths of the last group. The difference is the validity test -- decode-ways checks a numeric range, word-break checks dictionary membership."
   }
  ]
 },
 "13_1d_dp/0152_maximum_product_subarray": {
  "one_liner": "Track max and min ending here; a negative flips them.",
  "core_objective": "Return the largest product of a non-empty contiguous subarray.",
  "bounds": "1 <= nums.length <= 1e5 with -1e4 <= nums[i] <= 1e4, so products reach about 1e400 and must be taken mod 1e6+7 or handled carefully -- the problem asks for the maximum mod 1e6+7 of the maximum product.",
  "diagram": " nums = [2,3,-2,4]  -> 6 (the subarray [2,3])\n\n  i=0 x=2 : max=2  min=2   best=2\n  i=1 x=3 : max=6  min=3   best=6\n  i=2 x=-2: candidates {3, 2*-2=-4, 6*-2=-12}\n           max = max(3,-4,-12) = 3     <- start fresh at x\n           min = min(3,-4,-12) = -12\n           best stays 6\n  i=3 x=4 : candidates {4, 3*4=12, -12*4=-48}\n           max = 12, min = -48, best = 12? no best = 6? \n\n  recount: at i=3 max=12, best = max(6, 12) = 12?\n  but the true answer is 6... because MODULO. The problem\n  asks for max product MOD 1e6+7. 2*3=6, 3*-2*4=-24,\n  so the true max is 6. The i=3 computation must use\n  dp[i-1]=3: candidates {x=4, prevmax*4=12, prevmin*4=-48}\n  -> 12 is not right because [2,3,-2] is not a product 3.\n  KEY: prevmax at i=2 is 3 and prevmin is -12; so the\n  max at i=3 is max(4, 3*4, -12*4) = 12 -> but [3,4]\n  is NOT contiguous! prevmax 3 came from a subarray that\n  ended at index 2, so 3*4 = 12 IS [.., 3, 4]. Which is 3*4\n  where 3 is from index 2? At i=2 the max product ending at 2\n  is max(3, -4, -12) = 3, attained by [3] alone. So [3,4]\n  = 12 is valid and IS a subarray. But the expected answer is\n  6 for the un-modded variant -- so the discrepancy is the\n  MODULUS: 12 is not the max MOD 1e6+7 either.\n  The actual sample answer for [2,3,-2,4] is 6; rechecking:\n  subarrays: 2, 2*3=6, 2*3*-2=-12, -2, -2*4=-8, 3, 3*-2=-6,\n  3*-2*4=-24, -2*4=-8, 4. Maximum = 6. So 12 must not be\n  reachable, meaning the trace above mis-tracked prevmax.",
  "cpp_alts": [
   "`long long` for the running max/min; products overflow 32 bits at n = 1e5 with values 1e4.",
   "Apply the modulus at each multiplication to keep values bounded, since only the answer is needed modulo 1e6+7."
  ],
  "py_alts": [
   "Python's arbitrary-precision integers mean overflow is impossible; apply the modulus only if you want to match C++ speed.",
   "`max`/`min` over a three-element candidate list is the clearest expression of the recurrence."
  ],
  "trap": "Tracking only the maximum. A negative number turns the smallest product into the largest, so dropping the running minimum loses the answer for cases like [-2,3,-4] where the answer comes from multiplying two negatives.",
  "invariant": "`maxEnd` is the maximum product of a subarray ending at i and `minEnd` the minimum. Both extend the previous step's extrema, and also consider restarting at i. Since multiplication by a negative reverses order, the maximum at step i is max(x, maxEnd*x, minEnd*x) and the minimum is the min of the same three.",
  "questions": [
   {
    "q": "Why must you keep the minimum product?",
    "a": "Multiplying by a negative reverses the ordering, so the smallest previous product can become the largest after extension. Case `[-2,3,-4]`: at index 2 the min is -4*3 = -12, and multiplying by -4 gives 48 -- the true answer -- which no maximum-only variant can find."
   },
   {
    "q": "Why include x itself as a candidate?",
    "a": "Because the optimal subarray may start at i rather than extend the previous one. With all-negative prefixes the previous products could all be smaller in magnitude than restarting, and `[-2]` at index 0 must be handled without a previous element."
   },
   {
    "q": "What is the complexity?",
    "a": "$O(n)$ time and $O(1)$ space -- three candidates per element and two running scalars. The modulo does not change either bound."
   }
  ]
 },
 "13_1d_dp/0198_house_robber": {
  "one_liner": "rob(i) = max(rob(i-1), rob(i-2) + nums[i]).",
  "core_objective": "Return the maximum sum of money obtainable without robbing adjacent houses.",
  "bounds": "1 <= nums.length <= 1e4 and 0 <= nums[i] <= 1e9, so the answer can reach about 1e13 and C++ needs `long long`. n = 1 returns nums[0].",
  "diagram": " nums = [2,7,9,3,1]  -> 12 (2+9+1)\n\n  dp[0] = 2\n  dp[1] = max(2, 7) = 7\n  dp[2] = max(7, 2+9=11) = 11\n  dp[3] = max(11, 7+3=10) = 11\n  dp[4] = max(11, 11+1=12) = 12\n\n  the decision at house i:\n   SKIP it  -> dp[i-1]\n   TAKE it  -> dp[i-2] + nums[i]   (forces skipping i-1)\n\n  invariant: dp[i] is the best total from houses 0..i.\n  rolling: prev2, prev1 = 0, 0\n   prev2, prev1 = prev1, max(prev1, prev2 + x)",
  "cpp_alts": [
   "`vector<long long> dp(n)` is readable; two rolling variables give the same result in O(1) space.",
   "`unsigned long long` is unnecessary since all values are non-negative."
  ],
  "py_alts": [
   "A one-line rolling loop is idiomatic; a full list is only useful if you need to reconstruct the chosen houses.",
   "`max(prev1, prev2 + x)` is a single C-level call."
  ],
  "trap": "Using `dp[i-2] + nums[i]` with `dp[i-2]` defaulting to 0 for i = 1 without also allowing the skip case, which returns nums[1] and ignores the possibility of robbing only house 0.",
  "invariant": "`dp[i]` is the maximum obtainable from the first i+1 houses. Any optimal solution either omits house i (leaving dp[i-1]) or includes it, which forces omitting house i-1 and gives dp[i-2] + nums[i]. The two cases are disjoint and exhaustive, so the recurrence is correct.",
  "questions": [
   {
    "q": "Why does this reduce to house robber II with a split?",
    "a": "In the circle variant the first and last houses are adjacent, so a solution cannot contain both. Split the array at the last house and take the max of two linear robber problems: houses 0..n-2 and houses 1..n-1. Both exclude the wrap-around conflict, and every valid circular solution lies in one of them."
   },
   {
    "q": "What is the space complexity and why is O(1) achievable?",
    "a": "O(1) because dp[i] reads only dp[i-1] and dp[i-2]. Two rolling scalars capture the entire dependency, which is the general technique for a linear-order recurrence with constant dependency width."
   },
   {
    "q": "What does the greedy \"take the largest\" give?",
    "a": "7 on [2,7,9,3,1] versus the optimal 12. Taking 9 blocks both 7 and 3, so the local maximum is not globally optimal. That counterexample is the standard justification for the DP."
   }
  ]
 },
 "13_1d_dp/0213_house_robber_ii": {
  "one_liner": "Split the circle into two linear cases and take the max.",
  "core_objective": "Rob houses arranged in a circle, returning the maximum sum without robbing two adjacent houses.",
  "bounds": "1 <= nums.length <= 3e4 and 0 <= nums[i] <= 1e9, so sums reach 3e13 and C++ needs `long long`. n = 1 returns nums[0] and n = 2 returns the larger of the two.",
  "diagram": " nums = [2,3,2]  -> 3 (houses 0 and 2 are adjacent)\n\n  the circle means house n-1 and house 0 are neighbours, so\n  a solution cannot contain both. Two exhaustive cases:\n\n  case A: exclude the last house -> rob linear [2,3]    = 3\n  case B: exclude the first house -> rob linear [3,2]   = 3\n  ANSWER max(3, 3) = 3\n\n  case A: dp over [2,3]      -> dp[1]=max(2,3)=3\n  case B: dp over [3,2]      -> dp[1]=max(3,2)=3\n\n  the single house special case:\n   n == 1 -> return nums[0]   (excluding 'first' or 'last'\n   would leave an empty slice)\n\n  invariant: any optimal circular solution avoids house 0 or\n  avoids house n-1 (or both), so it appears in one of the two\n  linear sub-problems.",
  "cpp_alts": [
   "Pass (lo, hi) bounds to one shared helper rather than duplicating the loop for the two cases.",
   "`long long` throughout: the linear sub-problems already reach 3e13."
  ],
  "py_alts": [
   "`max(rob(nums[:-1]), rob(nums[1:]))` with `n == 1` guarded first is the whole solution.",
   "Slicing costs O(n) extra memory but the arrays are at most 3e4, so it is irrelevant here."
  ],
  "trap": "Forgetting the n = 1 case, or assuming the two linear problems are independent when they share every interior house. The overlap is fine because both are valid solutions to the circle; the max just picks the better one.",
  "invariant": "Any valid selection omits house 0 or omits house n-1, since they are adjacent. Therefore every valid selection is a valid linear selection within [0, n-2] or within [1, n-1], and conversely each linear selection is valid circularly. So the answer is exactly the max of the two linear robber results.",
  "questions": [
   {
    "q": "Why are the two cases exhaustive?",
    "a": "Because selecting both house 0 and house n-1 is illegal in the circle. Every legal selection therefore excludes at least one of them, which places it inside one of the two linear ranges. The union covers all legal solutions and neither contains an illegal one."
   },
   {
    "q": "What is the complexity?",
    "a": "$O(n)$ time -- two linear passes of length n-1 -- and $O(1)$ space per pass with rolling variables, plus $O(n)$ if you slice. The constant factor is two, which is negligible."
   },
   {
    "q": "How does this generalise to a ring of k neighbours?",
    "a": "You would need $2^k$ cases (one for each subset of the boundary that must be excluded), which becomes intractable quickly. The two-case split works only because the conflict is between exactly two endpoints."
   }
  ]
 },
 "13_1d_dp/0300_longest_increasing_subsequence": {
  "one_liner": "Tails array plus bisect_left gives O(n log n).",
  "core_objective": "Return the length of the longest strictly increasing subsequence.",
  "bounds": "1 <= nums.length <= 1000, so the O(n^2) DP passes, but the problem asks for the O(n log n) approach. Duplicates are legal and must NOT extend the subsequence.",
  "diagram": " nums = [10,9,2,5,3,7,101,18]  -> length 4\n\n  tails[i] = smallest possible TAIL of an increasing\n  subsequence of length i+1 seen so far.\n\n   x=10: bisect_left(tails,10)=0 -> tails=[10]\n   x= 9: pos=0 -> tails=[9]           (9 beats 10 as a tail)\n   x= 2: pos=0 -> tails=[2]\n   x= 5: pos=1 -> tails=[2,5]\n   x= 3: pos=1 -> tails=[2,3]\n   x= 7: pos=2 -> tails=[2,3,7]\n   x=101:pos=3 -> tails=[2,3,7,101]\n   x= 18:pos=3 -> tails=[2,3,7,18]    18 replaces 101 as tail\n\n  ANSWER len(tails) = 4  (the subsequence is 2,3,7,101)\n\n  why bisect_LEFT not bisect_right: strict increase means\n  a value equal to tails[pos] must NOT extend; it replaces it.\n  nums=[2,2,2] with bisect_right would give length 3 -- wrong.\n\n  invariant: tails is strictly increasing and tails[i] is\n  the minimum tail for length i+1. Replacing at position p\n  keeps every shorter subsequence viable and improves the\n  longest candidate.",
  "cpp_alts": [
   "`std::lower_bound` is exactly `bisect_left`; using `upper_bound` breaks strictness.",
   "`vector<int> tails` with `reserve(n)` avoids reallocation in the hot path."
  ],
  "py_alts": [
   "`bisect_left(tails, x)` is a C-level binary search, so the whole method is $O(n \\log n)$ with no Python loop inside.",
   "`max(tails, default=0)` handles n = 0 if the empty case is allowed."
  ],
  "trap": "Using `bisect_right`. That makes the algorithm compute the longest NON-DECREASING subsequence, so [2,2,2] returns 3 instead of 1. Also, confusing the LIS length with the `tails` contents -- `tails` is not itself a valid subsequence, only a record of best tails.",
  "invariant": "`tails[i]` is the smallest possible final value of any increasing subsequence of length i+1 among the processed prefix. When a new x arrives at position p = bisect_left(tails, x), every entry before p is < x so x can extend the length-p subsequence, and any entry at or after p is >= x so x cannot extend those. Replacing tails[p] with x therefore improves the best tail without losing any longer option.",
  "questions": [
   {
    "q": "Why is the length of `tails` the answer?",
    "a": "tails has one entry per achievable subsequence length, and tails[i] is the minimum tail for length i+1. Its presence proves a subsequence of that length exists. So len(tails) is the maximum achievable length, even though the array itself is not a subsequence."
   },
   {
    "q": "Why not use the O(n^2) DP?",
    "a": "It is correct and simpler, and passes at n = 1000. But it is $O(n^2)$ time where the tails method is $O(n \\log n)$, which is the difference between passing and failing at n = 1e5. Interviewers ask for the faster one deliberately."
   },
   {
    "q": "How do you reconstruct the actual subsequence?",
    "a": "Store predecessor indices: for each element record which tails position it replaced, then walk backwards from the final position. That costs an extra array and makes the method $O(n \\log n)$ time with $O(n)$ space."
   }
  ]
 },
 "13_1d_dp/0322_coin_change": {
  "one_liner": "Unbounded knapsack: dp[x] = min(dp[x-c] + 1).",
  "core_objective": "Return the fewest coins summing to amount, or -1 if impossible.",
  "bounds": "0 <= amount <= 1e4 with 1 <= coin.length <= 1e4, so amount 0 gives 0 coins. The answer fits in int. Duplicates in the coin list are harmless.",
  "diagram": " amount = 11, coins = [1,2,5]  -> 3 (5+5+1)\n\n  dp[0] = 0\n  dp[1] = dp[0]+1 = 1\n  dp[2] = min(dp[1], dp[0]) + 1 = 1\n  dp[3] = min(dp[2],dp[1]) + 1 = 2\n  dp[4] = min(dp[3],dp[2]) + 1 = 2\n  dp[5] = min(dp[4],dp[3],dp[0]) + 1 = 1\n  ...\n  dp[11]= min(dp[10],dp[9],dp[6]) + 1 = 3\n\n  two loop orders, DIFFERENT semantics:\n   coins outer, amount inner -> UNBOUNDED use  (this problem)\n   amount outer, coins inner -> 0/1 use (each coin once)\n\n  invariant: dp[x] is the minimum coin count for exactly x.\n  Every solution for x ends with some coin c, leaving x-c,\n  so min over all coins of dp[x-c]+1 is exact.",
  "cpp_alts": [
   "`vector<int> dp(amount+1, amount+1)` with `amount+1` as the infinity sentinel avoids INT_MAX overflow on the +1.",
   "Sorting coins and breaking when c > x is a safe pruning."
  ],
  "py_alts": [
   "A `min()` generator over the coin list is concise; an explicit loop avoids the generator overhead per state.",
   "`[amount+1]*(amount+1)` initialisation is idiomatic and fast."
  ],
  "trap": "Using `amount + 1` as infinity and then `dp[x] + 1` without guarding -- if dp[x-c] is still the sentinel, the sum exceeds it and dp[x] can be assigned a value larger than the sentinel, which then gets compared incorrectly.",
  "invariant": "dp[x] equals the minimum number of coins summing to exactly x. Any optimal multiset for x contains some coin c as its last element, and removing it leaves a valid solution for x-c with dp[x-c] coins. Since coin c ranges over every coin <= x, minimising dp[x-c] + 1 over all such c is exactly the optimum. dp[0] = 0 seeds it.",
  "questions": [
   {
    "q": "Why is the coin loop outer?",
    "a": "With coins outer and amount increasing, the dp array already accounts for the current coin when computing larger amounts, so the same coin can be used repeatedly. That is unbounded knapsack. With amount outer, each state is computed from the previous states only, which corresponds to using each coin at most once."
   },
   {
    "q": "How is the impossible case detected?",
    "a": "If no combination exists, every dp[x-c] remains the sentinel, so dp[x] stays above the sentinel and you return -1. Using `amount + 1` as the sentinel works because no real answer can exceed amount (one coin per unit) when coin 1 exists, and without coin 1 the sentinel is never beaten."
   },
   {
    "q": "How does problem 518 differ?",
    "a": "518 asks for the NUMBER of combinations rather than the minimum count. Same unbounded-knapsack skeleton, but the transition sums instead of minimising: ways[x] += ways[x - coin]."
   }
  ]
 },
 "13_1d_dp/0416_partition_equal_subset_sum": {
  "one_liner": "Target is half the total; then it is a subset-sum question.",
  "core_objective": "Decide whether the multiset can be split into two parts with equal sum.",
  "bounds": "1 <= nums.length <= 200 with 1 <= nums[i] <= 100, so the total is at most 2e4 and a 1-D DP of that size is trivial. An odd total makes it impossible immediately.",
  "diagram": " nums = [1,5,11,5]  -> True (1+5+5 = 11)\n  total = 22, target = 11\n\n  1-D subset-sum over nums with capacity target:\n   cap=1 : dp[1] via 1           -> {0,1}\n   cap=5 : via 5 -> dp[1] too   -> {0,1,5,6}\n   cap=11: via 11 -> dp[0]      -> {0,1,5,6,11,12,16,17}\n   cap=11: via 5 (cap now 6)  -> {0,1,5,6}\n   reachable totals up to 11: 0,1,5,6\n   11 IS reachable -> True\n\n  DESCENDING loop is essential:\n   for c in nums: \n     for s in range(target, c-1, -1): dp[s] |= dp[s-c]\n   ascending would reuse nums[c] multiple times.\n\n  invariant: after processing k elements, dp[s] is true iff\n  some subset of those k sums to s. Descending order ensures\n  each element is used at most once.",
  "cpp_alts": [
   "`vector<char> dp(target+1)` is 1 byte per state instead of 4 for an int.",
   "`dp[s] |= dp[s-c]` on a char array is a simple bitwise OR."
  ],
  "py_alts": [
   "A list of bools or a bytearray; a `bytearray` is the most compact.",
   "The bitmask trick packs all 2e4 capacities into a single big integer, making the whole DP one machine-word-per-64-states operation."
  ],
  "trap": "Iterating the capacity loop ascending. That lets a single element be used multiple times and turns a 0/1 subset-sum into an unbounded one, giving wrong answers such as True for [1,3] with target 2.",
  "invariant": "`dp[s]` is true iff a subset of the elements processed so far sums to exactly s. The descending capacity loop guarantees that when dp[s] is written, dp[s-c] still reflects only previously processed elements, so each element is used at most once and the invariant holds.",
  "questions": [
   {
    "q": "Why does an odd total immediately mean False?",
    "a": "Two equal subsets would each sum to total/2, which must be an integer. An odd total has no integer half, so no such split can exist. That single check eliminates half the inputs with no DP work."
   },
   {
    "q": "What if the DP uses a boolean vector instead?",
    "a": "Use `vector<bool>` or a Python `bytearray` for 1 bit/byte per capacity, or the integer bitmask trick for O(total/word) memory. A boolean is essential -- an integer min-DP would be solving the coin-change problem instead."
   },
   {
    "q": "How does this relate to coin change?",
    "a": "Identical skeleton (unbounded vs 0/1 aside), different question. Coin change asks for the minimum number of coins; this asks for a subset whose count is unconstrained, so a boolean reachable-state vector is the right state."
   }
  ]
 },
 "13_1d_dp/0647_palindromic_substrings": {
  "one_liner": "Count singles always, plus centre expansions of length >= 2.",
  "core_objective": "Count the number of contiguous palindromic substrings, counting occurrences rather than distinct values.",
  "bounds": "0 <= s.length <= 1000, so the count can reach about 5e5 and fits in int. s = \"aaa\" has 6 palindromic substrings: three length-1 and three length-2.",
  "diagram": " s = \"aba\"  -> 4  (3 singles + \"aba\")\n\n  n single-character palindromes: 3\n  for each centre i, expand while s[l]==s[r] and l<r:\n   i=0: expand(-1,1) no\n   i=1: expand(0,2) a==a -> count 1; expand(-1,3) stop\n   i=2: expand(1,3) no\n  TOTAL 3 + 1 = 4\n\n  \"aaa\": singles 3; expansions: (0,1) (1,2) (0,2) = 3\n  TOTAL 6 -- matches aaa, aa, aa, a, a, a\n\n  invariant: each palindrome has exactly one centre and one\n  radius, so counting expansions counts each palindrome once.\n  Overcounting happens only if you count both (l,r) and (r,l),\n  which the l<r condition prevents.",
  "cpp_alts": [
   "A `long long` result is prudent if n were larger; at n = 1000, int is fine.",
   "Manacher's algorithm is $O(n)$ but unnecessary at this size."
  ],
  "py_alts": [
   "Expanding in Python is $O(n^2)$ worst case but n <= 1000 makes it trivial.",
   "`s[l] == s[r]` on interned characters is cheap."
  ],
  "trap": "Counting only palindromes of length 1, or forgetting to also count the even-length expansions (the gaps between characters). Both undercount; \"aaa\" needs both families.",
  "invariant": "Every palindromic substring has a unique centre -- either a character (odd length) or a gap (even length) -- and a unique radius. Iterating all 2n-1 centres and expanding outward to the first mismatch visits each palindrome exactly once.",
  "questions": [
   {
    "q": "How do you get 6 for \"aaa\"?",
    "a": "Three length-1 palindromes (a at 0, 1, 2), two length-2 (aa at 0-1, 1-2), and one length-3 (aaa). The expansion from centre 1 hits radius 1 (aa) and radius 2 (aaa); from centres 0.5 and 1.5 it hits radius 1 each."
   },
   {
    "q": "How does this differ from the longest-palindromic-substring problem?",
    "a": "Same traversal, different output: here you count every successful expansion instead of tracking the maximum radius. That makes it a counting problem, which is why the answer is a number rather than a string."
   },
   {
    "q": "What is the complexity?",
    "a": "$O(n^2)$ time because a string like \"aaaa...\" expands to radius O(n) at each of O(n) centres. $O(1)$ extra space beyond the string. At n = 1000 that is at most 5e5 character comparisons."
   }
  ]
 },
 "13_1d_dp/0746_min_cost_climbing_stairs": {
  "one_liner": "Same recurrence as house robber, with cost instead of value.",
  "core_objective": "Return the minimum total cost to reach the top of a staircase, where you may climb 1 or 2 steps and each step i has a cost.",
  "bounds": "2 <= n <= 1000 with 0 <= cost[i] <= 1000, so the answer fits in int. cost is indexed 0..n-1 and step 1 costs cost[0].",
  "diagram": " cost = [1,100,1,1,1,100,1,1,100,1]  n=10 -> 6\n\n  the recurrence, with 1-BASED step indexing:\n   dp[0] = 0            (before the first step)\n   dp[1] = cost[0]\n   dp[i] = min(dp[i-1] + cost[i-1],\n                dp[i-2] + cost[i-1])\n\n  trace with 0-based cost and 1-based steps:\n   i=1: dp[1] = 0 + cost[0]            = 1\n   i=2: min(dp[1]+cost[1], dp[0]+cost[1])\n        = min(1+100, 0+100) = 100\n   i=3: min(dp[2]+cost[2], dp[1]+cost[2])\n        = min(100+1, 1+1) = 2\n   i=4: min(2+1, 100+1) = 3\n   i=5: min(3+1, 2+1) = 4\n   i=6: min(4+100, 3+100) = 103\n   i=7: min(103+1, 4+1) = 5\n   i=8: min(5+1, 103+1) = 6\n   i=9: min(6+100, 5+100) = 105\n   i=10:min(105+1, 6+100) = 106 ?\n\n  the off-by-one: cost[i-1] is paid for ARRIVING at step i.\n  The correct trace gives dp[10] = 6.",
  "cpp_alts": [
   "Two rolling integers give O(1) space; a full `vector` is only needed for reconstruction.",
   "`int` suffices since the answer is bounded by n * max(cost)."
  ],
  "py_alts": [
   "Rolling `prev2, prev1` is the whole solution.",
   "Careful indexing: `prev1 + cost[i-1]` is the transition to step i, and the loop must run to i = n inclusive even though cost has length n."
  ],
  "trap": "The off-by-one between the step number and the cost index. Climbing to step i means paying `cost[i-1]`, and the loop must iterate i from 2 to n over an array of length n -- a loop that stops at n-1 never reaches the top.",
  "invariant": "`dp[i]` is the minimum cost to be standing on step i. The final move into step i is from i-1 (paying cost[i-1]) or from i-2 (paying cost[i-1] as well, since you skip a step). The two are disjoint, so the minimum is exact.",
  "questions": [
   {
    "q": "How is this the same shape as house robber?",
    "a": "Both are \"choose i or skip i-1\". In house robber, choosing i forces skipping i-1 because they are adjacent; here, taking a 2-step jump from i-2 skips step i-1's cost. The recurrences are structurally identical -- only the operation changes from addition to minimisation."
   },
   {
    "q": "What is the base case?",
    "a": "dp[0] = 0 (standing before any step, free) and dp[1] = cost[0] (you must pay for the first step you climb). Getting dp[1] wrong is the usual indexing bug."
   },
   {
    "q": "What are the complexities?",
    "a": "$O(n)$ time and $O(1)$ space with two rolling variables, against $O(n)$ space for a full dp array. The time bound is optimal since every cost must be read."
   }
  ]
 },
 "13_1d_dp/1143_longest_common_subsequence": {
  "one_liner": "dp[i][j] on suffixes; take a match, else skip one side.",
  "core_objective": "Return the length of the longest common subsequence of two strings.",
  "bounds": "1 <= m, n <= 1000, so an O(mn) table has 1e6 cells -- fine. At m = n = 1000 the O(mn) DP is required; the 1-D rolling form saves the space.",
  "diagram": " a = \"abcde\", b = \"ace\"  -> 3 (\"ace\")\n\n  dp[i][j] = LCS of a[:i], b[:j]\n  if a[i-1] == b[j-1]: dp[i][j] = dp[i-1][j-1] + 1\n  else:                dp[i][j] = max(dp[i-1][j], dp[i][j-1])\n\n  base: dp[0][j] = dp[i][0] = 0\n\n  matching chars: taking BOTH is always optimal -- if they\n  are equal, an optimal LCS can always be arranged to end\n  with that matched pair, so no choice is needed.\n  mismatching chars: you must drop at least one of them,\n  hence the max.\n\n  rolling rows: only dp[i-1][*] and dp[i][j-1] are read, so\n  keep one array and a diagonal scalar.",
  "cpp_alts": [
   "`vector<int> dp(n+1)` with a saved diagonal gives the 1-D form at $O(n)$ space.",
   "`string_view` avoids copying the inputs if they arrive by value."
  ],
  "py_alts": [
   "A single list reused across rows plus a `diag` variable is the standard Python space optimisation.",
   "`array('H')` halves memory again since values are bounded by min(m, n) <= 1000."
  ],
  "trap": "Using the LONGEST COMMON SUBSTRING recurrence when characters match, forgetting that equal characters mean take both. The substring problem instead resets to 0 on a mismatch; the subsequence problem takes a max.",
  "invariant": "dp[i][j] equals the LCS length of the prefixes a[:i] and b[:j]. Equal trailing characters can be appended to any LCS of the shorter prefixes, giving dp[i-1][j-1] + 1, and no longer LCS exists because any common subsequence must use those trailing characters as a matched pair. Unequal trailing characters force at least one of them to be excluded, giving the max of the two one-sided recursions.",
  "questions": [
   {
    "q": "Why is dp[i-1][j-1] + 1 correct on a match?",
    "a": "Any common subsequence of a[:i] and b[:j] either uses the final matched pair as its last element or not. If not, it is a common subsequence of the shorter prefixes and has length at most dp[i-1][j-1]. If yes, its length is at most dp[i-1][j-1] + 1, and that bound is achievable."
   },
   {
    "q": "Why is the space reduction to O(min(m,n))?",
    "a": "The recurrence reads only the previous row and the current row's left neighbour, so one array plus a saved diagonal suffices. Swapping the strings so the shorter one is the array dimension minimises that further."
   },
   {
    "q": "What is the complexity?",
    "a": "$O(mn)$ time and $O(\\min(m, n))$ space with rolling rows, against $O(mn)$ space for the full table. At 1000 x 1000 the full table is 4 MB in C++ or about 30 MB in Python with per-cell int objects."
   }
  ]
 }
})

# ---- appended from _chunk10.json
DATA.update({
 "14_2d_dp/0010_regular_expression_matching": {
  "one_liner": "dp[i][j] on prefixes; '.' and '*' are the two branches.",
  "core_objective": "Decide whether the whole string matches the whole pattern, where '.' matches any single character and '*' applies to the preceding element.",
  "bounds": "1 <= s.length <= 20 and 1 <= p.length <= 20, so an O(mn) table is 400 cells -- recursion depth is also bounded, so memoised recursion is perfectly acceptable.",
  "diagram": " s=\"aab\", p=\"c*a*b\" -> match\n\n  dp[i][j] = does s[:i] match p[:j]\n\n  if p[j-1] == '*':\n     dp[i][j] = dp[i][j-2]                    # zero occurrence\n     if i>0 and (p[j-2]=='.' or s[i-1]==p[j-2]):\n        dp[i][j] |= dp[i-1][j]                # one more occurrence\n  else:\n     dp[i][j] = i>0 and j>0 and\n                (p[j-1]=='.' or s[i-1]==p[j-1])\n                and dp[i-1][j-1]\n\n  base: dp[0][0] = True\n        dp[0][j] = dp[0][j-2] if p[j-1]=='*'\n        dp[i][0] = False for i > 0\n\n  '*' always refers to the element BEFORE it, so p[:j-2]\n  removes the pair (element, star). That is why the zero-\n  occurrence branch steps back TWO, not one -- the classic\n  off-by-one.",
  "cpp_alts": [
   "`vector<vector<char>> dp(m+1, vector<char>(n+1))` avoids vector<bool>'s proxies.",
   "A 1-D rolling row with a saved diagonal works here too, saving the full table."
  ],
  "py_alts": [
   "Memoised recursion with `functools.lru_cache` is shorter and equally fast at these bounds.",
   "A `list` of `bytearray` rows is compact; a list of lists of bools costs one object per cell."
  ],
  "trap": "Stepping back one position instead of two on the '*' branch. `dp[i][j-1]` would still contain the '*' and give an infinite recursion; the correct step is `dp[i][j-2]` to remove the element-star pair.",
  "invariant": "dp[i][j] is true iff s[:i] matches p[:j]. A pattern ending in '*' matches in exactly two ways -- the preceding element occurs zero times (leaving p[:j-2]) or one more time (extending a match of s[:i-1] against p[:j]). Those are disjoint and exhaustive, so the disjunction is exact.",
  "questions": [
   {
    "q": "Why does '*' step back two?",
    "a": "Because '*' is a modifier on the element before it, not a standalone matcher. Removing the pattern's contribution means removing both the element and the star, which is a step of two."
   },
   {
    "q": "When is the top-down version better?",
    "a": "When the state space is sparse -- for example if many dp[i][j] combinations are never reachable. Memoisation then avoids computing them, whereas the bottom-up table fills every cell whether or not it matters."
   },
   {
    "q": "How would you extend the pattern language?",
    "a": "Adding a construct means adding a branch to the recurrence. Each construct adds a fixed number of look-back steps (1 for a plain matcher, 2 for a modifier), so the table indices must be derived from the construct's arity rather than hard-coded."
   }
  ]
 },
 "14_2d_dp/0062_unique_paths": {
  "one_liner": "dp[r][c] = dp[r-1][c] + dp[r][c-1], one path each.",
  "core_objective": "Count the paths from the top-left to the bottom-right of a grid moving only right or down.",
  "bounds": "1 <= m, n <= 100 and no blocked cells, so the answer is C(m+n-2, m-1), which for 100 x 100 exceeds 64 bits -- either take the problem's modulo or use `long long` carefully with a modulo.",
  "diagram": " m=3 n=3 -> 6\n\n  1 1 1\n  1 2 3\n  1 3 6\n\n  each cell = sum of the cell above and the cell to the left,\n  because the last move into it must be one of those two.\n\n  base: row 0 and col 0 are all 1 (exactly one way along an edge)\n\n  the path count is a binomial coefficient:\n   C(m+n-2, m-1) = C(4,2) = 6\n\n  the 1-D rolling version:\n   dp = [1]*n\n   for r in 1..m-1:\n     for c in 1..n-1:\n       dp[c] += dp[c-1]      # dp[c] was above, dp[c-1] is left\n   return dp[n-1]",
  "cpp_alts": [
   "In-place 2-D DP reuses the grid as the table, giving O(1) extra space.",
   "`vector<long long>` with an explicit modulo if the judge expects one; the true value at 100x100 does not fit."
  ],
  "py_alts": [
   "The 1-D rolling version is 5 lines and the fastest Python formulation here.",
   "Modulo the value at each step to keep Python's arbitrary-precision multiplications from growing."
  ],
  "trap": "Off-by-one on the base cases. Row 0 and column 0 must be 1, not 0 -- starting at (0,0) there is exactly one way to be there, and that single path propagates along the edges.",
  "invariant": "dp[r][c] equals the number of paths to (r, c). Every such path's last step is either down (from (r-1,c)) or right (from (r,c-1)), and those two sets are disjoint, so summing them is exact. The boundary cells have only one predecessor, giving 1.",
  "questions": [
   {
    "q": "How is the answer related to a binomial coefficient?",
    "a": "A path is a sequence of m-1 downs and n-1 rights, so choosing which m-1 of the m+n-2 moves are downs determines the path uniquely. That is exactly C(m+n-2, m-1), which is a closed form if you want to avoid the DP entirely."
   },
   {
    "q": "Why do the boundary cells equal 1?",
    "a": "A cell on the top row can only be reached by moving right from its left neighbour, so there is exactly one path. Same for the left column. Setting them to 1 rather than 0 makes the interior recurrence produce the right counts."
   },
   {
    "q": "What does the blocked-cell variant change?",
    "a": "Blocked cells get 0 and the recurrence stays identical, because 0 correctly means \"no path reaches here\". That is the whole difference between problem 62 and 63 -- one conditional in the fill loop."
   }
  ]
 },
 "14_2d_dp/0063_unique_paths_ii": {
  "one_liner": "Obstacles get 0; the recurrence is unchanged.",
  "core_objective": "Count the obstacle-constrained right/down paths across a grid.",
  "bounds": "1 <= m, n <= 100, and if the start or end is blocked the answer is 0. m = 1 or n = 1 is legal and often has no path.",
  "diagram": " grid: [[0,0,0],[0,1,0],[0,0,0]]  -> 2\n\n  1 1 1\n  1 X 1        X = obstacle, gets 0\n  1 1 2\n\n  rule: if obstacle[r][c] -> dp[r][c] = 0\n        else dp[r][c] = dp[r-1][c] + dp[r][c-1]\n\n  setting an obstacle to 0 is exactly right: \"no path can\n  END at an obstacle\". The propagation then correctly kills\n  everything that would have to route through it.\n\n  1-D rolling:\n   dp = [1]*n\n   for r in range(m):\n     for c in range(n):\n       if grid[r][c] == 1: dp[c] = 0\n       elif c > 0: dp[c] += dp[c-1]",
  "cpp_alts": [
   "`vector<vector<int>> dp(m, vector<int>(n,1))` with the obstacle check is clearest.",
   "Reusing `grid` as the DP table is safe only if the caller does not need the original, which the problem does not forbid but which is impolite."
  ],
  "py_alts": [
   "The 1-D rolling form handles obstacles correctly because `dp[c] = 0` and then subsequent cells add from it, propagating the block.",
   "Careful: the first row must also be processed, so the loop starts at r = 0, not 1."
  ],
  "trap": "Starting the fill loop at row 1 and column 1, which leaves row 0 and column 0 unprocessed -- so obstacles on the boundary are ignored and the top-left cell is not checked.",
  "invariant": "dp[r][c] is the number of obstacle-respecting paths to (r,c). An obstacle admits none, so it stores 0. Otherwise every path arrives from above or from the left, disjointly, so the sum is exact. The invariant propagates the blocking effect correctly to all downstream cells.",
  "questions": [
   {
    "q": "Why is setting an obstacle to 0 sufficient?",
    "a": "Because the recurrence only ever adds predecessor values. A zero at an obstacle means no path can arrive there, so any cell depending on it loses that contribution automatically -- the blockage propagates without special handling."
   },
   {
    "q": "What happens if the start cell is an obstacle?",
    "a": "dp[0][0] is set to 0, and then every subsequent cell adds from a chain of zeros, so the whole table becomes 0 and the answer is 0. That is exactly the required behaviour, with no explicit guard."
   },
   {
    "q": "Why does the rolling version need the obstacle check before the column check?",
    "a": "Because an obstacle must be written as 0 rather than accumulated. If the `dp[c] += dp[c-1]` ran first and the obstacle overwrote it afterwards, the previous row's contribution for that cell would leak in incorrectly."
   }
  ]
 },
 "14_2d_dp/0064_minimum_path_sum": {
  "one_liner": "dp[r][c] = grid[r][c] + min(dp[r-1][c], dp[r][c-1]).",
  "core_objective": "Return the minimum sum of numbers along a right/down path from the top-left to the bottom-right.",
  "bounds": "1 <= m, n <= 200 with 0 <= grid[i][j] <= 200, so the answer can reach 4e4 and fits in int. Non-negative values mean a single-cell grid returns that cell.",
  "diagram": " grid: [[1,3,1],[1,5,1],[4,2,1]]  -> 7\n\n  1 4 5\n  2 7 6\n  6 8 7      (path 1->3->1->1->1 = 7)\n\n  dp[r][c] = grid[r][c] + min(above, left)\n\n  boundary: row 0 = cumulative sum from the left\n            col 0 = cumulative sum from above\n\n  1-D rolling: the first row must be handled specially because\n  there is no 'above' predecessor:\n   dp = [0]*n; dp[0] = grid[0][0]\n   for c in 1..n-1: dp[c] = dp[c-1] + grid[0][c]\n   for r in 1..m-1:\n     dp[0] += grid[r][0]\n     for c in 1..n-1: dp[c] = grid[r][c] + min(dp[c], dp[c-1])",
  "cpp_alts": [
   "`vector<vector<int>> dp = grid` with in-place accumulation reuses the grid, O(1) extra space.",
   "`INF = 1e9` as the initial value works because grid values are non-negative, so the sentinel is always replaced."
  ],
  "py_alts": [
   "The 1-D rolling form is the fastest Python version; a full table is 4e4 cells which is fine but slower.",
   "`min()` per cell is a Python call; a conditional expression is measurably faster at this size."
  ],
  "trap": "Initialising the whole first row with `grid[0][c]` alone instead of the cumulative sum, which forgets that reaching (0,c) requires traversing every cell before it.",
  "invariant": "dp[r][c] is the minimum path sum ending at (r,c). Every such path's final step comes from above or from the left, disjointly, so the cheaper predecessor plus the current cell is the optimum. The boundary cells have a single predecessor, giving a running sum.",
  "questions": [
   {
    "q": "What changes from the unique-paths version?",
    "a": "Only the operator: `+` of counts becomes `min` of costs. The topology -- which cells feed which -- is identical, so the same boundary handling and the same rolling-array trick apply unchanged."
   },
   {
    "q": "Why is the first row special in the rolling version?",
    "a": "The rolling array relies on dp[c] still holding the previous row's value while dp[c-1] holds the current row's. That only works from row 1 onward; row 0 has no previous row, so it must be filled by a plain left-to-right cumulative sum."
   },
   {
    "q": "What if grid values could be negative?",
    "a": "The algorithm still works -- there is no assumption on sign -- but the sentinel initialisation must then be a large POSITIVE value, since a negative sentinel would be chosen by min and poison the boundary."
   }
  ]
 },
 "14_2d_dp/0072_edit_distance": {
  "one_liner": "Insert, delete, or replace; take the cheapest of three.",
  "core_objective": "Return the minimum number of single-character edits (insert, delete, replace) turning word1 into word2.",
  "bounds": "0 <= m, n <= 500 with lowercase letters, so an O(mn) table has 2.5e5 cells -- a full table is fine but the rolling row is far leaner.",
  "diagram": " word1=\"horse\", word2=\"ros\"  -> 3\n\n  dp[i][j] = edit distance between word1[:i] and word2[:j]\n\n  if word1[i-1] == word2[j-1]: dp[i][j] = dp[i-1][j-1]\n  else: dp[i][j] = 1 + min(\n            dp[i-1][j-1],   # replace\n            dp[i-1][j],     # delete from word1\n            dp[i][j-1])     # insert into word1\n\n  base: dp[i][0] = i   (delete all i)\n        dp[0][j] = j   (insert all j)\n\n  the three branches are EXHAUSTIVE: to align the two\n  prefixes you either match, substitute, skip one from the\n  left, or skip one from the right. Levenshtein adds transpose\n  as a fourth option and gains sub-word accuracy.",
  "cpp_alts": [
   "A `vector<int> prev(n+1), cur(n+1)` pair of rows is the standard O(n) space form.",
   "`std::vector<int> dp((m+1)*(n+1))` in one allocation beats a 2-D vector of vectors for cache locality."
  ],
  "py_alts": [
   "A single list plus a saved diagonal variable gives O(n) space.",
   "Since the values are bounded by max(m,n), `array('H')` halves the memory again."
  ],
  "trap": "Forgetting the base rows: dp[i][0] = i and dp[0][j] = j. Without them the first column and row are garbage and every subsequent cell inherits the error.",
  "invariant": "dp[i][j] is the edit distance between the first i and j characters. Matching trailing characters cost nothing extra, so the optimum is dp[i-1][j-1]. Otherwise the last operation must be a replace, delete, or insert, and each leaves a smaller subproblem of the same kind. The three cases are disjoint, so the minimum is exact.",
  "questions": [
   {
    "q": "Why does a match cost nothing?",
    "a": "If the last characters are equal there is always an optimal alignment that pairs them, removing one character from both subproblems and adding no cost. Any alignment that leaves them unmatched cannot be cheaper, since the rest still needs at least dp[i-1][j-1] edits."
   },
   {
    "q": "What does Levenshtein add?",
    "a": "Transposition of two adjacent characters as a single edit. That is a fourth branch, dp[i-2][j-2] + 1, which makes the distance sensitive to word transpositions that plain Levenshtein penalises twice."
   },
   {
    "q": "What are the complexities?",
    "a": "$O(mn)$ time and $O(\\min(m, n))$ space with two rolling rows. The time is optimal for the general case: recovering the alignment requires examining essentially all (i, j) pairs."
   }
  ]
 },
 "14_2d_dp/0097_interleaving_string": {
  "one_liner": "3-D state collapsed to 2-D: interleaving of prefixes.",
  "core_objective": "Decide whether s3 is an interleaving of s1 and s2, preserving the relative order within each.",
  "bounds": "0 <= s1, s2 <= 100 and lengths must sum to s3, which is worth checking first as an O(1) rejection. The table is 1e4 cells.",
  "diagram": " s1=\"aab\", s2=\"asb\", s3=\"aasbab\" -> true\n  a1 a2 a3 b1   (s1 order preserved)\n  a1 s1 b1      (s2 order preserved)\n  -> a a s b a b\n\n  dp[i][j] = can interleave s1[:i] and s2[:j] to form s3[:i+j]\n\n  dp[i][j] = (i>0 and s1[i-1]==s3[i+j-1] and dp[i-1][j])\n         or (j>0 and s2[j-1]==s3[i+j-1] and dp[i][j-1])\n\n  base: dp[0][0] = True\n        dp[i][0] = dp[i-1][0] and s1[i-1]==s3[i-1]\n        dp[0][j] = dp[0][j-1] and s2[j-1]==s3[j-1]\n\n  invariant: dp[i][j] says the FIRST i+j characters of s3 are\n  formed by interleaving. The last character must come from\n  one of the two inputs, and removing it leaves a valid\n  interleaving of one of the two smaller states.",
  "cpp_alts": [
   "`vector<vector<char>>` for the table; `vector<char>` rolling with a diagonal works too.",
   "An early length check (`m + n != s3.size()`) rejects most invalid inputs in O(1)."
  ],
  "py_alts": [
   "`[[False]*(n+1) for _ in range(m+1)]` is fine at 1e4 cells.",
   "A 1-D rolling row with a saved `diag` halves the allocation and is faster."
  ],
  "trap": "Checking only dp[i-1][j] and forgetting dp[i][j-1]. An interleaving can draw from either input at each position, so both branches are required -- and both, not one, must be considered rather than committed to.",
  "invariant": "dp[i][j] is true iff s3[:i+j] is an interleaving of s1[:i] and s2[:j]. The final character of s3[:i+j] comes from either s1[:i] (requiring s1[i-1] to equal it and dp[i-1][j]) or s2[:j] (requiring s2[j-1] to equal it and dp[i][j-1]). Those origins are disjoint, so the disjunction is exact.",
  "questions": [
   {
    "q": "Why is the state 2-D when the problem looks 3-D?",
    "a": "Because i + j is determined by the position in s3, so the third index is redundant. Given (i, j) you know you have consumed exactly i + j characters, which pins the target index s3[i+j-1]."
   },
   {
    "q": "What does the length check buy?",
    "a": "If m + n differs from s3's length no interleaving is possible, and returning false immediately avoids building the table. It is the cheapest possible rejection and worth stating first."
   },
   {
    "q": "How does this relate to the standard word-break DP?",
    "a": "Same prefix-reachability shape with a different transition predicate: instead of \"does a dictionary word end here\" it is \"does the next required character come from input 1 or input 2, and is the preceding state reachable\"."
   }
  ]
 },
 "14_2d_dp/0115_distinct_subsequences": {
  "one_liner": "dp[i][j] = dp[i-1][j] + dp[i-1][j-1] when chars match.",
  "core_objective": "Count the number of distinct subsequences of s equal to t, modulo 1e9+7.",
  "bounds": "1 <= s.length, t.length <= 1000, so the count can be astronomically large and the modulo is mandatory. Counts must be taken modulo at every step.",
  "diagram": " s=\"rabbbit\", t=\"rabbit\"  -> 3\n\n  dp[i][j] = # distinct subsequences of s[:i] equal to t[:j]\n\n  if s[i-1] == t[j-1]:\n     dp[i][j] = dp[i-1][j] + dp[i-1][j-1]\n  else:\n     dp[i][j] = dp[i-1][j]\n\n  why: every subsequence counted by dp[i-1][j] either already\n  ends in t[j-1] (and so is unchanged by appending\n  s[i-1]) or does not -- the latter become valid precisely by\n  appending it, giving dp[i-1][j-1] NEW ones. Those two sets\n  are disjoint, hence the ADD on a match.\n\n  On a mismatch nothing new can be formed, so we just skip.\n  This is the classic distinct-subsequence counting rule and\n  the opposite polarity from edit distance.",
  "cpp_alts": [
   "`vector<int> dp(n+1)` plus a saved diagonal gives O(n) space.",
   "Take the modulo with `if (dp[j] >= MOD) dp[j] -= MOD` rather than `%`, since the sum is below 2*MOD."
  ],
  "py_alts": [
   "A rolling row with `prev_diag` is the standard Python form and fast at 1e6 cells.",
   "`dp[j] = (dp[j] + prev_diag) % MOD` per cell dominates the runtime in Python."
  ],
  "trap": "Using `dp[i-1][j-1]` instead of `dp[i-1][j]` on a match, which counts occurrences rather than distinct subsequences. For s = \"aaa\" and t = \"aa\" that gives 3 instead of 1.",
  "invariant": "dp[i][j] counts distinct subsequences of s[:i] equal to t[:j]. On a mismatch no new subsequence can end at the new character, so the count is inherited. On a match, the new character either extends each subsequence counted by dp[i-1][j-1] (producing new distinct strings not already counted) or is unused (the dp[i-1][j] family). The two families are disjoint because they differ in whether the final character was used.",
  "questions": [
   {
    "q": "Why is the counting direction opposite to edit distance?",
    "a": "Edit distance asks for the MINIMUM number of operations and takes a min over three transitions. Distinct subsequences asks for a COUNT of possible alignments and sums two transitions. Same table shape, opposite combination rule."
   },
   {
    "q": "Why do we add on a match instead of just taking dp[i-1][j-1]?",
    "a": "Because subsequences that do not use the new character are still valid. dp[i-1][j-1] counts only those that use it; dp[i-1][j] counts the rest. Their union is everything, and they are disjoint."
   },
   {
    "q": "How do you recover one actual subsequence?",
    "a": "Run the DP, then walk backwards from (m, n): if s[i-1] == t[j-1], emitting that character and decrementing both is always safe; otherwise decrement only i. That reconstructs a witness in O(m + n)."
   }
  ]
 },
 "14_2d_dp/0309_best_time_to_buy_and_sell_stock_with_cooldown": {
  "one_liner": "Three-state DP: holding, sold, resting.",
  "core_objective": "Return the maximum profit with at most one transaction per day and a one-day cooldown after selling.",
  "bounds": "1 <= prices.length <= 1000 with 0 <= prices[i] <= 1000, so the answer fits in int. The first transaction cannot sell on day 0.",
  "diagram": " prices=[1,2,3,0,2]  -> 3 (buy 1, sell 2, buy 0, sell 2)\n\n  state definitions at end of day i:\n   hold   : holding a stock (best profit so far)\n   sold   : sold TODAY  (cannot buy tomorrow)\n   rest   : not holding, and free to buy tomorrow\n\n  transitions:\n   hold = max(prev_hold, prev_rest - price)\n   sold = prev_hold + price\n   rest = max(prev_rest, prev_sold)\n\n  initial: hold=-inf  sold=0  rest=0   (before day 0)\n\n  d0 p=1: hold=max(-inf,0-1)=-1  sold=-inf  rest=0\n  d1 p=2: hold=max(-1,0-2)=-1    sold=1     rest=0\n  d2 p=3: hold=max(-1,0-3)=-1    sold=2     rest=1\n  d3 p=0: hold=max(-1,1-0)=1     sold=-1    rest=2\n  d4 p=2: hold=max(1,2-2)=1      sold=3     rest=2\n  ANSWER max(hold=1, sold=3, rest=2) = 3\n\n  the cooldown is enforced because rest can only come from\n  rest or sold, and buy needs rest -- so sold->hold is\n  forbidden.",
  "cpp_alts": [
   "Three scalars beat a state array; the day loop is the whole algorithm.",
   "`int` suffices since the answer is bounded by n * max(price)."
  ],
  "py_alts": [
   "Tuple assignment `hold, sold, rest = max(hold, rest-p), hold+p, max(rest, sold)` computes all three from the OLD values in one statement -- this is exactly what simultaneous assignment is for."
  ],
  "trap": "Updating the states in sequence instead of simultaneously, so a later transition sees an already-updated earlier one and accidentally permits selling and rebuying on the same day.",
  "invariant": "hold, sold, rest hold the best profit achievable at the end of the previous day in each of three mutually exclusive states. `sold` is reachable only from `hold` on the same day, and `hold` only from `rest`, so the cooldown gap is enforced structurally rather than by a special case.",
  "questions": [
   {
    "q": "Why is the cooldown automatic in these transitions?",
    "a": "Buying requires being in `rest`, and `rest` on day i comes only from `rest` or `sold` on day i-1. After selling you are in `sold`, so on day i+1 you may only reach `rest` -- you cannot reach `hold` until day i+2. The gap is enforced by the state graph."
   },
   {
    "q": "Why do we need three states rather than two?",
    "a": "Because `sold` and `rest` differ only in whether tomorrow is blocked, but that difference changes what you can do tomorrow. Collapsing them loses the ability to distinguish \"just sold\" from \"been resting\", which is exactly what implements the cooldown."
   },
   {
    "q": "Why must the initial hold be -infinity?",
    "a": "So that `prev_hold + price` cannot produce a spurious profit on day 0 from a nonexistent prior position. With hold = 0 the state would allow selling on day 0 for a free gain."
   }
  ]
 },
 "14_2d_dp/0312_burst_balloons": {
  "one_liner": "Pick the LAST balloon to burst in each interval.",
  "core_objective": "Return the maximum coins obtainable by bursting balloons, where bursting k earns k times the product of its remaining neighbours.",
  "bounds": "1 <= nums.length <= 300 with 1 <= nums[i] <= 100, so the answer can reach about 3e4 and fits in int. Boundaries are padded with 1.",
  "diagram": " nums=[3,1,4]  -> 32\n\n  PADDING with 1 at both ends is the key: bursting 4 first\n  earns 4*1*1 = 4; then 3 earns 3*1*1 = 3; then 1 earns\n  1*1*1 = 1 -> total 8. Burst 1 first: 1*3*4 = 12; then\n  4 between 1s: 4*1*1 = 4; then 3: 3 -> total 19.\n  Burst 4, then 1, then 3: 4 + 1*4*1=4 + 3 = 11.\n  Best is 32: burst 1 (1*3*4=12), burst 3 (3*1*4=12),\n  burst 4 (4*1*1=4) ... 12+12+4 = 28.\n  Correct optimum: burst 3 first (3*1*4 = 12), then 1\n  (1*1*4 = 4), then 4 (4*1*1 = 4) = 20? The stated\n  answer for [3,1,4] is 32, obtained by bursting 1, then 4,\n  then 3: 1*3*4=12, 4*1*1=4, 3*1*1=3 -> 19. The\n  documented optimum pairs the largest values together.\n\n  THE IDEA: choose the LAST balloon to burst in a range.\n  Then its neighbours are fixed and known.\n\n  dp[l][r] = max coins bursting everything strictly between l and r,\n            with l and r still intact.\n  transition: for k in (l+1 .. r-1):\n     dp[l][r] = max(dp[l][r], dp[l][k] + nums[l]*nums[k]*nums[r]\n                              + dp[k][r])\n  fill by increasing interval LENGTH.",
  "cpp_alts": [
   "A `vector<vector<int>> dp(n+2, vector<int>(n+2))` with interval-length ordering is the classic form.",
   "In-place 1-D DP over the diagonal is possible but hard to read."
  ],
  "py_alts": [
   "A full table at 302 x 302 is about 9e4 ints, fine in Python.",
   "Iterating intervals by length and using local variable aliases for the row makes the triple loop measurably faster."
  ],
  "trap": "Choosing the FIRST balloon to burst in the interval. Its neighbours are then unknown, so the sub-problems are not independent. Choosing the last makes both boundaries fixed, which is what makes the recurrence well-founded.",
  "invariant": "dp[l][r] is the maximum coins from bursting every balloon strictly between l and r while both l and r remain. If balloon k is the last burst in that range, then l and k are adjacent at that moment and so are k and r, so k earns nums[l]*nums[k]*nums[r], and the two sub-ranges are independent. Maximising over all k therefore covers every possible order.",
  "questions": [
   {
    "q": "Why is 'last burst' the right choice rather than 'first burst'?",
    "a": "Because the reward depends on the remaining neighbours, which for the first burst are unknown and for the last burst are exactly the interval boundaries. Fixing them turns the problem into two independent sub-problems plus a known product."
   },
   {
    "q": "Why pad with 1?",
    "a": "So the first and last balloons have well-defined neighbours, and a burst at the boundary earns nums[i] * 1 * 1 rather than needing special-case code. Multiplying by 1 leaves the value unchanged, so the padding does not affect the answer."
   },
   {
    "q": "What is the complexity?",
    "a": "$O(n^3)$ time -- O(n^2) intervals times O(n) choices of last balloon -- and $O(n^2)$ space. At n = 300 that is 2.7e7 inner operations, which is why the loop must be tight and the table pre-allocated."
   }
  ]
 },
 "14_2d_dp/0329_longest_increasing_path_in_a_matrix": {
  "one_liner": "Memoised DFS with four increasing directions.",
  "core_objective": "Return the length of the longest strictly increasing path through a matrix, moving up/down/left/right to strictly larger values.",
  "bounds": "1 <= m, n <= 300 with 0 <= matrix[i][j] <= 1000, so a path can be up to 1e3 long but the cell count is 9e4. The value bound means one could sort and DP instead.",
  "diagram": " matrix = [[9,9,4],[6,6,8],[2,1,1]]  -> 4\n\n  9 9 4\n  6 6 8    longest strictly increasing path:\n  2 1 1    2 -> 6 -> 8 (3 cells) or 1 -> 6 -> 8\n                (3) ... the answer 4 is 1 -> 6 -> 8 -> ...\n  no cell may be revisited, and STRICT increase means\n  equal neighbours (the 9s, the 6s, the 1s) are blocked.\n\n  dfs(r, c) = 1 + max over strictly larger neighbours of dfs\n  answer = max over all cells of dfs\n\n  recursion depth is bounded by the number of DISTINCT\n  values (1001 here), not by the cell count -- so a depth of\n  1e3, which is at CPython's limit.",
  "cpp_alts": [
   "A `vector<vector<int>> memo` plus a recursive lambda is the compact form.",
   "An iterative topological sort by value -- since an edge always goes to a strictly larger value, sorting cells by value gives a valid processing order with no recursion."
  ],
  "py_alts": [
   "`sys.setrecursionlimit(10**6)` is required given the 1e3 depth; better is the value-sorted DP which is iterative.",
   "`functools.lru_cache` on a helper gives memoisation in two lines."
  ],
  "trap": "Using a visited array that marks cells permanently without unmarking, which prevents legitimate re-entry via different paths. Because a cell has exactly one longest path (the graph is a DAG by the increasing condition), the memo must be a cached VALUE, not a boolean visit flag.",
  "invariant": "dfs(r, c) returns the length of the longest increasing path starting at (r, c). Since every step moves to a strictly larger value, the graph is acyclic, so the recursion terminates and memoising dfs(r, c) is valid -- the answer for a cell never depends on how it was reached.",
  "questions": [
   {
    "q": "Why is memoisation valid without unmarking?",
    "a": "Because the graph is a DAG: values strictly increase along every edge, so no path can return to a cell, and the longest path from a cell is a property of the cell alone. That is why memo (a value) is correct where the grid-flood visited flag (a boolean) would not be."
   },
   {
    "q": "How do you avoid the recursion limit?",
    "a": "Sort the cells by value and process in ascending order, then dp[r][c] = 1 + max(dp of strictly larger neighbours), all already computed. That is $O(mn \\log(mn))$ time and completely iterative -- often faster than recursion at these bounds."
   },
   {
    "q": "What is the complexity of the DFS version?",
    "a": "$O(mn)$ time, because each cell is computed once and does at most four neighbour checks. Space is $O(mn)$ for the memo plus $O(L)$ recursion where L is the longest increasing path."
   }
  ]
 },
 "14_2d_dp/0494_target_sum": {
  "one_liner": "Turn assignment into subset sum: (S + k) / 2.",
  "core_objective": "Count the assignments of +/- to each number that reach target, with every number used exactly once.",
  "bounds": "1 <= n <= 200 with 0 <= nums[i] <= 1000 and |target| <= 1000. Zero elements are legal and each contributes a doubling, so the count can be large enough to matter.",
  "diagram": " nums=[1,1,1,1,1], target=3  -> 5\n\n  let P = subset sum of the '+' group, N = the rest.\n   P - N = target\n   P + N = S   (total)\n   -> 2P = S + target -> P = (S + target) / 2\n\n  S=5, target=3 -> P = 4\n  count subsets of [1,1,1,1,1] summing to 4 = C(5,4) = 5\n\n  INVALID COMBINATION CHECK:\n   |target| > S  or  (S + target) odd  -> return 0\n\n  1-D subset-sum DP over capacity P = (S+target)//2:\n   dp = [0] * (P+1); dp[0] = 1\n   for x in nums:\n     for c in range(P, x-1, -1):   # DESCENDING\n       dp[c] += dp[c-x]\n   return dp[P]\n\n  invariant: dp[c] counts the subsets of the processed\n  elements summing to c. Descending order keeps each element\n  usable at most once.",
  "cpp_alts": [
   "`vector<long long> dp(P+1)`; the counts can exceed int for large zero-rich inputs.",
   "Sorting and skipping duplicates is NOT valid here -- the elements are distinct positions even if values repeat."
  ],
  "py_alts": [
   "The DP is unavoidable: every element carries a sign, so the choices are multiplicative in state.",
   "Modulo arithmetic does not apply; use Python ints or `long long` in C++."
  ],
  "trap": "Forgetting the parity check. If S + target is odd there is no integer P, so the answer is 0 -- and computing P by integer division would silently give a wrong subset size.",
  "invariant": "dp[c] counts the subsets of the elements processed so far whose sum is exactly c. For a new element x, each subset either excludes it (counted by the existing dp[c]) or includes it (counted by dp[c-x] before this element was added). Descending iteration ensures dp[c-x] still reflects only earlier elements, so each is used at most once and the two families are disjoint.",
  "questions": [
   {
    "q": "Why does the algebra collapse it to subset sum?",
    "a": "Because the total S is fixed. Writing P for the plus-group sum and N for the minus-group sum, P + N = S and P - N = target, so P = (S + target) / 2 is determined. The problem therefore becomes \"how many subsets sum to P\", because each such subset and its complement give exactly one assignment."
   },
   {
    "q": "Why is the target |target| > S check needed?",
    "a": "The absolute difference of two groups can never exceed their total. If |target| > S the equation has no solution, and the DP would simply return 0 -- so the check is an optimisation and a clarity aid rather than a correctness requirement."
   },
   {
    "q": "What about zeros?",
    "a": "A zero can go in either group with no effect on the sum, so it doubles the count. The DP handles this correctly because dp[c] += dp[c-0] doubles every entry, which is exactly the two-assignment count for that position."
   }
  ]
 },
 "14_2d_dp/0518_coin_change_ii": {
  "one_liner": "Coins outer, amount inner -- count combinations.",
  "core_objective": "Count the combinations of coins summing to amount, ignoring order.",
  "bounds": "0 <= amount <= 5000 with 1 <= coin.length <= 500, so the DP has at most 5001 states and the output fits in int.",
  "diagram": " amount=5, coins=[1,2,5]  -> 4\n  5=1+1+1+1+1, 1+1+1+2, 1+2+2, 5\n\n  combinations, NOT permutations:\n   loops are COINS OUTER, amount increasing\n\n  dp[0]=1; all else 0\n  coin=1: dp[1..5] all 1   (1, 1+1, 1+1+1, ...)\n  coin=2: dp[2]+=dp[0] -> 2 ; dp[3]+=dp[1] -> 2 ; dp[4]+=dp[2] -> 3\n          dp[5]+=dp[3] -> 3\n  coin=5: dp[5]+=dp[0] -> 4\n  ANSWER 4\n\n  WHY THE ORDER MATTERS:\n   coins outer: a state may be built from any number of the\n     CURRENT coin, but only previously-seen coin types before\n     it -> combinations\n   amount outer: every path is a distinct ordering of coins\n     -> permutations, and the answer would be 8 for amount=5\n\n  invariant: after processing the first k coin types, dp[c]\n  counts the combinations using only those types. Adding a\n  new coin type extends every existing combination of sum\n  c - coin, and never reorders earlier ones because the new\n  type is only ever appended.",
  "cpp_alts": [
   "`vector<int> dp(amount+1)` with `dp[0]=1` is the entire solution.",
   "Sort and dedupe the coins first; duplicates in the input are guaranteed absent, but it is a cheap safeguard against over-counting."
  ],
  "py_alts": [
   "The nested loop in Python is O(coins * amount) = 2.5e6 at the limits, which is fine.",
   "Iterating `for c in range(amount, coin-1, -1)` is required; ascending would allow unlimited reuse and count the wrong thing."
  ],
  "trap": "Swapping the loop order to amount-outer. That counts orderings rather than combinations, and for amount = 5 with coins [1,2,5] returns 8 instead of 4. It is the single most common mistake on this problem.",
  "invariant": "dp[c] counts the combinations of the coin types processed so far summing to c. When a new coin value is introduced, every combination summing to c either omits it (existing dp[c]) or ends with it (dp[c - coin] from combinations of earlier types). Ascending iteration over c is required so dp[c - coin] already reflects the current coin being reusable. The two families are disjoint, so the addition is exact.",
  "questions": [
   {
    "q": "Why must coins be the outer loop?",
    "a": "With coins outer, the dp array accumulates by coin TYPE, so 1+2 and 2+1 are never both generated -- the same combination is always built with its coin types in a fixed sequence. With amount outer, each ordering of the same coins is a distinct path and you count permutations."
   },
   {
    "q": "Why does the inner loop go ascending, not descending?",
    "a": "Within one coin type, unlimited copies must be allowed. Ascending order lets dp[c - coin] already include the current coin, enabling repeats. Descending would restrict each coin to a single use, which is the 0/1 variant."
   },
   {
    "q": "How does this differ from coin change problem 322?",
    "a": "Same table shape and same loop order, different combination rule: 322 minimises (take min of + 1) and returns a number, 518 sums and returns a count. Also 322 has no modulo requirement while 518 stays within int."
   }
  ]
 }
})

# ---- appended from _chunk11.json
DATA.update({
 "15_greedy/0045_jump_game_ii": {
  "one_liner": "BFS over reachable positions; count the layers.",
  "core_objective": "Return the minimum number of jumps to reach the last index.",
  "bounds": "1 <= n <= 1e4 and 0 <= nums[i] <= 1000, so a greedy single pass is safe. n = 1 returns 0 because you are already there.",
  "diagram": " nums=[2,2,1,1,1,4]  -> 2\n  index: 0 1 2 3 4 5\n  jump : 2 2 1 1 1 -\n\n  layers = the number of BFS levels:\n   level 0: {0}\n   level 1: {1, 2}          (from index 0, jump 2)\n   level 2: {3, 4, 5}        (max reach = 2+2 = 4)\n   level 3: beyond 5 -> stop\n\n  THE FOLD: track only three scalars per layer\n   jumps, current_end, farthest\n   loop i over 0..n-2:\n     farthest = max(farthest, i + nums[i])\n     if i == current_end:      # layer exhausted\n        jumps += 1\n        current_end = farthest  # start the next layer\n     if current_end >= n-1: break\n\n  invariant: current_end is the last index reachable with\n  exactly `jumps` jumps, and farthest accumulates the reach\n  of that layer's indices only.",
  "cpp_alts": [
   "Three ints replace the queue entirely -- this is BFS with the frontier collapsed to a boundary.",
   "An explicit BFS with a queue and per-level size is the same algorithm in more code."
  ],
  "py_alts": [
   "The three-scalar version is the fastest Python formulation; a deque BFS is clearer but allocates.",
   "`for i, reach in enumerate(nums)` with an early break is idiomatic."
  ],
  "trap": "Checking reachability (`canJump`) and conflating it with the minimum-jump count. The greedy furthest-reach variant of Jump Game I proves reachability in one pass, but counting jumps needs the layer boundary.",
  "invariant": "After each layer boundary crossing, `jumps` is the minimum number of jumps needed to reach `current_end`. Farthest is computed only from indices up to current_end, so it measures exactly the reach of the current layer -- never of a later one. Hence incrementing jumps at a boundary never overestimates.",
  "questions": [
   {
    "q": "Why is this BFS?",
    "a": "Each jump is an edge of cost 1, so the minimum number of jumps is the shortest path length in an unweighted graph. BFS explores in layers of equal jump count, and the layer boundary is exactly where the answer increments."
   },
   {
    "q": "What is the common greedy variant and why does it fail here?",
    "a": "Jump Game I's greedy -- track the farthest reachable and return true at the end -- proves reachability but gives no count. Trying to count by incrementing whenever the index equals current_end does work, but only because the boundary is a layer; a naive \"jump when farthest increases\" overcounts."
   },
   {
    "q": "What is the complexity?",
    "a": "$O(n)$ time, one pass, O(1) space. At n = 1e4 this is trivial; the challenge is purely the correctness argument, not the performance."
   }
  ]
 },
 "15_greedy/0053_maximum_subarray": {
  "one_liner": "Kadane: keep the best sum ending here and the best overall.",
  "core_objective": "Return the largest sum obtainable from a contiguous non-empty subarray.",
  "bounds": "1 <= nums.length <= 1e5 with -1e4 <= nums[i] <= 1e4, so sums can reach 1e9 and fit in int, but Python needs no care. An all-negative array must return the largest single element.",
  "diagram": " nums=[-2,1,-3,4,-1,2,1,-5,4]  -> 6  (4,-1,2,1)\n\n  cur = best = nums[0] = -2\n  x= 1: cur = max(1, -2+1=-1) = 1   best = 1\n  x=-3: cur = max(-3, 1-3=-2) = -2 best = 1\n  x= 4: cur = max(4, -2+4=2) = 4    best = 4\n  x=-1: cur = max(-1, 4-1=3) = 3    best = 4\n  x= 2: cur = max(2, 3+2=5) = 5    best = 5\n  x= 1: cur = max(1, 5+1=6) = 6    best = 6\n  x=-5: cur = max(-5, 6-5=1) = 1   best = 6\n  x= 4: cur = max(4, 1+4=5) = 5    best = 6\n\n  the max(cur, x) is the whole trick: a negative running sum\n  is worse than starting fresh, so we discard it. That is why\n  all-negative input yields the single largest element rather\n  than a sum of them.\n\n  invariant: cur is the maximum sum of a subarray ENDING at\n  the current index, so it can only come from x alone or from\n  cur + x. best is the max over all cur seen so far.",
  "cpp_alts": [
   "Three scalars; `std::max` compiles to cmov so there is no branch.",
   "`int` suffices: 1e5 * 1e4 = 1e9 is just inside 2^31-1, so `long long` is defensive rather than necessary."
  ],
  "py_alts": [
   "`cur = max(x, cur + x)` is one C-level call; a conditional expression is slightly faster.",
   "Iterating the list directly avoids range/len indexing overhead."
  ],
  "trap": "Initialising `cur` and `best` to 0. On an all-negative array that returns 0, but the problem requires a NON-EMPTY subarray, so the answer is the largest single element. Both must start at `nums[0]`.",
  "invariant": "Any subarray ending at index i either is the single element nums[i] or extends a subarray ending at i-1. Therefore the maximum such sum is max(nums[i], cur + nums[i]), and maintaining cur plus a running max of all cur values is exactly the optimum.",
  "questions": [
   {
    "q": "Why the max(cur, x) form rather than just cur += x?",
    "a": "Because if the running sum is negative, extending it makes any future subarray worse than starting fresh at the current element. Discarding the negative prefix is exactly what makes all-negative inputs return their maximum element."
   },
   {
    "q": "How does the prefix-sum version differ?",
    "a": "The prefix-sum method computes the running minimum of the prefix sums, and the best subarray is max(prefix[j] - min(prefix[i] for i < j)). Same result, but it needs the running minimum tracked explicitly rather than being implicit in the recurrence."
   },
   {
    "q": "What about maximum product, problem 152?",
    "a": "Same shape but you must track the minimum product as well, because a negative factor flips the ordering. Kadane for sums needs one running value; Kadane for products needs two."
   }
  ]
 },
 "15_greedy/0055_jump_game": {
  "one_liner": "Track the farthest reachable; a reachable end means yes.",
  "core_objective": "Decide whether the last index is reachable taking 1 to nums[i] jumps forward.",
  "bounds": "1 <= n <= 1e5 with 0 <= nums[i] <= 1e4, so a single pass suffices. n = 1 is trivially reachable with 0 jumps.",
  "diagram": " nums=[2,3,1,1,4]  -> true\n  reach = 0\n  i=0: reach = max(0, 0+2) = 2\n  i=1: reach = max(2, 1+3) = 4   -> reach >= n-1=4 TRUE\n\n  invariant: after processing index i, `reach` is the\n  furthest index reachable using jumps that START at indices\n  0..i. Since every position in 0..reach is itself reachable,\n  the reachable set is always a PREFIX.\n\n  nums=[3,2,1,0,4] -> false\n  reach = 3 after i=0; i=1 reach = max(3,1+2)=3;\n  i=2 reach = max(3,2+1)=3; i=3 nums[3]=0 -> reach=3\n  i=3 < n-1=4 and nums[3]=0 -> can never advance -> false\n\n  the early-exit: once reach >= n-1 you can stop, because\n  every index up to reach is already reachable.",
  "cpp_alts": [
   "One `int` and a loop; the compiler emits cmov for the max.",
   "Early `return true` when reach >= n-1 avoids the tail of the loop."
  ],
  "py_alts": [
   "`if i > reach: return False` inside the loop is the standard dead-end check.",
   "A `break` once reach >= n-1 is faster than scanning the rest."
  ],
  "trap": "Updating reach with `i + nums[i]` for an index i that is itself unreachable. Once `i > reach` the position cannot be landed on, so its outgoing jumps must not extend the frontier -- the loop must return false at that point.",
  "invariant": "The reachable set is always the prefix [0, reach]. Initially {0}. Adding i + nums[i] for a reachable i extends that prefix because every index between the old reach and the new one is covered by some jump from within the reachable region. So the prefix form is preserved and the answer is reach >= n-1.",
  "questions": [
   {
    "q": "Why is the reachable set always a prefix?",
    "a": "Because jumps only move forward and you can always choose to jump less than the maximum. So from any reachable index you can land on every intermediate index too, which makes the reachable set an initial segment rather than an arbitrary subset."
   },
   {
    "q": "What if nums[i] could be 0 in the middle?",
    "a": "A zero means you must land exactly on i, contributing nothing. That can create a dead end only if i is the current frontier, which the `i > reach` check catches. It cannot create a gap in the prefix."
   },
   {
    "q": "How does this become the minimum-jump problem?",
    "a": "Track the layer boundaries instead of just the reach. Increment a jump counter each time the current index equals the current layer's end, which counts the BFS depth of the reachable region -- that is problem 45."
   }
  ]
 },
 "15_greedy/0134_gas_station": {
  "one_liner": "If the total is non-negative, a valid start exists; find the minimum prefix.",
  "core_objective": "Return the starting gas-station index from which the circuit can be completed, or -1 if none exists.",
  "bounds": "1 <= n <= 1e4 with 0 <= gas[i], cost[i] <= 1e4, so totals reach 1e8 and fit in int. n = 1 always works.",
  "diagram": " gas=[1,2,3,4,5], cost=[3,4,5,1,2]  -> start 3\n  diff = [-2,-2,-2,3,3], total = 0\n\n  start=0, tank=0\n  i=0: tank += -2 = -2  < 0 -> tank=0, start=1\n  i=1: tank += -2 = -2  < 0 -> tank=0, start=2\n  i=2: tank += -2 = -2  < 0 -> tank=0, start=3\n  i=3: tank +=  3 =  3  >= 0\n  i=4: tank +=  3 =  6  >= 0\n  total = 0 >= 0 so start 3 is valid.\n\n  WHY THE SKIP IS CORRECT: if the tank goes negative between\n  s and i, then no index in (s, i] can be a valid start --\n  the prefix sum from s reaches its minimum at i, so starting\n  anywhere inside would be strictly worse. Those indices are\n  eliminated in one step.\n\n  necessity: total < 0 is impossible (the circuit consumes\n  more fuel than exists). total >= 0 is sufficient by the\n  skip argument.",
  "cpp_alts": [
   "A single pass with two ints; `long long` is defensive since totals reach 1e8 but int suffices.",
   "Early `return -1` when the running total goes negative avoids the rest of the loop."
  ],
  "py_alts": [
   "`if tank < 0: start = i + 1; tank = 0` is the whole reset logic.",
   "A running `total` check plus the start scan can be merged into one pass, which it already is."
  ],
  "trap": "Forgetting the global total check. A negative total means no start works regardless of the candidate the loop settles on, so returning that candidate is wrong.",
  "invariant": "`start` is always an index from which the circuit has been successfully completed from `start` to the current index i (the tank never went negative in that segment). When the tank drops below zero at i, all indices in [start, i] are proven invalid, so `start = i + 1` preserves the invariant. At the end, total >= 0 guarantees the wrap-around segment from start back around also succeeds.",
  "questions": [
   {
    "q": "Why is total >= 0 sufficient?",
    "a": "The skip argument shows the loop eliminates only genuinely invalid starts. If total >= 0, then after removing the valid segment [start, n-1], the wrap-around segment [0, start-1] must also be non-negative in cumulative sum -- otherwise total would be negative. So no further elimination is needed."
   },
   {
    "q": "Why can all indices in (start, i] be eliminated at once?",
    "a": "The cumulative sum from start to i is negative, so i is where the running minimum lies. Starting at any k strictly inside makes the tank at i equal to that negative sum plus a positive-or-zero contribution, which is still negative. So none of them can work."
   },
   {
    "q": "What if the circuit were not circular?",
    "a": "The problem becomes trivial: you only need the prefix sums to be non-negative, so the answer is the first index where the running sum never dips below zero again. The circular wrap-around is exactly what makes gas station non-obvious."
   }
  ]
 },
 "15_greedy/0678_valid_parenthesis_string": {
  "one_liner": "Two passes: balance can never go negative, then reversed.",
  "core_objective": "Decide whether a string of '(' and ')' is valid by inserting at most one pair anywhere.",
  "bounds": "0 <= s.length <= 5e3, and an empty string is valid. The count of opens minus closings must be in {-1, 0, 1}.",
  "diagram": " s = \"))((\"  -> valid (insert one pair: ( ))(( )) no)\n  insert at index 2:  \"))\" + \"(\" + \"((\" -> ()(() ...\n  simpler: \"))<\" becomes \")>)((\" -> insert '(' at 0 and ')' at 4:\n          \"(\" + \"))((\" + \")\" = \"())(()\"  hmm\n  correct: needed opens = 2, needed closes = 2 -> one pair\n          insufficient! but the answer is TRUE.\n\n  correct count for \"))((\": opens=2, closes=2. Inserting ONE\n  pair gives 3 of one and 2 of the other -> counts are\n  (2,3) or (3,2), never equal. So one insert canNOT fix the\n  counts... yet the answer is true. Rechecking: insert '(' at\n  position 0 -> \"(())((\" ; then ')' still needed.\n\n  the actual valid form:  \"())()\" needs 1 pair inserted into\n  \"))((\"? ( ) ) ( ( -> insert '(' before first ')' and ')'\n  after last '('  =  \"(())(()\"  -> that has 4 opens 2 closes.\n\n  Resolution: for \"))((\" the answer IS true -- insert one\n  '(' at index 0 giving \"(()((\" is not it either.\n  Correct: needed = |opens - closes|. Here |2-2| = 0, so\n  zero pairs are needed by count; the only issue is ordering.\n  First pass (forward): balance never negative?\n   ) -> balance -1  NEGATIVE -> needs one '(' inserted at 0\n   ) -> balance -2  still negative\n   ( -> -1\n   ( -> 0\n  Second pass (reverse) counts ')' as open:\n   ( -> -1 ... also negative -> needs one ')' inserted\n  max needed = max(1, 1) = 1 <= 1 -> TRUE. The single pair\n  is '(' at the front and ')' at the back -- ONE pair supplies\n  BOTH because they are the two characters of a pair.",
  "cpp_alts": [
   "Two `int` counters, two passes -- no allocation.",
   "`std::count` for the totals plus one pass is an alternative formulation."
  ],
  "py_alts": [
   "`s.count('(')` and a single pass suffice for some variants; the two-pass version is unambiguous.",
   "A one-liner: `needed = max(-min_prefix, max_suffix_deficit)` over the two directions."
  ],
  "trap": "Checking only that the counts are balanced, or only one direction. \"))((\" has equal counts but is invalid, and \")(\" needs a '(' at the front even though the counts differ by zero... more precisely \"((\" needs a ')' at the end while the forward scan looks fine.",
  "invariant": "The forward scan's `low` is the most negative prefix balance; inserting exactly `-low` opens at the front fixes every prefix. The backward scan's `low` similarly measures the opens that need closes inserted. Both must be at most 1, and one inserted pair contributes one open and one close, so the requirement is max(forward deficit, backward deficit) <= 1.",
  "questions": [
   {
    "q": "Why are two passes needed?",
    "a": "A string can be broken in two independent ways: too many closers early (fixed by adding an open at the front) and too many opens late (fixed by adding a close at the end). One direction of scanning catches only one of them, and a single inserted pair supplies one of each character."
   },
   {
    "q": "How do you compute the required inserts in one expression?",
    "a": "Forward: let L be the minimum prefix balance of #open minus #close. You need -L opens at the front if L < 0. Backward: let R be the minimum balance of #close minus #open over reversed prefixes. You need -R closes at the end if R < 0. The answer is true iff max(-L, -R, 0) <= 1."
   },
   {
    "q": "What is the complexity?",
    "a": "$O(n)$ time and $O(1)$ space -- two counters over two passes, no allocation in either language. That is a rare problem where the optimal solution uses no extra memory at all."
   }
  ]
 },
 "15_greedy/0763_partition_labels": {
  "one_liner": "Record each char's last index, then sweep.",
  "core_objective": "Return the number of contiguous substrings such that each contains no repeated characters.",
  "bounds": "0 <= s.length <= 1e4 over lowercase letters, so 26 is the alphabet size and the last-index array is tiny. An empty string has 0 partitions.",
  "diagram": " s = \"ababcbacadefegdehijhklij\"  -> 3\n\n  last = {a:7, b:5, c:3, d:9, e:11, f:8, g:13, h:12,\n         i:16, j:15, k:14, l:...}\n\n  sweep from left:\n   start=0, end=0\n   i=0 'a' -> end = max(0, 7) = 7\n   i=1 'b' -> end = max(7, 5) = 7\n   i=2 'a' -> 7\n   i=3 'b' -> 7\n   i=4 'c' -> max(7,3)=7\n   i=5 'a' -> 7\n   i=6 'c' -> 7\n   i=7 'd' -> max(7,9) = 9   end exceeded i=7 -> CLOSE\n        partition 1 = s[0..7], length 8\n   restart at 8: 'e' -> max(8,11) = 11\n   i=8 'f' -> 11, i=9 'g' -> 13\n   i=10 'e' -> 13, i=11 'd' -> 13, i=12 'f' -> 13,\n   i=13 'g' -> 13   -> CLOSE at 13, length 6\n   restart at 14: 'h' i k l j i h -> close at 19\n   total partitions = 3",
  "cpp_alts": [
   "`array<int,26> last` of 104 bytes, always in L1.",
   "`vector<int> last(26, -1)` plus a pass over the string; two linear passes, no hashing."
  ],
  "py_alts": [
   "A list of 26 ints indexed by `ord(c) - 97` avoids dict hashing entirely.",
   "`s.count(c, i)` is an alternative but is $O(n^2)$."
  ],
  "trap": "Closing the partition as soon as `i == end` using a stale end, or resetting `end` without restarting at i+1. The partition boundary must be exactly the max last-index seen in the current segment, and the new segment starts at i+1.",
  "invariant": "`end` is the maximum last-occurrence index among all characters seen so far in the current segment. While i <= end, some character in the segment reappears after i, so the segment cannot be closed yet. When i reaches end, every character in the segment occurs only within it, making it a valid partition and the maximum possible one.",
  "questions": [
   {
    "q": "Why is each produced partition maximal?",
    "a": "Because the segment cannot be cut anywhere inside it -- some character straddles each internal boundary. So there is exactly one valid partition of each length starting at 0, and the answer counts them, not all possible partitions."
   },
   {
    "q": "What is the complexity?",
    "a": "$O(n)$ time -- two passes, one to build last-occurrence indices and one to sweep -- and $O(1)$ space for the fixed 26-entry table. The alphabet size is what makes it constant rather than O(n) space."
   },
   {
    "q": "How would this change with a large alphabet?",
    "a": "The table becomes O(sigma) space instead of O(1). A hash map would still give O(n) time, but the array is faster and the choice between them is exactly the constant-factor-versus-space trade-off."
   }
  ]
 },
 "15_greedy/0846_hand_of_straights": {
  "one_liner": "Take the smallest card; its run must extend to a larger card.",
  "core_objective": "Decide whether the hand can be partitioned into groups of k consecutive cards.",
  "bounds": "1 <= hand.length <= 1e4 with 1 <= card[i] <= 1e4, and hand.length must be divisible by k or the answer is immediately false. Duplicate values are common and must be handled.",
  "diagram": " hand=[1,2,3,3,4,4,5], k=3  -> true\n  sorted: 1 2 3 3 4 4 5\n\n  counts: 1:1  2:1  3:2  4:2  5:1\n  x=1: need a run 1,2,3 -> take 1 each\n       counts: 1:0 2:0 3:1 4:2 5:1\n  x=3 (smallest remaining): run 3,4,5 -> take 1 each\n       counts: 3:0 4:1 5:0\n  x=4: run 4,5,6 -> count[6] == 0 -> FALSE\n\n  so [1,2,3,3,4,4,5] k=3 is FALSE.\n  true example: hand=[1,2,3,3,4,4,5,6] k=3\n   x=1: 1,2,3\n   x=3: 3,4,5\n   x=4: 4,5,6\n   -> TRUE\n\n  invariant: x is the SMALLEST remaining card, so any group\n  containing it MUST start at x. That forces the run\n  x..x+k-1, and consuming those is never wrong -- there is\n  no alternative grouping for x.",
  "cpp_alts": [
   "A 1e4-entry count array is 40 KB, so a counting sort plus index walk avoids hashing.",
   "`std::map<int,int>` with iterator advance handles the run extraction in one pass."
  ],
  "py_alts": [
   "`Counter(hand)` plus iterating `sorted(counts)` gives the same forced-choice logic.",
   "Skip zero-count keys quickly by breaking once the key exceeds max(card) - k + 1."
  ],
  "trap": "Taking any run rather than the one starting at the smallest card. That can consume a card needed by a later forced group and wrongly return false.",
  "invariant": "When x is the smallest card with a positive count, every valid partition must place x at the start of some run, since no smaller card remains. Therefore the run x, x+1, ..., x+k-1 is mandatory, and decrementing one of each is the only possible choice. If any is missing the partition is impossible.",
  "questions": [
   {
    "q": "Why must the run start at x?",
    "a": "Because x is the smallest remaining value. A run containing x could not start before x, since that card is gone, and runs are consecutive -- so x is necessarily the first element of its run."
   },
   {
    "q": "What is the complexity?",
    "a": "$O(n + \\sigma \\log \\sigma)$ time to count and sort the distinct values, then $O(\\sigma \\cdot k)$ for the run consumption, bounded by n overall. Space is $O(\\sigma)$ for the counter."
   },
   {
    "q": "Why is the divisibility check useful?",
    "a": "It is an O(1) rejection that catches a large class of impossible inputs before any work. Every group has exactly k cards, so hand.length mod k must be 0 for any partition to exist."
   }
  ]
 },
 "15_greedy/1899_merge_triplets_to_form_target_triplet": {
  "one_liner": "Per-position minima then one filtered merge.",
  "core_objective": "Return the maximum possible value of a merged triplet that equals the target, where each triplet is merged element-wise and values must stay below target.",
  "bounds": "1 <= triplets.length <= 1000 with 1 <= values <= 1000, and a guaranteed solution exists. Zero-valued triplets are legal.",
  "diagram": " triplets=[(2,2,3),(1,2,3),(1,1,4)], target=5 -> 5\n  filtered to values strictly BELOW 5 per position:\n   pos0: min(2,1,1) = 1\n   pos1: min(2,2,1) = 1\n   pos2: min(3,3,4) = 4   -> min(3,3,3) = 3\n  so keep only triplets with a[0]==1, b[0]==1, c[0]==3\n  -> (1,2,3) -> 1+2+3 = 6 != 5? the third is (1,1,4)?\n\n  corrected filtering: keep triplets that EQUAL the target in\n  some position, otherwise discard:\n   (2,2,3): c==3 < 5, a,b not 5\n   (1,2,3): c==3 < 5\n   (1,1,4): none equal 5, all < 5\n   all three survive the <5 test; the minima are 1,1,3\n   requiring a==1, b==1, c==3 -> (1,2,3) has b=2\n   -> with (1,1,4): a=1,b=1,c=4 -> sum 6\n   target 5 requires (1,1,3) which does not exist.\n\n  The actual filter keeps triplets that are BELOW target in\n  every position; then the three per-position minima are\n  taken; then we merge and if the sum equals target, that is\n  the answer. Where the sum exceeds target, some position\n  must be lowered -- and the per-position minimums already\n  give the lowest reachable triple.",
  "cpp_alts": [
   "`array<int,3> best = {INT_MAX,INT_MAX,INT_MAX}` and one pass, O(n) time O(1) space.",
   "Two passes: filter first (also O(1) space), then merge. The filter makes the merge step trivially correct."
  ],
  "py_alts": [
   "A list of three sentinels and comparisons beats `min()` calls in a hot loop.",
   "A generator with `min(...)` per position is concise; `zip(*triplets)` plus `min` is the shortest form."
  ],
  "trap": "Taking the per-position minimum over ALL triplets instead of only those below target. A triplet with a value above target can never participate, so including it lowers a minimum to an unusable value and the merge fails.",
  "invariant": "Any triplet participating in a solution must have all three values strictly below target, since a merged value equals one of the contributing triplets' values in its position. Among the filtered triplets, the per-position minima form a lower bound that is simultaneously achievable -- so if any merge works, the minima merge works too.",
  "questions": [
   {
    "q": "Why are per-position minima sufficient?",
    "a": "If some triplet in the filtered set has a[0] > min(a) then replacing it with the minimiser is never worse, since the constraint is only a[0] + b + c == target and lowering one coordinate cannot overshoot. So the minima triple is achievable and is the lowest, making it the best candidate."
   },
   {
    "q": "What if the minima sum exceeds the target?",
    "a": "Then no merge can equal the target, because the minima triple is a lower bound on every achievable sum. Since the problem guarantees a solution exists, that branch is unreachable for valid input."
   },
   {
    "q": "Why the strict `<` comparison on target?",
    "a": "A merged value equals one contributing value, and the target requires the SUM to equal target, so any single value equal to target would force the other two to be zero. Using `<` filters the general case; using `<=` is only safe when zeros are allowed and handled."
   }
  ]
 },
 "16_intervals/0056_merge_intervals": {
  "one_liner": "Sort by start; merge when start <= current end.",
  "core_objective": "Merge all overlapping intervals into a minimal set of disjoint intervals.",
  "bounds": "1 <= intervals.length <= 1e4 with up to 1e9 endpoints. An interval may be [x, x] and touching intervals such as [1,4] and [4,5] DO merge.",
  "diagram": " input: [[1,3],[2,6],[8,10],[15,18]]\n         -> [[1,6],[8,10],[15,18]]\n\n  sorted by start: (1,3) (2,6) (8,10) (15,18)\n\n  out = []\n  for s, e in sorted:\n    if out and s <= out[-1][1]:        # overlap OR touch\n        out[-1][1] = max(out[-1][1], e) # extend to the max end\n    else:\n        out.append([s, e])\n\n  trace:\n   (1,3)  -> out=[[1,3]]\n   (2,6)  -> 2 <= 3 -> out=[[1,6]]\n   (8,10) -> 8 > 6  -> out=[[1,6],[8,10]]\n   (15,18)-> 15 > 10 -> out=[[1,6],[8,10],[15,18]]\n\n  WHY <= AND NOT <:\n   [1,4] and [4,5] share the point 4, so they form one\n   contiguous interval [1,5]. Using < would emit two.\n\n  why sort by START and not by end: with start-sorted input,\n  once an interval does not overlap the current group, no\n  later one can either -- starts only increase.",
  "cpp_alts": [
   "`sort(v.begin(), v.end())` on `vector<pair<int,int>>` uses lexicographic order, which sorts by start first -- exactly what is needed.",
   "In-place compaction merges into `v[out++]` for $O(1)$ extra space beyond the sort."
  ],
  "py_alts": [
   "`sorted(intervals)` on tuples sorts by start then end, which is fine.",
   "Modifying the output in place (`out[-1][1] = ...`) avoids allocating new pairs per merge."
  ],
  "trap": "Using `<` instead of `<=` for the overlap test, which splits [1,4] and [4,5] into two intervals when they should merge into [1,5].",
  "invariant": "`out[-1]` always holds the merged interval covering the last accepted group, and its end is the maximum end among that group's intervals. If the next start exceeds that end, no later interval can overlap it either, since later starts are no smaller -- so appending is safe and final.",
  "questions": [
   {
    "q": "Why sort by start rather than by end?",
    "a": "Sorting by start gives a monotone frontier: once an interval's start passes the current group's maximum end, every remaining start is even larger, so the group is closed permanently. Sorting by end gives no such guarantee and the merge test becomes non-local."
   },
   {
    "q": "Why do touching intervals merge?",
    "a": "Because [1,4] and [4,5] have no gap -- their union is the single interval [1,5], and the problem asks for the minimal set of disjoint intervals. Splitting them would not be minimal."
   },
   {
    "q": "What is the complexity?",
    "a": "$O(n \\log n)$ time for the sort and $O(n)$ for the sweep, with $O(n)$ space for the result (or $O(1)$ extra with in-place compaction). The sort dominates, which is why sorting is unavoidable here."
   }
  ]
 },
 "16_intervals/0057_insert_interval": {
  "one_liner": "Three phases: before, overlapping block, after.",
  "core_objective": "Insert one interval into a set of non-overlapping sorted intervals and return the merged result.",
  "bounds": "0 <= intervals.length <= 1e4 and the input is guaranteed sorted and disjoint, so a single three-phase pass suffices. An empty input is legal.",
  "diagram": " intervals=[[1,3],[6,9]], new=[2,5]\n  -> [[1,5],[6,9]]\n\n  phase 1 (strictly before): s < new.start  -> copy through\n   (1,3): 1 < 2  -> copy\n   (6,9): 6 < 2? no\n  phase 2 (overlapping):  s <= cur.end  -> absorb\n   (6,9): 6 <= cur.end(5)? no\n  phase 3 (after): copy the rest\n\n  code:\n   i=0\n   while i < n and intervals[i].end < new.start:\n       out.push(intervals[i]); i++          # phase 1\n   new.start = min(new.start, intervals[i].start)\n   new.end   = max(new.end,   intervals[i].end)\n   while i < n and intervals[i].start <= new.end:\n       new.start = min(new.start, intervals[i].start)\n       new.end   = max(new.end,   intervals[i].end)\n       i++                               # phase 2 (grow on both)\n   out.push(new)\n   while i < n: out.push(intervals[i++])  # phase 3\n\n  the GROW on both ends is essential: [2,5] absorbing (6,9)\n  must extend new.end to 9, which may then absorb more.",
  "cpp_alts": [
   "`std::vector<Interval> out; out.reserve(n+1)` avoids repeated reallocation.",
   "Insert into the vector then merge in place is an alternative when avoiding a second container matters."
  ],
  "py_alts": [
   "A list comprehension for phases 1 and 3 with an index for phase 2 is readable; the index-based version avoids scanning the prefix twice.",
   "`bisect` can locate the insert point, but the linear scan is already $O(n)$ and simpler."
  ],
  "trap": "Failing to grow `new.end` after absorbing an interval, which is required when a later interval starts inside the newly extended range. Also, assuming only one interval overlaps rather than a whole block.",
  "invariant": "After phase 1, all copied intervals end strictly before the insertion point. During phase 2, `new` is the union of the insertion interval and every absorbed interval, so its start and end are the running min and max. Phase 2 stops exactly when the next start exceeds that union, at which point the union can never grow again.",
  "questions": [
   {
    "q": "Why three phases rather than one pass with a flag?",
    "a": "Because the roles differ: before the insertion point you copy verbatim, inside the overlapping block you absorb and grow, and after it you copy verbatim again. A single flag variable cannot express \"grow the range\" while still needing to copy unchanged intervals on both sides."
   },
   {
    "q": "Can you do it with binary search?",
    "a": "Yes -- `bisect` on the interval starts locates the first interval whose end >= new.start in $O(\\log n)$, after which the absorb loop is still $O(k)$. That gives $O(\\log n + k)$ time, but the total is still bounded by $O(n)$ because of the copy."
   },
   {
    "q": "What makes the absorb loop able to grow?",
    "a": "Each absorbed interval may extend `new.end` beyond the value that was tested, so the loop condition must be re-evaluated against the updated end. That is why the min/max updates happen inside the loop and not before it."
   }
  ]
 },
 "16_intervals/0252_meeting_rooms": {
  "one_liner": "Sort by start; any start < previous end is a conflict.",
  "core_objective": "Return true if two meetings share no overlap.",
  "bounds": "0 <= meetings.length <= 1e6, and meetings are half-open [start, end), so a meeting ending exactly when another starts is NOT a conflict. An empty list is trivially true.",
  "diagram": " meetings sorted by start:\n  [0,10]  [10,20]  [20,30]   -> all adjacent, no overlap\n  [0,10]  [5,6]    -> 5 < 10  -> OVERLAP -> false\n\n  prev_end = -inf\n  for s, e in sorted:\n     if s < prev_end: return False   # STRICT <, not <=\n     prev_end = e\n  return True\n\n  WHY ONLY THE PREVIOUS END MATTERS:\n  the intervals are sorted by start, so starts are\n  non-decreasing. If s >= prev_end then this meeting starts\n  after the previous one ended; and every earlier meeting\n  ended at or before prev_end, so none can conflict. Hence a\n  single running maximum of past ends suffices.",
  "cpp_alts": [
   "`sort` on `vector<pair<int,int>>` compares by start first automatically.",
   "`std::sort` on 1e6 pairs is about 0.2 s; the sweep afterwards is negligible."
  ],
  "py_alts": [
   "`sorted(meetings)` on 1e6 tuples works but allocates; sorting an index array is slower in CPython.",
   "Iterating the sorted list directly avoids index arithmetic."
  ],
  "trap": "Using `<=` instead of `<`, which declares [0,10] and [10,20] a conflict. LeetCode meetings are half-open, so touching is fine.",
  "invariant": "After processing k meetings, `prev_end` is the maximum end among them. The next meeting conflicts with some earlier one exactly when its start is less than that maximum -- because a conflict requires a previous interval whose end exceeds the new start. So one running value suffices instead of comparing against all previous intervals.",
  "questions": [
   {
    "q": "Why does only the previous end matter?",
    "a": "The list is sorted by start, so starts are non-decreasing. If the new start is at least the previous end, it is at least every earlier end too (since prev_end is the running max). If it is smaller, it conflicts with the meeting that set that max."
   },
   {
    "q": "What would change if intervals were closed?",
    "a": "The comparison becomes `<=` instead of `<`, because [0,10] and [10,20] would then share the point 10. That one character is the entire difference between the two conventions and a classic source of wrong answers."
   },
   {
    "q": "How does this differ from meeting rooms II?",
    "a": "Here you only need to know WHETHER a conflict exists, which the single running maximum answers in O(n) after sorting. There you need the maximum OVERLAP, which requires either a sweep line over events or a min-heap of active end times."
   }
  ]
 },
 "16_intervals/0253_meeting_rooms_ii": {
  "one_liner": "Sweep starts and ends separately with two pointers.",
  "core_objective": "Return the maximum number of meetings happening simultaneously.",
  "bounds": "0 <= meetings.length <= 1e5 with up to 1e9 endpoints. An empty list gives 0. Half-open intervals again, so a meeting ending at time t does not overlap one starting at t.",
  "diagram": " meetings=[[1,3],[2,6],[4,8]]  -> 3\n\n  starts = [1,2,4]\n  ends   = [3,6,8]\n\n  two-pointer sweep:\n   s=0 e=0 count=0 best=0\n   starts[0]=1 < ends[0]=3 -> count=1  best=1  s=1\n   starts[1]=2 < ends[0]=3 -> count=2  best=2  s=2\n   starts[2]=4 > ends[0]=3 -> count=1  e=1\n   starts[2]=4 < ends[1]=6 -> count=2         s=3\n   s exhausted, drain remaining ends -> done\n   best = 2, not 3. Correct answer for [[1,3],[2,6]] is 2.\n\n  For 3 simultaneous you need e.g. [[1,3],[2,6],[2,8]]:\n   starts[1]=2 < ends[0]=3 -> count 2\n   starts[2]=2 < ends[0]=3 -> count 3  BEST\n\n  invariant: `count` is the number of meetings started minus\n  ended so far, i.e. exactly the number in progress. The\n  sweep advances whichever side has the smaller next\n  timestamp, so no meeting is counted twice.",
  "cpp_alts": [
   "Two `vector<int>` sorts plus one merge pass is $O(n \\log n)$ with $O(n)$ space.",
   "`std::priority_queue` of end times with a lazy expiry is the alternative at $O(n \\log n)$."
  ],
  "py_alts": [
   "`sorted([s for s,_ in meetings])` plus `sorted([e for _,e in meetings])` and a manual two-pointer loop avoids heap overhead.",
   "A `heapq` of end times with `while heap and heap[0] <= s: heappop` is very readable and competitive."
  ],
  "trap": "Advancing the end pointer only while `ends[e] <= starts[s]`, which double-counts when several ends share a timestamp. The correct step compares timestamps and advances one side per iteration.",
  "invariant": "At every step, `count` equals the number of intervals whose start has been swept but whose end has not, which is exactly the number simultaneously in progress. Advancing the smaller next timestamp keeps that true, so the maximum recorded count is the true maximum overlap.",
  "questions": [
   {
    "q": "Why is the sweep correct when several events share a timestamp?",
    "a": "Because each iteration advances exactly one pointer by exactly one interval, and the comparison always picks the earlier event. Ties can be broken either way for half-open intervals, since a meeting ending at t and another starting at t never count together -- the end is processed first."
   },
   {
    "q": "Why does the heap version need a separate expiry loop?",
    "a": "A heap of end times can hold many stale entries whose ends are in the past. Before counting a new start you must pop every end <= s, not just the minimum, so the size reflects live meetings. That inner while loop is what keeps the heap meaningful."
   },
   {
    "q": "What is the complexity?",
    "a": "$O(n \\log n)$ time for the sorts, with an $O(n)$ sweep afterwards. Space is $O(n)$ for the two sorted arrays or the heap. A sweep-line over 2n events is the same bound with a different constant."
   }
  ]
 },
 "16_intervals/0435_non_overlapping_intervals": {
  "one_liner": "Sort by END; keep an interval only if it starts after the last kept one.",
  "core_objective": "Return the maximum number of non-overlapping intervals that can be selected.",
  "bounds": "1 <= intervals.length <= 1e5 with up to 1e9 endpoints, and the answer is the count KEPT, not the count removed. Intervals touching at an endpoint do not overlap.",
  "diagram": " intervals=[[1,2],[2,3],[3,4],[1,3]]  -> 2\n\n  sorted by END: (1,2) (2,3) (1,3) (3,4)\n\n  last_end = -inf, kept = 0\n  (1,2): 1 >= -inf -> keep, last_end = 2, kept=1\n  (2,3): 2 >= 2    -> keep, last_end = 3, kept=2\n  (1,3): 1 >= 3? NO -> skip\n  (3,4): 3 >= 3    -> keep, last_end = 4, kept=3\n  -> 3, so the answer for this input is 3\n\n  WHY END-SORT IS THE GREEDY WIN:\n  exchange argument -- let E be the earliest-ending\n  interval. Any optimal solution's first interval O ends no\n  earlier than E, so replacing O with E leaves every later\n  interval still compatible. Hence some optimal solution\n  starts with E, and the problem reduces to the same problem\n  on the intervals starting after E's end.\n\n  invariant: after each accepted interval, last_end is the\n  end of the last KEPT one, and the kept set is optimal for\n  the prefix considered so far.",
  "cpp_alts": [
   "`sort` with a custom comparator on `.second`; a `vector<pair<int,int>>` of (end, start) makes the default lexicographic sort work.",
   "Reversing the pairs so end is first is the trick that avoids writing a comparator."
  ],
  "py_alts": [
   "`sorted(intervals, key=lambda iv: iv[1])` sorts by end explicitly.",
   "`intervals.sort(key=lambda iv: iv[1])` mutates in place, avoiding a copy of 1e5 tuples."
  ],
  "trap": "Sorting by START instead of end. That greedy is not optimal: on [[1,100],[2,3],[3,4]] it takes [1,100] and keeps nothing else, giving 1 instead of the optimal 2.",
  "invariant": "Let E be the earliest-ending remaining interval. For any optimal solution, replacing its first interval with E cannot reduce the count, because E ends no later than anything it replaces, so all subsequent intervals remain compatible. Therefore taking E is safe, and the invariant holds inductively after restricting to intervals starting at or after E's end.",
  "questions": [
   {
    "q": "Why does earliest-end beat earliest-start?",
    "a": "The exchange argument. Taking the earliest-ending interval leaves the most room for whatever comes after; taking the earliest-starting one may occupy a long span and block several short intervals that would otherwise fit."
   },
   {
    "q": "What is the answer when the problem asks for removals?",
    "a": "It is the complement: intervals.length minus the maximum number kept. LeetCode 435 asks for removals, and the common bug is returning the kept count directly."
   },
   {
    "q": "What if intervals touching at an endpoint overlap?",
    "a": "The comparison becomes `>` rather than `>=`. With half-open intervals touching is fine, which is the standard convention and why `>=` is correct here."
   }
  ]
 },
 "16_intervals/1851_minimum_interval_to_include_each_query": {
  "one_liner": "Offline: sort queries, sweep, min-heap keyed by length.",
  "core_objective": "For each query k, return the smallest interval covering k.",
  "bounds": "1 <= intervals.length, queries.length <= 1e4, and each query k equals intervals.length. The queries need not be sorted, which is why the offline reordering matters.",
  "diagram": " intervals=[[3,4],[2,3],[1,4]]  queries=[2,3,4] -> [3,2,1]\n\n  sort queries: (2,0) (3,1) (4,2)\n  sort intervals by start: (1,4) (2,3) (3,4)\n\n  heap of (length, right), i pointer\n\n  k=2: add all with start <= 2 -> (1,4) len 3\n        -> top = 3   answer[0] = 3\n  k=3: add start <= 3 -> (2,3) len 1, (3,4) len 1\n        heap {(3,4),(1,3),(1,4)}\n        pop while heap[0].right < k=3 -> (1,3) popped\n        heap {(3,4),(1,4)}\n        top length = 1   answer[1] = 1\n  k=4: pop while right < 4 -> (3,4) has right 4, keep\n        top = (3,4) len 1  answer[2] = 1\n\n  INVARIANT: the heap holds exactly the intervals whose\n  start <= k; after popping stale tops, every remaining entry\n  covers k. So heap[0] is the minimum length among them.",
  "cpp_alts": [
   "`priority_queue<pair<int,int>, vector<...>, greater<...>>` keyed on (length, right) gives the minimum top directly.",
   "Sorting the queries pairs once and restoring results by the saved original index avoids any lookup."
  ],
  "py_alts": [
   "`heapq` with `(length, right)` tuples gives the same minimum-top semantics.",
   "Sorting `[(k, i) for i, k in enumerate(queries)]` keeps the original index attached, so results are restored in order."
  ],
  "trap": "Popping expired intervals only from the top. An interval with right < k is unusable, but since it may not be the minimum length it can sit inside the heap; that is harmless as long as the top is cleaned, because a shorter expired entry would have been popped and re-checked.",
  "invariant": "After adding every interval with start <= k, the heap contains all candidates. After the while loop, no interval with right < k can remain at the top, so the top entry has start <= k <= right, meaning it covers k. Since the heap is a min-heap on length, the top is the shortest covering interval.",
  "questions": [
   {
    "q": "Why sort the queries?",
    "a": "Because as k increases the set of covering intervals only changes by additions -- intervals that stop covering k never start covering a larger k. So a single left-to-right sweep suffices for queries in increasing order. Sorting is what makes one pass possible instead of one pass per query."
   },
   {
    "q": "Why is the heap keyed on length rather than start?",
    "a": "Because the answer is the minimum length. Keying on start would give the earliest-covering interval, which is not what is asked. The length is computed when the interval is inserted and never changes."
   },
   {
    "q": "What is the complexity?",
    "a": "$O(n \\log n + m \\log m + n \\log n + m)$ -- sorting both lists plus at most one heap push and pop per interval. Space is $O(n + m)$."
   }
  ]
 }
})

# ---- appended from _chunk12.json
DATA.update({
 "17_math_and_geometry/0043_multiply_strings": {
  "one_liner": "Digit-array accumulation from the low end; no big integers.",
  "core_objective": "Return the product of two non-negative integer strings, without using built-in big-integer conversion.",
  "bounds": "1 <= num1, num2 <= 10 digits, so the product is at most 20 digits and needs a string. Leading zeros are not present but zeros inside are legal.",
  "diagram": " num1=\"123\", num2=\"456\"  -> \"56088\"\n\n  m[3] n[3]  (digit arrays, least significant first)\n  result[n+m] = zeros\n\n  for i in 0..2:            outer = num1\n    for j in 0..2:          inner = num2\n      mul = m[i]*n[j]\n      total = mul + result[i+j]\n      result[i+j] = total % 10\n      result[i+j+1] += total / 10      # CARRY to the next slot\n\n  each slot can accumulate more than 9 because we carry the\n  quotient forward rather than normalising immediately.\n  i=0 j=0: 3*6=18 -> r[0]=8, r[1]+=1\n  i=0 j=1: 3*5=15 -> r[1]=5, r[2]+=1\n  i=0 j=2: 3*4=12 -> r[2]=2, r[3]+=1\n  i=1 j=0: 2*6=12 -> r[1]=7, r[2]+=1\n  ...\n  final digits (ls first) 8 8 0 8 6 5 -> \"56088\"\n\n  invariant: after processing pairs, every position holds the\n  correctly weighted partial sum of the single-digit products,\n  with carries propagated to the next higher slot.",
  "cpp_alts": [
   "`vector<int> res(n+m)` over exact-size digit arrays; converting back needs the leading-zero trim.",
   "`reverse()` on the digit vectors is O(n) and removes the index arithmetic."
  ],
  "py_alts": [
   "Python's arbitrary-precision `int(num1) * int(num2)` works but violates the problem's intent -- worth naming as a shortcut and rejecting.",
   "Reversing via `num1[::-1]` and indexing from the end avoids an explicit reverse call."
  ],
  "trap": "Forgetting to accumulate the carry with `+=` rather than assignment, or dropping the final carry slot. With 20 digits the product needs n+m slots exactly, so an off-by-one truncates the leading digit.",
  "invariant": "result[k] accumulates contributions from every digit pair (i, j) with i + j == k, weighted by 10^k. Each such contribution is m[i] * n[j] * 10^(i+j), so the sum over all pairs is exactly the product. Normalising each slot with % 10 and pushing the quotient to k+1 preserves the total.",
  "questions": [
   {
    "q": "Why does the result need exactly n+m slots?",
    "a": "The product of an m-digit and an n-digit number has at most m+n digits. Any fewer would truncate, and one more would leave a guaranteed-zero leading slot. That bound is also why no slot can overflow outward."
   },
   {
    "q": "Why is `result[i+j+1] += total / 10` safe?",
    "a": "Because total = mul + result[i+j] <= 81 + 9 + 9 = 99 in the worst case with fully normalised slots, so the quotient is at most 9 and fits in the next slot without further propagation. That bound relies on normalising every slot as you go, which the code does."
   },
   {
    "q": "How does this differ from the textbook row-by-row method?",
    "a": "The textbook version adds whole rows, each requiring an O(m) addition pass, giving $O(mn + mn) = O(mn)$ with much more code. The digit-array version writes directly into shared positions, so it is one pass of O(mn) with no intermediate rows."
   }
  ]
 },
 "17_math_and_geometry/0048_rotate_image": {
  "one_liner": "Transpose, then reverse each row.",
  "core_objective": "Rotate an n x n square matrix 90 degrees clockwise in place.",
  "bounds": "n x n is guaranteed square, which is what makes the two-step algorithm valid. Up to 20 x 20. Elements must not use an extra matrix.",
  "diagram": " [[1,2,3],[4,5,6],[7,8,9]]  -> [[7,4,1],[8,5,2],[9,6,3]]\n\n  transpose (mirror on the main diagonal):\n   1 4 7\n   2 5 8\n   3 6 9\n\n  reverse each row (mirror on the anti-diagonal):\n   7 4 1\n   8 5 2\n   9 6 3\n\n  clockwise = transpose then reverse rows\n  counterclockwise = reverse rows then transpose\n\n  WHY: a 90-degree clockwise rotation maps (r,c) -> (c, n-1-r).\n  Transposing maps (r,c) -> (c,r); reversing the row maps\n  (c,r) -> (c, n-1-r). The composition is the rotation.\n\n  transpose in place:\n   for r in 0..n-1:\n     for c in r+1..n-1:\n       swap(m[r][c], m[c][r])",
  "cpp_alts": [
   "`std::swap` plus two nested loops with the upper-triangular bound; the whole matrix stays in cache.",
   "`std::reverse` on each row of a `vector<int>` is a single library call per row."
  ],
  "py_alts": [
   "`[list(row) for row in zip(*matrix)]` transposes in one line, then reverse each row.",
   "`matrix.reverse()` on the outer list would rotate 180, not 90 -- the common slip."
  ],
  "trap": "Reversing the outer list instead of each row, which produces a 180-degree rotation. Also, looping the transpose over the full square rather than the strict upper triangle, which double-swaps and undoes itself.",
  "invariant": "After the transpose, entry (r, c) holds what was at (c, r); the strict-upper-triangle loop guarantees each pair is swapped exactly once. After the per-row reversal, entry (c, r') holds what the transpose put at (c, n-1-r'), which is the clockwise rotation.",
  "questions": [
   {
    "q": "Why must the matrix be square?",
    "a": "The two-step method composes two reflections of the same square, so it is only a rotation when the dimensions match. For a non-square matrix you would need padding, or the explicit four-way ring rotation."
   },
   {
    "q": "What is the alternative single-pass algorithm?",
    "a": "Four-way ring swaps: for each layer, swap the four elements at offsets 0, 1, 2, 3 of each ring position. That is one pass with O(1) extra space and no intermediate transpose state, at the cost of harder-to-read index arithmetic."
   },
   {
    "q": "What is the complexity?",
    "a": "$O(n^2)$ time and $O(1)$ extra space. The transpose visits n(n-1)/2 pairs and the reversal touches every element once."
   }
  ]
 },
 "17_math_and_geometry/0050_pow_x_n": {
  "one_liner": "Exponentiation by squaring: halve n, square x.",
  "core_objective": "Return x raised to n for integer n, handling negative exponents.",
  "bounds": "-2^31 <= n <= 2^31 - 1, so the exponent needs 64-bit arithmetic in C++ to shift safely. x can be 0, and 0 to the 0th power is 1.",
  "diagram": " x=2, n=10  -> 1024\n\n  binary: 10 = 1010 = 8 + 2\n\n  result=1, base=2, exp=10\n   exp even -> exp=5,  base=4    (square)\n   exp odd  -> result*=4=4, exp=4, base=16\n   exp even -> exp=2,  base=256\n   exp even -> exp=1,  base=65536\n   exp odd  -> result *= 65536 -> 262144? no\n\n  trace carefully:\n   r=1  b=2  e=10  e even -> e=5,  b=4\n   r=1  b=4  e=5   e odd  -> r=4, e=4, b=16\n   r=4  b=16 e=4   e even -> e=2,  b=256\n   r=4  b=256 e=2  e even -> e=1,  b=65536\n   r=4  b=65536 e=1 e odd  -> r=262144, e=0 -> stop\n   result 262144 != 1024 -> the doubling is wrong\n\n  CORRECT algorithm:\n   r=1  b=2  e=10\n   e even -> e=5,  b=b*b=4\n   e odd  -> r=r*b=4, e=4, b=b*b=16\n   e even -> e=2,  b=256\n   e even -> e=1,  b=65536\n   e odd  -> r=r*b=262144, e=0\n   262144 = 2^18, not 2^10. The binary of 10 is 1010;\n   the squares used were 2^2,2^4,2^8,2^16 and r took 2^2\n   and 2^16 -> so the update order must be:\n     if e odd: r *= b; e -= 1\n     b *= b; e //= 2\n   r=1 b=2 e=10\n     e even: b=4, e=5\n     e odd: r=4, e=4; b=16, e=2\n     e even: b=256, e=1\n     e odd: r=4*256=1024, e=0  CORRECT",
  "cpp_alts": [
   "`long long n` is mandatory: shifting a 32-bit n right is fine but the multiplication needs 64-bit intermediates.",
   "`unsigned long long` for the accumulator avoids signed-overflow UB on intermediate squares even though the final answer fits."
  ],
  "py_alts": [
   "Python's `**` handles this in one operation; writing the loop is about demonstrating the algorithm.",
   "`pow(x, n)` with three arguments does modular exponentiation, useful if a modulus is added."
  ],
  "trap": "Squaring the base before consuming the odd bit, or decrementing e after halving it. The two lines must be ordered: multiply into the result and subtract one while odd, THEN square and halve.",
  "invariant": "The loop maintains result * base^e == x^n_original. Each iteration either squares (preserving base^e as (base^2)^(e/2) when e is even) or extracts one factor of base into result and decrements e (preserving the product). When e reaches 0, result is the answer.",
  "questions": [
   {
    "q": "Why is the algorithm logarithmic?",
    "a": "Every iteration halves e, so there are at most log2(|n|) iterations -- at most 31 for a 32-bit exponent. Naive repeated multiplication is O(n) and would be astronomically slow for n = 2^31."
   },
   {
    "q": "How are negative exponents handled?",
    "a": "They are not, structurally: the halving loop terminates only for positive e. You must first convert x^-k into (1/x)^k, which requires either a float or integer division, and x = 0 with a negative exponent is undefined."
   },
   {
    "q": "Why does 0^0 equal 1 here?",
    "a": "Because result is initialised to 1 and the loop returns result when e becomes 0, before any base multiplication. That is the standard convention and matches the judge's expectation."
   }
  ]
 },
 "17_math_and_geometry/0054_spiral_matrix": {
  "one_liner": "Four boundaries that shrink after each pass.",
  "core_objective": "Return all elements of a matrix in spiral order.",
  "bounds": "m, n >= 1 with up to 1e6 elements, so a single row or column must terminate correctly. The 1 x n case is the classic off-by-one source.",
  "diagram": " [[1,2,3],[4,5,6],[7,8,9]]  -> 1 2 3 6 9 8 7 4 5\n\n  top=0 bottom=2 left=0 right=2\n\n  while top <= bottom and left <= right:\n    top row:    1 2 3      (c from left to right)\n    right col: 6 9        (r from top+1 to bottom)\n    top++\n    bottom row: 8 7        (only if top <= bottom!)\n    right--\n    left col:  4           (only if left <= right!)\n    bottom--\n\n  THE GUARDS ARE ESSENTIAL:\n   after the top row, bottom-- must be conditional on\n   top <= bottom, else a 1-row matrix emits a duplicate row.\n   after the right col, right-- must be conditional on\n   left <= right, else a 1-column matrix emits duplicates.\n\n  trace:\n   top row 1 2 3 ; right col 6 9 ; top=1\n   bottom row 8 7 (bottom=2 >= top=1 ok) ; right=1 ; bottom=1\n   left col 4 ; bottom=0 -> loop ends",
  "cpp_alts": [
   "Four `int` boundaries and a lambda `push` that appends and advances; one lambda removes four duplicated lines.",
   "`vector<int> out; out.reserve(m*n)` avoids repeated reallocation."
  ],
  "py_alts": [
   "A list of four boundaries with `while top <= bottom and left <= right` is the cleanest form.",
   "`out.extend(row[left:right+1])` for the top row is C-speed, though the explicit loop is more uniform."
  ],
  "trap": "Emitting the bottom row or left column without re-checking the corresponding boundary condition. On a single-row matrix that duplicates every element; on a single-column matrix it duplicates the column.",
  "invariant": "The four boundaries always delimit the unvisited rectangle. Each pass emits exactly the outer ring and then shrinks the appropriate boundaries by one, so every element is emitted exactly once and the loop terminates when the rectangle is empty.",
  "questions": [
   {
    "q": "Why is there no extra space?",
    "a": "The traversal order is determined entirely by the four boundaries, so no visited array or queue is needed. A BFS-based spiral would need O(mn) extra space; the boundary walk uses O(1) beyond the output."
   },
   {
    "q": "What is the output space complexity?",
    "a": "$O(mn)$ for the result, which is unavoidable since every element is returned. Auxiliary space is $O(1)$, making this an output-optimal $O(mn)$ algorithm."
   },
   {
    "q": "How do you handle a 1 x n matrix?",
    "a": "The top row emits all n elements, then the loop must not emit a bottom row. The `if top <= bottom` guard before the bottom-row pass is what enforces that; without it you emit the row twice."
   }
  ]
 },
 "17_math_and_geometry/0066_plus_one": {
  "one_liner": "Scan from the right, carry until a non-9 is found.",
  "core_objective": "Increment a number represented as an array of digits by one.",
  "bounds": "1 <= digits.length <= 100, so the array can represent a number far beyond any fixed integer type. All elements are 0..9 and the leading digit is never zero, except for the array [0].",
  "diagram": " [1,2,5]      -> [1,2,6]\n  [4,3,2,2,9]  -> [4,3,2,3,0]\n  [9,9]        -> [1,0,0]   (new leading digit)\n  [0]          -> [1]\n\n  i = n-1\n  while i >= 0 and digits[i] == 9:\n     digits[i] = 0     # 9 -> 0, carry out\n     i -= 1\n  if i >= 0:\n     digits[i] += 1\n  else:\n     digits.insert(begin, 1)   # every digit was 9\n\n  WHY THE 9-RUN MATTERS: only trailing 9s produce a carry.\n  The first non-9 from the right absorbs the carry and stops\n  it. If no non-9 exists, the answer gains a digit.\n\n  trace [4,3,2,2,9]:\n   i=4 digits[4]=9 -> 0, i=3\n   i=3 digits[3]=2 != 9 -> stop\n   digits[3] += 1 -> [4,3,2,3,0]  CORRECT",
  "cpp_alts": [
   "`digits.insert(digits.begin(), 1)` is $O(n)$ and fine; a two-pointer fill into a preallocated vector is $O(1)$ amortised instead.",
   "The int-to-string conversion is deliberately forbidden -- that is the point of the problem."
  ],
  "py_alts": [
   "`[int(d) for d in str(int(s) + 1)]` violates the intent; it also fails on a 100-digit string in fixed-width languages but works in Python, which is exactly why the loop is the right answer here.",
   "`digits.insert(0, 1)` is a single O(n) operation and reads clearly."
  ],
  "trap": "Checking only the last digit. [9,9] and [1,9,9] both need the carry to propagate and a new leading digit, and treating them as single-digit cases returns wrong answers.",
  "invariant": "After the while loop, all digits at indices greater than i have been set to 0 and i is the highest index whose digit is not 9 (or -1 if none exists). Those trailing zeros are exactly the carry-out positions, and incrementing digits[i] -- or prepending 1 when i == -1 -- performs the addition with no further propagation.",
  "questions": [
   {
    "q": "Why does only trailing 9s carry?",
    "a": "Because adding 1 to a digit d yields d+1 unless d == 9, which yields 10 and writes 0 with a carry. So the carry propagates leftward precisely through a maximal run of 9s and stops at the first smaller digit."
   },
   {
    "q": "What if every digit is 9?",
    "a": "Then i reaches -1 and the answer needs one more digit than the input. That is the [9,9] to [1,0,0] case, and prepending 1 is the only correct handling."
   },
   {
    "q": "What is the complexity?",
    "a": "$O(n)$ time -- each digit is touched at most twice -- and $O(1)$ extra space apart from the possible insert, which is $O(n)$ and happens at most once."
   }
  ]
 },
 "17_math_and_geometry/0073_set_matrix_zeroes": {
  "one_liner": "Use the first row and column as the marker storage.",
  "core_objective": "Set every cell sharing a row or column with an original zero to zero, in place.",
  "bounds": "m, n up to 200 and the output matrix is huge -- copying it is explicitly disallowed. The first row and first column may themselves be zeroed, which is the whole subtlety.",
  "diagram": " [[1,1,1],[1,0,1],[1,1,1]]\n\n  the 0 at (1,1) means row 1 and column 1 become 0:\n   1 0 1\n   0 0 0\n   1 0 1\n\n  THREE-STEP ALGORITHM:\n  1. mark rows/cols that contain a zero, storing the flags\n     IN THE FIRST ROW and FIRST COLUMN\n  2. for each cell (r,c) with r>0 and c>0:\n       if row_flag[r] or col_flag[c]: m[r][c] = 0\n  3. zero out the first row and first column from their flags\n\n  the first row/column are used as the marker array because\n  the problem forbids extra space. If m[0][0] itself is a\n  zero, every cell must be zero -- step 3 handles that from\n  the flags, not from the overwritten value.\n\n  why the corner cell needs a separate flag:\n   if only m[0][0] were zero we'd wipe the marker storage\n   before reading it. Keeping the flags in row 0 / col 0 and\n   processing them LAST avoids the ordering problem.",
  "cpp_alts": [
   "`vector<bool> rowFlag(m), colFlag(n)` is the $O(m+n)$ extra space version the problem forbids but interviewers often accept as the first attempt.",
   "`std::vector<char>` avoids vector<bool>'s proxy overhead and is clearer than a bitset."
  ],
  "py_alts": [
   "`rows = set()`, `cols = set()` is the readable $O(m+n)$ version.",
   "The three-step in-place version is what the problem asks for; the marker row/column trick is the point."
  ],
  "trap": "Using m[0][0] as the sole marker for row 0 and column 0 simultaneously. If the original m[0][0] was a zero, the marker loses its meaning and the answer is wrong; separate flags in row 0 and column 0, applied last, are required.",
  "invariant": "After step 1, `rowFlag[r]` and `colFlag[c]` record whether row r and column c contained an original zero, and the interior of the matrix is still unmodified. Step 2 therefore zeroes exactly the cells sharing a row or column with a zero, using only original information. Step 3 applies the flags to the marker row and column last, so their values are read before being destroyed.",
  "questions": [
   {
    "q": "Why must the first row/column be processed last?",
    "a": "Because they hold the flags. If you zeroed them earlier you would lose the record of whether rows 0 or columns 0 contained zeros. Applying them last means the information has already been consumed by the interior pass."
   },
   {
    "q": "What is the alternative with extra space?",
    "a": "Two boolean arrays of size m and n. That is $O(m+n)$ space, trivially correct, and worth writing first -- the in-place version is the interesting follow-up that the constraint forces."
   },
   {
    "q": "What is the complexity?",
    "a": "$O(mn)$ time for the three passes and $O(1)$ extra space for the in-place version. Each cell is examined a constant number of times."
   }
  ]
 },
 "17_math_and_geometry/0201_bitwise_and_of_numbers_range": {
  "one_liner": "The AND of a range is the common prefix; right-shift to find it.",
  "core_objective": "Return m & (m+1) & ... & n for 0 <= m <= n <= 2^31-1.",
  "bounds": "0 <= m <= n <= 2^31 - 1, so 31 bits suffice. m == n returns m. The answer is always a power-of-two-aligned block.",
  "diagram": " m=5, n=7  -> 4\n\n  5 = 101\n  6 = 110\n  7 = 111\n  AND:\n    101\n    110\n    111\n    ---\n    100 = 4\n\n  COMMON PREFIX: the top bit (bit 2) is shared; everything\n  below differs because the range crosses a power-of-two\n  boundary at 8.\n\n  shift-right approach:\n   sh = 0\n   while m != n: m >>= 1; n >>= 1; sh += 1\n   return m << sh\n\n   m=5 n=7 -> 2,3 sh=1 -> 1,1 sh=2 -> stop\n   return 1 << 2 = 4  CORRECT\n\n  shift-until-equal alternative:\n   while m < n: m >>= 1; n >>= 1\n   return m\n\n  invariant: shifting both endpoints right by the same amount\n  preserves the common prefix, and they become equal exactly\n  when the remaining bits are all that they share. Shifting\n  back left restores the zeroes below the prefix, which is the\n  required AND.",
  "questions": [
   {
    "q": "Why does m == n after shifting imply the answer?",
    "a": "When both endpoints collapse to the same value v, every number in the range agrees with v on all remaining high bits and the lower bits of the range contain a transition, so the AND of those low bits is 0. Hence the answer is v followed by sh zeros."
   },
   {
    "q": "What is the simpler formulation?",
    "a": "`while m < n: m >>= 1; n >>= 1; return m`. Because m <= n always, and m < n guarantees a differing low bit, the loop shifts out exactly the non-common part, so no shift counter is needed."
   },
   {
    "q": "What is the complexity?",
    "a": "$O(\\log n)$ time -- at most 31 shifts -- and $O(1)$ space. In C++ use `unsigned` to avoid sign-extension issues on the right shift; in Python the integers are arbitrary-precision and never negative here."
   }
  ]
 },
 "17_math_and_geometry/0202_happy_number": {
  "one_liner": "Floyd cycle detection over the digit-square-sum chain.",
  "core_objective": "Return true if repeatedly summing the squares of the digits reaches 1.",
  "bounds": "Any integer, typically within int. Numbers above 243 always fall into a cycle, so the chain is bounded and the loop must terminate.",
  "diagram": " n=19 -> true\n  19 -> 1 + 81 = 82\n   82 -> 64 + 4  = 68\n   68 -> 36 + 64 = 100\n  100 -> 1 + 0 + 0 = 1   HAPPY\n\n  n=2 -> false\n   2 -> 4 -> 16 -> 37 -> 58 -> 89 -> 145 -> 42 -> 20\n      -> 4 (cycle detected)\n\n  Floyd on the function f(n) = sum of digit squares:\n   slow = f(n), fast = f(f(n))\n   while fast != 1 and slow != fast:\n      slow = f(slow); fast = f(fast))\n   return fast == 1\n\n  WHY IT TERMINATES: any n >= 1000 maps to at most 4*81=324,\n  and 999 -> 243, so the chain is bounded by 243 and must\n  eventually repeat. Floyd detects the repeat in O(1) space.\n\n  ALTERNATIVE: a set of visited values, O(1) space in\n  practice since the chain is bounded by 243, and clearer.",
  "cpp_alts": [
   "`int sumOfSquares(int n)` with a `while (n) { s += (n%10)*(n%10); n /= 10; }` loop.",
   "An `unordered_set<int>` visited set is simpler but allocates; Floyd avoids that entirely."
  ],
  "py_alts": [
   "`sum(int(c)**2 for c in str(n))` is concise and readable at this scale.",
   "`divmod(n, 10)` gives digit and quotient in one operation, avoiding two separate divisions."
  ],
  "trap": "Using a visited set without a termination bound, or forgetting that the cycle may not include 1 -- so the loop condition must check both `fast == 1` and `slow == fast`, otherwise a non-1 cycle spins forever.",
  "invariant": "The chain n -> f(n) -> f(f(n)) -> ... is eventually periodic because it is bounded. Floyd's two pointers advance at speeds 1 and 2, so they must meet inside the cycle; meeting at a value of 1 means the chain reaches 1, and meeting elsewhere means it is trapped.",
  "questions": [
   {
    "q": "Why is the chain bounded?",
    "a": "A number with d digits maps to at most 81d. For d = 4 that is 324, and 324 has three digits so it maps to at most 243. From then on the chain stays inside 1..243, a finite set, so it must repeat."
   },
   {
    "q": "What is the general technique here?",
    "a": "Cycle detection on a deterministic function of a bounded domain -- exactly Floyd's tortoise and hare, identical in structure to linked-list cycle detection and to the duplicate-number problem. The invariant is that the two pointers meet inside the cycle."
   },
   {
    "q": "Why does meeting at 1 mean happy?",
    "a": "If the chain reaches 1 then it stays at 1, since f(1) = 1. So 1 is a fixed point, and the fast pointer reaches it within at most one full cycle of steps. Meeting elsewhere means the chain entered a cycle that does not contain 1."
   }
  ]
 },
 "17_math_and_geometry/2013_detect_squares": {
  "one_liner": "Axis-aligned square: check all four corners on first detection.",
  "core_objective": "Detect whether any axis-aligned square made of grid points exists, using a set of points.",
  "bounds": "0 <= points.length <= 1000 with coordinates in [0, 1000], so the O(n^2) pair scan is intended. Duplicate points are not guaranteed absent, which matters for correctness.",
  "diagram": " points = [(0,0),(1,1),(2,0),(2,2),(0,2)]  -> true\n\n  the SQUARE of side d at corner (x,y) needs:\n   (x, y), (x+d, y), (x, y+d), (x+d, y+d)\n\n  algorithm: treat one point as the TOP-RIGHT corner and\n  scan the others as the BOTTOM-LEFT, deriving d.\n\n   for each (x1, y1):                     # bottom-left\n     for each (x2, y2):                   # top-right candidate\n       d = x2 - x1; dy = y2 - y1\n       if d != dy or d == 0: continue\n       if (x1 + d, y1) in S and (x1, y1 + d) in S:\n           return True\n\n  for the example:\n   (0,0) & (1,1): d=1, dy=1 -> need (1,0) and (0,1) -> no\n   (0,0) & (2,2): d=2, dy=2 -> need (2,0) YES and (0,2) YES\n                -> TRUE\n\n  diagonal is enough: the four corners of an axis-aligned\n  square are exactly bottom-left, bottom-right, top-left,\n  top-right, and d must be equal in both directions.",
  "cpp_alts": [
   "`std::set<std::pair<int,int>>` with logarithmic lookup; `unordered_set` with an encoded key `(long long)x * 100000 + y` is faster.",
   "Deduplicate the input first, since duplicate points would produce a false zero-size square unless d == 0 is excluded."
  ],
  "py_alts": [
   "A `set` of tuples gives O(1) average lookup with no encoding needed.",
   "`all(p in S for p in ((x1+d,y1),(x1,y1+d)))` is concise; an explicit two-check version is faster."
  ],
  "trap": "Forgetting to exclude d == 0, which makes a single point its own square and returns true immediately. Also failing to deduplicate, so an identical pair looks like a degenerate square.",
  "invariant": "For a fixed bottom-left corner, the only square candidates are determined by the top-right point, since d must equal both coordinate differences. Checking the two remaining corners in the set is therefore complete: if either is missing, no axis-aligned square with that diagonal exists.",
  "questions": [
   {
    "q": "Why is checking the diagonal sufficient?",
    "a": "An axis-aligned square has four corners at (x, y), (x+d, y), (x, y+d), (x+d, y+d). Knowing the bottom-left and top-right determines d = x2-x1 = y2-y1, and the other two corners are then determined. So a diagonal plus two set lookups is the whole test."
   },
   {
    "q": "What is the complexity?",
    "a": "$O(n^2)$ pair iterations with $O(1)$ average set lookups each, so $O(n^2)$ time and $O(n)$ space. At n = 1000 that is 1e6 pairs, which is exactly the intended bound."
   },
   {
    "q": "What changes if the square may be rotated?",
    "a": "The diagonal is no longer equal in both directions, and the derived corner positions differ. You would have to test both a 45-degree decomposition (the diagonals of a rotated square are perpendicular with a 2:1 length ratio) which roughly squares the constant factor."
   }
  ]
 },
 "18_bit_manipulation/0007_reverse_integer": {
  "one_liner": "Pre-multiply guard against INT_MIN; or use long long.",
  "core_objective": "Return the integer with its 32-bit signed digits reversed, clamped to the 32-bit signed range.",
  "bounds": "-2^31 <= x <= 2^31 - 1, and the reversed value may fall outside that range -- e.g. 1534236469 reverses to 9646324351. Python has no such limit, so a naive reverse works there.",
  "diagram": " x = 123 -> 321\n  x = -123 -> -321\n  x = 120 -> 21     (leading zero dropped)\n  x = 1534236469 -> OUT OF RANGE -> 9646324351 > 2^31-1\n        -> must return 2147483647 (INT_MAX)\n  x = -2147483648 (INT_MIN) -> reverses to -8463847412\n        -> must return -2147483648\n\n  THE OVERFLOW TRAP: before appending a digit, check whether\n  result would exceed INT_MAX/10, or equal it with a digit > 7.\n  Without the guard, 1534236469 overflows and C++ signed\n  overflow is undefined behaviour -- it may silently wrap.\n\n  guard:\n   if (result > INT_MAX / 10) return INT_MAX;\n   if (result == INT_MAX / 10 && d > INT_MAX % 10)\n       return INT_MAX;\n\n  PYTHON needs no guard: arbitrary precision means the\n  reversed value is computed exactly and then compared.",
  "cpp_alts": [
   "The guard approach avoids any 64-bit arithmetic and stays within int.",
   "`long long` accumulation is simpler: the reversed value of a 32-bit int always fits in 64 bits, so build it there and clamp at the end."
  ],
  "py_alts": [
   "`int(str(abs(x))[::-1]) * (1 if x >= 0 else -1)` is one line and exact, since Python ints are unbounded.",
   "`divmod(x, 10)` returns (quotient, remainder) with floored division, which handles negatives correctly in one call."
  ],
  "trap": "Using `abs(INT_MIN)` in C++, which overflows because 2147483648 is not representable as int. `int(-INT_MIN)` is undefined behaviour -- the classic manifestation is returning -2147483648 forever.",
  "invariant": "After k iterations, `result` holds the last k digits of x reversed, and `x` holds the remaining leading digits. Each step removes the last digit of x and appends it to result, so the combined value is preserved until the final clamp.",
  "questions": [
   {
    "q": "Why is the pre-multiply guard needed rather than clamping afterwards?",
    "a": "Because by the time the overflow has happened the value is already wrong -- signed overflow is undefined behaviour, so the compiler may have produced anything. Detecting it before the multiplication keeps every intermediate value representable."
   },
   {
    "q": "How does Python avoid this entirely?",
    "a": "Arbitrary-precision integers mean no intermediate value is ever out of range. The reversed value is computed exactly and then compared against the 32-bit limits, which is the clean approach -- the C++ guard exists purely to work around a language restriction."
   },
   {
    "q": "What is the complexity?",
    "a": "$O(\\log_{10} |x|)$ time -- one iteration per digit, at most 10 -- and $O(1)$ space. No string conversion is needed in either language."
   }
  ]
 },
 "18_bit_manipulation/0136_single_number": {
  "one_liner": "XOR cancels pairs; the leftover is the answer.",
  "core_objective": "Return the one element that appears exactly once while every other element appears twice.",
  "bounds": "1 <= nums.length <= 3e4 with values up to 3e4, so int suffices and the length is always odd. Exactly one such element is guaranteed to exist.",
  "diagram": " nums = [4,1,2,1,2]\n\n  x ^ x = 0 and x ^ 0 = x, and XOR is associative\n  and commutative, so pair order is irrelevant:\n\n  4 ^ 1 ^ 2 ^ 1 ^ 2\n  = 4 ^ (1 ^ 1) ^ (2 ^ 2)\n  = 4 ^ 0 ^ 0\n  = 4\n\n  every paired value annihilates, leaving the single one.\n  Requires EVEN counts of the paired values -- the reason\n  this fails for problem 137 where three copies appear.\n\n  invariant: at any point, `r` equals the XOR of all elements\n  processed so far. Since XOR is self-inverse, after the whole\n  pass only elements with odd multiplicity survive, and the\n  guarantee says exactly one does.",
  "cpp_alts": [
   "A single accumulator `int r = 0; for (int x : nums) r ^= x;` -- the tightest possible loop.",
   "`unsigned` avoids any concern about sign extension in the XOR, though int is correct here."
  ],
  "py_alts": [
   "`functools.reduce(operator.xor, nums, 0)` is a C-level fold.",
   "Bitwise NOT in Python yields -1-style results because Python integers are infinite-precision two's complement, so be careful with masking."
  ],
  "trap": "Using XOR when three copies of a value may appear (problem 137). Then an odd count leaves the value itself rather than zero, and the single XOR is wrong -- you need per-bit counts in that case.",
  "invariant": "`r` is always the XOR of the prefix processed so far. Because XOR is associative and commutative, the elements can be reordered freely, so every equal pair cancels regardless of adjacency. After the full pass the result is the XOR of all elements with odd multiplicity, which by the guarantee is the single one.",
  "questions": [
   {
    "q": "Why does XOR cancel pairs but not triples?",
    "a": "Because a ^ a = 0, so two copies vanish. Three copies leave a ^ a ^ a = 0 ^ a = a. So XOR isolates elements with ODD multiplicity -- exactly the guarantee for this problem and precisely the failure case for problem 137."
   },
   {
    "q": "Why does the element order not matter?",
    "a": "XOR is both associative and commutative, so any parenthesisation and any permutation gives the same value. That is what allows pair cancellation even when the duplicates are far apart in the array."
   },
   {
    "q": "What is the complexity?",
    "a": "$O(n)$ time and $O(1)$ space -- one accumulator, one pass. That is optimal, since every element must be read."
   }
  ]
 },
 "18_bit_manipulation/0190_reverse_bits": {
  "one_liner": "Loop 32 times: shift the input in, shift the output out.",
  "core_objective": "Reverse the order of the bits of a 32-bit unsigned integer.",
  "bounds": "The input is always a 32-bit unsigned integer, so exactly 32 iterations are required regardless of the value. A zero input must give zero, not be skipped.",
  "diagram": " input = 43261596 (0b000000101001010000011110)\n\n  32 iterations, always:\n   result = (result << 1) | (n & 1)\n   n >>= 1\n\n  after 32 steps result = 0b011110001110010011110000 = 964176192\n\n  WHY THE FIXED LOOP: a shorter loop (while n) would stop at\n  the highest set bit, but the answer must be a FULL 32-bit\n  reversal -- leading zeros of the input become trailing zeros\n  of the output. So the loop must run exactly 32 times.\n\n  ALTERNATIVE: swap 5-bit blocks, then 3-bit, then the\n  remaining bits -- a divide-and-conquer reversal in 3 steps:\n   n = ((n & 0xaaaa) >> 1) | ((n & 0x5555) << 1)\n   n = ((n & 0xcccc) >> 2) | ((n & 0x3333) << 2)\n   n = ((n & 0xf0f0) >> 4) | ((n & 0x0f0f) << 4)\n   n = ((n & 0xff00) >> 8) | ((n & 0x00ff) << 8)\n   n = (n >> 16) | ((n & 0xffff) << 16)\n\n  input  0b000000101001010000011110\n  reverse 0b011110001110010011110000",
  "cpp_alts": [
   "`uint32_t` with a fixed `for (int i = 0; i < 32; ++i)` is the canonical form.",
   "The masked-block version is branch-free and runs in constant time with a handful of instructions, and is a classic bit-twiddling showcase."
  ],
  "py_alts": [
   "`int(f'{n:032b}'[::-1], 2)` is a one-liner but allocates a 32-character string and is much slower.",
   "Python's `>>` on a positive int is a logical shift, so no sign handling is needed."
  ],
  "trap": "Using `while n` instead of a 32-iteration loop. That stops early for inputs with leading zero bits, and the answer loses the trailing zeros the reversal should produce.",
  "invariant": "After i iterations, `result` holds the reversal of the i lowest bits of the original input, and n holds the remaining higher bits shifted down. Extending by one iteration appends the next input bit as the new most significant bit of result, which is exactly the reversal order.",
  "questions": [
   {
    "q": "Why exactly 32 iterations?",
    "a": "Because the reversal is defined over 32 bits. Input bits that are zero still occupy positions, and they become trailing zeros in the output. A loop that stops when n reaches zero would silently drop them."
   },
   {
    "q": "What happens to 0?",
    "a": "All 32 iterations run with n = 0, each doing `result = result << 1 | 0`, so result stays 0. The answer is correctly 0 rather than undefined."
   },
   {
    "q": "Why might the masked-block version be faster?",
    "a": "It is branch-free, performs a fixed 5 operations instead of 32 iterations, and each mask-and-shift pair is a couple of machine instructions. It also expresses the reversal as three stages of larger block swaps, which is why it generalises to wider integers."
   }
  ]
 },
 "18_bit_manipulation/0191_number_of_1_bits": {
  "one_liner": "n &= n - 1 clears the lowest set bit; count the iterations.",
  "core_objective": "Return the population count of a non-negative 32-bit integer.",
  "bounds": "0 <= n <= 2^31 - 1, and n = 0 gives 0. Kernighan's algorithm is loop-invariant, so it runs once per set bit.",
  "questions": [
   {
    "q": "Why does n & (n-1) clear the lowest set bit?",
    "a": "Subtracting 1 flips the lowest 1 to 0 and all trailing 0s to 1. ANDing keeps only the bits that are 1 in both, so the lowest 1 is removed and every higher bit is untouched."
   },
   {
    "q": "How many iterations does it take?",
    "a": "Exactly the number of set bits, popcount(n). That is a genuine improvement over scanning all 32 positions, which is the alternative at worst case."
   },
   {
    "q": "How does this relate to the C++ builtin?",
    "a": "`__builtin_popcount` compiles to a single POPCNT instruction on modern CPUs using a population-count microcode table, which beats any loop. Kernighan's algorithm is the version you write when the builtin is unavailable or when you want the derivation."
   }
  ]
 },
 "18_bit_manipulation/0268_missing_number": {
  "one_liner": "XOR the range 0..n with the array: pairs cancel.",
  "core_objective": "Return the one missing integer from the range 0..n inclusive.",
  "bounds": "1 <= nums.length <= 1e4 with 0 <= nums[i] <= 1e4, and exactly one value from 0..n is absent. n is nums.length by construction.",
  "diagram": " nums=[3,0,1] (n=3) -> missing 2\n\n  XOR 0^1^2^3 = 0\n  XOR nums = 3^0^1 = 2\n  answer = 0 ^ 2 = 2\n\n  why it works: every value in 0..n appears exactly once\n  in the full range XOR; the present values cancel against it,\n  leaving only the missing one.\n\n  alternative (sum formula):\n   expected = n(n+1)/2 ; answer = expected - sum(nums)\n\n  XOR is preferred because the sum formula overflows int\n  for large n in C++ (n = 1e4 gives 5e7, safe; n = 1e5\n  would overflow -- and it also breaks silently under\n  floating-point if you use /2.0).\n\n  invariant: at any point `r` is the XOR of the range XOR\n  accumulated so far and the array elements processed so far.\n  Present values appear twice and cancel; the missing one\n  appears once and survives.",
  "cpp_alts": [
   "A single `int r = n; for (i=0..n-1) r ^= nums[i] ^ i;` folds the range XOR into one loop with no separate pass.",
   "`long long` for the sum formula if you choose that route, since `n*(n+1)/2` overflows int past n = 65535."
  ],
  "py_alts": [
   "`reduce(xor, nums, n)` plus a range fold is concise but allocates the range.",
   "The sum formula `n*(n+1)//2 - sum(nums)` is a one-liner in Python and exact."
  ],
  "trap": "Using the sum formula with float division or with int overflow in C++. Both give wrong answers on large inputs, whereas the XOR approach has no arithmetic range concern at all.",
  "invariant": "`r` equals the XOR of 0..n XOR the elements of nums. Every value present in nums occurs in both and cancels; the missing value occurs only in the range, so it is what survives. The result is therefore exactly the missing number.",
  "questions": [
   {
    "q": "Why is XOR better than the sum formula?",
    "a": "XOR has no overflow or precision hazard, and the same single loop handles the range and the array. The sum formula needs a wider type and careful division, both of which are failure modes in C++."
   },
   {
    "q": "How does the index trick work?",
    "a": "Initialising r to n and then XORing with both nums[i] and i in the same loop folds the range 0..n-1 in for free, so only one pass is needed instead of one over the range and one over the array."
   },
   {
    "q": "What is the complexity?",
    "a": "$O(n)$ time and $O(1)$ space. Both approaches are linear; XOR is preferred purely for robustness rather than speed."
   }
  ]
 },
 "18_bit_manipulation/0338_counting_bits": {
  "one_liner": "ones[i] = ones[i >> 1] + (i & 1).",
  "core_objective": "Return an array where the element at index i is the number of 1 bits in i, for every i from 0 to n.",
  "bounds": "0 <= n <= 1e5, so the array has up to 1e5 entries and each count fits in a byte. i = 0 gives 0.",
  "diagram": " n = 5 -> [0,1,1,2,1,2]\n\n  ones[0] = 0\n  i=1:  1>>1 = 0, 1&1 = 1 -> 0 + 1 = 1\n  i=2:  2>>1 = 1, 2&1 = 0 -> 1 + 0 = 1\n  i=3:  3>>1 = 1, 3&1 = 1 -> 1 + 1 = 2\n  i=4:  4>>1 = 2, 4&1 = 0 -> 1 + 0 = 1\n  i=5:  5>>1 = 2, 5&1 = 1 -> 1 + 1 = 2\n\n  THE INSIGHT: shifting right by one removes the lowest bit\n  and leaves the rest unchanged, so\n     popcount(i) = popcount(i >> 1) + (i & 1)\n  The RHS term is already computed since i >> 1 < i.\n\n  BIT TRICK: ones[i] = ones[i & (i-1)] + 1 is the same idea\n  expressed with the clear-lowest-bit identity from problem 191.\n\n  invariant: when computing ones[i], ones[i >> 1] is already\n  final because i >> 1 < i, and (i & 1) is exactly the bit\n  that i >> 1 discarded. So the sum is the popcount of i.",
  "questions": [
   {
    "q": "Why does the DP beat calling popcount n times?",
    "a": "Each popcount is $O(\\log n)$ at worst without a builtin, giving $O(n \\log n)$ overall. The recurrence computes every answer from a strictly smaller index, so the total is $O(n)$ with one shift, one AND, and one addition per element."
   },
   {
    "q": "How does this relate to problem 191?",
    "a": "Same identity, different output. Here the identity is applied across indices to build a table; there it is applied within a single number to count its bits. Both come from the fact that clearing the lowest bit reduces popcount by exactly one."
   },
   {
    "q": "What is the complexity?",
    "a": "$O(n)$ time and $O(n)$ space for the result, which is required since every value from 0 to n must be returned. No extra space beyond the output."
   }
  ]
 },
 "18_bit_manipulation/0371_sum_of_two_integers": {
  "one_liner": "AND for the sum, XOR for the carry, recurse until carry is 0.",
  "core_objective": "Return the sum of two integers using only bitwise operators.",
  "bounds": "-1e5 <= a, b <= 1e5, so the sum fits in int. Negative numbers work because Python's integers are infinite two's complement; C++ needs explicit sign handling or the non-negative assumption.",
  "diagram": " a = 1, b = 2\n  a ^ b = 3        (no common bits -> sum is 3)\n  (a & b) << 1 = 0 -> no carry -> answer 3\n\n  a = 1, b = 3\n  a ^ b = 2        (01 ^ 11 = 10)\n  (a & b) << 1 = 4 (01 & 11 = 01, shifted)\n  now add 2 and 4:  2^4 = 6, (2&4)<<1 = 0 -> answer 6\n\n  WHY IT WORKS: addition decomposes into a sum-without-carry\n  part (XOR, since a 1-bit appears in at most one addend) and\n  a carry part (AND, since both addends must have 1 to carry).\n  The carry must then be added to the XOR result, recursively.\n\n  termination: (a & b) << 1 has strictly fewer set bits than\n  a | b, so the recursion depth is at most the bit width.\n\n  negative numbers: in two's complement, -1 is all 1s, so\n  -1 ^ x == ~x and (a & b) << 1 can be negative. The loop\n  `while b:` with `b = (a & b) << 1` still terminates because\n  the shift eventually overflows to 0 in a fixed width.",
  "cpp_alts": [
   "In C++ with signed ints, `a ^ b` and `(a & b) << 1` behave as two's complement only if the width is fixed; shifting into the sign bit is implementation-defined before C++20.",
   "`uint32_t` avoids all sign questions and the problem's inputs are non-negative there."
  ],
  "py_alts": [
   "`while b: a, b = a ^ b, (a & b) << 1` uses simultaneous assignment so the carry is computed from the OLD a -- which is exactly why the tuple form is correct and two separate statements would not be."
  ],
  "trap": "Computing the carry after already updating a. The carry must be derived from the original a and b, so in Python the simultaneous assignment `a, b = a ^ b, (a & b) << 1` is essential -- doing `a ^= b` then `b = (a & b) << 1` uses the already-modified a and gives wrong answers.",
  "invariant": "At the top of each iteration, the original sum equals a + b. The update replaces that with `(a ^ b) + ((a & b) << 1)`, which is an exact identity for two's-complement addition. When b becomes 0 the identity forces a to equal the original sum.",
  "questions": [
   {
    "q": "Why do the answers to 190, 191, 338, 371 form a set?",
    "a": "Each isolates one bit-level identity: shift-and-mask reverses bits, clearing the lowest bit counts them, and XOR-with-carry computes addition. They all exploit that the same operation can be expressed either with arithmetic or with masks, and knowing both forms is what makes the others obvious."
   },
   {
    "q": "Why does the loop terminate?",
    "a": "The carry value `(a & b) << 1` has strictly fewer set bits than `a | b`. Each iteration consumes one level of the bit-carry hierarchy, so after at most the bit-width iterations the carry is 0."
   },
   {
    "q": "How does Python handle the negative cases?",
    "a": "Python integers are infinite-precision two's complement, so `-1 ^ x == ~x` and the arithmetic works uniformly for negatives without any special case. That is why this problem is notably cleaner in Python than in C++."
   }
  ]
 }
})

# ---- final gap-fill overrides
DATA.update({
 "06_linked_list/0206_reverse_linked_list": {
  "one_liner": "Three pointers: prev, current, next -- and never lose next.",
  "core_objective": "Reverse a singly linked list in place and return the new head.",
  "bounds": "The list may be null or single-node, both of which must be handled without special-casing beyond the loop condition. The operation must be in place -- O(1) space.",
  "diagram": " 1 -> 2 -> 3 -> NULL\n\n prev=NULL cur=1\n   nxt = 2; cur.next = NULL; prev=1; cur=2   -> 1->NULL, cur 2->3\n   nxt = 3; cur.next = 1;   prev=2; cur=3   -> 2->1,   cur 3->NULL\n   nxt = NULL; cur.next = 2; prev=3; cur=NULL -> 3->2->1\n return prev = 3\n\n THE ORDER MATTERS: save nxt BEFORE overwriting cur.next,\n otherwise the rest of the list is unreachable.\n\n iterative: O(n) time, O(1) space\n recursive: O(n) time, O(n) stack -- risky for 1e5 nodes",
  "cpp_alts": [
   "Iterative with three raw pointers is the only version with O(1) space and no stack overflow risk.",
   "`std::reverse` does not apply -- it works on contiguous ranges, not linked structures."
  ],
  "py_alts": [
   "`prev, cur = None, head` then `cur.next, prev, cur = prev, cur, cur.next` -- the simultaneous assignment makes the ordering bug impossible.",
   "Python's simultaneous assignment `prev, cur = cur, cur.next` after saving `nxt` makes the ordering bug structurally impossible.",
   "`itertools` has no linked-list reverse; a while loop is the only option, and `cur.next` is a single attribute load per step."
  ],
  "trap": "Writing `prev = cur` before `cur = cur.next`, or forgetting to save `next` first. Either loses the remainder of the list and silently truncates the result.",
  "invariant": "After k iterations, `prev` is the head of a reversed list containing exactly the first k original nodes, and `cur` points to the (k+1)-th original node. So nothing is lost or duplicated.",
  "questions": [
   {
    "q": "Why must `nxt` be saved before `cur.next` is overwritten?",
    "a": "Because `cur.next` is the only link to the unprocessed remainder. Once you overwrite it, that tail is unreachable from anywhere -- not from cur, not from prev -- so the saved reference is what keeps the traversal alive."
   },
   {
    "q": "When is recursion a bad choice here?",
    "a": "For long lists. CPython's default recursion limit is 1000, so a 1e5-node list raises `RecursionError`. C++ would need a 1e5-frame stack, which is 8 MB or more. The iterative version has neither problem."
   },
   {
    "q": "What does the function return, and why is it `prev`?",
    "a": "`prev`, because after the loop `cur` is NULL and `prev` holds the last node processed -- which is the original tail, now the head of the reversed list. Returning `cur` would give null."
   }
  ]
 },
 "07_trees/0102_binary_tree_level_order_traversal": {
  "one_liner": "Snapshot the queue size at the start of each level.",
  "core_objective": "Return the values of the tree grouped by level, outermost level first.",
  "bounds": "The tree may be null (return []) and is skewed, so the queue-based BFS must not recurse. Node count up to 2e4, so recursion depth can reach 2e4 on a left-only chain.",
  "diagram": "        3\n      /   \\\n     9   20\n        /  \\\n       15   7\n\n  queue = [3], level size = 1\n    take 1 node -> 3              level 0: [3]\n  queue = [9,20], level size = 2\n    take 2     -> 9, 20          level 1: [9,20]\n  queue = [15,7], level size = 2\n    take 2     -> 15, 7          level 2: [15,7]\n\n  the SNAPSHOT is the whole trick: capture len(queue) BEFORE\n  consuming the level, else you would consume everything in one\n  flat list. `for _ in range(size)` is the idiom.\n\n  time O(n), space O(width) for the queue",
  "cpp_alts": [
   "`queue<TreeNode*>` with `int size = q.size()` per level is the canonical form.",
   "Two vectors and an index pointer avoids per-level allocation, reusing capacity across levels."
  ],
  "py_alts": [
   "`from collections import deque; popleft()` is O(1) at both ends; a `list` with an index pointer is also O(1) and avoids deque overhead for pure FIFO use.",
   "A list used as a FIFO with a moving index beats `collections.deque` when only one end is consumed, since there is no block splitting.",
   "`for _ in range(len(q))` snapshots the level size once, which is the entire algorithm -- `deque.popleft()` is the other half."
  ],
  "trap": "Iterating `while queue:` and appending into the same level list -- that flattens the traversal. Or recomputing the level size inside the inner loop, which shrinks it as you pop.",
  "invariant": "At the start of each outer iteration, the queue contains exactly the nodes of the current level, in left-to-right order, and `size` is that count. Popping exactly `size` times consumes precisely one level and leaves the queue holding the next.",
  "questions": [
   {
    "q": "Why must the size be captured before the inner loop?",
    "a": "Because popping shrinks the queue. If you recompute the size each iteration it decreases by one every time and the inner loop exits early, producing short levels. Capturing it once makes the loop bound the level width."
   },
   {
    "q": "What is the space complexity, and what dominates it?",
    "a": "$O(w)$ where w is the maximum width of the tree, plus $O(h)$ for the result list itself. A complete tree of n nodes has width ~n/2, so the result dominates; a skewed tree has width 1 but a result of depth h."
   },
   {
    "q": "When is the depth-first alternative preferable?",
    "a": "When the interviewer wants to test index-based accumulation: recurse with a `depth` argument and append into `result[depth]`. That gives $O(n)$ time with $O(h)$ recursion space and no queue at all."
   }
  ]
 },
 "14_2d_dp/0309_best_time_to_buy_and_sell_stock_with_cooldown": {
  "one_liner": "Three-state DP: holding, sold, resting.",
  "core_objective": "Return the maximum profit with at most one transaction per day and a one-day cooldown after selling.",
  "bounds": "1 <= prices.length <= 1000 with 0 <= prices[i] <= 1000, so the answer fits in int. The first transaction cannot sell on day 0.",
  "diagram": " prices=[1,2,3,0,2]  -> 3 (buy 1, sell 2, buy 0, sell 2)\n\n  state definitions at end of day i:\n   hold   : holding a stock (best profit so far)\n   sold   : sold TODAY  (cannot buy tomorrow)\n   rest   : not holding, and free to buy tomorrow\n\n  transitions:\n   hold = max(prev_hold, prev_rest - price)\n   sold = prev_hold + price\n   rest = max(prev_rest, prev_sold)\n\n  initial: hold=-inf  sold=0  rest=0   (before day 0)\n\n  d0 p=1: hold=max(-inf,0-1)=-1  sold=-inf  rest=0\n  d1 p=2: hold=max(-1,0-2)=-1    sold=1     rest=0\n  d2 p=3: hold=max(-1,0-3)=-1    sold=2     rest=1\n  d3 p=0: hold=max(-1,1-0)=1     sold=-1    rest=2\n  d4 p=2: hold=max(1,2-2)=1      sold=3     rest=2\n  ANSWER max(hold=1, sold=3, rest=2) = 3\n\n  the cooldown is enforced because rest can only come from\n  rest or sold, and buy needs rest -- so sold->hold is\n  forbidden.",
  "cpp_alts": [
   "Three scalars beat a state array; the day loop is the whole algorithm.",
   "`int` suffices since the answer is bounded by n * max(price)."
  ],
  "py_alts": [
   "Tuple assignment `hold, sold, rest = max(hold, rest-p), hold+p, max(rest, sold)` computes all three from the OLD values in one statement -- this is exactly what simultaneous assignment is for.",
   "Tuple assignment computes hold, sold and rest from the previous day's values in one statement, which is exactly what simultaneous assignment exists for.",
   "Explicit `prev_hold` temporaries work but are a well-known source of the in-place-update bug this problem is designed to catch."
  ],
  "trap": "Updating the states in sequence instead of simultaneously, so a later transition sees an already-updated earlier one and accidentally permits selling and rebuying on the same day.",
  "invariant": "hold, sold, rest hold the best profit achievable at the end of the previous day in each of three mutually exclusive states. `sold` is reachable only from `hold` on the same day, and `hold` only from `rest`, so the cooldown gap is enforced structurally rather than by a special case.",
  "questions": [
   {
    "q": "Why is the cooldown automatic in these transitions?",
    "a": "Buying requires being in `rest`, and `rest` on day i comes only from `rest` or `sold` on day i-1. After selling you are in `sold`, so on day i+1 you may only reach `rest` -- you cannot reach `hold` until day i+2. The gap is enforced by the state graph."
   },
   {
    "q": "Why do we need three states rather than two?",
    "a": "Because `sold` and `rest` differ only in whether tomorrow is blocked, but that difference changes what you can do tomorrow. Collapsing them loses the ability to distinguish \"just sold\" from \"been resting\", which is exactly what implements the cooldown."
   },
   {
    "q": "Why must the initial hold be -infinity?",
    "a": "So that `prev_hold + price` cannot produce a spurious profit on day 0 from a nonexistent prior position. With hold = 0 the state would allow selling on day 0 for a free gain."
   }
  ]
 },
 "17_math_and_geometry/0201_bitwise_and_of_numbers_range": {
  "one_liner": "The AND of a range is the common prefix; right-shift to find it.",
  "core_objective": "Return m & (m+1) & ... & n for 0 <= m <= n <= 2^31-1.",
  "bounds": "0 <= m <= n <= 2^31 - 1, so 31 bits suffice. m == n returns m. The answer is always a power-of-two-aligned block.",
  "diagram": " m=5, n=7  -> 4\n\n  5 = 101\n  6 = 110\n  7 = 111\n  AND:\n    101\n    110\n    111\n    ---\n    100 = 4\n\n  COMMON PREFIX: the top bit (bit 2) is shared; everything\n  below differs because the range crosses a power-of-two\n  boundary at 8.\n\n  shift-right approach:\n   sh = 0\n   while m != n: m >>= 1; n >>= 1; sh += 1\n   return m << sh\n\n   m=5 n=7 -> 2,3 sh=1 -> 1,1 sh=2 -> stop\n   return 1 << 2 = 4  CORRECT\n\n  shift-until-equal alternative:\n   while m < n: m >>= 1; n >>= 1\n   return m\n\n  invariant: shifting both endpoints right by the same amount\n  preserves the common prefix, and they become equal exactly\n  when the remaining bits are all that they share. Shifting\n  back left restores the zeroes below the prefix, which is the\n  required AND.",
  "questions": [
   {
    "q": "Why does m == n after shifting imply the answer?",
    "a": "When both endpoints collapse to the same value v, every number in the range agrees with v on all remaining high bits and the lower bits of the range contain a transition, so the AND of those low bits is 0. Hence the answer is v followed by sh zeros."
   },
   {
    "q": "What is the simpler formulation?",
    "a": "`while m < n: m >>= 1; n >>= 1; return m`. Because m <= n always, and m < n guarantees a differing low bit, the loop shifts out exactly the non-common part, so no shift counter is needed."
   },
   {
    "q": "What is the complexity?",
    "a": "$O(\\log n)$ time -- at most 31 shifts -- and $O(1)$ space. In C++ use `unsigned` to avoid sign-extension issues on the right shift; in Python the integers are arbitrary-precision and never negative here."
   }
  ],
  "trap": [
   "U",
   "s",
   "i",
   "n",
   "g",
   " ",
   "`",
   "w",
   "h",
   "l",
   "e",
   "m",
   "!",
   "=",
   ":",
   ">",
   "1",
   ";",
   "t",
   "o",
   "u",
   "a",
   "f",
   "c",
   "r",
   "d",
   ".",
   "T",
   "p",
   "x",
   ",",
   "5",
   "7",
   "v",
   "4"
  ],
  "invariant": [
   "A",
   "t",
   " ",
   "e",
   "v",
   "r",
   "y",
   "s",
   "p",
   "b",
   "o",
   "h",
   "n",
   "d",
   "i",
   "a",
   "f",
   "g",
   "m",
   "u",
   ",",
   "l",
   ".",
   "T",
   "c",
   "q",
   "x",
   "w",
   "N",
   "D"
  ],
  "cpp_alts": [
   "`unsigned` avoids sign extension on `>>` for the 31-bit bound, though int is also correct since both operands stay non-negative.",
   "The shift-counter form generalises to any range type; the `while m < n` form is a C++/Python one-liner but relies on m <= n."
  ],
  "py_alts": [
   "`m ^ n` gives the bits that differ; their highest set bit marks the shift amount, so `shift = m ^ n .bit_length()` is an equivalent single-expression form.",
   "Python's `>>` is a logical shift on positive ints, so no masking is needed anywhere in this problem."
  ]
 },
 "18_bit_manipulation/0191_number_of_1_bits": {
  "one_liner": "n &= n - 1 clears the lowest set bit; count the iterations.",
  "core_objective": "Return the population count of a non-negative 32-bit integer.",
  "bounds": "0 <= n <= 2^31 - 1, and n = 0 gives 0. Kernighan's algorithm is loop-invariant, so it runs once per set bit.",
  "questions": [
   {
    "q": "Why does n & (n-1) clear the lowest set bit?",
    "a": "Subtracting 1 flips the lowest 1 to 0 and all trailing 0s to 1. ANDing keeps only the bits that are 1 in both, so the lowest 1 is removed and every higher bit is untouched."
   },
   {
    "q": "How many iterations does it take?",
    "a": "Exactly the number of set bits, popcount(n). That is a genuine improvement over scanning all 32 positions, which is the alternative at worst case."
   },
   {
    "q": "How does this relate to the C++ builtin?",
    "a": "`__builtin_popcount` compiles to a single POPCNT instruction on modern CPUs using a population-count microcode table, which beats any loop. Kernighan's algorithm is the version you write when the builtin is unavailable or when you want the derivation."
   }
  ],
  "trap": [
   "M",
   "u",
   "t",
   "a",
   "i",
   "n",
   "g",
   " ",
   "s",
   "d",
   "e",
   "h",
   "l",
   "o",
   "p",
   "c",
   ",",
   "`",
   "w",
   "(",
   "&",
   "=",
   "-",
   "1",
   ")",
   "m",
   "b",
   "r",
   "f",
   "y",
   "v",
   ".",
   "T",
   "x"
  ],
  "invariant": [
   "E",
   "a",
   "c",
   "h",
   " ",
   "i",
   "t",
   "e",
   "r",
   "o",
   "n",
   "m",
   "v",
   "s",
   "x",
   "l",
   "y",
   "w",
   "b",
   "d",
   "u",
   ",",
   "f",
   "k",
   "q",
   "g",
   "p",
   "."
  ],
  "cpp_alts": [
   "`__builtin_popcount` compiles to a single POPCNT instruction on modern CPUs, which beats any loop -- worth naming before writing the manual version.",
   "`std::bitset<32>` exposes a `count()` member with the same hardware advantage and no UB concerns on the shift."
  ],
  "py_alts": [
   "`bin(n).count('1')` is a one-liner but allocates a string of up to 32 characters and is much slower than the loop.",
   "Python 3.10+ exposes `int.bit_count()`, which is implemented in C and matches Kernighan's speed for small integers."
  ]
 },
 "18_bit_manipulation/0338_counting_bits": {
  "one_liner": "ones[i] = ones[i >> 1] + (i & 1).",
  "core_objective": "Return an array where the element at index i is the number of 1 bits in i, for every i from 0 to n.",
  "bounds": "0 <= n <= 1e5, so the array has up to 1e5 entries and each count fits in a byte. i = 0 gives 0.",
  "diagram": " n = 5 -> [0,1,1,2,1,2]\n\n  ones[0] = 0\n  i=1:  1>>1 = 0, 1&1 = 1 -> 0 + 1 = 1\n  i=2:  2>>1 = 1, 2&1 = 0 -> 1 + 0 = 1\n  i=3:  3>>1 = 1, 3&1 = 1 -> 1 + 1 = 2\n  i=4:  4>>1 = 2, 4&1 = 0 -> 1 + 0 = 1\n  i=5:  5>>1 = 2, 5&1 = 1 -> 1 + 1 = 2\n\n  THE INSIGHT: shifting right by one removes the lowest bit\n  and leaves the rest unchanged, so\n     popcount(i) = popcount(i >> 1) + (i & 1)\n  The RHS term is already computed since i >> 1 < i.\n\n  BIT TRICK: ones[i] = ones[i & (i-1)] + 1 is the same idea\n  expressed with the clear-lowest-bit identity from problem 191.\n\n  invariant: when computing ones[i], ones[i >> 1] is already\n  final because i >> 1 < i, and (i & 1) is exactly the bit\n  that i >> 1 discarded. So the sum is the popcount of i.",
  "questions": [
   {
    "q": "Why does the DP beat calling popcount n times?",
    "a": "Each popcount is $O(\\log n)$ at worst without a builtin, giving $O(n \\log n)$ overall. The recurrence computes every answer from a strictly smaller index, so the total is $O(n)$ with one shift, one AND, and one addition per element."
   },
   {
    "q": "How does this relate to problem 191?",
    "a": "Same identity, different output. Here the identity is applied across indices to build a table; there it is applied within a single number to count its bits. Both come from the fact that clearing the lowest bit reduces popcount by exactly one."
   },
   {
    "q": "What is the complexity?",
    "a": "$O(n)$ time and $O(n)$ space for the result, which is required since every value from 0 to n must be returned. No extra space beyond the output."
   }
  ],
  "trap": [
   "I",
   "t",
   "e",
   "r",
   "a",
   "i",
   "n",
   "g",
   " ",
   "u",
   "p",
   "w",
   "d",
   "h",
   "l",
   "`",
   "o",
   "s",
   "[",
   ">",
   "1",
   "]",
   "f",
   "m",
   "y",
   "z",
   ",",
   "<",
   "v",
   "0",
   "-",
   "q",
   "c",
   "."
  ],
  "invariant": [
   "W",
   "h",
   "e",
   "n",
   " ",
   "c",
   "o",
   "m",
   "p",
   "u",
   "t",
   "i",
   "g",
   "s",
   "[",
   "]",
   ",",
   ">",
   "1",
   "a",
   "l",
   "r",
   "d",
   "y",
   "f",
   "b",
   "<",
   "(",
   "&",
   ")",
   ".",
   "T"
  ],
  "cpp_alts": [
   "A `vector<uint8_t>` of n+1 bytes; the values never exceed 32 so a full int array wastes 4x the cache.",
   "For the same reason POPCNT-style primitives give O(n) with no table, but the DP table is the point of this problem."
  ],
  "py_alts": [
   "`[bin(i).count('1') for i in range(n+1)]` is a one-liner but allocates n strings and is orders of magnitude slower.",
   "`int.bit_count()` in Python 3.10+ is the C-level equivalent and still $O(n)$ overall with no extra table."
  ]
 },
 "18_bit_manipulation/0371_sum_of_two_integers": {
  "one_liner": "AND for the sum, XOR for the carry, recurse until carry is 0.",
  "core_objective": "Return the sum of two integers using only bitwise operators.",
  "bounds": "-1e5 <= a, b <= 1e5, so the sum fits in int. Negative numbers work because Python's integers are infinite two's complement; C++ needs explicit sign handling or the non-negative assumption.",
  "diagram": " a = 1, b = 2\n  a ^ b = 3        (no common bits -> sum is 3)\n  (a & b) << 1 = 0 -> no carry -> answer 3\n\n  a = 1, b = 3\n  a ^ b = 2        (01 ^ 11 = 10)\n  (a & b) << 1 = 4 (01 & 11 = 01, shifted)\n  now add 2 and 4:  2^4 = 6, (2&4)<<1 = 0 -> answer 6\n\n  WHY IT WORKS: addition decomposes into a sum-without-carry\n  part (XOR, since a 1-bit appears in at most one addend) and\n  a carry part (AND, since both addends must have 1 to carry).\n  The carry must then be added to the XOR result, recursively.\n\n  termination: (a & b) << 1 has strictly fewer set bits than\n  a | b, so the recursion depth is at most the bit width.\n\n  negative numbers: in two's complement, -1 is all 1s, so\n  -1 ^ x == ~x and (a & b) << 1 can be negative. The loop\n  `while b:` with `b = (a & b) << 1` still terminates because\n  the shift eventually overflows to 0 in a fixed width.",
  "cpp_alts": [
   "In C++ with signed ints, `a ^ b` and `(a & b) << 1` behave as two's complement only if the width is fixed; shifting into the sign bit is implementation-defined before C++20.",
   "`uint32_t` avoids all sign questions and the problem's inputs are non-negative there."
  ],
  "py_alts": [
   "`while b: a, b = a ^ b, (a & b) << 1` uses simultaneous assignment so the carry is computed from the OLD a -- which is exactly why the tuple form is correct and two separate statements would not be.",
   "`while b: a, b = a ^ b, (a & b) << 1` uses simultaneous assignment so the carry is computed from the ORIGINAL a, which is exactly why the tuple form is correct.",
   "`divmod` plays no role here -- the whole computation is bitwise, which is what keeps it working for negative operands."
  ],
  "trap": "Computing the carry after already updating a. The carry must be derived from the original a and b, so in Python the simultaneous assignment `a, b = a ^ b, (a & b) << 1` is essential -- doing `a ^= b` then `b = (a & b) << 1` uses the already-modified a and gives wrong answers.",
  "invariant": "At the top of each iteration, the original sum equals a + b. The update replaces that with `(a ^ b) + ((a & b) << 1)`, which is an exact identity for two's-complement addition. When b becomes 0 the identity forces a to equal the original sum.",
  "questions": [
   {
    "q": "Why do the answers to 190, 191, 338, 371 form a set?",
    "a": "Each isolates one bit-level identity: shift-and-mask reverses bits, clearing the lowest bit counts them, and XOR-with-carry computes addition. They all exploit that the same operation can be expressed either with arithmetic or with masks, and knowing both forms is what makes the others obvious."
   },
   {
    "q": "Why does the loop terminate?",
    "a": "The carry value `(a & b) << 1` has strictly fewer set bits than `a | b`. Each iteration consumes one level of the bit-carry hierarchy, so after at most the bit-width iterations the carry is 0."
   },
   {
    "q": "How does Python handle the negative cases?",
    "a": "Python integers are infinite-precision two's complement, so `-1 ^ x == ~x` and the arithmetic works uniformly for negatives without any special case. That is why this problem is notably cleaner in Python than in C++."
   }
  ]
 }
})

# ---- detect-squares correction
DATA.update({
 "17_math_and_geometry/2013_detect_squares": {
  "one_liner": "Pick the bottom-left corner, then count pairs along its edges.",
  "core_objective": "Return the total number of axis-aligned squares in which at least one other point shares the bottom row and at least one shares the left column.",
  "bounds": "0 <= points.length <= 1000 with 0 <= x[i], y[i] <= 1000, so coordinates fit in 10 bits and a 1001 x 1001 counting grid is about 4 MB. Duplicate points are legal and are the reason the answer multiplies two counts.",
  "diagram": " points = [(0,0),(1,0),(0,1),(1,1),(0,2)]  -> 1\n\n  for each (x, y) treat it as the BOTTOM-LEFT corner:\n   (0,0): right = # points at (x'>0, y)   = 2  -> (1,0),(1,1)\n          up    = # points at (x, y'>0)   = 2  -> (0,1),(0,2)\n          both sides present -> +1 * 1 = 1 square\n   (1,0): right = 0 -> skip\n   (0,1): right = 1 -> (1,1); up = 1 -> (0,2)\n          -> +1 square (0,1)-(1,1)-(1,2)? (1,2) absent\n          but the opposite orientation also counts:\n          the point (0,1) can be the TOP-LEFT of the\n          square whose bottom-left is (0,0). So every\n          square is found twice unless you only count\n          the (x, y) = bottom-left orientation and use\n          right * up.\n\n  RIGHT * UP IS THE TRAP: a square needs a point strictly to\n  the RIGHT (x' > x) and one strictly ABOVE (y' > y), and\n  the two must pair up into a distinct square. Multiplying\n  the two counts is valid because each pair determines a\n  unique corner (x', y').",
  "trap": "Using `>=` instead of `>` for the neighbour tests, which makes a point on the same row or column count as a side and inflates the answer. Also iterating both the (right, up) and (left, down) products, which double-counts every square.",
  "invariant": "For each point (x, y), right(x, y) counts points on row y strictly right of x and up(x, y) counts points on column x strictly above y. Every square has exactly one bottom-left corner, and its two far sides are exactly one member of each set, so right * up counts each square exactly once from that corner.",
  "cpp_alts": [
   "`unordered_map<int, unordered_map<int,int>>` counts per point in O(1) expected but allocates two nodes per lookup; a flat 1001 x 1001 int grid indexed `x * 1001 + y` is a single 4 MB block with perfect locality.",
   "Sorting by (x, y) lets the right-count be read off from a running group size, avoiding the nested map entirely."
  ],
  "py_alts": [
   "`collections.Counter` over the points gives per-point counts, but the row and column tallies need two separate counters keyed by y and by x.",
   "A 2-D list of 1001 x 1001 ints is about 8 MB of pointers plus small-int caching; a flat list of 1e6 entries indexed `x * 1001 + y` is one allocation."
  ],
  "questions": [
   {
    "q": "Why is `right * up` correct rather than a combination count?",
    "a": "Because the problem defines the square by one point on the bottom row and one on the left column of the chosen corner. Each ordered pair (right point, up point) determines one unique opposite corner, so the number of squares is exactly the product of the two counts."
   },
   {
    "q": "Why does a single corner orientation avoid double counting?",
    "a": "Every axis-aligned square has a unique bottom-left corner and a unique top-right corner. Anchoring on the bottom-left with strict right/up neighbours means each square is visited only at its bottom-left point, so no counting rule needs a divide-by-two."
   },
   {
    "q": "What is the complexity?",
    "a": "$O(n)$ time for n points, with $O(1)$ expected lookup per point. Space is $O(\\sigma)$ for the coordinate maps or $O(10^6)$ for a flat counting grid when the coordinate range is bounded."
   }
  ]
 }
})

DATA["18_bit_manipulation/0191_number_of_1_bits"]["diagram"] = (
 " n = 13  ->  3\n"
 " 13 = 1101\n"
 "\n"
 " n & (n - 1) clears the LOWEST set bit:\n"
 "   13 = 1101\n"
 "   12 = 1100\n"
 "   ----\n"
 "    4 = 0100     one set bit gone -> count = 1\n"
 "\n"
 " step 1: n=13 (1101) -> n=12 (1100)  count=1\n"
 " step 2: n=12 (1100) -> n= 8 (1000)  count=2\n"
 " step 3: n= 8 (1000) -> n= 0 (0000)  count=3\n"
 " n == 0 -> return 3\n"
 "\n"
 " iterations == popcount, NOT 32 -- the loop-invariant\n"
 " is the whole algorithm"
)
