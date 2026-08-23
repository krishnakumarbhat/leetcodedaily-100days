/*
 * =====================================================================
 * LeetCode 141 : Linked List Cycle                                (Easy)
 * https://leetcode.com/problems/linked-list-cycle/
 * Category   : Linked List
 * ---------------------------------------------------------------------
 * PROBLEM
 *   Given the head of a linked list, determine whether the list has a
 *   CYCLE (some node's next pointer points back into the list). A
 *   cycle means: walking next forever would never reach null.
 * ---------------------------------------------------------------------
 * INTUITION
 *   Two runners on a circular track ALWAYS meet: if one runs twice as
 *   fast as the other, the gap between them shrinks by one lap-step
 *   per unit time until they collide. In a straight corridor they can
 *   never meet (fast one hits the wall first). So: two pointers, one
 *   jumping 1 node at a time, one jumping 2 — collision ⇔ cycle.
 *   This is FLOYD'S CYCLE DETECTION (the tortoise and the hare).
 * ---------------------------------------------------------------------
 * APPROACH 1 — Floyd's fast/slow pointers (BEST)
 *   slow = head, fast = head->next (or both at head; the standard
 *   variant). Loop: slow += 1 step, fast += 2 steps. If they ever
 *   point at the SAME node → cycle. If fast hits null → no cycle.
 *   Time  Complexity : O(n)  — at most 2n steps before collision.
 *   Space Complexity : O(1)  — two pointers only.
 * ---------------------------------------------------------------------
 * APPROACH 2 — Hash set of visited nodes
 *   Walk the list, inserting every node pointer into a set. The first
 *   pointer seen twice is the cycle's entrance → return true. No
 *   cycle ⇔ we reach null.
 *   Time  Complexity : O(n)   Space Complexity : O(n) — the set.
 * ---------------------------------------------------------------------
 * DEEP DIVE — Floyd's math (fast = 2 × slow)
 *   Suppose the tail has length a and the cycle has length L. When
 *   slow enters the cycle (at distance a), fast is already somewhere
 *   inside it — at most L−1 steps ahead. Each round closes the gap by
 *   exactly 1 (fast gains 1 step per time unit), so they meet within
 *   L steps. Meeting inside a cycle PROVES a cycle exists; if there
 *   were none, fast would hit null in a straight run.
 *   Entry-point bonus (problem 0287 uses this): after the first
 *   meeting, move one pointer back to head and advance BOTH by 1 —
 *   they meet at the cycle entrance. Distance math: slow walked a+m,
 *   fast walked 2(a+m) = a + kL + m (k laps) ⇒ a ≡ 0 mod (L − …) ⇒
 *   head-to-entry distance equals meeting-to-entry distance mod L.
 *   Real world: checkpoints / version graphs / linked allocators all
 *   detect loops with this O(1)-space trick when a visited-set is too
 *   expensive. Git's fsck uses cycle detection on object graphs.
 * =====================================================================
 */

#include <vector>           // std::vector — test data
#include <unordered_set>    // std::unordered_set — approach 2's visited set
#include <chrono>           // std::chrono — timing
#include <iostream>         // std::cout — output
#include <sys/resource.h>   // getrusage — peak RAM
#include "list_node.h"      // our header: ListNode, buildList

/* =====================================================================
 * APPROACH 1 : Floyd's tortoise and hare — O(1) space
 * ===================================================================== */
class Solution_Floyd {
public:
    /*
     * Purpose : Detect a cycle with two pointers moving at 1× and 2×.
     * Inputs  : head — first node of the list (may be nullptr).
     * Output  : true if the list contains a cycle, false otherwise.
     */
    bool hasCycle(ListNode* head) {
        // Both start at head: fast just takes two hops per round.
        ListNode* slow = head;
        ListNode* fast = head;

        // fast->next check first: if fast is about to run off the end
        // (or already did), the list is a straight corridor → no cycle.
        while (fast != nullptr && fast->next != nullptr) {
            slow = slow->next;        // tortoise: 1 hop
            fast = fast->next->next;  // hare:     2 hops

            // Same node → the hare lapped the tortoise inside a loop.
            if (slow == fast) {
                return true;
            }
        }
        // We fell off the end of the list — it is acyclic.
        return false;
    }
};

/* =====================================================================
 * APPROACH 2 : Hash set of visited node addresses
 * ===================================================================== */
