# Lab 5: Static Code Analysis – Event Management System

**Student:** Suhas D (PES1UG24AM451)
**Assigned repo:** [SETAPESU26/L5_31_event_manager](https://github.com/SETAPESU26/L5_31_event_manager)
**Tools:** Pylint 4.1.3, Bandit 1.9.4, Flake8 7.4.1 (Python 3.10)

## Files

| File | Contents |
|------|----------|
| `event_manager.py` | Cleaned, fixed version of the program |
| `issues.md` | Issue table (12 issues documented and fixed) |
| `reflection.md` | Answers to the reflection questions |
| `reports/before/` | `pylint_report.txt`, `bandit_report.txt`, `flake8_report.txt`, `program_output.txt` for the original code |
| `reports/after/` | The same reports for the fixed code (`flake8_report.txt` is empty = no issues) |

## Results

| Tool | Before | After |
|------|--------|-------|
| Pylint | 4.64 / 10 | **10.00 / 10** |
| Bandit | 4 issues (1 High, 1 Medium, 2 Low) | **0** |
| Flake8 | 4 issues | **0** |

Bug found by running the program: `guests=[]` was shared by every event, so the Alumni Dinner was reported full before anyone had registered for it. Each event now gets its own list.

## Commits

1. Add original code and baseline reports
2. Fix Bandit security issues (shell injection, pickle, weak random)
3. Fix Flake8 style issues
4. Fix Pylint issues (mutable default, unused argument, naming, docstrings)
5. Add after reports, issue table and reflection

## Reproduce

```
python -m pip install pylint bandit flake8
python event_manager.py
python -m pylint event_manager.py > pylint_report.txt
python -m bandit -r event_manager.py > bandit_report.txt
python -m flake8 event_manager.py > flake8_report.txt
```
