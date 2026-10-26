"""Contracts for ED's generated vanilla wonder takeover."""

import copy
import re
import sys
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts_engineering_department"))

from wonder_mechanics._core import load_unique_wonders_source_data
from vanilla_takeover.parse import parse, walk
from vanilla_takeover.scan import scan_reference

# Independent acceptance inventory from handoff section 6. Counts include reads,
# writes and explicitly retained random-art operations; startup is checked below.
EXPECTED = {
    "taj_mahal": {"flavor_mug.6": 1},
    "saint_peters_basilica": {"flavor_pap.1501": 2},
    "porcelain_tower": {"flavor_chi.52": 1},
    "st_basil_cathedral": {"flavor_mos.62": 2},
    "trinity_lavra_st_sergius_work_of_art": {"flavor_mos.6": 1, "flavor_mos.7": 1, "flavor_mos.11": 6, "flavor_mos.12": 2, "flavor_mos.38": 2},
    "winter_palace": {"flavor_mos.92": 2, "flavor_rus.70": 2},
    "milan_cathedral": {"flavor_mlo.24": 1},
    "duomo_di_firenze": {"flavor_flo.28": 1},
    "peacock_throne": {"flavor_mug.8": 1},
    "ali_qapu_palace": {"flavor_ira.38": 1},
    "leaning_tower_of_pisa": {"flavor_pis.4": 2},
    "kremlin": {"mos_build_kremlin_decision": 2, "flavor_mos.28": 1, "flavor_mos.34": 1, "flavor_mos.35": 2, "flavor_mos.37": 2, "flavor_mos.57": 2, "flavor_mos.58": 1, "flavor_mos.62": 1},
    "forbidden_city": {"flavor_chi.53": 1, "flavor_chi.54": 2},
    "red_fort": {"flavor_mug.11": 1},
    "versailles": {"flavor_fra.10": 1, "flavor_fra.426": 1, "flavor_fra.428": 1, "fra_versailles_residence_decision": 1, "fra_versailles_permanent_decision": 1},
    "lighthouse_of_alexandria": {"flavor_mam.40": 1},
    "tower_of_belem": {"flavor_por.5": 1},
    "el_escorial_palace": {"flavor_cas.46": 1, "flavor_cas.69": 1, "flavor_cas.117": 1},
    "schonbrunn_palace": {"flavor_hab.25": 1},
    "enderun_academy": {"tur_enderun_academy_decision": 1},
    "fra_louvre_museum": {"flavor_fra.550": 1},
    "hanseatic_town_hall": {"flavor_hsa.7": 3},
    "venetian_arsenal": {"flavor_ven.28": 1, "grand_tour_events.2": 3},
    "alhambra": {"flavor_gra.14": 1},
    "woodhenge_of_cahokia": {"flavor_chk.3": 1, "flavor_chk.6": 1},
    "khmer_baray": {"flavor_khm.1000": 1, "flavor_khm.1001": 1},
    "ibadat_khana": {"flavor_mug.10": 2},
    "zwinger": {"flavor_mei.110": 1},
    "upgrade_great_wall": {"flavor_chi.2": 3},
    "destroy_grand_canal_china": {"flavor_chi.30": 1},
    "repair_grand_canal_china": {"flavor_chi.87": 1, "flavor_chi.124": 1},
    "louvre_palace_renovations": {"flavor_fra.305": 1},
}
STARTUP = {
    "hagia_sophia", "notre_dame_de_paris", "leaning_tower_of_pisa", "stonehenge",
    "mont_saint_michel", "aachen_cathedral", "lalibela_church_st_george_work_of_art",
    "teotihuacan_temple_work_of_art", "djenne_mosque", "sankore_madrasa",
    "kyiv_pechersk_lavra_work_of_art", "alhambra_palace", "hanseatic_town_hall",
    "venetian_arsenal", "alhambra", "great_enclosure", "great_hill_complex",
    "great_valley_complex", "khmer_baray", "monument_kairouan_mosque",
    "parthenon_of_athens_work_of_art",
}


@pytest.fixture(scope="module")
def scan():
    return scan_reference()


