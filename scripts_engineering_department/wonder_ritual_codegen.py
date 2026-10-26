"""Unified ritual lifecycle and project flow. All rewards share one executable preview."""
from wonder_mechanics._core import ritual_styles, ritual_rules, render_header, location_reward_estate
from wonder_mechanics.render import loc_line, variable_map_key_trigger

ESTATES = ('nobles_estate', 'clergy_estate', 'burghers_estate', 'peasants_estate', 'dhimmi_estate', 'tribes_estate', 'cossacks_estate')
STYLE_MAP = 'tv_wonder_ritual_style_by_id'
MEMORY_MAP = 'tv_wonder_ritual_memory_by_id'


def block(name, body):
    return name + ' = {\n' + '\n'.join('\t' + line for line in body.splitlines()) + '\n}\n\n'


def has_style(w, n=None):
    key = w['id']
    exists = variable_map_key_trigger(STYLE_MAP, key)
    if n is None:
        return exists
    return f'trigger_if = {{ limit = {{ {exists} }} "variable_map({STYLE_MAP}|{key})" ?= {n} }} trigger_else = {{ always = no }}'


def max_level_cache(w, map_name, level):
    """Country scope: supplement one known instance, preserving a higher sibling."""
    replace = f'''remove_from_variable_map = {{ name = {map_name} key = {w['id']} }}
add_to_variable_map = {{ name = {map_name} key = {w['id']} value = {level} }}'''
    return f'''if = {{
limit = {{ NOT = {{ {variable_map_key_trigger(map_name, w['id'])} }} }}
{replace}
}}
else = {{
set_local_variable = {{ name = tv_wonder_increment_old_level value = "variable_map({map_name}|{w['id']})" }}
if = {{ limit = {{ local_var:tv_wonder_increment_old_level < {level} }}
{replace}
}}
remove_local_variable = tv_wonder_increment_old_level
}}'''


def plain_cache(w, level):
    return ('set_variable = { name = tv_wonder_has_plain_wonder value = 1 }\n'
            + max_level_cache(w, 'tv_wonder_plain_level_by_wonder_id', level))


def forgotten_plain_cache(w):
    # Location scope. Read this completed building only; no project variables or
    # owned-location traversal are needed after a century has elapsed.
    levels = '\n'.join(
        f'''{'if' if level == 6 else 'else_if'} = {{
limit = {{ location_building_level = {{ building_type = building_type:{w['final_building']} value >= {level} }} }}
set_local_variable = {{ name = tv_wonder_plain_instance_level value = {level} }}
}}''' for level in range(6, 0, -1))
    return f'''if = {{ limit = {{ has_building = building_type:{w['final_building']} }}
{levels}
owner ?= {{
{plain_cache(w, 'local_var:tv_wonder_plain_instance_level')}
}}
remove_local_variable = tv_wonder_plain_instance_level
}}'''


