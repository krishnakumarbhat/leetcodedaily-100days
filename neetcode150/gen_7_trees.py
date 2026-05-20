#!/usr/bin/env python3
"""Generator for Section 7: Trees (15 problems)"""
import os
B = "/media/pope/projecteo/github_proj/leetcode/neetcode150/07_trees"
def w(name, content):
    os.makedirs(B, exist_ok=True)
    with open(f"{B}/{name}", 'w') as f: f.write(content)

# Helper template for Python tree problems
PY_TREE_HELPER = '''import time, tracemalloc
from typing import List, Optional
from collections import deque
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val; self.left = left; self.right = right
def build(vals):
    if not vals: return None
    root = TreeNode(vals[0]); queue = deque([root]); i = 1
    while queue and i < len(vals):
        node = queue.popleft()
        if i < len(vals) and vals[i] is not None:
            node.left = TreeNode(vals[i]); queue.append(node.left)
        i += 1
        if i < len(vals) and vals[i] is not None:
            node.right = TreeNode(vals[i]); queue.append(node.right)
        i += 1
    return root
'''

CPP_TREE_HELPER = '''#include <bits/stdc++.h>
#include <chrono>
using namespace std;
struct TreeNode { int val; TreeNode *left, *right; TreeNode(int x):val(x),left(nullptr),right(nullptr){} };
TreeNode* build(vector<int> v) {
    if(v.empty()) return nullptr;
    auto root=new TreeNode(v[0]); queue<TreeNode*> q; q.push(root);
    for(int i=1;i<v.size();i+=2){
        auto n=q.front(); q.pop();
        if(i<v.size()&&v[i]!=-1){n->left=new TreeNode(v[i]);q.push(n->left);}
        if(i+1<v.size()&&v[i+1]!=-1){n->right=new TreeNode(v[i+1]);q.push(n->right);}
    }
    return root;
}
'''

w("0226_invert_binary_tree.py", f'''"""LeetCode 226: Invert Binary Tree - Easy"""
{PY_TREE_HELPER}
# ============= Variation 1: Recursive (DFS) =============
# Time: O(n)   Space: O(h)
class Solution_v1:
    def invertTree(self, root):
        if not root: return None
        root.left, root.right = self.invertTree(root.right), self.invertTree(root.left)
        return root

# ============= Variation 2: Iterative (BFS) =============
# Time: O(n)   Space: O(n)
class Solution_v2:
    def invertTree(self, root):
        if not root: return None
        queue = deque([root])
        while queue:
            node = queue.popleft()
            node.left, node.right = node.right, node.left
            if node.left: queue.append(node.left)
            if node.right: queue.append(node.right)
        return root

# ============= Variation 3: Iterative (Stack/DFS) =============
# Time: O(n)   Space: O(h)
class Solution_v3:
    def invertTree(self, root):
        if not root: return None
        stack = [root]
        while stack:
            node = stack.pop()
            node.left, node.right = node.right, node.left
            if node.left: stack.append(node.left)
            if node.right: stack.append(node.right)
        return root

if __name__ == "__main__":
    data = [4,2,7,1,3,6,9]
    for i,(S,n) in enumerate(zip([Solution_v1,Solution_v2,Solution_v3],["DFS","BFS","Stack"]),1):
        tracemalloc.start(); t0=time.perf_counter()
        S().invertTree(build(data))
        t1=time.perf_counter(); mem=tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{{i}} ({{n}}): mem = {{mem}} bytes, time = {{(t1-t0)*1e6:.2f}} us")
# var1 mem = {{}} and time = {{}}
# var2 mem = {{}} and time = {{}}
# var3 mem = {{}} and time = {{}}
''')

w("0226_invert_binary_tree.cpp", f'''/* LeetCode 226: Invert Binary Tree - Easy */
{CPP_TREE_HELPER}
class Solution_v1 {{
public:
    TreeNode* invertTree(TreeNode* root) {{
        if(!root) return nullptr;
        swap(root->left, root->right);
        invertTree(root->left); invertTree(root->right);
        return root;
    }}
}};
class Solution_v2 {{
public:
    TreeNode* invertTree(TreeNode* root) {{
        if(!root) return nullptr;
        queue<TreeNode*> q; q.push(root);
        while(!q.empty()){{ auto n=q.front(); q.pop(); swap(n->left,n->right); if(n->left) q.push(n->left); if(n->right) q.push(n->right); }}
        return root;
    }}
}};
int main(){{
    auto r=build({{4,2,7,1,3,6,9}});
    auto s=chrono::high_resolution_clock::now(); Solution_v1().invertTree(r); auto e=chrono::high_resolution_clock::now();
    cout<<"var1 (DFS): "<<chrono::duration_cast<chrono::nanoseconds>(e-s).count()/1000.0<<" us"<<endl;
    return 0;
}}
// var1 mem = {{}} and time = {{}}
// var2 mem = {{}} and time = {{}}
''')