def test_parser_handles_comments_strings_helpers_and_namespaces():
    text = 'namespace = a\n# ignored = {\nscripted_effect helper = { log = "} # {" }\na.1 = { type = country_event helper = yes }\nnamespace = b\nscripted_trigger check = { always = yes }\nb.2 = { type = country_event }'
    nodes = parse(text)
    blocks = [n for n in nodes if n.opening is not None]
    assert [(n.key, n.declaration, n.namespace) for n in blocks] == [
        ("helper", "scripted_effect", "a"), ("a.1", "", "a"),
        ("check", "scripted_trigger", "b"), ("b.2", "", "b")]
    assert text[blocks[0].start:blocks[0].end] == 'scripted_effect helper = { log = "} # {" }'


def test_scanner_matches_handoff_inventory(scan):
    from collections import Counter
    expected = Counter((carrier, event) for carrier, events in EXPECTED.items() for event, n in events.items() for _ in range(n))
    actual = Counter((s.carrier.key, s.site_id) for s in scan.sites if s.form != "startup")
    assert actual == expected
    startup = [s for s in scan.sites if s.form == "startup"]
    assert Counter(s.carrier.key for s in startup) == Counter(STARTUP)
    assert all("/1337/" in s.source.path for s in startup)
    assert len(scan.sites) == 100


def test_carriers_exist_and_presence_thresholds(scan):
    assert all(c.definition or (c.kind == "art" and any(s.carrier is c for s in scan.sites)) for c in scan.carriers.values())
    assert all(c.level == (2 if c.key in {"kremlin", "woodhenge_of_cahokia"} else 1) for c in scan.carriers.values() if c.kind in {"art", "building"})


def test_takeover_helpers_match_declared_operations(scan):
    from vanilla_takeover.render import read_requirements
    triggers = (ROOT / "src/in_game/common/scripted_triggers/tv_vw_vanilla_takeover_triggers.txt").read_text(encoding="utf-8-sig")
    effects = (ROOT / "src/in_game/common/scripted_effects/tv_vw_vanilla_takeover_effects.txt").read_text(encoding="utf-8-sig")
    ts = {n.key for n in parse(triggers) if n.children}
    es = {n.key for n in parse(effects) if n.children}
    keys = {c.wonder["key"] for c in scan.carriers.values()}
    assert {f"tv_vw_{key}_gate_trigger" for key in keys} <= ts
    assert len([key for key in ts if key.endswith("_gate_trigger")]) == 43
    assert {f"tv_vw_{key}_present_{scope}_trigger" for key, scopes in read_requirements(scan).items() for scope in scopes} == {key for key in ts if "_present_" in key}
    expected_ops = {f"tv_vw_{s.carrier.wonder['key']}_{s.op}_effect" for s in scan.sites if s.form == "write"}
    assert expected_ops <= es
    assert "value >= 2" in effects
    assert "tv_vw_unique_grand_canal_damage_debt" in effects
    assert "custom_tooltip" not in effects
    assert "change_building_level_in_location" not in effects


def test_event_and_decision_copies_are_lossless_outside_rewrites():
    from vanilla_takeover.rewrite import copies
    compiled = copies()
    event_file = (ROOT / "src/in_game/events/0000_tv_vw_vanilla_event_overrides.txt").read_text(encoding="utf-8-sig")
    decision_file = (ROOT / "src/in_game/common/decisions/tv_vw_vanilla_decision_overrides.txt").read_text(encoding="utf-8-sig")
    assert "REPLACE:" not in event_file
    assert sum(not r.definition.declaration and "/events/" in r.source.path for r in compiled.records) == 50
    assert sum("/decisions/" in r.source.path for r in compiled.records) == 4
    for record in compiled.records:
        is_decision = "/decisions/" in record.source.path
        assert record.text in (decision_file if is_decision else event_file)
        raw = record.source.raw(record.definition)
        edited = record.text.removeprefix("REPLACE:")
        original_cursor = edited_cursor = 0
        restored = []
        for start, end, replacement in record.edits:
            unchanged = raw[original_cursor:start]
            assert edited[edited_cursor:edited_cursor + len(unchanged)] == unchanged
            restored.append(unchanged + raw[start:end])
            edited_cursor += len(unchanged)
            assert edited[edited_cursor:edited_cursor + len(replacement)] == replacement
            edited_cursor += len(replacement)
            original_cursor = end
        assert edited[edited_cursor:] == raw[original_cursor:]
        restored.append(edited[edited_cursor:])
        assert "".join(restored) == raw
    assert all(n.key.startswith("REPLACE:") for n in parse(decision_file) if n.children)


