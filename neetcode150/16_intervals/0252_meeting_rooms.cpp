/*
 * =====================================================================
 * LeetCode 252 : Meeting Rooms                                     (Easy)
 * https://leetcode.com/problems/meeting-rooms/
 * Category   : Intervals
 * ---------------------------------------------------------------------
 * PROBLEM
 *   Given an array of meeting time intervals [start, end], return
 *   true if ONE person can attend ALL meetings (no two intervals may
 *   overlap). A meeting occupies [start, end) — half-open: ending at
 *   4 and starting at 4 do NOT overlap.
 * ---------------------------------------------------------------------
 * INTUITION
 *   If any two meetings overlap, the person cannot be in both rooms.
 *   After sorting by start, overlaps only ever happen between
 *   NEIGHBOURS in the sorted order — so checking adjacent pairs is
 *   sufficient and provably complete (if i < j overlap, then i and
 *   i+1 already overlap along the chain).
 * ---------------------------------------------------------------------
 * APPROACH 1 — Sort by start + adjacent overlap check (BEST)
 *   Sort by start. Walk once: if interval[i].start < interval[i-1].end
 *   the previous meeting has not finished when this one begins ->
 *   return false immediately. Half-open semantics -> strict '<'.
 *   Time  Complexity : O(n log n) — sort dominates.
 *   Space Complexity : O(1) — in-place sort, one counter.
 * ---------------------------------------------------------------------
 * APPROACH 2 — Chronological event sweep (sweep-line)
 *   Flatten every meeting into two events: (start, +1) and (end, -1).
 *   Sort events by time — with ENDS before STARTS at the same time
 *   (half-open: a meeting ending at t is free at t). Sweep: active
 *   += delta; if active ever reaches 2, two meetings are live at once.
 *   Time  Complexity : O(n log n) — sorting 2n events.
 *   Space Complexity : O(n) — the event list (2n entries).
 * ---------------------------------------------------------------------
 * DATA STRUCTURE DEEP DIVE — sweep-line, the master pattern
 *   The sweep line turns "do intervals overlap anywhere?" into
 *   "does the counter ever exceed 1?". Every interval adds +1 at its
 *   start and -1 at its end; between events the answer is constant.
 *   Tie-breaking encodes the interval semantics:
 *     closed  [a,b] : +1 before -1 (they overlap at the shared point)
 *     half-open [a,b): -1 before +1 (ending at b frees the room at b)
 *   This same event trick powers Meeting Rooms II (count rooms),
 *   skyline problems, and calendar clash detectors. The C++ pair
 *   sort (time, then kind) gives you the tie-break for free.
 * =====================================================================
 */

#include <vector>         // std::vector — intervals + events
#include <utility>        // std::pair — (time, delta) events
#include <algorithm>      // std::sort
#include <chrono>         // std::chrono — benchmark timing
#include <iostream>       // std::cout — printing results
#include <sys/resource.h> // getrusage — peak RAM measurement

/* =====================================================================
 * APPROACH 1 : sort by start, check adjacent overlaps
 * ===================================================================== */
class Solution_1 {
public:
    /*
     * Purpose : Report whether all meetings fit one room.
     * Inputs  : intervals — [start, end) meetings, end may equal start.
     * Output  : true iff no two meetings overlap.
     */
    bool canAttendMeetings(std::vector<std::vector<int>>& intervals) {
        // Sort by start time — overlaps become adjacent afterwards.
        std::sort(intervals.begin(), intervals.end());
        for (int i = 1; i < static_cast<int>(intervals.size()); ++i) {
            // Half-open: next meeting starts BEFORE previous ends -> clash.
            if (intervals[i][0] < intervals[i - 1][1]) {
                return false;
            }
        }
        return true;
    }
};

/* =====================================================================
 * APPROACH 2 : chronological event sweep (sweep-line)
 * ===================================================================== */
