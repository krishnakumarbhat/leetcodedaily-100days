"""LeetCode 208: Implement Trie (Prefix Tree) - Medium"""
import time, tracemalloc

# Variation 1: HashMap-based TrieNode
class TrieNode_v1:
    def __init__(self):
        self.children = {}
        self.end = False

class Trie_v1:
    def __init__(self): self.root = TrieNode_v1()
    def insert(self, word):
        node = self.root
        for c in word:
            if c not in node.children: node.children[c] = TrieNode_v1()
            node = node.children[c]
        node.end = True
    def search(self, word):
        node = self.root
        for c in word:
            if c not in node.children: return False
            node = node.children[c]
        return node.end
    def startsWith(self, prefix):
        node = self.root
        for c in prefix:
            if c not in node.children: return False
            node = node.children[c]
        return True

# Variation 2: Array-based TrieNode (26 fixed slots, faster for lowercase letters)
class TrieNode_v2:
    def __init__(self):
        self.children = [None] * 26
        self.end = False

class Trie_v2:
    def __init__(self): self.root = TrieNode_v2()
    def insert(self, word):
        node = self.root
        for c in word:
            i = ord(c) - ord('a')
            if not node.children[i]: node.children[i] = TrieNode_v2()
            node = node.children[i]
        node.end = True
    def search(self, word):
        node = self.root
        for c in word:
            i = ord(c) - ord('a')
            if not node.children[i]: return False
            node = node.children[i]
        return node.end
    def startsWith(self, prefix):
        node = self.root
        for c in prefix:
            i = ord(c) - ord('a')
            if not node.children[i]: return False
            node = node.children[i]
        return True

if __name__ == "__main__":
    words = ["apple", "app", "application", "apply", "banana"]
    for Vi, Cls in enumerate([Trie_v1, Trie_v2], 1):
        tracemalloc.start(); t0 = time.perf_counter()
        t = Cls()
        for w in words: t.insert(w)
        r1 = t.search("apple"); r2 = t.search("app"); r3 = t.startsWith("app"); r4 = t.search("appl")
        t1 = time.perf_counter(); mem = tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{Vi}: search=({r1},{r2},{r4}), startsWith={r3}, mem={mem}bytes, time={(t1-t0)*1e6:.2f}us")
# var1 mem = {} and time = {}
# var2 mem = {} and time = {}
