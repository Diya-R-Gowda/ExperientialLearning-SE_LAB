import math
import string
from datetime import date

from hypothesis import given, strategies as st
from coupon_validator import split_code, most_expensive, expiry_days


# ---------- 1. Fuzz tests: the functions must never crash ----------
@given(st.text() | st.none())
def test_split_code_no_crash(s):
    try:
        split_code(s)
    except Exception as e:
        assert False, f"split_code crashed with: {e}"


@given(st.text() | st.none())
def test_most_expensive_no_crash(s):
    try:
        most_expensive(s)
    except Exception as e:
        assert False, f"most_expensive crashed with: {e}"


@given(st.text() | st.none())
def test_expiry_days_no_crash(s):
    try:
        expiry_days(s)
    except Exception as e:
        assert False, f"expiry_days crashed with: {e}"


# ---------- 2. Fuzz tests: wrong input types must not crash either ----------
wrong_types = st.one_of(st.integers(), st.floats(), st.booleans(),
                        st.lists(st.integers()), st.binary())


@given(wrong_types)
def test_non_string_inputs_are_rejected_safely(value):
    assert split_code(value) is None
    assert most_expensive(value) is None
    assert expiry_days(value) is None


# ---------- 3. Property tests: valid inputs must give correct answers ----------
@given(st.text(alphabet=string.ascii_letters, min_size=1),
       st.integers(min_value=0, max_value=10**9))
def test_split_code_valid_codes(prefix, value):
    assert split_code(f"{prefix}-{value}") == (prefix.upper(), value)
    assert split_code(f"  {prefix}-{value}  ") == (prefix.upper(), value)


@given(st.lists(st.floats(min_value=0, max_value=1e9,
                          allow_nan=False, allow_infinity=False),
                min_size=1))
def test_most_expensive_valid_prices(prices):
    csv = ",".join(repr(p) for p in prices)
    assert most_expensive(csv) == max(prices)


@given(st.text() | st.none())
def test_most_expensive_never_returns_nan_or_inf(s):
    result = most_expensive(s)
    assert result is None or math.isfinite(result)


@given(st.dates(min_value=date(1, 1, 1), max_value=date(9999, 12, 31)))
def test_expiry_days_valid_dates(d):
    text = f"{d.year:04d}-{d.month:02d}-{d.day:02d}"
    assert expiry_days(text) == (d.year - 2024) * 365 + (d.month - 1) * 30 + d.day


@given(st.text() | st.none())
def test_expiry_days_returns_int_or_none(s):
    result = expiry_days(s)
    assert result is None or isinstance(result, int)
