"""Regression contracts for all priority projects, including colocated projects.

Inspect generated Jomini blocks, rather than generator Python source, so that
scope, branch, and GUI bindings are checked at the integration boundary.
"""

from dataclasses import dataclass
import importlib.util
from pathlib import Path
import re
import sys

import pytest


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts_engineering_department"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))
GAME = ROOT / "src" / "in_game"


@dataclass(frozen=True)
class Statement:
    key: str
    op: str
    value: str | tuple

    @property
    def children(self):
        return self.value if isinstance(self.value, tuple) else ()


def parse(script):
    """Retain duplicate keys, scope links, optional comparisons and GUI quotes."""
    tokens = re.findall(r'#[^\n]*|"(?:\\.|[^"\\])*"|[{}]|\?=|[<>!]=?|=|[^\s{}=<>!?]+', script)
    tokens = [token for token in tokens if not token.startswith("#")]
    position = 0

    def block(nested=False):
        nonlocal position
        statements = []
        while position < len(tokens) and tokens[position] != "}":
            key = tokens[position]
            if key in {"block", "blockoverride"} and tokens[position + 2] == "{":
                name = tokens[position + 1]
                position += 3
                statements.append(Statement(key, name, block(nested=True)))
                continue
            op = tokens[position + 1] if position + 1 < len(tokens) else ""
            if op not in {"=", "?=", "<", ">", "<=", ">=", "!="}:
                statements.append(Statement(key.strip('"'), "", key))
                position += 1
                continue
            position += 2
            value = tokens[position]
            position += 1
            if value == "{":
                value = block(nested=True)
            statements.append(Statement(key.strip('"'), op, value))
        if nested:
            assert position < len(tokens), "Unclosed generated block"
            position += 1
        return tuple(statements)

    result = block()
    assert position == len(tokens), "Unexpected generated closing brace"
    return result


def walk(statements):
    for statement in statements:
        yield statement
        yield from walk(statement.children)


def child(statements, key):
    matches = [statement for statement in statements if statement.key == key]
    assert len(matches) == 1, f"Expected one {key}, got {len(matches)}"
    return matches[0]


def contains(statements, key, value=None):
    return any(item.key == key and (value is None or item.value == value) for item in walk(statements))


def load_generator(name, relative_path):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / relative_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def module_generator():
    return load_generator("priority_module_generator", "in_game/common/scripted_effects/gen_tv_wonder_module_effects.py")


@pytest.fixture(scope="module")
def generated_effects(module_generator):
    lines = []
    module_generator.append_priority_candidate_storage_effects(lines)
    definitions = parse("\n".join(lines))
    assert len({node.key for node in definitions}) == len(definitions), "Duplicate generated effect definitions"
    return {node.key: node.children for node in definitions}


@pytest.fixture(scope="module")
def gui_generator():
    return load_generator("priority_gui_generator", "in_game/gui/panels/organization/gen_tv_engineering_department_wonder_mechanics_gui.py")


def source_blocks(relative_path):
    return {node.key: node.children for node in parse((GAME / relative_path).read_text(encoding="utf-8-sig"))}


def test_deployed_priority_effects_match_the_generator(generated_effects):
    deployed = source_blocks("common/scripted_effects/tv_wonder_module_effects.txt")
    for name, body in generated_effects.items():
        assert deployed[name] == body, f"Regenerate deployed priority effect {name}"


def test_priority_refresh_visits_the_whole_registry(generated_effects):
    refresh = generated_effects["tv_wonder_select_saved_priority_proposal_effect"]
    loops = [node for node in walk(refresh) if node.key == "every_key_in_variable_map"]
    registry_loops = [node for node in loops if contains(node.children, "variable", "tv_wonder_priority_candidate_site_by_id")]
    assert len(registry_loops) == 1
    loop = registry_loops[0].children
    assert contains(loop, "tv_wonder_validate_priority_candidate_for_saved_wonder_effect", "yes")
    assert contains(loop, "tv_wonder_remove_current_priority_candidate_effect", "yes")
    assert not any(node.key.startswith("random_") for node in walk(refresh))
    assert not any(node.key in {"every_location", "every_owned_location", "every_location_in_the_world"} for node in walk(refresh))
    # Stopping after finding the first proposal silently loses all later rows.
    if any(node.key == "limit" for node in loop):
        assert not contains(child(loop, "limit").children, "has_variable", "tv_wonder_priority_found")


