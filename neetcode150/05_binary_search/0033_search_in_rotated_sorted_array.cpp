/* LeetCode 33: Search in Rotated Sorted Array - Medium */
#include <bits/stdc++.h>
#include <chrono>
using namespace std;
// ============= Variation 1: Binary Search =============
// Algorithm: One-pass binary search. Determine if target resides in the 
// continuously sorted half of the range.
// Time: O(log n)  Space: O(1)
class Solution_v1 {
public:
    int search(vector<int>& nums, int target) {
        int l=0, r=nums.size()-1;
        while(l<=r){
            int m=(l+r)/2;
            if(nums[m]==target) return m;
            if(nums[l]<=nums[m]){
                if(nums[l]<=target&&target<nums[m]) r=m-1; else l=m+1;
            } else {
                if(nums[m]<target&&target<=nums[r]) l=m+1; else r=m-1;
            }
        }
        return -1;
    }
};
int main(){
    vector<int> nums={4,5,6,7,0,1,2}; int target=0;
    auto s=chrono::high_resolution_clock::now(); int r=Solution_v1().search(nums,target); auto e=chrono::high_resolution_clock::now();
    cout<<"var1 (BS): "<<r<<", "<<chrono::duration_cast<chrono::nanoseconds>(e-s).count()/1000.0<<" us"<<endl;
    return 0;
}
// var1 mem = N/A and time = N/A
