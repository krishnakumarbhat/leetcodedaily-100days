/*
 * =====================================================================
 * LeetCode 23 : Merge K Sorted Lists                             (Hard)
 * https://leetcode.com/problems/merge-k-sorted-lists/
 * Category   : Linked List
 * ---------------------------------------------------------------------
 * PROBLEM
 *   Given an array of k sorted linked lists, merge them into one
 *   sorted list.
 *       [[1→4→5], [1→3→4], [2→6]]  →  1→1→2→3→4→4→5→6
 * ---------------------------------------------------------------------
 * INTUITION
 *   With TWO lists, the winner of each round is min of the two heads
 *   (0021). With k lists, the winner is the SMALLEST of the k heads.
 *   Scanning all k heads per round costs O(k·n); a MIN-HEAP answers
 *   "which head is smallest?" in O(log k) — k·log k for push,
 *   log k per pop. Total O(n·log k).
 * ---------------------------------------------------------------------
 * APPROACH 1 — Min-heap of k heads (BEST)
 *   Push all k heads (value, list index) into a min-heap. Repeatedly
 *   pop the smallest head, append it to the result, push its
 *   successor back into the heap. The heap never grows beyond k.
 *   Time  Complexity : O(n·log k) — n total nodes, log k per op.
 *   Space Complexity : O(k)       — the heap holds ≤ k entries.
 * ---------------------------------------------------------------------
 * APPROACH 2 — Sequential two-list merges
 *   result = lists[0]; for each later list: result = mergeTwoLists(
 *   result, lists[i]) using the 0021 merge. List i is merged in
 *   after i passes over its nodes → O(n·k) worst case.
 *   Time  Complexity : O(n·k)   Space Complexity : O(1).
 * ---------------------------------------------------------------------
 * DEEP DIVE — why the heap version wins
 *   Sequential merging pays a hidden tax: a node from list k−1 is
 *   touched k−1 times (re-merged once per earlier list). The heap
 *   touches every node exactly once. The heap here is a PRIORITY
 *   QUEUE keyed by node value — the standard tool whenever the
 *   "best next candidate" must be found among many streams:
 *   k-way merge is the internal engine of external sorts, database
 *   merge joins, and log shard aggregation. In C++,
 *   std::priority_queue (heap) with a custom comparator; entries
 *   are (value, listId) so equal values don't compare pointers.
 * =====================================================================
 */

#include <vector>           // std::vector — the array of lists
#include <queue>            // std::priority_queue — min-heap for heads
#include <functional>       // std::greater — ordering for the heap
#include <chrono>           // std::chrono — timing
#include <iostream>         // std::cout — output
#include <sys/resource.h>   // getrusage — peak RAM
#include "list_node.h"      // our header: ListNode, buildList

/* =====================================================================
 * APPROACH 1 : Min-heap over the k current heads
 * ===================================================================== */
class Solution_MinHeap {
public:
    /*
     * Purpose : Merge k sorted lists into one sorted list with a heap.
     * Inputs  : lists — vector of heads of sorted lists (may be null).
     * Output  : Head of the merged sorted list.
     */
    ListNode* mergeKLists(std::vector<ListNode*>& lists) {
        // Min-heap ordered by node value: (value, list index).
        // The pair trick keeps the heap deterministic for ties.
        using Entry = std::pair<int, int>;
        std::priority_queue<Entry, std::vector<Entry>, std::greater<Entry>> heap;

        // Seed the heap with every list's current head.
        for (int i = 0; i < static_cast<int>(lists.size()); ++i) {
            if (lists[i] != nullptr) {
                heap.push({lists[i]->val, i});
            }
        }

        // Dummy head for the result chain (the 0021 lesson again).
        ListNode* dummy = new ListNode(0);
        ListNode* tail = dummy;

        while (!heap.empty()) {
            // Pop the smallest head among all k lists.
            Entry top = heap.top();
            heap.pop();
            int i = top.second;
            ListNode* node = lists[i];

            // Advance THAT list; its new head re-enters the heap.
            lists[i] = node->next;
            if (lists[i] != nullptr) {
                heap.push({lists[i]->val, i});
            }

            // Append the popped node to the result chain.
            tail->next = node;
            tail = tail->next;
        }

        ListNode* head = dummy->next;
        delete dummy;
        return head;
    }
};

