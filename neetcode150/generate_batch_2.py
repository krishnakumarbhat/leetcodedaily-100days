#!/usr/bin/env python3
"""Batch generator for Sections 6-10"""
import os
BASE = "/media/pope/projecteo/github_proj/leetcode/neetcode150"
def write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(content)

# ======================================================================
# SECTION 6: LINKED LIST (11 problems)
# ======================================================================

write(f"{BASE}/06_linked_list/0206_reverse_linked_list.py", '''"""
LeetCode 206: Reverse Linked List - Easy
"""
import time, tracemalloc
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val; self.next = next
def build(arr):
    dummy = ListNode(0)
    cur = dummy
    for v in arr: cur.next = ListNode(v); cur = cur.next
    return dummy.next
def to_list(node):
    res = []
    while node: res.append(node.val); node = node.next
    return res

# ============= Variation 1: Iterative =============
# Time: O(n)   Space: O(1)
class Solution_v1:
    def reverseList(self, head):
        prev, cur = None, head
        while cur:
            nxt = cur.next; cur.next = prev; prev = cur; cur = nxt
        return prev

# ============= Variation 2: Recursive =============
# Time: O(n)   Space: O(n)
class Solution_v2:
    def reverseList(self, head):
        if not head or not head.next: return head
        new_head = self.reverseList(head.next)
        head.next.next = head; head.next = None
        return new_head

if __name__ == "__main__":
    data = [1, 2, 3, 4, 5]
    for i, (Sol, name) in enumerate(zip([Solution_v1, Solution_v2], ["Iterative", "Recursive"]), 1):
        tracemalloc.start(); t0 = time.perf_counter()
        result = to_list(Sol().reverseList(build(data)))
        t1 = time.perf_counter(); mem = tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{i} ({name}): result={result}, mem = {mem} bytes, time = {(t1-t0)*1e6:.2f} us")
# var1 mem = {} and time = {}
# var2 mem = {} and time = {}
''')

write(f"{BASE}/06_linked_list/0206_reverse_linked_list.cpp", '''/* LeetCode 206: Reverse Linked List - Easy */
#include <bits/stdc++.h>
#include <chrono>
using namespace std;
struct ListNode { int val; ListNode* next; ListNode(int x):val(x),next(nullptr){} };
class Solution_v1 {
public:
    ListNode* reverseList(ListNode* head) {
        ListNode *prev=nullptr, *cur=head;
        while(cur){ auto nxt=cur->next; cur->next=prev; prev=cur; cur=nxt; }
        return prev;
    }
};
class Solution_v2 {
public:
    ListNode* reverseList(ListNode* head) {
        if(!head||!head->next) return head;
        auto nh=reverseList(head->next);
        head->next->next=head; head->next=nullptr;
        return nh;
    }
};
int main(){
    auto build=[](vector<int> v){ ListNode* d=new ListNode(0); auto c=d; for(int x:v){c->next=new ListNode(x);c=c->next;} return d->next; };
    { auto h=build({1,2,3,4,5}); auto s=chrono::high_resolution_clock::now(); auto r=Solution_v1().reverseList(h); auto e=chrono::high_resolution_clock::now(); cout<<"var1: "<<chrono::duration_cast<chrono::nanoseconds>(e-s).count()/1000.0<<" us"<<endl; }
    { auto h=build({1,2,3,4,5}); auto s=chrono::high_resolution_clock::now(); auto r=Solution_v2().reverseList(h); auto e=chrono::high_resolution_clock::now(); cout<<"var2: "<<chrono::duration_cast<chrono::nanoseconds>(e-s).count()/1000.0<<" us"<<endl; }
    return 0;
}
// var1 mem = {} and time = {}
// var2 mem = {} and time = {}
''')

