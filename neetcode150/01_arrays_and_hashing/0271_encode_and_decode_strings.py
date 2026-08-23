"""
=====================================================================
LeetCode 271 : Encode and Decode Strings                     (Medium)
(Originally LintCode 659 — not on LeetCode main site)
Category   : Arrays & Hashing
---------------------------------------------------------------------
PROBLEM
    Design encode(strs) → one string and decode(s) → the original
    list. The payload may contain ANY character, including our
    delimiter — so naive joining is ambiguous.
---------------------------------------------------------------------
INTUITION
    The decoder must know where each word ENDS. Ship the LENGTH of
    every word first: "4#neet4#code". Framing is self-describing and
    immune to payload content.
---------------------------------------------------------------------
APPROACH 1 — Length-prefix framing (BEST, robust)
    Time  Complexity : O(T)   Space Complexity : O(T)
    (T = total characters).
    WHY length prefix beats a delimiter: if a word contains the
    delimiter itself, parsing breaks. Lengths are unambiguous — the
    same trick as HTTP Content-Length and Protobuf varints.
---------------------------------------------------------------------
APPROACH 2 — Escaped delimiter ('#' → "/#", '/' → "//")
    Also O(T)/O(T). Works, but every escape costs CPU and the stream
    is harder to read by eye.
=====================================================================
"""

from __future__ import annotations
import time
import tracemalloc
from typing import List


# =====================================================================
# APPROACH 1 : Length-prefix framing — "4#neet4#code"
# =====================================================================
class Codec_LengthPrefix:
    """
    Purpose : Serialize a list of words into one unambiguous string.
    Inputs  : strs — list of arbitrary strings (any characters).
    Output  : the framed stream "len#word len#word ...".
    """

    def encode(self, strs: List[str]) -> str:
        # result : the growing framed stream.
        result = ""

        # Frame every word with its byte length.
        for word in strs:
            # length, then the '#' separator, then the raw word.
            result += str(len(word)) + "#" + word

        return result

    def decode(self, s: str) -> List[str]:
        """
        Purpose : Recover the original list from a framed stream.
        Inputs  : s — the stream produced by encode().
        Output  : the decoded list of words.
        """
        # result : the recovered words.
        result: List[str] = []

        # i : read position inside the stream.
        i = 0
        while i < len(s):
            # Find the '#' that ends the length digits.
            j = s.index("#", i)

            # Parse the length (e.g. "4" → 4).
            length = int(s[i:j])

            # Jump past "len#" and slice exactly `length` characters.
            i = j + 1
            result.append(s[i:i + length])

            # Advance past the word to the next frame.
            i += length

        return result


# =====================================================================
# APPROACH 2 : Escaped delimiter — '#' → "/#", '/' → "//"
# =====================================================================
class Codec_EscapeDelimiter:
    """
    Purpose : Serialize a list of words with an escaped delimiter.
    Inputs  : strs — list of arbitrary strings.
    Output  : words joined by '#', with '#' and '/' escaped.
    """

    def encode(self, strs: List[str]) -> str:
        # result : the escaped, joined stream.
        result = ""
        for word in strs:
            # Escape every '#' and '/' inside the word FIRST, so the
            # joining '#' is the ONLY unescaped one.
            for ch in word:
                if ch in "#/":
                    result += "/"  # escape marker prefix
                result += ch

            # The separator between words stays a bare '#'.
            result += "#"

        return result

    def decode(self, s: str) -> List[str]:
        """
        Purpose : Recover the original list from an escaped stream.
        Inputs  : s — the stream produced by encode().
        Output  : the decoded list of words.
        """
        # result : the recovered words.
        result: List[str] = []
        # current : the word being rebuilt.
        current = ""

        # i : read position inside the stream.
        i = 0
        while i < len(s):
            # '#' while unescaped = end of the current word.
            if s[i] == "#":
                result.append(current)
                current = ""
            elif s[i] == "/":
                # Escape marker: the NEXT character is literal.
                i += 1
                current += s[i]
            else:
                # Ordinary character → part of the current word.
                current += s[i]
            i += 1

        return result


# =====================================================================
# BENCHMARK — time + peak memory for both approaches
# =====================================================================
if __name__ == "__main__":
    # Words containing the delimiter, slashes and empty string — the
    # nasty cases that break naive encoders.
    words = ["neet", "code", "#has#hash#", "a/b/c", "", "end"]

    tracemalloc.start()
    t0 = time.perf_counter()
    c1 = Codec_LengthPrefix()
    dec1 = c1.decode(c1.encode(words))
    t1 = time.perf_counter()
    _, peak1 = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    tracemalloc.start()
    t2 = time.perf_counter()
    c2 = Codec_EscapeDelimiter()
    dec2 = c2.decode(c2.encode(words))
    t3 = time.perf_counter()
    _, peak2 = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    ok1 = dec1 == words
    ok2 = dec2 == words
    print(f"Approach 1 (length prefix)  : round-trip={'OK' if ok1 else 'FAIL'}  time = {(t1 - t0) * 1e6:.2f} µs  peak-mem = {peak1} bytes")
    print(f"Approach 2 (escaped delim)  : round-trip={'OK' if ok2 else 'FAIL'}  time = {(t3 - t2) * 1e6:.2f} µs  peak-mem = {peak2} bytes")
    print("PASS : both codecs round-trip correctly." if ok1 and ok2 else "FAIL : round-trip mismatch.")