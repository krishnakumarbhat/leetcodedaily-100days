#!/usr/bin/env python3
"""
Batch generator for remaining NeetCode 150 problems.
Creates .py and .cpp files with complete implementations.
"""
import os

BASE = "/media/pope/projecteo/github_proj/leetcode/neetcode150"

def write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(content)

# ======================================================================
# SECTION 4: STACK (7 problems)
# ======================================================================

write(f"{BASE}/04_stack/0020_valid_parentheses.py", '''"""
LeetCode 20: Valid Parentheses
Link: https://leetcode.com/problems/valid-parentheses/
Difficulty: Easy
"""
import time, tracemalloc

# ============= Variation 1: Replace Pairs =============
# Time Complexity: O(n^2)   Space Complexity: O(n)
class Solution_v1:
    def isValid(self, s: str) -> bool:
        while '()' in s or '{}' in s or '[]' in s:
            s = s.replace('()', '').replace('{}', '').replace('[]', '')
        return s == ''

# ============= Variation 2: Stack =============
# Time Complexity: O(n)   Space Complexity: O(n)
class Solution_v2:
    def isValid(self, s: str) -> bool:
        stack = []
        mapping = {')': '(', '}': '{', ']': '['}
        for c in s:
            if c in mapping:
                if not stack or stack[-1] != mapping[c]: return False
                stack.pop()
            else:
                stack.append(c)
        return not stack

if __name__ == "__main__":
    s = "()[]{}"
    for i, (Sol, name) in enumerate(zip([Solution_v1, Solution_v2], ["Replace", "Stack"]), 1):
        tracemalloc.start(); t0 = time.perf_counter()
        result = Sol().isValid(s)
        t1 = time.perf_counter(); mem = tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{i} ({name}): result={result}, mem = {mem} bytes, time = {(t1-t0)*1e6:.2f} µs")
# var1 mem = {} and time = {}
# var2 mem = {} and time = {}
''')

write(f"{BASE}/04_stack/0020_valid_parentheses.cpp", '''/* LeetCode 20: Valid Parentheses - Easy */
#include <bits/stdc++.h>
#include <chrono>
using namespace std;
class Solution_v1 {
public:
    bool isValid(string s) {
        stack<char> st;
        unordered_map<char,char> mp = {{')','('},{'}','{'},{']','['}};
        for (char c : s) {
            if (mp.count(c)) {
                if (st.empty() || st.top()!=mp[c]) return false;
                st.pop();
            } else st.push(c);
        }
        return st.empty();
    }
};
int main() {
    string s = "()[]{}";
    auto st=chrono::high_resolution_clock::now(); bool r=Solution_v1().isValid(s); auto e=chrono::high_resolution_clock::now();
    cout<<"var1 (Stack): "<<r<<", "<<chrono::duration_cast<chrono::nanoseconds>(e-st).count()/1000.0<<" us"<<endl;
    return 0;
}
// var1 mem = {} and time = {}
''')

write(f"{BASE}/04_stack/0155_min_stack.py", '''"""
LeetCode 155: Min Stack
Link: https://leetcode.com/problems/min-stack/
Difficulty: Medium
"""
import time, tracemalloc

# ============= Variation 1: Two Stacks =============
# Time Complexity: O(1) all ops   Space Complexity: O(n)
class MinStack_v1:
    def __init__(self):
        self.stack = []
        self.min_stack = []
    def push(self, val: int) -> None:
        self.stack.append(val)
        self.min_stack.append(min(val, self.min_stack[-1] if self.min_stack else val))
    def pop(self) -> None:
        self.stack.pop(); self.min_stack.pop()
    def top(self) -> int:
        return self.stack[-1]
    def getMin(self) -> int:
        return self.min_stack[-1]

# ============= Variation 2: Stack with Tuples =============
# Time Complexity: O(1) all ops   Space Complexity: O(n)
class MinStack_v2:
    def __init__(self):
        self.stack = []  # (val, current_min)
    def push(self, val: int) -> None:
        cur_min = min(val, self.stack[-1][1] if self.stack else val)
        self.stack.append((val, cur_min))
    def pop(self) -> None:
        self.stack.pop()
    def top(self) -> int:
        return self.stack[-1][0]
    def getMin(self) -> int:
        return self.stack[-1][1]

if __name__ == "__main__":
    for i, (Cls, name) in enumerate(zip([MinStack_v1, MinStack_v2], ["Two Stacks", "Tuples"]), 1):
        tracemalloc.start(); t0 = time.perf_counter()
        ms = Cls(); ms.push(-2); ms.push(0); ms.push(-3)
        r = ms.getMin(); ms.pop(); r2 = ms.top(); r3 = ms.getMin()
        t1 = time.perf_counter(); mem = tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{i} ({name}): min={r}, top={r2}, min={r3}, mem = {mem} bytes, time = {(t1-t0)*1e6:.2f} µs")
# var1 mem = {} and time = {}
# var2 mem = {} and time = {}
''')