write(f"{BASE}/06_linked_list/0021_merge_two_sorted_lists.py", '''"""
LeetCode 21: Merge Two Sorted Lists - Easy
"""
import time, tracemalloc
class ListNode:
    def __init__(self, val=0, next=None): self.val = val; self.next = next
def build(arr):
    dummy = ListNode(0); cur = dummy
    for v in arr: cur.next = ListNode(v); cur = cur.next
    return dummy.next
def to_list(node):
    res = []
    while node: res.append(node.val); node = node.next
    return res

# ============= Variation 1: Iterative =============
# Time: O(n+m)   Space: O(1)
class Solution_v1:
    def mergeTwoLists(self, l1, l2):
        dummy = ListNode(0); cur = dummy
        while l1 and l2:
            if l1.val <= l2.val: cur.next = l1; l1 = l1.next
            else: cur.next = l2; l2 = l2.next
            cur = cur.next
        cur.next = l1 or l2
        return dummy.next

# ============= Variation 2: Recursive =============
# Time: O(n+m)   Space: O(n+m)
class Solution_v2:
    def mergeTwoLists(self, l1, l2):
        if not l1: return l2
        if not l2: return l1
        if l1.val <= l2.val: l1.next = self.mergeTwoLists(l1.next, l2); return l1
        else: l2.next = self.mergeTwoLists(l1, l2.next); return l2

if __name__ == "__main__":
    for i, (Sol, name) in enumerate(zip([Solution_v1, Solution_v2], ["Iterative", "Recursive"]), 1):
        tracemalloc.start(); t0 = time.perf_counter()
        result = to_list(Sol().mergeTwoLists(build([1,2,4]), build([1,3,4])))
        t1 = time.perf_counter(); mem = tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{i} ({name}): result={result}, mem = {mem} bytes, time = {(t1-t0)*1e6:.2f} us")
# var1 mem = {} and time = {}
# var2 mem = {} and time = {}
''')

write(f"{BASE}/06_linked_list/0021_merge_two_sorted_lists.cpp", '''/* LeetCode 21: Merge Two Sorted Lists - Easy */
#include <bits/stdc++.h>
#include <chrono>
using namespace std;
struct ListNode { int val; ListNode* next; ListNode(int x):val(x),next(nullptr){} };
class Solution_v1 {
public:
    ListNode* mergeTwoLists(ListNode* l1, ListNode* l2) {
        ListNode d(0); auto c=&d;
        while(l1&&l2){ if(l1->val<=l2->val){c->next=l1;l1=l1->next;} else{c->next=l2;l2=l2->next;} c=c->next; }
        c->next=l1?l1:l2; return d.next;
    }
};
int main(){
    auto build=[](vector<int> v){ ListNode* d=new ListNode(0); auto c=d; for(int x:v){c->next=new ListNode(x);c=c->next;} return d->next; };
    auto l1=build({1,2,4}), l2=build({1,3,4});
    auto s=chrono::high_resolution_clock::now(); auto r=Solution_v1().mergeTwoLists(l1,l2); auto e=chrono::high_resolution_clock::now();
    cout<<"var1: "<<chrono::duration_cast<chrono::nanoseconds>(e-s).count()/1000.0<<" us"<<endl;
    return 0;
}
// var1 mem = {} and time = {}
''')

write(f"{BASE}/06_linked_list/0143_reorder_list.py", '''"""
LeetCode 143: Reorder List - Medium
"""
import time, tracemalloc
class ListNode:
    def __init__(self, val=0, next=None): self.val = val; self.next = next
def build(arr):
    dummy = ListNode(0); cur = dummy
    for v in arr: cur.next = ListNode(v); cur = cur.next
    return dummy.next
def to_list(node):
    res = []
    while node: res.append(node.val); node = node.next
    return res

# ============= Variation 1: Array =============
# Time: O(n)   Space: O(n)
class Solution_v1:
    def reorderList(self, head):
        if not head: return
        nodes = []
        cur = head
        while cur: nodes.append(cur); cur = cur.next
        l, r = 0, len(nodes) - 1
        while l < r:
            nodes[l].next = nodes[r]; l += 1
            if l == r: break
            nodes[r].next = nodes[l]; r -= 1
        nodes[l].next = None

# ============= Variation 2: Find Mid + Reverse + Merge =============
# Time: O(n)   Space: O(1)
class Solution_v2:
    def reorderList(self, head):
        if not head or not head.next: return
        slow = fast = head
        while fast.next and fast.next.next: slow = slow.next; fast = fast.next
        prev, cur = None, slow.next; slow.next = None
        while cur: nxt = cur.next; cur.next = prev; prev = cur; cur = nxt
        first, second = head, prev
        while second:
            t1, t2 = first.next, second.next
            first.next = second; second.next = t1
            first, second = t1, t2

if __name__ == "__main__":
    for i, (Sol, name) in enumerate(zip([Solution_v1, Solution_v2], ["Array", "In-Place"]), 1):
        tracemalloc.start(); t0 = time.perf_counter()
        h = build([1,2,3,4,5]); Sol().reorderList(h); result = to_list(h)
        t1 = time.perf_counter(); mem = tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{i} ({name}): result={result}, mem = {mem} bytes, time = {(t1-t0)*1e6:.2f} us")
# var1 mem = {} and time = {}
# var2 mem = {} and time = {}
''')

