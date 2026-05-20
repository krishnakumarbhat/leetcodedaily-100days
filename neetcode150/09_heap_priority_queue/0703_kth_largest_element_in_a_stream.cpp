#include <bits/stdc++.h>
#include <chrono>
using namespace std;
/* LeetCode 703: Kth Largest Element in a Stream - Easy */
class KthLargest {
    priority_queue<int,vector<int>,greater<int>> pq;
    int k;
public:
    KthLargest(int k, vector<int>& nums) : k(k) {
        for (int n : nums) { pq.push(n); if((int)pq.size()>k) pq.pop(); }
    }
    int add(int val) { pq.push(val); if((int)pq.size()>k) pq.pop(); return pq.top(); }
};
int main() {
    vector<int> nums = {4,5,8,2};
    auto s = chrono::high_resolution_clock::now();
    KthLargest kl(3, nums);
    vector<int> ops = {3,5,10,9,4};
    for (int v : ops) cout << kl.add(v) << " "; cout << endl;
    auto e = chrono::high_resolution_clock::now();
    cout << "var1 time=" << chrono::duration_cast<chrono::nanoseconds>(e-s).count()/1000.0 << "us" << endl;
}
// var1 mem = {} and time = {}
