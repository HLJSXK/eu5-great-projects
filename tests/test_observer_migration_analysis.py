from scripts.analyze_observer_migration import has_migration_right, population_flows


def test_only_current_exact_privilege_counts():
    country = b'\tgovernment={\n\t\timplemented_privileges={ { object=peasants_free_peasantry }}\n\t}\n'
    assert has_migration_right(country)
    assert not has_migration_right(country.replace(b'object=peasants_free_peasantry', b'object=peasants_free_peasantry_expired'))
    assert not has_migration_right(b'\thistory={ object=peasants_free_peasantry }\n')


def test_compact_list_end_excludes_other_objects():
    country = b'\tgovernment={\n\t\timplemented_privileges={ { object=communal_lands }}\n\t\tother={ object=peasants_free_peasantry }\n\t}\n'
    assert not has_migration_right(country)


def test_migration_is_separate_from_growth_and_social_mobility():
    pop = b'\t\t\t\t\tpeasants={\n\t\t\t\t\t\tpopulation_ratio=999\n\t\t\t\t\t\tunemployed=2\n\t\t\t\t\t\tchanges={\n\t\t\t\t\t\t\tMigrationIn=1.5\n\t\t\t\t\t\t\tMigrationOut=-0.25\n\t\t\t\t\t\t\tPromotionOut=-0.6\n\t\t\t\t\t\t\tReproduction=0.1\n\t\t\t\t\t\t}\n\t\t\t\t\t}\n'
    row = population_flows(pop)
    assert row['peasants_MigrationIn'] == 1.5
    assert row['peasants_MigrationOut'] == -0.25
    assert row['peasants_Reproduction'] == 0.1
    assert row['peasants_PromotionOut'] == -0.6
    assert row['peasants_unemployed'] == 2
    assert row['laborers_MigrationIn'] == 0
    assert 'peasants_size' not in row