def test_local_helpers_copied_transitively_and_renamed():
    from vanilla_takeover.rewrite import copies
    compiled = copies()
    helpers = [r for r in compiled.records if r.definition.declaration]
    assert {r.definition.key for r in helpers} == {"is_yuan_china", "upgrade_great_wall", "is_part_of_yellow_river_near_canal", "destroy_grand_canal_china", "repair_grand_canal_china"}
    for record in compiled.records:
        originals = {n.key for n in record.source.definitions if n.declaration}
        assert all(n.key not in originals for top in parse(record.text) for n, _ in walk(top))
    wall = next(r for r in compiled.records if r.definition.key == "flavor_chi.2")
    assert wall.text.count("tv_vw_upgrade_great_wall = yes") == 3
    assert wall.text.count("tv_vw_unique_ming_great_wall_raise_effect = yes") == 3
    helper = next(r for r in helpers if r.definition.key == "upgrade_great_wall")
    assert "tv_vw_unique_ming_great_wall_raise_effect" not in helper.text


def test_transferred_reads_and_original_fallbacks(scan):
    from vanilla_takeover.rewrite import copies, replacement
    copies()
    for site in scan.sites:
        if site.form == "write" and site.carrier.declaration["mode"] == "replace":
            assert site.source.raw(site.node) in replacement(site)
    kremlin = next(s for s in scan.sites if s.carrier.key == "kremlin" and s.form == "level")
    assert "ed_level = 3 vanilla_level = 2" in replacement(kremlin)
    winter = next(s for s in scan.sites if s.carrier.key == "winter_palace" and s.form == "art_here")
    assert "this = work_of_art:catherine_palace" in replacement(winter)
    assert all(s.status in {"改写", "保持"} for s in scan.sites if s.form != "startup")


def test_vanilla_definition_ownership_is_unique():
    from collections import defaultdict
    owners = defaultdict(list)
    pattern = re.compile(r"(?m)^((?:REPLACE:)[\w.]+|[\w]+\.\d+)\s*=\s*\{")
    for root in ("src",):
        for path in (ROOT / root).rglob("*.txt"):
            text = path.read_text(encoding="utf-8-sig")
            for m in pattern.finditer(text):
                owners[m[1]].append(str(path.relative_to(ROOT)))
    assert not {key: paths for key, paths in owners.items() if len(paths) > 1}


def test_building_seals_have_one_allow_and_preserve_other_vanilla_fields(scan):
    text = (ROOT / "src/in_game/common/building_types/tv_vw_vanilla_building_overrides.txt").read_text(encoding="utf-8-sig")
    nodes = {n.key: n for n in parse(text) if n.children}
    carriers = [c for c in scan.carriers.values() if c.kind == "building"]
    assert len(nodes) == len(carriers) == 21
    for c in carriers:
        n = nodes["REPLACE:" + c.key]
        allows = [child for child in n.children if child.key == "allow"]
        assert len(allows) == 1
        tooltip = next(child for child in allows[0].children if child.key == "custom_tooltip" and child.scalar("text") == "TV_VW_CARRIER_LOCKED_TT")
        assert tooltip.scalar("text") == "TV_VW_CARRIER_LOCKED_TT"
        assert tooltip.child("NOT").child("owner").op == "?="
        assert tooltip.child("NOT").scalar("owner") == f"location:{c.wonder['location']}.owner"
        source, original = c.definition
        for child in original.children:
            if child.key == "unique_production_methods":
                copied = n.child("unique_production_methods")
                assert len(copied.children) == len(child.children)
                for method, renamed in zip(child.children, copied.children):
                    assert renamed.key == "tv_vw_" + method.key
                    assert text[renamed.start + len(renamed.key):renamed.end] == source.raw(method)[len(method.key):]
            elif child.key != "allow":
                assert source.raw(child) in text[n.start:n.end]
            else:
                for condition in child.children:
                    assert source.raw(condition) in text[allows[0].start:allows[0].end]


