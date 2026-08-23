/*
 * =====================================================================
 * LeetCode 143 : Reorder List                                   (Medium)
 * https://leetcode.com/problems/reorder-list/
 * Category   : Linked List
 * ---------------------------------------------------------------------
 * PROBLEM
 *   Reorder  L0→L1→…→Ln−1→Ln  into  L0→Ln→L1→Ln−1→L2→…  in place
 *   (only the pointers change, no new nodes).
 *       1→2→3→4  →  1→4→2→3       1→2→3→4→5 → 1→5→2→4→3
 * ---------------------------------------------------------------------
 * INTUITION
 *   The target order pulls alternately from the front and the back.
 *   A singly linked list cannot walk BACKWARD, so: split the list in
 *   half, REVERSE the second half (0206's algorithm), then weave the
 *   two halves front→back. Three known micro-algorithms chained.
 * ---------------------------------------------------------------------
 * APPROACH 1 — Split + reverse + weave, three-pointer hunt (BEST)
 *   (a) FIND MIDDLE with the fast/slow technique: slow walks 1 step,
 *       fast 2 steps → when fast ends, slow is the middle.
 *   (b) REVERSE the second half (prev/cur flip from 0206).
 *   (c) WEAVE: repeatedly take one node from each half and relink
 *       them head → tail → next-head → next-tail → …
 *   Time  Complexity : O(n)  — three linear passes total.
 *   Space Complexity : O(1)  — pointers only.
 * ---------------------------------------------------------------------
 * APPROACH 2 — Straighten into a vector, then weave
 *   Collect every node pointer into an array (O(n) extra space),
 *   then walk l from 0 and r from n−1 inward, relinking l→r.
 *   Time  Complexity : O(n).   Space Complexity : O(n) — the array.
 * ---------------------------------------------------------------------
 * DEEP DIVE — the fast/slow middle finder
 *   slow starts at head, fast at head->next (variant) or head. Each
 *   round: slow += 1, fast += 2. Because fast moves twice as fast,
 *   when fast reaches the end, slow has covered HALF the distance —
 *   the middle (for even length: the first of the two middles, which
 *   is the correct split point here). Same speed-ratio trick as
 *   Floyd's cycle detection (0141) — one math idea, two problems.
 *   The weave loop reads cur1->next BEFORE overwriting it:
 *   `ListNode* next1 = cur1->next;` — the cache-first discipline
 *   from 0206 applied again.
 * =====================================================================
 */

#include <vector>           // std::vector — test data + approach 2
#include <chrono>           // std::chrono — timing
#include <iostream>         // std::cout — output
#include <sys/resource.h>   // getrusage — peak RAM
#include "list_node.h"      // our header: ListNode, buildList

/* =====================================================================
 * APPROACH 1 : Split at middle (fast/slow) + reverse + weave
 * ===================================================================== */
class Solution_SplitReverseWeave {
public:
    /*
     * Purpose : Reorder L0→L1→…→Ln into L0→Ln→L1→Ln−1→… in place.
     * Inputs  : head — first node of the list to reorder.
     * Output  : Returns nothing; the input list is reordered in place.
     */
    void reorderList(ListNode* head) {
        if (head == nullptr || head->next == nullptr) {
            return;   // 0 or 1 node: nothing to reorder
        }

        // (a) Find the middle with fast/slow. fast does 2 hops per
        // slow hop, so when fast can go no further, slow is centered.
        ListNode* slow = head;
        ListNode* fast = head->next;
        while (fast != nullptr && fast->next != nullptr) {
            slow = slow->next;
            fast = fast->next->next;
        }

        // (b) Reverse the SECOND half starting at slow->next, using
        // the 0206 flip: save, flip, slide.
        ListNode* prev = nullptr;
        ListNode* cur = slow->next;
        slow->next = nullptr;         // sever the halves!
        while (cur != nullptr) {
            ListNode* nxt = cur->next;
            cur->next = prev;
            prev = cur;
            cur = nxt;
        }
        ListNode* second = prev;      // new head of the reversed half

        // (c) Weave: take one from the first half, one from the
        // second, alternately. second is ≤ first in length, so
        // second runs out first — loop while it lives.
        ListNode* first = head;
        while (second != nullptr) {
            ListNode* next1 = first->next;   // CACHE first's survivor
            ListNode* next2 = second->next;  // CACHE second's survivor
            first->next = second;            // first → second
            second->next = next1;            // second → rest of first
            first = next1;                   // advance both
            second = next2;
        }
    }
};