def state_effects(wonders, mechanics, reward_lines, location_reward_lines):
    out = []
    days = ritual_rules(mechanics)['memory_years'] * 365
    for w in wonders:
        prefix, wid = f"tv_wonder_{w['key']}_ritual", w['id']
        sync = ['save_scope_as = tv_wonder_ritual_sync_target_country'] if w.get('is_unique') else []
        for r in ritual_styles(w, mechanics):
            n, mod, loc = r['style'], r['modifier'], r['location_modifier']
            holding = (f"location:{w['location']} = {{ owner ?= scope:tv_wonder_ritual_sync_target_country has_building = building_type:{w['final_building']} {has_style(w, n)} }}"
                       if w.get('is_unique') else f"any_owned_location = {{ has_building = building_type:{w['final_building']} {has_style(w, n)} }}")
            sync.append(f'''if = {{
limit = {{ {holding} }}
add_country_modifier = {{ modifier = {mod} years = -1 mode = replace }}
}}
else = {{ remove_country_modifier = {mod} }}''')
            body = f'''hidden_effect = {{
remove_from_variable_map = {{ name = {STYLE_MAP} key = {wid} }}
add_to_variable_map = {{ name = {STYLE_MAP} key = {wid} value = {n} }}
remove_from_variable_map = {{ name = {MEMORY_MAP} key = {wid} }}
add_to_variable_map = {{ name = {MEMORY_MAP} key = {wid} value = 1 days = {days} }}
trigger_event_silently = {{ id = tv_engineering_department.{3000 + wid} days = {days + 1} }}
}}
owner = {{ add_country_modifier = {{ modifier = {mod} years = -1 mode = replace }} }}'''
            if loc:
                body += f'\nadd_location_modifier = {{ modifier = {loc} years = -1 mode = replace }}'
            out.append(block(f'{prefix}_{n}_grant_effect', body))
            sv = r['societal_value']
            settle = f"change_societal_value = {{ type = {sv['axis']} value = {sv['sign'] * sv['shock']} }}\n"
            settle += '\n'.join(reward_lines(r['one_shot'], 0))
            out.append(block(f'{prefix}_{n}_settle_effect', settle))
            preview = f'owner ?= {{ add_country_modifier = {{ modifier = {mod} years = -1 mode = replace }} }}'
            if loc:
                preview += f'\nadd_location_modifier = {{ modifier = {loc} years = -1 mode = replace }}'
            out.append(block(f'tv_wonder_display_{wid}_ritual_{n}_location_tooltip_effect', preview))
            # The encyclopedia has no active project/site. Render the same
            # native reward commands using the viewer's capital as the example
            # location, without writing project or dedication state.
            catalogue = f'add_country_modifier = {{ modifier = {mod} years = -1 mode = replace }}\n'
            catalogue += f'change_societal_value = {{ type = {sv["axis"]} value = {sv["sign"] * sv["shock"]} }}\n'
            local = f'add_location_modifier = {{ modifier = {loc} years = -1 mode = replace }}\n' if loc else ''
            local += '\n'.join(location_reward_lines(r['one_shot'], 0))
            if local.strip(): catalogue += 'capital ?= {\n' + local + '\n}'
            out.append(block(f'tv_wonder_display_{wid}_ritual_{n}_catalogue_effect', catalogue))
        out.append(block(f'{prefix}_sync_country_effect', '\n'.join(sync)))
        revoke = '\n'.join(f"remove_location_modifier = {r['location_modifier']}" for r in ritual_styles(w, mechanics) if r['location_modifier'])
        revoke += f'''\nremove_from_variable_map = {{ name = {STYLE_MAP} key = {wid} }}
remove_from_variable_map = {{ name = {MEMORY_MAP} key = {wid} }}
scope:tv_wonder_ritual_sync_country ?= {{ {prefix}_sync_country_effect = yes }}'''
        out.append(block(f'{prefix}_revoke_effect', revoke))
    out.append(block('tv_wonder_ritual_revoke_location_effect', '\n'.join(
        f"if = {{ limit = {{ {has_style(w)} }} tv_wonder_{w['key']}_ritual_revoke_effect = yes }}" for w in wonders)))
    return ''.join(out)


