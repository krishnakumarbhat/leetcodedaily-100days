/* LeetCode 74: Search a 2D Matrix - Medium */
#include <bits/stdc++.h>
#include <chrono>
using namespace std;
// ============= Variation 1: Binary Search =============
// Algorithm: View the matrix as a flattened array and run binary search on 
// the virtual range `[0, m*n - 1]`.
// Time: O(log(m*n))  Space: O(1)
class Solution_v1 {
public:
    bool searchMatrix(vector<vector<int>>& matrix, int target) {
        int m=matrix.size(), n=matrix[0].size(), l=0, r=m*n-1;
        while(l<=r){ int mid=(l+r)/2, val=matrix[mid/n][mid%n]; if(val==target) return true; else if(val<target) l=mid+1; else r=mid-1; }
        return false;
    }
};
int main(){
    vector<vector<int>> matrix={{1,3,5,7},{10,11,16,20},{23,30,34,60}}; int target=3;
    auto s=chrono::high_resolution_clock::now(); bool r=Solution_v1().searchMatrix(matrix,target); auto e=chrono::high_resolution_clock::now();
    cout<<"var1 (BS): "<<r<<", "<<chrono::duration_cast<chrono::nanoseconds>(e-s).count()/1000.0<<" us"<<endl;
    return 0;
}
// var1 mem = N/A and time = N/A
