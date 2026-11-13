"""
Lab 7 - Fuzz testing restaurant_bill_parser.py with Hypothesis
SRN : PES1UG24AM451
Name: Suhas D

Each test feeds random text (and None) to one function and fails if the
function raises any exception. The fixed module must also return values of
the expected type.
"""
from hypothesis import given, settings, strategies as st
from restaurant_bill_parser import clean_dish_name, parse_item_prices, split_amount

# Random unicode text, None, and inputs shaped like the real formats
# ("250,180,320" and "1200/4") so the fuzzer also reaches the parsing logic.
price_list_text = st.lists(
    st.one_of(st.integers(), st.text(max_size=5)), max_size=6
).map(lambda xs: ",".join(str(x) for x in xs))
split_text = st.tuples(
    st.one_of(st.integers(), st.text(max_size=4)),
    st.one_of(st.integers(), st.text(max_size=4)),
).map(lambda t: f"{t[0]}/{t[1]}")


@settings(max_examples=300)
@given(st.text() | st.none())
def test_clean_dish_name_no_crash(s):
    try:
        result = clean_dish_name(s)
    except Exception as e:
        assert False, f"clean_dish_name crashed with: {type(e).__name__}: {e}"
    assert isinstance(result, str)
    for marker in "*#~":
        assert marker not in result


@settings(max_examples=300)
@given(st.text() | st.none() | price_list_text)
def test_parse_item_prices_no_crash(s):
    try:
        result = parse_item_prices(s)
    except Exception as e:
        assert False, f"parse_item_prices crashed with: {type(e).__name__}: {e}"
    assert isinstance(result, list)
    assert all(isinstance(p, int) and p >= 0 for p in result)


@settings(max_examples=300)
@given(st.text() | st.none() | split_text)
def test_split_amount_no_crash(s):
    try:
        result = split_amount(s)
    except Exception as e:
        assert False, f"split_amount crashed with: {type(e).__name__}: {e}"
    assert result is None or (isinstance(result, int) and result >= 0)
