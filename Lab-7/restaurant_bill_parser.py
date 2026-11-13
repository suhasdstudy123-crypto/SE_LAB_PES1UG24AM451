"""
Restaurant bill parser - fixed (hardened) version.
SRN : PES1UG24AM451
Name: Suhas D

Every function now validates its input and never raises on bad input:
  * clean_dish_name   -> always returns a str ("" for invalid input)
  * parse_item_prices -> always returns a list of non-negative ints
  * split_amount      -> returns an int share, or None if the input is invalid
"""
import re

DISH_MARKERS = ('*', '#', '~')
MAX_DIGITS = 9                      # prices/totals above 999,999,999 are rejected
WHOLE_NUMBER = re.compile(r'\+?\d{1,%d}' % MAX_DIGITS, re.ASCII)


def _to_whole_number(value):
    """Return value as a non-negative int, or None if it is not a plain
    ASCII whole number (rejects '', '-5', '12.5', 'abc', '1_000', unicode
    digits and absurdly long numbers)."""
    value = value.strip()
    if not WHOLE_NUMBER.fullmatch(value):
        return None
    return int(value)


def clean_dish_name(name):
    """
    Removes the chef's-special markers (*, #, ~) and title-cases the name.
    Non-string input (e.g. None) returns an empty string.
    """
    if not isinstance(name, str):
        return ""
    for ch in DISH_MARKERS:
        name = name.replace(ch, '')
    # collapse runs of whitespace left behind by removed markers
    return " ".join(name.split()).title()


def parse_item_prices(text):
    """
    Parses comma-separated prices into a list of ints.
    Empty, negative, decimal or non-numeric entries are skipped.
    Non-string input returns an empty list.
    """
    if not isinstance(text, str):
        return []
    prices = []
    for part in text.split(','):
        price = _to_whole_number(part)
        if price is not None:
            prices.append(price)
    return prices


def split_amount(text):
    """
    Splits 'TOTAL/PEOPLE' into the amount each person pays.
    Returns None when the input is not exactly two whole numbers separated
    by one '/', or when PEOPLE is zero.
    """
    if not isinstance(text, str):
        return None
    parts = text.split('/')
    if len(parts) != 2:
        return None
    total = _to_whole_number(parts[0])
    people = _to_whole_number(parts[1])
    if total is None or people is None or people == 0:
        return None
    return total // people


def main():
    print("==== Running clean_dish_name ====")
    value = input("Enter a dish name from the menu (e.g. *paneer tikka*): ")
    name = clean_dish_name(value)
    print("Dish name:", name if name else "Invalid dish name")

    print("\n==== Running parse_item_prices ====")
    value = input("Enter item prices separated by commas (e.g. 250,180,320): ")
    print("Item prices:", parse_item_prices(value))

    print("\n==== Running split_amount ====")
    value = input("Enter the bill and number of people as TOTAL/PEOPLE (e.g. 1200/4): ")
    share = split_amount(value)
    if share is None:
        print("Invalid input: use TOTAL/PEOPLE with whole numbers and PEOPLE > 0")
    else:
        print("Each person pays:", share)


if __name__ == "__main__":
    main()
