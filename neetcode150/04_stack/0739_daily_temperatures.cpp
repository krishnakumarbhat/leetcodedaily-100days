/* LeetCode 739: Daily Temperatures - Medium */
#include <bits/stdc++.h>
#include <chrono>
using namespace std;
// ============= Variation 1: Monotonic Stack =============
// Algorithm: Push elements onto stack as long as temperatures are lower. 
// Populate result vector as soon as a warmer temperature triggers stack pops.
// Time: O(n)  Space: O(n)
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
// var1 mem = N/A and time = N/A