w("0104_maximum_depth_of_binary_tree.py", f'''"""LeetCode 104: Maximum Depth of Binary Tree - Easy"""
{PY_TREE_HELPER}
# ============= Variation 1: Recursive DFS =============
# Time: O(n)   Space: O(h)
class Solution_v1:
    def maxDepth(self, root): return 0 if not root else 1+max(self.maxDepth(root.left),self.maxDepth(root.right))

# ============= Variation 2: BFS =============
# Time: O(n)   Space: O(n)
class Solution_v2:
    def maxDepth(self, root):
        if not root: return 0
        q = deque([root]); depth = 0
        while q:
            depth += 1
            for _ in range(len(q)):
                n = q.popleft()
                if n.left: q.append(n.left)
                if n.right: q.append(n.right)
        return depth

# ============= Variation 3: Iterative DFS =============
# Time: O(n)   Space: O(h)
class Solution_v3:
    def maxDepth(self, root):
        if not root: return 0
        stack = [(root, 1)]; mx = 0
        while stack:
            node, d = stack.pop(); mx = max(mx, d)
            if node.left: stack.append((node.left, d+1))
            if node.right: stack.append((node.right, d+1))
        return mx

if __name__ == "__main__":
    data = [3,9,20,None,None,15,7]
    for i,(S,n) in enumerate(zip([Solution_v1,Solution_v2,Solution_v3],["RecDFS","BFS","IterDFS"]),1):
        tracemalloc.start(); t0=time.perf_counter(); r=S().maxDepth(build(data))
        t1=time.perf_counter(); mem=tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{{i}} ({{n}}): result={{r}}, mem = {{mem}} bytes, time = {{(t1-t0)*1e6:.2f}} us")
# var1 mem = {{}} and time = {{}}
# var2 mem = {{}} and time = {{}}
# var3 mem = {{}} and time = {{}}
''')

w("0104_maximum_depth_of_binary_tree.cpp", f'''/* LeetCode 104: Maximum Depth of Binary Tree - Easy */
{CPP_TREE_HELPER}
class Solution {{ public: int maxDepth(TreeNode* r) {{ return r?1+max(maxDepth(r->left),maxDepth(r->right)):0; }} }};
int main(){{ auto r=build({{3,9,20,-1,-1,15,7}}); auto s=chrono::high_resolution_clock::now(); cout<<"var1: "<<Solution().maxDepth(r); auto e=chrono::high_resolution_clock::now(); cout<<", "<<chrono::duration_cast<chrono::nanoseconds>(e-s).count()/1000.0<<" us"<<endl; }}
// var1 mem = {{}} and time = {{}}
''')

w("0543_diameter_of_binary_tree.py", f'''"""LeetCode 543: Diameter of Binary Tree - Easy"""
{PY_TREE_HELPER}
class Solution_v1:
    def diameterOfBinaryTree(self, root):
        self.res = 0
        def dfs(node):
            if not node: return 0
            l, r = dfs(node.left), dfs(node.right)
            self.res = max(self.res, l + r); return 1 + max(l, r)
        dfs(root); return self.res
if __name__ == "__main__":
    tracemalloc.start(); t0=time.perf_counter(); r=Solution_v1().diameterOfBinaryTree(build([1,2,3,4,5]))
    t1=time.perf_counter(); mem=tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
    print(f"var1 (DFS): result={{r}}, mem = {{mem}} bytes, time = {{(t1-t0)*1e6:.2f}} us")
# var1 mem = {{}} and time = {{}}
''')