def phase_effects(wonders, mechanics):
    rules = ritual_rules(mechanics)
    out = []
    # Explicit style dispatch is also the actual completion effect shown by the GUI.
    for n in (1, 2, 3):
        body = []
        for index, w in enumerate(wonders):
            head = 'if' if index == 0 else 'else_if'
            body.append(f'''{head} = {{ limit = {{ var:tv_wonder_locked ?= {w['id']} }}
var:tv_wonder_site ?= {{ tv_wonder_{w['key']}_ritual_{n}_grant_effect = yes }}
tv_wonder_{w['key']}_ritual_{n}_settle_effect = yes
}}''')
        out.append(block(f'tv_wonder_ritual_apply_style_{n}_effect', '\n'.join(body)))
    out.append(block('tv_wonder_ritual_apply_choice_effect', '''if = {
limit = { NOT = { has_variable = tv_wonder_ritual_reward_claimed } }
if = { limit = { var:tv_wonder_finalization_outcome ?= 1 } tv_wonder_ritual_apply_style_1_effect = yes }
else_if = { limit = { var:tv_wonder_finalization_outcome ?= 2 } tv_wonder_ritual_apply_style_2_effect = yes }
else_if = { limit = { var:tv_wonder_finalization_outcome ?= 3 } tv_wonder_ritual_apply_style_3_effect = yes }
else_if = { limit = { var:tv_wonder_stage ?= 4 var:tv_wonder_ritual_choice ?= 1 } tv_wonder_ritual_apply_style_1_effect = yes }
else_if = { limit = { var:tv_wonder_stage ?= 4 var:tv_wonder_ritual_choice ?= 2 } tv_wonder_ritual_apply_style_2_effect = yes }
else_if = { limit = { var:tv_wonder_stage ?= 4 var:tv_wonder_ritual_choice ?= 3 } tv_wonder_ritual_apply_style_3_effect = yes }
if = { limit = { var:tv_wonder_project_mode ?= 3 } add_prestige = ''' + str(rules['reritual_prestige']) + ''' }
hidden_effect = { set_variable = { name = tv_wonder_ritual_reward_claimed value = 1 } }
}'''))
    # Cached axis position and reward badges are refreshed outside GUI render paths.
    cache, prefs = [], []
    axes = list(mechanics['societal_axes'])
    for w in wonders:
        rows = ritual_styles(w, mechanics)
        body = []
        for r in rows:
            n, sv = r['style'], r['societal_value']
            body += [f'set_variable = {{ name = tv_wonder_ritual_display_axis_{n} value = {axes.index(sv["axis"]) + 1} }}',
                     f'set_variable = {{ name = tv_wonder_ritual_reward_kind_{n} value = {int(bool(r["country_modifier"])) + 2 * int(bool(r["location_modifier"])) + 4 * int(bool(r["one_shot"]))} }}',
                     f'set_variable = {{ name = tv_wonder_ritual_display_dir_{n} value = {sv["sign"]} }}',
                     f'set_variable = {{ name = tv_wonder_ritual_position_{n} value = 0 }}',
                     f'set_variable = {{ name = tv_wonder_ritual_alignment_{n} value = 0 }}',
                     f'if = {{ limit = {{ has_societal_value = societal_value_type:{sv["axis"]} }} set_variable = {{ name = tv_wonder_ritual_position_{n} value = {{ value = societal_value:{sv["axis"]} divide = 100 }} }} set_variable = {{ name = tv_wonder_ritual_alignment_{n} value = {{ value = societal_value:{sv["axis"]} multiply = {sv["sign"]} divide = 100 }} }} }}']
        cache.append(f"if = {{ limit = {{ var:tv_wonder_locked ?= {w['id']} }}\n" + '\n'.join(body) + '\n}')
        body = []
        for estate, preference in rows[0]['estate_preferences'].items():
            var = f'tv_wonder_estate_pref_{estate}'
            set_pref = f'set_variable = {{ name = {var} value = {preference} }}' if preference != 'random' else 'random_list = { ' + ' '.join(f'1 = {{ set_variable = {{ name = {var} value = {n} }} }}' for n in (1, 2, 3)) + ' }'
            local_owner = estate == location_reward_estate(w) and any(r['location_modifier'] and r['style'] == preference for r in rows)
            source = 1 if local_owner else 3 if preference == 'random' else 2
            body.append(f'if = {{ limit = {{ country_has_estate = estate_type:{estate} }} {set_pref} set_variable = {{ name = tv_wonder_estate_pref_source_{estate} value = {source} }} }}')
        prefs.append(f"if = {{ limit = {{ var:tv_wonder_locked ?= {w['id']} }}\n" + '\n'.join(body) + '\n}')
    # Count the seven cached preferences once at lifecycle/preview refresh. No
    # location scans or live estate iteration occur on the GUI read path.
    counts = ['set_local_variable = { name = tv_ritual_estate_total value = 0 }']
    counts += [f'set_local_variable = {{ name = tv_ritual_support_{n} value = 0 }}' for n in (1, 2, 3)]
    for estate in ESTATES:
        counts.append(f'if = {{ limit = {{ has_variable = tv_wonder_estate_pref_{estate} }} change_local_variable = {{ name = tv_ritual_estate_total add = 1 }} }}')
        for n in (1, 2, 3):
            counts.append(f'if = {{ limit = {{ var:tv_wonder_estate_pref_{estate} ?= {n} }} change_local_variable = {{ name = tv_ritual_support_{n} add = 1 }} }}')
    for n in (1, 2, 3):
        counts += [f'set_variable = {{ name = tv_wonder_ritual_support_{n} value = {{ value = local_var:tv_ritual_support_{n} }} }}',
                   f'set_variable = {{ name = tv_wonder_ritual_oppose_{n} value = {{ value = local_var:tv_ritual_estate_total subtract = local_var:tv_ritual_support_{n} }} }}',
                   f'remove_local_variable = tv_ritual_support_{n}']
    counts.append('remove_local_variable = tv_ritual_estate_total')
    selected_cache = []
    for n in (1, 2, 3):
        copies = '\n'.join(f'set_variable = {{ name = tv_wonder_ritual_{field}_selected value = {{ value = var:tv_wonder_ritual_{field}_{n} }} }}'
                           for field in ('display_axis', 'display_dir', 'position'))
        selected_cache.append(f'if = {{ limit = {{ var:tv_wonder_ritual_choice ?= {n} has_variable = tv_wonder_ritual_display_axis_{n} }}\n{copies}\n}}')
    out.append(block('tv_wonder_ritual_refresh_display_effect', '\n'.join(cache + counts + selected_cache)))
    out.append(block('tv_wonder_ritual_roll_estates_effect', '\n'.join(f'remove_variable = tv_wonder_estate_pref_{e}' for e in ESTATES) + '\n' + '\n'.join(prefs)))
    for mode in ('choice', 'plain'):
        body = []
        for estate in ESTATES:
            var = f'tv_wonder_estate_pref_{estate}'
            penalty = f'add_estate_satisfaction = {{ type = estate_type:{estate} value = {rules["estate_satisfaction"]["oppose"]} }}'
            effect = penalty
            if mode == 'choice':
                effect = f'''if = {{ limit = {{ var:{var} ?= $style$ }} add_estate_satisfaction = {{ type = estate_type:{estate} value = {rules['estate_satisfaction']['support']} }} }}
else = {{ {penalty} }}'''
            body.append(f'if = {{ limit = {{ country_has_estate = estate_type:{estate} has_variable = {var} }}\n{effect}\n}}')
        name = 'tv_wonder_ritual_settle_estates_effect' if mode == 'choice' else 'tv_wonder_ritual_settle_estates_plain_effect'
        out.append(block(name, '\n'.join(body)))
    inherited = '\n'.join(f'''if = {{ limit = {{ var:tv_wonder_locked ?= {w['id']} var:tv_wonder_site ?= {{ {has_style(w)} }} }}
set_variable = {{ name = tv_wonder_finalization_outcome value = 9 }}
}}''' for w in wonders)
    out.append(block('tv_wonder_ritual_enter_phase_effect', f'''remove_variable = tv_wonder_ritual_choice
remove_variable = tv_wonder_finalization_outcome
remove_variable = tv_wonder_ritual_reward_claimed
set_variable = {{ name = tv_wonder_ritual_duration_months value = {rules['duration_months']} }}
set_variable = {{ name = tv_wonder_ritual_months_completed value = 0 }}
set_variable = {{ name = tv_wonder_ritual_progress_pct value = 0 }}
set_variable = {{ name = tv_wonder_ritual_ai_wait_months value = 0 }}
if = {{ limit = {{ var:tv_wonder_project_mode ?= 2 }}
{inherited}
}}
if = {{ limit = {{ var:tv_wonder_finalization_outcome ?= 9 }} tv_wonder_finalize_effect = yes }}
else = {{ tv_wonder_ritual_roll_estates_effect = yes tv_wonder_ritual_refresh_display_effect = yes }}'''))
    out.append(block('tv_wonder_ritual_preview_effect', '''if = { limit = { tv_wonder_ritual_can_preview_trigger = yes }
set_variable = { name = tv_wonder_ritual_choice value = $style$ }
tv_wonder_ritual_refresh_display_effect = yes
}'''))
    out.append(block('tv_wonder_ritual_confirm_effect', '''if = { limit = { tv_wonder_ritual_can_confirm_trigger = yes }
if = { limit = { NOT = { has_variable = tv_wonder_cmm_skip_ceremony } } tv_wonder_ritual_pay_effect = yes }
if = { limit = { var:tv_wonder_ritual_choice ?= 1 } tv_wonder_ritual_settle_estates_effect = { style = 1 } }
else_if = { limit = { var:tv_wonder_ritual_choice ?= 2 } tv_wonder_ritual_settle_estates_effect = { style = 2 } }
else_if = { limit = { var:tv_wonder_ritual_choice ?= 3 } tv_wonder_ritual_settle_estates_effect = { style = 3 } }
hidden_effect = {
set_variable = { name = tv_wonder_ritual_in_progress value = 1 }
if = { limit = { has_variable = tv_wonder_cmm_skip_ceremony } tv_wonder_ritual_complete_effect = yes }
}
}'''))
    pay = '\n'.join(f'if = {{ limit = {{ var:tv_wonder_locked_size ?= {n} }} pay_price = price:tv_wonder_ritual_{size}_price }}' for n, size in enumerate(('small','medium','large'),1))
    out.append(block('tv_wonder_ritual_pay_effect', pay))
    out.append(block('tv_wonder_ritual_choose_plain_effect', '''if = { limit = { tv_wonder_ritual_can_preview_trigger = yes NOT = { var:tv_wonder_project_mode ?= 3 } }
tv_wonder_ritual_settle_estates_plain_effect = yes
hidden_effect = {
set_variable = { name = tv_wonder_finalization_outcome value = 0 }
remove_variable = tv_wonder_ritual_choice
tv_wonder_finalize_effect = yes
}
}'''))
    out.append(block('tv_wonder_ritual_cancel_reritual_effect', '''if = { limit = { var:tv_wonder_project_mode ?= 3 var:tv_wonder_stage ?= 4 }
tv_wonder_clear_project_state_core_effect = yes
tv_wonder_start_concept_effect = { reason = 4 }
}'''))
    out.append(block('tv_wonder_ritual_monthly_effect', '''if = { limit = { var:tv_wonder_stage ?= 4 has_variable = tv_wonder_ritual_in_progress }
change_variable = { name = tv_wonder_ritual_months_completed add = 1 }
set_variable = { name = tv_wonder_ritual_progress_pct value = { value = var:tv_wonder_ritual_months_completed multiply = 100 divide = var:tv_wonder_ritual_duration_months } }
if = { limit = { var:tv_wonder_ritual_months_completed >= var:tv_wonder_ritual_duration_months } tv_wonder_ritual_complete_effect = yes }
}'''))
    finish = '\n'.join(f'if = {{ limit = {{ var:tv_wonder_locked ?= {w["id"]} }} trigger_event_non_silently = {{ id = tv_engineering_department.{4000+w["id"]} days = 1 }} }}' for w in wonders)
    out.append(block('tv_wonder_ritual_complete_effect', '''if = { limit = { var:tv_wonder_stage ?= 4 has_variable = tv_wonder_ritual_in_progress NOT = { has_variable = tv_wonder_ritual_completed } }
remove_variable = tv_wonder_ritual_in_progress
set_variable = { name = tv_wonder_ritual_completed value = 1 }
set_variable = { name = tv_wonder_ritual_months_completed value = var:tv_wonder_ritual_duration_months }
set_variable = { name = tv_wonder_ritual_progress_pct value = 100 }
set_variable = { name = tv_wonder_finalization_outcome value = var:tv_wonder_ritual_choice }
if = { limit = { var:tv_wonder_project_mode ?= 3 }
''' + finish + '''
}
else = { tv_wonder_finalize_effect = yes }
}'''))
    out.append(block('tv_wonder_ritual_clear_project_effect', '\n'.join(f'remove_variable = {v}' for v in [
        'tv_wonder_ritual_choice','tv_wonder_ritual_in_progress','tv_wonder_ritual_completed','tv_wonder_ritual_reward_claimed',
        'tv_wonder_finalization_outcome','tv_wonder_ritual_months_completed','tv_wonder_ritual_progress_pct','tv_wonder_ritual_duration_months','tv_wonder_ritual_ai_wait_months',
        *[f'tv_wonder_ritual_{field}_{n}' for field in ('display_axis', 'display_dir', 'position', 'alignment', 'reward_kind', 'support', 'oppose') for n in (1, 2, 3)],
        *[f'tv_wonder_ritual_{field}_selected' for field in ('display_axis', 'display_dir', 'position')],
        *[f'tv_wonder_estate_pref_{e}' for e in ESTATES], *[f'tv_wonder_estate_pref_source_{e}' for e in ESTATES]])))
    return ''.join(out)


