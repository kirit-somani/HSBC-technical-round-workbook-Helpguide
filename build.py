import re, glob, html, sys, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
from run_tests import parse

esc = lambda t: html.escape(t, quote=False)

PY_RE = re.compile(
    r'''(#[^\n]*)|("""[\s\S]*?"""|f?"(?:\\.|[^"\\\n])*"|f?'(?:\\.|[^'\\\n])*')'''
    r'''|\b(\d[\d_]*(?:\.\d+)?)\b'''
    r'''|\b(def|class|return|if|elif|else|for|while|in|not|and|or|is|None|True|False|import|from|as|raise|try|except|finally|with|lambda|pass|break|continue|global|assert|del|yield)\b'''
    r'''|(@\w+)'''
    r'''|\b(self|cls|print|len|range|min|max|sum|sorted|enumerate|zip|list|dict|set|tuple|str|int|float|isinstance|super|type|IndexError|ValueError|TypeError)\b''')
PY_CLS = ["c", "s", "n", "k", "d", "b"]

SQL_KW = ("SELECT|FROM|WHERE|GROUP BY|ORDER BY|HAVING|LIMIT|OFFSET|JOIN|LEFT|INNER|ON|AS|AND|OR|NOT|IN|IS|NULL|DISTINCT|"
          "CREATE|TABLE|INSERT|INTO|VALUES|PRIMARY|KEY|INTEGER|TEXT|DESC|ASC|OVER|PARTITION BY|BETWEEN|LIKE|UNION|EXISTS|CASE|WHEN|THEN|ELSE|END|UPDATE|SET|BEGIN|COMMIT|ROLLBACK|INDEX|DELETE|TRUNCATE|DROP|ALTER|ADD")
SQL_RE = re.compile(
    r"(--[^\n]*)|('(?:[^']|'')*')|\b(\d+)\b|\b(" + SQL_KW + r")\b|\b(COUNT|MAX|MIN|AVG|SUM|COALESCE|RANK|DENSE_RANK|ROW_NUMBER)\b",
    re.I)
SQL_CLS = ["c", "s", "n", "k", "b"]

def highlight(text, rx, classes):
    out, last = [], 0
    for m in rx.finditer(text):
        out.append(esc(text[last:m.start()]))
        cls = next(classes[i - 1] for i in range(1, len(m.groups()) + 1) if m.group(i) is not None)
        out.append(f'<span class="{cls}">{esc(m.group(0))}</span>')
        last = m.end()
    out.append(esc(text[last:]))
    return "".join(out)

py = {}
for f in ("snippets_a.py", "snippets_b.py", "snippets_c.py"):
    py.update(parse(f, "#@@ "))
sql = parse("snippets.sql", "--@@ ")

def code_block(kind, name):
    if kind == "py":
        if name not in py: sys.exit("missing py snippet " + name)
        body = highlight(py[name], PY_RE, PY_CLS)
    else:
        if name not in sql: sys.exit("missing sql snippet " + name)
        body = highlight(sql[name], SQL_RE, SQL_CLS)
    return f'<pre class="code"><code>{body}</code></pre>'

parts = "\n".join(open(p, encoding="utf-8").read() for p in sorted(glob.glob("parts/*.html")))
parts = re.sub(r"\[\[(py|sql):([\w]+)\]\]", lambda m: code_block(m.group(1), m.group(2)), parts)

def try_repl(m):
    attrs = m.group(1)
    tid = re.search(r'id="([^"]+)"', attrs).group(1)
    title = re.search(r'title="([^"]+)"', attrs).group(1)
    badge = '<span class="badge">Priority</span>' if 'must="1"' in attrs else ""
    lv = re.search(r'level="([^"]+)"', attrs)
    if lv:
        badge = f'<span class="badge level">{lv.group(1)}</span>' + badge
    return (f'<div class="try" id="try-{tid}"><div class="try-head"><h3>Try it: {title}</h3>{badge}</div>'
            f'<div class="try-body">{m.group(2)}</div>'
            f'<details class="solution"><summary>Show solution and explanation</summary><div class="sol-body">{m.group(3)}</div></details>'
            f'<label class="done"><input type="checkbox" data-done="{tid}"><span>Mark as done</span></label></div>')
parts = re.sub(r"<try ([^>]*)>(.*?)<solution>(.*?)</try>", try_repl, parts, flags=re.S)

parts = re.sub(r'<qa q="([^"]*)">(.*?)</qa>',
               lambda m: f'<details class="qa"><summary>{m.group(1)}</summary><div>{m.group(2)}</div></details>', parts, flags=re.S)
def qaset_repl(m):
    attrs = m.group(1)
    qid = re.search(r'id="([^"]+)"', attrs).group(1)
    title = re.search(r'title="([^"]+)"', attrs).group(1)
    return (f'<div class="qaset"><h3>{title}</h3><p class="qa-hint">Say each answer out loud in about 30 seconds, then open it and compare.</p>'
            f'{m.group(2)}<label class="done"><input type="checkbox" data-done="{qid}"><span>I have gone through all of these</span></label></div>')
parts = re.sub(r"<qaset ([^>]*)>(.*?)</qaset>", qaset_repl, parts, flags=re.S)

parts = re.sub(r'<tip(?: title="([^"]*)")?>(.*?)</tip>',
               lambda m: '<aside class="tip">' + (f'<p class="tip-title">{m.group(1)}</p>' if m.group(1) else "") + m.group(2) + "</aside>",
               parts, flags=re.S)
parts = re.sub(r"<table>(.*?)</table>", r'<div class="tablewrap"><table>\1</table></div>', parts, flags=re.S)

mods = []
def mod_repl(m):
    mid, day, time, title = m.groups()
    mods.append((mid, day, title))
    num = len(mods)
    return (f'<section class="module" id="{mid}" data-day="{day}"><header class="mod-head"><p class="mod-meta">'
            f'<span class="day-chip">Day {day}</span><span>Module {num}, about {time}</span></p><h2>{title}</h2></header>')
parts = re.sub(r'<mod id="([^"]+)" day="(\d)" time="([^"]+)" title="([^"]+)">', mod_repl, parts)
parts = parts.replace("</mod>", "</section>")
num_of = {mid: i + 1 for i, (mid, _, _) in enumerate(mods)}
parts = re.sub(r"\{n:(\w+)\}", lambda m: str(num_of[m.group(1)]), parts)

day_names = {"1": "Day 1: coding and OOP", "2": "Day 2: DSA, SQL, DBMS, OS", "3": "Day 3: networks, resume, mock, HR"}
side = ['<h2>Start here</h2><ul><li><a href="#top"><span>The 3-day plan</span></a></li></ul>']
for d in ("1", "2", "3"):
    side.append(f"<h2>{day_names[d]}</h2><ul>")
    for mid, day, title in mods:
        if day == d:
            side.append(f'<li data-mod="{mid}"><a href="#{mid}"><span>{num_of[mid]}. {title}</span><span class="count"></span></a></li>')
    side.append("</ul>")

tpl = open("template.html", encoding="utf-8").read()
out = tpl.replace("{{SIDEBAR}}", "\n".join(side)).replace("{{CONTENT}}", parts)
os.makedirs("dist", exist_ok=True)
open("dist/hsbc-technical-workbook.html", "w", encoding="utf-8").write(out)
open("dist/index.html", "w", encoding="utf-8").write(out)
print("Built dist/hsbc-technical-workbook.html & dist/index.html:", len(out) // 1024, "KB,", len(mods), "modules")
