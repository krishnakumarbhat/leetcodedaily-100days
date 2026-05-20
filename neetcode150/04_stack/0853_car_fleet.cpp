/* LeetCode 853: Car Fleet - Medium */
#include <bits/stdc++.h>
#include <chrono>
using namespace std;
// ============= Variation 1: Sort + Stack =============
// Algorithm: Sort by position DESC. Calculate arrival time. Maintain a stack of 
// "fleet leaders". If a trailing car reaches target slower, it becomes a new leader.
// Time: O(n log n)  Space: O(n)
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
// var1 mem = N/A and time = N/A