write(f"{BASE}/04_stack/0155_min_stack.cpp", '''/* LeetCode 155: Min Stack - Medium */
#include <bits/stdc++.h>
#include <chrono>
using namespace std;
class MinStack {
    stack<pair<int,int>> st;
public:
    void push(int val) { int mn = st.empty() ? val : min(val, st.top().second); st.push({val, mn}); }
    void pop() { st.pop(); }
    int top() { return st.top().first; }
    int getMin() { return st.top().second; }
};
int main() {
    auto s=chrono::high_resolution_clock::now();
    MinStack ms; ms.push(-2); ms.push(0); ms.push(-3);
    cout<<"min="<<ms.getMin(); ms.pop(); cout<<" top="<<ms.top()<<" min="<<ms.getMin()<<endl;
    auto e=chrono::high_resolution_clock::now();
    cout<<"time = "<<chrono::duration_cast<chrono::nanoseconds>(e-s).count()/1000.0<<" us"<<endl;
    return 0;
}
// var1 mem = {} and time = {}
''')

write(f"{BASE}/04_stack/0150_evaluate_reverse_polish_notation.py", '''"""
LeetCode 150: Evaluate Reverse Polish Notation
Link: https://leetcode.com/problems/evaluate-reverse-polish-notation/
Difficulty: Medium
"""
import time, tracemalloc
from typing import List

# ============= Variation 1: Stack =============
# Time Complexity: O(n)   Space Complexity: O(n)
class Solution_v1:
    def evalRPN(self, tokens: List[str]) -> int:
        stack = []
        for t in tokens:
            if t in '+-*/':
                b, a = stack.pop(), stack.pop()
                if t == '+': stack.append(a + b)
                elif t == '-': stack.append(a - b)
                elif t == '*': stack.append(a * b)
                else: stack.append(int(a / b))
            else:
                stack.append(int(t))
        return stack[0]

if __name__ == "__main__":
    tokens = ["2", "1", "+", "3", "*"]
    tracemalloc.start(); t0 = time.perf_counter()
    result = Solution_v1().evalRPN(tokens)
    t1 = time.perf_counter(); mem = tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
    print(f"var1 (Stack): result={result}, mem = {mem} bytes, time = {(t1-t0)*1e6:.2f} µs")
# var1 mem = {} and time = {}
''')

write(f"{BASE}/04_stack/0150_evaluate_reverse_polish_notation.cpp", '''/* LeetCode 150: Evaluate Reverse Polish Notation - Medium */
#include <bits/stdc++.h>
#include <chrono>
using namespace std;
class Solution_v1 {
public:
    int evalRPN(vector<string>& tokens) {
        stack<int> st;
        for (auto& t : tokens) {
            if (t=="+"||t=="-"||t=="*"||t=="/") {
                int b=st.top(); st.pop(); int a=st.top(); st.pop();
                if(t=="+") st.push(a+b); else if(t=="-") st.push(a-b);
                else if(t=="*") st.push(a*b); else st.push(a/b);
            } else st.push(stoi(t));
        }
        return st.top();
    }
};
int main() {
    vector<string> tokens = {"2","1","+","3","*"};
    auto s=chrono::high_resolution_clock::now(); int r=Solution_v1().evalRPN(tokens); auto e=chrono::high_resolution_clock::now();
    cout<<"var1 (Stack): "<<r<<", "<<chrono::duration_cast<chrono::nanoseconds>(e-s).count()/1000.0<<" us"<<endl;
    return 0;
}
// var1 mem = {} and time = {}
''')

write(f"{BASE}/04_stack/0022_generate_parentheses.py", '''"""
LeetCode 22: Generate Parentheses
Link: https://leetcode.com/problems/generate-parentheses/
Difficulty: Medium
"""
import time, tracemalloc
from typing import List

# ============= Variation 1: Backtracking =============
# Time Complexity: O(4^n/sqrt(n))   Space Complexity: O(n)
class Solution_v1:
    def generateParenthesis(self, n: int) -> List[str]:
        result = []
        def backtrack(s, open_c, close_c):
            if len(s) == 2 * n:
                result.append(s); return
            if open_c < n: backtrack(s + '(', open_c + 1, close_c)
            if close_c < open_c: backtrack(s + ')', open_c, close_c + 1)
        backtrack('', 0, 0)
        return result

# ============= Variation 2: Iterative (BFS) =============
# Time Complexity: O(4^n/sqrt(n))   Space Complexity: O(4^n/sqrt(n))
class Solution_v2:
    def generateParenthesis(self, n: int) -> List[str]:
        from collections import deque
        queue = deque([('', 0, 0)])
        result = []
        while queue:
            s, o, c = queue.popleft()
            if len(s) == 2 * n: result.append(s); continue
            if o < n: queue.append((s + '(', o + 1, c))
            if c < o: queue.append((s + ')', o, c + 1))
        return result

if __name__ == "__main__":
    n = 3
    for i, (Sol, name) in enumerate(zip([Solution_v1, Solution_v2], ["Backtracking", "BFS"]), 1):
        tracemalloc.start(); t0 = time.perf_counter()
        result = Sol().generateParenthesis(n)
        t1 = time.perf_counter(); mem = tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{i} ({name}): count={len(result)}, mem = {mem} bytes, time = {(t1-t0)*1e6:.2f} µs")
# var1 mem = {} and time = {}
# var2 mem = {} and time = {}
''')

