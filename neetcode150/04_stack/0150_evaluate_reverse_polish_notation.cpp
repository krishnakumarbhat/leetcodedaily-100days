/* LeetCode 150: Evaluate Reverse Polish Notation - Medium */
#include <bits/stdc++.h>
#include <chrono>
using namespace std;
// ============= Variation 1: Stack =============
// Algorithm: Standard stack-based evaluation. Handles tokens by checking for 
// arithmetic operators and performing `stoi` on operands.
// Time: O(n)  Space: O(n)
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
// var1 mem = N/A and time = N/A
