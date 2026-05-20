#include <bits/stdc++.h>
#include <chrono>
using namespace std;
/* LeetCode 1046: Last Stone Weight - Easy */
// var1: max-heap
int lastStoneWeight_v1(vector<int>& s) {
    priority_queue<int> pq(s.begin(), s.end());
    while (pq.size() > 1) {
        int a=pq.top(); pq.pop(); int b=pq.top(); pq.pop();
        if (a != b) pq.push(a - b);
    }
    return pq.empty() ? 0 : pq.top();
}
// var2: sort each step
int lastStoneWeight_v2(vector<int> s) {
    while (s.size() > 1) {
        sort(s.begin(), s.end());
        int a=s.back(); s.pop_back(); int b=s.back(); s.pop_back();
        if (a != b) s.push_back(a-b);
    }
    return s.empty() ? 0 : s[0];
}
int main() {
    vector<int> s = {2,7,4,1,8,1};
    auto t1=chrono::high_resolution_clock::now(); cout<<"var1: "<<lastStoneWeight_v1(s)<<endl;
    auto t2=chrono::high_resolution_clock::now(); cout<<"var1 time="<<chrono::duration_cast<chrono::nanoseconds>(t2-t1).count()/1000.0<<"us"<<endl;
    s={2,7,4,1,8,1};
    auto t3=chrono::high_resolution_clock::now(); cout<<"var2: "<<lastStoneWeight_v2(s)<<endl;
    auto t4=chrono::high_resolution_clock::now(); cout<<"var2 time="<<chrono::duration_cast<chrono::nanoseconds>(t4-t3).count()/1000.0<<"us"<<endl;
}
// var1 mem = {} and time = {}
// var2 mem = {} and time = {}
