/* LeetCode 84: Largest Rectangle in Histogram - Hard */
#include <bits/stdc++.h>
#include <chrono>
using namespace std;
// ============= Variation 1: Monotonic Stack =============
// Algorithm: Use a stack to track indices where heights are non-decreasing. 
// When a drop in height occurs, pop elements and calculate potential area.
// Time: O(n)  Space: O(n)
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
// var1 mem = N/A and time = N/A