def test_replaced_building_production_method_ids_are_unique_and_localized(scan):
    from vanilla_takeover.render import buildings
    expected = {
        "lighthouse_of_alexandria_maintenance", "venetian_arsenal_maintenance",
        "cahokia_woodhenge_production_method", "ibadat_khana_maintenance", "endrun_academy_maintenance",
    }
    generated = buildings()
    path = ROOT / 'src/in_game/common/building_types/tv_vw_vanilla_building_overrides.txt'
    assert path.read_text(encoding='utf-8-sig').split('\n\n', 1)[1] == generated.rstrip() + '\n'
    names = [method.key for n in parse(generated) for group in n.children
             if group.key == 'unique_production_methods' for method in group.children]
    assert set(names) == {'tv_vw_' + key for key in expected}
    assert len(names) == len(set(names)) == 5
    vanilla = {method.key for c in scan.carriers.values() if c.kind == 'building'
               for group in c.definition[1].children if group.key == 'unique_production_methods'
               for method in group.children}
    assert not vanilla.intersection(names)
    locales = ROOT / 'src/main_menu/localization'
    files = list(locales.glob('*/tv_engineering_department_l_*.yml'))
    assert len(files) == 11
    for locale in files:
        assert locale.read_bytes().startswith(b'\xef\xbb\xbf')
        text = locale.read_text(encoding='utf-8-sig')
        for key in expected:
            assert re.search(r'^ tv_vw_' + key + r':0 "\$' + key + r'\$"$', text, re.M), locale


def test_startup_reconciliation_is_owned_and_runs_after_ed_initialization(scan):
    effects = (ROOT / "src/in_game/common/scripted_effects/tv_vw_vanilla_takeover_effects.txt").read_text(encoding="utf-8-sig")
    startup = next(n for n in parse(effects) if n.key == "tv_vw_startup_reconcile_effect")
    body = effects[startup.start:startup.end]
    assert "tv_wonder_raise_" not in body and "tv_wonder_lower_" not in body
    assert body.count("destroy_art = ") + body.count("destroy_building_forcefully = ") == 21
    for c in scan.carriers.values():
        for site in c.startup:
            assert f"location:{c.wonder['location']}.owner" in body
            if c.kind == "building":
                assert f"location:{site.location} = {{" in body
                assert f'"building(building_type:{c.key}|owner)"' in body
            else:
                assert f"exists = work_of_art:{c.key}" in body
                assert f"work_of_art:{c.key} ?= {{ location.owner ?= location:{c.wonder['location']}.owner }}" in body
    hook = "tv_wonder_vw_startup_reconcile_on_game_start"
    ed = (ROOT / "src/in_game/common/on_action/tv_engineering_department_pulse_bridges.txt").read_text(encoding="utf-8-sig")
    assert not (ROOT / "src/in_game/common/on_action/tv_pulse_bridges.txt").exists()
    start = next(n for n in parse(ed) if n.key == "on_game_start")
    load = next(n for n in parse(ed) if n.key == "on_game_load")
    assert hook in ed[start.start:start.end]
    assert hook not in ed[load.start:load.end]
    names = [n.key for n in start.child("on_actions").children]
    assert names.index(hook) == names.index("tv_wonder_initialize_existing_unique_wonders_on_game_start") + 1
    callback_path = ROOT / "src/in_game/common/on_action/tv_vw_vanilla_takeover_on_action.txt"
    callback = parse(callback_path.read_text(encoding="utf-8-sig"))[0]
    hidden = callback.child("effect").child("hidden_effect")
    assert [(n.key, n.value) for n in hidden.children] == [("tv_vw_startup_reconcile_effect", "yes")]


@pytest.mark.parametrize("kind", ["building", "art"])
def test_startup_gate_distinguishes_instance_owner_from_ed_site_owner(scan, monkeypatch, kind):
    from dataclasses import replace
    from types import SimpleNamespace
    from vanilla_takeover import render
    site = next(s for s in scan.sites if s.form == "startup" and s.carrier.kind == kind)
    different = "genoa" if site.carrier.wonder["location"] != "genoa" else "venice"
    site = replace(site, location=different)
    monkeypatch.setattr(render, "scan_reference", lambda: SimpleNamespace(sites=[site]))
    generated = parse(render.startup_reconcile())[0]
    if kind == "building":
        location = generated.children[0]
        assert location.key == f"location:{different}"
        guard = location.child("if").child("limit").child("owner")
        assert guard.op == "?="
        instance_location = location.key.removeprefix("location:")
    else:
        art = generated.children[0].child("limit").child(f"work_of_art:{site.carrier.key}")
        guard = art.child("location.owner")
        assert art.op == guard.op == "?="
        # The art object's live placement, rather than its setup declaration,
        # supplies the left-hand owner. Exercise a displaced artwork as well.
        instance_location = different
    ed_location = guard.value.removeprefix("location:").removesuffix(".owner")
    assert ed_location == site.carrier.wonder["location"]
    assert instance_location != ed_location
    for owners, expected in [({instance_location: "A", ed_location: "B"}, False),
                             ({instance_location: "A", ed_location: "A"}, True),
                             ({ed_location: "A"}, False), ({}, False)]:
        actual = owners.get(instance_location) is not None and owners.get(instance_location) == owners.get(ed_location)
        assert actual == expected


