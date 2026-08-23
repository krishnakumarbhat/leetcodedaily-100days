/*
 * =====================================================================
 * LeetCode 208 : Implement Trie (Prefix Tree)                     (Medium)
 * https://leetcode.com/problems/implement-trie-prefix-tree/
 * Category   : Tries
 * ---------------------------------------------------------------------
 * PROBLEM
 *   Implement a trie (prefix tree) supporting three operations:
 *     insert(word)       : store the word.
 *     search(word)       : true iff `word` was inserted VERBATIM.
 *     startsWith(prefix) : true iff SOME inserted word begins with it.
 *   All words are lowercase English letters only.
 * ---------------------------------------------------------------------
 * INTUITION
 *   A hash set answers "is this EXACT string stored?" in O(1) — but
 *   "does ANY stored word START with this prefix?" has no hash to
 *   probe; it would force a scan of every stored word (O(n·L)). A
 *   trie stores words along a SHARED spine: identical prefixes occupy
 *   the same nodes, so a prefix query is one root→leaf walk that is
 *   shared by every matching word. Each node holds one letter; the
 *   path root→node spells a prefix.
 * ---------------------------------------------------------------------
 * APPROACH 1 — 26-array trie (BEST for a fixed lowercase alphabet)
 *   Node  = { children[26], isEnd }. children[i] is the child for
 *   letter 'a'+i (null = that letter never follows this prefix);
 *   isEnd marks a node where an inserted word terminates.
 *   insert    : walk letters, allocate missing children, set isEnd.
 *   search    : walk letters; missing child ⇒ false; return final isEnd.
 *   startsWith: walk letters; missing child ⇒ false; else true — NO
 *               isEnd check, any descendant counts.
 *   Time  Complexity : O(L) per op — L = word length.
 *   Space Complexity : O(26·n·L) worst case — n·L nodes, each a
 *                        26-pointer array; prefix sharing shrinks it.
 * ---------------------------------------------------------------------
 * APPROACH 2 — Hash set + linear prefix scan (contrast)
 *   Keep every inserted word in a hash set (unordered_set = separate
 *   chaining: bucket + linked list of colliding keys).
 *   search    : O(1) average — one probe of h(k, i) = (hash(k) + i) mod m.
 *   startsWith: scan ALL stored words and prefix-compare each — O(n·L).
 *   Time  Complexity : search O(1) avg; startsWith O(n·L).
 *   Space Complexity : O(n·L) for the stored words.
 * ---------------------------------------------------------------------
 * DATA STRUCTURE DEEP DIVE — trie vs hash map
 *   A trie is a 26-way tree: every node carries 26 child pointers
 *   (one branch per letter position) + an isEnd flag. Two words that
 *   share a prefix share EVERY node of that prefix — inserting "app"
 *   then "apple" costs only 2 extra nodes, not 5.
 *   Hash maps (C++ unordered_set = separate chaining; Python set =
 *   open addressing with linear probing h(k,i) = (hash(k) + i) mod m)
 *   give O(1) EXACT matches, but a prefix is not a key — "all words
 *   starting with 'app'" forces a full scan. The trie turns that query
 *   into one O(L) walk. The price is memory: each node pre-allocates
 *   26 pointers (26×8 B ≈ 208 B) even when only 1–2 children exist.
 *   Fixed small alphabet → array children (child lookup = 1 multiply,
 *   cache-friendly); large/unbounded alphabets (Unicode) → hash-map
 *   children allocate only what is actually used.
 * =====================================================================
 */

#include <iostream>       // std::cout — printing benchmark results
#include <vector>         // std::vector — test-case op lists, scanning
#include <string>         // std::string — words and prefixes
#include <chrono>         // std::chrono — high-resolution timing
#include <sys/resource.h> // getrusage — peak-RAM measurement
#include <unordered_set>  // std::unordered_set — approach 2's word store

/* =====================================================================
 * APPROACH 1 : 26-array trie
 * ===================================================================== */
class Solution_One {
private:
    /* One node per letter of a prefix: 26 child pointers + end flag. */
    struct TrieNode {
        TrieNode* children[26]; // null = that letter not present below
        bool isEnd;             // true = an inserted word ENDS at this node
        TrieNode() : children(), isEnd(false) {} // zero-initialize pointers
    };

    TrieNode* root; // sentinel; the path below it spells every word

    /* Free the whole subtree — recursive walk, called by the destructor. */
    static void freeNode(TrieNode* n) {
        for (int i = 0; i < 26; ++i) {
            if (n->children[i]) freeNode(n->children[i]);
        }
        delete n;
    }

public:
    /* Purpose : Build an empty trie (only the sentinel root exists).
     * Inputs  : none.
     * Output  : a ready-to-use trie object. */
    Solution_One() : root(new TrieNode()) {}

    /* Purpose : Free every node in the trie to keep the benchmark clean.
     * Inputs  : none.
     * Output  : nothing. */
    ~Solution_One() { freeNode(root); }

    /* Purpose : Store `word` in the trie.
     * Inputs  : word — lowercase string to insert.
     * Output  : void; trie gains the word (duplicates are idempotent). */
    void insert(const std::string& word) {
        TrieNode* n = root;
        for (char c : word) {
            int i = c - 'a';                          // letter → slot 0..25
            if (!n->children[i]) n->children[i] = new TrieNode(); // grow path
            n = n->children[i];                       // descend one level
        }
        n->isEnd = true;                              // mark word completion
    }

