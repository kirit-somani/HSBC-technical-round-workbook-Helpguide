# HSBC technical interview workbook (source)

A 17-module study workbook (Python, DSA, SQL, DBMS, OS, networks, resume questions, mock round, HR).

## Just read it
Open `dist/hsbc-technical-workbook.html` in any browser (Chrome, Edge, Firefox, Safari).
Works offline. Fonts load from Google Fonts when online and fall back to system fonts otherwise.
Your "Mark as done" ticks are saved in that browser on that computer.

## Rebuild it (after editing)
Requires Python 3.9+ (no other packages).

    python run_tests.py     # runs every Python solution, every SQL query, and the OS examples
    python build.py         # rebuilds dist/hsbc-technical-workbook.html

## Folder layout
- parts/*.html      the lessons, exercises and Q&A (edit these; files are joined in name order)
- snippets_*.py     tested Python solutions shown on the page (a "#@@ name" line starts a snippet,
                    "#@@ test name" holds its hidden test)
- snippets.sql      the SQL schema and query solutions ("--@@ name" starts a snippet)
- template.html     page design (CSS) and the progress-tracking script
- build.py          fills the template and injects the code snippets with syntax colouring
- run_tests.py      the test runner

In a part file, write [[py:name]] or [[sql:name]] to insert a snippet.
Exercises use <try id="..." title="..." level="Easy" must="1"> ... <solution> ... </try>.