def test_current_startup_sites_and_inherited_bookmark_provenance(scan):
    assert all(s.location == s.carrier.wonder["location"] for s in scan.sites if s.form == "startup")
    assert scan.setup_includes["main_menu/setup/1658/11_art.txt"] == ["setup/1337/11_art"]
    assert scan.setup_includes["main_menu/setup/1658/07_cities_and_buildings.txt"] == ["setup/1337/07_cities_and_buildings"]


def test_porcelain_tower_upstream_saved_location_matches_ed_site(scan):
    from vanilla_takeover.parse import REFERENCE, Source
    source = Source.read(REFERENCE / "in_game/events/DHE/flavor_chi.txt")
    upstream = next(n for n in source.definitions if n.key == "flavor_chi.51")
    saves = [(n, parents) for n, parents in walk(upstream) if n.key == "save_scope_as" and n.value == "target_location"]
    assert len(saves) == 1
    source_site = next(n.key.removeprefix("location:") for n in reversed(saves[0][1]) if n.key.startswith("location:"))
    carrier = scan.carriers["porcelain_tower"]
    assert source_site == carrier.wonder["location"] == "shangyuan"
    assert any(n.key == "trigger_event_silently" and n.scalar("id") == "flavor_chi.52" for n, _ in walk(upstream))
    downstream = next(s for s in scan.sites if s.carrier is carrier and s.site_id == "flavor_chi.52")
    assert downstream.ancestors[-1].key == "scope:target_location"


def test_localization_key_is_bom_encoded():
    for lang in ("english", "simp_chinese"):
        raw = (ROOT / f"src/main_menu/localization/{lang}/tv_engineering_department_l_{lang}.yml").read_bytes()
        assert raw.startswith(b"\xef\xbb\xbf")
        assert len(re.findall(r'^ TV_VW_CARRIER_LOCKED_TT: ".*"\r?$', raw.decode("utf-8-sig"), re.M)) == 1


def test_disaster_dispatch_matches_entire_ed_final_building_map():
    from vanilla_takeover.parse import REFERENCE, Source
    from vanilla_takeover.render import DAMAGE_EFFECTS
    path = ROOT / "src/in_game/common/scripted_effects/tv_vw_vanilla_damage_overrides.txt"
    text = path.read_text(encoding="utf-8-sig")
    nodes = parse(text)
    assert {n.key for n in nodes} == {"REPLACE:" + key for key in DAMAGE_EFFECTS}
    index = (ROOT / "src/in_game/common/scripted_effects/tv_wonder_index_effects.txt").read_text(encoding="utf-8-sig")
    pairs = re.findall(r'add_to_global_variable_map = \{ name = tv_wonder_final_building_type_to_wonder_id key = building_type:(\w+) value = (\d+) \}', index)
    assert len(pairs) == 195
    assert len({i for _, i in pairs}) == 195
    expected = dict(pairs)
    vanilla = Source.read(REFERENCE / "in_game/common/scripted_effects/location_effects.txt")
    original = {n.key: n for n in vanilla.definitions}
    ed_branches = []
    for n in nodes:
        ed = n.child("if")
        fallback = n.child("else")
        ed_branches.append(text[ed.start:ed.end])
        assert "tv_wonder_final_building_type_to_wonder_id" in text[ed.start:ed.end]
        assert "damage_debt" not in text[ed.start:ed.end]
        assert "change_building_level_in_location" not in text[ed.start:ed.end]
        dispatch = [child for child in ed.children if child.key in {"if", "else_if"}]
        assert len(dispatch) == 195
        actual = {}
        for branch in dispatch:
            building = branch.child("limit").child("prev")
            final = building.scalar("building_type").removeprefix("building_type:")
            level = building.child("building_level")
            assert level.op == ">=" and level.value == "2"
            calls = [child for child in branch.children if child.key.startswith("tv_wonder_lower_")]
            assert len(calls) == 1
            unique = int(expected[final]) > 100
            assert calls[0].key == f"tv_wonder_lower_{'unique' if unique else 'generic'}_level_effect"
            actual[final] = calls[0].scalar("wonder")
        assert set(actual) == set(expected)
        orig = original[n.key.removeprefix("REPLACE:")]
        assert text[fallback.opening+1:fallback.closing] == vanilla.text[orig.opening+1:orig.closing]
    assert ed_branches[0] == ed_branches[1] == ed_branches[2]


