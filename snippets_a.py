#@@ py_toolkit
from collections import Counter, defaultdict, deque
import heapq

nums = [5, 3, 8, 3, 5, 5]

Counter(nums)                    # Counter({5: 3, 3: 2, 8: 1})
Counter(nums).most_common(1)     # [(5, 3)]

groups = defaultdict(list)       # a missing key becomes an empty list
groups["a"].append(1)

q = deque([1, 2, 3])
q.append(4)                      # add on the right, O(1)
q.popleft()                      # remove from the left, O(1)

heap = []
heapq.heappush(heap, 5)          # min-heap
heapq.heappush(heap, 2)
heapq.heappop(heap)              # 2, the smallest

words = ["pear", "fig", "apple"]
sorted(words, key=len)                       # ['fig', 'pear', 'apple']
sorted(words, key=lambda w: (-len(w), w))    # longest first, ties A-Z

for i, w in enumerate(words):    # index and value together
    pass

s = "hello"
s[::-1]                          # 'olleh'
s[1:3]                           # 'el'
nums[-1]                         # last element
#@@ test py_toolkit
assert Counter(nums).most_common(1) == [(5, 3)]
assert sorted(words, key=len) == ["fig", "pear", "apple"]
assert sorted(words, key=lambda w: (-len(w), w)) == ["apple", "pear", "fig"]
assert heap == [5]

#@@ wordfreq
from collections import Counter

def top_two_words(text):
    words = text.lower().split()
    return Counter(words).most_common(2)
#@@ test wordfreq
assert top_two_words("a b A c b a") == [("a", 3), ("b", 2)]

#@@ warmups
def reverse_string(s):
    return s[::-1]

def is_prime(n):
    if n < 2:
        return False
    i = 2
    while i * i <= n:          # only test up to the square root
        if n % i == 0:
            return False
        i += 1
    return True

def fib(n):                    # iterative: O(n) time, O(1) space
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

def fizzbuzz(n):
    out = []
    for i in range(1, n + 1):
        if i % 15 == 0:
            out.append("FizzBuzz")
        elif i % 3 == 0:
            out.append("Fizz")
        elif i % 5 == 0:
            out.append("Buzz")
        else:
            out.append(str(i))
    return out

def count_vowels(s):
    return sum(1 for ch in s.lower() if ch in "aeiou")
#@@ test warmups
assert reverse_string("abc") == "cba"
assert [n for n in range(20) if is_prime(n)] == [2, 3, 5, 7, 11, 13, 17, 19]
assert [fib(i) for i in range(8)] == [0, 1, 1, 2, 3, 5, 8, 13]
assert fizzbuzz(15)[-1] == "FizzBuzz" and fizzbuzz(5) == ["1", "2", "Fizz", "4", "Buzz"]
assert count_vowels("Education") == 5

#@@ fib_memo
from functools import lru_cache

@lru_cache(maxsize=None)
def fib_recursive(n):
    if n < 2:
        return n
    return fib_recursive(n - 1) + fib_recursive(n - 2)
#@@ test fib_memo
assert fib_recursive(30) == 832040

#@@ stack
class Stack:
    def __init__(self):
        self._items = []

    def push(self, x):
        self._items.append(x)

    def pop(self):
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self._items.pop()

    def peek(self):
        if self.is_empty():
            raise IndexError("peek from empty stack")
        return self._items[-1]

    def is_empty(self):
        return len(self._items) == 0

    def size(self):
        return len(self._items)
#@@ test stack
s = Stack(); s.push(1); s.push(2)
assert s.pop() == 2 and s.peek() == 1 and s.size() == 1
s.pop()
try:
    s.pop(); assert False
except IndexError:
    pass

#@@ queue
from collections import deque

