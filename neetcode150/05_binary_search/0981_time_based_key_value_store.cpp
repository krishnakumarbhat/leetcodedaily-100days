/*
 * =====================================================================
 * LeetCode 0981 : Time Based Key-Value Store                        (Medium)
 * https://leetcode.com/problems/time-based-key-value-store/
 * Category   : Binary Search (over a per-key timestamp vector)
 * ---------------------------------------------------------------------
 * PROBLEM
 *   Design a key-value store where every set(key, value, timestamp)
 *   call is logged, and get(key, timestamp) returns the value whose
 *   timestamp is the LARGEST one <= the query timestamp (or "" if
 *   the key has no such record). Timestamps only ever INCREASE per
 *   key (callers set them in ascending order).
 * ---------------------------------------------------------------------
 * INTUITION
 *   Each key owns a chronologically ordered list of (timestamp,value)
 *   records. get() is then a LOWER-BOUND query on that sorted list:
 *   "last record with ts <= query" == the predecessor of the first
 *   record with ts > query. Since every key's list is sorted, binary
 *   search answers each get() in O(log n) instead of a linear scan.
 * ---------------------------------------------------------------------
 * APPROACH 1 — map<key, vector<(ts,val)>> + binary search (BEST)
 *   C++ : std::map (red-black tree) maps the string key to a vector
 *   of (timestamp, value) pairs appended in order. In get():
 *     std::upper_bound(v.begin(), v.end(), ts, comp) finds the FIRST
 *     pair with timestamp > ts; the element BEFORE it is the answer
 *     (ts <= query). Every probe compares mid's timestamp with the
 *     query — the 0704 invariant with a twist: we want the last
 *     "<= query" element, i.e. predecessor of the upper bound.
 *   Python : dict[str, list[(int,str)]] + bisect_right on the
 *   timestamps list (same upper-bound semantics).
 *   set : O(1) amortized append. get : O(log n) per key.
 *   Time  Complexity : set O(1), get O(log n)   (n = records for key)
 *   Space Complexity : O(records) total across all keys.
 * ---------------------------------------------------------------------
 * APPROACH 2 — Linear scan of the per-key vector (contrast)
 *   Same storage, but get() walks the list from the END backward and
 *   returns the first record with ts <= query. Correct, zero binary
 *   search machinery — but O(n) per get; a hot key queried a million
 *   times turns into a billion comparisons.
 *   Time  Complexity : set O(1), get O(n)   Space Complexity : O(records)
 * ---------------------------------------------------------------------
 * DEEP DIVE — std::lower_bound vs std::upper_bound, and why 0981
 *   needs the latter
 *   lower_bound(key) → FIRST element NOT LESS than key   (>= key).
 *   upper_bound(key) → FIRST element GREATER than key    (> key).
 *   Here we want "last ts <= query": that is the predecessor of
 *   upper_bound(query) — for an exact hit, lower_bound would work,
 *   but the query usually falls BETWEEN timestamps, and only
 *   upper_bound's "strictly greater" boundary points at the first
 *   record that overshoots. Both run O(log n); the off-by-one is
 *   entirely about which boundary you take. The same "monotone
 *   predicate + predecessor" trick is how databases implement
 *   "most recent value at or before time T" (time-series lookups,
 *   versioned configs, event replay).
 * =====================================================================
 */

#include <iostream>     // std::cout — printing results
#include <vector>       // std::vector — per-key (ts, value) records
#include <string>       // std::string — keys and values
#include <unordered_map>// std::unordered_map — hash map variant (contrast)
#include <map>          // std::map — ordered key → record vector
#include <chrono>       // std::chrono — high-resolution timing
#include <sys/resource.h> // getrusage — peak RAM measurement

/* =====================================================================
 * APPROACH 1 : std::map of vectors + std::upper_bound binary search
 * ===================================================================== */
class TimeMap_BinarySearch {
public:
    /*
     * Purpose : Store a (timestamp, value) record for a key.
     * Inputs  : key — string key; value — string payload;
     *           timestamp — strictly increasing per key.
     * Output  : none (appends to the key's ordered record list).
     */
    void set(const std::string& key, const std::string& value, int timestamp) {
        // std::map keeps keys ordered; timestamps arrive ascending,
        // so a plain push_back keeps the per-key list sorted.
        store[key].emplace_back(timestamp, value);
    }

    /*
     * Purpose : Return the value with the largest ts <= timestamp.
     * Inputs  : key — string key; timestamp — query time.
     * Output  : std::string value, or "" when no record qualifies.
     */
    std::string get(const std::string& key, int timestamp) {
        // Unknown key → no records at all.
        auto it = store.find(key);
        if (it == store.end()) {
            return "";
        }
        const std::vector<std::pair<int, std::string>>& vals = it->second;

        // upper_bound: FIRST pair whose ts is STRICTLY > timestamp.
        // The pair before it is the last one with ts <= timestamp.
        int lo = 0;
        int hi = static_cast<int>(vals.size());

        // Hand-rolled upper_bound so the probe is visible — this is
        // exactly what std::upper_bound does internally.
        while (lo < hi) {
            int mid = lo + (hi - lo) / 2;
            if (vals[mid].first <= timestamp) {
                lo = mid + 1;              // mid qualifies → try right.
            } else {
                hi = mid;                  // first > query → keep scope.
            }
        }

        // lo == first index with ts > timestamp → answer is lo - 1.
        if (lo == 0) {
            return "";                     // every record is too new.
        }
        return vals[lo - 1].second;
    }

private:
    // key → chronologically ordered (timestamp, value) records.
    std::map<std::string, std::vector<std::pair<int, std::string>>> store;
};