def test_fixed_site_cap_and_deleted_id(unique_source):
    from collections import Counter
    ws = unique_source["unique_wonders"]
    assert len(ws) == 139
    assert 198 not in {w["id"] for w in ws}
    assert max(Counter(w["location"] for w in ws).values()) <= 3
    assert {w["key"] for w in ws if w["location"] == "paris"} == {"unique_notre_dame_de_paris", "unique_louvre_palace", "unique_versailles_palace"}


def test_final_coverage_has_no_unhandled_sites(scan):
    from collections import Counter
    from vanilla_takeover.rewrite import copies
    from vanilla_takeover.render import startup_reconcile
    copies()
    startup_reconcile()
    assert Counter(s.status for s in scan.sites) == {"改写": 75, "保持": 4, "开局对齐": 21}


def test_generated_takeover_files_are_current():
    from vanilla_takeover.render import block, buildings, damage, operations, startup_reconcile, triggers
    from vanilla_takeover.rewrite import copies
    expected = {
        "in_game/common/scripted_triggers/tv_vw_vanilla_takeover_triggers.txt": triggers(),
        "in_game/common/scripted_effects/tv_vw_vanilla_takeover_effects.txt": operations() + "\n\n" + startup_reconcile(),
        "in_game/common/building_types/tv_vw_vanilla_building_overrides.txt": buildings(),
        "in_game/common/scripted_effects/tv_vw_vanilla_damage_overrides.txt": damage(),
        "in_game/events/0000_tv_vw_vanilla_event_overrides.txt": copies().events,
        "in_game/common/decisions/tv_vw_vanilla_decision_overrides.txt": copies().decisions,
        "in_game/common/on_action/tv_vw_vanilla_takeover_on_action.txt": block("tv_wonder_vw_startup_reconcile_on_game_start", block("effect", block("hidden_effect", "tv_vw_startup_reconcile_effect = yes"))),
    }
    for path, body in expected.items():
        text = (ROOT / "src" / path).read_text(encoding="utf-8-sig")
        assert text.split("\n\n", 1)[1] == body.rstrip() + "\n", path


def test_takeover_sources_preserve_bom_and_generated_newline_convention():
    assert (ROOT / "data/unique_wonders.yaml").read_bytes().startswith(b"\xef\xbb\xbf")
    registry = yaml.load((ROOT / "data/generated_files.yaml").read_text(encoding="utf-8-sig"), Loader=yaml.CSafeLoader)
    paths = [ROOT / e["output"] for e in registry["generated"] if "/gen_tv_vw_" in e["script"]]
    assert len(paths) == 7
    for path in paths:
        raw = path.read_bytes()
        assert raw.startswith(b"\xef\xbb\xbf"), path
        assert b"\r\n" not in raw and raw.count(b"\n") > 0, path


@pytest.fixture(scope="module")
def unique_source():
    return yaml.load((ROOT / "data/unique_wonders.yaml").read_text(encoding="utf-8-sig"), Loader=yaml.CSafeLoader)


def test_declarations_load():
    ws = load_unique_wonders_source_data()["unique_wonders"]
    assert sum("vanilla_carriers" in w for w in ws) == 43
    assert sum(len(w.get("vanilla_carriers", [])) for w in ws) == 48


@pytest.mark.parametrize("bad", ["kind", "mode", "replace_op", "duplicate", "augment_op", "level", "waiver"])
def test_carrier_shape_rejected(tmp_path, unique_source, bad):
    wonder = copy.deepcopy(unique_source["unique_wonders"][0])
    carrier = wonder["vanilla_carriers"][0]
    if bad == "kind":
        carrier["kind"] = "unknown"
    elif bad == "mode":
        carrier["mode"] = "unknown"
    elif bad == "replace_op":
        carrier["op"] = "raise"
    elif bad == "duplicate":
        wonder["vanilla_carriers"].append(copy.deepcopy(carrier))
    elif bad == "augment_op":
        carrier.update(kind="effect", mode="augment")
    elif bad == "level":
        carrier["present_at_level"] = 0
    else:
        wonder["vanilla_waivers"] = [{"site": "flavor_x.1", "carrier": "unknown", "reason": "test"}]
    path = tmp_path / "unique.yaml"
    path.write_text(yaml.dump({"unique_wonders": [wonder]}, Dumper=yaml.CSafeDumper), encoding="utf-8")
    with pytest.raises(ValueError):
        load_unique_wonders_source_data(path)
