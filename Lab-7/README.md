# Lab 7 – Fuzzing for Input Validation Bugs

**Name:** Suhas D  **SRN:** PES1UG24AM451
**Assigned scenario:** L6_L7_58 – Restaurant Bill (`restaurant_bill_parser.py`)

## Files

| File | Description |
|------|-------------|
| `restaurant_bill_parser.py` | Fixed (hardened) module: all three functions handle any input without crashing |
| `test_restaurant_bill_parser.py` | Completed Hypothesis fuzz tests, one per function |
| `PES1UG24AM451_SUHAS_D_LAB7.pdf` | Screenshots SS1–SS4, bug table and reflection answers |
| `screenshots/` | SS1–SS4 as PNG |

## Run

```bash
pip install hypothesis pytest
python restaurant_bill_parser.py
pytest test_restaurant_bill_parser.py
```

## Bugs found by fuzzing → fix

| Function | Minimal failing input | Bug | Fix |
|----------|----------------------|-----|-----|
| `clean_dish_name` | `None` | AttributeError (`.strip`) | Non-string → `""` |
| `parse_item_prices` | `None` | AttributeError (`.split`) | Non-string → `[]` |
| `parse_item_prices` | `''`, `'250,,320'` | ValueError from `int('')` | Validate each item, skip empty/invalid/negative |
| `split_amount` | `None` | AttributeError (`.split`) | Non-string → `None` |
| `split_amount` | `''` | ValueError: not enough values to unpack | Require exactly one `/` |
| `split_amount` | `'/'` | ValueError from `int('')` | Validate both parts |
| `split_amount` | `'0/0'` | ZeroDivisionError | Reject people = 0 |
| `split_amount` | `'-1/1'` | Negative share returned | Accept only non-negative whole numbers |

Before the fix: **3 failed** (SS2). After the fix: **3 passed** (SS4).
