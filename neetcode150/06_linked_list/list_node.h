/*
 * =====================================================================
 * list_node.h — SHARED HEADER for the Linked List section (06)
 * ---------------------------------------------------------------------
 * WHAT A HEADER FILE IS (the lesson of this section)
 *   A .h (header) file is a CONTRACT between code files: it declares
 *   types and functions ONCE so that any .cpp that #includes it can
 *   use them without re-typing the definitions. The C++ compiler
 *   performs TEXTUAL INCLUSION: `#include "list_node.h"` literally
 *   pastes this file's contents into the .cpp at that line — one
 *   definition, shared by every solution.
 *
 *   Without a header, every one of the 11 solution files below would
 *   have to re-declare `struct ListNode` + buildList + printList by
 *   copy-paste. Copy-paste means 11 copies to keep in sync — a header
 *   keeps the definition in ONE place (Single Source of Truth).
 *
 *   Headers traditionally declare only, while definitions (bodies)
 *   live in a matching .cpp — for teaching clarity we inline the
 *   small helper bodies here so each solution file stays
 *   self-contained and compilable with one command:
 *       g++ -std=c++17 -O2 0206_reverse_linked_list.cpp -o run && ./run
 *
 * HOW TO USE
 *   In any solution .cpp of this folder, write:
 *       #include "list_node.h"
 *   The quotes (not <>) tell the compiler to look in the CURRENT
 *   folder first — exactly what we want for local project headers.
 * ---------------------------------------------------------------------
 * CONTENT
 *   struct ListNode :  val, next, random  (random used by 0138 only;
 *                     present for every problem so one header works
 *                     for the whole section).
 *   buildList(...)   : make a heap-allocated list from a vector.
 *   printList(...)   : print a list as  1 → 2 → 3 → null.
 *   deleteList(...)  : free every node (memory hygiene in main()).
 * =====================================================================
 */

#ifndef LIST_NODE_H
#define LIST_NODE_H

#include <vector>    // std::vector — input container for buildList
#include <iostream>  // std::cout — output for printList
#include <cstddef>   // std::nullptr_t support / nullptr

/*
 * Purpose : The node type of a singly linked list. Every node stores
 *           an int value and one pointer to the NEXT node (nullptr
 *           marks the end). `random` is a second pointer used ONLY by
 *           problem 0138 (Copy List with Random Pointer); it stays
 *           nullptr everywhere else — harmless for other problems.
 * Inputs  : val    — the integer payload of the node.
 *           next   — pointer to the following node (defaults nullptr).
 *           random — optional extra pointer (defaults nullptr).
 * Output  : A heap-allocated ListNode ready to be chained.
 */
struct ListNode {
    int val;          // payload of the node
    ListNode* next;   // pointer to the NEXT node; nullptr = end of list
    ListNode* random; // extra pointer; ONLY used by problem 0138

    // Constructor: initializes all three fields.
    ListNode(int v, ListNode* n = nullptr, ListNode* r = nullptr)
        : val(v), next(n), random(r) {}
};

/*
 * Purpose : Build a heap-allocated linked list from a vector of ints,
 *           preserving order. Used by main() of every solution to turn
 *           readable test data into the linked structure being solved.
 * Inputs  : values — the ints the list must contain, in order.
 * Output  : Pointer to the HEAD node (nullptr if `values` is empty).
 */
inline ListNode* buildList(const std::vector<int>& values) {
    // Dummy head: its ->next becomes the real head; the dummy itself
    // is thrown away so we never special-case the first insertion.
    ListNode* dummy = new ListNode(0);
    ListNode* tail = dummy;              // tail = last node we built
    for (int v : values) {
        tail->next = new ListNode(v);    // append one node per value
        tail = tail->next;               // the new node is now the tail
    }
    ListNode* head = dummy->next;        // first REAL node (or nullptr)
    delete dummy;                        // dummy was scaffolding only
    return head;
}

/*
 * Purpose : Print a linked list as  1 → 2 → 3 → null  so test output
 *           is human-readable and comparable across solutions.
 * Inputs  : head — first node to print (nullptr = empty list).
 * Output  : Prints to std::cout; returns nothing (void).
 */
inline void printList(ListNode* head) {
    if (head == nullptr) {
        std::cout << "null";
        return;
    }
    // Walk the chain; print each value followed by the arrow.
    for (ListNode* cur = head; cur != nullptr; cur = cur->next) {
        std::cout << cur->val;
        std::cout << (cur->next != nullptr ? " → " : " → null");
    }
}

/*
 * Purpose : Free every node of a list (heap memory hygiene). Without
 *           this, every test run would leak the whole chain.
 * Inputs  : head — first node to delete.
 * Output  : Returns nothing (void).
 */
inline void deleteList(ListNode* head) {
    // Save the next pointer BEFORE deleting: reading ->next after a
    // delete is a use-after-free bug.
    while (head != nullptr) {
        ListNode* next = head->next;
        delete head;
        head = next;
    }
}

#endif // LIST_NODE_H — include guard: this file compiles exactly once
