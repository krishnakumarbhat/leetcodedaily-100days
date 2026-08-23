"""
=====================================================================
LeetCode 50 : Pow(x, n)                                        (Medium)
https://leetcode.com/problems/powx-n/
Category   : Math & Geometry
---------------------------------------------------------------------
PROBLEM
    Implement pow(x, n): raise a float `x` to an integer `n` where
    n may be negative (down to -2^31). Return a double.
---------------------------------------------------------------------
INTUITION
    Naive: multiply x by itself |n| times → O(n), hopeless for
    n = 10^9. KEY OBSERVATION: squaring HALVES the exponent:
    x^8 = (x^4)^2 = ((x^2)^2)^2 → only log2(8) = 3 multiplications.
    That is exponentiation by squaring: O(log n) multiplications.
---------------------------------------------------------------------
APPROACH 1 — Iterative exponentiation by squaring (BEST)
    Sweep the BITS of n. Maintain base = x^(2^k) (doubling k each
    step via base *= base). Whenever bit k of n is set, multiply
    base into the running result.
    Time  Complexity : O(log n)   Space Complexity : O(1)
    WHY it works: binary expansion n = Σ 2^k (set bits) gives
    x^n = ∏ x^(2^k) — the squaring chain materializes each factor.
---------------------------------------------------------------------
APPROACH 2 — Recursive halving
    Recurrence: n even → p = pow(x, n//2), return p·p;
                n odd  → return x · p · p.
    Time  Complexity : O(log n)   Space Complexity : O(log n)
    (call stack depth ≈ log2(n))
---------------------------------------------------------------------
REAL LIFE
    • Cryptography: modular exponentiation in RSA/Diffie-Hellman is
      the same bit-sweep — a 2048-bit exponent needs only ~2048
      squarings, not 2^2048 multiplications.
    • Graphics/simulations: lighting falloff, camera zoom factors
      and interest compounding all evaluate big powers cheaply.
=====================================================================
"""

from __future__ import annotations

import time
import tracemalloc


# =====================================================================
# APPROACH 1 : Iterative exponentiation by squaring (bit sweep)
# =====================================================================
class SolutionOne:
    """
    Purpose : Compute x raised to the integer power n.
    Inputs  : x — base (float); n — exponent (int, may be negative).
    Output  : float approximation of x**n.
    """

    def myPow(self, x: float, n: int) -> float:
        # 64-bit exponent: -(-2^31) overflows a 32-bit int, not Python
        # ints (arbitrary precision) — but keep the pattern anyway.
        exp = n

        # Negative exponent → reciprocal of the positive power.
        # Inverting x up-front makes the bit loop work only on exp > 0.
        if exp < 0:
            x = 1.0 / x
            exp = -exp

        result = 1.0
        base = x                 # base = x^(2^k) as the loop advances k

        while exp > 0:
            # Bit k of exp is set → x^(2^k) belongs in the product.
            if exp % 2 == 1:
                result *= base
            base *= base         # square: x^(2^k) → x^(2^(k+1))
            exp //= 2            # advance to the next bit
        return result


# =====================================================================
# APPROACH 2 : Recursive halving (same math, O(log n) call stack)
# =====================================================================
class SolutionTwo:
    """
    Purpose : Compute x**n via the halving recurrence.
    Inputs  : x — base (float); n — exponent (int, may be negative).
    Output  : float approximation of x**n.
    """

    def myPow(self, x: float, n: int) -> float:
        if n == 0:
            return 1.0            # x^0 = 1 for every x

        if n < 0:
            # Reciprocal, computed recursively on -n (Python ints
            # negate INT_MIN without overflow).
            return 1.0 / self.myPow(x, -n)

        p = self.myPow(x, n // 2)  # halve: p = x^(n//2) (floor for odd n)

        # even n → x^n = (x^(n/2))² ; odd n → one extra factor of x.
        return p * p if n % 2 == 0 else p * p * x


# =====================================================================
# BENCHMARK — both approaches on 3 tests; time + peak memory (KB)
# =====================================================================
if __name__ == "__main__":
    tests = [(2.0, 10, 1024.0), (2.1, 3, 9.261), (2.0, -2, 0.25)]

    def run(label: str, solve) -> bool:
        """
        Purpose : Run one solution class over every test and print a row.
        Inputs  : label — display name of the approach.
                  solve — callable(x, n) -> float.
        Output  : bool — True when every test passed.
        """
        tracemalloc.start()
        t0 = time.perf_counter()
        ok = True
        for x, n, want in tests:
            got = solve(x, n)
            rel = (got - want) / want if want != 0.0 else got
            pass_ = abs(rel) < 1e-9
            ok = ok and pass_
            print(f"  {x}^{n} = {got}  {'PASS' if pass_ else 'FAIL (want ' + str(want) + ')'}")
        t1 = time.perf_counter()
        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        print(f"{label} : {'PASS' if ok else 'FAIL'}  time = {(t1 - t0) * 1e6:.1f} us  peak-mem = {peak // 1024} KB")
        return ok

    ok1 = run("Approach 1 (iterative bit sweep)   ", lambda x, n: SolutionOne().myPow(x, n))
    ok2 = run("Approach 2 (recursive halving)     ", lambda x, n: SolutionTwo().myPow(x, n))

    print("PASS : both approaches match the expected powers on all tests."
          if ok1 and ok2
          else "FAIL : at least one test failed.")