w("0543_diameter_of_binary_tree.cpp", f'''/* LeetCode 543: Diameter of Binary Tree - Easy */
{CPP_TREE_HELPER}
class Solution {{ int res=0; int dfs(TreeNode* n){{ if(!n) return 0; int l=dfs(n->left),r=dfs(n->right); res=max(res,l+r); return 1+max(l,r); }}
public: int diameterOfBinaryTree(TreeNode* r){{ res=0; dfs(r); return res; }} }};
int main(){{ auto r=build({{1,2,3,4,5}}); auto s=chrono::high_resolution_clock::now(); cout<<"var1: "<<Solution().diameterOfBinaryTree(r); auto e=chrono::high_resolution_clock::now(); cout<<", "<<chrono::duration_cast<chrono::nanoseconds>(e-s).count()/1000.0<<" us"<<endl; }}
// var1 mem = {{}} and time = {{}}
''')

w("0110_balanced_binary_tree.py", f'''"""LeetCode 110: Balanced Binary Tree - Easy"""
{PY_TREE_HELPER}
class Solution_v1:
    def isBalanced(self, root):
        def dfs(node):
            if not node: return 0
            l, r = dfs(node.left), dfs(node.right)
            if l == -1 or r == -1 or abs(l - r) > 1: return -1
            return 1 + max(l, r)
        return dfs(root) != -1
if __name__ == "__main__":
    tracemalloc.start(); t0=time.perf_counter(); r=Solution_v1().isBalanced(build([3,9,20,None,None,15,7]))
    t1=time.perf_counter(); mem=tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
    print(f"var1: result={{r}}, mem = {{mem}} bytes, time = {{(t1-t0)*1e6:.2f}} us")
# var1 mem = {{}} and time = {{}}
''')

w("0110_balanced_binary_tree.cpp", f'''/* LeetCode 110: Balanced Binary Tree - Easy */
{CPP_TREE_HELPER}
class Solution {{ int dfs(TreeNode* n){{ if(!n) return 0; int l=dfs(n->left),r=dfs(n->right); if(l==-1||r==-1||abs(l-r)>1) return -1; return 1+max(l,r); }}
public: bool isBalanced(TreeNode* r){{ return dfs(r)!=-1; }} }};
int main(){{ auto r=build({{3,9,20,-1,-1,15,7}}); auto s=chrono::high_resolution_clock::now(); cout<<"var1: "<<Solution().isBalanced(r); auto e=chrono::high_resolution_clock::now(); cout<<", "<<chrono::duration_cast<chrono::nanoseconds>(e-s).count()/1000.0<<" us"<<endl; }}
// var1 mem = {{}} and time = {{}}
''')

w("0100_same_tree.py", f'''"""LeetCode 100: Same Tree - Easy"""
{PY_TREE_HELPER}
class Solution_v1:
    def isSameTree(self, p, q):
        if not p and not q: return True
        if not p or not q or p.val != q.val: return False
        return self.isSameTree(p.left, q.left) and self.isSameTree(p.right, q.right)
class Solution_v2:
    def isSameTree(self, p, q):
        stack = [(p, q)]
        while stack:
            a, b = stack.pop()
            if not a and not b: continue
            if not a or not b or a.val != b.val: return False
            stack.append((a.left, b.left)); stack.append((a.right, b.right))
        return True
if __name__ == "__main__":
    for i,(S,n) in enumerate(zip([Solution_v1,Solution_v2],["Recursive","Iterative"]),1):
        tracemalloc.start(); t0=time.perf_counter(); r=S().isSameTree(build([1,2,3]),build([1,2,3]))
        t1=time.perf_counter(); mem=tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{{i}} ({{n}}): result={{r}}, mem = {{mem}} bytes, time = {{(t1-t0)*1e6:.2f}} us")
# var1 mem = {{}} and time = {{}}
# var2 mem = {{}} and time = {{}}
''')

w("0100_same_tree.cpp", f'''/* LeetCode 100: Same Tree - Easy */
{CPP_TREE_HELPER}
class Solution {{ public: bool isSameTree(TreeNode* p, TreeNode* q) {{ if(!p&&!q) return true; if(!p||!q||p->val!=q->val) return false; return isSameTree(p->left,q->left)&&isSameTree(p->right,q->right); }} }};
int main(){{ auto s=chrono::high_resolution_clock::now(); cout<<Solution().isSameTree(build({{1,2,3}}),build({{1,2,3}})); auto e=chrono::high_resolution_clock::now(); cout<<", "<<chrono::duration_cast<chrono::nanoseconds>(e-s).count()/1000.0<<" us"<<endl; }}
// var1 mem = {{}} and time = {{}}
''')

