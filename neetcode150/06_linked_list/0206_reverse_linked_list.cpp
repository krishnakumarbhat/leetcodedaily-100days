/*
 * =====================================================================
 * LeetCode 206 : Reverse Linked List                             (Easy)
 * https://leetcode.com/problems/reverse-linked-list/
 * Category   : Linked List
 * ---------------------------------------------------------------------
 * PROBLEM
 *   Given the head of a singly linked list, reverse the list and
 *   return the new head. The chain is  n0 → n1 → n2 → … → nk  and
 *   must become  nk → … → n2 → n1 → n0.
 * ---------------------------------------------------------------------
 * INTUITION
 *   To reverse a chain you must rewrite every node's `next` pointer
 *   to point at its PREVIOUS node. The only hard part is that
 *   overwriting cur->next destroys the rest of the chain — so you
 *   must CACHE the successor before the flip. That single insight
 *   (save-next, flip, slide) is the whole algorithm.
 * ---------------------------------------------------------------------
 * APPROACH 1 — Iterative (3 pointers) (BEST)
 *   prev = nullptr, cur = head. Loop: nxt = cur->next (save the
 *   survivor), cur->next = prev (flip the arrow), prev = cur,
 *   cur = nxt (slide forward). When cur hits null, prev IS the new
 *   head. Every arrow is flipped exactly once.
 *   Time  Complexity : O(n)  — every node visited once.
 *   Space Complexity : O(1)  — three pointers, no extra memory.
 * ---------------------------------------------------------------------
 * APPROACH 2 — Recursive
 *   Reverse the tail  head->next…  FIRST (recursion), which returns
 *   the new head; then wire  head->next->next = head  (the old tail
 *   now points back) and  head->next = nullptr. The recursion stack
 *   does the "remember the successor" job for us.
 *   Time  Complexity : O(n)  — one call per node.
 *   Space Complexity : O(n)  — recursion stack depth n.
 * ---------------------------------------------------------------------
 * DEEP DIVE — pointer-chasing fundamentals
 *   This problem teaches the THREE pointer-chasing patterns that the
 *   whole section builds on:
 *   (1) THE CACHE: any time you overwrite a pointer you are pointing
 *       at (cur->next), copy it out first — otherwise the data behind
 *       it becomes unreachable (a leak in real programs).
 *   (2) THE DUMMY NODE: an extra sentinel head makes edge cases
 *       (empty list, single node, inserting at position 0) disappear
 *       — main() in list_node.h uses the same trick.
 *   (3) THE SLIDE: advancing prev/cur/nxt together keeps all needed
 *       context reachable with O(1) memory.
 *   Real-world: linked lists survive as LRU caches (0146), hash-map
 *   buckets (separate chaining), and intrusive memory allocators —
 *   every one of them rewrites next pointers exactly like this.
 * =====================================================================
 */

#include <vector>          // std::vector — test data containers
#include <chrono>          // std::chrono — high-resolution timing
#include <iostream>        // std::cout — printing benchmark results
#include <sys/resource.h>  // getrusage — peak-RAM measurement
#include "list_node.h"     // OUR header: ListNode + buildList + printList
                           // (quotes = look in THIS folder first)

/* =====================================================================
 * APPROACH 1 : Iterative with 3 sliding pointers
 * ===================================================================== */
class Solution_Iterative {
public:
    /*
     * Purpose : Reverse a linked list in place using O(1) extra memory.
     * Inputs  : head — first node of the list to reverse.
     * Output  : Pointer to the NEW head (the old last node).
     */
    ListNode* reverseList(ListNode* head) {
        // prev = already-reversed part; starts at null (new list's end).
        ListNode* prev = nullptr;
        // cur = the node we are about to flip right now.
        ListNode* cur = head;

        // Keep going until we walk off the end of the chain.
        while (cur != nullptr) {
            // THE CACHE: save the successor BEFORE overwriting ->next,
            // otherwise the rest of the list is lost.
            ListNode* nxt = cur->next;

            // THE FLIP: this node must now point at its previous one.
            cur->next = prev;

            // THE SLIDE: move both pointers one step forward.
            prev = cur;
            cur = nxt;
        }

        // cur fell off the list → prev is the node that WAS the tail,
        // i.e. the head of the reversed list.
        return prev;
    }
};