class Solution_2 {
public:
    /*
     * Purpose : Report whether all meetings fit one room (event sweep).
     * Inputs  : intervals — [start, end) meetings.
     * Output  : true iff no two meetings overlap.
     */
    bool canAttendMeetings(std::vector<std::vector<int>>& intervals) {
        // events: (time, delta). kind encodes tie-break order: use
        // 0 for END (-1) and 1 for START (+1) so ends sort first.
        std::vector<std::pair<int, int>> events;
        events.reserve(intervals.size() * 2);
        for (const std::vector<int>& it : intervals) {
            events.push_back({it[0], 1}); // start  : +1 active, tie kind 1
            events.push_back({it[1], 0}); // end    : -1 active, tie kind 0
        }
        // Second element 0 (end) before 1 (start) at equal times.
        std::sort(events.begin(), events.end());

        int active = 0;
        for (const std::pair<int, int>& ev : events) {
            active += (ev.second == 1) ? 1 : -1;
            if (active > 1) return false; // two meetings live simultaneously
        }
        return true;
    }
};

/* =====================================================================
 * BENCHMARK — run both approaches on 3 tests, verify + time + RAM
 * ===================================================================== */
int main() {
    std::vector<std::vector<std::vector<int>>> tests = {
        {{0, 30}, {5, 10}, {15, 20}},               // false — [5,10] inside [0,30]
        {{7, 10}, {2, 4}},                          // true  — disjoint
        {{0, 5}, {5, 10}, {10, 15}, {3, 8}}         // false — chain + [3,8]
    };

    // brute force: any pair (i, j) with i.start < j.end && j.start < i.end
    // (half-open semantics: strict both sides) -> overlap
    auto brute = [](const std::vector<std::vector<int>>& ivs) {
        for (size_t i = 0; i < ivs.size(); ++i)
            for (size_t j = i + 1; j < ivs.size(); ++j)
                if (ivs[i][0] < ivs[j][1] && ivs[j][0] < ivs[i][1])
                    return false;
        return true;
    };

    bool allPass = true;
    for (size_t t = 0; t < tests.size(); ++t) {

        std::vector<std::vector<int>> in1 = tests[t];
        struct rusage b1, a1;
        getrusage(RUSAGE_SELF, &b1);
        auto s1 = std::chrono::high_resolution_clock::now();
        bool r1 = Solution_1().canAttendMeetings(in1);
        auto e1 = std::chrono::high_resolution_clock::now();
        getrusage(RUSAGE_SELF, &a1);
        double us1 = std::chrono::duration_cast<std::chrono::nanoseconds>(e1 - s1).count() / 1000.0;
        long kb1 = a1.ru_maxrss - b1.ru_maxrss;
        bool ok1 = r1 == brute(tests[t]);

        std::vector<std::vector<int>> in2 = tests[t];
        struct rusage b2, a2;
        getrusage(RUSAGE_SELF, &b2);
        auto s2 = std::chrono::high_resolution_clock::now();
        bool r2 = Solution_2().canAttendMeetings(in2);
        auto e2 = std::chrono::high_resolution_clock::now();
        getrusage(RUSAGE_SELF, &a2);
        double us2 = std::chrono::duration_cast<std::chrono::nanoseconds>(e2 - s2).count() / 1000.0;
        long kb2 = a2.ru_maxrss - b2.ru_maxrss;
        bool ok2 = r2 == brute(tests[t]);

        bool pass = ok1 && ok2;
        allPass = allPass && pass;
        std::cout << "Test " << (t + 1) << " : "
                  << (pass ? "PASS" : "FAIL")
                  << "  A1=" << us1 << "us/" << kb1 << "KB  A2=" << us2 << "us/" << kb2 << "KB  "
                  << "canAttend=" << (r1 ? "true" : "false") << "\n";
    }
    std::cout << (allPass ? "PASS : both approaches agree with the brute-force overlap check."
                          : "FAIL : at least one approach disagrees with brute force.")
              << "\n";
    return allPass ? 0 : 1;
}