    /* Purpose : Report whether `word` was inserted verbatim.
     * Inputs  : word — lowercase string to look up.
     * Output  : true iff a node exists for every letter AND the last
     *           one is a word-end. */
    bool search(const std::string& word) const {
        const TrieNode* n = root;
        for (char c : word) {
            n = n->children[c - 'a'];
            if (!n) return false;                     // path dies → absent
        }
        return n->isEnd;                              // must END here exactly
    }

    /* Purpose : Report whether any inserted word starts with `prefix`.
     * Inputs  : prefix — lowercase string to match as a prefix.
     * Output  : true iff a node exists for every letter of the prefix
     *           (any word finishing below it makes the prefix valid). */
    bool startsWith(const std::string& prefix) const {
        const TrieNode* n = root;
        for (char c : prefix) {
            n = n->children[c - 'a'];
            if (!n) return false;
        }
        return true; // a path exists — some word continues from here
    }
};

/* =====================================================================
 * APPROACH 2 : hash set + linear prefix scan (no trie at all)
 * ===================================================================== */
class Solution_Two {
private:
    std::unordered_set<std::string> words; // exact-match store (chaining)

public:
    /* Purpose : Build an empty word dictionary.
     * Inputs  : none.
     * Output  : a ready-to-use object. */
    Solution_Two() = default;

    /* Purpose : Store `word` verbatim in the hash set.
     * Inputs  : word — lowercase string to insert.
     * Output  : void. */
    void insert(const std::string& word) { words.insert(word); }

    /* Purpose : Exact membership test.
     * Inputs  : word — lowercase string.
     * Output  : true iff word is in the set — O(1) average, one hash
     *           probe (chained buckets on collision). */
    bool search(const std::string& word) const { return words.find(word) != words.end(); }

    /* Purpose : Prefix test WITHOUT a prefix data structure.
     * Inputs  : prefix — lowercase string.
     * Output  : true iff some stored word starts with it — must scan
     *           every stored word, O(n·L), because a hash set cannot
     *           answer range/prefix queries. */
    bool startsWith(const std::string& prefix) const {
        for (const std::string& w : words) {
            if (w.size() >= prefix.size() &&
                w.compare(0, prefix.size(), prefix) == 0) {
                return true;
            }
        }
        return false;
    }
};

/* =====================================================================
 * BENCHMARK — run both approaches on 3 batches, compare time + RAM
 * ===================================================================== */
namespace {
    /* One batch of operations: "insert X" stores, "search X" and
       "prefix X" must equal the corresponding boolean in `expect`. */
    struct TestCase {
        std::string name;
        std::vector<std::string> ops;
        std::vector<bool> expect;
    };
}

/* Runs every op in `tc` against a solver; returns false on mismatch.
   `expect` holds one boolean per NON-insert op, so it needs its own
   index (inserts interleave with checks). Template allows one driver
   for both solver classes (same API). */
template <typename Solver>
bool runOps(Solver& s, const TestCase& tc) {
    size_t j = 0; // position inside tc.expect — only advances on checks
    for (size_t i = 0; i < tc.ops.size(); ++i) {
        const std::string& op = tc.ops[i];
        if (op.rfind("insert ", 0) == 0) {
            s.insert(op.substr(7)); // inserts never fail — skip the check
            continue;
        }
        bool result = op.rfind("search ", 0) == 0
            ? s.search(op.substr(7))
            : s.startsWith(op.substr(7));
        if (result != tc.expect[j]) return false; // mismatch → FAIL
        ++j;
    }
    return true;
}

/* Measures one solver across all batches; prints time + RAM per batch. */
template <typename Solver>
bool bench(const std::string& label, const std::vector<TestCase>& tests) {
    bool allOk = true;
    for (const TestCase& tc : tests) {
        struct rusage before, after;
        getrusage(RUSAGE_SELF, &before);
        auto start = std::chrono::high_resolution_clock::now();
        Solver solver;                              // fresh object per batch
        bool ok = runOps(solver, tc);
        auto end = std::chrono::high_resolution_clock::now();
        getrusage(RUSAGE_SELF, &after);

        double us = std::chrono::duration_cast<std::chrono::nanoseconds>(end - start).count() / 1000.0;
        long memKb = after.ru_maxrss - before.ru_maxrss; // ru_maxrss is in KB
        allOk = allOk && ok;
        std::cout << label << " | " << tc.name << " : "
                  << (ok ? "PASS" : "FAIL")
                  << "  time = " << us << " µs  peak-ram-delta = "
                  << memKb << " KB\n";
    }
    return allOk;
}

int main() {
    /* Three batches: shared-prefix depth, exact-vs-prefix semantics,
       and a long-prefix miss — every search/prefix op carries the
       expected boolean in `expect`. */
    const std::vector<TestCase> tests = {
        { "problem example",
          { "insert apple", "search apple", "search app", "prefix app",
            "insert app",  "search app" },
          { true, false, true, true } },
        { "shared prefixes",
          { "insert a", "insert ab", "insert abc", "insert abd",
            "search ab", "prefix ab", "search abd", "search abe", "prefix abc" },
          { true, true, true, false, true } },
        { "long prefix miss",
          { "insert zookeeper", "insert zoo", "insert zoom",
            "search zoo", "prefix zo", "prefix zooo", "search zook", "search zoom" },
          { true, true, false, false, true } }
    };

    bool ok1 = bench<Solution_One>("Approach 1 (26-array trie) ", tests);
    bool ok2 = bench<Solution_Two>("Approach 2 (hash set + scan)", tests);

    std::cout << (ok1 && ok2
        ? "PASS : both approaches return the expected answers on all batches."
        : "FAIL : at least one answer was wrong.") << "\n";
    return 0;
}
