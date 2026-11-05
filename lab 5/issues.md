# Lab 5: Identified Issues — `library_catalog_system.py`

Baseline: Pylint **5.32/10**, Bandit **5 issues** (2 High, 1 Medium, 2 Low), Flake8 **6 issues**.
Final: Pylint **10.00/10**, Bandit **0**, Flake8 **0**. Reports are in `reports/before/` and `reports/after/`.

Line numbers refer to the original file.

## High and medium severity

| # | Issue | Type | Tool / Code | Line(s) | Description | Fix Approach |
|---|-------|------|-------------|---------|-------------|--------------|
| 1 | Shell command injection | Security (High) | Bandit B605 | 58 | `os.system("echo ... " + filename)` runs a shell command built from a string. A filename like `x; rm -rf ~` would run arbitrary commands. | Removed the shell call and used `print()` to show the message. |
| 2 | Weak MD5 hash | Security (High) | Bandit B324 | 47 | MD5 is broken for security use. Patron hashes could be collided or brute-forced. | Replaced with `hashlib.sha256`. |
| 3 | Use of `eval()` | Security (Medium) | Bandit B307, Pylint W0123 | 40–43 | `calculate_fine` ran `eval(calc_expr)`, so any caller-supplied string would run as Python code. | Changed the signature to `calculate_fine(days_overdue, rate_per_day=2.0)` and compute `days_overdue * rate_per_day`. |
| 4 | Hardcoded secret printed to console | Security (Medium) | Manual review (Bandit B105 missed it because of the variable name) | 62, 70 | `librarian_key = "MASTER_LIB_ACCESS_TOKEN_2026"` was stored in source and printed in full. | Read the key from the `LIBRARIAN_KEY` environment variable and print only whether it is configured. |
| 5 | Mutable default argument | Bug | Pylint W0102 | 15 | `active_issues=[]` is created once and shared by every call, so logs leak between calls. | Default changed to `None`, with a new list created inside the function. |
| 6 | Bare `except` / try-except-pass | Bug | Bandit B110, Flake8 E722, Pylint W0702 | 24–27 | `return_book` swallowed every error, including typos and `KeyboardInterrupt`, and gave no sign of failure. | Removed the try/except. The function looks the book up with `.get()` and returns `False` for unknown IDs. |
| 7 | Return inflates stock (logic bug) | Bug | Manual (found by running the program) | 23–25, 64 | `return_book("B02")` raised B02 to 2 copies when the library owns 1. No tool flags this. | Added a `total` field to each book. `return_book` refuses a return when `copies >= total`. |
| 8 | File not closed safely, no encoding | Bug | Pylint R1732, W1514 | 55–57 | `open()`/`close()` leaks the file handle if `write` raises, and the encoding depends on the platform. | Used `with open(..., encoding="utf-8")`. |

## Low severity / style

| # | Issue | Type | Tool / Code | Line(s) | Description | Fix Approach |
|---|-------|------|-------------|---------|-------------|--------------|
| 9 | Insecure random for PIN | Security (Low) | Bandit B311 | 51 | `random` is predictable and not meant for PINs. | Used `1000 + secrets.randbelow(9000)`. |
| 10 | Unused import `csv` | Style | Flake8 F401, Pylint W0611 | 6 | Imported but never used. The export wrote `str(dict)` instead of CSV. | Rewrote `export_catalog` with `csv.writer` so the export is real CSV. |
| 11 | Unused variables | Style | Flake8 F841, Pylint W0612 | 31, 41 | `late_fee` and `days` were assigned but never used. | Removed them. |
| 12 | Comparison to `None` with `==` | Style | Flake8 E711, Pylint C0121 | 32 | Should use an identity check. | Changed to `is None`. |
| 13 | Non-snake_case function name | Convention | Pylint C0103 | 15 | `issueBook` breaks the PEP 8 naming convention. | Renamed to `issue_book` and updated the caller. |
| 14 | Old-style `%` formatting | Convention | Pylint C0209 | 19 | Could be an f-string. | Converted to an f-string. |
| 15 | Redundant if/else returning bool | Refactor | Pylint R1703, R1705 | 34–37 | `if x: return True else: return False`. | Simplified to `return book is not None and book["copies"] > 0`. |
| 16 | Missing docstrings | Convention | Pylint C0116 | 15, 23, 30, 40, 46, 50, 54, 61 | Functions had no docstrings. | Added a docstring to every function. |
| 17 | No final newline | Style | Flake8 W292, Pylint C0304 | 73 | File did not end with a newline. | Added the trailing newline. |
| 18 | `main()` runs on import | Design | Manual | 73 | Importing the module ran the demo and wrote a file. | Wrapped the call in `if __name__ == "__main__":`. |
