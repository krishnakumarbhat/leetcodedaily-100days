/*
 * =====================================================================
 * LeetCode 146 : LRU Cache                                     (Medium)
 * https://leetcode.com/problems/lru-cache/
 * Category   : Linked List
 * ---------------------------------------------------------------------
 * PROBLEM
 *   Design a cache with capacity C supporting O(1) average:
 *     get(key) → value, or −1 if absent. Access marks key RECENT.
 *     put(k,v) → insert (or overwrite); if full, EVICT the
 *                LEAST RECENTLY USED entry first.
 * ---------------------------------------------------------------------
 * INTUITION
 *   A hash map alone gives O(1) get/put but cannot tell you "which
 *   key was least recently used" — that needs an ORDER, and the
 *   order must be updatable in O(1) whenever a key is touched.
 *   A doubly linked list (LRU ⇔ MRU) delivers: moving a node to the
 *   MRU end costs O(1) with the right pointers. Map key → list node.
 *   Map = the O(1) lookup; list = the O(1) eviction order.
 * ---------------------------------------------------------------------
 * APPROACH 1 — Hash map key → node + doubly linked list (BEST)
 *   DLL keeps keys in recency order: head = LRU (eviction victim),
 *   tail = MRU. get(k): map hit → move node to tail → return value.
 *   put(k,v): exists → update + move to tail; new → append at tail,
 *   and if size > C, unlink head and erase it from the map.
 *   Time  Complexity : O(1) average per get/put.
 *   Space Complexity : O(C) — the map + the list hold ≤ C entries.
 * ---------------------------------------------------------------------
 * APPROACH 2 — Naive: map key → (value, lastUsedTick)
 *   Every get/put stamps the current tick counter. Eviction: scan
 *   all entries for the smallest tick — O(C) per eviction.
 *   Time  Complexity : O(1) get, O(C) put-when-full.
 *   Space Complexity : O(C).
 * ---------------------------------------------------------------------
 * DEEP DIVE — hash map (probing) + doubly linked list marriage
 *   Python dict keys use open addressing with LINEAR PROBING:
 *       h(k, i) = (hash(k) + i) mod m ,  i = 0, 1, 2, …
 *   C++ std::unordered_map uses separate chaining. Both give the
 *   O(1) average random access the DLL cannot provide alone.
 *   The DLL is the OPPOSITE structure: O(1) insert/delete at known
 *   positions but O(n) search — together they cover each other's
 *   weakness: map finds the node, list reorders it. This exact pair
 *   (hash table + doubly linked list) is how real caches work:
 *   Redis' allkeys-lru, memcached's LRU, and the Linux kernel's
 *   page cache (radix tree + LRU list). Eviction = "drop the head",
 *   promotion = "move to tail" — every browser tab, every CDN.
 * =====================================================================
 */

#include <unordered_map>   // std::unordered_map — O(1) key lookup
#include <vector>          // std::vector — op sequences for tests
#include <chrono>          // std::chrono — timing
#include <iostream>        // std::cout — output
#include <sys/resource.h>  // getrusage — peak RAM
#include "list_node.h"     // our header (ListNode unused here; the
                           // lesson: headers centralize shared types)

/* =====================================================================
 * APPROACH 1 : Hash map + custom doubly linked list (BEST)
 * ===================================================================== */
class LRUCache_List {
private:
    // Doubly linked list node: key, value, prev, next.
    struct DNode {
        int key;
        int value;
        DNode* prev;
        DNode* next;
        DNode(int k, int v) : key(k), value(v), prev(nullptr), next(nullptr) {}
    };

    int capacity_;
    // map: key → pointer to its list node (O(1) location).
    std::unordered_map<int, DNode*> map_;
    DNode* head_;   // LRU end — eviction victim lives here
    DNode* tail_;   // MRU end — most recently used lives here

    // Move an existing node to the MRU end (tail). Four pointer
    // rewrites on a doubly linked list — O(1).
    void moveToTail(DNode* node) {
        if (node == tail_) {
            return;   // already most recent
        }
        // Unlink: bridge prev <-> next around the node.
        if (node->prev != nullptr) node->prev->next = node->next;
        if (node->next != nullptr) node->next->prev = node->prev;
        if (node == head_) head_ = node->next;   // node was the victim
        // Re-attach at the tail.
        node->prev = tail_;
        node->next = nullptr;
        tail_->next = node;
        tail_ = node;
    }

    // Append a BRAND-NEW node at the MRU end.
    void pushBack(int key, int value) {
        DNode* node = new DNode(key, value);
        map_[key] = node;
        if (tail_ == nullptr) {
            head_ = tail_ = node;   // first node ever
        } else {
            node->prev = tail_;
            tail_->next = node;
            tail_ = node;
        }
    }

    // Evict the LRU (head) — O(1).
    void popFront() {
        DNode* victim = head_;
        head_ = head_->next;
        if (head_ != nullptr) {
            head_->prev = nullptr;
        } else {
            tail_ = nullptr;
        }
        map_.erase(victim->key);   // forget the key too
        delete victim;
    }

public:
    /*
     * Purpose : Construct a cache with the given capacity.
     * Inputs  : capacity — maximum number of entries before eviction.
     */
    LRUCache_List(int capacity) : capacity_(capacity), head_(nullptr), tail_(nullptr) {}

