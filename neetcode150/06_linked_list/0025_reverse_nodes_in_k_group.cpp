/*
 * =====================================================================
 * LeetCode 25 : Reverse Nodes in k-Group                        (Hard)
 * https://leetcode.com/problems/reverse-nodes-in-k-group/
 * Category   : Linked List
 * ---------------------------------------------------------------------
 * PROBLEM
 *   Reverse the nodes of a list k AT A TIME. The leftover tail
 *   (fewer than k nodes) stays as it is. Reverse the direction of
 *   every group's arrows — the grouping itself never changes.
 *       1→2→3→4→5, k=2  →  2→1→4→3→5
 *       1→2→3→4→5, k=3  →  3→2→1→4→5
 * ---------------------------------------------------------------------
 * INTUITION
 *   Cut the list into k-node blocks. Each block is reversed with the
 *   EXACT prev/cur flip from 0206, but the block boundaries must be
 *   sewn back together: block_start->next = next_block_head, and the
 *   previous block's tail must point at this block's NEW head. A
 *   dummy node carries the pointer to the very first group's new head.
 * ---------------------------------------------------------------------
 * APPROACH 1 — Iterative with dummy + group cursor (BEST)
 *   dummy → head; cursor = dummy. Loop: peek k nodes ahead; if
 *   fewer than k remain, stop (leftover tail untouched). Otherwise
 *   reverse the k nodes right after cursor using the standard flip,
 *   then reattach: cursor->next->next = next_group (sew tail), and
 *   cursor->next = new_group_head. cursor jumps to the block's old
 *   head (now its tail).
 *   Time  Complexity : O(n)  — each node flipped exactly once.
 *   Space Complexity : O(1)  — pointers only.
 * ---------------------------------------------------------------------
 * APPROACH 2 — Recursive per group
 *   Reverse the first k nodes (they become the group's new head);
 *   recurse on the REMAINDER of the list, which returns the next
 *   group's reversed head; sew  tail_of_this_group->next = that.
 *   Base case: fewer than k nodes remain → return as-is.
 *   Time  Complexity : O(n)   Space Complexity : O(n/k) stack.
 * ---------------------------------------------------------------------
 * DEEP DIVE — reversing a BOUNDED segment between two fixed points
 *   Iterative k-group reversal is the "between markers" version of
 *   the flip: instead of flipping until null, flip exactly k nodes.
 *   The three anchors are:
 *       cursor  — node before the segment (never moves while
 *                 reversing inside);
 *       oldHead = cursor->next (first node of the segment, becomes
 *                 the segment's TAIL);
 *       prev/cur — the standard 0206 sliders doing the flips.
 *   After k flips, cur points at the next segment's first node, and
 *   oldHead's ->next must be set to it (sewing the chain back).
 *   This "reverse exactly K between anchors" pattern is the same
 *   one used by doubly-linked-page list manipulation and by
 *   block-wise transforms in databases. Get the anchor invariants
 *   right here and 0206/0143/0025 become one skill.
 * =====================================================================
 */

#include <vector>          // std::vector — test data
#include <chrono>          // std::chrono — timing
#include <iostream>        // std::cout — output
#include <sys/resource.h>  // getrusage — peak RAM
#include "list_node.h"     // our header: ListNode, buildList

/* =====================================================================
 * APPROACH 1 : Iterative — dummy head + anchored segment flips
 * ===================================================================== */
class Solution_Iterative {
public:
    /*
     * Purpose : Reverse the list in groups of exactly k nodes.
     * Inputs  : head — first node of the list; k — group size ≥ 1.
     * Output  : Head of the regrouped list (leftover tail unmodified).
     */
    ListNode* reverseKGroup(ListNode* head, int k) {
        // Dummy lets the FIRST group's new head be sewn in uniformly.
        ListNode* dummy = new ListNode(0, head);
        ListNode* cursor = dummy;   // node just BEFORE the current group

        while (true) {
            // Peek: does a full k-node group remain after cursor?
            ListNode* probe = cursor;
            for (int i = 0; i < k; ++i) {
                probe = probe->next;
                if (probe == nullptr) {
                    // Fewer than k nodes left → leftover tail stays.
                    ListNode* result = dummy->next;
                    delete dummy;
                    return result;
                }
            }

            // Segment anchors: oldHead is first of the group and will
            // end up as its TAIL after the reversal.
            ListNode* oldHead = cursor->next;
            ListNode* prev = cursor;      // flip target starts at cursor
            ListNode* cur = cursor->next; // node to flip first

            // Flip exactly k nodes (the 0206 flip, bounded).
            for (int i = 0; i < k; ++i) {
                ListNode* nxt = cur->next;  // CACHE successor
                cur->next = prev;           // flip the arrow
                prev = cur;                 // slide
                cur = nxt;
            }

            // Sewing: oldHead (now group tail) must point at the next
            // group's first node; cursor (before the group) points at
            // the group's NEW head (prev).
            oldHead->next = cur;
            cursor->next = prev;

            cursor = oldHead;  // next group starts right after oldHead
        }
    }
};

