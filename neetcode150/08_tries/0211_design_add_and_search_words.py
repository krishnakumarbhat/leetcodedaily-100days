"""LeetCode 211: Design Add and Search Words Data Structure - Medium"""
import time, tracemalloc

class TrieNode:
    def __init__(self):
        self.children = {}
        self.end = False

# Variation 1: DFS with '.' wildcard matching
class WordDictionary_v1:
    def __init__(self): self.root = TrieNode()
    def addWord(self, word):
        node = self.root
        for c in word:
            if c not in node.children: node.children[c] = TrieNode()
            node = node.children[c]
        node.end = True
    def search(self, word):
        def dfs(node, i):
            if i == len(word): return node.end
            if word[i] == '.':
                return any(dfs(child, i+1) for child in node.children.values())
            if word[i] not in node.children: return False
            return dfs(node.children[word[i]], i+1)
        return dfs(self.root, 0)

# Variation 2: Iterative BFS approach for wildcard
class WordDictionary_v2:
    def __init__(self): self.root = TrieNode()
    def addWord(self, word):
        node = self.root
        for c in word:
            if c not in node.children: node.children[c] = TrieNode()
            node = node.children[c]
        node.end = True
    def search(self, word):
        from collections import deque
        q = deque([self.root])
        for c in word:
            nxt = deque()
            while q:
                node = q.popleft()
                if c == '.':
                    for child in node.children.values(): nxt.append(child)
                elif c in node.children:
                    nxt.append(node.children[c])
            q = nxt
        return any(node.end for node in q)

if __name__ == "__main__":
    test_add = ["bad", "dad", "mad", "pad"]
    test_search = [".ad", "b..", "ba.", "pad", "bad", "xyz"]
    for Vi, Cls in enumerate([WordDictionary_v1, WordDictionary_v2], 1):
        tracemalloc.start(); t0 = time.perf_counter()
        wd = Cls()
        for w in test_add: wd.addWord(w)
        results = [wd.search(s) for s in test_search]
        t1 = time.perf_counter(); mem = tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{Vi}: {dict(zip(test_search, results))}, mem={mem}bytes, time={(t1-t0)*1e6:.2f}us")
# var1 mem = {} and time = {}
# var2 mem = {} and time = {}
