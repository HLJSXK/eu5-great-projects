"""Save-format checks for the observer audit; no engine simulation."""
from scripts.analyze_observer_saves import REC, LOC, values, scalar, block, array, building_category


def test_scope_references_are_not_fixed_point_values():
    raw = b'flag=tv_wonder_site\n data={ type=loc location=24698 } flag=tv_wonder_level data={ type=value identity=200000 }'
    assert values(raw) == {'tv_wonder_site': 24698, 'tv_wonder_level': 2}


def test_signed_fixed_point_and_omitted_zero():
    raw = f'flag=loss data={{ type=value identity={(1 << 64) - 125000} }} flag=zero data={{ type=value }}'.encode()
    assert values(raw) == {'loss': -1.25, 'zero': 0}


def test_nested_fields_do_not_replace_owner_or_expenses():
    raw = b'\towner=3\n\tdata={\n\t\towner=4\n\t}\n\teconomy={\n\t\tincome=10\n\t\texpense=13\n\t\trecent_balance={ 2 1 -3 }\n\t}\n'
    assert scalar(raw, 'owner') == 3
    econ = block(raw, 'economy')
    assert array(econ, 'recent_balance')[-1] == -3
    assert scalar(econ, 'income', 2) - scalar(econ, 'expense', 2) == -3


def test_record_boundaries_and_deleted_ids():
    raw = b'0=none\n1={\n\ttype=x\n\tfoo={\n\t\tid=4\n\t}\n}\n2={\n\ttype=y\n}\n'
    records = list(REC.finditer(raw))
    assert [int(r[1]) for r in records] == [1, 2]
    assert [scalar(r[2], 'type') for r in records] == ['x', 'y']


def test_location_indentation_and_explicit_close():
    raw = b'\t\t13={\n\t\t\towner=3\n\t\t}\n\t\t14={\n\t\t\towner=4\n\t\t}\n'
    assert [scalar(r[2], 'owner', 3) for r in LOC.finditer(raw)] == [3, 4]
    assert scalar(b'\tlevel=1\n', 'open', default='omitted') == 'omitted'
    assert scalar(b'\topen=no\n', 'open', default='omitted') == 'no'


def test_shared_old_maintenance_is_not_a_building_category():
    pm = 'tv_wonder_module_maintenance'
    assert building_category('tv_wonder_university_city', pm, set()) == 'shell'
    assert building_category('tv_wonder_university_city_foundation', pm, set()) == 'module'
    assert building_category('tv_wonder_finished', pm, {'tv_wonder_finished'}) == 'final'