/* =====================================================================
 * APPROACH 2 : Same storage, linear scan from the newest record
 * ===================================================================== */
class TimeMap_LinearScan {
public:
    /*
     * Purpose : Store a (timestamp, value) record for a key.
     * Inputs  : key — string key; value — string payload;
     *           timestamp — strictly increasing per key.
     * Output  : none (appends to the key's ordered record list).
     */
    void set(const std::string& key, const std::string& value, int timestamp) {
        store[key].emplace_back(timestamp, value);
    }

    /*
     * Purpose : Return the value with the largest ts <= timestamp.
     * Inputs  : key — string key; timestamp — query time.
     * Output  : std::string value, or "" when no record qualifies.
     */
    std::string get(const std::string& key, int timestamp) {
        auto it = store.find(key);
        if (it == store.end()) {
            return "";
        }
        const std::vector<std::pair<int, std::string>>& vals = it->second;

        // Scan from the newest record backward — first hit wins.
        for (int i = static_cast<int>(vals.size()) - 1; i >= 0; --i) {
            if (vals[i].first <= timestamp) {
                return vals[i].second;
            }
        }
        return "";                         // all records too new.
    }

private:
    std::map<std::string, std::vector<std::pair<int, std::string>>> store;
};

/* =====================================================================
 * BENCHMARK — run both approaches, print time + peak RAM
 * ===================================================================== */
int main() {
    // The official example script: 3 sets then 3 gets.
    {
        TimeMap_BinarySearch tm;
        struct rusage before, after;
        getrusage(RUSAGE_SELF, &before);
        auto start = std::chrono::high_resolution_clock::now();
        tm.set("foo", "bar", 1);
        tm.set("foo", "bar2", 4);
        std::string g1 = tm.get("foo", 1);    // expect "bar"
        std::string g2 = tm.get("foo", 3);    // expect "bar"
        std::string g3 = tm.get("foo", 5);    // expect "bar2"
        auto end = std::chrono::high_resolution_clock::now();
        getrusage(RUSAGE_SELF, &after);
        double us = std::chrono::duration_cast<std::chrono::nanoseconds>(end - start).count() / 1000.0;
        long kb = after.ru_maxrss - before.ru_maxrss; // ru_maxrss is KB on Linux

        bool ok = (g1 == "bar") && (g2 == "bar") && (g3 == "bar2");
        std::cout << "A1 BS (upper_bound): get(1)=" << g1 << " get(3)=" << g2
                  << " get(5)=" << g3 << "  time = " << us << " us  peak-ram = +"
                  << kb << " KB  | " << (ok ? "PASS" : "FAIL") << "\n";
    }
    {
        TimeMap_LinearScan tm;
        struct rusage before, after;
        getrusage(RUSAGE_SELF, &before);
        auto start = std::chrono::high_resolution_clock::now();
        tm.set("foo", "bar", 1);
        tm.set("foo", "bar2", 4);
        std::string g1 = tm.get("foo", 1);
        std::string g2 = tm.get("foo", 3);
        std::string g3 = tm.get("foo", 5);
        auto end = std::chrono::high_resolution_clock::now();
        getrusage(RUSAGE_SELF, &after);
        double us = std::chrono::duration_cast<std::chrono::nanoseconds>(end - start).count() / 1000.0;
        long kb = after.ru_maxrss - before.ru_maxrss;

        bool ok = (g1 == "bar") && (g2 == "bar") && (g3 == "bar2");
        std::cout << "A2 linear scan     : get(1)=" << g1 << " get(3)=" << g2
                  << " get(5)=" << g3 << "  time = " << us << " us  peak-ram = +"
                  << kb << " KB  | " << (ok ? "PASS" : "FAIL") << "\n";
    }

    // Second scenario: key with no qualifying record (expect "").
    {
        TimeMap_BinarySearch tm;
        tm.set("love", "high", 10);
        tm.set("love", "low", 20);
        std::string g1 = tm.get("love", 5);   // expect ""
        std::string g2 = tm.get("love", 10);  // expect "high"
        std::string g3 = tm.get("love", 15);  // expect "high"
        std::string g4 = tm.get("love", 20);  // expect "low"
        bool ok = g1.empty() && g2 == "high" && g3 == "high" && g4 == "low";
        std::cout << "A1 edge cases: get(5)=\"" << g1 << "\" get(10)=" << g2
                  << " get(15)=" << g3 << " get(20)=" << g4
                  << " | " << (ok ? "PASS" : "FAIL") << "\n";
    }

    return 0;
}