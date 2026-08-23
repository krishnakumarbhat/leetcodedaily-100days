/*
 * =====================================================================
 * LeetCode 287 : Find the Duplicate Number                     (Medium)
 * https://leetcode.com/problems/find-the-duplicate-number/
 * Category   : Linked List
 * ---------------------------------------------------------------------
 * PROBLEM
 *   nums has n+1 integers, each in [1, n]. Exactly ONE value repeats
 *   (at least twice); every other value appears once. Find the
 *   duplicate WITHOUT modifying nums, using O(1) EXTRA space.
 * ---------------------------------------------------------------------
 * INTUITION
 *   Think of the array as a FUNCTION f(i) = nums[i]. Chasing values
 *   — index i, then nums[i], then nums[nums[i]] — walks a linked
 *   list of indices. Since some value appears twice, two different
 *   indices point at the SAME value: the walk must eventually cycle,
 *   and the cycle ENTRY is the duplicated value. This is Floyd's
 *   cycle detection (0141) applied to an implicit linked list — the
 *   same section skill, a new skin.
 * ---------------------------------------------------------------------
 * APPROACH 1 — Floyd's tortoise and hare on the array (BEST)
 *   slow = nums[slow], fast = nums[nums[fast]] until they meet (a
 *   cycle is guaranteed). Then walk slow and a fresh pointer from 0
 *   at equal speed — they meet exactly at the cycle entry = answer.
 *   Time  Complexity : O(n)  — O(n) to meet, O(n) to find the entry.
 *   Space Complexity : O(1)  — three pointers.
 * ---------------------------------------------------------------------
 * APPROACH 2 — Hash set of seen values
 *   Insert every value into a set; the first repeat is the answer.
 *   Time  Complexity : O(n).   Space Complexity : O(n) — the set.
 * ---------------------------------------------------------------------
 * DEEP DIVE — Floyd's math: why the entry is the duplicate
 *   The index walk i → nums[i] is a FUNCTION on {0..n}, so its
 *   picture is disjoint chains feeding into cycles (a functional
 *   graph). Because values live in [1, n] and there are n+1 of
 *   them, at least one value is the "head" of two chains — which
 *   forces a cycle, and the cycle's ENTRY is the duplicated value.
 *   Entry distance: after the first meeting, moving one pointer back
 *   to index 0 and advancing BOTH one step at a time makes them
 *   meet at the cycle entry — because the tail length a satisfies
 *   a ≡ (distance from meeting point to entry) (mod cycle length).
 *   The same argument proves the 0141 entry-point trick; the
 *   hash map h(k, i) = (hash(k)+i) mod m analogy: here the "hash"
 *   is the array itself — the array IS the hash table, and the
 *   cycle-entry lookup finds the duplicate without one extra byte.
 * =====================================================================
 */

#include <vector>           // std::vector — the array
#include <unordered_set>    // std::unordered_set — approach 2
#include <chrono>           // std::chrono — timing
#include <iostream>         // std::cout — output
#include <sys/resource.h>   // getrusage — peak RAM
#include "list_node.h"      // our header: the array models a linked
                            // list (index i → "node" nums[i]), so the
                            // whole section shares one mental model

/* =====================================================================
 * APPROACH 1 : Floyd's tortoise and hare on the index graph
 * ===================================================================== */
class Solution_Floyd {
public:
    /*
     * Purpose : Find the duplicated value in O(1) extra space.
     * Inputs  : nums — n+1 values in [1, n], exactly one duplicate.
     * Output  : The duplicated value.
     */
    int findDuplicate(const std::vector<int>& nums) {
        // Phase 1 — DETECT the cycle. slow takes 1 step (one array
        // hop), fast takes 2. A cycle exists, so they MUST meet.
        int slow = 0;
        int fast = 0;
        do {
            slow = nums[slow];          // 1 hop: i → nums[i]
            fast = nums[nums[fast]];    // 2 hops
        } while (slow != fast);

        // Phase 2 — FIND the cycle entry. From the meeting point and
        // from index 0, advance at EQUAL speed: they collide exactly
        // at the entry, and the entry value is the duplicate.
        int slow2 = 0;
        while (slow != slow2) {
            slow = nums[slow];
            slow2 = nums[slow2];
        }
        return slow;
    }
};

/* =====================================================================
 * APPROACH 2 : Hash set of seen values
 * ===================================================================== */
class Solution_HashSet {
public:
    /*
     * Purpose : Find the duplicated value with a hash set.
     * Inputs  : nums — n+1 values in [1, n], exactly one duplicate.
     * Output  : The duplicated value.
     */
    int findDuplicate(const std::vector<int>& nums) {
        std::unordered_set<int> seen;
        for (int v : nums) {
            if (seen.find(v) != seen.end()) {
                return v;   // second sighting → the duplicate
            }
            seen.insert(v);
        }
        return -1;   // unreachable per problem statement
    }
};

/* =====================================================================
 * BENCHMARK — 3 tests, both approaches, time + peak RAM
 * ===================================================================== */
int main() {
    std::vector<std::vector<int>> tests = {
        {1, 3, 4, 2, 2},     // official example 1 → 2
        {3, 1, 3, 4, 2},     // official example 2 → 3
        {3, 3, 3, 3, 3}      // all duplicates → 3
    };
    std::vector<int> expected = {2, 3, 3};

    bool ok1 = true, ok2 = true;

    // ---- Approach 1 ----
    struct rusage r1a, r1b;
    getrusage(RUSAGE_SELF, &r1a);
    auto s1 = std::chrono::high_resolution_clock::now();
    for (std::size_t t = 0; t < tests.size(); ++t) {
        int got = Solution_Floyd().findDuplicate(tests[t]);
        ok1 = (got == expected[t]) && ok1;
    }
    auto e1 = std::chrono::high_resolution_clock::now();
    getrusage(RUSAGE_SELF, &r1b);

    // ---- Approach 2 ----
    struct rusage r2a, r2b;
    getrusage(RUSAGE_SELF, &r2a);
    auto s2 = std::chrono::high_resolution_clock::now();
    for (std::size_t t = 0; t < tests.size(); ++t) {
        int got = Solution_HashSet().findDuplicate(tests[t]);
        ok2 = (got == expected[t]) && ok2;
    }
    auto e2 = std::chrono::high_resolution_clock::now();
    getrusage(RUSAGE_SELF, &r2b);

    double us1 = std::chrono::duration_cast<std::chrono::nanoseconds>(e1 - s1).count() / 1000.0;
    double us2 = std::chrono::duration_cast<std::chrono::nanoseconds>(e2 - s2).count() / 1000.0;
    long kb1 = (r1b.ru_maxrss - r1a.ru_maxrss) / 1024;
    long kb2 = (r2b.ru_maxrss - r2a.ru_maxrss) / 1024;

    std::cout << "0287 Find the Duplicate Number\n";
    std::cout << "Approach 1 (Floyd)   : time = " << us1 << " µs  peak-ram-delta = " << kb1 << " KB\n";
    std::cout << "Approach 2 (hash set) : time = " << us2 << " µs  peak-ram-delta = " << kb2 << " KB\n";
    std::cout << (ok1 && ok2 ? "PASS : both approaches found the duplicate on all 3 tests."
                             : "FAIL : at least one test returned the wrong value.")
              << "\n";
    return 0;
}
