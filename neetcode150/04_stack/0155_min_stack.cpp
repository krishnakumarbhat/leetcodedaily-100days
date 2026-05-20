/* LeetCode 155: Min Stack - Medium */
#include <bits/stdc++.h>
#include <chrono>
using namespace std;
// ============= Variation 1: Stack of Pairs =============
// Algorithm: Every element pushed contains the actual value and the local minimum
// at the time of insertion, enabling constant time `getMin`.
// Time: O(1)  Space: O(n)
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
