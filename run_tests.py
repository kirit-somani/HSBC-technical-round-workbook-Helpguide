import re, sqlite3, sys, os, io, contextlib
os.chdir(os.path.dirname(os.path.abspath(__file__)))
from collections import deque

def parse(path, marker):
    """Return dict name -> text, splitting on lines that start with marker."""
    sections, name, buf = {}, None, []
    for line in open(path, encoding="utf-8").read().split("\n"):
        if line.startswith(marker):
            if name is not None:
                sections[name] = "\n".join(buf).strip("\n")
            name, buf = line[len(marker):].strip(), []
        else:
            buf.append(line)
    if name is not None:
        sections[name] = "\n".join(buf).strip("\n")
    return sections

def load_py():
    s = {}
    for f in ("snippets_a.py", "snippets_b.py", "snippets_c.py"):
        s.update(parse(f, "#@@ "))
    return s

def run_python():
    secs = load_py()
    ok = 0
    sql = parse("snippets.sql", "--@@ ")
    with open("schema.sql", "w") as f:
        f.write(sql["schema"])
    for key in secs:
        if not key.startswith("test "):
            continue
        head = key[5:]
        name, _, deps = head.partition(":")
        name = name.strip()
        ns = {}
        code = ""
        for d in [x.strip() for x in deps.split(",") if x.strip()]:
            code += secs[d] + "\n"
        code += secs[name] + "\n" + secs[key]
        buf = io.StringIO()
        try:
            with contextlib.redirect_stdout(buf):
                exec(compile(code, name, "exec"), ns)
            ok += 1
        except Exception as e:
            print("FAIL", name, repr(e))
            sys.exit(1)
    print(f"python snippets passed: {ok}")

def run_sql():
    sql = parse("snippets.sql", "--@@ ")
    conn = sqlite3.connect(":memory:")
    conn.executescript(sql["schema"])
    expected = {
        "q_above_avg": [("Asha", 90000), ("Rahul", 70000), ("Meera", 95000)],
        "q_second_highest": [(90000,)],
        "q_nth_highest": [(70000,)],
        "q_dense_rank": [(90000,)],
        "q_dup_salary": [(50000, 2), (60000, 2)],
        "q_manager": [("Meera", 95000, "Asha", 90000)],
        "q_never_ordered": [("Bhavna",)],
        "q_dept_max": [("Engineering", "Meera", 95000), ("Finance", "Neha", 60000),
                       ("Finance", "Vikram", 60000), ("Operations", "Karan", 50000),
                       ("Operations", "Sana", 50000)],
        "q_headcount_having": [("Engineering", 3), ("Operations", 3)],
        "q_dept_left": [("Engineering", 3, 255000), ("Operations", 3, 145000),
                        ("Finance", 2, 120000), ("Legal", 0, 0)],
        "q_customer_totals": [("Amit", 800), ("Chirag", 700)],
    }
    for name, exp in expected.items():
        rows = conn.execute(sql[name]).fetchall()
        if sorted(rows) != sorted(exp) if name in ("q_above_avg", "q_dup_salary", "q_headcount_having") else rows != exp:
            print("SQL FAIL", name, rows, exp)
            sys.exit(1)
    rows = conn.execute(sql["q_window_rank"]).fetchall()
    ranks = {r[0]: r[3] for r in rows}
    assert ranks["Meera"] == 1 and ranks["Asha"] == 2 and ranks["Rahul"] == 3
    assert ranks["Karan"] == 1 and ranks["Sana"] == 1 and ranks["Arjun"] == 3   # RANK skips 2 after a tie
    print("sql queries passed:", len(expected) + 1)

def run_os():
    # CPU scheduling: P1=5, P2=3, P3=8, all arrive at 0
    burst = {"P1": 5, "P2": 3, "P3": 8}
    def waiting(order):
        t, w = 0, {}
        for p in order:
            w[p] = t
            t += burst[p]
        return w
    fcfs = waiting(["P1", "P2", "P3"])
    sjf = waiting(sorted(burst, key=burst.get))
    assert fcfs == {"P1": 0, "P2": 5, "P3": 8} and round(sum(fcfs.values()) / 3, 2) == 4.33
    assert sjf == {"P2": 0, "P1": 3, "P3": 8} and round(sum(sjf.values()) / 3, 2) == 3.67
    # Round robin, quantum 4
    rem, t, done, q = dict(burst), 0, {}, deque(["P1", "P2", "P3"])
    timeline = []
    while q:
        p = q.popleft()
        run = min(4, rem[p])
        timeline.append((p, t, t + run))
        t += run
        rem[p] -= run
        if rem[p]:
            q.append(p)
        else:
            done[p] = t
    assert timeline == [("P1", 0, 4), ("P2", 4, 7), ("P3", 7, 11), ("P1", 11, 12), ("P3", 12, 16)]
    wait = {p: done[p] - burst[p] for p in burst}
    assert done == {"P2": 7, "P1": 12, "P3": 16} and wait == {"P1": 7, "P2": 4, "P3": 8}
    assert round(sum(wait.values()) / 3, 2) == 6.33
    # Page replacement, 3 frames
    refs = [7, 0, 1, 2, 0, 3, 0, 4]
    def fifo(refs, n):
        frames, faults = deque(), 0
        for r in refs:
            if r not in frames:
                faults += 1
                if len(frames) == n:
                    frames.popleft()
                frames.append(r)
        return faults
    def lru(refs, n):
        frames, faults = [], 0
        for r in refs:
            if r in frames:
                frames.remove(r)
            else:
                faults += 1
                if len(frames) == n:
                    frames.pop(0)
            frames.append(r)
        return faults
    assert fifo(refs, 3) == 7 and lru(refs, 3) == 6
    print("os examples verified: FCFS 4.33, SJF 3.67, RR 6.33, FIFO 7 faults, LRU 6 faults")

if __name__ == "__main__":
    run_python()
    run_sql()
    run_os()
