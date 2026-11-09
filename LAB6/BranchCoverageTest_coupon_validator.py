import pytest
from coupon_validator import coupon_discount, best_discount, is_expired


# ---------- coupon_discount ----------
def test_welcome_coupon_new_user():
    assert coupon_discount("WELCOME10", 200, True, "mon") == 20


def test_welcome_coupon_existing_user_gets_nothing():
    assert coupon_discount("WELCOME10", 200, False, "mon") == 0


def test_empty_cart_raises_error():
    with pytest.raises(ValueError):
        coupon_discount("WELCOME10", 0, True, "mon")


def test_negative_cart_raises_error():
    with pytest.raises(ValueError):
        coupon_discount("FLAT100", -50, True, "mon")


def test_weekend_coupon_big_cart_on_weekend():
    assert coupon_discount("WEEKEND20", 600, False, "sat") == pytest.approx(120)


def test_weekend_coupon_small_cart_on_weekend():
    assert coupon_discount("WEEKEND20", 200, False, "sun") == 50


def test_weekend_coupon_on_weekday_gives_nothing():
    assert coupon_discount("WEEKEND20", 600, False, "tue") == 0


def test_flat100_large_cart():
    assert coupon_discount("FLAT100", 400, False, "mon") == 100


def test_flat100_small_cart_gives_nothing():
    assert coupon_discount("FLAT100", 250, False, "mon") == 0


def test_unknown_code_gives_nothing():
    assert coupon_discount("FREESTUFF", 400, True, "sat") == 0


# ---------- best_discount ----------
def test_best_discount_picks_highest_coupon():
    assert best_discount(["WELCOME10", "FLAT100"], 400, True, "mon") == 100


def test_best_discount_is_capped_at_forty_percent():
    assert best_discount(["WEEKEND20"], 100, False, "sun") == pytest.approx(40)


# ---------- is_expired ----------
def test_zero_validity_expired():
    assert is_expired(10, 5, 0) is True


def test_coupon_within_validity_not_expired():
    assert is_expired(10, 5, 10) is False


# ================= extra tests added for BRANCH coverage =================
def test_best_discount_keeps_earlier_coupon_when_later_one_is_smaller():
    # FLAT100 (100) comes first, WELCOME10 (40) is not better -> skip branch
    assert best_discount(["FLAT100", "WELCOME10"], 400, True, "mon") == 100


def test_best_discount_with_no_codes_is_zero():
    # loop never runs
    assert best_discount([], 400, True, "mon") == 0


def test_best_discount_equal_to_cap_is_not_reduced():
    # WEEKEND20 gives 50 on a 125 cart and the cap is exactly 50
    assert best_discount(["WEEKEND20"], 125, False, "sat") == pytest.approx(50)


def test_best_discount_ignores_unknown_codes():
    assert best_discount(["BOGUS", "FLAT100"], 400, False, "mon") == 100


def test_weekend_coupon_on_saturday_and_sunday_both_work():
    assert coupon_discount("WEEKEND20", 500, False, "sat") == pytest.approx(100)
    assert coupon_discount("WEEKEND20", 500, False, "sun") == pytest.approx(100)


def test_weekend_coupon_cart_boundary_at_500():
    assert coupon_discount("WEEKEND20", 500, False, "sat") == pytest.approx(100)
    assert coupon_discount("WEEKEND20", 499, False, "sat") == 50


def test_weekend_coupon_on_friday_gives_nothing():
    assert coupon_discount("WEEKEND20", 500, False, "fri") == 0


def test_flat100_cart_boundary_at_300():
    assert coupon_discount("FLAT100", 300, False, "mon") == 0
    assert coupon_discount("FLAT100", 301, False, "mon") == 100


def test_is_expired_on_last_valid_day_is_false():
    assert is_expired(15, 5, 10) is False


def test_is_expired_one_day_after_validity_is_true():
    assert is_expired(16, 5, 10) is True


def test_negative_validity_is_expired():
    assert is_expired(10, 5, -3) is True