w("0572_subtree_of_another_tree.py", f'''"""LeetCode 572: Subtree of Another Tree - Easy"""
{PY_TREE_HELPER}
class Solution_v1:
    def isSubtree(self, root, subRoot):
        if not root: return False
        if self._same(root, subRoot): return True
        return self.isSubtree(root.left, subRoot) or self.isSubtree(root.right, subRoot)
    def _same(self, p, q):
        if not p and not q: return True
        if not p or not q or p.val != q.val: return False
        return self._same(p.left, q.left) and self._same(p.right, q.right)
if __name__ == "__main__":
    tracemalloc.start(); t0=time.perf_counter(); r=Solution_v1().isSubtree(build([3,4,5,1,2]),build([4,1,2]))
    t1=time.perf_counter(); mem=tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
    print(f"var1: result={{r}}, mem = {{mem}} bytes, time = {{(t1-t0)*1e6:.2f}} us")
# var1 mem = {{}} and time = {{}}
''')

w("0572_subtree_of_another_tree.cpp", f'''/* LeetCode 572: Subtree of Another Tree - Easy */
{CPP_TREE_HELPER}
class Solution {{ bool same(TreeNode*p,TreeNode*q){{ if(!p&&!q) return true; if(!p||!q||p->val!=q->val) return false; return same(p->left,q->left)&&same(p->right,q->right); }}
public: bool isSubtree(TreeNode*r,TreeNode*s){{ if(!r) return false; if(same(r,s)) return true; return isSubtree(r->left,s)||isSubtree(r->right,s); }} }};
int main(){{ auto s=chrono::high_resolution_clock::now(); cout<<Solution().isSubtree(build({{3,4,5,1,2}}),build({{4,1,2}})); auto e=chrono::high_resolution_clock::now(); cout<<", "<<chrono::duration_cast<chrono::nanoseconds>(e-s).count()/1000.0<<" us"<<endl; }}
// var1 mem = {{}} and time = {{}}
''')

w("0235_lowest_common_ancestor_of_bst.py", f'''"""LeetCode 235: Lowest Common Ancestor of BST - Medium"""
{PY_TREE_HELPER}
class Solution_v1:
    def lowestCommonAncestor(self, root, p, q):
        while root:
            if p.val < root.val and q.val < root.val: root = root.left
            elif p.val > root.val and q.val > root.val: root = root.right
            else: return root
class Solution_v2:
    def lowestCommonAncestor(self, root, p, q):
        if not root: return None
        if p.val < root.val and q.val < root.val: return self.lowestCommonAncestor(root.left, p, q)
        if p.val > root.val and q.val > root.val: return self.lowestCommonAncestor(root.right, p, q)
        return root
if __name__ == "__main__":
    root = build([6,2,8,0,4,7,9,None,None,3,5]); p = root.left; q = root.right
    for i,(S,n) in enumerate(zip([Solution_v1,Solution_v2],["Iterative","Recursive"]),1):
        tracemalloc.start(); t0=time.perf_counter(); r=S().lowestCommonAncestor(build([6,2,8,0,4,7,9,None,None,3,5]),TreeNode(2),TreeNode(8))
        t1=time.perf_counter(); mem=tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{{i}} ({{n}}): result={{r.val if r else None}}, mem = {{mem}} bytes, time = {{(t1-t0)*1e6:.2f}} us")
# var1 mem = {{}} and time = {{}}
# var2 mem = {{}} and time = {{}}
''')

w("0235_lowest_common_ancestor_of_bst.cpp", f'''/* LeetCode 235: LCA of BST - Medium */
{CPP_TREE_HELPER}
class Solution {{ public: TreeNode* lowestCommonAncestor(TreeNode* r, TreeNode* p, TreeNode* q) {{ while(r){{ if(p->val<r->val&&q->val<r->val) r=r->left; else if(p->val>r->val&&q->val>r->val) r=r->right; else return r; }} return nullptr; }} }};
int main(){{ auto r=build({{6,2,8,0,4,7,9}}); auto p=r->left; auto q=r->right; auto s=chrono::high_resolution_clock::now(); auto a=Solution().lowestCommonAncestor(r,p,q); auto e=chrono::high_resolution_clock::now(); cout<<"var1: "<<a->val<<", "<<chrono::duration_cast<chrono::nanoseconds>(e-s).count()/1000.0<<" us"<<endl; }}
// var1 mem = {{}} and time = {{}}
''')