def triggers(mechanics, wonders):
    out = block('tv_wonder_ritual_can_preview_trigger', '''var:tv_wonder_stage ?= 4
tv_wonder_construction_site_selected_trigger = yes
NOT = { has_variable = tv_wonder_ritual_in_progress }
NOT = { has_variable = tv_wonder_ritual_completed }
NOT = { has_variable = tv_wonder_finalized }''')
    afford = '\n'.join(f'AND = {{ var:tv_wonder_locked_size ?= {n} can_pay_price = price:tv_wonder_ritual_{size}_price }}' for n,size in enumerate(('small','medium','large'),1))
    out += block('tv_wonder_ritual_can_confirm_trigger', 'tv_wonder_ritual_can_preview_trigger = yes\nOR = { var:tv_wonder_ritual_choice ?= 1 var:tv_wonder_ritual_choice ?= 2 var:tv_wonder_ritual_choice ?= 3 }\nOR = { has_variable = tv_wonder_cmm_skip_ceremony\n' + afford + '\n}')
    out += block('tv_wonder_ritual_outcome_ready_trigger', '''var:tv_wonder_stage ?= 4
OR = { var:tv_wonder_finalization_outcome ?= 0 var:tv_wonder_finalization_outcome ?= 9 has_variable = tv_wonder_ritual_completed }''')
    out += block('tv_wonder_current_site_is_shell_trigger', 'OR = {\n' + '\n'.join(f'AND = {{ var:tv_wonder_locked ?= {w["id"]} var:tv_wonder_site ?= {{ has_building = building_type:tv_wonder_{w["key"]} NOT = {{ has_building = building_type:{w["final_building"]} }} }} }}' for w in wonders) + '\n}')
    return out


