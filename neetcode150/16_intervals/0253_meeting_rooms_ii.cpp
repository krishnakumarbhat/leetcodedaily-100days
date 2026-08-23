/*
 * =====================================================================
 * LeetCode 253 : Meeting Rooms II                                (Medium)
 * https://leetcode.com/problems/meeting-rooms-ii/
 * Category   : Intervals
 * ---------------------------------------------------------------------
 * PROBLEM
 *   Given an array of meeting time intervals [start, end), return the
 *   MINIMUM number of conference rooms required. Rooms are freed at
 *   end times (half-open intervals: [0,5] and [5,10] share one room).
 * ---------------------------------------------------------------------
 * INTUITION
 *   The answer is the maximum number of meetings ALIVE at one moment
 *   ("max depth" of the schedule). To track that while sweeping by
 *   start time, we only need to know: of the meetings already opened,
 *   which one ends FIRST? A MIN-HEAP over end times answers that in
 *   O(log n) per meeting and keeps exactly the active meetings.
 * ---------------------------------------------------------------------
 * APPROACH 1 — Sort by start + min-heap of end times (BEST)
 *   Sort meetings by start. For each meeting: if the EARLIEST-ending
 *   active meeting has already finished (heap top <= start), pop it —
 *   that room is reused. Then push this meeting's end; the heap size
 *   is the number of rooms in use -> answer = max heap size.
 *   Time  Complexity : O(n log n) — sort + n heap ops of O(log n).
 *   Space Complexity : O(n) — the heap holds <= n end times.
 * ---------------------------------------------------------------------
 * APPROACH 2 — Two pointers over sorted starts & ends
 *   Sort starts and ends SEPARATELY. Walk a room counter: when the
 *   next meeting starts before the earliest free time (starts[s] <
 *   ends[e]), we need a NEW room. Otherwise reuse: the room ending at
 *   ends[e] becomes free -> advance e. Classic sweep on two channels.
 *   Time  Complexity : O(n log n) — two sorts, walk is O(n).
 *   Space Complexity : O(n) — two sorted copies.
 * ---------------------------------------------------------------------
 * DATA STRUCTURE DEEP DIVE — WHY the heap holds ACTIVE meetings
 *   A naive sweep must know "when is the next meeting over?" — a
 *   min-heap makes that its root in O(1). Crucially the heap only
 *   contains meetings whose start we HAVE seen: expired ones (root
 *   end <= current start) are popped before pushing, so heap.size()
 *   == number of concurrently open meetings — the exact quantity we
 *   maximise. Python: heapq (min-heap). C++: std::priority_queue with
 *   std::greater<int> to invert max→min. Lazy deletion is NOT needed
 *   here (we pop while root is expired, not once) — but the same
 *   pattern reappears in 1851 where expiry is checked per query.
 * =====================================================================
 */

#include <vector>         // std::vector — intervals + sorted copies
#include <queue>          // std::priority_queue — min-heap of end times
#include <algorithm>      // std::sort, std::greater
#include <functional>     // std::greater<int> — min-heap comparator
#include <chrono>         // std::chrono — benchmark timing
#include <iostream>       // std::cout — printing results
#include <sys/resource.h> // getrusage — peak RAM measurement

/* =====================================================================
 * APPROACH 1 : sort by start + min-heap of end times
 * ===================================================================== */
class Solution_1 {
public:
    /*
     * Purpose : Return the minimum number of rooms for all meetings.
     * Inputs  : intervals — [start, end) meetings.
     * Output  : int — peak number of simultaneously active meetings.
     */
    int minMeetingRooms(std::vector<std::vector<int>>& intervals) {
        std::sort(intervals.begin(), intervals.end()); // by start

        // Min-heap of END times of currently active meetings.
        std::priority_queue<int, std::vector<int>, std::greater<int>> ends;
        int rooms = 0;

        for (const std::vector<int>& it : intervals) {
            // Reuse: the active meeting that ends earliest is over
            // (or ends exactly now — half-open [s,e) frees at e).
            if (!ends.empty() && ends.top() <= it[0]) {
                ends.pop(); // that room is now free
            }
            ends.push(it[1]); // this meeting occupies a room until it[1]

            // heap size == meetings alive right now == rooms in use.
            rooms = std::max(rooms, static_cast<int>(ends.size()));
        }
        return rooms;
    }
};

