#include <bits/stdc++.h>
#include <chrono>
using namespace std;
int main(){
    vector<vector<int>> matrix = {{1,2,3},{4,5,6},{7,8,9}};
    auto t=chrono::high_resolution_clock::now();
    vector<int> res;
    int left = 0, right = matrix[0].size();
    int top = 0, bottom = matrix.size();
    while (left < right && top < bottom) {
        for (int i = left; i < right; i++) res.push_back(matrix[top][i]);
        top++;
        for (int i = top; i < bottom; i++) res.push_back(matrix[i][right - 1]);
        right--;
        if (!(left < right && top < bottom)) break;
        for (int i = right - 1; i >= left; i--) res.push_back(matrix[bottom - 1][i]);
        bottom--;
        for (int i = bottom - 1; i >= top; i--) res.push_back(matrix[i][left]);
        left++;
    }
    auto e=chrono::high_resolution_clock::now();
    cout<<"var1 time="<<chrono::duration_cast<chrono::nanoseconds>(e-t).count()/1000.0<<"us"<<endl;
}
// var1 mem = {} and time = {}
