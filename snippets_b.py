#@@ oop_bank
from abc import ABC, abstractmethod

class Account(ABC):                            # abstract: cannot be created directly
    bank_name = "Demo Bank"                    # class variable: shared by all accounts

    def __init__(self, owner, balance=0):
        self.owner = owner                     # instance variables: one copy per object
        self._balance = balance                # leading underscore: "internal, don't touch"

    @property
    def balance(self):                         # read-only access from outside
        return self._balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("amount must be positive")
        self._balance += amount

    def withdraw(self, amount):
        if amount > self._balance + self.overdraft_limit():
            raise ValueError("insufficient funds")
        self._balance -= amount

    @abstractmethod
    def overdraft_limit(self):                 # every subclass MUST implement this
        ...

    def describe(self):
        return f"{type(self).__name__} of {self.owner}: {self._balance}"


class SavingsAccount(Account):
    def overdraft_limit(self):                 # overriding
        return 0


class CurrentAccount(Account):
    def overdraft_limit(self):
        return 1000

    def describe(self):                        # overriding + reusing the parent's version
        return super().describe() + " (overdraft allowed)"
#@@ test oop_bank
s = SavingsAccount("Asha", 500)
c = CurrentAccount("Ravi", 500)
try:
    s.withdraw(600); assert False
except ValueError:
    pass
c.withdraw(1200)
assert c.balance == -700
s.deposit(100)
assert s.balance == 600
try:
    Account("x"); assert False
except TypeError:
    pass
assert Account.bank_name == "Demo Bank"
assert [a.describe() for a in (s, c)] == [
    "SavingsAccount of Asha: 600",
    "CurrentAccount of Ravi: -700 (overdraft allowed)",
]

#@@ oop_misc
class Calculator:
    def add(self, *args):                      # Python's version of "overloading"
        return sum(args)

Calculator().add(1, 2)          # 3
Calculator().add(1, 2, 3)       # 6


class Employee:
    company = "Demo Bank"
    count = 0

    def __init__(self, name):
        self.name = name
        Employee.count += 1

    @classmethod
    def from_string(cls, text):                # gets the class, used as an alternative constructor
        return cls(text.split("-")[0])

    @staticmethod
    def is_valid_name(name):                   # gets neither self nor cls
        return name.isalpha()
#@@ test oop_misc
assert Calculator().add(1, 2, 3) == 6
e = Employee.from_string("Asha-Engineering")
assert e.name == "Asha" and Employee.count == 1 and Employee.is_valid_name("Asha")

#@@ os_lock
import threading

counter = 0
lock = threading.Lock()

def work():
    global counter
    for _ in range(100_000):
        with lock:                             # only one thread inside at a time
            counter += 1

threads = [threading.Thread(target=work) for _ in range(4)]
for t in threads:
    t.start()
for t in threads:
    t.join()

print(counter)                                 # always 400000 with the lock
#@@ test os_lock
assert counter == 400000

#@@ mock_first_unique
from collections import Counter

def first_unique_index(s):
    counts = Counter(s)
    for i, ch in enumerate(s):
        if counts[ch] == 1:
            return i
    return -1
#@@ test mock_first_unique
assert first_unique_index("leetcode") == 0 and first_unique_index("loveleetcode") == 2
assert first_unique_index("aabb") == -1

#@@ mock_totals
from collections import defaultdict

def totals_by_account(transactions):
    totals = defaultdict(int)
    for account, amount in transactions:
        totals[account] += amount
    # biggest total first; ties broken by account name
    return sorted(totals.items(), key=lambda kv: (-kv[1], kv[0]))
#@@ test mock_totals
tx = [("B", 50), ("A", 100), ("B", 70), ("C", 130), ("A", 20)]
assert totals_by_account(tx) == [("C", 130), ("A", 120), ("B", 120)]
assert totals_by_account([("X", 5), ("Y", 9)]) == [("Y", 9), ("X", 5)]

#@@ mock_logged_in
def still_logged_in(events):
    online = set()
    for user, action in events:
        if action == "login":
            online.add(user)
        elif action == "logout":
            online.discard(user)          # discard: no error if not present
    return sorted(online)
#@@ test mock_logged_in
ev = [("ravi", "login"), ("asha", "login"), ("ravi", "logout"), ("meena", "login"), ("zed", "logout")]
assert still_logged_in(ev) == ["asha", "meena"]

#@@ karat_skeleton
def solve(data):
    # 1. Clarify: what are the inputs, sizes, and edge cases?
    # 2. Brute force first, say its complexity out loud.
    # 3. Improve it (hashmap? sort? two pointers?).
    # 4. Code it in small, named steps.
    # 5. Test with one normal case and one edge case by hand.
    ...
#@@ test karat_skeleton
assert solve(None) is None

#@@ sql_runner
import sqlite3

conn = sqlite3.connect(":memory:")
with open("schema.sql") as f:                 # the schema above, saved as schema.sql
    conn.executescript(f.read())

query = """
SELECT name, salary
FROM employees
ORDER BY salary DESC
LIMIT 3
"""
for row in conn.execute(query):
    print(row)
#@@ test sql_runner
assert True

#@@ sql_injection
name = "x' OR '1'='1"                    # what an attacker might type

# UNSAFE: the input becomes part of the SQL text
unsafe = "SELECT name FROM employees WHERE name = '" + name + "'"
print(conn.execute(unsafe).fetchall())   # returns EVERY employee

# SAFE: the ? placeholder keeps the input as plain data, never as SQL
safe = "SELECT name FROM employees WHERE name = ?"
print(conn.execute(safe, (name,)).fetchall())   # returns nothing
#@@ test sql_injection : sql_runner
assert len(conn.execute(unsafe).fetchall()) == 8
assert conn.execute(safe, (name,)).fetchall() == []