/* =====================================================================
 * APPROACH 2 : two pointers over separately sorted starts/ends
 * ===================================================================== */
class Solution_2 {
public:
    /*
     * Purpose : Return the minimum number of rooms (two-pointer sweep).
     * Inputs  : intervals — [start, end) meetings.
     * Output  : int — peak number of simultaneously active meetings.
     */
    int minMeetingRooms(std::vector<std::vector<int>>& intervals) {
        std::vector<int> starts, ends;
        starts.reserve(intervals.size());
        ends.reserve(intervals.size());
        for (const std::vector<int>& it : intervals) {
            starts.push_back(it[0]);
            ends.push_back(it[1]);
        }
        std::sort(starts.begin(), starts.end());
        std::sort(ends.begin(), ends.end());

        int rooms = 0, active = 0, e = 0;
        for (int s = 0; s < static_cast<int>(starts.size()); ++s) {
            // While the earliest end frees rooms before this start,
            // close them: half-open means end <= start releases.
            while (e < static_cast<int>(ends.size()) && ends[e] <= starts[s]) {
                --active;
                ++e;
            }
            ++active; // open the current meeting
            rooms = std::max(rooms, active);
        }
        return rooms;
    }
};

/* =====================================================================
 * BENCHMARK — run both approaches on 3 tests, verify + time + RAM
 * ===================================================================== */
int main() {
    std::vector<std::vector<std::vector<int>>> tests = {
        {{0, 30}, {5, 10}, {15, 20}},                 // 2 rooms
        {{7, 10}, {2, 4}},                            // 1 room
        {{0, 5}, {5, 10}, {10, 15}, {15, 20}, {3, 8}} // 2 rooms ([3,8] overlaps two)
    };

    // brute force: max number of intervals covering any single point.
    auto brute = [](const std::vector<std::vector<int>>& ivs) {
        int best = ivs.empty() ? 0 : 1;   // every meeting needs >= 1 room
        for (size_t i = 0; i < ivs.size(); ++i) {
            int c = 0;
            for (size_t j = 0; j < ivs.size(); ++j)
                if (i != j && ivs[i][0] < ivs[j][1] && ivs[j][0] < ivs[i][1])
                    ++c; // half-open overlap with a DIFFERENT meeting
            best = std::max(best, c);
        }
        return best;
    };

    bool allPass = true;
    for (size_t t = 0; t < tests.size(); ++t) {

        std::vector<std::vector<int>> in1 = tests[t];
        struct rusage b1, a1;
        getrusage(RUSAGE_SELF, &b1);
        auto s1 = std::chrono::high_resolution_clock::now();
        int r1 = Solution_1().minMeetingRooms(in1);
        auto e1 = std::chrono::high_resolution_clock::now();
        getrusage(RUSAGE_SELF, &a1);
        double us1 = std::chrono::duration_cast<std::chrono::nanoseconds>(e1 - s1).count() / 1000.0;
        long kb1 = a1.ru_maxrss - b1.ru_maxrss;
        bool ok1 = r1 == brute(tests[t]);

        std::vector<std::vector<int>> in2 = tests[t];
        struct rusage b2, a2;
        getrusage(RUSAGE_SELF, &b2);
        auto s2 = std::chrono::high_resolution_clock::now();
        int r2 = Solution_2().minMeetingRooms(in2);
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
                  << "rooms=" << r1 << "\n";
    }
    std::cout << (allPass ? "PASS : both approaches return the brute-force peak occupancy."
                          : "FAIL : at least one approach disagrees with brute force.")
              << "\n";
    return allPass ? 0 : 1;
}