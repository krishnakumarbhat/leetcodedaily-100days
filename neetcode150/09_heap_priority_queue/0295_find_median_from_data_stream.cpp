#include <bits/stdc++.h>
#include <chrono>
using namespace std;
/* LeetCode 295: Find Median from Data Stream - Hard */
class MedianFinder {
    priority_queue<int> lo;                             // max-heap (lower half)
    priority_queue<int,vector<int>,greater<int>> hi;    // min-heap (upper half)
public:
    void addNum(int num) {
        lo.push(num);
        hi.push(lo.top()); lo.pop();
        if (hi.size() > lo.size()) { lo.push(hi.top()); hi.pop(); }
    }
    double findMedian() {
        return lo.size() > hi.size() ? lo.top() : (lo.top() + hi.top()) / 2.0;
    }
};
int main(){
    auto s=chrono::high_resolution_clock::now();
    MedianFinder mf;
    for(int v:{1,2,3,4,5}){ mf.addNum(v); cout<<mf.findMedian()<<" "; } cout<<endl;
    auto e=chrono::high_resolution_clock::now();
    cout<<"var1 time="<<chrono::duration_cast<chrono::nanoseconds>(e-s).count()/1000.0<<"us"<<endl;
}
// var1 mem = {} and time = {}
