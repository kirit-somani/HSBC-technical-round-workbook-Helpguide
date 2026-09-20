#@@ dsa_remove_dups
def remove_duplicates(nums):
    if not nums:
        return 0
    write = 1                                   # next slot for a new unique value
    for read in range(1, len(nums)):
        if nums[read] != nums[write - 1]:
            nums[write] = nums[read]
            write += 1
    return write
#@@ test dsa_remove_dups
a = [1, 1, 2, 2, 2, 3]
k = remove_duplicates(a)
assert k == 3 and a[:k] == [1, 2, 3] and remove_duplicates([]) == 0 and remove_duplicates([5]) == 1

#@@ dsa_missing
def missing_number(nums):                       # nums holds 0..n with one value missing
    n = len(nums)
    return n * (n + 1) // 2 - sum(nums)
#@@ test dsa_missing
assert missing_number([3, 0, 1]) == 2 and missing_number([0, 1]) == 2 and missing_number([1]) == 0

#@@ dsa_majority
def majority_element(nums):                     # the value that appears more than n/2 times
    candidate, count = None, 0
    for n in nums:
        if count == 0:
            candidate = n
        count += 1 if n == candidate else -1
    return candidate
#@@ test dsa_majority
assert majority_element([2, 2, 1, 1, 1, 2, 2]) == 2 and majority_element([3]) == 3

#@@ dsa_product
def product_except_self(nums):
    n = len(nums)
    result = [1] * n
    prefix = 1
    for i in range(n):                          # result[i] = product of everything left of i
        result[i] = prefix
        prefix *= nums[i]
    suffix = 1
    for i in range(n - 1, -1, -1):              # multiply in everything right of i
        result[i] *= suffix
        suffix *= nums[i]
    return result
#@@ test dsa_product
assert product_except_self([1, 2, 3, 4]) == [24, 12, 8, 6]
assert product_except_self([2, 0, 3]) == [0, 6, 0]

#@@ dsa_rotate
def rotate(nums, k):                            # rotate right by k, in place
    if not nums:
        return nums
    n = len(nums)
    k %= n

    def reverse(lo, hi):
        while lo < hi:
            nums[lo], nums[hi] = nums[hi], nums[lo]
            lo += 1
            hi -= 1

    reverse(0, n - 1)                           # reverse everything
    reverse(0, k - 1)                           # then the first k
    reverse(k, n - 1)                           # then the rest
    return nums
#@@ test dsa_rotate
assert rotate([1, 2, 3, 4, 5, 6, 7], 3) == [5, 6, 7, 1, 2, 3, 4]
assert rotate([1, 2], 5) == [2, 1] and rotate([1, 2, 3], 0) == [1, 2, 3] and rotate([], 2) == []

#@@ dsa_colors
def sort_colors(nums):                          # values are only 0, 1, 2
    low, mid, high = 0, 0, len(nums) - 1
    while mid <= high:
        if nums[mid] == 0:
            nums[low], nums[mid] = nums[mid], nums[low]
            low += 1
            mid += 1
        elif nums[mid] == 1:
            mid += 1
        else:
            nums[mid], nums[high] = nums[high], nums[mid]
            high -= 1                           # do not advance mid: the swapped value is unchecked
    return nums
#@@ test dsa_colors
assert sort_colors([2, 0, 2, 1, 1, 0]) == [0, 0, 1, 1, 2, 2] and sort_colors([]) == []

#@@ dsa_subarray_sum
from collections import defaultdict

def subarray_sum(nums, k):                      # how many contiguous subarrays add up to k
    counts = defaultdict(int)
    counts[0] = 1                               # the empty prefix
    running = 0
    total = 0
    for n in nums:
        running += n
        total += counts[running - k]            # earlier prefixes that leave exactly k
        counts[running] += 1
    return total
#@@ test dsa_subarray_sum
assert subarray_sum([1, 1, 1], 2) == 2 and subarray_sum([1, 2, 3], 3) == 2
assert subarray_sum([1, -1, 0], 0) == 3

#@@ dsa_three_sum
def three_sum(nums):
    nums.sort()
    result = []
    for i in range(len(nums) - 2):
        if i > 0 and nums[i] == nums[i - 1]:
            continue                            # skip repeated first numbers
        lo, hi = i + 1, len(nums) - 1
        while lo < hi:
            s = nums[i] + nums[lo] + nums[hi]
            if s < 0:
                lo += 1
            elif s > 0:
                hi -= 1
            else:
                result.append([nums[i], nums[lo], nums[hi]])
                lo += 1
                hi -= 1
                while lo < hi and nums[lo] == nums[lo - 1]:
                    lo += 1                     # skip repeated second numbers
    return result
#@@ test dsa_three_sum
assert three_sum([-1, 0, 1, 2, -1, -4]) == [[-1, -1, 2], [-1, 0, 1]]
assert three_sum([0, 0, 0, 0]) == [[0, 0, 0]] and three_sum([1, 2]) == []

