/* LeetCode 287: Find the Duplicate Number - Medium */
#include <bits/stdc++.h>
#include <chrono>
using namespace std;
class Solution_v1 {
public:
    int findDuplicate(vector<int>& nums) {
        int slow=0, fast=0;
        do{ slow=nums[slow]; fast=nums[nums[fast]]; } while(slow!=fast);
        int slow2=0;
        while(slow!=slow2){ slow=nums[slow]; slow2=nums[slow2]; }
        return slow;
    }
};
int main(){
    vector<int> nums={1,3,4,2,2};
    auto s=chrono::high_resolution_clock::now(); int r=Solution_v1().findDuplicate(nums); auto e=chrono::high_resolution_clock::now();
    cout<<"var1 (Floyd): "<<r<<", "<<chrono::duration_cast<chrono::nanoseconds>(e-s).count()/1000.0<<" us"<<endl;
    return 0;
}
// var1 mem = {} and time = {}