write(f"{BASE}/04_stack/0022_generate_parentheses.cpp", '''/* LeetCode 22: Generate Parentheses - Medium */
#include <bits/stdc++.h>
#include <chrono>
using namespace std;
class Solution_v1 {
public:
    vector<string> res;
    void bt(string s, int o, int c, int n) {
        if (s.size()==2*n) { res.push_back(s); return; }
        if (o<n) bt(s+'(',o+1,c,n);
        if (c<o) bt(s+')',o,c+1,n);
    }
    vector<string> generateParenthesis(int n) { res.clear(); bt("",0,0,n); return res; }
};
int main() {
    auto s=chrono::high_resolution_clock::now(); auto r=Solution_v1().generateParenthesis(3); auto e=chrono::high_resolution_clock::now();
    cout<<"var1 (Backtrack): count="<<r.size()<<", "<<chrono::duration_cast<chrono::nanoseconds>(e-s).count()/1000.0<<" us"<<endl;
    return 0;
}
// var1 mem = {} and time = {}
''')

write(f"{BASE}/04_stack/0739_daily_temperatures.py", '''"""
LeetCode 739: Daily Temperatures
Link: https://leetcode.com/problems/daily-temperatures/
Difficulty: Medium
"""
import time, tracemalloc
from typing import List

# ============= Variation 1: Brute Force =============
# Time Complexity: O(n^2)   Space Complexity: O(n)
class Solution_v1:
    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:
        n = len(temperatures); result = [0] * n
        for i in range(n):
            for j in range(i + 1, n):
                if temperatures[j] > temperatures[i]:
                    result[i] = j - i; break
        return result

# ============= Variation 2: Monotonic Stack =============
# Time Complexity: O(n)   Space Complexity: O(n)
class Solution_v2:
    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:
        n = len(temperatures); result = [0] * n; stack = []
        for i in range(n):
            while stack and temperatures[i] > temperatures[stack[-1]]:
                idx = stack.pop(); result[idx] = i - idx
            stack.append(i)
        return result

if __name__ == "__main__":
    temps = [73, 74, 75, 71, 69, 72, 76, 73]
    for i, (Sol, name) in enumerate(zip([Solution_v1, Solution_v2], ["Brute Force", "Mono Stack"]), 1):
        tracemalloc.start(); t0 = time.perf_counter()
        result = Sol().dailyTemperatures(temps[:])
        t1 = time.perf_counter(); mem = tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{i} ({name}): result={result}, mem = {mem} bytes, time = {(t1-t0)*1e6:.2f} µs")
# var1 mem = {} and time = {}
# var2 mem = {} and time = {}
''')

write(f"{BASE}/04_stack/0739_daily_temperatures.cpp", '''/* LeetCode 739: Daily Temperatures - Medium */
#include <bits/stdc++.h>
#include <chrono>
using namespace std;
class Solution_v1 {
public:
    vector<int> dailyTemperatures(vector<int>& t) {
        int n=t.size(); vector<int> res(n,0); stack<int> st;
        for(int i=0;i<n;i++){
            while(!st.empty()&&t[i]>t[st.top()]){int idx=st.top();st.pop();res[idx]=i-idx;}
            st.push(i);
        }
        return res;
    }
};
int main(){
    vector<int> t={73,74,75,71,69,72,76,73};
    auto s=chrono::high_resolution_clock::now(); auto r=Solution_v1().dailyTemperatures(t); auto e=chrono::high_resolution_clock::now();
    cout<<"var1 (Mono Stack): "<<chrono::duration_cast<chrono::nanoseconds>(e-s).count()/1000.0<<" us"<<endl;
    return 0;
}
// var1 mem = {} and time = {}
''')

write(f"{BASE}/04_stack/0853_car_fleet.py", '''"""
LeetCode 853: Car Fleet
Link: https://leetcode.com/problems/car-fleet/
Difficulty: Medium
"""
import time, tracemalloc
from typing import List

# ============= Variation 1: Sort + Stack =============
# Time Complexity: O(n log n)   Space Complexity: O(n)
class Solution_v1:
    def carFleet(self, target: int, position: List[int], speed: List[int]) -> int:
        pairs = sorted(zip(position, speed), reverse=True)
        stack = []
        for pos, spd in pairs:
            t = (target - pos) / spd
            if not stack or t > stack[-1]:
                stack.append(t)
        return len(stack)

if __name__ == "__main__":
    target, position, speed = 12, [10, 8, 0, 5, 3], [2, 4, 1, 1, 3]
    tracemalloc.start(); t0 = time.perf_counter()
    result = Solution_v1().carFleet(target, position, speed)
    t1 = time.perf_counter(); mem = tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
    print(f"var1 (Sort+Stack): result={result}, mem = {mem} bytes, time = {(t1-t0)*1e6:.2f} µs")
# var1 mem = {} and time = {}
''')

