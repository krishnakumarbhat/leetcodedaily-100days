"""
=====================================================================
LeetCode 355 : Design Twitter                                    (Medium)
https://leetcode.com/problems/design-twitter/
Category   : Heap / design
---------------------------------------------------------------------
PROBLEM
    postTweet(user, id), getNewsFeed(user) -> up to 10 most recent
    tweets of the user and everyone they follow; follow / unfollow.
---------------------------------------------------------------------
INTUITION
    Global increasing clock; each user's tweets form a chronologically
    sorted list. The feed is a k-way merge of these lists — a max-heap
    keyed by timestamp pops the newest tweet among all followed users.
---------------------------------------------------------------------
APPROACH 1 · Merge-k with a max-heap (best)
    Push the newest tweet of every followed user; pop the max; then
    push that user's next-newest; stop at 10. Heap stays ≤ #follows.
APPROACH 2 · Gather-all + sort (baseline)
    Collect every tweet of every followed user, sort by time desc.
---------------------------------------------------------------------
DEEP DIVE · k-way merge vs flat sort
    Flat: O(F·K log(F·K)) with F follows and K tweets each. Merge-k:
    O(F log F) per popped tweet — the classic external-sort pattern.
    Ties: we never pop more than one tweet of a user before its
    successor enters the heap, so ordering stays strictly chronological.
    The clock counts up per post, so "most recent" == "largest clock".
---------------------------------------------------------------------
TIME COMPLEXITY : getNewsFeed O(F log F); post/follow O(1).
MEMORY COMPLEXITY: O(T) for T tweets + follow edges.
=====================================================================
"""
import heapq, time, tracemalloc, collections


class Solution_1:
    """Merge-k feed with a max-heap of per-user tweet cursors."""

    def __init__(self):
        self.tweets = collections.defaultdict(list)   # user -> [(clock, id)]
        self.follows = collections.defaultdict(set)
        self.clock = 0

    def postTweet(self, userId, tweetId):
        self.tweets[userId].append((self.clock, tweetId))
        self.clock += 1

    def follow(self, followerId, followeeId):
        if followerId != followeeId:
            self.follows[followerId].add(followeeId)

    def unfollow(self, followerId, followeeId):
        self.follows[followerId].discard(followeeId)

    def getNewsFeed(self, userId):
        heap = []                                  # (-clock, id, author, idx)
        for author in {userId} | set(self.follows[userId]):
            tv = self.tweets[author]
            if tv:
                c, tid = tv[-1]
                heap.append((-c, tid, author, len(tv) - 1))
        heapq.heapify(heap)
        feed = []
        while heap and len(feed) < 10:
            neg_c, tid, author, idx = heapq.heappop(heap)
            feed.append(tid)
            if idx > 0:
                c, nid = self.tweets[author][idx - 1]
                heapq.heappush(heap, (-c, nid, author, idx - 1))
        return feed


class Solution_2:
    """Baseline: gather all tweets and sort."""

    def __init__(self):
        self.all = collections.defaultdict(list)
        self.follows = collections.defaultdict(set)
        self.clock = 0

    def postTweet(self, userId, tweetId):
        self.all[userId].append((self.clock, tweetId))
        self.clock += 1

    def follow(self, followerId, followeeId):
        if followerId != followeeId:
            self.follows[followerId].add(followeeId)

    def unfollow(self, followerId, followeeId):
        self.follows[followerId].discard(followeeId)

    def getNewsFeed(self, userId):
        pool = []
        for author in {userId} | set(self.follows[userId]):
            pool.extend(self.all[author])
        pool.sort()
        return [tid for _, tid in pool[-10:]][::-1]


if __name__ == "__main__":
    tracemalloc.start()
    t0 = time.perf_counter()
    s1, s2 = Solution_1(), Solution_2()
    ok = True


    def run(uid, want):
        global ok
        r1, r2 = s1.getNewsFeed(uid), s2.getNewsFeed(uid)
        ok &= r1 == want and r2 == want
        print(f"feed({uid}) -> {r1} want {want} {'PASS' if r1 == want and r2 == want else 'FAIL'}")


    s1.postTweet(1, 5); s2.postTweet(1, 5)
    run(1, [5])
    s1.follow(1, 2); s2.follow(1, 2)
    s1.postTweet(2, 6); s2.postTweet(2, 6)
    run(1, [6, 5])
    s1.unfollow(1, 2); s2.unfollow(1, 2)
    run(1, [5])
    s1.postTweet(2, 7); s2.postTweet(2, 7)
    run(1, [5])
    dt = time.perf_counter() - t0
    mem = tracemalloc.get_traced_memory()[1] / 1024
    tracemalloc.stop()
    print(f"{'PASS : all steps' if ok else 'FAIL'} | time: {dt * 1e6:.0f} us | mem: {mem:.0f} KB")