#@@ dsa_lcp
def longest_common_prefix(words):
    if not words:
        return ""
    prefix = words[0]
    for w in words[1:]:
        while not w.startswith(prefix):
            prefix = prefix[:-1]                # shrink until it fits
    return prefix
#@@ test dsa_lcp
assert longest_common_prefix(["flower", "flow", "flight"]) == "fl"
assert longest_common_prefix(["dog", "car"]) == "" and longest_common_prefix(["a"]) == "a"

#@@ dsa_string_misc
def reverse_words(s):
    return " ".join(s.split()[::-1])            # split() also drops extra spaces

def is_rotation(a, b):                          # is b a rotation of a?
    return len(a) == len(b) and b in a + a
#@@ test dsa_string_misc
assert reverse_words("  the sky  is blue ") == "blue is sky the"
assert is_rotation("waterbottle", "erbottlewat") and not is_rotation("abc", "acb")

#@@ dsa_bits
def single_number(nums):                        # every value appears twice except one
    result = 0
    for n in nums:
        result ^= n                             # x ^ x = 0, and x ^ 0 = x
    return result

def is_power_of_two(n):
    return n > 0 and (n & (n - 1)) == 0         # a power of two has exactly one 1-bit

def count_set_bits(n):
    count = 0
    while n:
        n &= n - 1                              # clears the lowest 1-bit
        count += 1
    return count
#@@ test dsa_bits
assert single_number([4, 1, 2, 1, 2]) == 4
assert [n for n in range(1, 20) if is_power_of_two(n)] == [1, 2, 4, 8, 16] and not is_power_of_two(0)
assert count_set_bits(13) == 3 and count_set_bits(0) == 0

#@@ dsa_next_greater
def next_greater(nums):
    result = [-1] * len(nums)
    stack = []                                  # indices still waiting for a bigger value
    for i, n in enumerate(nums):
        while stack and nums[stack[-1]] < n:
            result[stack.pop()] = n
        stack.append(i)
    return result
#@@ test dsa_next_greater
assert next_greater([2, 1, 2, 4, 3]) == [4, 2, 4, -1, -1] and next_greater([]) == []

#@@ dsa_ll_more
def remove_nth_from_end(head, n):
    dummy = ListNode(0, head)                   # dummy handles removing the head
    fast = slow = dummy
    for _ in range(n):                          # open a gap of n nodes
        fast = fast.next
    while fast.next:                            # move both until fast is at the last node
        fast = fast.next
        slow = slow.next
    slow.next = slow.next.next                  # slow is just before the target
    return dummy.next

def add_two_numbers(a, b):                      # digits stored in reverse order
    dummy = tail = ListNode()
    carry = 0
    while a or b or carry:
        total = carry + (a.val if a else 0) + (b.val if b else 0)
        carry, digit = divmod(total, 10)
        tail.next = ListNode(digit)
        tail = tail.next
        a = a.next if a else None
        b = b.next if b else None
    return dummy.next
#@@ test dsa_ll_more : listnode
assert to_list(remove_nth_from_end(from_list([1, 2, 3, 4, 5]), 2)) == [1, 2, 3, 5]
assert to_list(remove_nth_from_end(from_list([1, 2]), 2)) == [2]
assert to_list(remove_nth_from_end(from_list([1]), 1)) == []
assert to_list(add_two_numbers(from_list([2, 4, 3]), from_list([5, 6, 4]))) == [7, 0, 8]
assert to_list(add_two_numbers(from_list([9, 9]), from_list([1]))) == [0, 0, 1]

#@@ dsa_rotated
def search_rotated(nums, target):
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return mid
        if nums[lo] <= nums[mid]:               # the left half is sorted
            if nums[lo] <= target < nums[mid]:
                hi = mid - 1
            else:
                lo = mid + 1
        else:                                   # the right half is sorted
            if nums[mid] < target <= nums[hi]:
                lo = mid + 1
            else:
                hi = mid - 1
    return -1
#@@ test dsa_rotated
r = [4, 5, 6, 7, 0, 1, 2]
assert [search_rotated(r, x) for x in r] == list(range(7))
assert search_rotated(r, 3) == -1 and search_rotated([1], 1) == 0 and search_rotated([], 1) == -1
assert search_rotated([3, 1], 1) == 1

#@@ dsa_kth
import heapq

def kth_largest(nums, k):
    heap = []                                   # min-heap holding the k largest seen so far
    for n in nums:
        heapq.heappush(heap, n)
        if len(heap) > k:
            heapq.heappop(heap)                 # drop the smallest of the k+1
    return heap[0]
#@@ test dsa_kth
assert kth_largest([3, 2, 1, 5, 6, 4], 2) == 5 and kth_largest([3, 2, 3, 1, 2, 4, 5, 5, 6], 4) == 4