write(f"{BASE}/04_stack/0853_car_fleet.cpp", '''/* LeetCode 853: Car Fleet - Medium */
#include <bits/stdc++.h>
#include <chrono>
using namespace std;
class Solution_v1 {
public:
    int carFleet(int target, vector<int>& position, vector<int>& speed) {
        vector<pair<int,int>> pairs;
        for(int i=0;i<position.size();i++) pairs.push_back({position[i],speed[i]});
        sort(pairs.rbegin(),pairs.rend());
        stack<double> st;
        for(auto&[p,s]:pairs){
            double t=(double)(target-p)/s;
            if(st.empty()||t>st.top()) st.push(t);
        }
        return st.size();
    }
};
int main(){
    vector<int> pos={10,8,0,5,3}, spd={2,4,1,1,3}; int target=12;
    auto s=chrono::high_resolution_clock::now(); int r=Solution_v1().carFleet(target,pos,spd); auto e=chrono::high_resolution_clock::now();
    cout<<"var1 (Sort+Stack): "<<r<<", "<<chrono::duration_cast<chrono::nanoseconds>(e-s).count()/1000.0<<" us"<<endl;
    return 0;
}
// var1 mem = {} and time = {}
''')

write(f"{BASE}/04_stack/0084_largest_rectangle_in_histogram.py", '''"""
LeetCode 84: Largest Rectangle in Histogram
Link: https://leetcode.com/problems/largest-rectangle-in-histogram/
Difficulty: Hard
"""
import time, tracemalloc
from typing import List

# ============= Variation 1: Brute Force =============
# Time Complexity: O(n^2)   Space Complexity: O(1)
class Solution_v1:
    def largestRectangleArea(self, heights: List[int]) -> int:
        max_area = 0
        for i in range(len(heights)):
            min_h = heights[i]
            for j in range(i, len(heights)):
                min_h = min(min_h, heights[j])
                max_area = max(max_area, min_h * (j - i + 1))
        return max_area

# ============= Variation 2: Monotonic Stack =============
# Time Complexity: O(n)   Space Complexity: O(n)
class Solution_v2:
    def largestRectangleArea(self, heights: List[int]) -> int:
        stack = []; max_area = 0
        for i, h in enumerate(heights + [0]):
            while stack and heights[stack[-1]] > h:
                height = heights[stack.pop()]
                width = i if not stack else i - stack[-1] - 1
                max_area = max(max_area, height * width)
            stack.append(i)
        return max_area

if __name__ == "__main__":
    heights = [2, 1, 5, 6, 2, 3]
    for i, (Sol, name) in enumerate(zip([Solution_v1, Solution_v2], ["Brute Force", "Mono Stack"]), 1):
        tracemalloc.start(); t0 = time.perf_counter()
        result = Sol().largestRectangleArea(heights[:])
        t1 = time.perf_counter(); mem = tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{i} ({name}): result={result}, mem = {mem} bytes, time = {(t1-t0)*1e6:.2f} µs")
# var1 mem = {} and time = {}
# var2 mem = {} and time = {}
''')

write(f"{BASE}/04_stack/0084_largest_rectangle_in_histogram.cpp", '''/* LeetCode 84: Largest Rectangle in Histogram - Hard */
#include <bits/stdc++.h>
#include <chrono>
using namespace std;
class Solution_v1 {
public:
    int largestRectangleArea(vector<int>& heights) {
        stack<int> st; int mx=0;
        heights.push_back(0);
        for(int i=0;i<heights.size();i++){
            while(!st.empty()&&heights[st.top()]>heights[i]){
                int h=heights[st.top()]; st.pop();
                int w=st.empty()?i:i-st.top()-1;
                mx=max(mx,h*w);
            }
            st.push(i);
        }
        return mx;
    }
};
int main(){
    vector<int> h={2,1,5,6,2,3};
    auto s=chrono::high_resolution_clock::now(); int r=Solution_v1().largestRectangleArea(h); auto e=chrono::high_resolution_clock::now();
    cout<<"var1 (Mono Stack): "<<r<<", "<<chrono::duration_cast<chrono::nanoseconds>(e-s).count()/1000.0<<" us"<<endl;
    return 0;
}
// var1 mem = {} and time = {}
''')

# ======================================================================
# SECTION 5: BINARY SEARCH (7 problems)
# ======================================================================

write(f"{BASE}/05_binary_search/0704_binary_search.py", '''"""
LeetCode 704: Binary Search
Link: https://leetcode.com/problems/binary-search/
Difficulty: Easy
"""
import time, tracemalloc
from typing import List

# ============= Variation 1: Iterative =============
# Time Complexity: O(log n)   Space Complexity: O(1)
class Solution_v1:
    def search(self, nums: List[int], target: int) -> int:
        l, r = 0, len(nums) - 1
        while l <= r:
            mid = (l + r) // 2
            if nums[mid] == target: return mid
            elif nums[mid] < target: l = mid + 1
            else: r = mid - 1
        return -1

# ============= Variation 2: Recursive =============
# Time Complexity: O(log n)   Space Complexity: O(log n)
class Solution_v2:
    def search(self, nums: List[int], target: int) -> int:
        def bs(l, r):
            if l > r: return -1
            mid = (l + r) // 2
            if nums[mid] == target: return mid
            elif nums[mid] < target: return bs(mid + 1, r)
            else: return bs(l, mid - 1)
        return bs(0, len(nums) - 1)

if __name__ == "__main__":
    nums, target = [-1, 0, 3, 5, 9, 12], 9
    for i, (Sol, name) in enumerate(zip([Solution_v1, Solution_v2], ["Iterative", "Recursive"]), 1):
        tracemalloc.start(); t0 = time.perf_counter()
        result = Sol().search(nums[:], target)
        t1 = time.perf_counter(); mem = tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{i} ({name}): result={result}, mem = {mem} bytes, time = {(t1-t0)*1e6:.2f} µs")
# var1 mem = {} and time = {}
# var2 mem = {} and time = {}
''')

