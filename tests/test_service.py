
from __future__ import annotations

from app import data


def test_root_lists_the_service_and_endpoints(http_get):
    resp = http_get("/")
    assert resp.status == 200
    assert resp.content_type == "application/json"
    payload = resp.json()
    assert payload["service"] == "Northwind Logistics delivery tracking"
    assert "/health" in payload["endpoints"]


def test_health_always_returns_ok(http_get):
    resp = http_get("/health")
    assert resp.status == 200
    assert resp.json() == {"status": "ok"}


def test_deliveries_returns_all_records(http_get):
    resp = http_get("/deliveries")
    assert resp.status == 200
    payload = resp.json()
    assert isinstance(payload, list)
    assert len(payload) == len(data.DELIVERIES)


def test_single_delivery_is_returned_by_id(http_get):
    resp = http_get("/deliveries/NL-1004")
    assert resp.status == 200
    payload = resp.json()
    assert payload["id"] == "NL-1004"
    assert payload["destination"] == "Glasgow"


def test_unknown_delivery_id_returns_404_with_message(http_get):
    resp = http_get("/deliveries/NL-9999")
    assert resp.status == 404
    assert "NL-9999" in resp.json()["error"]


def test_unknown_path_returns_404(http_get):
    resp = http_get("/not-a-real-path")
    assert resp.status == 404
    assert resp.json() == {"error": "Not found"}


def test_trailing_slash_is_normalised(http_get):
    """`/deliveries/` and `/deliveries` should behave the same."""
    with_slash = http_get("/deliveries/")
    without_slash = http_get("/deliveries")
    assert with_slash.status == without_slash.status == 200
    assert with_slash.json() == without_slash.json()


def test_query_string_is_ignored_for_routing(http_get):
    resp = http_get("/deliveries/NL-1001?verbose=true")
    assert resp.status == 200
    assert resp.json()["id"] == "NL-1001"


def test_responses_declare_json_content_type(http_get):
    for path in ("/", "/health", "/deliveries", "/deliveries/NL-1001"):
        resp = http_get(path)
        assert resp.content_type == "application/json", path
def test_deliveries_have_expected_shape(http_get):
    """Every delivery record exposes the core fields clients rely on."""
    payload = http_get("/deliveries").json()
    for record in payload:
        assert "id" in record
        assert "destination" in record
def test_health_declares_json_and_ok_body(http_get):
    resp = http_get("/health")
    assert resp.status == 200
    assert resp.content_type == "application/json"
    assert resp.json() == {"status": "ok"}
def test_root_endpoint_advertises_all_routes(http_get):
    endpoints = http_get("/").json()["endpoints"]
    assert set(endpoints) >= {"/health", "/deliveries", "/deliveries/{id}"}