def actions():
    rows = [(f'tv_wonder_ritual_preview_{n}', 'tv_wonder_ritual_can_preview_trigger = yes', f'hidden_effect = {{ tv_wonder_ritual_preview_effect = {{ style = {n} }} }}') for n in (1,2,3)]
    rows += [('tv_wonder_ritual_preview_plain', 'tv_wonder_ritual_can_preview_trigger = yes NOT = { var:tv_wonder_project_mode ?= 3 }', 'hidden_effect = { tv_wonder_ritual_preview_effect = { style = 0 } }'),
             ('tv_wonder_ritual_confirm','tv_wonder_ritual_can_confirm_trigger = yes','tv_wonder_ritual_confirm_effect = yes'),
             ('tv_wonder_ritual_choose_plain','tv_wonder_ritual_can_preview_trigger = yes NOT = { var:tv_wonder_project_mode ?= 3 }','tv_wonder_ritual_choose_plain_effect = yes'),
             ('tv_wonder_ritual_cancel_reritual','var:tv_wonder_project_mode ?= 3 tv_wonder_ritual_can_preview_trigger = yes','hidden_effect = { tv_wonder_ritual_cancel_reritual_effect = yes }')]
    return ''.join(block(name, f'''type = owncountry
potential = {{ scope:actor = {{ has_variable = tv_engineering_department_member }} }}
allow = {{ scope:actor = {{ {allow} }} }}
effect = {{ scope:actor = {{ {effect} }} }}
ai_tick = monthly
ai_tick_frequency = 99999
ai_will_do = {{ add = -100 }}''') for name,allow,effect in rows)