write(f"{BASE}/05_binary_search/0704_binary_search.cpp", '''/* LeetCode 704: Binary Search - Easy */
#include <bits/stdc++.h>
#include <chrono>
using namespace std;
class Solution_v1 {
public:
    int search(vector<int>& nums, int target) {
        int l=0, r=nums.size()-1;
        while(l<=r){int m=(l+r)/2; if(nums[m]==target) return m; else if(nums[m]<target) l=m+1; else r=m-1;}
        return -1;
    }
};
int main(){
    vector<int> nums={-1,0,3,5,9,12}; int target=9;
    auto s=chrono::high_resolution_clock::now(); int r=Solution_v1().search(nums,target); auto e=chrono::high_resolution_clock::now();
    cout<<"var1 (Iterative): "<<r<<", "<<chrono::duration_cast<chrono::nanoseconds>(e-s).count()/1000.0<<" us"<<endl;
    return 0;
}
// var1 mem = {} and time = {}
''')

write(f"{BASE}/05_binary_search/0074_search_a_2d_matrix.py", '''"""
LeetCode 74: Search a 2D Matrix
Link: https://leetcode.com/problems/search-a-2d-matrix/
Difficulty: Medium
"""
import time, tracemalloc
from typing import List

# ============= Variation 1: Brute Force =============
# Time Complexity: O(m*n)   Space Complexity: O(1)
class Solution_v1:
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        for row in matrix:
            if target in row: return True
        return False

# ============= Variation 2: Binary Search (flattened) =============
# Time Complexity: O(log(m*n))   Space Complexity: O(1)
class Solution_v2:
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        m, n = len(matrix), len(matrix[0])
        l, r = 0, m * n - 1
        while l <= r:
            mid = (l + r) // 2
            val = matrix[mid // n][mid % n]
            if val == target: return True
            elif val < target: l = mid + 1
            else: r = mid - 1
        return False

if __name__ == "__main__":
    matrix = [[1,3,5,7],[10,11,16,20],[23,30,34,60]]; target = 3
    for i, (Sol, name) in enumerate(zip([Solution_v1, Solution_v2], ["Brute Force", "Binary Search"]), 1):
        tracemalloc.start(); t0 = time.perf_counter()
        result = Sol().searchMatrix(matrix, target)
        t1 = time.perf_counter(); mem = tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{i} ({name}): result={result}, mem = {mem} bytes, time = {(t1-t0)*1e6:.2f} µs")
# var1 mem = {} and time = {}
# var2 mem = {} and time = {}
''')

write(f"{BASE}/05_binary_search/0074_search_a_2d_matrix.cpp", '''/* LeetCode 74: Search a 2D Matrix - Medium */
#include <bits/stdc++.h>
#include <chrono>
using namespace std;
class Solution_v1 {
public:
    bool searchMatrix(vector<vector<int>>& matrix, int target) {
        int m=matrix.size(), n=matrix[0].size(), l=0, r=m*n-1;
        while(l<=r){ int mid=(l+r)/2, val=matrix[mid/n][mid%n]; if(val==target) return true; else if(val<target) l=mid+1; else r=mid-1; }
        return false;
    }
};
int main(){
    vector<vector<int>> matrix={{1,3,5,7},{10,11,16,20},{23,30,34,60}}; int target=3;
    auto s=chrono::high_resolution_clock::now(); bool r=Solution_v1().searchMatrix(matrix,target); auto e=chrono::high_resolution_clock::now();
    cout<<"var1 (BS): "<<r<<", "<<chrono::duration_cast<chrono::nanoseconds>(e-s).count()/1000.0<<" us"<<endl;
    return 0;
}
// var1 mem = {} and time = {}
''')

