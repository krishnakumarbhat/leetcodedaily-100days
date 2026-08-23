/*
 * =====================================================================
 * LeetCode 2 : Add Two Numbers                                   (Medium)
 * https://leetcode.com/problems/add-two-numbers/
 * Category   : Linked List
 * ---------------------------------------------------------------------
 * PROBLEM
 *   Two linked lists store NON-NEGATIVE integers in REVERSE order
 *   (head = least significant digit). Return the sum as a linked
 *   list in the same format.
 *       2→4→3  (342)  +  5→6→4  (465)  =  7→0→8  (807)
 * ---------------------------------------------------------------------
 * INTUITION
 *   Reverse order means the heads are the ONES digits — so addition
 *   from the head is just grade-school column addition:
 *   digit sum = (a + b + carry) ; carry = sum / 10 ; digit = sum % 10.
 *   No digit lists to pad: a missing node contributes 0.
 * ---------------------------------------------------------------------
 * APPROACH 1 — Iterative with a dummy node + carry (BEST)
 *   Walk both lists with two pointers; while either lives (or carry
 *   is non-zero), sum the digits plus carry, append sum % 10, keep
 *   sum / 10 as the new carry. Dummy head removes the first-append
 *   special case.
 *   Time  Complexity : O(max(n, m)) — one node per result digit.
 *   Space Complexity : O(1)         — pointers only (output excluded).
 * ---------------------------------------------------------------------
 * APPROACH 2 — Recursive
 *   Same column arithmetic, distributed over the call stack. Base
 *   case: both lists null AND carry == 0 → null. Each call consumes
 *   one digit from each list and lets the recursion build the rest.
 *   Time  Complexity : O(max(n, m)).
 *   Space Complexity : O(max(n, m)) — recursion depth.
 * ---------------------------------------------------------------------
 * DEEP DIVE — why reverse order is a GIFT
 *   Human arithmetic is done right-to-left (least significant first),
 *   which is EXACTLY the layout of these lists — the carry never
 *   forces you to walk back, and the result is produced in final
 *   order without reversing. If the lists were stored most-significant
 *   first, you would need a stack or a reverse step. This problem is
 *   the canonical "linked list = digit stream" pattern used in
 *   arbitrary-precision arithmetic: Python ints, Java BigInteger and
 *   C++ boost::multiprecision all store digits in chunks and add
 *   them with exactly this carry loop, on arrays instead of nodes.
 * =====================================================================
 */

#include <vector>          // std::vector — test data
#include <chrono>          // std::chrono — timing
#include <iostream>        // std::cout — output
#include <sys/resource.h>  // getrusage — peak RAM
#include "list_node.h"     // our header: ListNode, buildList

/* =====================================================================
 * APPROACH 1 : Iterative column addition with a dummy head
 * ===================================================================== */
class Solution_Iterative {
public:
    /*
     * Purpose : Sum two reverse-ordered digit lists into a new list.
     * Inputs  : l1, l2 — heads of two digit lists (head = ones digit).
     * Output  : Head of the sum list (same reverse digit order).
     */
    ListNode* addTwoNumbers(ListNode* l1, ListNode* l2) {
        // Dummy sentinel so the result chain needs no first-append case.
        ListNode* dummy = new ListNode(0);
        ListNode* tail = dummy;
        int carry = 0;

        // Keep adding while digits remain OR the carry is still live
        // (e.g. 5 + 5 → 0, carry 1 → one extra result node).
        while (l1 != nullptr || l2 != nullptr || carry != 0) {
            // Missing digit contributes 0 — no padding needed.
            int sum = carry;
            if (l1 != nullptr) { sum += l1->val; l1 = l1->next; }
            if (l2 != nullptr) { sum += l2->val; l2 = l2->next; }

            carry = sum / 10;         // overflow moves to the next column
            tail->next = new ListNode(sum % 10);  // one result digit
            tail = tail->next;
        }

        ListNode* head = dummy->next;
        delete dummy;                 // scaffold goes away
        return head;
    }
};

/* =====================================================================
 * APPROACH 2 : Recursive column addition
 * ===================================================================== */
