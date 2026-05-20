#include <bits/stdc++.h>
#include <chrono>
using namespace std;
int sumOfSquares(int n) {
    int output = 0;
    while (n) { int digit = n % 10; digit = digit * digit; output += digit; n = n / 10; }
    return output;
}
int main(){
    int n = 19;
    auto t=chrono::high_resolution_clock::now();
    int slow = n, fast = sumOfSquares(n);
    while(fast != 1 && slow != fast){ slow = sumOfSquares(slow); fast = sumOfSquares(sumOfSquares(fast)); }
    cout<<"var1: "<<(fast == 1)<<endl;
    auto e=chrono::high_resolution_clock::now();
    cout<<"var1 time="<<chrono::duration_cast<chrono::nanoseconds>(e-t).count()/1000.0<<"us"<<endl;
}
// var1 mem = {} and time = {}