write(f"{BASE}/06_linked_list/0143_reorder_list.cpp", '''/* LeetCode 143: Reorder List - Medium */
#include <bits/stdc++.h>
#include <chrono>
using namespace std;
struct ListNode { int val; ListNode* next; ListNode(int x):val(x),next(nullptr){} };
class Solution_v1 {
public:
    void reorderList(ListNode* head) {
        if(!head||!head->next) return;
        auto slow=head, fast=head;
        while(fast->next&&fast->next->next){slow=slow->next;fast=fast->next;}
        ListNode *prev=nullptr, *cur=slow->next; slow->next=nullptr;
        while(cur){auto n=cur->next;cur->next=prev;prev=cur;cur=n;}
        auto f=head, s=prev;
        while(s){auto t1=f->next,t2=s->next;f->next=s;s->next=t1;f=t1;s=t2;}
    }
};
int main(){
    auto build=[](vector<int> v){ ListNode* d=new ListNode(0); auto c=d; for(int x:v){c->next=new ListNode(x);c=c->next;} return d->next; };
    auto h=build({1,2,3,4,5});
    auto s=chrono::high_resolution_clock::now(); Solution_v1().reorderList(h); auto e=chrono::high_resolution_clock::now();
    cout<<"var1: "<<chrono::duration_cast<chrono::nanoseconds>(e-s).count()/1000.0<<" us"<<endl;
    return 0;
}
// var1 mem = {} and time = {}
''')

write(f"{BASE}/06_linked_list/0019_remove_nth_node_from_end_of_list.py", '''"""
LeetCode 19: Remove Nth Node From End of List - Medium
"""
import time, tracemalloc
class ListNode:
    def __init__(self, val=0, next=None): self.val = val; self.next = next
def build(arr):
    dummy = ListNode(0); cur = dummy
    for v in arr: cur.next = ListNode(v); cur = cur.next
    return dummy.next
def to_list(node):
    res = []
    while node: res.append(node.val); node = node.next
    return res

# ============= Variation 1: Two Pass =============
# Time: O(n)   Space: O(1)
class Solution_v1:
    def removeNthFromEnd(self, head, n):
        length = 0; cur = head
        while cur: length += 1; cur = cur.next
        if length == n: return head.next
        cur = head
        for _ in range(length - n - 1): cur = cur.next
        cur.next = cur.next.next
        return head

# ============= Variation 2: One Pass (Two Pointers) =============
# Time: O(n)   Space: O(1)
class Solution_v2:
    def removeNthFromEnd(self, head, n):
        dummy = ListNode(0, head); fast = slow = dummy
        for _ in range(n + 1): fast = fast.next
        while fast: fast = fast.next; slow = slow.next
        slow.next = slow.next.next
        return dummy.next

if __name__ == "__main__":
    for i, (Sol, name) in enumerate(zip([Solution_v1, Solution_v2], ["Two Pass", "One Pass"]), 1):
        tracemalloc.start(); t0 = time.perf_counter()
        result = to_list(Sol().removeNthFromEnd(build([1,2,3,4,5]), 2))
        t1 = time.perf_counter(); mem = tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{i} ({name}): result={result}, mem = {mem} bytes, time = {(t1-t0)*1e6:.2f} us")
# var1 mem = {} and time = {}
# var2 mem = {} and time = {}
''')

write(f"{BASE}/06_linked_list/0019_remove_nth_node_from_end_of_list.cpp", '''/* LeetCode 19: Remove Nth Node From End - Medium */
#include <bits/stdc++.h>
#include <chrono>
using namespace std;
struct ListNode { int val; ListNode* next; ListNode(int x):val(x),next(nullptr){} };
class Solution_v1 {
public:
    ListNode* removeNthFromEnd(ListNode* head, int n) {
        ListNode d(0); d.next=head; auto fast=&d, slow=&d;
        for(int i=0;i<=n;i++) fast=fast->next;
        while(fast){fast=fast->next;slow=slow->next;}
        slow->next=slow->next->next;
        return d.next;
    }
};
int main(){
    auto build=[](vector<int> v){ ListNode* d=new ListNode(0); auto c=d; for(int x:v){c->next=new ListNode(x);c=c->next;} return d->next; };
    auto h=build({1,2,3,4,5});
    auto s=chrono::high_resolution_clock::now(); auto r=Solution_v1().removeNthFromEnd(h,2); auto e=chrono::high_resolution_clock::now();
    cout<<"var1: "<<chrono::duration_cast<chrono::nanoseconds>(e-s).count()/1000.0<<" us"<<endl;
    return 0;
}
// var1 mem = {} and time = {}
''')

