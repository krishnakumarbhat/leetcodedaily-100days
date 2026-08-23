/*
 * =====================================================================
 * LeetCode 138 : Copy List with Random Pointer                 (Medium)
 * https://leetcode.com/problems/copy-list-with-random-pointer/
 * Category   : Linked List
 * ---------------------------------------------------------------------
 * PROBLEM
 *   A linked list has TWO pointers per node: `next` (normal chain)
 *   and `random` (points at ANY node of the list, or null). Build a
 *   DEEP COPY — brand-new nodes with identical values AND random
 *   pointers into the NEW list. The twist: when you clone node 3,
 *   its random target may not exist yet.
 * ---------------------------------------------------------------------
 * INTUITION
 *   The hard part is remapping random pointers: old-node → new-node.
 *   Two strategies: remember the mapping explicitly (hash map), or
 *   make the mapping IMPLICIT by physically pairing every old node
 *   with its clone (interleaving) — then the clone of old->random is
 *   ALWAYS the node right next to it.
 * ---------------------------------------------------------------------
 * APPROACH 1 — Interleaving (weave) — O(1) space (BEST)
 *   Pass 1: for every node, insert a clone right after it
 *           (old1 → NEW1 → old2 → NEW2 → …).
 *   Pass 2: every NEW node's random = its OLD partner's random->next
 *           (the clone sitting beside the target).
 *   Pass 3: unweave — restore old->next, connect new->next.
 *   Time  Complexity : O(n)   Space Complexity : O(1) extra.
 * ---------------------------------------------------------------------
 * APPROACH 2 — Hash map old → new
 *   Pass 1: create every clone and record old->new in a hash map.
 *   Pass 2: for each old node, set clone->next  = map[old->next]
 *           and clone->random = map[old->random].
 *   Time  Complexity : O(n)   Space Complexity : O(n) — the map.
 * ---------------------------------------------------------------------
 * DEEP DIVE — why interleaving is safe
 *   After pass 1 the list reads  old1,new1,old2,new2,…  so the clone
 *   of any node is exactly ONE step behind it: cloneOf(x) = x->next.
 *   In pass 2 the clone of old->random is therefore
 *   old->random->next. All rewiring is done with pure pointer math —
 *   no lookup table, hence O(1) space. This "store the mapping in
 *   the data structure itself" trick is the same spirit as
 *   morphing algorithms that temporarily decorate nodes (e.g.
 *   marking visited state with colors). The C++ version reuses
 *   our shared struct ListNode which carries the `random` member
 *   (list_node.h) — the section's header pays off here: every
 *   problem shares ONE node type.
 * =====================================================================
 */

#include <vector>           // std::vector — test data
#include <unordered_map>    // std::unordered_map — approach 2's mapping
#include <chrono>           // std::chrono — timing
#include <iostream>         // std::cout — output
#include <sys/resource.h>   // getrusage — peak RAM
#include "list_node.h"      // our header: ListNode (WITH `random` member)

/* =====================================================================
 * APPROACH 1 : Interleaving — clone woven next to each original
 * ===================================================================== */
class Solution_Interleave {
public:
    /*
     * Purpose : Deep-copy a random-pointer list using O(1) space.
     * Inputs  : head — first node of the original list.
     * Output  : Head of the deep copy (identical values + random).
     */
    ListNode* copyRandomList(ListNode* head) {
        if (head == nullptr) {
            return nullptr;
        }

        // PASS 1 — weave: old → NEW → old → NEW → …
        for (ListNode* cur = head; cur != nullptr; cur = cur->next->next) {
            // Clone is born beside its original; original's chain is
            // temporarily stretched around it.
            ListNode* clone = new ListNode(cur->val, cur->next);
            cur->next = clone;
        }

        // PASS 2 — random wiring: clone's random = original's random's
        // clone, and the clone of any node lives at x->next.
        for (ListNode* cur = head; cur != nullptr; cur = cur->next->next) {
            ListNode* clone = cur->next;
            clone->random = (cur->random != nullptr) ? cur->random->next : nullptr;
        }

        // PASS 3 — unweave: restore old->next; chain the clones up.
        ListNode* copyHead = head->next;
        for (ListNode* cur = head; cur != nullptr; cur = cur->next) {
            ListNode* clone = cur->next;
            cur->next = clone->next;                       // restore old chain
            clone->next = (clone->next != nullptr) ? clone->next->next : nullptr;
        }
        return copyHead;
    }
};

/* =====================================================================
 * APPROACH 2 : Hash map old node → new node
 * ===================================================================== */
class Solution_HashMap {
public:
    /*
     * Purpose : Deep-copy a random-pointer list with a hash map.
     * Inputs  : head — first node of the original list.
     * Output  : Head of the deep copy.
     */
    ListNode* copyRandomList(ListNode* head) {
        if (head == nullptr) {
            return nullptr;
        }

        // Pass 1: create clones; remember old → clone correspondence.
        std::unordered_map<ListNode*, ListNode*> map;
        for (ListNode* cur = head; cur != nullptr; cur = cur->next) {
            map[cur] = new ListNode(cur->val);
        }

        // Pass 2: wire next + random through the map (O(1) each).
        for (ListNode* cur = head; cur != nullptr; cur = cur->next) {
            map[cur]->next = (cur->next != nullptr) ? map[cur->next] : nullptr;
            map[cur]->random = (cur->random != nullptr) ? map[cur->random] : nullptr;
        }
        return map[head];
    }
};

