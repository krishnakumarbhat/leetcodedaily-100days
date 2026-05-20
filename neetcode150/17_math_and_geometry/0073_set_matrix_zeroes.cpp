#include <bits/stdc++.h>
#include <chrono>
using namespace std;
int main(){
    vector<vector<int>> matrix = {{1,1,1},{1,0,1},{1,1,1}};
    auto t=chrono::high_resolution_clock::now();
    int ROWS = matrix.size(), COLS = matrix[0].size();
    bool rowZero = false;
    for(int r=0; r<ROWS; r++){
        for(int c=0; c<COLS; c++){
            if(matrix[r][c] == 0){
                matrix[0][c] = 0;
                if(r > 0) matrix[r][0] = 0;
                else rowZero = true;
            }
        }
    }
    for(int r=1; r<ROWS; r++){
        for(int c=1; c<COLS; c++){
            if(matrix[0][c] == 0 || matrix[r][0] == 0) matrix[r][c] = 0;
        }
    }
    if(matrix[0][0] == 0) for(int r=0; r<ROWS; r++) matrix[r][0] = 0;
    if(rowZero) for(int c=0; c<COLS; c++) matrix[0][c] = 0;
    auto e=chrono::high_resolution_clock::now();
    cout<<"var1 time="<<chrono::duration_cast<chrono::nanoseconds>(e-t).count()/1000.0<<"us"<<endl;
}
// var1 mem = {} and time = {}
