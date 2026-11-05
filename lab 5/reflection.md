# Lab 5: Reflection

**1. Which issues were the easiest to fix, and which were the hardest? Why?**

The easiest were the Flake8 style issues and the simple Pylint warnings: the missing final newline, `== None` changed to `is None`, the unused variables and import, the missing docstrings, and renaming `issueBook` to `issue_book`. Each one is a single-line change that can't break behaviour, and the tool message explains the fix.

The hardest were the issues where the fix changes how the code works. Removing `eval()` meant redesigning `calculate_fine`: it used to accept any expression string, so I had to choose a safer interface (a numeric `rate_per_day`) and update the caller. The `return_book` problem was harder still. Bandit and Pylint only complained about the bare `except: pass`, but running the program showed a real logic bug: returning a book that was never issued raised its copy count above the library's stock. No tool flags that, so I had to understand what the function was meant to do and add a `total` field to enforce the limit.

**2. Did the static analysis tools report any false positives? If so, describe one example.**

Not strict false positives, but some findings depend on context. Bandit B311 (insecure `random`) only matters because the value is a PIN. If `random` had been used to shuffle a reading list, the warning would be noise and could be suppressed with `# nosec`. Similarly, most of the Pylint docstring warnings (C0116) cost points but don't change correctness.

The opposite case was more interesting: a false negative. Bandit did not flag the hardcoded `librarian_key` token, because its B105 check matches variable names like `password` or `secret`. I only caught it by reading the code, which shows that a clean report doesn't guarantee secure code.

**3. How would you integrate static analysis tools into your actual software development workflow?**

- **Locally:** run Flake8 and Pylint in the editor so problems show up while typing, and add a `pre-commit` hook that runs Flake8, Pylint and Bandit before every commit.
- **In CI:** add a GitHub Actions job that runs all three tools on every push and pull request. The build fails on any Bandit Medium/High finding, any Flake8 error, or a Pylint score below a set threshold (for example 9.5).
- **Shared configuration:** keep the rules in `.pylintrc`, `setup.cfg`/`.flake8` and `pyproject.toml` so everyone uses the same rules. Allow justified suppressions (`# nosec`, `# pylint: disable=...`) only with a comment explaining why.
- Use Bandit's severity levels to decide what blocks a merge and what can be logged as tech debt.

**4. What tangible improvements did you observe in code quality, readability, or potential robustness after applying the fixes?**

- **Measured:** Pylint went from 5.32/10 to 10.00/10, Bandit from 5 issues (2 High) to 0, and Flake8 from 6 issues to 0.
- **Security:** the program no longer runs arbitrary code (`eval`) or shell commands (`os.system`), uses SHA-256 and `secrets`, and no longer stores or prints a hardcoded access token.
- **Robustness:** the copy count can't go above stock, returns of unknown books return `False` instead of failing silently, issue logs no longer leak between calls through the mutable default, and the export file is always closed and written as valid UTF-8 CSV.
- **Readability:** every function has a docstring, names follow PEP 8, and `check_availability` is now one clear expression. The module can also be imported (for example, by tests) without running the demo, thanks to the `__main__` guard.