write(f"{BASE}/06_linked_list/0138_copy_list_with_random_pointer.py", '''"""
LeetCode 138: Copy List with Random Pointer - Medium
"""
import time, tracemalloc
class Node:
    def __init__(self, x, next=None, random=None):
        self.val = x; self.next = next; self.random = random

# ============= Variation 1: HashMap =============
# Time: O(n)   Space: O(n)
class Solution_v1:
    def copyRandomList(self, head):
        if not head: return None
        old_to_new = {}
        cur = head
        while cur: old_to_new[cur] = Node(cur.val); cur = cur.next
        cur = head
        while cur:
            old_to_new[cur].next = old_to_new.get(cur.next)
            old_to_new[cur].random = old_to_new.get(cur.random)
            cur = cur.next
        return old_to_new[head]

# ============= Variation 2: Interleaving =============
# Time: O(n)   Space: O(1)
class Solution_v2:
    def copyRandomList(self, head):
        if not head: return None
        cur = head
        while cur:
            new_node = Node(cur.val, cur.next); cur.next = new_node; cur = new_node.next
        cur = head
        while cur:
            if cur.random: cur.next.random = cur.random.next
            cur = cur.next.next
        old, new_head = head, head.next
        cur_new = new_head
        while old:
            old.next = old.next.next
            cur_new.next = cur_new.next.next if cur_new.next else None
            old = old.next; cur_new = cur_new.next
        return new_head

if __name__ == "__main__":
    n1 = Node(7); n2 = Node(13); n3 = Node(11)
    n1.next = n2; n2.next = n3; n2.random = n1; n3.random = n1
    for i, (Sol, name) in enumerate(zip([Solution_v1, Solution_v2], ["HashMap", "Interleave"]), 1):
        tracemalloc.start(); t0 = time.perf_counter()
        n1c = Node(7); n2c = Node(13); n3c = Node(11)
        n1c.next = n2c; n2c.next = n3c; n2c.random = n1c; n3c.random = n1c
        result = Sol().copyRandomList(n1c)
        t1 = time.perf_counter(); mem = tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{i} ({name}): mem = {mem} bytes, time = {(t1-t0)*1e6:.2f} us")
# var1 mem = {} and time = {}
# var2 mem = {} and time = {}
''')

write(f"{BASE}/06_linked_list/0138_copy_list_with_random_pointer.cpp", '''/* LeetCode 138: Copy List with Random Pointer - Medium */
#include <bits/stdc++.h>
#include <chrono>
using namespace std;
struct Node { int val; Node* next; Node* random; Node(int x):val(x),next(nullptr),random(nullptr){} };
class Solution_v1 {
public:
    Node* copyRandomList(Node* head) {
        if(!head) return nullptr;
        unordered_map<Node*,Node*> mp;
        auto cur=head; while(cur){mp[cur]=new Node(cur->val);cur=cur->next;}
        cur=head; while(cur){mp[cur]->next=mp[cur->next];mp[cur]->random=mp[cur->random];cur=cur->next;}
        return mp[head];
    }
};
int main(){
    auto n1=new Node(7), n2=new Node(13), n3=new Node(11);
    n1->next=n2; n2->next=n3; n2->random=n1; n3->random=n1;
    auto s=chrono::high_resolution_clock::now(); auto r=Solution_v1().copyRandomList(n1); auto e=chrono::high_resolution_clock::now();
    cout<<"var1: "<<chrono::duration_cast<chrono::nanoseconds>(e-s).count()/1000.0<<" us"<<endl;
    return 0;
}
// var1 mem = {} and time = {}
''')

write(f"{BASE}/06_linked_list/0002_add_two_numbers.py", '''"""
LeetCode 2: Add Two Numbers - Medium
"""
import time, tracemalloc
class ListNode:
    def __init__(self, val=0, next=None): self.val = val; self.next = next
def build(arr):
    dummy = ListNode(0); cur = dummy
    for v in arr: cur.next = ListNode(v); cur = cur.next
    return dummy.next
def to_list(node):
    res = []
    while node: res.append(node.val); node = node.next
    return res

# ============= Variation 1: Iterative =============
# Time: O(max(m,n))   Space: O(max(m,n))
class Solution_v1:
    def addTwoNumbers(self, l1, l2):
        dummy = ListNode(0); cur = dummy; carry = 0
        while l1 or l2 or carry:
            v1 = l1.val if l1 else 0
            v2 = l2.val if l2 else 0
            s = v1 + v2 + carry
            carry = s // 10
            cur.next = ListNode(s % 10); cur = cur.next
            if l1: l1 = l1.next
            if l2: l2 = l2.next
        return dummy.next

if __name__ == "__main__":
    tracemalloc.start(); t0 = time.perf_counter()
    result = to_list(Solution_v1().addTwoNumbers(build([2,4,3]), build([5,6,4])))
    t1 = time.perf_counter(); mem = tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
    print(f"var1: result={result}, mem = {mem} bytes, time = {(t1-t0)*1e6:.2f} us")
# var1 mem = {} and time = {}
''')