write(f"{BASE}/05_binary_search/0875_koko_eating_bananas.py", '''"""
LeetCode 875: Koko Eating Bananas
Link: https://leetcode.com/problems/koko-eating-bananas/
Difficulty: Medium
"""
import time, tracemalloc, math
from typing import List

# ============= Variation 1: Brute Force =============
# Time Complexity: O(max(piles) * n)   Space Complexity: O(1)
class Solution_v1:
    def minEatingSpeed(self, piles: List[int], h: int) -> int:
        for k in range(1, max(piles) + 1):
            total = sum(math.ceil(p / k) for p in piles)
            if total <= h: return k
        return max(piles)

# ============= Variation 2: Binary Search =============
# Time Complexity: O(n * log(max(piles)))   Space Complexity: O(1)
class Solution_v2:
    def minEatingSpeed(self, piles: List[int], h: int) -> int:
        l, r = 1, max(piles)
        result = r
        while l <= r:
            k = (l + r) // 2
            total = sum(math.ceil(p / k) for p in piles)
            if total <= h: result = k; r = k - 1
            else: l = k + 1
        return result

if __name__ == "__main__":
    piles, h = [3, 6, 7, 11], 8
    for i, (Sol, name) in enumerate(zip([Solution_v1, Solution_v2], ["Brute Force", "Binary Search"]), 1):
        tracemalloc.start(); t0 = time.perf_counter()
        result = Sol().minEatingSpeed(piles[:], h)
        t1 = time.perf_counter(); mem = tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{i} ({name}): result={result}, mem = {mem} bytes, time = {(t1-t0)*1e6:.2f} µs")
# var1 mem = {} and time = {}
# var2 mem = {} and time = {}
''')

write(f"{BASE}/05_binary_search/0875_koko_eating_bananas.cpp", '''/* LeetCode 875: Koko Eating Bananas - Medium */
#include <bits/stdc++.h>
#include <chrono>
using namespace std;
class Solution_v1 {
public:
    int minEatingSpeed(vector<int>& piles, int h) {
        int l=1, r=*max_element(piles.begin(),piles.end()), res=r;
        while(l<=r){
            int k=(l+r)/2; long total=0;
            for(int p:piles) total+=(p+k-1)/k;
            if(total<=h){res=k;r=k-1;} else l=k+1;
        }
        return res;
    }
};
int main(){
    vector<int> piles={3,6,7,11}; int h=8;
    auto s=chrono::high_resolution_clock::now(); int r=Solution_v1().minEatingSpeed(piles,h); auto e=chrono::high_resolution_clock::now();
    cout<<"var1 (BS): "<<r<<", "<<chrono::duration_cast<chrono::nanoseconds>(e-s).count()/1000.0<<" us"<<endl;
    return 0;
}
// var1 mem = {} and time = {}
''')

write(f"{BASE}/05_binary_search/0153_find_minimum_in_rotated_sorted_array.py", '''"""
LeetCode 153: Find Minimum in Rotated Sorted Array
Link: https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/
Difficulty: Medium
"""
import time, tracemalloc
from typing import List

# ============= Variation 1: Linear Scan =============
# Time Complexity: O(n)   Space Complexity: O(1)
class Solution_v1:
    def findMin(self, nums: List[int]) -> int:
        return min(nums)

# ============= Variation 2: Binary Search =============
# Time Complexity: O(log n)   Space Complexity: O(1)
class Solution_v2:
    def findMin(self, nums: List[int]) -> int:
        l, r = 0, len(nums) - 1
        result = nums[0]
        while l <= r:
            if nums[l] < nums[r]: result = min(result, nums[l]); break
            mid = (l + r) // 2
            result = min(result, nums[mid])
            if nums[mid] >= nums[l]: l = mid + 1
            else: r = mid - 1
        return result

if __name__ == "__main__":
    nums = [3, 4, 5, 1, 2]
    for i, (Sol, name) in enumerate(zip([Solution_v1, Solution_v2], ["Linear", "Binary Search"]), 1):
        tracemalloc.start(); t0 = time.perf_counter()
        result = Sol().findMin(nums[:])
        t1 = time.perf_counter(); mem = tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{i} ({name}): result={result}, mem = {mem} bytes, time = {(t1-t0)*1e6:.2f} µs")
# var1 mem = {} and time = {}
# var2 mem = {} and time = {}
''')

write(f"{BASE}/05_binary_search/0153_find_minimum_in_rotated_sorted_array.cpp", '''/* LeetCode 153: Find Min in Rotated Sorted Array - Medium */
#include <bits/stdc++.h>
#include <chrono>
using namespace std;
class Solution_v1 {
public:
    int findMin(vector<int>& nums) {
        int l=0, r=nums.size()-1, res=nums[0];
        while(l<=r){
            if(nums[l]<nums[r]){res=min(res,nums[l]);break;}
            int m=(l+r)/2; res=min(res,nums[m]);
            if(nums[m]>=nums[l]) l=m+1; else r=m-1;
        }
        return res;
    }
};
int main(){
    vector<int> nums={3,4,5,1,2};
    auto s=chrono::high_resolution_clock::now(); int r=Solution_v1().findMin(nums); auto e=chrono::high_resolution_clock::now();
    cout<<"var1 (BS): "<<r<<", "<<chrono::duration_cast<chrono::nanoseconds>(e-s).count()/1000.0<<" us"<<endl;
    return 0;
}
// var1 mem = {} and time = {}
''')