/* =====================================================================
 * BENCHMARK — 3 tests, both approaches, time + peak RAM
 * ===================================================================== */
int main() {
    // Test lists with random targets as NODE OFFSETS (-1 = null):
    //   T1: 7→13→11→10→1,  random = [null, 0, 4, 2, 0]
    //   T2: 1→2→3,        random = [2, 0, 1]   (fully crossed)
    //   T3: single node    random = [-1]
    struct TestSpec {
        std::vector<int> vals;
        std::vector<int> randomIdx;
    };
    std::vector<TestSpec> specs = {
        {{7, 13, 11, 10, 1}, {-1, 0, 4, 2, 0}},
        {{1, 2, 3}, {2, 0, 1}},
        {{42}, {-1}}
    };

    // Build a random-pointer list from a spec (nodes must be arrayed
    // to resolve offsets → collect pointers first).
    auto makeList = [](const TestSpec& s) {
        std::vector<ListNode*> nodes;
        for (int v : s.vals) nodes.push_back(new ListNode(v));
        for (std::size_t i = 0; i < nodes.size(); ++i) {
            nodes[i]->next = (i + 1 < nodes.size()) ? nodes[i + 1] : nullptr;
            nodes[i]->random = (s.randomIdx[i] >= 0) ? nodes[static_cast<std::size_t>(s.randomIdx[i])] : nullptr;
        }
        return nodes;   // caller keeps the vector for cleanup
    };

    // Verify a deep copy: same values, same random OFFSETS, and no
    // node shared with the original (that is what "deep" means).
    // Note: random targets live in the COPY, so the position map is
    // built by walking the copy chain itself.
    auto verify = [](ListNode* orig, ListNode* copy, const TestSpec& s) {
        std::unordered_map<ListNode*, int> pos;
        int i = 0;
        for (ListNode* cur = copy; cur != nullptr; cur = cur->next) pos[cur] = i++;
        ListNode* o = orig;
        ListNode* c = copy;
        for (std::size_t idx = 0; idx < s.vals.size(); ++idx) {
            if (o == nullptr || c == nullptr) return false;
            if (o == c) return false;                     // SHARED node → not deep
            if (o->val != c->val) return false;
            int wantRandom = s.randomIdx[idx];
            // pos.find (NOT pos[]) — operator[] would INSERT a 0 for
            // missing keys, silently corrupting the comparison.
            int gotRandom = -1;
            if (c->random != nullptr) {
                auto hit = pos.find(c->random);
                gotRandom = (hit != pos.end()) ? hit->second : -999;
            }
            if (gotRandom != wantRandom) return false;    // random mismatch
            o = o->next;
            c = c->next;
        }
        return o == nullptr && c == nullptr;
    };

    bool ok1 = true, ok2 = true;

    // ---- Approach 1 ----
    struct rusage r1a, r1b;
    getrusage(RUSAGE_SELF, &r1a);
    auto s1 = std::chrono::high_resolution_clock::now();
    for (const auto& spec : specs) {
        std::vector<ListNode*> nodes = makeList(spec);
        ListNode* copy = Solution_Interleave().copyRandomList(nodes[0]);
        ok1 = verify(nodes[0], copy, spec) && ok1;
        // Free: original chain, then the copy chain.
        for (ListNode* n : nodes) delete n;
        for (ListNode* cur = copy; cur != nullptr; ) {
            ListNode* nxt = cur->next;
            delete cur;
            cur = nxt;
        }
    }
    auto e1 = std::chrono::high_resolution_clock::now();
    getrusage(RUSAGE_SELF, &r1b);

    // ---- Approach 2 ----
    struct rusage r2a, r2b;
    getrusage(RUSAGE_SELF, &r2a);
    auto s2 = std::chrono::high_resolution_clock::now();
    for (const auto& spec : specs) {
        std::vector<ListNode*> nodes = makeList(spec);
        ListNode* copy = Solution_HashMap().copyRandomList(nodes[0]);
        ok2 = verify(nodes[0], copy, spec) && ok2;
        for (ListNode* n : nodes) delete n;
        for (ListNode* cur = copy; cur != nullptr; ) {
            ListNode* nxt = cur->next;
            delete cur;
            cur = nxt;
        }
    }
    auto e2 = std::chrono::high_resolution_clock::now();
    getrusage(RUSAGE_SELF, &r2b);

    double us1 = std::chrono::duration_cast<std::chrono::nanoseconds>(e1 - s1).count() / 1000.0;
    double us2 = std::chrono::duration_cast<std::chrono::nanoseconds>(e2 - s2).count() / 1000.0;
    long kb1 = (r1b.ru_maxrss - r1a.ru_maxrss) / 1024;
    long kb2 = (r2b.ru_maxrss - r2a.ru_maxrss) / 1024;

    std::cout << "0138 Copy List with Random Pointer\n";
    std::cout << "Approach 1 (interleave) : time = " << us1 << " µs  peak-ram-delta = " << kb1 << " KB\n";
    std::cout << "Approach 2 (hash map)   : time = " << us2 << " µs  peak-ram-delta = " << kb2 << " KB\n";
    std::cout << (ok1 && ok2 ? "PASS : both approaches produced deep copies with correct random pointers."
                             : "FAIL : at least one copy was wrong or shared nodes.")
              << "\n";
    return 0;
}
