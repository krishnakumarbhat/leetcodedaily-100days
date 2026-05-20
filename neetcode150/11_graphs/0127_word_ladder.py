"""LeetCode 127: Word Ladder - Hard"""
import time, tracemalloc
from collections import deque, defaultdict

# Variation 1: BFS one-directional
class Solution_v1:
    def ladderLength(self, beginWord: str, endWord: str, wordList) -> int:
        wordSet=set(wordList)
        if endWord not in wordSet: return 0
        q=deque([(beginWord,1)])
        while q:
            word,steps=q.popleft()
            for i in range(len(word)):
                for c in "abcdefghijklmnopqrstuvwxyz":
                    nw=word[:i]+c+word[i+1:]
                    if nw==endWord: return steps+1
                    if nw in wordSet: wordSet.remove(nw); q.append((nw,steps+1))
        return 0

# Variation 2: Bidirectional BFS (faster in practice)
class Solution_v2:
    def ladderLength(self, beginWord: str, endWord: str, wordList) -> int:
        wordSet=set(wordList)
        if endWord not in wordSet: return 0
        front,back={beginWord},{endWord}
        steps=1
        while front:
            if len(front)>len(back): front,back=back,front
            nxt=set()
            for word in front:
                for i in range(len(word)):
                    for c in "abcdefghijklmnopqrstuvwxyz":
                        nw=word[:i]+c+word[i+1:]
                        if nw in back: return steps+1
                        if nw in wordSet: wordSet.discard(nw); nxt.add(nw)
            front=nxt; steps+=1
        return 0

# Variation 3: BFS with adjacency preprocessing
class Solution_v3:
    def ladderLength(self, beginWord: str, endWord: str, wordList) -> int:
        wordSet=set(wordList)
        if endWord not in wordSet: return 0
        adj=defaultdict(list)
        for w in wordList+[beginWord]:
            for i in range(len(w)): adj[w[:i]+"*"+w[i+1:]].append(w)
        q=deque([(beginWord,1)]); visited={beginWord}
        while q:
            word,steps=q.popleft()
            for i in range(len(word)):
                pat=word[:i]+"*"+word[i+1:]
                for nb in adj[pat]:
                    if nb==endWord: return steps+1
                    if nb not in visited: visited.add(nb); q.append((nb,steps+1))
        return 0

if __name__ == "__main__":
    wl=["hot","dot","dog","lot","log","cog"]
    for Vi,Cls in enumerate([Solution_v1,Solution_v2,Solution_v3],1):
        tracemalloc.start(); t0=time.perf_counter()
        r=Cls().ladderLength("hit","cog",wl[:])
        t1=time.perf_counter(); mem=tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{Vi}: length={r}, mem={mem}bytes, time={(t1-t0)*1e6:.2f}us")
# var1 mem = {} and time = {}
# var2 mem = {} and time = {}
# var3 mem = {} and time = {}