w("0102_binary_tree_level_order_traversal.py", f'''"""LeetCode 102: Binary Tree Level Order Traversal - Medium"""
{PY_TREE_HELPER}
class Solution_v1:
    def levelOrder(self, root):
        if not root: return []
        result, queue = [], deque([root])
        while queue:
            level = []
            for _ in range(len(queue)):
                node = queue.popleft(); level.append(node.val)
                if node.left: queue.append(node.left)
                if node.right: queue.append(node.right)
            result.append(level)
        return result
class Solution_v2:
    def levelOrder(self, root):
        res = []
        def dfs(node, depth):
            if not node: return
            if depth == len(res): res.append([])
            res[depth].append(node.val)
            dfs(node.left, depth+1); dfs(node.right, depth+1)
        dfs(root, 0); return res
if __name__ == "__main__":
    for i,(S,n) in enumerate(zip([Solution_v1,Solution_v2],["BFS","DFS"]),1):
        tracemalloc.start(); t0=time.perf_counter(); r=S().levelOrder(build([3,9,20,None,None,15,7]))
        t1=time.perf_counter(); mem=tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{{i}} ({{n}}): result={{r}}, mem = {{mem}} bytes, time = {{(t1-t0)*1e6:.2f}} us")
# var1 mem = {{}} and time = {{}}
# var2 mem = {{}} and time = {{}}
''')

w("0102_binary_tree_level_order_traversal.cpp", f'''/* LeetCode 102: Binary Tree Level Order Traversal - Medium */
{CPP_TREE_HELPER}
class Solution {{ public: vector<vector<int>> levelOrder(TreeNode* root) {{ vector<vector<int>> res; if(!root) return res; queue<TreeNode*> q; q.push(root); while(!q.empty()){{ int sz=q.size(); vector<int> lv; for(int i=0;i<sz;i++){{ auto n=q.front();q.pop();lv.push_back(n->val); if(n->left)q.push(n->left); if(n->right)q.push(n->right); }} res.push_back(lv); }} return res; }} }};
int main(){{ auto r=build({{3,9,20,-1,-1,15,7}}); auto s=chrono::high_resolution_clock::now(); auto res=Solution().levelOrder(r); auto e=chrono::high_resolution_clock::now(); cout<<"var1: levels="<<res.size()<<", "<<chrono::duration_cast<chrono::nanoseconds>(e-s).count()/1000.0<<" us"<<endl; }}
// var1 mem = {{}} and time = {{}}
''')

w("0199_binary_tree_right_side_view.py", f'''"""LeetCode 199: Binary Tree Right Side View - Medium"""
{PY_TREE_HELPER}
class Solution_v1:
    def rightSideView(self, root):
        if not root: return []
        result, queue = [], deque([root])
        while queue:
            for i in range(len(queue)):
                node = queue.popleft()
                if i == 0: result.append(node.val)
                if node.right: queue.append(node.right)
                if node.left: queue.append(node.left)
        return result
class Solution_v2:
    def rightSideView(self, root):
        res = []
        def dfs(node, depth):
            if not node: return
            if depth == len(res): res.append(node.val)
            dfs(node.right, depth+1); dfs(node.left, depth+1)
        dfs(root, 0); return res
if __name__ == "__main__":
    for i,(S,n) in enumerate(zip([Solution_v1,Solution_v2],["BFS","DFS"]),1):
        tracemalloc.start(); t0=time.perf_counter(); r=S().rightSideView(build([1,2,3,None,5,None,4]))
        t1=time.perf_counter(); mem=tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{{i}} ({{n}}): result={{r}}, mem = {{mem}} bytes, time = {{(t1-t0)*1e6:.2f}} us")
# var1 mem = {{}} and time = {{}}
# var2 mem = {{}} and time = {{}}
''')

w("0199_binary_tree_right_side_view.cpp", f'''/* LeetCode 199: Binary Tree Right Side View - Medium */
{CPP_TREE_HELPER}
class Solution {{ public: vector<int> rightSideView(TreeNode* root) {{ vector<int> res; if(!root) return res; queue<TreeNode*> q; q.push(root); while(!q.empty()){{ int sz=q.size(); for(int i=0;i<sz;i++){{ auto n=q.front();q.pop(); if(i==sz-1) res.push_back(n->val); if(n->left)q.push(n->left); if(n->right)q.push(n->right); }} }} return res; }} }};
int main(){{ auto r=build({{1,2,3,-1,5,-1,4}}); auto s=chrono::high_resolution_clock::now(); auto res=Solution().rightSideView(r); auto e=chrono::high_resolution_clock::now(); cout<<"var1: "<<chrono::duration_cast<chrono::nanoseconds>(e-s).count()/1000.0<<" us"<<endl; }}
// var1 mem = {{}} and time = {{}}
''')