#@@ dsa_tree_more
def invert_tree(root):
    if root is None:
        return None
    root.left, root.right = invert_tree(root.right), invert_tree(root.left)
    return root

def is_valid_bst(root, low=float("-inf"), high=float("inf")):
    if root is None:
        return True
    if not (low < root.val < high):             # every node must sit inside its allowed range
        return False
    return (is_valid_bst(root.left, low, root.val) and
            is_valid_bst(root.right, root.val, high))

def lowest_common_ancestor(root, p, q):         # for a BST, p and q are values
    while root:
        if p < root.val and q < root.val:
            root = root.left
        elif p > root.val and q > root.val:
            root = root.right
        else:
            return root.val                     # the paths split here
    return None
#@@ test dsa_tree_more : tree
def build(vals):
    r = None
    for v in vals:
        r = bst_insert(r, v)
    return r
t = build([8, 3, 10, 1, 6, 14])
assert is_valid_bst(t)
assert lowest_common_ancestor(t, 1, 6) == 3 and lowest_common_ancestor(t, 1, 14) == 8
assert lowest_common_ancestor(t, 3, 6) == 3
bad = TreeNode(5); bad.left = TreeNode(1); bad.right = TreeNode(4)
bad.right.left = TreeNode(3); bad.right.right = TreeNode(6)
assert not is_valid_bst(bad)
inv = invert_tree(build([8, 3, 10, 1, 6, 14]))
assert inorder(inv) == [14, 10, 8, 6, 3, 1] and invert_tree(None) is None

#@@ dsa_stairs
def climb_stairs(n):                            # ways to climb n steps, taking 1 or 2 at a time
    a, b = 1, 1                                 # ways to reach step 0 and step 1
    for _ in range(n - 1):
        a, b = b, a + b
    return b
#@@ test dsa_stairs
assert [climb_stairs(n) for n in range(1, 7)] == [1, 2, 3, 5, 8, 13]

#@@ dsa_rob
def rob(nums):                                  # max money without robbing two adjacent houses
    take, skip = 0, 0                           # best total if we take / skip the current house
    for n in nums:
        take, skip = skip + n, max(take, skip)
    return max(take, skip)
#@@ test dsa_rob
assert rob([1, 2, 3, 1]) == 4 and rob([2, 7, 9, 3, 1]) == 12 and rob([]) == 0 and rob([5]) == 5

#@@ dsa_coin
def coin_change(coins, amount):
    INF = float("inf")
    dp = [0] + [INF] * amount                   # dp[a] = fewest coins that make amount a
    for a in range(1, amount + 1):
        for c in coins:
            if c <= a and dp[a - c] + 1 < dp[a]:
                dp[a] = dp[a - c] + 1
    return dp[amount] if dp[amount] != INF else -1
#@@ test dsa_coin
assert coin_change([1, 2, 5], 11) == 3 and coin_change([2], 3) == -1 and coin_change([1], 0) == 0
assert coin_change([1, 3, 4], 6) == 2

#@@ dsa_lcs
def lcs(a, b):                                  # length of the longest common subsequence
    dp = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]
    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp[len(a)][len(b)]
#@@ test dsa_lcs
assert lcs("abcde", "ace") == 3 and lcs("abc", "def") == 0 and lcs("", "a") == 0

#@@ dsa_graph
from collections import deque

graph = {"A": ["B", "C"], "B": ["D"], "C": ["D"], "D": []}

def bfs(graph, start):
    seen, order, queue = {start}, [], deque([start])
    while queue:
        node = queue.popleft()
        order.append(node)
        for nxt in graph[node]:
            if nxt not in seen:
                seen.add(nxt)                   # mark when queued, so nothing is queued twice
                queue.append(nxt)
    return order

def dfs(graph, node, seen=None):
    if seen is None:
        seen = set()
    seen.add(node)
    order = [node]
    for nxt in graph[node]:
        if nxt not in seen:
            order += dfs(graph, nxt, seen)
    return order
#@@ test dsa_graph
assert bfs(graph, "A") == ["A", "B", "C", "D"] and dfs(graph, "A") == ["A", "B", "D", "C"]

#@@ dsa_islands
def num_islands(grid):
    if not grid:
        return 0
    rows, cols = len(grid), len(grid[0])

    def sink(r, c):                             # flood-fill: turn a whole island into water
        if r < 0 or c < 0 or r >= rows or c >= cols or grid[r][c] != "1":
            return
        grid[r][c] = "0"
        sink(r + 1, c)
        sink(r - 1, c)
        sink(r, c + 1)
        sink(r, c - 1)

    count = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "1":
                count += 1                      # found a new island
                sink(r, c)
    return count
#@@ test dsa_islands
g = [list(x) for x in ["11000", "11000", "00100", "00011"]]
assert num_islands(g) == 3 and num_islands([]) == 0 and num_islands([["0"]]) == 0
