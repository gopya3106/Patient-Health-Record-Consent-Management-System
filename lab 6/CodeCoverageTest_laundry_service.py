"""Lab 6 - Code (line) coverage tests for laundry_service.py.

Goal: execute every statement in laundry_service.py at least once.
"""
import pytest
from laundry_service import extra_weight_charge, order_acceptable, dropoff_status


# ---------------- extra_weight_charge ----------------

def test_within_included_weight():
    assert extra_weight_charge("regular", 4, "standard", False) == 0


def test_unknown_garment_type_raises():
    with pytest.raises(ValueError, match="unknown garment type"):
        extra_weight_charge("leather", 5, "standard", False)


def test_negative_weight_raises():
    with pytest.raises(ValueError, match="invalid weight"):
        extra_weight_charge("regular", -1, "standard", False)


def test_member_gets_extra_included_kg():
    # regular: 5 + 2 (member) = 7 included -> 9 kg gives 2 extra * 30
    assert extra_weight_charge("regular", 9, "standard", True) == 60


def test_standard_speed_small_extra():
    # 10 - 5 = 5 extra * 30
    assert extra_weight_charge("regular", 10, "standard", False) == 150


def test_express_speed_large_extra():
    # 20 - 5 = 15 extra; rate 50 + 15 (heavy) + 10 (express) = 75
    assert extra_weight_charge("regular", 20, "express", False) == 15 * 75


# ---------------- order_acceptable ----------------

def test_order_acceptable():
    assert order_acceptable(10, 20, False) is True


def test_delicate_order():
    assert order_acceptable(5, 3, True) is True


def test_overweight_order_rejected():
    assert order_acceptable(30, 10, False) is False


# ---------------- dropoff_status ----------------

def test_dropoff_bedding_express_accepted():
    # cutoff = 90 + 30 = 120
    assert dropoff_status(120, True, True) == "accepted"


def test_dropoff_regular_late():
    # cutoff = 60, late window 40..59
    assert dropoff_status(45, False, False) == "late"


def test_dropoff_regular_rejected():
    assert dropoff_status(10, False, False) == "rejected"
