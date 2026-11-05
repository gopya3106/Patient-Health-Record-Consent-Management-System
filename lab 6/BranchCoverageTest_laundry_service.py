"""Lab 6 - Branch coverage tests for laundry_service.py.

Goal: make every decision (if / elif / else) evaluate to BOTH True and False,
and exercise the boundary values of each comparison.
"""
import pytest
from laundry_service import extra_weight_charge, order_acceptable, dropoff_status


# ======================= extra_weight_charge =======================

# --- garment_type not in INCLUDED_KG : True / False ---
def test_unknown_garment_type_raises():
    with pytest.raises(ValueError, match="unknown garment type"):
        extra_weight_charge("leather", 5, "standard", False)


@pytest.mark.parametrize("garment, included", [("regular", 5), ("delicate", 3), ("bedding", 8)])
def test_each_known_garment_at_included_limit_is_free(garment, included):
    assert extra_weight_charge(garment, included, "standard", False) == 0


# --- weight_kg < 0 : True / False (boundary 0) ---
def test_negative_weight_raises():
    with pytest.raises(ValueError, match="invalid weight"):
        extra_weight_charge("regular", -1, "standard", False)


def test_zero_weight_is_valid_and_free():
    assert extra_weight_charge("regular", 0, "standard", False) == 0


# --- is_member and garment_type != "bedding" ---
def test_member_non_bedding_gets_two_extra_kg():
    # regular: 5 + 2 = 7 included -> 9 kg = 2 extra * 30
    assert extra_weight_charge("regular", 9, "standard", True) == 60


def test_member_delicate_gets_two_extra_kg():
    # delicate: 3 + 2 = 5 included -> 5 kg = free
    assert extra_weight_charge("delicate", 5, "standard", True) == 0


def test_member_bedding_gets_no_bonus():
    # bedding: 8 included (no member bonus) -> 10 kg = 2 extra * 30
    assert extra_weight_charge("bedding", 10, "standard", True) == 60


def test_non_member_no_bonus():
    # regular: 5 included -> 7 kg = 2 extra * 30
    assert extra_weight_charge("regular", 7, "standard", False) == 60


# --- extra <= 0 : True / False (boundary) ---
def test_extra_exactly_zero_is_free():
    assert extra_weight_charge("regular", 5, "express", False) == 0


def test_extra_just_above_zero_is_charged():
    assert extra_weight_charge("regular", 5.5, "standard", False) == pytest.approx(15)


# --- speed == "standard" : True / False ---
def test_standard_rate_small_extra():
    assert extra_weight_charge("regular", 10, "standard", False) == 5 * 30


def test_express_rate_small_extra():
    assert extra_weight_charge("regular", 10, "express", False) == 5 * 50


def test_other_speed_uses_non_standard_rate():
    # any speed that is not "standard" falls into the else branch (rate 50),
    # but only "express" gets the +10 heavy surcharge
    assert extra_weight_charge("regular", 10, "same-day", False) == 5 * 50


# --- extra > 10 : True / False (boundary 10) ---
def test_extra_exactly_ten_no_heavy_surcharge():
    assert extra_weight_charge("regular", 15, "standard", False) == 10 * 30


def test_heavy_standard_load():
    # extra 15, rate 30 + 15 = 45 ; inner `speed == "express"` is False
    assert extra_weight_charge("regular", 20, "standard", False) == 15 * 45


def test_heavy_express_load():
    # extra 15, rate 50 + 15 + 10 = 75 ; inner `speed == "express"` is True
    assert extra_weight_charge("regular", 20, "express", False) == 15 * 75


def test_heavy_other_speed_load():
    # extra 15, rate 50 + 15 = 65 ; not standard, not express
    assert extra_weight_charge("regular", 20, "same-day", False) == 15 * 65


def test_heavy_member_bedding_express():
    # bedding 8 included (no bonus) -> 30 kg = 22 extra, rate 75
    assert extra_weight_charge("bedding", 30, "express", True) == 22 * 75


# ======================= order_acceptable =======================

# --- is_delicate True: items <= 5 True / False ---
def test_delicate_at_item_limit_accepted():
    assert order_acceptable(5, 5, True) is True


def test_delicate_over_item_limit_rejected():
    assert order_acceptable(5, 6, True) is False


def test_delicate_ignores_weight_limit():
    assert order_acceptable(30, 3, True) is True


# --- is_delicate False: weight_kg > 25 True / False ---
def test_overweight_order_rejected():
    assert order_acceptable(26, 10, False) is False


def test_weight_at_limit_accepted():
    assert order_acceptable(25, 10, False) is True


# --- items <= 40 True / False ---
def test_order_acceptable():
    assert order_acceptable(10, 20, False) is True


def test_items_at_limit_accepted():
    assert order_acceptable(10, 40, False) is True


def test_too_many_items_rejected():
    assert order_acceptable(10, 41, False) is False


# ======================= dropoff_status =======================

# --- has_bedding x is_express (all four cutoff combinations) ---
@pytest.mark.parametrize(
    "has_bedding, is_express, cutoff",
    [(False, False, 60), (False, True, 90), (True, False, 90), (True, True, 120)],
)
def test_cutoff_boundaries(has_bedding, is_express, cutoff):
    # >= cutoff -> accepted
    assert dropoff_status(cutoff, has_bedding, is_express) == "accepted"
    # just below cutoff -> late
    assert dropoff_status(cutoff - 1, has_bedding, is_express) == "late"
    # exactly cutoff - 20 -> still late
    assert dropoff_status(cutoff - 20, has_bedding, is_express) == "late"
    # below late window -> rejected
    assert dropoff_status(cutoff - 21, has_bedding, is_express) == "rejected"


def test_dropoff_well_before_closing_accepted():
    assert dropoff_status(200, False, False) == "accepted"


def test_dropoff_at_closing_rejected():
    assert dropoff_status(0, True, True) == "rejected"