write(f"{BASE}/06_linked_list/0002_add_two_numbers.cpp", '''/* LeetCode 2: Add Two Numbers - Medium */
#include <bits/stdc++.h>
#include <chrono>
using namespace std;
struct ListNode { int val; ListNode* next; ListNode(int x):val(x),next(nullptr){} };
class Solution_v1 {
public:
    ListNode* addTwoNumbers(ListNode* l1, ListNode* l2) {
        ListNode d(0); auto c=&d; int carry=0;
        while(l1||l2||carry){
            int s=(l1?l1->val:0)+(l2?l2->val:0)+carry;
            carry=s/10; c->next=new ListNode(s%10); c=c->next;
            if(l1) l1=l1->next; if(l2) l2=l2->next;
        }
        return d.next;
    }
};
int main(){
    auto build=[](vector<int> v){ ListNode* d=new ListNode(0); auto c=d; for(int x:v){c->next=new ListNode(x);c=c->next;} return d->next; };
    auto s=chrono::high_resolution_clock::now(); auto r=Solution_v1().addTwoNumbers(build({2,4,3}),build({5,6,4})); auto e=chrono::high_resolution_clock::now();
    cout<<"var1: "<<chrono::duration_cast<chrono::nanoseconds>(e-s).count()/1000.0<<" us"<<endl;
    return 0;
}
// var1 mem = {} and time = {}
''')

write(f"{BASE}/06_linked_list/0141_linked_list_cycle.py", '''"""
LeetCode 141: Linked List Cycle - Easy
"""
import time, tracemalloc
class ListNode:
    def __init__(self, val=0, next=None): self.val = val; self.next = next

# ============= Variation 1: HashSet =============
# Time: O(n)   Space: O(n)
class Solution_v1:
    def hasCycle(self, head):
        seen = set()
        while head:
            if id(head) in seen: return True
            seen.add(id(head)); head = head.next
        return False

# ============= Variation 2: Fast & Slow Pointers =============
# Time: O(n)   Space: O(1)
class Solution_v2:
    def hasCycle(self, head):
        slow = fast = head
        while fast and fast.next:
            slow = slow.next; fast = fast.next.next
            if slow == fast: return True
        return False

if __name__ == "__main__":
    n1 = ListNode(3); n2 = ListNode(2); n3 = ListNode(0); n4 = ListNode(-4)
    n1.next = n2; n2.next = n3; n3.next = n4; n4.next = n2
    for i, (Sol, name) in enumerate(zip([Solution_v1, Solution_v2], ["HashSet", "Floyd"]), 1):
        tracemalloc.start(); t0 = time.perf_counter()
        result = Sol().hasCycle(n1)
        t1 = time.perf_counter(); mem = tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{i} ({name}): result={result}, mem = {mem} bytes, time = {(t1-t0)*1e6:.2f} us")
# var1 mem = {} and time = {}
# var2 mem = {} and time = {}
''')

write(f"{BASE}/06_linked_list/0141_linked_list_cycle.cpp", '''/* LeetCode 141: Linked List Cycle - Easy */
#include <bits/stdc++.h>
#include <chrono>
using namespace std;
struct ListNode { int val; ListNode* next; ListNode(int x):val(x),next(nullptr){} };
class Solution_v1 {
public:
    bool hasCycle(ListNode* head) {
        auto slow=head, fast=head;
        while(fast&&fast->next){ slow=slow->next; fast=fast->next->next; if(slow==fast) return true; }
        return false;
    }
};
int main(){
    auto n1=new ListNode(3), n2=new ListNode(2), n3=new ListNode(0), n4=new ListNode(-4);
    n1->next=n2; n2->next=n3; n3->next=n4; n4->next=n2;
    auto s=chrono::high_resolution_clock::now(); bool r=Solution_v1().hasCycle(n1); auto e=chrono::high_resolution_clock::now();
    cout<<"var1 (Floyd): "<<r<<", "<<chrono::duration_cast<chrono::nanoseconds>(e-s).count()/1000.0<<" us"<<endl;
    return 0;
}
// var1 mem = {} and time = {}
''')

