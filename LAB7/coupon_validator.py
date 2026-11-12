import math
import re
from datetime import date


def split_code(code):
    """Split a coupon code like 'save-20' into ('SAVE', 20).

    Returns None if the input is not a string or is not in PREFIX-NUMBER form.
    """
    if not isinstance(code, str):
        return None
    parts = code.strip().upper().split('-')
    if len(parts) != 2:
        return None
    prefix, value = parts
    if not prefix:
        return None
    # only plain digits 0-9: rejects '', '+5', '1_0', ' 5' and other odd forms
    if not (value.isascii() and value.isdigit()):
        return None
    return prefix, int(value)


def most_expensive(prices_csv):
    """Return the highest price in a comma separated string.

    Returns None if the input is not a string, is empty, or contains anything
    that is not a finite, non negative number.
    """
    if not isinstance(prices_csv, str):
        return None
    prices = []
    for item in prices_csv.split(','):
        try:
            price = float(item)
        except ValueError:
            return None
        if not math.isfinite(price) or price < 0:
            return None
        prices.append(price)
    return max(prices)


def expiry_days(date_text):
    """Return the number of days since 2024 for a date written as YYYY-MM-DD.

    Returns None if the input is not a string or is not a real calendar date.
    """
    if not isinstance(date_text, str):
        return None
    match = re.fullmatch(r"(\d{4})-(\d{1,2})-(\d{1,2})", date_text.strip(),
                         re.ASCII)
    if match is None:
        return None
    year, month, day = (int(p) for p in match.groups())
    try:
        date(year, month, day)  # rejects month 13, day 32, 30 February, year 0
    except ValueError:
        return None
    return (year - 2024) * 365 + (month - 1) * 30 + day


def main():
    print("==== Running split_code ====")
    user_input = input("Enter a coupon code (e.g. save-20): ")
    result = split_code(user_input)
    if result is None:
        print("Invalid coupon code. Use the form PREFIX-NUMBER.")
    else:
        print("Prefix and Value:", result)

    print("\n==== Running most_expensive ====")
    user_input = input("Enter item prices as CSV (e.g. 199,49.5,320): ")
    result = most_expensive(user_input)
    if result is None:
        print("Invalid prices. Use non negative numbers separated by commas.")
    else:
        print("Most Expensive Item:", result)

    print("\n==== Running expiry_days ====")
    user_input = input("Enter an expiry date as YYYY-MM-DD: ")
    result = expiry_days(user_input)
    if result is None:
        print("Invalid date. Use a real date in the form YYYY-MM-DD.")
    else:
        print("Days Since 2024:", result)


if __name__ == "__main__":
    main()