def test_priority_validation_checks_owner_and_both_project_kinds(module_generator):
    wonders = [{"key": "unfinished_fixture", "id": 1}, {"key": "unique_fixture", "id": 101}]
    lines = []
    module_generator.append_priority_candidate_validation_effect(lines, wonders)
    validation = parse("\n".join(lines))[0].children
    cases = [node.children for node in validation if node.key == "if"]
    assert len(cases) == len(wonders)
    for wonder, case in zip(wonders, cases):
        guard = child(case, "limit").children
        assert contains(guard, "has_owner", "yes")
        assert contains(guard, "owner", "scope:tv_wonder_priority_owner")
        assert contains(guard, "var:tv_wonder_priority_candidate_wonder_id", str(wonder["id"]))
        for suffix in ("module", "final"):
            assert contains(case, f"tv_wonder_location_is_valid_priority_{suffix}_project_for_{wonder['key']}_trigger", "yes")


def test_colocated_wonders_are_listed_by_distinct_registration_ids(generated_effects):
    registration = generated_effects["tv_wonder_register_current_priority_candidate_effect"]
    # Registration assigns a new ID to each (site, wonder) project. In particular,
    # a final wonder and a different unfinished project can share one location.
    writes = [node.children for node in walk(registration) if node.key == "add_to_variable_map"]
    for map_name in ("site", "wonder", "mode"):
        entry = next(fields for fields in writes
                     if contains(fields, "name", f"tv_wonder_priority_candidate_{map_name}_by_id"))
        assert child(entry, "key").value == "local_var:tv_wonder_priority_candidate_id"
    assert any(contains(node.children, "name", "tv_wonder_priority_next_candidate_id")
               and contains(node.children, "add", "1")
               for node in walk(registration) if node.key == "change_variable")

    refresh = generated_effects["tv_wonder_select_saved_priority_proposal_effect"]
    additions = [node.children for node in walk(refresh) if node.key == "add_to_variable_list"]
    for group in ("unfinished", "expansion"):
        entry = next(fields for fields in additions
                     if contains(fields, "name", f"tv_wonder_priority_{group}_list"))
        assert child(entry, "target").value == "local_var:tv_wonder_priority_candidate_id"


def test_priority_refresh_clears_rows_and_display_cache_before_rebuilding(generated_effects):
    clear = generated_effects["tv_wonder_clear_priority_proposal_list_effect"]
    for group in ("unfinished", "expansion"):
        assert contains(clear, "clear_variable_list", f"tv_wonder_priority_{group}_list")
    for field in ("level", "cap", *(f"module_{part}" for part in range(1, 5))):
        assert contains(clear, "clear_variable_map", f"tv_wonder_priority_display_{field}")
    assert contains(clear, "clear_variable_map", "tv_wonder_priority_valid_candidate_deck")
    assert contains(clear, "remove_variable", "tv_wonder_priority_selected_candidate_id")
    # Clearing must preserve the registry, which is maintained by lifecycle hooks.
    for field in ("site", "wonder", "mode"):
        assert not contains(clear, "clear_variable_map", f"tv_wonder_priority_candidate_{field}_by_id")
    refresh = generated_effects["tv_wonder_select_saved_priority_proposal_effect"]
    clear_index = next(index for index, node in enumerate(refresh)
                       if node.key == "tv_wonder_clear_priority_proposal_list_effect")
    build_index = next(index for index, node in enumerate(refresh)
                       if contains((node,), "every_key_in_variable_map"))
    assert clear_index < build_index


def test_initial_preview_prefers_unfinished_and_does_not_consume_rows(generated_effects):
    refresh = generated_effects["tv_wonder_select_saved_priority_proposal_effect"]
    loops = [node.children for node in refresh if node.key == "every_in_list"]
    assert [child(loop, "variable").value for loop in loops] == [
        "tv_wonder_priority_unfinished_list", "tv_wonder_priority_expansion_list",
    ]
    for loop in loops:
        guard = child(loop, "limit").children
        assert contains(child(guard, "NOT").children, "has_variable", "tv_wonder_priority_found")
        assert contains(loop, "tv_wonder_apply_priority_candidate_by_id_effect", "yes")
        assert not contains(loop, "remove_from_variable_list")


