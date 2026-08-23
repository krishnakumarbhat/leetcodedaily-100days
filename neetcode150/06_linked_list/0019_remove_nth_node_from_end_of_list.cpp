/*
 * =====================================================================
 * LeetCode 19 : Remove Nth Node From End of List               (Medium)
 * https://leetcode.com/problems/remove-nth-node-from-end-of-list/
 * Category   : Linked List
 * ---------------------------------------------------------------------
 * PROBLEM
 *   Given the head of a list and n, remove the n-th node COUNTING
 *   FROM THE END (1-indexed) and return the head. The list is singly
 *   linked — there are no back pointers to locate the tail cheaply.
 *       1→2→3→4→5, n=2  →  1→2→3→5
 * ---------------------------------------------------------------------
 * INTUITION
 *   "n-th from the end" = "n steps BEFORE the null at the end".
 *   Two pointers hold a measuring stick of length n: if right is
 *   already n steps ahead of left, then when right reaches null,
 *   left is EXACTLY at the node before the victim. Deleting = skip.
 * ---------------------------------------------------------------------
 * APPROACH 1 — One pass: dummy + fixed-gap two pointers (BEST)
 *   dummy → head. right walks n steps ahead of left (they share the
 *   gap). Walk both until right hits null → left->next is the victim;
 *   left->next = left->next->next deletes it. The dummy guarantees
 *   the victim may be the original head without an edge case.
 *   Time  Complexity : O(n)  — one pass.
 *   Space Complexity : O(1)  — two pointers.
 * ---------------------------------------------------------------------
 * APPROACH 2 — Two passes: count, then delete
 *   Pass 1 counts L nodes (O(L)). The victim is the (L − n + 1)-th
 *   node from the start; walk to its predecessor (L − n steps from
 *   head) and skip it. Needs the dummy for the n == L case too.
 *   Time  Complexity : O(n)  — but two passes.
 *   Space Complexity : O(1).
 * ---------------------------------------------------------------------
 * DEEP DIVE — deleting a node = pointer surgery
 *   A singly linked list can only delete a node if you can SEE its
 *   predecessor — that is why we stop at left->next, never at the
 *   victim itself. The one tricky case is deleting the head (no
 *   predecessor exists): the dummy node makes the head a normal
 *   node with a normal predecessor. This "dummy absorbs the edge
 *   case" idea is the same trick that powers 0021 (merge) and
 *   0025 (reverse k-group). Memory hygiene note: in a real runtime
 *   you also free the skipped node (we do, then rebuild from test
 *   data). Two-pointer gap windows appear in real systems: network
 *   ring buffers keep a read pointer exactly K bytes behind a write
 *   pointer, i.e. "the n-from-the-end element".
 * =====================================================================
 */

#include <vector>          // std::vector — test data
#include <chrono>          // std::chrono — timing
#include <iostream>        // std::cout — output
#include <sys/resource.h>  // getrusage — peak RAM
#include "list_node.h"     // our header: ListNode, buildList

/* =====================================================================
 * APPROACH 1 : One pass with a dummy node + fixed-gap pointers
 * ===================================================================== */
class Solution_OnePass {
public:
    /*
     * Purpose : Delete the n-th node from the end in a single walk.
     * Inputs  : head — first node of the list; n — 1-indexed distance
     *                  from the end (guaranteed ≤ list length).
     * Output  : Head of the list with the target node removed.
     */
    ListNode* removeNthFromEnd(ListNode* head, int n) {
        // Dummy so the original head can be deleted like any node.
        ListNode* dummy = new ListNode(0, head);
        ListNode* left = dummy;
        ListNode* right = dummy;

        // Stretch the measuring stick: right jumps n steps first.
        for (int i = 0; i < n; ++i) {
            right = right->next;
        }

        // Slide the stick: gap stays n; when right is at null,
        // left sits exactly at the node BEFORE the victim.
        while (right->next != nullptr) {
            left = left->next;
            right = right->next;
        }

        // Pointer surgery: skip the victim (and free it).
        ListNode* victim = left->next;
        left->next = victim->next;      // bridge over the deleted node
        delete victim;                  // return its memory

        ListNode* newHead = dummy->next;
        delete dummy;                   // scaffold goes away
        return newHead;
    }
};

/* =====================================================================
 * APPROACH 2 : Two passes — count the length, then delete
 * ===================================================================== */
class Solution_TwoPass {
public:
    /*
     * Purpose : Delete the n-th node from the end using two walks.
     * Inputs  : head — first node of the list; n — 1-indexed distance
     *                  from the end.
     * Output  : Head of the list with the target node removed.
     */
    ListNode* removeNthFromEnd(ListNode* head, int n) {
        // Pass 1: measure the total length L.
        int length = 0;
        for (ListNode* cur = head; cur != nullptr; cur = cur->next) {
            ++length;
        }

        // Victim from the start is (L − n + 1); we need its
        // predecessor, i.e. the (L − n)-th node. Dummy handles n == L.
        ListNode* dummy = new ListNode(0, head);
        ListNode* cur = dummy;
        for (int i = 0; i < length - n; ++i) {
            cur = cur->next;            // walk to the predecessor
        }

        ListNode* victim = cur->next;
        cur->next = victim->next;       // bridge over it
        delete victim;

        ListNode* newHead = dummy->next;
        delete dummy;
        return newHead;
    }
};

/* =====================================================================
 * BENCHMARK — 3 tests, both approaches, time + peak RAM
 * ===================================================================== */
int main() {
    std::vector<std::vector<int>> vals = {{1, 2, 3, 4, 5}, {1}, {1, 2}};
    std::vector<int> n = {2, 1, 2};
    std::vector<std::vector<int>> exp = {{1, 2, 3, 5}, {}, {2}};

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
        ListNode* out = Solution_OnePass().removeNthFromEnd(head, n[t]);
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
        ListNode* out = Solution_TwoPass().removeNthFromEnd(head, n[t]);
        ok2 = verify(out, t) && ok2;
        deleteList(out);
    }
    auto e2 = std::chrono::high_resolution_clock::now();
    getrusage(RUSAGE_SELF, &r2b);

    double us1 = std::chrono::duration_cast<std::chrono::nanoseconds>(e1 - s1).count() / 1000.0;
    double us2 = std::chrono::duration_cast<std::chrono::nanoseconds>(e2 - s2).count() / 1000.0;
    long kb1 = (r1b.ru_maxrss - r1a.ru_maxrss) / 1024;
    long kb2 = (r2b.ru_maxrss - r2a.ru_maxrss) / 1024;

    std::cout << "0019 Remove Nth Node From End of List\n";
    std::cout << "Approach 1 (one pass) : time = " << us1 << " µs  peak-ram-delta = " << kb1 << " KB\n";
    std::cout << "Approach 2 (two pass) : time = " << us2 << " µs  peak-ram-delta = " << kb2 << " KB\n";
    std::cout << (ok1 && ok2 ? "PASS : both approaches removed the right node on all 3 tests."
                             : "FAIL : at least one test produced a wrong list.")
              << "\n";
    return 0;
}