write(f"{BASE}/05_binary_search/0033_search_in_rotated_sorted_array.py", '''"""
LeetCode 33: Search in Rotated Sorted Array
Link: https://leetcode.com/problems/search-in-rotated-sorted-array/
Difficulty: Medium
"""
import time, tracemalloc
from typing import List

# ============= Variation 1: Linear Scan =============
# Time Complexity: O(n)   Space Complexity: O(1)
class Solution_v1:
    def search(self, nums: List[int], target: int) -> int:
        return nums.index(target) if target in nums else -1

# ============= Variation 2: Binary Search =============
# Time Complexity: O(log n)   Space Complexity: O(1)
class Solution_v2:
    def search(self, nums: List[int], target: int) -> int:
        l, r = 0, len(nums) - 1
        while l <= r:
            mid = (l + r) // 2
            if nums[mid] == target: return mid
            if nums[l] <= nums[mid]:
                if nums[l] <= target < nums[mid]: r = mid - 1
                else: l = mid + 1
            else:
                if nums[mid] < target <= nums[r]: l = mid + 1
                else: r = mid - 1
        return -1

if __name__ == "__main__":
    nums, target = [4, 5, 6, 7, 0, 1, 2], 0
    for i, (Sol, name) in enumerate(zip([Solution_v1, Solution_v2], ["Linear", "Binary Search"]), 1):
        tracemalloc.start(); t0 = time.perf_counter()
        result = Sol().search(nums[:], target)
        t1 = time.perf_counter(); mem = tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{i} ({name}): result={result}, mem = {mem} bytes, time = {(t1-t0)*1e6:.2f} µs")
# var1 mem = {} and time = {}
# var2 mem = {} and time = {}
''')

write(f"{BASE}/05_binary_search/0033_search_in_rotated_sorted_array.cpp", '''/* LeetCode 33: Search in Rotated Sorted Array - Medium */
#include <bits/stdc++.h>
#include <chrono>
using namespace std;
class Solution_v1 {
public:
    int search(vector<int>& nums, int target) {
        int l=0, r=nums.size()-1;
        while(l<=r){
            int m=(l+r)/2;
            if(nums[m]==target) return m;
            if(nums[l]<=nums[m]){
                if(nums[l]<=target&&target<nums[m]) r=m-1; else l=m+1;
            } else {
                if(nums[m]<target&&target<=nums[r]) l=m+1; else r=m-1;
            }
        }
        return -1;
    }
};
int main(){
    vector<int> nums={4,5,6,7,0,1,2}; int target=0;
    auto s=chrono::high_resolution_clock::now(); int r=Solution_v1().search(nums,target); auto e=chrono::high_resolution_clock::now();
    cout<<"var1 (BS): "<<r<<", "<<chrono::duration_cast<chrono::nanoseconds>(e-s).count()/1000.0<<" us"<<endl;
    return 0;
}
// var1 mem = {} and time = {}
''')

write(f"{BASE}/05_binary_search/0981_time_based_key_value_store.py", '''"""
LeetCode 981: Time Based Key-Value Store
Link: https://leetcode.com/problems/time-based-key-value-store/
Difficulty: Medium
"""
import time, tracemalloc
from collections import defaultdict
import bisect

# ============= Variation 1: Binary Search =============
# Time Complexity: O(log n) per get   Space Complexity: O(n)
class TimeMap_v1:
    def __init__(self):
        self.store = defaultdict(list)
    def set(self, key: str, value: str, timestamp: int) -> None:
        self.store[key].append((timestamp, value))
    def get(self, key: str, timestamp: int) -> str:
        vals = self.store[key]
        l, r, result = 0, len(vals) - 1, ""
        while l <= r:
            mid = (l + r) // 2
            if vals[mid][0] <= timestamp:
                result = vals[mid][1]; l = mid + 1
            else: r = mid - 1
        return result

if __name__ == "__main__":
    tracemalloc.start(); t0 = time.perf_counter()
    tm = TimeMap_v1()
    tm.set("foo", "bar", 1); tm.set("foo", "bar2", 4)
    r1 = tm.get("foo", 1); r2 = tm.get("foo", 3); r3 = tm.get("foo", 5)
    t1 = time.perf_counter(); mem = tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
    print(f"var1 (BS): get(1)={r1}, get(3)={r2}, get(5)={r3}, mem = {mem} bytes, time = {(t1-t0)*1e6:.2f} µs")
# var1 mem = {} and time = {}
''')

write(f"{BASE}/05_binary_search/0981_time_based_key_value_store.cpp", '''/* LeetCode 981: Time Based Key-Value Store - Medium */
#include <bits/stdc++.h>
#include <chrono>
using namespace std;
class TimeMap {
    unordered_map<string, vector<pair<int,string>>> store;
public:
    void set(string key, string value, int timestamp) { store[key].push_back({timestamp, value}); }
    string get(string key, int timestamp) {
        auto& vals = store[key];
        int l=0, r=vals.size()-1; string res="";
        while(l<=r){ int m=(l+r)/2; if(vals[m].first<=timestamp){res=vals[m].second;l=m+1;} else r=m-1; }
        return res;
    }
};
int main(){
    auto s=chrono::high_resolution_clock::now();
    TimeMap tm; tm.set("foo","bar",1); tm.set("foo","bar2",4);
    cout<<tm.get("foo",1)<<" "<<tm.get("foo",3)<<" "<<tm.get("foo",5)<<endl;
    auto e=chrono::high_resolution_clock::now();
    cout<<"var1 (BS): "<<chrono::duration_cast<chrono::nanoseconds>(e-s).count()/1000.0<<" us"<<endl;
    return 0;
}
// var1 mem = {} and time = {}
''')

