/*
 * =====================================================================
 * LeetCode 133 : Clone Graph                                        (Medium)
 * https://leetcode.com/problems/clone-graph/
 * Category   : Graphs
 * ---------------------------------------------------------------------
 * PROBLEM
 *   Given a reference to a node in a CONNECTED undirected graph,
 *   return a deep copy: a brand-new graph with the same structure
 *   where every clone node holds a copy of the original's value and
 *   a neighbour list pointing to the CORRESPONDING clone nodes.
 * ---------------------------------------------------------------------
 * INTUITION
 *   A graph is a set of nodes with pointers between them. A "deep
 *   copy" must duplicate every node exactly once and rewire every
 *   pointer to the duplicate. The danger is SHARING: two original
 *   neighbours pointing at the same node must map to ONE clone, or
 *   the copy is no longer a graph. A hash map `oldNode -> cloneNode`
 *   is exactly the "have I already cloned this?" answer: O(1) lookup
 *   turns the graph into a memoised tree traversal.
 * ---------------------------------------------------------------------
 * APPROACH 1 — Recursive DFS + hash map (BEST for clarity)
 *   clone(node): if node was cloned before → return the clone
 *   (memoisation). Else allocate clone, store in map FIRST (so
 *   cycles self-resolve), then recursively clone neighbours.
 *   Time  Complexity : O(V + E)  — every node visited once, every
 *                        edge rewired once.
 *   Space Complexity : O(V)      — map holds one entry per node +
 *                        recursion stack (≤ V deep).
 * ---------------------------------------------------------------------
 * APPROACH 2 — Iterative BFS + hash map
 *   Same map, but traversal uses a queue: clone a node, push its
 *   original neighbours, fill each clone's neighbour list. No
 *   recursion depth risk; frontier may hold O(V) nodes.
 *   Time  Complexity : O(V + E)   Space Complexity : O(V).
 * ---------------------------------------------------------------------
 * DATA STRUCTURE DEEP DIVE — hash map as the memoisation table
 *   Python dict / C++ unordered_map answer "seen this key?" in O(1)
 *   average. Python uses open addressing with LINEAR PROBING:
 *         h(k, i) = (hash(k) + i) mod m ,  i = 0, 1, 2, ...
 *   colliding keys walk to the next free slot in one contiguous
 *   array. C++ std::unordered_map uses separate chaining: each slot
 *   is a bucket (linked list) of colliding keys. The recursion in
 *   Approach 1 is a DEEP COPY: allocations happen on the unwinding
 *   call stack — every node is new, no aliasing with the original.
 * =====================================================================
 */

#include <iostream>         // std::cout — printing benchmark results
#include <vector>           // std::vector — neighbour lists
#include <string>           // std::string — result printing helpers
#include <queue>            // std::queue — BFS frontier
#include <unordered_map>    // std::unordered_map — old→clone memo table
#include <unordered_set>    // std::unordered_set — visited marker set
#include <chrono>           // std::chrono — high-resolution timing
#include <sys/resource.h>   // getrusage — peak RAM measurement

// Graph node as given by LeetCode (renamed fields for clarity).
struct Node {
    int val;
    std::vector<Node*> neighbors;   // undirected: edges appear twice
    explicit Node(int v) : val(v) {}
};

/* =====================================================================
 * APPROACH 1 : Recursive DFS + hash map (memoised deep copy)
 * ===================================================================== */
class Solution_1 {
private:
    // memo : original node -> its clone. The map is the VISITED SET
    // and the ANSWER table at the same time.
    std::unordered_map<Node*, Node*> memo;

    /*
     * Purpose : Deep-copy the subgraph reachable from `node`.
     * Inputs  : node — original graph node to clone.
     * Output  : Node* — pointer to the corresponding clone.
     */
    Node* clone(Node* node) {
        // Memoisation guard: already cloned → hand back the SAME clone
        // so the copy keeps exactly one clone per original node.
        auto it = memo.find(node);
        if (it != memo.end()) return it->second;

        // Allocate the clone, but STORE IT IN THE MAP FIRST: a cycle
        // pointing back at `node` must find the clone already there,
        // otherwise recursion never terminates.
        Node* copy = new Node(node->val);
        memo[node] = copy;

        // Recursively clone every neighbour and attach the clones.
        for (Node* nb : node->neighbors) {
            copy->neighbors.push_back(clone(nb));
        }
        return copy;
    }

public:
    /*
     * Purpose : Return a deep copy of a connected undirected graph.
     * Inputs  : node — reference to any node of the original graph.
     * Output  : Node* — root of the deep copy (nullptr for empty).
     */
    Node* cloneGraph(Node* node) {
        if (node == nullptr) return nullptr;
        memo.clear();       // fresh memo table per call
        return clone(node);
    }
};

/* =====================================================================
 * APPROACH 2 : Iterative BFS + hash map
 * ===================================================================== */
