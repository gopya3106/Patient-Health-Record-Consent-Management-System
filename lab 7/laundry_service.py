import math


def _to_finite_float(value):
    """Convert a string to a finite float, or return None if it isn't one."""
    try:
        number = float(value)
    except (TypeError, ValueError, OverflowError):
        return None
    if not math.isfinite(number):        # rejects nan, inf, -inf
        return None
    return number


def parse_order(text):
    """'garment:kg' -> ('Garment', kg). Returns None for invalid input."""
    if not isinstance(text, str):
        return None
    parts = text.split(':')
    if len(parts) != 2:                  # missing or extra ':'
        return None
    garment = parts[0].strip()
    if not garment:                      # empty garment name
        return None
    kg = _to_finite_float(parts[1].strip())
    if kg is None or kg <= 0:            # non-numeric, nan/inf, zero or negative
        return None
    return garment.title(), kg


def weight_average(weights_csv):
    """'3,5,8' -> mean weight (rounded to 2 dp). Returns None for invalid input."""
    if not isinstance(weights_csv, str) or not weights_csv.strip():
        return None
    values = []
    for raw in weights_csv.split(','):
        raw = raw.strip()
        if not raw:                      # empty element, e.g. "1,,3"
            return None
        number = _to_finite_float(raw)
        if number is None or number < 0:  # non-numeric, nan/inf or negative
            return None
        values.append(number)
    # true division (the original // truncated the average)
    return round(math.fsum(values) / len(values), 2)


def payable_charge(text):
    """'charge|discount' -> charge*1.18 - discount, never below 0.
    Returns None for invalid input."""
    if not isinstance(text, str):
        return None
    parts = text.split('|')
    if len(parts) != 2:                  # missing or extra '|'
        return None
    charge = _to_finite_float(parts[0].strip())
    discount = _to_finite_float(parts[1].strip())
    if charge is None or discount is None:
        return None
    if charge < 0 or discount < 0:       # negative values not allowed
        return None
    total = charge * 1.18 - discount
    if not math.isfinite(total):         # overflow for huge charges
        return None
    return round(max(total, 0), 2)


def main():
    print("==== Running parse_order ====")
    user_input = input("Enter garment:weight in kg (e.g. regular:6): ")
    result = parse_order(user_input)
    print("Garment and Weight:", result if result is not None else "Invalid input")

    print("\n==== Running weight_average ====")
    user_input = input("Enter garment weights as CSV (e.g. 3,5,8): ")
    result = weight_average(user_input)
    print("Average Weight:", result if result is not None else "Invalid input")

    print("\n==== Running payable_charge ====")
    user_input = input("Enter charge|discount (e.g. 300|40): ")
    result = payable_charge(user_input)
    print("Payable Charge:", result if result is not None else "Invalid input")


if __name__ == "__main__":
    main()
