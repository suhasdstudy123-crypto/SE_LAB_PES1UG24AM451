"""
Lab 6 - Code (line) coverage tests for restaurant_bill.py
SRN : PES1UG24AM451
Name: Suhas D

Goal: execute every statement of restaurant_bill.py at least once.
Run:
    coverage run -m pytest CodeCoverageTest_PES1UG24AM451_restaurant_bill.py
    coverage report -m
"""
import pytest
from restaurant_bill import bill_total, split_bill, table_wait


# ---------------- bill_total ----------------
def test_dine_in_bill():
    # 1000 + 10% service = 1100, + 5% tax = 1155
    assert bill_total("dine_in", 1000, 2, False) == 1155


def test_unknown_section_raises():
    with pytest.raises(ValueError, match="unknown section"):
        bill_total("patio", 1000, 2, False)


def test_negative_food_total_raises():
    with pytest.raises(ValueError, match="invalid order"):
        bill_total("dine_in", -1, 2, False)


def test_happy_hour_large_party_rooftop():
    # happy hour: 1000 -> 800, service 15% = 120, large party +200
    # total = 800 + 320 = 1120, + 5% tax (56) = 1176
    assert bill_total("rooftop", 1000, 8, True) == 1176


# ---------------- split_bill ----------------
def test_even_split():
    assert split_bill(1000, 4, 10) == 275


def test_uneven_split_rounds_up():
    # 1000 / 3 = 333.33 -> each pays 334
    assert split_bill(1000, 3, 0) == 334


def test_split_invalid_people_raises():
    with pytest.raises(ValueError, match="invalid people count"):
        split_bill(1000, 0, 10)


def test_split_negative_tip_raises():
    with pytest.raises(ValueError, match="invalid tip"):
        split_bill(1000, 2, -5)


# ---------------- table_wait ----------------
def test_big_party_call_ahead():
    assert table_wait(13, 5, False) == "call ahead"


def test_reservation_seat_now():
    assert table_wait(4, 0, True) == "seat now"


def test_no_free_tables_waitlist():
    assert table_wait(4, 0, False) == "waitlist"


def test_large_party_one_table_waitlist():
    assert table_wait(8, 1, False) == "waitlist"


def test_small_party_free_table_seat_now():
    assert table_wait(4, 3, False) == "seat now"