/* =====================================================================
 * APPROACH 2 : Recursive — reverse first group, recurse on the rest
 * ===================================================================== */
class Solution_Recursive {
public:
    /*
     * Purpose : Reverse the list in groups of exactly k nodes.
     * Inputs  : head — first node of the list; k — group size ≥ 1.
     * Output  : Head of the regrouped list.
     * Note    : O(n/k) recursion depth.
     */
    ListNode* reverseKGroup(ListNode* head, int k) {
        // Probe: are there k nodes from here?
        ListNode* probe = head;
        for (int i = 0; i < k; ++i) {
            if (probe == nullptr) {
                return head;   // fewer than k → this tail stays as-is
            }
            probe = probe->next;
        }

        // Reverse exactly k nodes (bounded 0206 flip).
        ListNode* prev = nullptr;
        ListNode* cur = head;
        for (int i = 0; i < k; ++i) {
            ListNode* nxt = cur->next;
            cur->next = prev;
            prev = cur;
            cur = nxt;
        }

        // head is now this group's TAIL → it must point at the
        // next group's reversed head (computed recursively).
        head->next = reverseKGroup(cur, k);
        return prev;   // new head of this group
    }
};

/* =====================================================================
 * BENCHMARK — 3 tests, both approaches, time + peak RAM
 * ===================================================================== */
int main() {
    std::vector<std::vector<int>> vals = {{1, 2, 3, 4, 5}, {1, 2, 3, 4, 5}, {1, 2}};
    std::vector<int> k = {2, 3, 2};
    std::vector<std::vector<int>> exp = {{2, 1, 4, 3, 5}, {3, 2, 1, 4, 5}, {2, 1}};

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
        ListNode* out = Solution_Iterative().reverseKGroup(head, k[t]);
        ok1 = verify(out, t) && ok1;
        deleteList(out);
    }
    auto e1 = std::chrono::high_resolution_clock::now();
    getrusage(RUSAGE_SELF, &r1b);

    // ---- Approach 2 ----
    struct rusage r2a, r2b;
    getrusage(RUSAGE_SELF, &r2a);
    auto s2 = std::chrono::high_resolution_clock::now();
    for (std::size_t t = 0; t < vals.size(); ++t) {
        ListNode* head = buildList(vals[t]);
        ListNode* out = Solution_Recursive().reverseKGroup(head, k[t]);
        ok2 = verify(out, t) && ok2;
        deleteList(out);
    }
    auto e2 = std::chrono::high_resolution_clock::now();
    getrusage(RUSAGE_SELF, &r2b);

    double us1 = std::chrono::duration_cast<std::chrono::nanoseconds>(e1 - s1).count() / 1000.0;
    double us2 = std::chrono::duration_cast<std::chrono::nanoseconds>(e2 - s2).count() / 1000.0;
    long kb1 = (r1b.ru_maxrss - r1a.ru_maxrss) / 1024;
    long kb2 = (r2b.ru_maxrss - r2a.ru_maxrss) / 1024;

    std::cout << "0025 Reverse Nodes in k-Group\n";
    std::cout << "Approach 1 (iterative) : time = " << us1 << " µs  peak-ram-delta = " << kb1 << " KB\n";
    std::cout << "Approach 2 (recursive) : time = " << us2 << " µs  peak-ram-delta = " << kb2 << " KB\n";
    std::cout << (ok1 && ok2 ? "PASS : both approaches regrouped all 3 tests correctly."
                             : "FAIL : at least one test produced a wrong list.")
              << "\n";
    return 0;
}