def reritual_effects(wonders, mechanics):
    body = ['save_scope_as = tv_wonder_reritual_owner', 'remove_variable = tv_wonder_reritual_found']
    for w in wonders:
        valid = f'has_building = building_type:{w["final_building"]} NOT = {{ {has_style(w)} }}'
        level_capture = '\n'.join(
            f'{"if" if level == 6 else "else_if"} = {{ limit = {{ location_building_level = {{ building_type = building_type:{w["final_building"]} value >= {level} }} }} scope:tv_wonder_reritual_owner = {{ set_variable = {{ name = tv_wonder_level value = {level} }} set_variable = {{ name = tv_wonder_project_base_level value = {level} }} }} }}'
            for level in range(6, 0, -1)
        )
        lock = f'''save_scope_as = tv_wonder_reritual_site
{level_capture}
scope:tv_wonder_reritual_owner = {{
set_variable = {{ name = tv_wonder_reritual_found value = 1 }}
set_variable = {{ name = tv_wonder_locked value = {w['id']} }}
set_variable = {{ name = tv_wonder_site value = scope:tv_wonder_reritual_site }}
set_variable = {{ name = tv_wonder_project_mode value = 3 }}
set_variable = {{ name = tv_wonder_construction_complete value = 1 }}
set_variable = {{ name = tv_wonder_stage value = 4 }}
remove_variable = tv_wonder_concept_in_progress
remove_variable = tv_wonder_cmm_skip_ceremony
if = {{ limit = {{ is_ai = no has_global_variable = tv_engineering_department_skip_ceremony }} set_variable = {{ name = tv_wonder_cmm_skip_ceremony value = 1 }} }}
tv_wonder_index_refresh_country_cache_effect = yes
tv_wonder_ritual_enter_phase_effect = yes
}}'''
        if w.get('is_unique'):
            find = f'location:{w["location"]} = {{ if = {{ limit = {{ owner ?= scope:tv_wonder_reritual_owner {valid} }}\n{lock}\n}} }}'
        else:
            # max = 1 is safe even when a stale cache has no remaining candidates.
            order = ' '.join(f'if = {{ limit = {{ location_building_level = {{ building_type = building_type:{w["final_building"]} value >= {level} }} }} add = 1 }}' for level in range(1,7))
            find = f'''ordered_owned_location = {{
limit = {{ {valid} }}
order_by = {{ value = 0 {order} }}
max = 1
check_range_bounds = no
{lock}
}}'''
        body.append(f'if = {{ limit = {{ var:tv_wonder_reritual_pending_id ?= {w["id"]} }}\n{find}\n}}')
    body.append('''if = { limit = { NOT = { has_variable = tv_wonder_reritual_found } }
remove_from_variable_map = { name = tv_wonder_plain_level_by_wonder_id key = var:tv_wonder_reritual_pending_id }
trigger_event_non_silently = { id = tv_engineering_department.2003 days = 1 }
}
remove_variable = tv_wonder_reritual_found''')
    out = block('tv_wonder_reritual_lock_effect', 'if = { limit = { var:tv_wonder_stage ?= 0 has_variable = tv_wonder_concept_in_progress has_variable = tv_wonder_reritual_pending_id }\n' + '\n'.join(body) + '\n}\nremove_variable = tv_wonder_reritual_pending_id')
    out += block('tv_wonder_reritual_finish_effect', '''if = { limit = { var:tv_wonder_project_mode ?= 3 has_variable = tv_wonder_ritual_reward_claimed }
var:tv_wonder_site ?= { tv_wonder_mechanics_refresh_location_display_state_effect = yes }
tv_wonder_clear_project_state_core_effect = yes
tv_wonder_start_concept_effect = { reason = 4 }
}''')
    return out