class Solution_HashSet {
public:
    /*
     * Purpose : Detect a cycle by remembering every visited address.
     * Inputs  : head — first node of the list (may be nullptr).
     * Output  : true if the list contains a cycle, false otherwise.
     */
    bool hasCycle(ListNode* head) {
        // Set of POINTER VALUES (memory addresses) we already walked.
        std::unordered_set<ListNode*> seen;

        // Walk the chain; null = straight list ends → no cycle.
        for (ListNode* cur = head; cur != nullptr; cur = cur->next) {
            // Address already visited → some node points back → cycle.
            if (seen.find(cur) != seen.end()) {
                return true;
            }
            seen.insert(cur);
        }
        return false;
    }
};

/* =====================================================================
 * BENCHMARK — 4 tests (incl. cycle cases), time + peak RAM
 * ===================================================================== */
int main() {
    // Test vectors + expected verdicts. Cycle is expressed as the
    // position whose node the LAST node points back at (-1 = no cycle).
    std::vector<std::vector<int>> vals = {{3, 2, 0, -4}, {1, 2}, {1}, {}};
    std::vector<int> cyclePos = {1, 0, -1, -1};   // pos index or -1
    std::vector<bool> expected = {true, true, false, false};

    auto makeList = [&](std::size_t t) {
        // Build the list, then wire the tail into the requested node.
        ListNode* head = buildList(vals[t]);
        if (cyclePos[t] >= 0) {
            ListNode* entry = head;
            for (int i = 0; i < cyclePos[t]; ++i) entry = entry->next;
            // Walk to the tail and close the loop.
            ListNode* tail = head;
            while (tail->next != nullptr) tail = tail->next;
            tail->next = entry;   // THE CYCLE
        }
        return head;
    };

    bool ok1 = true, ok2 = true;

    // ---- Approach 1 ----
    struct rusage r1a, r1b;
    getrusage(RUSAGE_SELF, &r1a);
    auto s1 = std::chrono::high_resolution_clock::now();
    for (std::size_t t = 0; t < vals.size(); ++t) {
        ListNode* head = makeList(t);
        bool got = Solution_Floyd().hasCycle(head);
        ok1 = (got == expected[t]) && ok1;
        // Cycles self-own their nodes: break the cycle before deleting.
        if (cyclePos[t] >= 0) {
            // Simple cleanup: walk to entry, null it, then deleteList.
            ListNode* entry = head;
            for (int i = 0; i < cyclePos[t]; ++i) entry = entry->next;
            ListNode* tail = head;
            while (tail->next != entry) tail = tail->next;
            tail->next = nullptr;
        }
        deleteList(head);
    }
    auto e1 = std::chrono::high_resolution_clock::now();
    getrusage(RUSAGE_SELF, &r1b);

    // ---- Approach 2 ----
    struct rusage r2a, r2b;
    getrusage(RUSAGE_SELF, &r2a);
    auto s2 = std::chrono::high_resolution_clock::now();
    for (std::size_t t = 0; t < vals.size(); ++t) {
        ListNode* head = makeList(t);
        bool got = Solution_HashSet().hasCycle(head);
        ok2 = (got == expected[t]) && ok2;
        if (cyclePos[t] >= 0) {
            ListNode* entry = head;
            for (int i = 0; i < cyclePos[t]; ++i) entry = entry->next;
            ListNode* tail = head;
            while (tail->next != entry) tail = tail->next;
            tail->next = nullptr;
        }
        deleteList(head);
    }
    auto e2 = std::chrono::high_resolution_clock::now();
    getrusage(RUSAGE_SELF, &r2b);

    double us1 = std::chrono::duration_cast<std::chrono::nanoseconds>(e1 - s1).count() / 1000.0;
    double us2 = std::chrono::duration_cast<std::chrono::nanoseconds>(e2 - s2).count() / 1000.0;
    long kb1 = (r1b.ru_maxrss - r1a.ru_maxrss) / 1024;
    long kb2 = (r2b.ru_maxrss - r2a.ru_maxrss) / 1024;

    std::cout << "0141 Linked List Cycle\n";
    std::cout << "Approach 1 (Floyd 2-ptr) : time = " << us1 << " µs  peak-ram-delta = " << kb1 << " KB\n";
    std::cout << "Approach 2 (hash set)    : time = " << us2 << " µs  peak-ram-delta = " << kb2 << " KB\n";
    std::cout << (ok1 && ok2 ? "PASS : both approaches detected cycles on all 4 tests."
                             : "FAIL : at least one test returned the wrong verdict.")
              << "\n";
    return 0;
}