w("0098_validate_binary_search_tree.py", f'''"""LeetCode 98: Validate Binary Search Tree - Medium"""
{PY_TREE_HELPER}
class Solution_v1:
    def isValidBST(self, root):
        def valid(node, lo, hi):
            if not node: return True
            if not (lo < node.val < hi): return False
            return valid(node.left, lo, node.val) and valid(node.right, node.val, hi)
        return valid(root, float('-inf'), float('inf'))
class Solution_v2:
    def isValidBST(self, root):
        stack, prev = [], float('-inf')
        while stack or root:
            while root: stack.append(root); root = root.left
            root = stack.pop()
            if root.val <= prev: return False
            prev = root.val; root = root.right
        return True
if __name__ == "__main__":
    for i,(S,n) in enumerate(zip([Solution_v1,Solution_v2],["Recursive","Inorder"]),1):
        tracemalloc.start(); t0=time.perf_counter(); r=S().isValidBST(build([2,1,3]))
        t1=time.perf_counter(); mem=tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{{i}} ({{n}}): result={{r}}, mem = {{mem}} bytes, time = {{(t1-t0)*1e6:.2f}} us")
# var1 mem = {{}} and time = {{}}
# var2 mem = {{}} and time = {{}}
''')

w("0098_validate_binary_search_tree.cpp", f'''/* LeetCode 98: Validate BST - Medium */
{CPP_TREE_HELPER}
class Solution {{ bool valid(TreeNode* n, long lo, long hi){{ if(!n) return true; if(n->val<=lo||n->val>=hi) return false; return valid(n->left,lo,n->val)&&valid(n->right,n->val,hi); }}
public: bool isValidBST(TreeNode* r){{ return valid(r,LONG_MIN,LONG_MAX); }} }};
int main(){{ auto r=build({{2,1,3}}); auto s=chrono::high_resolution_clock::now(); cout<<Solution().isValidBST(r); auto e=chrono::high_resolution_clock::now(); cout<<", "<<chrono::duration_cast<chrono::nanoseconds>(e-s).count()/1000.0<<" us"<<endl; }}
// var1 mem = {{}} and time = {{}}
''')

w("0230_kth_smallest_element_in_bst.py", f'''"""LeetCode 230: Kth Smallest Element in a BST - Medium"""
{PY_TREE_HELPER}
class Solution_v1:
    def kthSmallest(self, root, k):
        stack = []; n = 0
        while True:
            while root: stack.append(root); root = root.left
            root = stack.pop(); n += 1
            if n == k: return root.val
            root = root.right
class Solution_v2:
    def kthSmallest(self, root, k):
        def inorder(node):
            if not node: return []
            return inorder(node.left) + [node.val] + inorder(node.right)
        return inorder(root)[k-1]
if __name__ == "__main__":
    for i,(S,n) in enumerate(zip([Solution_v1,Solution_v2],["Iterative","Recursive"]),1):
        tracemalloc.start(); t0=time.perf_counter(); r=S().kthSmallest(build([3,1,4,None,2]),1)
        t1=time.perf_counter(); mem=tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{{i}} ({{n}}): result={{r}}, mem = {{mem}} bytes, time = {{(t1-t0)*1e6:.2f}} us")
# var1 mem = {{}} and time = {{}}
# var2 mem = {{}} and time = {{}}
''')

w("0230_kth_smallest_element_in_bst.cpp", f'''/* LeetCode 230: Kth Smallest Element in BST - Medium */
{CPP_TREE_HELPER}
class Solution {{ public: int kthSmallest(TreeNode* r, int k) {{ stack<TreeNode*> st; while(true){{ while(r){{st.push(r);r=r->left;}} r=st.top();st.pop(); if(--k==0) return r->val; r=r->right; }} }} }};
int main(){{ auto r=build({{3,1,4,-1,2}}); auto s=chrono::high_resolution_clock::now(); cout<<Solution().kthSmallest(r,1); auto e=chrono::high_resolution_clock::now(); cout<<", "<<chrono::duration_cast<chrono::nanoseconds>(e-s).count()/1000.0<<" us"<<endl; }}
// var1 mem = {{}} and time = {{}}
''')

