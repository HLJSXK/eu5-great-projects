"""Generate paid identity decisions and their vanilla lifecycle integration."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / 'scripts_engineering_department'))
from wonder_mechanics.io import load_all_wonder_mechanics
from wonder_mechanics.render import render_header
from wonder_mechanics.naming import final_building_level_sync_hidden_event_id
from wonder_identity import variants
from wonder_ritual_codegen import block
from vanilla_takeover.parse import Source, REFERENCE, splice

SCRIPT_REL = 'scripts_engineering_department/in_game/common/scripted_effects/gen_tv_wonder_identity_effects.py'
DATA_REL = 'data/unique_wonders.yaml + .eu5-base/reference_game_files/game'


def outputs():
    wonders, _ = load_all_wonder_mechanics()
    effects, decisions, callbacks = [], [], []
    vanilla = []
    for w, v in variants(wonders):
        prefix = f"tv_wonder_{w['key']}_{v['key']}"
        flag = v['global_variable']
        marker = prefix + '_ritual_identity'
        site = f"location:{w['location']}"
        sync = f"trigger_event_silently = {{ id = tv_engineering_department.{final_building_level_sync_hidden_event_id(w)} days = 1 }}"
        idle = f"NOT = {{ var:tv_wonder_locked ?= {w['id']} var:tv_wonder_stage ?= {{ this >= 3 }} }}"
        eligible = f"owns = {site}\n{v['eligible_script']}\nNOT = {{ has_global_variable = {flag} }}\n{site} = {{ location_building_level = {{ building_type = building_type:{w['final_building']} value >= 1 }} }}\n{idle}"
        reset = f"owner ?= {{ save_scope_as = tv_wonder_ritual_sync_country }}\ntv_wonder_{w['key']}_ritual_revoke_effect = yes"
        # Reuse the final-building callback next day to rebuild country/plain/display caches.
        changed = f"{site} = {{\n{reset}\nset_variable = {{ name = {marker} value = 1 }}\n{sync}\n}}"
        effects.append(block(prefix + '_changed_effect', changed))
        affordable = f"gold >= {{ save_temporary_value_as = {{ name = scale value = {v['cost_scale']} }} value = scaled_gold_for_effect }}"
        effect = f"if = {{ limit = {{ {eligible}\n{affordable} }}\nchange_gold_effect = {{ scale = -{v['cost_scale']} }}\n{v['reward_script']}\nhidden_effect = {{ set_global_variable = {flag}\nforce_city_gfx_rebuild = {site}\n{prefix}_changed_effect = yes }}\n}}"
        decisions.append(block(prefix + '_decision', f"decision_category = other_decisions\npotential = {{ owns = {site} {v['eligible_script']} NOT = {{ has_global_variable = {flag} }} }}\nallow = {{ {eligible}\n{affordable} }}\nai_will_do = {{ value = 0 }}\noption = {{ name = {prefix}_decision.a effect = {{ {effect} }} }}"))
        # The native hook may already have removed the flag; the marker remembers only
        # which dedication needs invalidating, never drives presentation or eligibility.
        restored = f"{site} = {{ if = {{ limit = {{ has_variable = {marker} }}\n{reset}\nremove_variable = {marker}\nforce_city_gfx_rebuild = {site}\n{sync}\n}} }}"
        callbacks.append(block(prefix + '_religion_changed', f"trigger = {{ owns = {site} {v['restore_script']} }}\neffect = {{ hidden_effect = {{ {restored} }} }}"))
        # Ownership already revokes every dedication. Drop the old identity marker
        # on Christian reconquest so a later denomination change cannot erase a new rite.
        callbacks.append(block(prefix + '_owner_changed', f"trigger = {{ this = {site} scope:winner ?= {{ {v['restore_script']} }} }}\neffect = {{ hidden_effect = {{ remove_variable = {marker} force_city_gfx_rebuild = {site} {sync} }} }}"))
        if 'vanilla_event' in v:
            spec = v['vanilla_event']
            source = Source.read(REFERENCE / spec['path'])
            node = next(n for n in source.definitions if n.key == spec['id'])
            option = next(n for n in node.children if n.key == 'option' and n.scalar('name') == spec['option'])
            # Copy only this event; keep vanilla cost, rewards, random path and timing.
            trigger = node.child('trigger')
            first_effect = next(n for n in option.children if n.key == 'set_global_variable')
            additions = [(trigger.closing - node.start, trigger.closing - node.start,
                          '\n' + f"{site} = {{ location_building_level = {{ building_type = building_type:{w['final_building']} value >= 1 }} }}\n{idle}\n"),
                         (first_effect.start - node.start, first_effect.start - node.start,
                          f'trigger = {{ {eligible} }}\n if = {{ limit = {{ {eligible} }}\n'),
                         (option.closing - node.start, option.closing - node.start,
                          f'\n hidden_effect = {{ {prefix}_changed_effect = yes }}\n }}\n')]
            vanilla.append(f"namespace = {node.namespace}\n" + splice(source.raw(node), additions))
    header = '\n'.join(render_header(SCRIPT_REL, DATA_REL)) + '\n'
    return {
        'in_game/common/scripted_effects/tv_wonder_identity_effects.txt': header + ''.join(effects),
        'in_game/common/decisions/tv_wonder_identity_decisions.txt': header + ''.join(decisions),
        'in_game/common/on_action/tv_wonder_identity_on_action.txt': header + ''.join(callbacks),
        'in_game/events/0000_tv_wonder_identity_events.txt': header + '\n'.join(vanilla),
    }


def main():
    for relative, content in outputs().items():
        path = ROOT / 'src' / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding='utf-8-sig', newline="\n")
        print(f'Wrote {path.relative_to(ROOT)}')


if __name__ == '__main__':
    main()
