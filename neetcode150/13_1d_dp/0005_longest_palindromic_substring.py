"""LeetCode 5: Longest Palindromic Substring - Medium"""
import time, tracemalloc

# Variation 1: Expand around center O(n^2)
class Solution_v1:
    def longestPalindrome(self, s: str) -> str:
        res=""
        def expand(l,r):
            nonlocal res
            while l>=0 and r<len(s) and s[l]==s[r]: l-=1;r+=1
            if r-l-1>len(res): res=s[l+1:r]
        for i in range(len(s)): expand(i,i); expand(i,i+1)
        return res

# Variation 2: DP table O(n^2)
class Solution_v2:
    def longestPalindrome(self, s: str) -> str:
        n=len(s); dp=[[False]*n for _ in range(n)]
        start,mx=0,1
        for i in range(n): dp[i][i]=True
        for i in range(n-1):
            if s[i]==s[i+1]: dp[i][i+1]=True; start=i; mx=2
        for length in range(3,n+1):
            for i in range(n-length+1):
                j=i+length-1
                if s[i]==s[j] and dp[i+1][j-1]: dp[i][j]=True; start=i; mx=length
        return s[start:start+mx]

# Variation 3: Manacher O(n)
class Solution_v3:
    def longestPalindrome(self, s: str) -> str:
        t="$#"+"#".join(s)+"#@"; n=len(t)
        p=[0]*n; c=r=0
        for i in range(1,n-1):
            if i<r: p[i]=min(r-i,p[2*c-i])
            while t[i+p[i]+1]==t[i-p[i]-1]: p[i]+=1
            if i+p[i]>r: c,r=i,i+p[i]
        best=max(range(n),key=lambda i:p[i])
        return s[(best-p[best])//2:(best+p[best])//2]

if __name__ == "__main__":
    s="babad"
    for Vi,Cls in enumerate([Solution_v1,Solution_v2,Solution_v3],1):
        tracemalloc.start(); t0=time.perf_counter()
        r=Cls().longestPalindrome(s)
        t1=time.perf_counter(); mem=tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{Vi}: {r!r}, mem={mem}bytes, time={(t1-t0)*1e6:.2f}us")
# var1 mem = {} and time = {}
# var2 mem = {} and time = {}
# var3 mem = {} and time = {}