/* =====================================================================
 * APPROACH 2 : Flatten to a vector of pointers, then weave
 * ===================================================================== */
class Solution_VectorWeave {
public:
    /*
     * Purpose : Reorder the list using an auxiliary array of nodes.
     * Inputs  : head — first node of the list to reorder.
     * Output  : Returns nothing; the input list is reordered in place.
     * Note    : Simpler logic, but O(n) extra memory.
     */
    void reorderList(ListNode* head) {
        if (head == nullptr || head->next == nullptr) {
            return;
        }

        // Collect every node pointer into a contiguous array.
        std::vector<ListNode*> nodes;
        for (ListNode* cur = head; cur != nullptr; cur = cur->next) {
            nodes.push_back(cur);
        }

        // Weave with two indices marching inward.
        int l = 0;
        int r = static_cast<int>(nodes.size()) - 1;
        while (l < r) {
            nodes[l]->next = nodes[r];   // left node → right node
            ++l;
            // Stop before creating a self-loop on odd counts:
            // when l == r the middle node must point at null.
            if (l == r) {
                nodes[r]->next = nullptr;
                break;
            }
            nodes[r]->next = nodes[l];   // right node → next left
            --r;
        }
        nodes[r]->next = nullptr;        // last node closes the chain
    }
};

/* =====================================================================
 * BENCHMARK — 3 tests, both approaches, time + peak RAM
 * ===================================================================== */
int main() {
    std::vector<std::vector<int>> vals = {{1, 2, 3, 4}, {1, 2, 3, 4, 5}, {1}};
    std::vector<std::vector<int>> exp = {{1, 4, 2, 3}, {1, 5, 2, 4, 3}, {1}};

    auto verify = [&](ListNode* h, std::size_t t) {
        for (int want : exp[t]) {
            if (h == nullptr || h->val != want) return false;
            h = h->next;
        }
        return h == nullptr;
    };

    bool ok1 = true, ok2 = true;

    // ---- Approach 1 ----
    struct rusage r1a, r1b;
    getrusage(RUSAGE_SELF, &r1a);
    auto s1 = std::chrono::high_resolution_clock::now();
    for (std::size_t t = 0; t < vals.size(); ++t) {
        ListNode* head = buildList(vals[t]);
        Solution_SplitReverseWeave().reorderList(head);
        ok1 = verify(head, t) && ok1;
        deleteList(head);
    }
    auto e1 = std::chrono::high_resolution_clock::now();
    getrusage(RUSAGE_SELF, &r1b);

    // ---- Approach 2 ----
    struct rusage r2a, r2b;
    getrusage(RUSAGE_SELF, &r2a);
    auto s2 = std::chrono::high_resolution_clock::now();
    for (std::size_t t = 0; t < vals.size(); ++t) {
        ListNode* head = buildList(vals[t]);
        Solution_VectorWeave().reorderList(head);
        ok2 = verify(head, t) && ok2;
        deleteList(head);
    }
    auto e2 = std::chrono::high_resolution_clock::now();
    getrusage(RUSAGE_SELF, &r2b);

    double us1 = std::chrono::duration_cast<std::chrono::nanoseconds>(e1 - s1).count() / 1000.0;
    double us2 = std::chrono::duration_cast<std::chrono::nanoseconds>(e2 - s2).count() / 1000.0;
    long kb1 = (r1b.ru_maxrss - r1a.ru_maxrss) / 1024;
    long kb2 = (r2b.ru_maxrss - r2a.ru_maxrss) / 1024;

    std::cout << "0143 Reorder List\n";
    std::cout << "Approach 1 (split+reverse+weave) : time = " << us1 << " µs  peak-ram-delta = " << kb1 << " KB\n";
    std::cout << "Approach 2 (vector weave)         : time = " << us2 << " µs  peak-ram-delta = " << kb2 << " KB\n";
    std::cout << (ok1 && ok2 ? "PASS : both approaches reordered all 3 tests correctly."
                             : "FAIL : at least one test produced a wrong order.")
              << "\n";
    return 0;
}
