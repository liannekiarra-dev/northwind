from __future__ import annotations

from app import data


def test_all_deliveries_returns_all_seed_records():
    deliveries = data.all_deliveries()
    assert len(deliveries) == len(data.DELIVERIES)
    assert {d["id"] for d in deliveries} == {d["id"] for d in data.DELIVERIES}


def test_every_delivery_has_the_expected_shape():
    for delivery in data.all_deliveries():
        assert set(delivery) == {"id", "destination", "status", "driver"}
        assert delivery["id"].startswith("NL-")
        assert delivery["status"] in {"pending", "in_transit", "delivered"}


def test_all_deliveries_returns_copies_not_references():
    """Callers must not be able to mutate the seed data by accident."""
    first = data.all_deliveries()
    first[0]["status"] = "TAMPERED"
    second = data.all_deliveries()
    assert second[0]["status"] != "TAMPERED"


def test_find_delivery_returns_the_matching_record():
    delivery = data.find_delivery("NL-1002")
    assert delivery is not None
    assert delivery["destination"] == "Bristol"
    assert delivery["status"] == "delivered"


def test_find_delivery_returns_a_copy():
    delivery = data.find_delivery("NL-1001")
    assert delivery is not None
    delivery["driver"] = "TAMPERED"
    assert data.find_delivery("NL-1001")["driver"] != "TAMPERED"


def test_find_delivery_unknown_id_returns_none():
    assert data.find_delivery("does-not-exist") is None


def test_find_delivery_is_case_sensitive():
    assert data.find_delivery("nl-1001") is None