write(f"{BASE}/06_linked_list/0287_find_the_duplicate_number.py", '''"""
LeetCode 287: Find the Duplicate Number - Medium
"""
import time, tracemalloc
from typing import List

# ============= Variation 1: Sorting =============
# Time: O(n log n)   Space: O(1)
class Solution_v1:
    def findDuplicate(self, nums: List[int]) -> int:
        nums.sort()
        for i in range(1, len(nums)):
            if nums[i] == nums[i-1]: return nums[i]

# ============= Variation 2: Floyd's Cycle Detection =============
# Time: O(n)   Space: O(1)
class Solution_v2:
    def findDuplicate(self, nums: List[int]) -> int:
        slow = fast = 0
        while True:
            slow = nums[slow]; fast = nums[nums[fast]]
            if slow == fast: break
        slow2 = 0
        while slow != slow2:
            slow = nums[slow]; slow2 = nums[slow2]
        return slow

if __name__ == "__main__":
    nums = [1, 3, 4, 2, 2]
    for i, (Sol, name) in enumerate(zip([Solution_v1, Solution_v2], ["Sorting", "Floyd"]), 1):
        tracemalloc.start(); t0 = time.perf_counter()
        result = Sol().findDuplicate(nums[:])
        t1 = time.perf_counter(); mem = tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{i} ({name}): result={result}, mem = {mem} bytes, time = {(t1-t0)*1e6:.2f} us")
# var1 mem = {} and time = {}
# var2 mem = {} and time = {}
''')

write(f"{BASE}/06_linked_list/0287_find_the_duplicate_number.cpp", '''/* LeetCode 287: Find the Duplicate Number - Medium */
#include <bits/stdc++.h>
#include <chrono>
using namespace std;
class Solution_v1 {
public:
    int findDuplicate(vector<int>& nums) {
        int slow=0, fast=0;
        do{ slow=nums[slow]; fast=nums[nums[fast]]; } while(slow!=fast);
        int slow2=0;
        while(slow!=slow2){ slow=nums[slow]; slow2=nums[slow2]; }
        return slow;
    }
};
int main(){
    vector<int> nums={1,3,4,2,2};
    auto s=chrono::high_resolution_clock::now(); int r=Solution_v1().findDuplicate(nums); auto e=chrono::high_resolution_clock::now();
    cout<<"var1 (Floyd): "<<r<<", "<<chrono::duration_cast<chrono::nanoseconds>(e-s).count()/1000.0<<" us"<<endl;
    return 0;
}
// var1 mem = {} and time = {}
''')

write(f"{BASE}/06_linked_list/0146_lru_cache.py", '''"""
LeetCode 146: LRU Cache - Medium
"""
import time, tracemalloc
from collections import OrderedDict

# ============= Variation 1: OrderedDict =============
# Time: O(1) all ops   Space: O(capacity)
class LRUCache_v1:
    def __init__(self, capacity: int):
        self.cache = OrderedDict(); self.cap = capacity
    def get(self, key: int) -> int:
        if key not in self.cache: return -1
        self.cache.move_to_end(key); return self.cache[key]
    def put(self, key: int, value: int) -> None:
        if key in self.cache: self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.cap: self.cache.popitem(last=False)

# ============= Variation 2: Doubly Linked List + HashMap =============
# Time: O(1) all ops   Space: O(capacity)
class DNode:
    def __init__(self, k=0, v=0): self.key=k; self.val=v; self.prev=None; self.next=None
class LRUCache_v2:
    def __init__(self, capacity: int):
        self.cap = capacity; self.cache = {}
        self.head, self.tail = DNode(), DNode()
        self.head.next = self.tail; self.tail.prev = self.head
    def _remove(self, node):
        node.prev.next = node.next; node.next.prev = node.prev
    def _add(self, node):
        node.prev = self.tail.prev; node.next = self.tail
        self.tail.prev.next = node; self.tail.prev = node
    def get(self, key):
        if key not in self.cache: return -1
        node = self.cache[key]; self._remove(node); self._add(node); return node.val
    def put(self, key, value):
        if key in self.cache: self._remove(self.cache[key])
        node = DNode(key, value); self._add(node); self.cache[key] = node
        if len(self.cache) > self.cap:
            lru = self.head.next; self._remove(lru); del self.cache[lru.key]

if __name__ == "__main__":
    for i, (Cls, name) in enumerate(zip([LRUCache_v1, LRUCache_v2], ["OrderedDict", "DLL+Map"]), 1):
        tracemalloc.start(); t0 = time.perf_counter()
        c = Cls(2); c.put(1,1); c.put(2,2); r1=c.get(1); c.put(3,3); r2=c.get(2); c.put(4,4); r3=c.get(1); r4=c.get(3); r5=c.get(4)
        t1 = time.perf_counter(); mem = tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{i} ({name}): gets={r1},{r2},{r3},{r4},{r5}, mem = {mem} bytes, time = {(t1-t0)*1e6:.2f} us")
# var1 mem = {} and time = {}
# var2 mem = {} and time = {}
''')

