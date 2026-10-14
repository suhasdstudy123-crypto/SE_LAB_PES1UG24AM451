# Lab 5 – Reflection

**1. Which issues were the easiest to fix, and which were the hardest? Why?**

The Flake8 issues (E231, E225, E261, E305) were the easiest: each one names the exact line and column, and the fix is a single space or blank line. Renaming to snake_case and adding docstrings was also mechanical, just repetitive. The hardest were the security issues. Replacing `pickle` meant checking that every value in `events` could be stored as JSON, and replacing `os.system` meant rewriting the call so the event name is passed as an argument instead of being joined into a shell string. The mutable default argument was the most important one: Pylint only says "dangerous default value", and I had to run the program to see the real effect, which was guests of one event filling up another event.

**2. Did the static analysis tools report any false positives? If so, describe one example.**

Yes, partly. Bandit B311 flags `random.choice` as unsuitable for cryptography, but a lucky draw is not cryptography. I still switched to `secrets.choice` because it costs nothing and makes the draw unpredictable. After the fix, Bandit also reports B404 (importing `subprocess`) and B603 (`subprocess` call) as Low. These warn about *any* use of subprocess, even when there is no shell and the arguments are a fixed list, so I reviewed them and marked them with `# nosec`. Pylint's C0103 naming and missing-docstring messages are style preferences rather than bugs. In the other direction, no tool caught the real behaviour bug by itself: Pylint flagged the mutable default, but only running the code showed that "Alumni Dinner is full" was wrong.

**3. How would you integrate static analysis tools into your actual software development workflow?**

- Run Flake8 and Pylint in the editor (VS Code extensions) so problems show up while typing.
- Add a `pre-commit` hook that runs `flake8`, `pylint --fail-under=9.5` and `bandit -r .` so bad code cannot be committed.
- Add a GitHub Actions job that runs the same three tools on every push and pull request and fails the build on any Bandit Medium/High issue.
- Keep a shared config (`.pylintrc`, `.flake8`, `pyproject.toml`) so the whole team uses the same rules, and only use `# nosec` / `# pylint: disable` with a comment explaining why.

**4. What tangible improvements did you observe in the code quality, readability, or potential robustness after applying the fixes?**

- **Correctness:** each event now has its own guest list. Meena is registered and Alumni Dinner shows 1 seat left instead of "full". `guest_report` actually uses its sort argument.
- **Security:** no shell command injection, no code execution from a tampered save file, and an unpredictable lucky draw. Bandit went from 4 issues to 0.
- **Readability:** PEP 8 names, docstrings on every function, and no extra `else` nesting. Pylint went from 4.64 to 10.00 and Flake8 is clean.
- **Robustness / reuse:** the `if __name__ == "__main__":` guard means the module can be imported or tested without running the demo, and the save file is now human-readable JSON with explicit UTF-8 encoding.
