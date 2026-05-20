/* LeetCode 239: Sliding Window Maximum - Hard */
#include <bits/stdc++.h>
#include <chrono>
using namespace std;
// ============= Variation 1: Monotonic Deque =============
// Algorithm: Pop queue elements strictly outside the window linearly. 
// Pop elements smaller than current mapping to maintain peak elements instantly.
// Time: O(n)  Space: O(k)
class Solution_v1 {
public:
    vector<int> maxSlidingWindow(vector<int>& nums, int k) {
        deque<int> dq; vector<int> res;
        for(int i=0;i<nums.size();i++){
            while(!dq.empty()&&dq.front()<i-k+1) dq.pop_front();
            while(!dq.empty()&&nums[dq.back()]<nums[i]) dq.pop_back();
            dq.push_back(i);
            if(i>=k-1) res.push_back(nums[dq.front()]);
        }
        return res;
    }
};
int main(){
    vector<int> nums={1,3,-1,-3,5,3,6,7,2,4}; int k=3;
    auto st=chrono::high_resolution_clock::now(); auto r=Solution_v1().maxSlidingWindow(nums,k); auto e=chrono::high_resolution_clock::now();
    cout<<"var1 (Deque): size="<<r.size()<<", "<<chrono::duration_cast<chrono::nanoseconds>(e-st).count()/1000.0<<" us"<<endl;
    return 0;
}
// var1 mem = N/A and time = N/A