write(f"{BASE}/06_linked_list/0146_lru_cache.cpp", '''/* LeetCode 146: LRU Cache - Medium */
#include <bits/stdc++.h>
#include <chrono>
using namespace std;
class LRUCache {
    int cap; list<pair<int,int>> dl; unordered_map<int,list<pair<int,int>>::iterator> mp;
public:
    LRUCache(int capacity):cap(capacity){}
    int get(int key){
        if(!mp.count(key)) return -1;
        dl.splice(dl.end(),dl,mp[key]); return mp[key]->second;
    }
    void put(int key, int value){
        if(mp.count(key)){mp[key]->second=value;dl.splice(dl.end(),dl,mp[key]);return;}
        if((int)dl.size()==cap){auto f=dl.front();mp.erase(f.first);dl.pop_front();}
        dl.push_back({key,value}); mp[key]=prev(dl.end());
    }
};
int main(){
    auto s=chrono::high_resolution_clock::now();
    LRUCache c(2); c.put(1,1); c.put(2,2); cout<<c.get(1)<<" "; c.put(3,3); cout<<c.get(2)<<" ";
    auto e=chrono::high_resolution_clock::now();
    cout<<chrono::duration_cast<chrono::nanoseconds>(e-s).count()/1000.0<<" us"<<endl;
    return 0;
}
// var1 mem = {} and time = {}
''')

write(f"{BASE}/06_linked_list/0023_merge_k_sorted_lists.py", '''"""
LeetCode 23: Merge k Sorted Lists - Hard
"""
import time, tracemalloc, heapq
from typing import List
class ListNode:
    def __init__(self, val=0, next=None): self.val = val; self.next = next
def build(arr):
    dummy = ListNode(0); cur = dummy
    for v in arr: cur.next = ListNode(v); cur = cur.next
    return dummy.next
def to_list(node):
    res = []
    while node: res.append(node.val); node = node.next
    return res

# ============= Variation 1: Merge All + Sort =============
# Time: O(N log N)   Space: O(N)
class Solution_v1:
    def mergeKLists(self, lists):
        vals = []
        for l in lists:
            while l: vals.append(l.val); l = l.next
        dummy = ListNode(0); cur = dummy
        for v in sorted(vals): cur.next = ListNode(v); cur = cur.next
        return dummy.next

# ============= Variation 2: Min Heap =============
# Time: O(N log k)   Space: O(k)
class Solution_v2:
    def mergeKLists(self, lists):
        heap = []; dummy = ListNode(0); cur = dummy
        for i, l in enumerate(lists):
            if l: heapq.heappush(heap, (l.val, i, l))
        while heap:
            val, i, node = heapq.heappop(heap)
            cur.next = node; cur = cur.next
            if node.next: heapq.heappush(heap, (node.next.val, i, node.next))
        return dummy.next

# ============= Variation 3: Divide and Conquer =============
# Time: O(N log k)   Space: O(log k)
class Solution_v3:
    def mergeKLists(self, lists):
        if not lists: return None
        def merge2(l1, l2):
            d = ListNode(0); c = d
            while l1 and l2:
                if l1.val <= l2.val: c.next = l1; l1 = l1.next
                else: c.next = l2; l2 = l2.next
                c = c.next
            c.next = l1 or l2; return d.next
        while len(lists) > 1:
            merged = []
            for i in range(0, len(lists), 2):
                l1 = lists[i]; l2 = lists[i+1] if i+1 < len(lists) else None
                merged.append(merge2(l1, l2))
            lists = merged
        return lists[0]

if __name__ == "__main__":
    for i, (Sol, name) in enumerate(zip([Solution_v1, Solution_v2, Solution_v3], ["Sort", "Heap", "D&C"]), 1):
        tracemalloc.start(); t0 = time.perf_counter()
        lists = [build([1,4,5]), build([1,3,4]), build([2,6])]
        result = to_list(Sol().mergeKLists(lists))
        t1 = time.perf_counter(); mem = tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{i} ({name}): result={result}, mem = {mem} bytes, time = {(t1-t0)*1e6:.2f} us")
# var1 mem = {} and time = {}
# var2 mem = {} and time = {}
# var3 mem = {} and time = {}
''')

