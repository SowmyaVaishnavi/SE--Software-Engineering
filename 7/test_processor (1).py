import string
import pytest
from hypothesis import given, strategies as st
from processor import sanitize_license_plate, parse_trip_mileage, format_rental_invoice


# ---------- 1. No-crash fuzz tests ----------

@given(st.text() | st.none())
def test_sanitize_license_plate_no_crash(s):
    try:
        sanitize_license_plate(s)
    except Exception as e:
        assert False, f"sanitize_license_plate crashed with: {e!r} on input {s!r}"


@given(st.text() | st.none())
def test_parse_trip_mileage_safe(s):
    try:
        parse_trip_mileage(s)
    except Exception as e:
        assert False, f"parse_trip_mileage crashed with: {e!r} on input {s!r}"


@given(st.text() | st.none())
def test_format_rental_invoice_safe(s):
    try:
        format_rental_invoice(s)
    except Exception as e:
        assert False, f"format_rental_invoice crashed with: {e!r} on input {s!r}"


# ---------- 2. Extra: non-string types must not crash ----------

@given(st.one_of(st.integers(), st.floats(), st.lists(st.integers()),
                 st.booleans(), st.none()))
def test_all_functions_handle_non_strings(x):
    for fn in (sanitize_license_plate, parse_trip_mileage, format_rental_invoice):
        try:
            fn(x)
        except Exception as e:
            assert False, f"{fn.__name__} crashed with: {e!r} on input {x!r}"


# ---------- 3. Extra: correctness on valid inputs ----------

ALNUM = string.ascii_letters + string.digits


@given(st.text(alphabet=ALNUM, min_size=1, max_size=10))
def test_sanitize_valid(p):
    messy = f" -{p[:1]}_ {p[1:]}# "
    assert sanitize_license_plate(messy) == p.upper()


@given(st.lists(st.floats(min_value=0, max_value=1e6,
                          allow_nan=False, allow_infinity=False),
                min_size=1, max_size=20))
def test_parse_trip_mileage_valid(values):
    csv = ", ".join(repr(v) for v in values)
    assert parse_trip_mileage(csv) == values


@given(st.text(alphabet=string.ascii_letters, min_size=1, max_size=10),
       st.integers(min_value=1, max_value=365),
       st.sampled_from(["SUV", "suv", "Sedan", "Van"]))
def test_format_rental_invoice_valid(driver, days, category):
    rate = 50.0 if category.lower() == "suv" else 30.0
    expected = f"Driver {driver} booked {category} for {days} days: Total ${days * rate:.2f}"
    assert format_rental_invoice(f"{driver}:{days}:{category}") == expected
