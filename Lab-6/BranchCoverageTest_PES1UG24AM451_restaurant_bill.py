"""
Lab 6 - Branch coverage tests for restaurant_bill.py
SRN : PES1UG24AM451
Name: Suhas D

Goal: make every decision (if / elif / compound condition) evaluate to
both True and False at least once, including boundary values.
Run:
    coverage run --branch -m pytest BranchCoverageTest_PES1UG24AM451_restaurant_bill.py
    coverage report -m
"""
import pytest
from restaurant_bill import bill_total, split_bill, table_wait


# ======================= bill_total =======================
# Decision 1: section not in SERVICE_CHARGE  -> True / False
def test_bill_unknown_section_true():
    with pytest.raises(ValueError, match="unknown section"):
        bill_total("patio", 1000, 2, False)


def test_bill_known_section_false():
    # 1000 + 100 service = 1100, + 55 tax = 1155
    assert bill_total("dine_in", 1000, 2, False) == 1155


# Decision 2: food_total < 0 or guests < 1  -> each operand True, both False
def test_bill_negative_food_total():
    with pytest.raises(ValueError, match="invalid order"):
        bill_total("dine_in", -1, 2, False)


def test_bill_zero_guests():
    with pytest.raises(ValueError, match="invalid order"):
        bill_total("dine_in", 1000, 0, False)


def test_bill_zero_food_total_is_valid():
    # boundary: food_total == 0 is allowed
    assert bill_total("dine_in", 0, 1, False) == 0


# Decision 3: is_happy_hour and section != "takeaway"
def test_bill_happy_hour_dine_in_discount_applied():
    # 1000 -> 800, service 80, total 880, tax 44 -> 924
    assert bill_total("dine_in", 1000, 2, True) == 924


def test_bill_happy_hour_takeaway_no_discount():
    # happy hour True but section == takeaway -> no discount
    # 1000, service 0, tax 50 -> 1050
    assert bill_total("takeaway", 1000, 2, True) == 1050


def test_bill_no_happy_hour_rooftop():
    # 1000, service 150, total 1150, tax 57 -> 1207
    assert bill_total("rooftop", 1000, 2, False) == 1207


# Decision 4: guests >= 8  -> True / False with boundary 7 / 8
def test_bill_large_party_boundary_8():
    # 1000 + 100 + 200 = 1300, tax 65 -> 1365
    assert bill_total("dine_in", 1000, 8, False) == 1365


def test_bill_party_of_7_no_large_party_charge():
    assert bill_total("dine_in", 1000, 7, False) == 1155


def test_bill_rooftop_happy_hour_large_party():
    # 800 + 120 + 200 = 1120, tax 56 -> 1176
    assert bill_total("rooftop", 1000, 8, True) == 1176


# ======================= split_bill =======================
# Decision 1: people < 1
def test_split_zero_people():
    with pytest.raises(ValueError, match="invalid people count"):
        split_bill(1000, 0, 10)


def test_split_single_person():
    # boundary people == 1: 1000 + 10% tip = 1100
    assert split_bill(1000, 1, 10) == 1100


# Decision 2: tip_percent < 0
def test_split_negative_tip():
    with pytest.raises(ValueError, match="invalid tip"):
        split_bill(1000, 2, -1)


def test_split_zero_tip():
    # boundary tip == 0
    assert split_bill(1000, 2, 0) == 500


# Decision 3: grand_total % people != 0
def test_split_even_no_round_up():
    assert split_bill(1000, 4, 10) == 275


def test_split_uneven_round_up():
    # 1000 / 3 = 333 r1 -> 334
    assert split_bill(1000, 3, 0) == 334


# ======================= table_wait =======================
# Decision 1: party_size > 12
def test_wait_party_13_call_ahead():
    assert table_wait(13, 5, False) == "call ahead"


def test_wait_party_12_not_call_ahead():
    # boundary: 12 is not > 12
    assert table_wait(12, 5, False) == "seat now"


# Decision 2: has_reservation
def test_wait_reservation_seat_now():
    assert table_wait(4, 0, True) == "seat now"


# Decision 3: free_tables == 0
def test_wait_no_free_tables():
    assert table_wait(4, 0, False) == "waitlist"


# Decision 4 (elif): party_size > 6 and free_tables < 2
def test_wait_large_party_one_table():
    # both True -> waitlist
    assert table_wait(8, 1, False) == "waitlist"


def test_wait_large_party_two_tables():
    # party > 6 True, free_tables < 2 False -> seat now
    assert table_wait(8, 2, False) == "seat now"


def test_wait_small_party_one_table():
    # party > 6 False (short-circuit) -> seat now
    assert table_wait(6, 1, False) == "seat now"
