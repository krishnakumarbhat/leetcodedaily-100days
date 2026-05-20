#include <bits/stdc++.h>
#include <chrono>
using namespace std;
int main(){
    vector<int> digits = {1,2,3};
    auto t=chrono::high_resolution_clock::now();
    for(int i = digits.size() - 1; i >= 0; i--) {
        if(digits[i] == 9) digits[i] = 0;
        else { digits[i] += 1; break; }
    }
    if(digits[0] == 0) { digits.insert(digits.begin(), 1); }
    auto e=chrono::high_resolution_clock::now();
    cout<<"var1 time="<<chrono::duration_cast<chrono::nanoseconds>(e-t).count()/1000.0<<"us"<<endl;
}
// var1 mem = {} and time = {}