/* =====================================================================
 * APPROACH 2 : Sequential two-list merges (reuse 0021's merge)
 * ===================================================================== */
class Solution_Sequential {
public:
    /*
     * Purpose : Merge k sorted lists by folding them in one by one.
     * Inputs  : lists — vector of heads of sorted lists (may be null).
     * Output  : Head of the merged sorted list.
     * Note    : O(n·k) worst case — late lists get re-merged k times.
     */
    ListNode* mergeKLists(std::vector<ListNode*>& lists) {
        ListNode* result = nullptr;

        // Fold every list into `result` with the two-list merge.
        for (ListNode* head : lists) {
            result = mergeTwo(result, head);
        }
        return result;
    }

private:
    /*
     * Purpose : The 0021 two-list merge (iterative, dummy head).
     * Inputs  : a, b — heads of two sorted lists.
     * Output  : Head of the merged sorted list.
     */
    ListNode* mergeTwo(ListNode* a, ListNode* b) {
        ListNode* dummy = new ListNode(0);
        ListNode* tail = dummy;
        while (a != nullptr && b != nullptr) {
            if (a->val <= b->val) {
                tail->next = a;
                a = a->next;
            } else {
                tail->next = b;
                b = b->next;
            }
            tail = tail->next;
        }
        tail->next = (a != nullptr) ? a : b;
        ListNode* head = dummy->next;
        delete dummy;
        return head;
    }
};

/* =====================================================================
 * BENCHMARK — 3 test sets, both approaches, time + peak RAM
 * ===================================================================== */
int main() {
    // Each test set: list of value-vectors; null entries allowed.
    std::vector<std::vector<std::vector<int>>> sets = {
        {{1, 4, 5}, {1, 3, 4}, {2, 6}},
        {{}, {1, 3}, {2}},
        {{1}}
    };
    std::vector<std::vector<int>> exp = {
        {1, 1, 2, 3, 4, 4, 5, 6},
        {1, 2, 3},
        {1}
    };

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
    for (std::size_t t = 0; t < sets.size(); ++t) {
        // Build k fresh lists; keep them for cleanup.
        std::vector<ListNode*> lists;
        for (const auto& v : sets[t]) lists.push_back(buildList(v));
        ListNode* merged = Solution_MinHeap().mergeKLists(lists);
        ok1 = verify(merged, t) && ok1;
        deleteList(merged);   // merged reuses the input nodes
    }
    auto e1 = std::chrono::high_resolution_clock::now();
    getrusage(RUSAGE_SELF, &r1b);

    // ---- Approach 2 ----
    struct rusage r2a, r2b;
    getrusage(RUSAGE_SELF, &r2a);
    auto s2 = std::chrono::high_resolution_clock::now();
    for (std::size_t t = 0; t < sets.size(); ++t) {
        std::vector<ListNode*> lists;
        for (const auto& v : sets[t]) lists.push_back(buildList(v));
        ListNode* merged = Solution_Sequential().mergeKLists(lists);
        ok2 = verify(merged, t) && ok2;
        deleteList(merged);
    }
    auto e2 = std::chrono::high_resolution_clock::now();
    getrusage(RUSAGE_SELF, &r2b);

    double us1 = std::chrono::duration_cast<std::chrono::nanoseconds>(e1 - s1).count() / 1000.0;
    double us2 = std::chrono::duration_cast<std::chrono::nanoseconds>(e2 - s2).count() / 1000.0;
    long kb1 = (r1b.ru_maxrss - r1a.ru_maxrss) / 1024;
    long kb2 = (r2b.ru_maxrss - r2a.ru_maxrss) / 1024;

    std::cout << "0023 Merge K Sorted Lists\n";
    std::cout << "Approach 1 (min-heap)  : time = " << us1 << " µs  peak-ram-delta = " << kb1 << " KB\n";
    std::cout << "Approach 2 (sequential) : time = " << us2 << " µs  peak-ram-delta = " << kb2 << " KB\n";
    std::cout << (ok1 && ok2 ? "PASS : both approaches merged all 3 test sets correctly."
                             : "FAIL : at least one test set produced a wrong list.")
              << "\n";
    return 0;
}
