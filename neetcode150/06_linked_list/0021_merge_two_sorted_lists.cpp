/*
 * =====================================================================
 * LeetCode 21 : Merge Two Sorted Lists                            (Easy)
 * https://leetcode.com/problems/merge-two-sorted-lists/
 * Category   : Linked List
 * ---------------------------------------------------------------------
 * PROBLEM
 *   Given the heads of two SORTED linked lists, merge them into ONE
 *   sorted list. Return the merged head. Example:
 *       1→2→4   merged with   1→3→4   gives   1→1→2→3→4→4
 * ---------------------------------------------------------------------
 * INTUITION
 *   Both lists are already sorted, so the smallest remaining node is
 *   ALWAYS the smaller of the two heads. Repeatedly peel off that
 *   smaller head and append it to a result chain — that is a merge,
 *   not a re-sort: O(n) total, no comparisons re-done.
 * ---------------------------------------------------------------------
 * APPROACH 1 — Iterative with a DUMMY node (BEST)
 *   dummy = sentinel before the result head (never special-cases the
 *   very first append). While both lists are alive, attach the smaller
 *   head to tail. Then attach whatever list still has nodes (the "tail
 *   leftover" shortcut — no need to copy, just splice the pointer).
 *   Time  Complexity : O(n + m) — each node visited once.
 *   Space Complexity : O(1)     — only pointers.
 * ---------------------------------------------------------------------
 * APPROACH 2 — Recursive
 *   If one list is empty, the other IS the answer (base case).
 *   Otherwise the smaller head leads; its ->next = merge(its tail,
 *   the other list). Merge work is spread over the call stack.
 *   Time  Complexity : O(n + m).
 *   Space Complexity : O(n + m) — recursion depth.
 * ---------------------------------------------------------------------
 * DEEP DIVE — the dummy-node trick
 *   Building a result chain with `tail = tail->next` demands an
 *   initial tail. Without a dummy you must write `if (head==nullptr)
 *   head = node; else tail->next = node;` on EVERY append — a
 *   branch paid O(n) times. The dummy removes the branch:
 *       dummy = new Node;  tail = dummy;  append always via tail->next
 *   list_node.h's buildList, every insert-at-front solution, and
 *   problem 0025 (reverse k-group) all rely on this trick. The dummy
 *   is scaffolding: discard it at the end (delete) and return
 *   dummy->next. Real-world: kernel linked lists (struct list_head)
 *   embed sentinel heads exactly like this.
 * =====================================================================
 */

#include <vector>          // std::vector — test data
#include <chrono>          // std::chrono — timing
#include <iostream>        // std::cout — output
#include <sys/resource.h>  // getrusage — peak RAM
#include "list_node.h"     // our header: ListNode, buildList, printList

/* =====================================================================
 * APPROACH 1 : Iterative merge with a dummy head
 * ===================================================================== */
class Solution_DummyNode {
public:
    /*
     * Purpose : Merge two sorted lists into one sorted list, in place.
     * Inputs  : l1, l2 — heads of two ascending singly linked lists.
     * Output  : Head of the merged ascending list (O(1) extra space).
     */
    ListNode* mergeTwoLists(ListNode* l1, ListNode* l2) {
        // Dummy sentinel: tail->next is where the next node goes.
        // Removing the "is this the first node?" branch on every append.
        ListNode* dummy = new ListNode(0);
        ListNode* tail = dummy;

        // Both lists still have nodes → pick the smaller head.
        while (l1 != nullptr && l2 != nullptr) {
            if (l1->val <= l2->val) {
                tail->next = l1;   // l1's head wins this round
                l1 = l1->next;     // advance only l1
            } else {
                tail->next = l2;   // l2's head wins
                l2 = l2->next;
            }
            tail = tail->next;     // result chain grows by one
        }

        // The leftover shortcut: whichever list remains is already
        // sorted and already a chain — splice the whole pointer.
        tail->next = (l1 != nullptr) ? l1 : l2;

        ListNode* head = dummy->next;  // first REAL node
        delete dummy;                  // scaffold goes away
        return head;
    }
};

