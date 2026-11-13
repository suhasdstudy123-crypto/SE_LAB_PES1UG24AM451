# Lab 6 – Code and Branch Coverage Analysis

**Name:** Suhas D  **SRN:** PES1UG24AM451
**Assigned scenario:** L6_L7_58 – Restaurant Bill (`restaurant_bill.py`)

## Files

| File | Description |
|------|-------------|
| `restaurant_bill.py` | Application under test (unchanged from the assigned repo) |
| `test_restaurant_bill.py` | Original starter test file (2 tests) |
| `CodeCoverageTest_PES1UG24AM451_restaurant_bill.py` | Tests written to reach ≥ 90% line (code) coverage |
| `BranchCoverageTest_PES1UG24AM451_restaurant_bill.py` | Tests written to reach ≥ 90% branch coverage |
| `screenshots/` | Terminal output of the coverage runs |

## Commands

```bash
pip install coverage pytest

# line (code) coverage
coverage run -m pytest CodeCoverageTest_PES1UG24AM451_restaurant_bill.py
coverage report -m

# branch coverage
coverage run --branch -m pytest BranchCoverageTest_PES1UG24AM451_restaurant_bill.py
coverage report -m
```

## Results

| Run | Tests | Line coverage | Branch coverage |
|-----|-------|---------------|-----------------|
| Starter `test_restaurant_bill.py` | 2 | 16 of 33 lines missed | 7 partial branches, 44% combined |
| `CodeCoverageTest_…` | 13 | **100%** (33/33) | – |
| `BranchCoverageTest_…` | 24 | **100%** (33/33) | **100%** (22/22, 0 partial) |

Screenshots:
- `screenshots/01_initial_starter_test_branch_coverage.png`: baseline with the starter tests
- `screenshots/02_code_coverage_after.png`: line coverage after the new tests (100%)
- `screenshots/03_branch_coverage_after.png`: branch coverage after the new tests (100%)

## Analysis

**Starter tests.** Only two tests existed (`bill_total` for dine-in and an even `split_bill`).
None of the error checks, the happy-hour discount, the large-party charge, the
round-up in `split_bill` or any of `table_wait` was executed (missing lines 6, 8, 10, 13, 20, 22, 26, 31-39).

**Code coverage tests.** One test per unexecuted statement was added:
invalid section, invalid order, happy hour + large party (rooftop), uneven split,
invalid people, negative tip and one test per `return` in `table_wait`.
That executes all 33 statements (100% line coverage).

**Branch coverage tests.** Line coverage does not check that each decision went both ways.
For example, `is_happy_hour and section != "takeaway"` must also be tested with
happy hour on takeaway (discount *not* applied). The branch test file
tests every decision with both True and False outcomes, plus the boundary values:

| Function | Decision | True case | False case |
|----------|----------|-----------|------------|
| `bill_total` | `section not in SERVICE_CHARGE` | `"patio"` | `"dine_in"` |
| | `food_total < 0 or guests < 1` | food = -1 / guests = 0 | food = 0, guests = 1 |
| | `is_happy_hour and section != "takeaway"` | dine_in + happy hour | takeaway + happy hour, rooftop no happy hour |
| | `guests >= 8` | 8 guests | 7 guests |
| `split_bill` | `people < 1` | 0 people | 1 person |
| | `tip_percent < 0` | -1 | 0 |
| | `grand_total % people != 0` | 1000/3 | 1100/4 |
| `table_wait` | `party_size > 12` | 13 | 12 |
| | `has_reservation` | True | False |
| | `free_tables == 0` | 0 | > 0 |
| | `party_size > 6 and free_tables < 2` | (8, 1) | (8, 2), (6, 1) |

Result: 22/22 branches covered, 0 partial branches, so **100% branch coverage**.
