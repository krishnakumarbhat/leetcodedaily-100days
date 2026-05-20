#include <bits/stdc++.h>
#include <chrono>
using namespace std;
int main(){
    int x = 123;
    auto t=chrono::high_resolution_clock::now();
    int res = 0;
    while(x){
        int digit = x % 10; x /= 10;
        if(res > INT_MAX / 10 || (res == INT_MAX / 10 && digit >= INT_MAX % 10)){ cout<<"var1: 0"<<endl; return 0; }
        if(res < INT_MIN / 10 || (res == INT_MIN / 10 && digit <= INT_MIN % 10)){ cout<<"var1: 0"<<endl; return 0; }
        res = (res * 10) + digit;
    }
    cout<<"var1: "<<res<<endl;
    auto e=chrono::high_resolution_clock::now();
    cout<<"var1 time="<<chrono::duration_cast<chrono::nanoseconds>(e-t).count()/1000.0<<"us"<<endl;
}
// var1 mem = {} and time = {}
