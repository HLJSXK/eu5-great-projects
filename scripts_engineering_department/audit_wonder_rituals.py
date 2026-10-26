"""Static contract audit for the unified ritual system (not an engine test)."""
from collections import Counter
from pathlib import Path
import re

from wonder_mechanics.io import load_all_wonder_mechanics
from wonder_mechanics.rituals import ritual_styles

ROOT = Path(__file__).resolve().parents[1]


def audit():
    wonders, mechanics = load_all_wonder_mechanics()
    assert len(wonders) == 195
    by_key = {w['key']: w for w in wonders}
    assert len({w['final_building'] for w in wonders}) == len(wonders)
    counts = Counter()
    for wonder in wonders:
        rows = ritual_styles(wonder, mechanics)
        assert [r['style'] for r in rows] == [1, 2, 3]
        assert not {'ritual', 'ceremony', 'final_buildings'} & wonder.keys()
        for row in rows:
            counts['country'] += 1
            counts['location'] += bool(row['location_modifier'])
            sv = row['societal_value']
            counts['age_direction' if mechanics['societal_axes'][sv['axis']]['age'] else 'other_direction'] += not wonder['is_unique']
            counts['conditional_direction'] += not wonder['is_unique'] and mechanics['societal_axes'][sv['axis']]['conditional']
            assert row['country_modifier'][f"monthly_towards_{sv['direction']}"] == 0.1
            assert sv['shock'] == 20
            if wonder['is_unique']:
                inherited = ritual_styles(by_key[wonder['mechanic_key']], mechanics)[row['style'] - 1]
                for field in ('country_modifier', 'location_modifier_values', 'one_shot', 'societal_value', 'estate_preferences'):
                    assert row[field] == inherited[field], (wonder['key'], field)
                assert row['modifier'] != inherited['modifier']
    assert counts['country'] == 585 and counts['location'] == 195
    all_events = '\n'.join(p.read_text(encoding='utf-8-sig') for p in (ROOT/'src/in_game/events').glob('*.txt'))
    ids = re.findall(r'(?m)^tv_engineering_department\.(\d+)\s*=\s*\{', all_events)
    assert len(ids) == len(set(ids)), 'duplicate event IDs'
    assert not any(str(n) in ids for n in [*range(9300, 9308), *range(6301, 6309), *range(7300, 7309)])
    for wonder in wonders:
        assert str(3000 + wonder['id']) in ids
        assert str(4000 + wonder['id']) in ids
    assert all(not any(k.startswith('monthly_towards_') for k in values) for values in mechanics['base_modifiers'].values())
    print(f"[OK] Unified rituals: {len(wonders)} final buildings, {counts['country']} country modifiers, {counts['location']} location modifiers; age/other directions {counts['age_direction']}/{counts['other_direction']} ({counts['conditional_direction']} conditional).")


if __name__ == '__main__':
    audit()