    /*
     * Purpose : Return the value of `key` if cached, else −1.
     * Inputs  : key — the lookup key.
     * Output  : The cached value, or −1. A hit refreshes recency.
     */
    int get(int key) {
        auto it = map_.find(key);
        if (it == map_.end()) {
            return -1;   // miss: nothing to refresh
        }
        moveToTail(it->second);   // hit ⇒ now the MOST recent
        return it->second->value;
    }

    /*
     * Purpose : Insert or overwrite key→value; evict LRU if full.
     * Inputs  : key — the key to store; value — the value to store.
     * Output  : Returns nothing (void).
     */
    void put(int key, int value) {
        auto it = map_.find(key);
        if (it != map_.end()) {
            // Existing key: update the value, refresh recency.
            it->second->value = value;
            moveToTail(it->second);
            return;
        }
        // New key: if full, evict the least-recently-used first.
        if (static_cast<int>(map_.size()) == capacity_) {
            popFront();
        }
        pushBack(key, value);
    }
};

/* =====================================================================
 * APPROACH 2 : Naive tick counter + linear eviction scan (contrast)
 * ===================================================================== */
class LRUCache_Naive {
private:
    int capacity_;
    long long tick_;   // global clock, incremented on every op
    // key → (value, lastUsedTick)
    std::unordered_map<int, std::pair<int, long long>> store_;

public:
    /*
     * Purpose : Construct a cache with the given capacity.
     * Inputs  : capacity — maximum number of entries before eviction.
     */
    LRUCache_Naive(int capacity) : capacity_(capacity), tick_(0) {}

    /*
     * Purpose : Return the value of `key` if cached, else −1.
     * Inputs  : key — the lookup key.
     * Output  : The cached value, or −1. A hit refreshes recency.
     */
    int get(int key) {
        auto it = store_.find(key);
        if (it == store_.end()) {
            return -1;
        }
        it->second.second = ++tick_;   // stamp the access time
        return it->second.first;
    }

    /*
     * Purpose : Insert or overwrite key→value; evict LRU if full.
     * Inputs  : key — the key to store; value — the value to store.
     * Output  : Returns nothing (void).
     */
    void put(int key, int value) {
        auto it = store_.find(key);
        if (it != store_.end()) {
            it->second = {value, ++tick_};
            return;
        }
        if (static_cast<int>(store_.size()) == capacity_) {
            // Eviction needs the OLDEST stamp — scan everything.
            int victimKey = -1;
            long long oldest = tick_;
            for (const auto& entry : store_) {
                if (entry.second.second < oldest) {
                    oldest = entry.second.second;
                    victimKey = entry.first;
                }
            }
            store_.erase(victimKey);
        }
        store_[key] = {value, ++tick_};
    }
};

/* =====================================================================
 * BENCHMARK — official example + a burst, time + peak RAM
 * ===================================================================== */
int main() {
    // Official example: capacity 2,
    // put(1,1) put(2,2) get(1) put(3,3) get(2) put(4,4) get(1) get(3) get(4)
    // → [null, null, 1, null, -1, null, -1, 3, 4]
    std::vector<int> expected = {1, -1, -1, 3, 4};

    auto runExample = [&](auto& cache) {
        std::vector<int> out;
        cache.put(1, 1);
        cache.put(2, 2);
        out.push_back(cache.get(1));   // 1  (2 was least recent)
        cache.put(3, 3);               // evicts 2
        out.push_back(cache.get(2));   // -1 (gone)
        cache.put(4, 4);               // evicts 1
        out.push_back(cache.get(1));   // -1 (gone)
        out.push_back(cache.get(3));   // 3
        out.push_back(cache.get(4));   // 4
        return out == expected;
    };

    bool ok1 = false, ok2 = false;

    // ---- Approach 1 ----
    struct rusage r1a, r1b;
    getrusage(RUSAGE_SELF, &r1a);
    auto s1 = std::chrono::high_resolution_clock::now();
    {
        LRUCache_List cache(2);
        ok1 = runExample(cache);
    }
    auto e1 = std::chrono::high_resolution_clock::now();
    getrusage(RUSAGE_SELF, &r1b);

    // ---- Approach 2 ----
    struct rusage r2a, r2b;
    getrusage(RUSAGE_SELF, &r2a);
    auto s2 = std::chrono::high_resolution_clock::now();
    {
        LRUCache_Naive cache(2);
        ok2 = runExample(cache);
    }
    auto e2 = std::chrono::high_resolution_clock::now();
    getrusage(RUSAGE_SELF, &r2b);

    double us1 = std::chrono::duration_cast<std::chrono::nanoseconds>(e1 - s1).count() / 1000.0;
    double us2 = std::chrono::duration_cast<std::chrono::nanoseconds>(e2 - s2).count() / 1000.0;
    long kb1 = (r1b.ru_maxrss - r1a.ru_maxrss) / 1024;
    long kb2 = (r2b.ru_maxrss - r2a.ru_maxrss) / 1024;

    std::cout << "0146 LRU Cache\n";
    std::cout << "Approach 1 (map + DLL) : time = " << us1 << " µs  peak-ram-delta = " << kb1 << " KB\n";
    std::cout << "Approach 2 (naive tick) : time = " << us2 << " µs  peak-ram-delta = " << kb2 << " KB\n";
    std::cout << (ok1 && ok2 ? "PASS : both caches reproduced the official example (1, -1, -1, 3, 4)."
                             : "FAIL : at least one cache deviated from the expected outputs.")
              << "\n";
    return 0;
}
