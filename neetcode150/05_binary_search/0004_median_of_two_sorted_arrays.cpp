/* LeetCode 4: Median of Two Sorted Arrays - Hard */
#include <bits/stdc++.h>
#include <chrono>
using namespace std;
// ============= Variation 1: Merge =============
// Algorithm: Use `std::merge` to combine sorted vectors into one, then 
// calculate median based on even/odd size.
// Time: O(m+n)  Space: O(m+n)
class Solution_v1 {
public:
    double findMedianSortedArrays(vector<int>& nums1, vector<int>& nums2) {
        vector<int> merged;
        merge(nums1.begin(),nums1.end(),nums2.begin(),nums2.end(),back_inserter(merged));
        int n=merged.size();
        if(n%2) return merged[n/2];
        return (merged[n/2-1]+merged[n/2])/2.0;
    }
};
// ============= Variation 2: Binary Search =============
// Algorithm: Partition-based approach. Binary search on the smaller array to 
// find a cut point that satisfies the median properties across both arrays.
// Time: O(log(min(m,n)))  Space: O(1)
class Solution_v2 {
public:
    double findMedianSortedArrays(vector<int>& nums1, vector<int>& nums2) {
        auto& A = nums1.size()<=nums2.size() ? nums1 : nums2;
        auto& B = nums1.size()<=nums2.size() ? nums2 : nums1;
        int total=A.size()+B.size(), half=total/2;
        int l=0, r=A.size()-1;
        while(true){
            int i=(l+r)/2, j=half-i-2;
            double Al=i>=0?A[i]:-1e9, Ar=i+1<(int)A.size()?A[i+1]:1e9;
            double Bl=j>=0?B[j]:-1e9, Br=j+1<(int)B.size()?B[j+1]:1e9;
            if(Al<=Br&&Bl<=Ar){
                if(total%2) return min(Ar,Br);
                return (max(Al,Bl)+min(Ar,Br))/2.0;
            } else if(Al>Br) r=i-1; else l=i+1;
        }
    }
};
int main(){
    vector<int> n1={1,3,5,7}, n2={2,4,6,8,10};
    { auto s=chrono::high_resolution_clock::now(); double r=Solution_v1().findMedianSortedArrays(n1,n2); auto e=chrono::high_resolution_clock::now(); cout<<"var1: "<<r<<", "<<chrono::duration_cast<chrono::nanoseconds>(e-s).count()/1000.0<<" us"<<endl; }
    { auto s=chrono::high_resolution_clock::now(); double r=Solution_v2().findMedianSortedArrays(n1,n2); auto e=chrono::high_resolution_clock::now(); cout<<"var2: "<<r<<", "<<chrono::duration_cast<chrono::nanoseconds>(e-s).count()/1000.0<<" us"<<endl; }
    return 0;
}
// var1 mem = N/A and time = N/A
// var2 mem = N/A and time = N/A
