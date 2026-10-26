import json
from copy import deepcopy

import pytest
from fastapi.testclient import TestClient

from great_projects_editor_web.services.wonder import sources, values
from great_projects_editor_web.services.wonder_resource import WonderResourceService
from great_projects_editor_web.services.platform import snapshot_files


@pytest.fixture(scope="module")
def service():
    return WonderResourceService()


def test_bootstrap_is_summary_only(service, monkeypatch):
    def fail_detail(_wonder_id):
        raise AssertionError("bootstrap must not build a wonder detail")

    monkeypatch.setattr(service, "get_wonder_payload", fail_detail)
    payload = service.bootstrap_payload()
    assert payload["initial_wonder_id"] == payload["wonders"][0]["id"]
    assert "current_wonder" not in payload
    assert "ritual_designs" not in payload
    assert len(json.dumps(payload, ensure_ascii=False).encode("utf-8")) < 200_000


def test_detail_uses_versioned_option_catalog_and_source_values_exclude_options(service):
    catalog = service.option_catalog_payload()
    assert set(catalog["catalogs"]) == {
        "country_modifier", "local_modifier", "reward_type"
    }
    assert all(catalog["catalogs"].values())
    wonders = service.list_wonders()
    ids = (
        wonders[0]["id"],
        next(wonder["id"] for wonder in wonders if wonder["is_unique"] and "lavra" in wonder["key"]),
    )
    for wonder_id in ids:
        detail = service.get_wonder_payload(wonder_id)
        assert detail["catalog_version"] == catalog["version"]
        assert len(json.dumps(detail, ensure_ascii=False).encode("utf-8")) < 500_000
        fields = [field for section in detail["mechanics"]["sections"] for field in section["fields"]]
        assert any('"catalog_ref"' in json.dumps(field["structured_value"]) for field in fields)
        for field in fields:
            if field["structured_value"] is not None and field["field_type"] in {
                "modifier_table", "reward_editor", "unique_ritual_editor", "unique_ceremony_editor",
                "site_trigger_template", "site_preference_template",
            }:
                source_value = json.loads(field["original_value"])
                assert '"options"' not in json.dumps(source_value)
                assert '"cost_options"' not in json.dumps(source_value)
                assert source_value == values.without_editor_options(field["structured_value"])












def test_http_unavailable_service(monkeypatch):
    from great_projects_editor_web import server

    def fail_load(_operation_store):
        raise ValueError("invalid wonder data")

    monkeypatch.setattr(server, "WonderResourceService", fail_load)
    with TestClient(server.create_app()) as client:
        for path in ("/api/resources/editor.wonder", "/api/wonder-localization/catalog"):
            response = client.get(path)
            assert response.status_code == 503
            assert response.json()["detail"] == "invalid wonder data"