def test_selecting_a_row_requires_registry_membership_and_current_eligibility(generated_effects):
    apply = generated_effects["tv_wonder_apply_priority_candidate_by_id_effect"]
    registered = child(apply, "if").children
    membership = child(registered, "limit").children
    for name in ("tv_wonder_priority_valid_candidate_deck", *(
        f"tv_wonder_priority_candidate_{field}_by_id" for field in ("site", "wonder", "mode")
    )):
        assert any(contains(node.children, "name", name)
                   and contains(node.children, "target", "local_var:tv_wonder_priority_candidate_id")
                   for node in membership if node.key == "is_key_in_variable_map")
    validation_index = next(index for index, node in enumerate(registered)
                            if contains((node,), "tv_wonder_validate_priority_candidate_for_saved_wonder_effect", "yes"))
    valid_index = next(index for index, node in enumerate(registered)
                      if node.key == "if" and contains(child(node.children, "limit").children,
                                                      "has_variable", "tv_wonder_priority_candidate_valid"))
    assert validation_index < valid_index
    valid = registered[valid_index].children
    for name in ("tv_wonder_proposal", "tv_wonder_proposal_mode", "tv_wonder_proposal_site",
                 "tv_wonder_priority_selected_candidate_id"):
        writes = [node for node in walk(apply) if node.key == "set_variable" and contains(node.children, "name", name)]
        assert writes and all(node in tuple(walk(valid)) for node in writes)
    # The newly computed mode must replace the saved mode if a project's state changed.
    mode = next(node.children for node in walk(valid)
                if node.key == "set_variable" and contains(node.children, "name", "tv_wonder_proposal_mode"))
    assert child(mode, "value").value == "var:tv_wonder_priority_candidate_current_mode"


def test_display_data_keeps_each_project_key_at_a_shared_site(module_generator):
    lines = []
    module_generator.append_priority_candidate_display_effect(lines, [
        {"id": 1, "key": "fixture", "final_building": "fixture_final"},
    ])
    display = parse("\n".join(lines))[0].children
    writes = [node.children for node in walk(display) if node.key == "add_to_variable_map"]
    expected = {f"tv_wonder_priority_display_{field}" for field in (
        "level", "cap", *(f"module_{part}" for part in range(1, 5)),
    )}
    assert {child(fields, "name").value for fields in writes} == expected
    assert all(child(fields, "key").value == "local_var:tv_wonder_priority_candidate_id" for fields in writes)


def test_priority_scripted_gui_guards_direct_selection_without_a_value_selector():
    name = "tv_wonder_select_priority_candidate"
    assert name not in source_blocks("common/generic_actions/tv_engineering_department_actions.txt")
    scripted_gui = source_blocks("common/scripted_guis/tv_wonder_priority_selection.txt")[name]
    assert child(scripted_gui, "scope").value == "country"
    assert contains(child(scripted_gui, "saved_scopes").children, "target_1")
    valid = child(scripted_gui, "is_valid").children
    for key, value in (("has_variable", "tv_engineering_department_member"),
                       ("tv_wonder_has_open_proposal_trigger", "yes"),
                       ("has_variable", "tv_wonder_priority_found"),
                       ("exists", "scope:target_1")):
        assert contains(valid, key, value)
    effect = child(scripted_gui, "effect").children
    guarded = child(effect, "if").children
    assert contains(child(guarded, "limit").children, "has_variable", "tv_engineering_department_member")
    assert contains(guarded, "tv_wonder_select_priority_candidate_effect", "yes")


def test_accept_revalidates_before_locking_and_refreshes_expired_selection():
    effects = source_blocks("common/scripted_effects/tv_engineering_department_effects.txt")
    accept = child(effects["tv_wonder_accept_proposal_effect"], "hidden_effect").children
    validation_index = next(index for index, node in enumerate(accept)
                            if node.key == "tv_wonder_validate_selected_priority_proposal_effect")
    guarded_index = next(index for index, node in enumerate(accept) if node.key == "if")
    assert validation_index < guarded_index
    guard = child(accept[guarded_index].children, "limit").children
    assert contains(guard, "has_variable", "tv_wonder_priority_selection_valid")
    assert contains(guard, "tv_wonder_has_open_proposal_trigger", "yes")
    assert contains(accept[guarded_index].children, "name", "tv_wonder_locked")
    assert contains(child(accept, "else_if").children, "tv_wonder_roll_new_proposal_effect", "yes")
    for cleanup in ("tv_wonder_clear_current_proposal_effect", "tv_wonder_clear_feasible_deck_effect"):
        assert contains(effects[cleanup], "tv_wonder_clear_priority_proposal_list_effect", "yes")


@pytest.mark.parametrize("choice", ["refute", "bribe"])
def test_rejection_leaves_priority_mode_before_starting_new_concept(choice):
    effects = source_blocks("common/scripted_effects/tv_engineering_department_effects.txt")
    hidden = child(effects[f"tv_wonder_{choice}_proposal_effect"], "hidden_effect").children
    declined = child(hidden, "if").children
    assert contains(child(declined, "limit").children, "has_variable", "tv_wonder_proposal_mode")
    assert any(contains(node.children, "name", "tv_wonder_priority_declined")
               and contains(node.children, "value", "1") for node in declined if node.key == "set_variable")
    assert contains(declined, "tv_wonder_clear_current_proposal_effect", "yes")
    assert contains(declined, "tv_wonder_clear_proposal_on_great_engineer_effect", "yes")
    assert [node.key for node in hidden] == ["if", "tv_wonder_start_concept_effect"]


