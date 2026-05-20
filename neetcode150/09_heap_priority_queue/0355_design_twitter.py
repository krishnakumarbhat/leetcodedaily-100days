"""LeetCode 355: Design Twitter - Medium"""
import time, tracemalloc
import heapq
from collections import defaultdict

# Variation 1: Heap-based news feed (merge k sorted lists)
class Twitter_v1:
    def __init__(self):
        self.time = 0
        self.tweets = defaultdict(list)   # userId -> [(ts, tweetId)]
        self.following = defaultdict(set) # userId -> {followeeId}

    def postTweet(self, userId: int, tweetId: int) -> None:
        self.time += 1
        self.tweets[userId].append((self.time, tweetId))

    def getNewsFeed(self, userId: int):
        heap = []
        users = self.following[userId] | {userId}
        for u in users:
            for ts, tid in self.tweets[u][-10:]:
                heapq.heappush(heap, (ts, tid))
        return [tid for _, tid in heapq.nlargest(10, heap)]

    def follow(self, followerId: int, followeeId: int) -> None:
        self.following[followerId].add(followeeId)

    def unfollow(self, followerId: int, followeeId: int) -> None:
        self.following[followerId].discard(followeeId)

# Variation 2: Min-heap of size 10 per user feed
class Twitter_v2:
    def __init__(self):
        self.time = 0
        self.tweets = defaultdict(list)
        self.following = defaultdict(set)

    def postTweet(self, userId: int, tweetId: int) -> None:
        self.time += 1
        self.tweets[userId].append((-self.time, tweetId))  # negate for max behavior

    def getNewsFeed(self, userId: int):
        all_tweets = []
        for u in self.following[userId] | {userId}:
            all_tweets.extend(self.tweets[u])
        all_tweets.sort()  # sort by neg time (most recent first)
        return [tid for _, tid in all_tweets[:10]]

    def follow(self, followerId: int, followeeId: int) -> None:
        self.following[followerId].add(followeeId)

    def unfollow(self, followerId: int, followeeId: int) -> None:
        self.following[followerId].discard(followeeId)

if __name__ == "__main__":
    for Vi, Cls in enumerate([Twitter_v1, Twitter_v2], 1):
        tracemalloc.start(); t0 = time.perf_counter()
        tw = Cls()
        tw.postTweet(1, 5); tw.postTweet(1, 3)
        tw.follow(1, 2); tw.postTweet(2, 6)
        f1 = tw.getNewsFeed(1)
        tw.unfollow(1, 2); f2 = tw.getNewsFeed(1)
        t1 = time.perf_counter(); mem = tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{Vi}: feed1={f1}, feed2={f2}, mem={mem}bytes, time={(t1-t0)*1e6:.2f}us")
# var1 mem = {} and time = {}
# var2 mem = {} and time = {}
