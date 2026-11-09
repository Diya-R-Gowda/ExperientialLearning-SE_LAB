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
    # WELCOME10 gives 40, FLAT100 gives 100 -> 100 wins, below the 40% cap (160)
    assert best_discount(["WELCOME10", "FLAT100"], 400, True, "mon") == 100


def test_best_discount_is_capped_at_forty_percent():
    # WEEKEND20 gives 50 on a 100 cart, but the cap is 40
    assert best_discount(["WEEKEND20"], 100, False, "sun") == pytest.approx(40)


# ---------- is_expired ----------
def test_zero_validity_expired():
    assert is_expired(10, 5, 0) is True


def test_coupon_within_validity_not_expired():
    assert is_expired(10, 5, 10) is False
