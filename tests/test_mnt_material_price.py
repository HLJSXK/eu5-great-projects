from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COMPAT_GOODS = ROOT / "submods/tv_meiou_and_taxes_compat/in_game/common/goods/tv_wonder_goods.txt"


def test_mnt_compat_halves_gp_material_price_without_changing_goods_identity():
    text = COMPAT_GOODS.read_text(encoding="utf-8-sig")
    assert "REPLACE:tv_wonder_materials = {" in text
    assert "default_market_price = 2.5" in text
    for field in (
        "category = produced",
        "color = goods_tv_wonder_materials",
        "transport_cost = 2",
        "all = 1.0",
        "ai_rgo_expansion_priority = 0.25",
    ):
        assert field in text
    assert "\ntv_wonder_materials = {" not in text
