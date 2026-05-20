"""LeetCode 70: Climbing Stairs - Easy"""
import time, tracemalloc

# Variation 1: DP bottom-up O(n)
class Solution_v1:
    def climbStairs(self, n: int) -> int:
        if n<=2: return n
        a,b=1,2
        for _ in range(3,n+1): a,b=b,a+b
        return b

# Variation 2: Memoized recursion
class Solution_v2:
    def climbStairs(self, n: int) -> int:
        from functools import lru_cache
        @lru_cache(None)
        def dp(i): return i if i<=2 else dp(i-1)+dp(i-2)
        return dp(n)

# Variation 3: Matrix exponentiation O(log n)
class Solution_v3:
    def climbStairs(self, n: int) -> int:
        def mat_mul(A,B):
            return [[A[0][0]*B[0][0]+A[0][1]*B[1][0], A[0][0]*B[0][1]+A[0][1]*B[1][1]],
                    [A[1][0]*B[0][0]+A[1][1]*B[1][0], A[1][0]*B[0][1]+A[1][1]*B[1][1]]]
        def mat_pow(M,p):
            result=[[1,0],[0,1]]
            while p:
                if p%2: result=mat_mul(result,M)
                M=mat_mul(M,M); p//=2
            return result
        M=[[1,1],[1,0]]
        return mat_pow(M,n)[0][0]

if __name__ == "__main__":
    n=10
    for Vi,Cls in enumerate([Solution_v1,Solution_v2,Solution_v3],1):
        tracemalloc.start(); t0=time.perf_counter()
        r=Cls().climbStairs(n)
        t1=time.perf_counter(); mem=tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{Vi}: ways={r}, mem={mem}bytes, time={(t1-t0)*1e6:.2f}us")
# var1 mem = {} and time = {}
# var2 mem = {} and time = {}
# var3 mem = {} and time = {}
