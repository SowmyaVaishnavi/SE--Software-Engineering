import math

MAX_DAYS = 365


def sanitize_license_plate(plate):
    """Remove '-', ' ', '_' and '#' from a plate and upper-case it.

    Returns None if the input is not a string or nothing is left after cleaning.
    """
    if not isinstance(plate, str):
        return None
    plate = plate.strip()
    for ch in ['-', ' ', '_', '#']:
        plate = plate.replace(ch, '')
    plate = plate.upper()
    return plate if plate else None


def _parse_mileage(text):
    """Parse one non-negative, finite mileage value, or return None."""
    text = text.strip()
    if not text or not text.isascii() or '_' in text:
        return None
    try:
        value = float(text)
    except ValueError:
        return None
    if not math.isfinite(value) or value < 0:  # rejects nan, inf, negatives
        return None
    return value


def parse_trip_mileage(mileage_csv):
    """Parse '100.5, 45.2, 80.0' into [100.5, 45.2, 80.0].

    Returns None if the input is invalid.
    """
    if not isinstance(mileage_csv, str):
        return None
    result = []
    for part in mileage_csv.split(','):
        value = _parse_mileage(part)
        if value is None:
            return None
        result.append(value)
    return result


def format_rental_invoice(record):
    """Turn 'Driver:Days:Category' into an invoice line.

    Returns None if the input is invalid.
    """
    if not isinstance(record, str):
        return None
    parts = record.split(':')
    if len(parts) != 3:
        return None
    driver = parts[0].strip()
    days_text = parts[1].strip()
    category = parts[2].strip()
    if not driver or not category:
        return None
    # ASCII digits only: rejects '', '-3', '1.5', '1_0', '²'
    if not (days_text.isascii() and days_text.isdigit()):
        return None
    try:
        days = int(days_text)
    except ValueError:  # absurdly long digit strings
        return None
    if not 1 <= days <= MAX_DAYS:
        return None
    daily_rate = 50.0 if category.lower() == "suv" else 30.0
    total = days * daily_rate
    return f"Driver {driver} booked {category} for {days} days: Total ${total:.2f}"


def main():
    print("==== Running sanitize_license_plate ====")
    raw_plate = input("Enter license plate with delimiters (-, _, #): ")
    clean_plate = sanitize_license_plate(raw_plate)
    print("Sanitized Plate:", clean_plate if clean_plate is not None else "Invalid plate")

    print("\n==== Running parse_trip_mileage ====")
    csv_input = input("Enter CSV of mileages (e.g. 100.5, 45.2, 80.0): ")
    mileage_list = parse_trip_mileage(csv_input)
    print("Parsed Mileage List:", mileage_list if mileage_list is not None else "Invalid mileage data")

    print("\n==== Running format_rental_invoice ====")
    record_input = input("Enter rental record (Driver:Days:Category): ")
    invoice = format_rental_invoice(record_input)
    print("Rental Invoice:", invoice if invoice is not None else "Invalid rental record")


if __name__ == "__main__":
    main()
