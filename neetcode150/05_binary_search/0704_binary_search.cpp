/* LeetCode 704: Binary Search - Easy */
#include <bits/stdc++.h>
#include <chrono>
using namespace std;
// ============= Variation 1: Iterative =============
// Algorithm: Classic binary search using while loop and mid-point comparisons.
// Time: O(log n)  Space: O(1)
class Solution_v1 {
public:
    int search(vector<int>& nums, int target) {
        int l=0, r=nums.size()-1;
        while(l<=r){int m=(l+r)/2; if(nums[m]==target) return m; else if(nums[m]<target) l=m+1; else r=m-1;}
        return -1;
    }
};
int main(){
    vector<int> nums={-1,0,3,5,9,12}; int target=9;
    auto s=chrono::high_resolution_clock::now(); int r=Solution_v1().search(nums,target); auto e=chrono::high_resolution_clock::now();
    cout<<"var1 (Iterative): "<<r<<", "<<chrono::duration_cast<chrono::nanoseconds>(e-s).count()/1000.0<<" us"<<endl;
    return 0;
}
// var1 mem = N/A and time = N/A
