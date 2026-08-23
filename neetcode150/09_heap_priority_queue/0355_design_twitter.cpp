/*
 * =====================================================================
 * LeetCode 355 : Design Twitter                                    (Medium)
 * https://leetcode.com/problems/design-twitter/
 * Category   : Heap / Priority queue / design
 * ---------------------------------------------------------------------
 * PROBLEM
 *   Design a mini Twitter: postTweet(user, id), getNewsFeed(user)
 *   (10 most recent tweets from the user + everyone they follow,
 *   including themselves), follow(a, b), unfollow(a, b).
 * ---------------------------------------------------------------------
 * INTUITION
 *   Store every tweet with a global increasing timestamp. For a feed,
 *   merge the k most recent tweets from each followed user with a
 *   max-heap keyed by timestamp — like merging k sorted lists.
 * ---------------------------------------------------------------------
 * APPROACH 1 · Merge-k with max-heap (best)
 *   tweets: userId → list of (time, id), pushed chronologically.
 *   For getNewsFeed: push the LATEST tweet of every followed user,
 *   pop the newest, then push that user's next-latest. Stop at 10.
 * APPROACH 2 · Naive gather + sort (baseline)
 *   Collect all tweets of all followed users, sort by time desc, cut 10.
 * ---------------------------------------------------------------------
 * DEEP DIVE · Why the heap merge beats a flat sort
 *   Flat sort: O(f · k · log(f · k)) where f = follows, k = tweets each.
 *   Merge-k only ever holds f entries in the heap: O(f·log f) per
 *   popped tweet. For heavy accounts (k large) this is the classic
 *   k-way merge win. Timestamps: we just count up, so "recent" =
 *   "largest timestamp" — no wall-clock math needed.
 * ---------------------------------------------------------------------
 * TIME COMPLEXITY : getNewsFeed O(f · log f) with f followed users.
 * MEMORY COMPLEXITY: O(T) for T stored tweets + follow maps.
 * =====================================================================
 */
#include <iostream>
#include <vector>
#include <queue>
#include <unordered_map>
#include <unordered_set>
#include <utility>
#include <algorithm>
#include <chrono>
#include <sys/resource.h>

class Solution_1 {
    struct Tweet { int time; int id; };
    std::unordered_map<int, std::vector<Tweet>> tweets_;       // author → tweets
    std::unordered_map<int, std::unordered_set<int>> follows_; // user → follows
    int clock_ = 0;
public:
    void postTweet(int userId, int tweetId) {
        tweets_[userId].push_back({clock_++, tweetId});
    }
    void follow(int followerId, int followeeId) {
        if (followerId != followeeId) follows_[followerId].insert(followeeId);
    }
    void unfollow(int followerId, int followeeId) {
        follows_[followerId].erase(followeeId);
    }
    std::vector<int> getNewsFeed(int userId) {
        // newest-first heap: (time, tweetId, author, indexOfNext)
        using Node = std::tuple<int, int, int, int>;
        std::priority_queue<Node> heap;
        auto pushUser = [&](int author) {
            auto it = tweets_.find(author);
            if (it != tweets_.end() && !it->second.empty()) {
                size_t last = it->second.size() - 1;
                heap.emplace(it->second[last].time, it->second[last].id, author,
                             static_cast<int>(last));
            }
        };
        pushUser(userId);                                      // own tweets
        for (int f : follows_[userId]) pushUser(f);            // followed users
        std::vector<int> feed;
        while (!heap.empty() && feed.size() < 10) {
            auto [time, id, author, idx] = heap.top();
            heap.pop();
            feed.push_back(id);
            if (idx > 0) {                                     // next-latest tweet
                const auto& tv = tweets_[author][idx - 1];
                heap.emplace(tv.time, tv.id, author, idx - 1);
            }
        }
        return feed;
    }
};

class Solution_2 {
    std::unordered_map<int, std::vector<std::pair<int,int>>> all_; // user → (time,id)
    std::unordered_map<int, std::unordered_set<int>> follows_;
    int clock_ = 0;
public:
    void postTweet(int userId, int tweetId) {
        all_[userId].emplace_back(clock_++, tweetId);
    }
    void follow(int followerId, int followeeId) {
        if (followerId != followeeId) follows_[followerId].insert(followeeId);
    }
    void unfollow(int followerId, int followeeId) {
        follows_[followerId].erase(followeeId);
    }
    std::vector<int> getNewsFeed(int userId) {
        std::vector<std::pair<int,int>> pool;
        auto add = [&](int author) { for (auto& p : all_[author]) pool.push_back(p); };
        add(userId);
        for (int f : follows_[userId]) add(f);
        std::sort(pool.begin(), pool.end());                   // ascending time
        std::vector<int> feed;
        for (size_t i = pool.size(); i-- > 0 && feed.size() < 10;)
            feed.push_back(pool[i].second);                    // newest first
        return feed;
    }
};

static long long nowUs() {
    return std::chrono::duration_cast<std::chrono::microseconds>(
        std::chrono::steady_clock::now().time_since_epoch()).count();
}
static long memKb() { struct rusage r{}; getrusage(RUSAGE_SELF, &r); return r.ru_maxrss; }

int main() {
    const long mem0 = memKb();
    auto t0 = nowUs();
    Solution_1 s1;
    Solution_2 s2;
    bool allOk = true;
    auto run = [&](int uid, const std::vector<int>& expect) {
        auto r1 = s1.getNewsFeed(uid);
        auto r2 = s2.getNewsFeed(uid);
        bool ok = r1 == expect && r2 == expect;
        allOk = allOk && ok;
        std::cout << "feed(" << uid << ") → [" ;
        for (size_t i = 0; i < r1.size(); ++i) std::cout << (i ? "," : "") << r1[i];
        std::cout << "] A2=[" ;
        for (size_t i = 0; i < r2.size(); ++i) std::cout << (i ? "," : "") << r2[i];
        std::cout << "] want=[" ;
        for (size_t i = 0; i < expect.size(); ++i) std::cout << (i ? "," : "") << expect[i];
        std::cout << "] " << (ok ? "PASS" : "FAIL") << "\n";
    };
    s1.postTweet(1, 5); s2.postTweet(1, 5);
    run(1, {5});
    s1.follow(1, 2); s2.follow(1, 2);
    s1.postTweet(2, 6); s2.postTweet(2, 6);
    run(1, {6, 5});
    s1.unfollow(1, 2); s2.unfollow(1, 2);
    run(1, {5});
    s1.postTweet(2, 7); s2.postTweet(2, 7);
    run(1, {5});
    auto t1 = nowUs();
    std::cout << (allOk ? "PASS : all steps" : "FAIL") << " | time: " << (t1 - t0)
              << " us | mem: " << (memKb() - mem0) << " KB\n";
    return 0;
}
