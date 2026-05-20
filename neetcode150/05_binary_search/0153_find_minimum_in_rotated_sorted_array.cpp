/* LeetCode 153: Find Min in Rotated Sorted Array - Medium */
#include <bits/stdc++.h>
#include <chrono>
using namespace std;
// ============= Variation 1: Binary Search =============
// Algorithm: Standard rotary search. If `nums[l] < nums[r]`, the range is sorted 
// and `nums[l]` is the candidate min. Otherwise, check `mid`.
// Time: O(log n)  Space: O(1)
class Solution_v1 {
public:
    int findMin(vector<int>& nums) {
        int l=0, r=nums.size()-1, res=nums[0];
        while(l<=r){
            if(nums[l]<nums[r]){res=min(res,nums[l]);break;}
            int m=(l+r)/2; res=min(res,nums[m]);
            if(nums[m]>=nums[l]) l=m+1; else r=m-1;
        }
        return res;
    }
};
int main(){
    vector<int> nums={3,4,5,1,2};
    auto s=chrono::high_resolution_clock::now(); int r=Solution_v1().findMin(nums); auto e=chrono::high_resolution_clock::now();
    cout<<"var1 (BS): "<<r<<", "<<chrono::duration_cast<chrono::nanoseconds>(e-s).count()/1000.0<<" us"<<endl;
    return 0;
}
// var1 mem = N/A and time = N/A
