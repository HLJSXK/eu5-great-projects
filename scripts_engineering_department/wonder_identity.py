"""Identity presentation shared by ED generators; vanilla globals are authoritative."""
from functools import lru_cache


@lru_cache(maxsize=1)
def identity_wonders():
    if __package__:
        from .wonder_mechanics.io import load_all_wonder_mechanics
    else:
        from wonder_mechanics.io import load_all_wonder_mechanics
    return load_all_wonder_mechanics()[0]


def variants(wonders):
    return ((w, v) for w in wonders for v in w.get('identity_variants', []))


def active(v):
    return f"GetGlobalVariable('{v['global_variable']}').IsSet"


def image_expression(wonders, id_expression, default, *, cropped=False):
    expression = default
    if wonders is None:
        wonders = identity_wonders()
    for w, v in reversed(list(variants(wonders))):
        suffix = 'image' if cropped else 'full_image'
        concept = f"tv_wonder_identity_{suffix}_{w['id']}_{v['key']}"
        condition = active(v)
        if id_expression:
            condition = f"And(EqualTo_CFixedPoint({id_expression}, '(CFixedPoint){w['id']}.0'), {condition})"
        expression = f"Select_CString({condition}, '{concept}', {expression})"
    return f"GetConceptTexture({expression})"


def apply_localization(localization, wonders, mechanics, ritual_styles):
    for w in wonders:
        identities = w.get('identity_variants', [])
        if not identities:
            continue
        for language, values in localization.items():
            suffix = 'zh' if language == 'simp_chinese' else 'en'
            replacements = {}
            name_keys = [w['concept'], f"game_concept_{w['concept']}"]
            desc_keys = [f"game_concept_{w['concept']}_desc", f"{w['concept']}_desc"]
            for prefix in ('tv_wonder_display_', 'tv_wonder_display_image_', 'tv_wonder_display_full_image_'):
                name_keys.append(f"game_concept_{prefix}{w['id']}")
                desc_keys.append(f"game_concept_{prefix}{w['id']}_desc")
            # The final building retains its static, shared historical name.
            desc_keys.append(f"{w['final_building']}_desc")
            desc_keys.append(f"tv_engineering_department.500.d_{w['key']}")
            for v in identities:
                for image_kind in ('image', 'full_image'):
                    image_key = f"game_concept_tv_wonder_identity_{image_kind}_{w['id']}_{v['key']}"
                    values[image_key] = v[f'name_{suffix}']
                    values[image_key + '_desc'] = v[f'desc_{suffix}']
                for key in name_keys:
                    replacements.setdefault(key, []).append((v, v[f'name_{suffix}']))
                for key in desc_keys:
                    replacements.setdefault(key, []).append((v, v[f'desc_{suffix}']))
                decision = f"tv_wonder_{w['key']}_{v['key']}_decision"
                values[decision] = v[f'decision_{suffix}']
                values[decision + '_desc'] = v[f'decision_desc_{suffix}']
                values[decision + '.a'] = v[f'decision_{suffix}']
                for row in ritual_styles(w, mechanics):
                    n = row['style']
                    flavor = v['ritual_text'][n]
                    names = [f"TV_WONDER_RITUAL_NAME_{n}_{w['id']}", row['name_key'], f"STATIC_MODIFIER_NAME_{row['modifier']}"]
                    descriptions = [f"TV_WONDER_RITUAL_DESC_{n}_{w['id']}", row['desc_key'], row['final_desc_key']]
                    if row['location_modifier']:
                        names.append(f"STATIC_MODIFIER_NAME_{row['location_modifier']}")
                    for key in dict.fromkeys(names):
                        replacements.setdefault(key, []).append((v, flavor[f'name_{suffix}']))
                    for key in dict.fromkeys(descriptions):
                        replacements.setdefault(key, []).append((v, flavor[f'desc_{suffix}']))
                plain = f"tv_engineering_department.500.d_{w['key']}_plain"
                replacements.setdefault(plain, []).append((v, v[f'desc_{suffix}']))
            for key, choices in replacements.items():
                base_key = key + '_identity_default'
                values[base_key] = values[key]
                expression = f"Localize('{base_key}')"
                for v, text in reversed(choices):
                    variant_key = key + '_identity_' + v['key']
                    values[variant_key] = text
                    expression = f"SelectLocalization({active(v)}, '{variant_key}', '{base_key}')" if len(choices) == 1 else f"Select_CString({active(v)}, Localize('{variant_key}'), {expression})"
                values[key] = '[' + expression + ']'
            prefs_key = f"TV_WONDER_RITUAL_ESTATE_PREFS_{w['id']}"
            for n in (1, 2, 3):
                values[prefs_key] = values[prefs_key].replace(w['ritual_text'][n][f'name_{suffix}'], f"[Localize('TV_WONDER_RITUAL_NAME_{n}_{w['id']}')]")


def collapse_localization(localization, wonders):
    """Restore authored church text before the editor writes canonical YAML."""
    for values in localization.values():
        for key in list(values):
            if key.endswith('_identity_default'):
                values[key.removesuffix('_identity_default')] = values[key]
        for w, v in variants(wonders):
            decision = f"tv_wonder_{w['key']}_{v['key']}_decision"
            for key in list(values):
                if key.endswith(('_identity_default', '_identity_' + v['key'])) or key.startswith(decision):
                    values.pop(key)
            for kind in ('image', 'full_image'):
                key = f"game_concept_tv_wonder_identity_{kind}_{w['id']}_{v['key']}"
                values.pop(key, None)
                values.pop(key + '_desc', None)
