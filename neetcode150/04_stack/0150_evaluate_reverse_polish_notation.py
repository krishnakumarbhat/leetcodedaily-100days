"""
=====================================================================
LeetCode 150 : Evaluate Reverse Polish Notation              (Medium)
https://leetcode.com/problems/evaluate-reverse-polish-notation/
Category   : Stack
---------------------------------------------------------------------
PROBLEM
    Given an array of strings `tokens` holding a valid Reverse Polish
    (postfix) arithmetic expression over + - * / with integer operands,
    evaluate it. Division truncates toward ZERO, and operands /
    results fit in 32-bit ints.
---------------------------------------------------------------------
INTUITION
    In postfix notation an operator ALWAYS applies to the two most
    recently seen operands. "Most recent first" = LIFO = stack: push
    numbers as they arrive; on an operator, pop the two top operands,
    compute, push the result back. When the token stream ends, the
    single value left on the stack is the answer.
---------------------------------------------------------------------
APPROACH 1 — Stack + operator set (BEST)
    Operands are pushed; operators pop a and b (b popped SECOND is the
    LEFT operand — order matters for - and /), then push the result.
    A set answers "is this token an operator?" in O(1).
    Time  Complexity : O(n)   Space Complexity : O(n)
---------------------------------------------------------------------
APPROACH 2 — Stack + char switch (no hash set)
    Same algorithm, but operators are recognised by shape: every
    operator token is a SINGLE character and not a digit. That makes
    a 4-case if/elif chain possible and avoids allocating a set.
    Time  Complexity : O(n)   Space Complexity : O(n)
---------------------------------------------------------------------
DEEP DIVE — the stack, and the division trap
    Postfix is stack-native: no parentheses, no precedence — the stack
    IS the expression tree being evaluated bottom-up.
    C++ int division truncates TOWARD ZERO, which matches the problem.
    Python's `//` truncates toward −∞, so -3 // 2 == -2 — the port
    must use int(a / b) to emulate C++ semantics. Same idea anywhere,
    one line changes the whole behaviour.
---------------------------------------------------------------------
REAL LIFE
    • Calculators (HP RPN calculators, spreadsheet formulas) evaluate
      postfix because it needs no parentheses or precedence table.
    • Bytecode interpreters (JVM, CPython) execute stack machines:
      every instruction pops operands and pushes a result — literally
      this problem, millions of times per second.
=====================================================================
"""

from __future__ import annotations

import time
import tracemalloc
from typing import List, Set

# =====================================================================
# APPROACH 1 : Stack + operator set (best)
# =====================================================================
class SolutionOne:
    """
    Purpose : Evaluate a valid RPN expression.
    Inputs  : tokens — postfix tokens: int strings and + - * /.
    Output  : the integer value of the expression.
    """

    def evalRPN(self, tokens: List[str]) -> int:
        # ops : the four operators, for O(1) membership tests.
        ops: Set[str] = {"+", "-", "*", "/"}

        st: List[int] = []

        for tok in tokens:
            # Number token → push the parsed value onto the stack.
            if tok not in ops:
                st.append(int(tok))
                continue

            # Operator token → pop the two most recent operands.
            # b was pushed LATER → b is the LEFT operand for - and /.
            b = st.pop()
            a = st.pop()

            # Apply, push the result — it may feed another operator.
            if tok == "+":
                st.append(a + b)
            elif tok == "-":
                st.append(a - b)
            elif tok == "*":
                st.append(a * b)
            else:
                # C++ int division truncates toward zero; Python's //
                # truncates toward −∞ → int(a / b) emulates C++.
                st.append(int(a / b))

        # Valid RPN leaves exactly one value on the stack.
        return st[-1]


# =====================================================================
# APPROACH 2 : Stack + char switch (no hash set)
# =====================================================================
class SolutionTwo:
    """
    Purpose : Evaluate a valid RPN expression.
    Inputs  : tokens — postfix tokens: int strings and + - * /.
    Output  : the integer value of the expression.
    """

    def evalRPN(self, tokens: List[str]) -> int:
        st: List[int] = []

        for tok in tokens:
            # Every operator token is exactly one non-digit character
            # (numbers may be multi-digit and signed → size > 1).
            is_op = len(tok) == 1 and not tok.isdigit()
            if not is_op:
                st.append(int(tok))
                continue

            # Same pops as approach 1 — b is the left operand.
            b = st.pop()
            a = st.pop()

            # 4-way chain: the token's single character IS the op.
            if tok == "+":
                st.append(a + b)
            elif tok == "-":
                st.append(a - b)
            elif tok == "*":
                st.append(a * b)
            else:  # '/'
                st.append(int(a / b))   # truncate toward zero

        return st[-1]


# =====================================================================
# BENCHMARK — run both approaches and compare time + peak memory
# =====================================================================
if __name__ == "__main__":
    # --- Correctness tests ---
    tests = [
        (["2", "1", "+", "3", "*"], 9),                       # (2+1)*3
        (["4", "13", "5", "/", "+"], 6),                      # 4 + 13/5
        (["10", "6", "9", "3", "+", "-11", "*", "/", "*",
          "17", "+", "5", "+"], 22),                          # long example
        (["5", "8", "-", "2", "*"], -6)                       # negative result
    ]

    all_ok = True
    for tokens, expect in tests:
        r1 = SolutionOne().evalRPN(tokens)
        r2 = SolutionTwo().evalRPN(tokens)
        ok = r1 == expect and r2 == expect
        if not ok:
            all_ok = False
        print(f"{'PASS' if ok else 'FAIL'} : {len(tokens)} tokens"
              f"  set={r1}  switch={r2}  expect={expect}")

    # --- Benchmark: long chain of mixed operations ---
    big = []
    for i in range(50000):
        big.extend([str(i), str(i + 1), "+"])
    big.extend(["2", "*"])

    tracemalloc.start()
    t0 = time.perf_counter()
    rb1 = SolutionOne().evalRPN(big)
    t1 = time.perf_counter()
    _, peak_1 = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    tracemalloc.start()
    t0b = time.perf_counter()
    rb2 = SolutionTwo().evalRPN(big)
    t1b = time.perf_counter()
    _, peak_2 = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print(f"Approach 1 (stack + set)    : {rb1}  time = {(t1 - t0) * 1e6:.2f} µs"
          f"  peak-mem = {peak_1} bytes")
    print(f"Approach 2 (stack + switch) : {rb2}  time = {(t1b - t0b) * 1e6:.2f} µs"
          f"  peak-mem = {peak_2} bytes")

    print("PASS : all tests" if all_ok else "FAIL : a test was wrong")