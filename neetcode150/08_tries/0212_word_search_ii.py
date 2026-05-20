"""LeetCode 212: Word Search II - Hard"""
import time, tracemalloc
from typing import List

class TrieNode:
    def __init__(self):
        self.children = {}
        self.word = None
        self.refs = 0  # for pruning

# Variation 1: Trie + DFS backtracking (basic)
class Solution_v1:
    def findWords(self, board: List[List[str]], words: List[str]) -> List[str]:
        root = TrieNode()
        for w in words:
            node = root
            for c in w:
                if c not in node.children: node.children[c] = TrieNode()
                node = node.children[c]
            node.word = w
        res = []
        rows, cols = len(board), len(board[0])
        def dfs(r, c, node):
            if r < 0 or r >= rows or c < 0 or c >= cols: return
            ch = board[r][c]
            if ch not in node.children: return
            node = node.children[ch]
            if node.word:
                res.append(node.word)
                node.word = None
            board[r][c] = '#'
            for dr, dc in [(1,0),(-1,0),(0,1),(0,-1)]: dfs(r+dr, c+dc, node)
            board[r][c] = ch
        for r in range(rows):
            for c in range(cols): dfs(r, c, root)
        return res

# Variation 2: Trie + DFS with pruning (remove exhausted branches)
class Solution_v2:
    def findWords(self, board: List[List[str]], words: List[str]) -> List[str]:
        root = TrieNode()
        for w in words:
            node = root; node.refs += 1
            for c in w:
                if c not in node.children: node.children[c] = TrieNode()
                node = node.children[c]; node.refs += 1
            node.word = w
        res = []
        rows, cols = len(board), len(board[0])
        def dfs(r, c, node):
            if r < 0 or r >= rows or c < 0 or c >= cols: return
            ch = board[r][c]
            if ch not in node.children or node.children[ch].refs <= 0: return
            child = node.children[ch]
            if child.word:
                res.append(child.word)
                child.word = None
                child.refs -= 1
            board[r][c] = '#'
            for dr, dc in [(1,0),(-1,0),(0,1),(0,-1)]: dfs(r+dr, c+dc, child)
            board[r][c] = ch
            if child.refs <= 0: del node.children[ch]
        for r in range(rows):
            for c in range(cols): dfs(r, c, root)
        return res

if __name__ == "__main__":
    board1 = [["o","a","a","n"],["e","t","a","e"],["i","h","k","r"],["i","f","l","v"]]
    words1 = ["oath","pea","eat","rain"]
    import copy
    for Vi, Cls in enumerate([Solution_v1, Solution_v2], 1):
        b = copy.deepcopy(board1)
        tracemalloc.start(); t0 = time.perf_counter()
        r = Cls().findWords(b, words1[:])
        t1 = time.perf_counter(); mem = tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{Vi}: {sorted(r)}, mem={mem}bytes, time={(t1-t0)*1e6:.2f}us")
# var1 mem = {} and time = {}
# var2 mem = {} and time = {}