/* =====================================================================
 * APPROACH 2 : Recursive — merge work distributed on the stack
 * ===================================================================== */
class Solution_Recursive {
public:
    /*
     * Purpose : Merge two sorted lists recursively.
     * Inputs  : l1, l2 — heads of two ascending singly linked lists.
     * Output  : Head of the merged ascending list.
     * Note    : O(n + m) time, O(n + m) recursion stack space.
     */
    ListNode* mergeTwoLists(ListNode* l1, ListNode* l2) {
        // Base case: an empty list is trivially merged — the other
        // list, fully intact, IS the result.
        if (l1 == nullptr) return l2;
        if (l2 == nullptr) return l1;

        // The smaller head leads the merged list; its tail is merged
        // with the OTHER list by the recursive call.
        if (l1->val <= l2->val) {
            l1->next = mergeTwoLists(l1->next, l2);
            return l1;
        }
        l2->next = mergeTwoLists(l1, l2->next);
        return l2;
    }
};

/* =====================================================================
 * BENCHMARK — 3 tests, both approaches, time + peak RAM
 * ===================================================================== */
int main() {
    // (list A, list B, expected merged values)
    std::vector<std::vector<int>> a = {{1, 2, 4}, {}, {5}};
    std::vector<std::vector<int>> b = {{1, 3, 4}, {1, 2}, {}};
    std::vector<std::vector<int>> exp = {{1, 1, 2, 3, 4, 4}, {1, 2}, {5}};

    auto verify = [&](ListNode* merged, std::size_t t) {
        // Walk merged and compare against the expected values.
        for (int want : exp[t]) {
            if (merged == nullptr || merged->val != want) return false;
            merged = merged->next;
        }
        return merged == nullptr;   // no leftover nodes either
    };

    bool ok1 = true, ok2 = true;

    // ---- Approach 1 ----
    struct rusage m1a, m1b;
    getrusage(RUSAGE_SELF, &m1a);
    auto s1 = std::chrono::high_resolution_clock::now();
    for (std::size_t t = 0; t < a.size(); ++t) {
        ListNode* l1 = buildList(a[t]);
        ListNode* l2 = buildList(b[t]);
        ListNode* merged = Solution_DummyNode().mergeTwoLists(l1, l2);
        ok1 = verify(merged, t) && ok1;
        deleteList(merged);  // merged reuses l1/l2 nodes — one free pass
    }
    auto e1 = std::chrono::high_resolution_clock::now();
    getrusage(RUSAGE_SELF, &m1b);

    // ---- Approach 2 ----
    struct rusage m2a, m2b;
    getrusage(RUSAGE_SELF, &m2a);
    auto s2 = std::chrono::high_resolution_clock::now();
    for (std::size_t t = 0; t < a.size(); ++t) {
        ListNode* l1 = buildList(a[t]);
        ListNode* l2 = buildList(b[t]);
        ListNode* merged = Solution_Recursive().mergeTwoLists(l1, l2);
        ok2 = verify(merged, t) && ok2;
        deleteList(merged);
    }
    auto e2 = std::chrono::high_resolution_clock::now();
    getrusage(RUSAGE_SELF, &m2b);

    double us1 = std::chrono::duration_cast<std::chrono::nanoseconds>(e1 - s1).count() / 1000.0;
    double us2 = std::chrono::duration_cast<std::chrono::nanoseconds>(e2 - s2).count() / 1000.0;
    long kb1 = (m1b.ru_maxrss - m1a.ru_maxrss) / 1024;
    long kb2 = (m2b.ru_maxrss - m2a.ru_maxrss) / 1024;

    std::cout << "0021 Merge Two Sorted Lists\n";
    std::cout << "Approach 1 (dummy node) : time = " << us1 << " µs  peak-ram-delta = " << kb1 << " KB\n";
    std::cout << "Approach 2 (recursive)  : time = " << us2 << " µs  peak-ram-delta = " << kb2 << " KB\n";
    std::cout << (ok1 && ok2 ? "PASS : both approaches merged all 3 tests correctly."
                             : "FAIL : at least one test produced a wrong list.")
              << "\n";
    return 0;
}
