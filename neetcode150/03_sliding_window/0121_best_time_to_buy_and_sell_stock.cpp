/*
 * LeetCode 121: Best Time to Buy and Sell Stock
 * Difficulty: Easy
 */
#include <bits/stdc++.h>
#include <chrono>
using namespace std;

// ============= Variation 1: Brute Force =============
// Algorithm: Check all (buy, sell) pair prices to evaluate delta.
// Time: O(n^2)  Space: O(1)
class Solution_v1 {
public:
    int maxProfit(vector<int>& prices) {
        int mx = 0;
        for (int i = 0; i < prices.size(); i++)
            for (int j = i+1; j < prices.size(); j++)
                mx = max(mx, prices[j] - prices[i]);
        return mx;
    }
};

// ============= Variation 2: One Pass =============
// Algorithm: Lazily track the minP seen across loop iterations mapping maximum bounds natively.
// Time: O(n)  Space: O(1)
class Solution_v2 {
public:
    int maxProfit(vector<int>& prices) {
        int minP = INT_MAX, mx = 0;
        for (int p : prices) { minP = min(minP, p); mx = max(mx, p - minP); }
        return mx;
    }
};

int main() {
    vector<int> prices = {7, 1, 5, 3, 6, 4, 8, 2, 9, 1};
    { auto d=prices; auto s=chrono::high_resolution_clock::now(); int r=Solution_v1().maxProfit(d); auto e=chrono::high_resolution_clock::now(); cout<<"var1 (Brute): "<<r<<", "<<chrono::duration_cast<chrono::nanoseconds>(e-s).count()/1000.0<<" us"<<endl; }
    { auto d=prices; auto s=chrono::high_resolution_clock::now(); int r=Solution_v2().maxProfit(d); auto e=chrono::high_resolution_clock::now(); cout<<"var2 (OnePass): "<<r<<", "<<chrono::duration_cast<chrono::nanoseconds>(e-s).count()/1000.0<<" us"<<endl; }
    return 0;
}
// var1 mem = N/A and time = N/A
// var2 mem = N/A and time = N/A