write(f"{BASE}/05_binary_search/0004_median_of_two_sorted_arrays.py", '''"""
LeetCode 4: Median of Two Sorted Arrays
Link: https://leetcode.com/problems/median-of-two-sorted-arrays/
Difficulty: Hard
"""
import time, tracemalloc
from typing import List

# ============= Variation 1: Merge + Sort =============
# Time Complexity: O((m+n) log(m+n))   Space Complexity: O(m+n)
class Solution_v1:
    def findMedianSortedArrays(self, nums1: List[int], nums2: List[int]) -> float:
        merged = sorted(nums1 + nums2)
        n = len(merged)
        if n % 2: return merged[n // 2]
        return (merged[n // 2 - 1] + merged[n // 2]) / 2

# ============= Variation 2: Binary Search =============
# Time Complexity: O(log(min(m,n)))   Space Complexity: O(1)
class Solution_v2:
    def findMedianSortedArrays(self, nums1: List[int], nums2: List[int]) -> float:
        A, B = nums1, nums2
        if len(A) > len(B): A, B = B, A
        total = len(A) + len(B)
        half = total // 2
        l, r = 0, len(A) - 1
        while True:
            i = (l + r) // 2
            j = half - i - 2
            Aleft = A[i] if i >= 0 else float('-inf')
            Aright = A[i + 1] if (i + 1) < len(A) else float('inf')
            Bleft = B[j] if j >= 0 else float('-inf')
            Bright = B[j + 1] if (j + 1) < len(B) else float('inf')
            if Aleft <= Bright and Bleft <= Aright:
                if total % 2: return min(Aright, Bright)
                return (max(Aleft, Bleft) + min(Aright, Bright)) / 2
            elif Aleft > Bright: r = i - 1
            else: l = i + 1

if __name__ == "__main__":
    nums1, nums2 = [1, 3, 5, 7], [2, 4, 6, 8, 10]
    for i, (Sol, name) in enumerate(zip([Solution_v1, Solution_v2], ["Merge+Sort", "Binary Search"]), 1):
        tracemalloc.start(); t0 = time.perf_counter()
        result = Sol().findMedianSortedArrays(nums1[:], nums2[:])
        t1 = time.perf_counter(); mem = tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{i} ({name}): result={result}, mem = {mem} bytes, time = {(t1-t0)*1e6:.2f} µs")
# var1 mem = {} and time = {}
# var2 mem = {} and time = {}
''')

write(f"{BASE}/05_binary_search/0004_median_of_two_sorted_arrays.cpp", '''/* LeetCode 4: Median of Two Sorted Arrays - Hard */
#include <bits/stdc++.h>
#include <chrono>
using namespace std;
class Solution_v1 {
public:
    double findMedianSortedArrays(vector<int>& nums1, vector<int>& nums2) {
        vector<int> merged;
        merge(nums1.begin(),nums1.end(),nums2.begin(),nums2.end(),back_inserter(merged));
        int n=merged.size();
        if(n%2) return merged[n/2];
        return (merged[n/2-1]+merged[n/2])/2.0;
    }
};
class Solution_v2 {
public:
    double findMedianSortedArrays(vector<int>& nums1, vector<int>& nums2) {
        auto& A = nums1.size()<=nums2.size() ? nums1 : nums2;
        auto& B = nums1.size()<=nums2.size() ? nums2 : nums1;
        int total=A.size()+B.size(), half=total/2;
        int l=0, r=A.size()-1;
        while(true){
            int i=(l+r)/2, j=half-i-2;
            double Al=i>=0?A[i]:-1e9, Ar=i+1<(int)A.size()?A[i+1]:1e9;
            double Bl=j>=0?B[j]:-1e9, Br=j+1<(int)B.size()?B[j+1]:1e9;
            if(Al<=Br&&Bl<=Ar){
                if(total%2) return min(Ar,Br);
                return (max(Al,Bl)+min(Ar,Br))/2.0;
            } else if(Al>Br) r=i-1; else l=i+1;
        }
    }
};
int main(){
    vector<int> n1={1,3,5,7}, n2={2,4,6,8,10};
    { auto s=chrono::high_resolution_clock::now(); double r=Solution_v1().findMedianSortedArrays(n1,n2); auto e=chrono::high_resolution_clock::now(); cout<<"var1: "<<r<<", "<<chrono::duration_cast<chrono::nanoseconds>(e-s).count()/1000.0<<" us"<<endl; }
    { auto s=chrono::high_resolution_clock::now(); double r=Solution_v2().findMedianSortedArrays(n1,n2); auto e=chrono::high_resolution_clock::now(); cout<<"var2: "<<r<<", "<<chrono::duration_cast<chrono::nanoseconds>(e-s).count()/1000.0<<" us"<<endl; }
    return 0;
}
// var1 mem = {} and time = {}
// var2 mem = {} and time = {}
''')

print("Sections 4-5 generated!")