/* =====================================================================
 * APPROACH 2 : Recursive — let the call stack remember the successor
 * ===================================================================== */
class Solution_Recursive {
public:
    /*
     * Purpose : Reverse a linked list recursively (head → new head).
     * Inputs  : head — first node of the list (or sub-list) to reverse.
     * Output  : Pointer to the NEW head of the reversed sub-list.
     * Note    : Same O(n) time as iterative but O(n) stack space.
     */
    ListNode* reverseList(ListNode* head) {
        // Base case: empty list or single node → already "reversed".
        if (head == nullptr || head->next == nullptr) {
            return head;
        }

        // Reverse the TAIL first. The result is the new head of the
        // whole list and must be returned all the way up unchanged.
        ListNode* newHead = reverseList(head->next);

        // Wiring step: the node AFTER head (old tail of this sub-list)
        // must now point BACK at head — one arrow flip.
        head->next->next = head;
        // head becomes the new tail of the sub-list.
        head->next = nullptr;

        return newHead;
    }
};

/* =====================================================================
 * BENCHMARK — run both approaches on 3 tests, verify + time + RAM
 * ===================================================================== */
int main() {
    // Three test cases: normal, single node, empty list.
    std::vector<std::vector<int>> tests = {
        {1, 2, 3, 4, 5},   // classic 5-node reverse
        {7},               // single node → unchanged
        {}                 // empty list → null head
    };

    // True answer per test, computed independently by reversal.
    std::vector<std::vector<int>> expected = {
        {5, 4, 3, 2, 1},
        {7},
        {}
    };

    bool allPass = true;

    // ---- Approach 1: time + peak-RAM delta ----
    struct rusage r1a, r1b;
    getrusage(RUSAGE_SELF, &r1a);                       // RAM before
    auto t1a = std::chrono::high_resolution_clock::now();
    bool ok1 = true;
    for (std::size_t t = 0; t < tests.size(); ++t) {
        ListNode* head = buildList(tests[t]);           // fresh input
        ListNode* rev = Solution_Iterative().reverseList(head);
        // Verify by walking the reversed list against `expected`.
        for (int want : expected[t]) {
            if (rev == nullptr || rev->val != want) { ok1 = false; break; }
            rev = rev->next;
        }
        if (rev != nullptr) ok1 = false;                // too many nodes
        deleteList(head);                               // free memory
    }
    auto t1b = std::chrono::high_resolution_clock::now();
    getrusage(RUSAGE_SELF, &r1b);                       // RAM after

    double us1 = std::chrono::duration_cast<std::chrono::nanoseconds>(t1b - t1a).count() / 1000.0;
    long kb1 = (r1b.ru_maxrss - r1a.ru_maxrss) / 1024;  // KB delta
    allPass = allPass && ok1;

    // ---- Approach 2: same harness, recursive class ----
    struct rusage r2a, r2b;
    getrusage(RUSAGE_SELF, &r2a);
    auto t2a = std::chrono::high_resolution_clock::now();
    bool ok2 = true;
    for (std::size_t t = 0; t < tests.size(); ++t) {
        ListNode* head = buildList(tests[t]);
        ListNode* rev = Solution_Recursive().reverseList(head);
        for (int want : expected[t]) {
            if (rev == nullptr || rev->val != want) { ok2 = false; break; }
            rev = rev->next;
        }
        if (rev != nullptr) ok2 = false;
        deleteList(head);
    }
    auto t2b = std::chrono::high_resolution_clock::now();
    getrusage(RUSAGE_SELF, &r2b);

    double us2 = std::chrono::duration_cast<std::chrono::nanoseconds>(t2b - t2a).count() / 1000.0;
    long kb2 = (r2b.ru_maxrss - r2a.ru_maxrss) / 1024;
    allPass = allPass && ok2;

    // ---- Report ----
    std::cout << "0206 Reverse Linked List\n";
    std::cout << "Approach 1 (iterative) : time = " << us1 << " µs  peak-ram-delta = " << kb1 << " KB\n";
    std::cout << "Approach 2 (recursive) : time = " << us2 << " µs  peak-ram-delta = " << kb2 << " KB\n";
    std::cout << (allPass ? "PASS : both approaches reversed all 3 tests correctly."
                          : "FAIL : at least one test produced a wrong list.")
              << "\n";
    return 0;
}