def test_gui_lists_keep_candidate_identity_instead_of_collapsing_by_location(gui_generator):
    script = gui_generator.priority_candidates_list()
    nodes = parse(script)
    models = [node.value for node in walk(nodes) if node.key == "datamodel"]
    for group in ("unfinished", "expansion"):
        assert any(f"GetList('tv_wonder_priority_{group}_list')" in model for model in models)
    rows = [node.children for node in walk(nodes) if node.key == "item"]
    assert len(rows) == 2
    for row in rows:
        # Both rows execute the ID that was clicked, without opening a selector.
        button = child(row[0].children, "button").children
        scope = "GuiScope.SetRoot(InternationalOrganizationsView.GetPlayer.MakeScope).AddScope('target_1', MakeScopeValue(Scope.GetValue)).End"
        assert child(button, "onclick").value == f'"[GetScriptedGui(\'tv_wonder_select_priority_candidate\').Execute({scope})]"'
        assert child(button, "enabled").value == f'"[GetScriptedGui(\'tv_wonder_select_priority_candidate\').IsValid({scope})]"'
        assert not any(node.key in {"scripted_action_tooltip", "button_tooltip_override", "select_trigger"} for node in walk(row))
    assert "UIAction" not in script
    assert "IsUberButtonEnabled" not in script
    assert "action_tooltip_pop_out" not in script
    for map_name in ("candidate_wonder_by_id", "candidate_site_by_id", "display_level", "display_cap",
                     *(f"display_module_{part}" for part in range(1, 5))):
        assert f"GetVariableFromVariableMap('tv_wonder_priority_{map_name}', MakeScopeValue(Scope.GetValue))" in script
    assert "Scope.Self" not in script
    # A bare data type cannot supply an expression argument or action parameter.
    assert not re.search(r"\bScope\s*[)\]]", script)


@pytest.mark.parametrize("expansion", [False, True])
def test_priority_click_layer_has_explicit_transparent_texture(gui_generator, expansion):
    row = parse(gui_generator.priority_candidate_row(expansion=expansion))[0].children
    button = child(row, "button").children
    assert child(button, "texture").value == '"gfx/portraits/portrait_transparent.dds"'
    tooltip = child(button, "tooltipwidget").children
    assert contains(tooltip, "text", '"tv_wonder_select_priority_candidate"')
    assert contains(tooltip, "text", '"tv_wonder_select_priority_candidate_desc"')


def test_deployed_priority_rows_match_generated_bindings(gui_generator):
    deployed = (GAME / "gui" / "panels" / "organization" / "tv_engineering_department.gui").read_text(encoding="utf-8-sig")
    marker = "TV_WONDER_MECHANICS_PRIORITY_CANDIDATES"
    block = deployed.split(f"# BEGIN GENERATED {marker}\n", 1)[1].split(f"# END GENERATED {marker}", 1)[0]
    assert parse(block) == parse(gui_generator.priority_candidates_list())


@pytest.mark.parametrize("language", ["english", "simp_chinese"])
def test_priority_localization_uses_scope_values_and_direct_selection_tooltip(language):
    loc_dir = ROOT / "src" / "main_menu" / "localization" / language
    for filename in (f"tv_engineering_department_l_{language}.yml",
                     f"tv_engineering_department_wonder_mechanics_l_{language}.yml"):
        path = loc_dir / filename
        assert path.read_bytes().startswith(b"\xef\xbb\xbf"), path
    labels = (loc_dir / f"tv_engineering_department_l_{language}.yml").read_text(encoding="utf-8-sig")
    assert re.search(r'(?m)^ tv_wonder_select_priority_candidate: ".+"$', labels)
    assert re.search(r'(?m)^ tv_wonder_select_priority_candidate_desc: ".+"$', labels)
    assert "tv_wonder_no_priority_candidate_available:" not in labels
    assert "PERFORM_tv_wonder_select_priority_candidate_ACTION" not in labels
    mechanics = (loc_dir / f"tv_engineering_department_wonder_mechanics_l_{language}.yml").read_text(encoding="utf-8-sig")
    level_label = next(line for line in mechanics.splitlines()
                       if line.startswith(" TV_ENGINEERING_PRIORITY_LEVEL:"))
    for map_name in ("display_level", "display_cap"):
        assert f"GetVariableFromVariableMap('tv_wonder_priority_{map_name}', MakeScopeValue(Scope.GetValue))" in level_label
    assert "Scope.Self" not in level_label
    assert not re.search(r"\bScope\s*[)\]]", level_label)
