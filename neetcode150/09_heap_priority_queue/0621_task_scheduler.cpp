/*
 * =====================================================================
 * LeetCode 621 : Task Scheduler                                    (Medium)
 * https://leetcode.com/problems/task-scheduler/
 * Category   : Heap / Priority queue / greedy
 * ---------------------------------------------------------------------
 * PROBLEM
 *   Given tasks labeled 'A'..'Z' and a cooldown n (same task cannot
 *   run twice within n steps), schedule the tasks so the CPU is busy
 *   as soon as possible — return the minimum number of time units.
 *   Idle slots are allowed.
 * ---------------------------------------------------------------------
 * INTUITION
 *   The tasks with the HIGHEST frequency dominate the schedule: the
 *   only reason to add idle time is to satisfy the cooldown of the
 *   most frequent task. Two clean views:
 *   (a) formula — count of max-frequency tasks determines the core;
 *   (b) simulation — a max-heap + cooldown queue mimics the CPU.
 * ---------------------------------------------------------------------
 * APPROACH 1 · Math formula (O(n), best)
 *   Let m = max frequency, c = how many tasks share it.
 *   frames = (m - 1) * (n + 1) + c  ⇒ answer = max(frames, tasks.size()).
 * APPROACH 2 · Heap simulation (O(26 log 26))
 *   Each second pop the most frequent available task, push it to a
 *   cooldown FIFO, re-add after n seconds. Idle when the heap is empty.
 * ---------------------------------------------------------------------
 * DEEP DIVE · Why the formula works
 *   The busiest task T with frequency m needs at least m slots; its
 *   (m-1) gaps between occurrences each demand n idle/other-task slots.
 *   Filling those gaps with other tasks (c tasks tie with T: they can
 *   fill the LAST slot row) is always possible greedily, so the bound
 *   is exact — the answer is just the larger of this schedule skeleton
 *   and the raw task count. This is why O(1) beats any heap version.
 * ---------------------------------------------------------------------
 * TIME COMPLEXITY : O(1) — one pass over 26 counters.
 * MEMORY COMPLEXITY: O(1).
 * =====================================================================
 */
#include <iostream>
#include <vector>
#include <string>
#include <queue>
#include <array>
#include <algorithm>
#include <chrono>
#include <sys/resource.h>

class Solution_1 {
public:
    int leastInterval(std::vector<char>& tasks, int n) {
        std::array<int, 26> cnt{};
        for (char t : tasks) ++cnt[t - 'A'];
        int m = *std::max_element(cnt.begin(), cnt.end());
        int c = static_cast<int>(std::count(cnt.begin(), cnt.end(), m));
        int frames = (m - 1) * (n + 1) + c;          // skeleton w/ idle gaps
        return std::max(frames, static_cast<int>(tasks.size()));
    }
};

class Solution_2 {
public:
    int leastInterval(std::vector<char>& tasks, int n) {
        std::array<int, 26> cnt{};
        for (char t : tasks) ++cnt[t - 'A'];
        std::priority_queue<int> heap;               // max-heap of counts
        for (int x : cnt) if (x) heap.push(x);
        int time = 0;
        std::queue<std::pair<int,int>> cooldown;     // (count, readyAt)
        while (!heap.empty() || !cooldown.empty()) {
            ++time;
            if (!heap.empty()) {
                int c = heap.top() - 1; heap.pop();  // run one instance
                if (c > 0) cooldown.push({c, time + n});
            }
            if (!cooldown.empty() && cooldown.front().second == time) {
                heap.push(cooldown.front().first);   // cooled down → ready
                cooldown.pop();
            }
        }
        return time;
    }
};

static long long nowUs() {
    return std::chrono::duration_cast<std::chrono::microseconds>(
        std::chrono::steady_clock::now().time_since_epoch()).count();
}
static long memKb() { struct rusage r{}; getrusage(RUSAGE_SELF, &r); return r.ru_maxrss; }

int main() {
    struct Case { std::vector<char> tasks; int n; int expect; };
    const Case cases[] = {
        {{'A','A','A','B','B','B'}, 2, 8},
        {{'A','A','A','B','B','B'}, 0, 6},
        {{'A','A','A','A','A','A','B','C','D','E','F','G'}, 2, 16},
        {{'A','B','C','D'}, 3, 4}
    };
    const long mem0 = memKb();
    auto t0 = nowUs();
    bool allOk = true;
    for (const auto& c : cases) {
        int r1 = Solution_1().leastInterval(const_cast<std::vector<char>&>(c.tasks), c.n);
        int r2 = Solution_2().leastInterval(const_cast<std::vector<char>&>(c.tasks), c.n);
        bool ok = r1 == c.expect && r2 == c.expect;
        allOk = allOk && ok;
        std::cout << "n=" << c.n << " → A1=" << r1 << " A2=" << r2
                  << " (want " << c.expect << ") " << (ok ? "PASS" : "FAIL") << "\n";
    }
    auto t1 = nowUs();
    std::cout << (allOk ? "PASS : all cases" : "FAIL") << " | time: " << (t1 - t0)
              << " us | mem: " << (memKb() - mem0) << " KB\n";
    return 0;
}
