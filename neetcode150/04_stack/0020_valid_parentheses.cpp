/* LeetCode 20: Valid Parentheses - Easy */
#include <bits/stdc++.h>
#include <chrono>
using namespace std;
// ============= Variation 1: Stack =============
// Algorithm: Push opening brackets onto a stack. When a closing bracket is met, 
// cross-reference the top element in a map. If it matches, pop; else fail early.
// Time: O(n)  Space: O(n)
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
// var1 mem = N/A and time = N/A