def lifecycle_events(wonders, mechanics):
    out = ['namespace = tv_engineering_department\n\n']
    choices = []
    for w in wonders:
        choices.append(block('option', f'''name = tv_wonder_reritual_option_{w['id']}
trigger = {{ {variable_map_key_trigger('tv_wonder_plain_level_by_wonder_id', w['id'])} }}
custom_tooltip = TV_WONDER_RERITUAL_LOCK_TT
hidden_effect = {{
set_variable = {{ name = tv_wonder_reritual_pending_id value = {w['id']} }}
trigger_event_silently = {{ id = tv_engineering_department.2002 days = 0 }}
}}'''))
    out.append(block('tv_engineering_department.2001', '''type = country_event
title = TV_WONDER_RERITUAL_TITLE
desc = TV_WONDER_RERITUAL_DESC
outcome = neutral
''' + ''.join(choices) + 'option = { name = TV_WONDER_RERITUAL_LATER }'))
    out.append(block('tv_engineering_department.2002', 'type = country_event\ntitle = empty_text\ndesc = empty_text\nhidden = yes\nimmediate = { tv_wonder_reritual_lock_effect = yes }'))
    out.append(block('tv_engineering_department.2003', 'type = country_event\ntitle = TV_WONDER_RERITUAL_TITLE\ndesc = TV_WONDER_RERITUAL_STALE\noutcome = neutral\noption = { name = TV_WONDER_RITUAL_ACK }'))
    out.append(block('tv_engineering_department.2010', 'type = country_event\ntitle = TV_WONDER_RITUAL_FORGOTTEN_TITLE\ndesc = TV_WONDER_RITUAL_FORGOTTEN_DESC\noutcome = neutral\noption = { name = TV_WONDER_RITUAL_ACK }'))
    out.append(block('tv_engineering_department.2004', 'type = country_event\ntitle = empty_text\ndesc = empty_text\nhidden = yes\nimmediate = { tv_wonder_reritual_finish_effect = yes }'))
    for w in wonders:
        wid = w['id']
        out.append(block(f'tv_engineering_department.{3000+wid}', f'''type = location_event
title = empty_text
desc = empty_text
hidden = yes
immediate = {{
if = {{ limit = {{ {has_style(w)} NOT = {{ {variable_map_key_trigger(MEMORY_MAP, wid)} }} }}
save_scope_as = tv_wonder_forgotten_site
save_scope_value_as = {{ name = tv_wonder_forgotten_id value = {wid} }}
set_local_variable = {{ name = tv_wonder_forgotten_style_value value = "variable_map({STYLE_MAP}|{wid})" }}
save_scope_value_as = {{ name = tv_wonder_forgotten_style value = local_var:tv_wonder_forgotten_style_value }}
remove_local_variable = tv_wonder_forgotten_style_value
clear_saved_scope = tv_wonder_ritual_sync_country
owner ?= {{
save_scope_as = tv_wonder_ritual_sync_country
}}
tv_wonder_{w['key']}_ritual_revoke_effect = yes
tv_wonder_mechanics_refresh_location_display_state_effect = yes
{forgotten_plain_cache(w)}
owner ?= {{
trigger_event_non_silently = {{ id = tv_engineering_department.2010 days = 1 }}
}}
}}
}}'''))
        out.append(block(f'tv_engineering_department.{4000+wid}', f'''type = country_event
title = TV_WONDER_RERITUAL_COMPLETE_TITLE
desc = TV_WONDER_RERITUAL_COMPLETE_DESC
outcome = positive
option = {{ name = TV_WONDER_RITUAL_ACK
if = {{ limit = {{ var:tv_wonder_locked ?= {wid} var:tv_wonder_project_mode ?= 3 has_variable = tv_wonder_ritual_completed var:tv_wonder_site ?= {{ owner ?= root has_building = building_type:{w['final_building']} NOT = {{ {has_style(w)} }} }} }}
tv_wonder_ritual_apply_choice_effect = yes
hidden_effect = {{ trigger_event_silently = tv_engineering_department.2004 }}
}}
}}'''))
    return ''.join(out)