w("0105_construct_binary_tree_from_preorder_and_inorder.py", f'''"""LeetCode 105: Construct Binary Tree from Preorder and Inorder - Medium"""
{PY_TREE_HELPER}
class Solution_v1:
    def buildTree(self, preorder, inorder):
        if not preorder: return None
        root = TreeNode(preorder[0])
        mid = inorder.index(preorder[0])
        root.left = self.buildTree(preorder[1:mid+1], inorder[:mid])
        root.right = self.buildTree(preorder[mid+1:], inorder[mid+1:])
        return root
class Solution_v2:
    def buildTree(self, preorder, inorder):
        inorder_map = {{v:i for i,v in enumerate(inorder)}}
        self.idx = 0
        def helper(l, r):
            if l > r: return None
            val = preorder[self.idx]; self.idx += 1
            node = TreeNode(val)
            node.left = helper(l, inorder_map[val]-1)
            node.right = helper(inorder_map[val]+1, r)
            return node
        return helper(0, len(inorder)-1)
if __name__ == "__main__":
    for i,(S,n) in enumerate(zip([Solution_v1,Solution_v2],["Recursive","HashMap"]),1):
        tracemalloc.start(); t0=time.perf_counter(); r=S().buildTree([3,9,20,15,7],[9,3,15,20,7])
        t1=time.perf_counter(); mem=tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{{i}} ({{n}}): mem = {{mem}} bytes, time = {{(t1-t0)*1e6:.2f}} us")
# var1 mem = {{}} and time = {{}}
# var2 mem = {{}} and time = {{}}
''')

w("0105_construct_binary_tree_from_preorder_and_inorder.cpp", f'''/* LeetCode 105: Build Tree from Preorder & Inorder - Medium */
{CPP_TREE_HELPER}
class Solution {{ unordered_map<int,int> mp; int idx=0;
    TreeNode* helper(vector<int>& pre, int l, int r){{ if(l>r) return nullptr; int val=pre[idx++]; auto n=new TreeNode(val); n->left=helper(pre,l,mp[val]-1); n->right=helper(pre,mp[val]+1,r); return n; }}
public: TreeNode* buildTree(vector<int>& pre, vector<int>& in){{ for(int i=0;i<in.size();i++) mp[in[i]]=i; idx=0; return helper(pre,0,in.size()-1); }} }};
int main(){{ vector<int> pre={{3,9,20,15,7}},in={{9,3,15,20,7}}; auto s=chrono::high_resolution_clock::now(); Solution().buildTree(pre,in); auto e=chrono::high_resolution_clock::now(); cout<<"var1: "<<chrono::duration_cast<chrono::nanoseconds>(e-s).count()/1000.0<<" us"<<endl; }}
// var1 mem = {{}} and time = {{}}
''')

w("0124_binary_tree_maximum_path_sum.py", f'''"""LeetCode 124: Binary Tree Maximum Path Sum - Hard"""
{PY_TREE_HELPER}
class Solution_v1:
    def maxPathSum(self, root):
        self.res = float('-inf')
        def dfs(node):
            if not node: return 0
            l = max(dfs(node.left), 0); r = max(dfs(node.right), 0)
            self.res = max(self.res, node.val + l + r)
            return node.val + max(l, r)
        dfs(root); return self.res
if __name__ == "__main__":
    tracemalloc.start(); t0=time.perf_counter(); r=Solution_v1().maxPathSum(build([1,2,3]))
    t1=time.perf_counter(); mem=tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
    print(f"var1: result={{r}}, mem = {{mem}} bytes, time = {{(t1-t0)*1e6:.2f}} us")
# var1 mem = {{}} and time = {{}}
''')

w("0124_binary_tree_maximum_path_sum.cpp", f'''/* LeetCode 124: Binary Tree Maximum Path Sum - Hard */
{CPP_TREE_HELPER}
class Solution {{ int res=INT_MIN; int dfs(TreeNode* n){{ if(!n) return 0; int l=max(dfs(n->left),0),r=max(dfs(n->right),0); res=max(res,n->val+l+r); return n->val+max(l,r); }}
public: int maxPathSum(TreeNode* r){{ res=INT_MIN; dfs(r); return res; }} }};
int main(){{ auto r=build({{1,2,3}}); auto s=chrono::high_resolution_clock::now(); cout<<Solution().maxPathSum(r); auto e=chrono::high_resolution_clock::now(); cout<<", "<<chrono::duration_cast<chrono::nanoseconds>(e-s).count()/1000.0<<" us"<<endl; }}
// var1 mem = {{}} and time = {{}}
''')