class Queue:
    def __init__(self):
        self._items = deque()

    def enqueue(self, x):
        self._items.append(x)

    def dequeue(self):
        if self.is_empty():
            raise IndexError("dequeue from empty queue")
        return self._items.popleft()

    def peek(self):
        if self.is_empty():
            raise IndexError("peek from empty queue")
        return self._items[0]

    def is_empty(self):
        return len(self._items) == 0

    def size(self):
        return len(self._items)
#@@ test queue
q = Queue(); q.enqueue("a"); q.enqueue("b")
assert q.dequeue() == "a" and q.peek() == "b" and q.size() == 1
q.dequeue()
assert q.is_empty()
try:
    q.dequeue(); assert False
except IndexError:
    pass

#@@ valid_parens
def is_valid(s):
    pairs = {")": "(", "]": "[", "}": "{"}
    stack = []
    for ch in s:
        if ch in pairs:                        # a closing bracket
            if not stack or stack.pop() != pairs[ch]:
                return False
        else:                                  # an opening bracket
            stack.append(ch)
    return not stack                           # leftovers mean unclosed
#@@ test valid_parens
assert is_valid("()[]{}") and is_valid("{[()]}") and is_valid("")
assert not is_valid("(]") and not is_valid("(((") and not is_valid("())")

#@@ min_stack
class MinStack:
    def __init__(self):
        self._stack = []          # each entry is (value, minimum so far)

    def push(self, x):
        current_min = min(x, self._stack[-1][1]) if self._stack else x
        self._stack.append((x, current_min))

    def pop(self):
        return self._stack.pop()[0]

    def top(self):
        return self._stack[-1][0]

    def get_min(self):
        return self._stack[-1][1]
#@@ test min_stack
m = MinStack(); m.push(5); m.push(2); m.push(7)
assert m.get_min() == 2
m.pop(); m.pop()
assert m.get_min() == 5 and m.top() == 5

#@@ queue_two_stacks
class QueueWithStacks:
    def __init__(self):
        self._in = []
        self._out = []

    def enqueue(self, x):
        self._in.append(x)

    def dequeue(self):
        if not self._out:                      # refill only when empty
            while self._in:
                self._out.append(self._in.pop())
        if not self._out:
            raise IndexError("dequeue from empty queue")
        return self._out.pop()
#@@ test queue_two_stacks
q = QueueWithStacks()
for x in (1, 2, 3):
    q.enqueue(x)
assert q.dequeue() == 1
q.enqueue(4)
assert [q.dequeue(), q.dequeue(), q.dequeue()] == [2, 3, 4]

#@@ two_sum
def two_sum(nums, target):
    seen = {}                        # value -> index
    for i, n in enumerate(nums):
        need = target - n
        if need in seen:
            return [seen[need], i]
        seen[n] = i
    return []
#@@ test two_sum
assert two_sum([2, 7, 11, 15], 9) == [0, 1]
assert two_sum([3, 3], 6) == [0, 1]
assert two_sum([1, 2], 10) == []

#@@ two_sum_brute
def two_sum_brute(nums, target):
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]
    return []
#@@ test two_sum_brute
assert two_sum_brute([2, 7, 11, 15], 9) == [0, 1]

#@@ hash_basics
from collections import Counter, defaultdict

def is_anagram(a, b):
    return Counter(a) == Counter(b)

def has_duplicate(nums):
    return len(set(nums)) != len(nums)

def group_anagrams(words):
    groups = defaultdict(list)
    for w in words:
        groups["".join(sorted(w))].append(w)
    return list(groups.values())

def top_k_frequent(nums, k):
    return [n for n, _ in Counter(nums).most_common(k)]
#@@ test hash_basics
assert is_anagram("listen", "silent") and not is_anagram("ab", "abb")
assert has_duplicate([1, 2, 1]) and not has_duplicate([1, 2, 3])
g = group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"])
assert sorted(sorted(x) for x in g) == [["ate", "eat", "tea"], ["bat"], ["nat", "tan"]]
assert top_k_frequent([1, 1, 1, 2, 2, 3], 2) == [1, 2]