write(f"{BASE}/06_linked_list/0023_merge_k_sorted_lists.cpp", '''/* LeetCode 23: Merge k Sorted Lists - Hard */
#include <bits/stdc++.h>
#include <chrono>
using namespace std;
struct ListNode { int val; ListNode* next; ListNode(int x):val(x),next(nullptr){} };
class Solution_v1 {
public:
    ListNode* mergeKLists(vector<ListNode*>& lists) {
        auto cmp=[](ListNode* a, ListNode* b){return a->val>b->val;};
        priority_queue<ListNode*,vector<ListNode*>,decltype(cmp)> pq(cmp);
        for(auto l:lists) if(l) pq.push(l);
        ListNode d(0); auto c=&d;
        while(!pq.empty()){ auto n=pq.top(); pq.pop(); c->next=n; c=c->next; if(n->next) pq.push(n->next); }
        return d.next;
    }
};
int main(){
    auto build=[](vector<int> v){ ListNode* d=new ListNode(0); auto c=d; for(int x:v){c->next=new ListNode(x);c=c->next;} return d->next; };
    vector<ListNode*> lists={build({1,4,5}),build({1,3,4}),build({2,6})};
    auto s=chrono::high_resolution_clock::now(); auto r=Solution_v1().mergeKLists(lists); auto e=chrono::high_resolution_clock::now();
    cout<<"var1 (Heap): "<<chrono::duration_cast<chrono::nanoseconds>(e-s).count()/1000.0<<" us"<<endl;
    return 0;
}
// var1 mem = {} and time = {}
''')

write(f"{BASE}/06_linked_list/0025_reverse_nodes_in_k_group.py", '''"""
LeetCode 25: Reverse Nodes in k-Group - Hard
"""
import time, tracemalloc
class ListNode:
    def __init__(self, val=0, next=None): self.val = val; self.next = next
def build(arr):
    dummy = ListNode(0); cur = dummy
    for v in arr: cur.next = ListNode(v); cur = cur.next
    return dummy.next
def to_list(node):
    res = []
    while node: res.append(node.val); node = node.next
    return res

# ============= Variation 1: Iterative =============
# Time: O(n)   Space: O(1)
class Solution_v1:
    def reverseKGroup(self, head, k):
        dummy = ListNode(0, head); group_prev = dummy
        while True:
            kth = group_prev
            for _ in range(k):
                kth = kth.next
                if not kth: return dummy.next
            group_next = kth.next
            prev, cur = kth.next, group_prev.next
            while cur != group_next:
                nxt = cur.next; cur.next = prev; prev = cur; cur = nxt
            tmp = group_prev.next; group_prev.next = kth; group_prev = tmp
        return dummy.next

if __name__ == "__main__":
    tracemalloc.start(); t0 = time.perf_counter()
    result = to_list(Solution_v1().reverseKGroup(build([1,2,3,4,5]), 2))
    t1 = time.perf_counter(); mem = tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
    print(f"var1: result={result}, mem = {mem} bytes, time = {(t1-t0)*1e6:.2f} us")
# var1 mem = {} and time = {}
''')

write(f"{BASE}/06_linked_list/0025_reverse_nodes_in_k_group.cpp", '''/* LeetCode 25: Reverse Nodes in k-Group - Hard */
#include <bits/stdc++.h>
#include <chrono>
using namespace std;
struct ListNode { int val; ListNode* next; ListNode(int x):val(x),next(nullptr){} };
class Solution_v1 {
public:
    ListNode* reverseKGroup(ListNode* head, int k) {
        ListNode d(0); d.next=head; auto gp=&d;
        while(true){
            auto kth=gp;
            for(int i=0;i<k;i++){kth=kth->next;if(!kth) return d.next;}
            auto gn=kth->next; auto prev=gn; auto cur=gp->next;
            while(cur!=gn){auto n=cur->next;cur->next=prev;prev=cur;cur=n;}
            auto tmp=gp->next; gp->next=kth; gp=tmp;
        }
    }
};
int main(){
    auto build=[](vector<int> v){ ListNode* d=new ListNode(0); auto c=d; for(int x:v){c->next=new ListNode(x);c=c->next;} return d->next; };
    auto h=build({1,2,3,4,5});
    auto s=chrono::high_resolution_clock::now(); auto r=Solution_v1().reverseKGroup(h,2); auto e=chrono::high_resolution_clock::now();
    cout<<"var1: "<<chrono::duration_cast<chrono::nanoseconds>(e-s).count()/1000.0<<" us"<<endl;
    return 0;
}
// var1 mem = {} and time = {}
''')

print("Section 6 (Linked List) generated! 11 problems x 2 = 22 files")
