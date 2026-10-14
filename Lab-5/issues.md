# Lab 5 – Issue Table (`event_manager.py`)

Line numbers refer to the **original** file (`reports/before/`). Ordered by severity (High → Low).

| # | Issue | Tool / Code | Type | Severity | Line(s) | Description | Fix Approach |
|---|-------|-------------|------|----------|---------|-------------|--------------|
| 1 | Shell command injection | Bandit B605 | Security | High | 56 | `os.system("lp badges_" + eventName + ".txt")` runs through a shell. An event name such as `x; rm -rf ~` would run extra commands. | Replaced with `subprocess.run(["lp", badge_file], check=False)`: arguments passed as a list, no shell. Spaces in the name are replaced with `_`. |
| 2 | Unsafe deserialization with pickle | Bandit B301 (+ B403 import) | Security | Medium (B403 Low) | 2, 51 | `pickle.load` can execute arbitrary code if `events.pkl` is tampered with. | Save/load with `json` instead (data is only strings, ints and lists). Files opened with `encoding="utf-8"`; file renamed to `events.json`. |
| 3 | Mutable default argument | Pylint W0102 | Bug | High (logic) | 9 | `guests=[]` is created once and shared by every event. Guests of *Tech Meetup* also appear in *Alumni Dinner*, so the demo printed "Alumni Dinner is full, cannot add Meena" and 0 seats left. | Default changed to `guests=None`; a new list is created inside the function (`list(guests)` also copies a caller's list). Output now shows 1 seat left and Meena is registered. |
| 4 | Unused argument | Pylint W0613 | Bug | Medium | 39 | `sortOrder` was accepted but ignored, so callers could not choose the order. | `guest_report` now honours `sort_order`: `"name"` sorts alphabetically, anything else keeps registration order. |
| 5 | Weak random generator | Bandit B311 | Security | Low | 72 | `random.choice` is predictable; a lucky draw should not be guessable. | Use `secrets.choice`. |
| 6 | Non-snake_case names | Pylint C0103 | Convention | Low | 9–54 | `createEvent`, `eventName`, `fileName` etc. break PEP 8 naming. | Renamed to `create_event`, `event_name`, `file_name`, … |
| 7 | Missing docstrings | Pylint C0114 / C0116 | Documentation | Low | 1, 9–59 | No module or function docstrings. | Added a module docstring and a docstring to every function. |
| 8 | Unnecessary `else` after `return` | Pylint R1705 | Refactor | Low | 33 | `else:` branch after `return` adds nesting. | Removed the `else` and de-indented the return. |
| 9 | Missing whitespace after `,` | Flake8 E231 | Style | Low | 61 | `"Rooftop",2` | `"Rooftop", 2` |
| 10 | Missing whitespace around operator | Flake8 E225 | Style | Low | 66 | `left=seatsLeft(...)` | `left = seats_left(...)` |
| 11 | Inline comment spacing | Flake8 E261 | Style | Low | 75 | Only one space before `#`. | Two spaces before inline comment. |
| 12 | Blank lines after function | Flake8 E305 | Style | Low | 79 | Only one blank line before the top-level `main()` call. | Two blank lines; call wrapped in `if __name__ == "__main__":` so importing the module does not run the demo. |

## Results

| Tool | Before | After |
|------|--------|-------|
| Pylint | 4.64 / 10 (30 messages) | **10.00 / 10** |
| Bandit | 4 issues (1 High, 1 Medium, 2 Low) | **0 issues** |
| Flake8 | 4 issues | **0 issues** (empty report) |

Bandit note: `subprocess` is still used for printing badges, but only with a fixed argument list and no shell. The remaining informational checks (B404 import, B603/B607 partial path) were reviewed and marked with `# nosec` on those lines.