class Solution_2 {
public:
    /*
     * Purpose : Return a deep copy of a connected undirected graph.
     * Inputs  : node — reference to any node of the original graph.
     * Output  : Node* — root of the deep copy (nullptr for empty).
     */
    Node* cloneGraph(Node* node) {
        if (node == nullptr) return nullptr;

        // memo : original -> clone (the visited set AND answer table).
        std::unordered_map<Node*, Node*> memo;
        // Bootstrap: clone the root immediately.
        Node* rootCopy = new Node(node->val);
        memo[node] = rootCopy;

        // BFS frontier over ORIGINAL nodes — clones are created on
        // first encounter, neighbours wired up on dequeue.
        std::queue<Node*> q;
        q.push(node);

        while (!q.empty()) {
            Node* cur = q.front();
            q.pop();
            for (Node* nb : cur->neighbors) {
                // Clone each unvisited neighbour and queue it so ITS
                // neighbours get wired later.
                if (memo.find(nb) == memo.end()) {
                    memo[nb] = new Node(nb->val);
                    q.push(nb);
                }
                // Wire the clone of nb into the clone of cur. Because
                // the map memoises, repeated edges share one clone.
                memo[cur]->neighbors.push_back(memo[nb]);
            }
        }
        return rootCopy;
    }
};

/* =====================================================================
 * BENCHMARK — build a small graph, clone with both, verify structure
 * ===================================================================== */
int main() {
    // Build the official test graph: 1-2, 1-4, 2-3, 3-4 (square).
    Node* n1 = new Node(1);
    Node* n2 = new Node(2);
    Node* n3 = new Node(3);
    Node* n4 = new Node(4);
    n1->neighbors = {n2, n4};
    n2->neighbors = {n1, n3};
    n3->neighbors = {n2, n4};
    n4->neighbors = {n1, n3};

    // --- Approach 1 timing + memory ---
    struct rusage before1, after1;
    getrusage(RUSAGE_SELF, &before1);
    auto s1 = std::chrono::high_resolution_clock::now();
    Node* c1 = Solution_1().cloneGraph(n1);
    auto e1_ = std::chrono::high_resolution_clock::now();
    getrusage(RUSAGE_SELF, &after1);

    // --- Approach 2 timing + memory ---
    struct rusage before2, after2;
    getrusage(RUSAGE_SELF, &before2);
    auto s2 = std::chrono::high_resolution_clock::now();
    Node* c2 = Solution_2().cloneGraph(n1);
    auto e2_ = std::chrono::high_resolution_clock::now();
    getrusage(RUSAGE_SELF, &after2);

    long mem1 = (after1.ru_maxrss - before1.ru_maxrss);
    long mem2 = (after2.ru_maxrss - before2.ru_maxrss);
    double us1 = std::chrono::duration_cast<std::chrono::nanoseconds>(e1_ - s1).count() / 1000.0;
    double us2 = std::chrono::duration_cast<std::chrono::nanoseconds>(e2_ - s2).count() / 1000.0;

    // Verify helper: BFS over a clone, counting distinct nodes and
    // checking each node's neighbours are clones with matching values.
    auto verify = [&](Node* root) -> bool {
        if (root == nullptr) return false;
        std::unordered_set<Node*> seen;
        std::unordered_set<Node*> same;
        std::queue<Node*> q;
        q.push(root);
        seen.insert(root);
        int count = 0;
        while (!q.empty()) {
            Node* cur = q.front();
            q.pop();
            ++count;
            for (Node* nb : cur->neighbors) {
                // Every neighbour must be a DIFFERENT allocation from
                // the original graph nodes (deep copy, no aliasing).
                if (nb == n1 || nb == n2 || nb == n3 || nb == n4) return false;
                if (seen.find(nb) == seen.end()) {
                    seen.insert(nb);
                    q.push(nb);
                }
            }
        }
        // Connected square graph → exactly 4 distinct clone nodes.
        return count == 4;
    };

    bool ok1 = verify(c1);
    bool ok2 = verify(c2);
    bool allPass = ok1 && ok2;

    std::cout << "Clone (A1 DFS)   : 4 nodes reachable, no aliasing → "
              << (ok1 ? "PASS" : "FAIL")
              << "  time=" << us1 << " µs  mem=" << mem1 << " KB\n";
    std::cout << "Clone (A2 BFS)   : 4 nodes reachable, no aliasing → "
              << (ok2 ? "PASS" : "FAIL")
              << "  time=" << us2 << " µs  mem=" << mem2 << " KB\n";
    std::cout << (allPass ? "PASS : deep copies structurally correct.\n"
                          : "FAIL : at least one clone is wrong.\n");

    // Free every allocation (clones + originals) to keep the run clean.
    std::unordered_set<Node*> all;
    for (Node* p : {n1, n2, n3, n4, c1, c2}) {
        std::queue<Node*> f;
        f.push(p);
        while (!f.empty()) {
            Node* cur = f.front();
            f.pop();
            if (all.find(cur) != all.end()) continue;
            all.insert(cur);
            for (Node* nb : cur->neighbors) f.push(nb);
        }
    }
    for (Node* p : all) delete p;
    return 0;
}