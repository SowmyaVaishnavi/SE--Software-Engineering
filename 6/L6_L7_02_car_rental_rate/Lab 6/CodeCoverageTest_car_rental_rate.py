import pytest
from car_rental_rate import process_rental_fleet, check_fleet_telematics

def r(**kw):
    d = {"is_confirmed": True, "vehicle_type": "economy", "driver_age": 30, "days": 1, "trip_segments": []}
    d.update(kw)
    return d

def test_single_economy_rental():
    res = process_rental_fleet([r(days=2, trip_segments=[100])], 10.0)
    assert res == {"total_revenue": 110.0, "status": "STANDARD"}

def test_invalid_not_list():
    with pytest.raises(ValueError):
        process_rental_fleet("abc", 10)

def test_invalid_negative_fee():
    with pytest.raises(ValueError):
        process_rental_fleet([], -1)

def test_unconfirmed_is_empty_batch():
    res = process_rental_fleet([{"is_confirmed": False}], 10)
    assert res == {"total_revenue": 0.0, "status": "EMPTY_BATCH"}

def test_defaults():
    res = process_rental_fleet([{"is_confirmed": True}], 10)
    assert res["total_revenue"] == 50.0

def test_zero_days_flag():
    res = process_rental_fleet([r(days=0)], 10)
    assert res["status"] == "EMPTY_BATCH"

def test_luxury():
    assert process_rental_fleet([r(vehicle_type="luxury")], 10)["total_revenue"] == 130.0

def test_suv():
    res = process_rental_fleet([r(vehicle_type="suv", days=2, trip_segments=[50])], 10)
    assert res["total_revenue"] == pytest.approx(160.0)

def test_negative_miles():
    res = process_rental_fleet([r(trip_segments=[-5, 100])], 0)
    assert res["total_revenue"] == pytest.approx(60.0)

def test_long_trip_adult():
    res = process_rental_fleet([r(trip_segments=[400])], 0)
    assert res["total_revenue"] == pytest.approx(200.0)

def test_long_trip_young_driver_breaks():
    res = process_rental_fleet([r(driver_age=20, days=2, trip_segments=[400, 50])], 0)
    assert res["total_revenue"] == pytest.approx(370.0)

def test_young_luxury_surcharge():
    res = process_rental_fleet([r(driver_age=22, vehicle_type="luxury", days=2)], 0)
    assert res["total_revenue"] == pytest.approx(340.0)

def test_high_risk():
    res = process_rental_fleet([r(days=0) for _ in range(5)], 0)
    assert res == {"total_revenue": 0.0, "status": "HIGH_RISK_AUDIT"}

def test_telematics_no_data():
    assert check_fleet_telematics([]) == "NO_DATA"

def test_telematics_ground():
    assert check_fleet_telematics([[110, 120]]) == "GROUND_VEHICLE"

def test_telematics_safe_with_reset():
    assert check_fleet_telematics([[110, 50, 110], [60]]) == "SAFE"