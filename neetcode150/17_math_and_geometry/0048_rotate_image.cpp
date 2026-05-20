#include <bits/stdc++.h>
#include <chrono>
using namespace std;
int main(){
    vector<vector<int>> matrix = {{1,2,3},{4,5,6},{7,8,9}};
    auto t=chrono::high_resolution_clock::now();
    reverse(matrix.begin(), matrix.end());
    for(int i=0; i<matrix.size(); i++){
        for(int j=0; j<i; j++){
            swap(matrix[i][j], matrix[j][i]);
        }
    }
    auto e=chrono::high_resolution_clock::now();
    cout<<"var1 time="<<chrono::duration_cast<chrono::nanoseconds>(e-t).count()/1000.0<<"us"<<endl;
}
// var1 mem = {} and time = {}
