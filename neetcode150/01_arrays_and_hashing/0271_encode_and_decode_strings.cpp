/*
 * =====================================================================
 * LeetCode 271 : Encode and Decode Strings                     (Medium)
 * (Originally LintCode 659 — not on LeetCode main site)
 * Category   : Arrays & Hashing
 * ---------------------------------------------------------------------
 * PROBLEM
 *   Design encode(strs) → a single string and decode(s) → the
 *   original list. The payload may contain ANY character, including
 *   the delimiter we pick — so naive joining with '#' is ambiguous.
 * ---------------------------------------------------------------------
 * INTUITION
 *   The decoder needs to know where each word ENDS. Instead of a
 *   terminator character (which the payload can fake), ship the
 *   LENGTH of each word first: "4#neet4#code". The decoder reads an
 *   integer, then that many characters — framing is self-describing
 *   and immune to payload content.
 * ---------------------------------------------------------------------
 * APPROACH 1 — Length-prefix framing (BEST, robust)
 *   encode : for each word → to_string(len) + "#" + word, concatenate.
 *   decode : scan s; read digits until '#'; take that many chars.
 *   Time  Complexity : O(T)   Space Complexity : O(T)
 *   (T = total characters in all words).
 *   WHY length prefix beats a plain delimiter: if a word itself
 *   contains '#' or the delimiter sequence, naive parsing breaks.
 *   Lengths make the frame unambiguous — the exact format used by
 *   network protocols (e.g. HTTP Content-Length, Protobuf varints).
 * ---------------------------------------------------------------------
 * APPROACH 2 — Escaped delimiter
 *   Replace every '#' in a word with "/#" and every '/' with "//",
 *   join with '#'; decode reverses the escape. Works too, but every
 *   escape costs CPU and the format is harder to eyeball.
 * =====================================================================
 */

#include <vector>          // std::vector — input/output list of words
#include <string>          // std::string — words and the framed stream
#include <chrono>          // timing for the benchmark
#include <iostream>        // std::cout — benchmark output
#include <sys/resource.h>  // getrusage — peak RAM measurement

using namespace std;

/* =====================================================================
 * APPROACH 1 : Length-prefix framing — "4#neet4#code"
 * ===================================================================== */
class Codec_LengthPrefix {
public:
    /*
     * Purpose : Serialize a list of words into one unambiguous string.
     * Inputs  : strs — list of arbitrary strings (any characters).
     * Output  : the framed stream "len#word len#word ...".
     */
    string encode(const vector<string>& strs) {

        // result : the growing framed stream.
        string result;

        // Frame every word with its byte length.
        for (const string& w : strs) {
            // length, then the '#' separator, then the raw word.
            result += to_string(w.size()) + "#" + w;
        }
        return result;
    }

    /*
     * Purpose : Recover the original list from a framed stream.
     * Inputs  : s — the stream produced by encode().
     * Output  : the decoded list of words.
     */
    vector<string> decode(const string& s) {

        // result : the recovered words.
        vector<string> result;

        // i : read position inside the stream.
        int i = 0;
        while (i < static_cast<int>(s.size())) {

            // Collect all digits up to '#' — that is the frame length.
            int j = i;
            while (s[j] != '#') {
                ++j;
            }

            // Parse the length (e.g. "4" → 4).
            int len = stoi(s.substr(i, j - i));

            // Jump past "len#" and slice exactly `len` characters.
            i = j + 1;
            result.push_back(s.substr(i, len));

            // Advance past the word to the next frame.
            i += len;
        }
        return result;
    }
};

/* =====================================================================
 * APPROACH 2 : Escaped delimiter — '#' → "/#", '/' → "//"
 * ===================================================================== */
class Codec_EscapeDelimiter {
public:
    /*
     * Purpose : Serialize a list of words with an escaped delimiter.
     * Inputs  : strs — list of arbitrary strings.
     * Output  : words joined by '#', with '#' and '/' escaped.
     */
    string encode(const vector<string>& strs) {

        // result : the escaped, joined stream.
        string result;
        for (const string& w : strs) {

            // Escape every '#' and '/' inside the word FIRST,
            // so the joining '#' is the ONLY unescaped one.
            for (char c : w) {
                if (c == '#' || c == '/') {
                    result += '/';  // escape marker prefix
                }
                result += c;
            }

            // The separator between words stays a bare '#'.
            result += '#';
        }
        return result;
    }

    /*
     * Purpose : Recover the original list from an escaped stream.
     * Inputs  : s — the stream produced by encode().
     * Output  : the decoded list of words.
     */
    vector<string> decode(const string& s) {

        // result : the recovered words.
        vector<string> result;

        // current : the word being rebuilt.
        string current;

        // i : read position inside the stream.
        for (int i = 0; i < static_cast<int>(s.size()); ++i) {

            // '#' while unescaped = end of the current word.
            if (s[i] == '#') {
                result.push_back(current);
                current.clear();
                continue;
            }

            // Escape marker: the NEXT character is literal.
            if (s[i] == '/') {
                ++i;                    // consume the marker
                current += s[i];        // take the escaped character verbatim
                continue;
            }

            // Ordinary character → part of the current word.
            current += s[i];
        }
        return result;
    }
};

/* =====================================================================
 * BENCHMARK — time + peak RAM for both approaches
 * ===================================================================== */
int main() {
    // Words containing the delimiter, slashes and empty string — the
    // nasty cases that break naive encoders.
    vector<string> words = {"neet", "code", "#has#hash#", "a/b/c", "", "end"};

    // --- Approach 1 ---
    struct rusage b1, a1;
    getrusage(RUSAGE_SELF, &b1);
    auto s1 = chrono::high_resolution_clock::now();
    Codec_LengthPrefix c1;
    string enc1 = c1.encode(words);
    vector<string> dec1 = c1.decode(enc1);
    auto e1 = chrono::high_resolution_clock::now();
    getrusage(RUSAGE_SELF, &a1);
    double us1 = chrono::duration_cast<chrono::nanoseconds>(e1 - s1).count() / 1000.0;
    long mem1 = (a1.ru_maxrss - b1.ru_maxrss) / 1024;

    // --- Approach 2 ---
    struct rusage b2, a2;
    getrusage(RUSAGE_SELF, &b2);
    auto s2 = chrono::high_resolution_clock::now();
    Codec_EscapeDelimiter c2;
    string enc2 = c2.encode(words);
    vector<string> dec2 = c2.decode(enc2);
    auto e2 = chrono::high_resolution_clock::now();
    getrusage(RUSAGE_SELF, &a2);
    double us2 = chrono::duration_cast<chrono::nanoseconds>(e2 - s2).count() / 1000.0;
    long mem2 = (a2.ru_maxrss - b2.ru_maxrss) / 1024;

    cout << "Approach 1 (length prefix)  : \"" << enc1 << "\" → "
         << dec1.size() << " words  time = " << us1 << " µs  peak-ram-delta = " << mem1 << " MB\n";
    cout << "Approach 2 (escaped delim)  : \"" << enc2 << "\" → "
         << dec2.size() << " words  time = " << us2 << " µs  peak-ram-delta = " << mem2 << " MB\n";

    bool ok1 = (dec1 == words);
    bool ok2 = (dec2 == words);
    cout << ((ok1 && ok2) ? "PASS : both codecs round-trip correctly."
                          : "FAIL : round-trip mismatch.")
         << "\n";
    return 0;
}