class Solution_Recursive {
public:
    /*
     * Purpose : Sum two digit lists recursively (helpers below).
     * Inputs  : l1, l2 — heads of two reverse-ordered digit lists.
     * Output  : Head of the sum list.
     */
    ListNode* addTwoNumbers(ListNode* l1, ListNode* l2) {
        // Public entry: recursion starts with a zero carry.
        return addRec(l1, l2, 0);
    }

private:
    /*
     * Purpose : One recursive column: digit = (a+b+carry)%10, next
     *           column = recursion with carry (a+b+carry)/10.
     * Inputs  : a, b — remaining digit lists (null = 0), carry.
     * Output  : Head of the sum of the remaining columns.
     */
    ListNode* addRec(ListNode* a, ListNode* b, int carry) {
        // Base case: nothing left and no carry → chain ends here.
        if (a == nullptr && b == nullptr && carry == 0) {
            return nullptr;
        }
        // Read the current column; null nodes contribute 0.
        int sum = carry;
        if (a != nullptr) sum += a->val;
        if (b != nullptr) sum += b->val;

        // This column's digit leads; the tail is built by recursion.
        ListNode* node = new ListNode(sum % 10);
        node->next = addRec(a != nullptr ? a->next : nullptr,
                            b != nullptr ? b->next : nullptr,
                            sum / 10);
        return node;
    }
};

/* =====================================================================
 * BENCHMARK — 3 tests, both approaches, time + peak RAM
 * ===================================================================== */
int main() {
    std::vector<std::vector<int>> a = {{2, 4, 3}, {0}, {9, 9, 9, 9, 9}};
    std::vector<std::vector<int>> b = {{5, 6, 4}, {0}, {1}};
    std::vector<std::vector<int>> exp = {{7, 0, 8}, {0}, {0, 0, 0, 0, 0, 1}};

    auto verify = [&](ListNode* sum, std::size_t t) {
        for (int want : exp[t]) {
            if (sum == nullptr || sum->val != want) return false;
            sum = sum->next;
        }
        return sum == nullptr;
    };

    bool ok1 = true, ok2 = true;

    // ---- Approach 1 ----
    struct rusage r1a, r1b;
    getrusage(RUSAGE_SELF, &r1a);
    auto s1 = std::chrono::high_resolution_clock::now();
    for (std::size_t t = 0; t < a.size(); ++t) {
        ListNode* l1 = buildList(a[t]);
        ListNode* l2 = buildList(b[t]);
        ListNode* sum = Solution_Iterative().addTwoNumbers(l1, l2);
        ok1 = verify(sum, t) && ok1;
        deleteList(l1);
        deleteList(l2);
        deleteList(sum);
    }
    auto e1 = std::chrono::high_resolution_clock::now();
    getrusage(RUSAGE_SELF, &r1b);

    // ---- Approach 2 ----
    struct rusage r2a, r2b;
    getrusage(RUSAGE_SELF, &r2a);
    auto s2 = std::chrono::high_resolution_clock::now();
    for (std::size_t t = 0; t < a.size(); ++t) {
        ListNode* l1 = buildList(a[t]);
        ListNode* l2 = buildList(b[t]);
        ListNode* sum = Solution_Recursive().addTwoNumbers(l1, l2);
        ok2 = verify(sum, t) && ok2;
        deleteList(l1);
        deleteList(l2);
        deleteList(sum);
    }
    auto e2 = std::chrono::high_resolution_clock::now();
    getrusage(RUSAGE_SELF, &r2b);

    double us1 = std::chrono::duration_cast<std::chrono::nanoseconds>(e1 - s1).count() / 1000.0;
    double us2 = std::chrono::duration_cast<std::chrono::nanoseconds>(e2 - s2).count() / 1000.0;
    long kb1 = (r1b.ru_maxrss - r1a.ru_maxrss) / 1024;
    long kb2 = (r2b.ru_maxrss - r2a.ru_maxrss) / 1024;

    std::cout << "0002 Add Two Numbers\n";
    std::cout << "Approach 1 (iterative) : time = " << us1 << " µs  peak-ram-delta = " << kb1 << " KB\n";
    std::cout << "Approach 2 (recursive) : time = " << us2 << " µs  peak-ram-delta = " << kb2 << " KB\n";
    std::cout << (ok1 && ok2 ? "PASS : both approaches produced correct sums on all 3 tests."
                             : "FAIL : at least one test produced a wrong sum.")
              << "\n";
    return 0;
}
