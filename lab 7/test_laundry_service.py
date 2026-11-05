import math

from hypothesis import given, settings, strategies as st
from laundry_service import parse_order, weight_average, payable_charge

# Text that looks a bit like real input, so the fuzzer also reaches the
# "almost valid" paths (separators, digits, signs, nan/inf, spaces).
near_valid = st.text(alphabet="0123456789.,:|-+ eE nainfNAIF regulardlicatbeding", max_size=30)
fuzz_input = st.text() | near_valid | st.none() | st.integers() | st.floats()


# ---------------- parse_order ----------------

@settings(max_examples=500)
@given(fuzz_input)
def test_parse_order_no_crash(s):
    try:
        result = parse_order(s)
    except Exception as e:
        assert False, f"parse_order crashed with: {e!r}"
    # Either rejected (None) or a valid (garment, weight) pair
    if result is not None:
        garment, kg = result
        assert isinstance(garment, str) and garment != ""
        assert math.isfinite(kg) and kg > 0


@given(st.sampled_from(["regular", "delicate", "bedding"]),
       st.floats(min_value=0.1, max_value=1000, allow_nan=False))
def test_parse_order_valid_input(garment, kg):
    assert parse_order(f"  {garment} : {kg} ") == (garment.title(), kg)


# ---------------- weight_average ----------------

@settings(max_examples=500)
@given(fuzz_input)
def test_weight_average_no_crash(s):
    try:
        result = weight_average(s)
    except Exception as e:
        assert False, f"weight_average crashed with: {e!r}"
    if result is not None:
        assert math.isfinite(result) and result >= 0


@given(st.lists(st.integers(min_value=0, max_value=10_000), min_size=1, max_size=20))
def test_weight_average_is_true_mean(weights):
    csv = ",".join(str(w) for w in weights)
    result = weight_average(csv)
    assert math.isclose(result, sum(weights) / len(weights), abs_tol=0.01)
    assert min(weights) - 0.01 <= result <= max(weights) + 0.01


# ---------------- payable_charge ----------------

@settings(max_examples=500)
@given(fuzz_input)
def test_payable_charge_no_crash(s):
    try:
        result = payable_charge(s)
    except Exception as e:
        assert False, f"payable_charge crashed with: {e!r}"
    if result is not None:
        assert math.isfinite(result) and result >= 0


@given(st.floats(min_value=0, max_value=100_000, allow_nan=False),
       st.floats(min_value=0, max_value=100_000, allow_nan=False))
def test_payable_charge_valid_input(charge, discount):
    result = payable_charge(f"{charge}|{discount}")
    expected = round(max(charge * 1.18 - discount, 0), 2)
    assert math.isclose(result, expected, abs_tol=0.01)