def prices(mechanics):
    return ''.join(block(f'tv_wonder_ritual_{size}_price', f'scaled_gold = {value}') for size,value in ritual_rules(mechanics)['cost']['value'].items())


def message_localization(language, localization):
    actions = [*[f'tv_wonder_ritual_preview_{n}' for n in (1, 2, 3)], 'tv_wonder_ritual_preview_plain', 'tv_wonder_ritual_confirm', 'tv_wonder_ritual_choose_plain', 'tv_wonder_ritual_cancel_reritual']
    # Non-primary languages use the authored English text. Their old action-key
    # aliases had no local target and could display raw ids in notifications.
    labels = localization['simp_chinese' if language == 'simp_chinese' else 'english']
    header = '\n'.join(' ' + line for line in render_header('scripts_engineering_department/in_game/common/scripted_effects/gen_tv_wonder_ritual_state_effects.py', 'data/wonder_generic_rituals.yaml + data/wonder_localization.yaml'))
    lines = [f'l_{language}:', header]
    lines.extend(loc_line(f'PERFORM_{action}_ACTION_{suffix}', labels[action])
                 for action in actions for suffix in ('HEADER', 'TITLE', 'SETUP', 'LOG', 'MAP'))
    return '\n'.join(line.rstrip() for line in lines).rstrip() + '\n'