#@@ palindrome
def is_palindrome(s):
    left, right = 0, len(s) - 1
    while left < right:
        while left < right and not s[left].isalnum():
            left += 1
        while left < right and not s[right].isalnum():
            right -= 1
        if s[left].lower() != s[right].lower():
            return False
        left += 1
        right -= 1
    return True
#@@ test palindrome
assert is_palindrome("A man, a plan, a canal: Panama")
assert not is_palindrome("race a car") and is_palindrome("")

#@@ max_profit
def max_profit(prices):
    lowest = float("inf")
    best = 0
    for p in prices:
        lowest = min(lowest, p)             # cheapest day so far
        best = max(best, p - lowest)        # sell today?
    return best
#@@ test max_profit
assert max_profit([7, 1, 5, 3, 6, 4]) == 5 and max_profit([7, 6, 4, 3, 1]) == 0

#@@ kadane
def max_subarray(nums):
    best = current = nums[0]
    for n in nums[1:]:
        current = max(n, current + n)       # extend, or start fresh at n
        best = max(best, current)
    return best
#@@ test kadane
assert max_subarray([-2, 1, -3, 4, -1, 2, 1, -5, 4]) == 6
assert max_subarray([-3, -1, -2]) == -1

#@@ longest_substring
def length_of_longest_substring(s):
    last_seen = {}
    start = 0                               # left edge of the window
    best = 0
    for i, ch in enumerate(s):
        if ch in last_seen and last_seen[ch] >= start:
            start = last_seen[ch] + 1       # jump past the repeat
        last_seen[ch] = i
        best = max(best, i - start + 1)
    return best
#@@ test longest_substring
assert length_of_longest_substring("abcabcbb") == 3
assert length_of_longest_substring("bbbbb") == 1
assert length_of_longest_substring("pwwkew") == 3 and length_of_longest_substring("") == 0
assert length_of_longest_substring("abba") == 2

#@@ merge_intervals
def merge_intervals(intervals):
    intervals.sort(key=lambda x: x[0])
    merged = []
    for start, end in intervals:
        if merged and start <= merged[-1][1]:       # overlaps the last one
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    return merged
#@@ test merge_intervals
assert merge_intervals([[1, 3], [8, 10], [2, 6], [15, 18]]) == [[1, 6], [8, 10], [15, 18]]
assert merge_intervals([[1, 4], [4, 5]]) == [[1, 5]]

#@@ move_zeroes
def move_zeroes(nums):
    write = 0
    for read in range(len(nums)):
        if nums[read] != 0:
            nums[write], nums[read] = nums[read], nums[write]
            write += 1
    return nums
#@@ test move_zeroes
assert move_zeroes([0, 1, 0, 3, 12]) == [1, 3, 12, 0, 0]

#@@ listnode
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def from_list(values):                 # helper: build a list to test with
    dummy = tail = ListNode()
    for v in values:
        tail.next = ListNode(v)
        tail = tail.next
    return dummy.next

def to_list(head):                     # helper: turn it back into a Python list
    out = []
    while head:
        out.append(head.val)
        head = head.next
    return out
#@@ test listnode
assert to_list(from_list([1, 2, 3])) == [1, 2, 3]

#@@ sll
class SinglyLinkedList:
    def __init__(self):
        self.head = None

    def append(self, val):
        node = ListNode(val)
        if self.head is None:
            self.head = node
            return
        curr = self.head
        while curr.next:
            curr = curr.next
        curr.next = node

    def prepend(self, val):
        self.head = ListNode(val, self.head)

    def delete(self, val):
        if self.head is None:
            return False
        if self.head.val == val:
            self.head = self.head.next
            return True
        curr = self.head
        while curr.next:
            if curr.next.val == val:
                curr.next = curr.next.next
                return True
            curr = curr.next
        return False

    def to_list(self):
        return to_list(self.head)
