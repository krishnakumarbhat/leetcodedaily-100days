/* LeetCode 875: Koko Eating Bananas - Medium */
#include <bits/stdc++.h>
#include <chrono>
using namespace std;
// ============= Variation 1: Binary Search =============
// Algorithm: Binary search on the speed `K`. Uses integer division ceiling logic 
// `(p + k - 1) / k` to compute total hours across all piles.
// Time: O(n * log(max(piles)))  Space: O(1)
class Solution_v1 {
public:
    int minEatingSpeed(vector<int>& piles, int h) {
        int l=1, r=*max_element(piles.begin(),piles.end()), res=r;
        while(l<=r){
            int k=(l+r)/2; long total=0;
            for(int p:piles) total+=(p+k-1)/k;
            if(total<=h){res=k;r=k-1;} else l=k+1;
        }
        return res;
    }
};
int main(){
    vector<int> piles={3,6,7,11}; int h=8;
    auto s=chrono::high_resolution_clock::now(); int r=Solution_v1().minEatingSpeed(piles,h); auto e=chrono::high_resolution_clock::now();
    cout<<"var1 (BS): "<<r<<", "<<chrono::duration_cast<chrono::nanoseconds>(e-s).count()/1000.0<<" us"<<endl;
    return 0;
}
// var1 mem = N/A and time = N/A