w("0297_serialize_and_deserialize_binary_tree.py", f'''"""LeetCode 297: Serialize and Deserialize Binary Tree - Hard"""
{PY_TREE_HELPER}
class Codec_v1:
    def serialize(self, root):
        res = []
        def dfs(node):
            if not node: res.append("N"); return
            res.append(str(node.val)); dfs(node.left); dfs(node.right)
        dfs(root); return ",".join(res)
    def deserialize(self, data):
        vals = iter(data.split(","))
        def dfs():
            v = next(vals)
            if v == "N": return None
            node = TreeNode(int(v)); node.left = dfs(); node.right = dfs()
            return node
        return dfs()
if __name__ == "__main__":
    tracemalloc.start(); t0=time.perf_counter()
    c = Codec_v1(); s = c.serialize(build([1,2,3,None,None,4,5])); r = c.deserialize(s)
    t1=time.perf_counter(); mem=tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
    print(f"var1: serialized={{s}}, mem = {{mem}} bytes, time = {{(t1-t0)*1e6:.2f}} us")
# var1 mem = {{}} and time = {{}}
''')

w("0297_serialize_and_deserialize_binary_tree.cpp", f'''/* LeetCode 297: Serialize and Deserialize Binary Tree - Hard */
{CPP_TREE_HELPER}
class Codec {{
public:
    string serialize(TreeNode* root) {{ if(!root) return "N"; return to_string(root->val)+","+serialize(root->left)+","+serialize(root->right); }}
    TreeNode* deserialize(string data) {{ istringstream ss(data); return dfs(ss); }}
    TreeNode* dfs(istringstream& ss) {{ string v; getline(ss,v,','); if(v=="N") return nullptr; auto n=new TreeNode(stoi(v)); n->left=dfs(ss); n->right=dfs(ss); return n; }}
}};
int main(){{ auto r=build({{1,2,3,-1,-1,4,5}}); Codec c; auto s=chrono::high_resolution_clock::now(); auto ser=c.serialize(r); c.deserialize(ser); auto e=chrono::high_resolution_clock::now(); cout<<"var1: "<<chrono::duration_cast<chrono::nanoseconds>(e-s).count()/1000.0<<" us"<<endl; }}
// var1 mem = {{}} and time = {{}}
''')

w("1448_count_good_nodes_in_binary_tree.py", f'''"""LeetCode 1448: Count Good Nodes in Binary Tree - Medium"""
{PY_TREE_HELPER}
class Solution_v1:
    def goodNodes(self, root):
        def dfs(node, max_val):
            if not node: return 0
            res = 1 if node.val >= max_val else 0
            max_val = max(max_val, node.val)
            return res + dfs(node.left, max_val) + dfs(node.right, max_val)
        return dfs(root, root.val)
if __name__ == "__main__":
    tracemalloc.start(); t0=time.perf_counter(); r=Solution_v1().goodNodes(build([3,1,4,3,None,1,5]))
    t1=time.perf_counter(); mem=tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
    print(f"var1: result={{r}}, mem = {{mem}} bytes, time = {{(t1-t0)*1e6:.2f}} us")
# var1 mem = {{}} and time = {{}}
''')

w("1448_count_good_nodes_in_binary_tree.cpp", f'''/* LeetCode 1448: Count Good Nodes - Medium */
{CPP_TREE_HELPER}
class Solution {{ int dfs(TreeNode* n, int mx){{ if(!n) return 0; int r=(n->val>=mx)?1:0; mx=max(mx,n->val); return r+dfs(n->left,mx)+dfs(n->right,mx); }}
public: int goodNodes(TreeNode* r){{ return dfs(r,r->val); }} }};
int main(){{ auto r=build({{3,1,4,3,-1,1,5}}); auto s=chrono::high_resolution_clock::now(); cout<<Solution().goodNodes(r); auto e=chrono::high_resolution_clock::now(); cout<<", "<<chrono::duration_cast<chrono::nanoseconds>(e-s).count()/1000.0<<" us"<<endl; }}
// var1 mem = {{}} and time = {{}}
''')

print("Section 7 (Trees) generated! 15 problems x 2 = 30 files")