#@@ test sll : listnode
l = SinglyLinkedList()
l.append(2); l.append(3); l.prepend(1)
assert l.to_list() == [1, 2, 3]
assert l.delete(2) and l.to_list() == [1, 3]
assert l.delete(1) and l.to_list() == [3]
assert not l.delete(99)

#@@ ll_algos
def reverse_list(head):
    prev = None
    curr = head
    while curr:
        nxt = curr.next          # 1. remember the rest
        curr.next = prev         # 2. flip the pointer
        prev = curr              # 3. move prev forward
        curr = nxt               # 4. move curr forward
    return prev

def has_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            return True
    return False

def middle_node(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow

def merge_two_lists(a, b):
    dummy = tail = ListNode()
    while a and b:
        if a.val <= b.val:
            tail.next = a
            a = a.next
        else:
            tail.next = b
            b = b.next
        tail = tail.next
    tail.next = a or b           # attach whichever list still has nodes
    return dummy.next
#@@ test ll_algos : listnode
assert to_list(reverse_list(from_list([1, 2, 3, 4]))) == [4, 3, 2, 1]
assert reverse_list(None) is None
h = from_list([1, 2, 3, 4, 5])
assert middle_node(h).val == 3
assert middle_node(from_list([1, 2, 3, 4])).val == 3
assert not has_cycle(h)
tail = h
while tail.next:
    tail = tail.next
tail.next = h.next
assert has_cycle(h)
assert to_list(merge_two_lists(from_list([1, 3, 5]), from_list([2, 4, 6, 7]))) == [1, 2, 3, 4, 5, 6, 7]

#@@ binary_search
def binary_search(nums, target):
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return mid
        if nums[mid] < target:
            lo = mid + 1                 # target is in the right half
        else:
            hi = mid - 1                 # target is in the left half
    return -1
#@@ test binary_search
a = [1, 3, 5, 7, 9, 11]
assert [binary_search(a, x) for x in a] == [0, 1, 2, 3, 4, 5]
assert binary_search(a, 4) == -1 and binary_search([], 1) == -1

#@@ search_insert
def search_insert(nums, target):
    lo, hi = 0, len(nums)                # hi = len, because we may insert at the end
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] < target:
            lo = mid + 1
        else:
            hi = mid
    return lo
#@@ test search_insert
assert search_insert([1, 3, 5, 6], 5) == 2 and search_insert([1, 3, 5, 6], 2) == 1
assert search_insert([1, 3, 5, 6], 7) == 4 and search_insert([1, 3, 5, 6], 0) == 0

#@@ merge_sort
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    merged = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged
#@@ test merge_sort
import random
for _ in range(50):
    arr = [random.randint(-20, 20) for _ in range(random.randint(0, 30))]
    assert merge_sort(arr) == sorted(arr)

#@@ tree
from collections import deque

class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None

def bst_insert(root, val):
    if root is None:
        return TreeNode(val)
    if val < root.val:
        root.left = bst_insert(root.left, val)
    else:
        root.right = bst_insert(root.right, val)
    return root

def inorder(root):                       # left, node, right -> sorted for a BST
    if root is None:
        return []
    return inorder(root.left) + [root.val] + inorder(root.right)

def height(root):
    if root is None:
        return 0
    return 1 + max(height(root.left), height(root.right))

def level_order(root):                   # breadth-first, one level at a time
    if root is None:
        return []
    result, queue = [], deque([root])
    while queue:
        level = []
        for _ in range(len(queue)):
            node = queue.popleft()
            level.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        result.append(level)
    return result
#@@ test tree
root = None
for v in [8, 3, 10, 1, 6, 14]:
    root = bst_insert(root, v)
assert inorder(root) == [1, 3, 6, 8, 10, 14]
assert height(root) == 3
assert level_order(root) == [[8], [3, 10], [1, 6, 14]]
