# ED：候选建筑、艺术品类型与开局实体

入口：[扫描总览](ED_Vanilla_Wonder_Construction_Audit.md)。此表保留独有/事件建筑与建筑语义候选，不把文件名 `unique_buildings` 等同于“世界唯一奇观”。普通地域建筑、军营、官署也保留为低置信度边界项。

## 候选建筑定义与控制入口

共 **270 种建筑**。`always = no` 通常表示常规入口被关闭，应继续查看事件/效果；本表不把它推断为“绝对无法建造”。空条件不等同于引擎没有额外规则。

### ablaq_palace — 阿卜拉克宫殿

原版定义：[in_game/common/building_types/event_only_buildings.txt:1713](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/event_only_buildings.txt:1713>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 5`
- `build_time = generic_event_building`
- `country_potential = { custom_tooltip = { text = unlocked_ablaq_palace_tt has_variable = enable_ablaq_palace_variable } }`
- `location_potential = { counts_as_capital = yes this = location:cairo }`
- `allow = { is_capital = yes }`
- `custom_tags = { unique_palace }`

行为或条件引用：

- [mam_ablaq_palace_decision](ED_Vanilla_Wonder_Construction_Actions.md#mam_ablaq_palace_decision-1622-a14531)：开罗的宏伟宫殿；construct_building；[in_game/common/decisions/flavor_decisions_various.txt:1622](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/decisions/flavor_decisions_various.txt:1622>)。

### academy_of_sciences — 彼得堡科学院

原版定义：[in_game/common/building_types/unique_buildings.txt:3551](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:3551>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `country_potential = { custom_tooltip = { text = academy_of_sciences_why OR = { tag = MOS tag = RUS } has_variable = academy_of_sciences } }`
- `allow = { always = no }`
- `build_time = cultural_building_time`
- `location_potential = { this = location:neva }`

行为或条件引用：

- [rus_academy_of_sciences_decision](ED_Vanilla_Wonder_Construction_Actions.md#rus_academy_of_sciences_decision-1693-f996cd)：科学院；construct_building；[in_game/common/decisions/flavor_decisions_rus.txt:1693](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/decisions/flavor_decisions_rus.txt:1693>)。
- [flavor_rus.46](ED_Vanilla_Wonder_Construction_Actions.md#flavor_rus-46-3616-201f60)：莫斯科公报的意识形态编辑；construct_building；[in_game/events/DHE/flavor_RUS.txt:3616](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_RUS.txt:3616>)。
- `flavor_rus.47`：[mikhail_speransky.GetNameWithNoTooltip]；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_RUS.txt:3704](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_RUS.txt:3704>)。
- [flavor_rus.70](ED_Vanilla_Wonder_Construction_Actions.md#flavor_rus-70-6009-201f60)：[yury_felten.GetNameWithNoTooltip]的精心改进；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_RUS.txt:6009](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_RUS.txt:6009>)。

### adm_vatican_library — 梵蒂冈图书馆：行政侧

原版定义：[in_game/common/building_types/event_only_buildings.txt:1088](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/event_only_buildings.txt:1088>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `build_time = large_cultural_building_time`
- `country_potential = { always = no }`

行为或条件引用：

- [flavor_pap.13](ED_Vanilla_Wonder_Construction_Actions.md#flavor_pap-13-661-09eb6b)：梵蒂冈图书馆；change_building_level_in_location；[in_game/events/DHE/flavor_pap.txt:661](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_pap.txt:661>)。

### adu_jewish_community — 犹太区

原版定义：[in_game/common/building_types/event_only_buildings.txt:4490](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/event_only_buildings.txt:4490>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `build_time = large_cultural_building_time`
- `country_potential = { has_unlocked_building_trigger = { type = adu_jewish_community } }`
- `allow = { "religion_percentage(religion:judaism)" > 0 }`
- `remove_if = { location = { "religion_percentage(religion:judaism)" = 0 } }`

行为或条件引用：

- [flavor_gra.9](ED_Vanilla_Wonder_Construction_Actions.md#flavor_gra-9-365-afe809)：塞法迪犹太人；construct_building, unlock_building_effect；[in_game/events/DHE/flavor_gra.txt:365](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_gra.txt:365>)。

### al_azhar_madrasa — 爱资哈尔大学

原版定义：[in_game/common/building_types/event_only_buildings.txt:2932](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/event_only_buildings.txt:2932>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `build_time = large_cultural_building_time`
- `country_potential = { always = no }`
- `allow = { always = no }`
- `remove_if = { location = { owner ?= { religion.group != religion_group:muslim } } }`

行为或条件引用：

- [flavor_mam.41](ED_Vanilla_Wonder_Construction_Actions.md#flavor_mam-41-2315-3a1e35)：爱资哈尔大学；construct_building；[in_game/events/DHE/flavor_MAM.txt:2315](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_MAM.txt:2315>)。

### al_qaysariyya_market — 盖萨里耶巴扎

原版定义：[in_game/common/building_types/unique_buildings.txt:6347](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:6347>)。

- `is_foreign = no`
- `max_levels = 1`
- `build_time = market_build_time`
- `country_potential = { has_unlocked_building_trigger = { type = al_qaysariyya_market } }`
- `location_potential = { this = location:granada }`

行为或条件引用：

- [flavor_gra.20](ED_Vanilla_Wonder_Construction_Actions.md#flavor_gra-20-1212-afe809)：格拉纳达市场的繁荣；construct_building, unlock_building_effect；[in_game/events/DHE/flavor_gra.txt:1212](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_gra.txt:1212>)。

### alhambra — 阿尔罕布拉宫

原版定义：[in_game/common/building_types/unique_buildings.txt:4156](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:4156>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = alhambra_max_level`
- `build_time = large_capital_build_time`
- `country_potential = { OR = { has_or_had_tag = GRA culture = culture:andalusi } }`
- `location_potential = { counts_as_capital = yes }`
- `allow = { is_capital = yes country_has_no_other_copy_of_building = { type = alhambra } }`

行为或条件引用：

- `flavor_gra.14`：幸园宫；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_gra.txt:743](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_gra.txt:743>)。

1337 开局实例：`granada`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2006](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2006>)。

### ambras_castle — 安布拉斯城堡

原版定义：[in_game/common/building_types/event_only_buildings.txt:3150](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/event_only_buildings.txt:3150>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `country_potential = { has_variable = unlocked_ambras_castle }`
- `allow = { always = no }`
- `build_time = large_cultural_building_time`

行为或条件引用：

- [flavor_hab.41](ED_Vanilla_Wonder_Construction_Actions.md#flavor_hab-41-2285-a07f59)：安布拉斯城堡；construct_building；[in_game/events/DHE/flavor_HAB.txt:2285](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_HAB.txt:2285>)。

### amsterdam_admiralty — 阿姆斯特丹海军部

原版定义：[in_game/common/building_types/event_only_buildings.txt:2027](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/event_only_buildings.txt:2027>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `build_time = large_port_building_time`
- `country_potential = { always = no }`
- `location_potential = { this = location:amsterdam is_capital = no }`

行为或条件引用：

- [ned_unified_dutch_admiralties_decision](ED_Vanilla_Wonder_Construction_Actions.md#ned_unified_dutch_admiralties_decision-2096-a14531)：建立五大海军部；construct_building；[in_game/common/decisions/flavor_decisions_various.txt:2096](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/decisions/flavor_decisions_various.txt:2096>)。

### aqueduct_system — 引水系统

原版定义：[in_game/common/building_types/town_buildings.txt:622](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/town_buildings.txt:622>)。

- `is_foreign = no`
- `max_levels = aqueduct_system_max_level`
- `build_time = infrastructure_build_time`
- `country_potential = { OR = { tag = BYZ tag = ROM owns = location:constantinople owns = location:rome owns = location:avignon owns = location:segovia } }`
- `location_potential = { OR = { this = location:constantinople this = location:rome this = location:avignon this = location:segovia } }`

行为或条件引用：

- [aqueduct_system](ED_Vanilla_Wonder_Construction_Actions.md#aqueduct_system-183-38a6e9)：引水系统；unlock_building；[in_game/common/advances/0_age_of_traditions.txt:183](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/advances/0_age_of_traditions.txt:183>)。
- [flavor_tur.92](ED_Vanilla_Wonder_Construction_Actions.md#flavor_tur-92-6330-bf9554)：[mimar_sinan.GetNameWithNoTooltip]的伟大杰作；construct_building；[in_game/events/DHE/flavor_TUR.txt:6330](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_TUR.txt:6330>)。

1337 开局实例：`constantinople`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:4513](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:4513>)；`rome`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:4514](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:4514>)；`avignon`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:4515](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:4515>)；`segovia`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:4516](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:4516>)。

### archive_of_the_indies — 西印度档案馆

原版定义：[in_game/common/building_types/event_only_buildings.txt:1338](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/event_only_buildings.txt:1338>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `country_potential = { OR = { has_or_had_tag = CAS has_or_had_tag = SPA } has_unlocked_building_trigger = { type = archive_of_the_indies } }`
- `allow = { custom_tooltip = { text = archive_of_the_indies_why always = no } }`
- `build_time = government_build_time`

行为或条件引用：

- [flavor_cas.1503](ED_Vanilla_Wonder_Construction_Actions.md#flavor_cas-1503-11191-9abc78)：西印度档案馆；construct_building, unlock_building_effect；[in_game/events/DHE/flavor_CAS.txt:11191](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_CAS.txt:11191>)。

### arts_academy — 美术学院

原版定义：[in_game/common/building_types/culture_buildings.txt:395](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/culture_buildings.txt:395>)。

- `is_foreign = no`
- `max_levels = 1`
- `obsolete = art_school`
- `build_time = large_cultural_building_time`
- `location_potential = { counts_as_capital = yes }`
- `allow = { is_capital = yes country_has_no_other_copy_of_building = { type = arts_academy } }`
- `remove_if = { is_no_longer_capital = yes }`
- `country_potential = { }`

行为或条件引用：

- [arts_academy_advance](ED_Vanilla_Wonder_Construction_Actions.md#arts_academy_advance-1181-3be8a5)：美术学院；unlock_building；[in_game/common/advances/1_building_unlocks.txt:1181](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/advances/1_building_unlocks.txt:1181>)。
- [eng_royal_academy_of_arts_decision](ED_Vanilla_Wonder_Construction_Actions.md#eng_royal_academy_of_arts_decision-915-b67bf8)：皇家艺术学会；门槛/关联引用；需看上下文；[in_game/common/decisions/flavor_decisions_eng.txt:915](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/decisions/flavor_decisions_eng.txt:915>)。
- [estate_cooperation](ED_Vanilla_Wonder_Construction_Actions.md#estate_cooperation-1-821312)：阶层合作；门槛/关联引用；需看上下文；[in_game/common/missions/generic_estate_cooperation_mission_pack.txt:1](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/missions/generic_estate_cooperation_mission_pack.txt:1>)。
- `artist_events.15`：雕塑艺术区；门槛/关联引用；需看上下文；[in_game/events/character/artist_events.txt:973](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/character/artist_events.txt:973>)。
- [artist_events.23](ED_Vanilla_Wonder_Construction_Actions.md#artist_events-23-1373-29e721)：[ShowInstitutionNameWithNoTooltip('renaissance')\|U]艺术的繁荣；construct_building；[in_game/events/character/artist_events.txt:1373](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/character/artist_events.txt:1373>)。
- `cultural_event.6`：特许成立$STATIC_MODIFIER_NAME_guild_of_st_luke$；门槛/关联引用；需看上下文；[in_game/events/culture/cultural_event.txt:149](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/culture/cultural_event.txt:149>)。
- [flavor_byz.13](ED_Vanilla_Wonder_Construction_Actions.md#flavor_byz-13-883-64397c)：光荣的学术中心；construct_building；[in_game/events/DHE/flavor_BYZ.txt:883](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_BYZ.txt:883>)。
- `flavor_byz.42`：flavor_byz.42；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_BYZ.txt:3178](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_BYZ.txt:3178>)。
- `flavor_flo.29`：第一位现代工程师；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_flo.txt:516](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_flo.txt:516>)。
- `flavor_flo.30`：一位伟大的意大利画家；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_flo.txt:590](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_flo.txt:590>)。
- `flavor_flo.33`：[target_artist.GetNameWithNoTooltip]；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_flo.txt:784](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_flo.txt:784>)。
- `flavor_flo.37`：[target_artist.GetNameWithNoTooltip]；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_flo.txt:1083](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_flo.txt:1083>)。
- `flavor_flo.48`：[target_location.GetNameWithNoTooltip]的辉煌学院；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_flo.txt:1928](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_flo.txt:1928>)。
- [flavor_kie.4](ED_Vanilla_Wonder_Construction_Actions.md#flavor_kie-4-387-98122e)：[target_character.GetNameWithNoTooltip]；construct_building；[in_game/events/DHE/flavor_kie.txt:387](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_kie.txt:387>)。
- [flavor_sie.10](ED_Vanilla_Wonder_Construction_Actions.md#flavor_sie-10-663-c38786)：锡耶纳艺术风格；construct_building；[in_game/events/DHE/flavor_SIE.txt:663](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_SIE.txt:663>)。

### bajang_ratu — 双柱门

原版定义：[in_game/common/building_types/unique_buildings.txt:4938](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:4938>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `build_time = large_capital_build_time`
- `location_potential = { counts_as_capital = yes }`
- `allow = { is_capital = yes country_has_no_other_copy_of_building = { type = bajang_ratu } }`

行为或条件引用：

- [maj_bajang_ratu](ED_Vanilla_Wonder_Construction_Actions.md#maj_bajang_ratu-46-ef86ee)：双柱门；unlock_building；[in_game/common/advances/country_maj.txt:46](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/advances/country_maj.txt:46>)。

### banking_office — 银行

原版定义：[in_game/common/building_types/unique_buildings.txt:567](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:567>)。

- `is_special = yes`
- `is_foreign = yes`
- `max_levels = 1`
- `country_potential = { has_reform = government_reform:banking_country }`
- `build_time = bank_office_build_time`

行为或条件引用：

- [flavor_ara.220](ED_Vanilla_Wonder_Construction_Actions.md#flavor_ara-220-3201-e41b99)：巴塞罗那兑换银行；change_building_level_in_location；[in_game/events/DHE/flavor_ARA.txt:3201](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_ARA.txt:3201>)。
- [flavor_flo.57](ED_Vanilla_Wonder_Construction_Actions.md#flavor_flo-57-2593-82835e)：[medici_dynasty.GetNameWithNoTooltip]银行；change_building_level_in_location；[in_game/events/DHE/flavor_flo.txt:2593](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_flo.txt:2593>)。
- [flavor_flo.59](ED_Vanilla_Wonder_Construction_Actions.md#flavor_flo-59-2800-82835e)：新分行成立；change_building_level_in_location；[in_game/events/DHE/flavor_flo.txt:2800](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_flo.txt:2800>)。
- [flavor_gen.14](ED_Vanilla_Wonder_Construction_Actions.md#flavor_gen-14-740-55f1ae)：加扎里亚的命运；change_building_level_in_location；[in_game/events/DHE/flavor_GEN.txt:740](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_GEN.txt:740>)。
- [flavor_gen.46](ED_Vanilla_Wonder_Construction_Actions.md#flavor_gen-46-3029-55f1ae)：圣乔治银行；change_building_level_in_location；[in_game/events/DHE/flavor_GEN.txt:3029](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_GEN.txt:3029>)。
- [flavor_gen.52](ED_Vanilla_Wonder_Construction_Actions.md#flavor_gen-52-3352-55f1ae)：格里马尔迪银行；change_building_level_in_location；[in_game/events/DHE/flavor_GEN.txt:3352](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_GEN.txt:3352>)。
- [flavor_gen.54](ED_Vanilla_Wonder_Construction_Actions.md#flavor_gen-54-3501-55f1ae)：斯皮诺拉银行；change_building_level_in_location；[in_game/events/DHE/flavor_GEN.txt:3501](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_GEN.txt:3501>)。
- [flavor_gen.56](ED_Vanilla_Wonder_Construction_Actions.md#flavor_gen-56-3651-55f1ae)：帕拉维奇诺银行；change_building_level_in_location；[in_game/events/DHE/flavor_GEN.txt:3651](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_GEN.txt:3651>)。
- [flavor_ham.1](ED_Vanilla_Wonder_Construction_Actions.md#flavor_ham-1-3-9ea0c9)：贝伦贝格银行；change_building_level_in_location；[in_game/events/DHE/flavor_HAM.txt:3](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_HAM.txt:3>)。
- [flavor_ham.3](ED_Vanilla_Wonder_Construction_Actions.md#flavor_ham-3-137-9ea0c9)：汉堡银行；change_building_level_in_location；[in_game/events/DHE/flavor_HAM.txt:137](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_HAM.txt:137>)。
- [flavor_por.65](ED_Vanilla_Wonder_Construction_Actions.md#flavor_por-65-4902-f14e68)：门德斯家族；change_building_level_in_location；[in_game/events/DHE/flavor_por.txt:4902](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_por.txt:4902>)。
- [flavor_sie.1](ED_Vanilla_Wonder_Construction_Actions.md#flavor_sie-1-3-c38786)：牧山银行；change_building_level_in_location；[in_game/events/DHE/flavor_SIE.txt:3](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_SIE.txt:3>)。
- [flavor_ven.73](ED_Vanilla_Wonder_Construction_Actions.md#flavor_ven-73-3551-888d6c)：汇划银行；change_building_level_in_location；[in_game/events/DHE/flavor_VEN.txt:3551](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_VEN.txt:3551>)。
- [banking.1](ED_Vanilla_Wonder_Construction_Actions.md#banking-1-6-738c10)：富格尔家族的崛起；change_building_level_in_location；[in_game/events/economy/banking.txt:6](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/economy/banking.txt:6>)。
- [banking.3](ED_Vanilla_Wonder_Construction_Actions.md#banking-3-108-738c10)：韦尔瑟家族；change_building_level_in_location；[in_game/events/economy/banking.txt:108](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/economy/banking.txt:108>)。

1337 开局实例：`florence`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1397](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1397>)；`london`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1398](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1398>)；`bruges`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1399](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1399>)；`paris`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1400](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1400>)；`avignon`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1401](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1401>)；`rodos`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1402](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1402>)；`florence`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1404](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1404>)；`barcelona`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1405](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1405>)；`sevilla`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1406](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1406>)；`palma`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1407](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1407>)；`paris`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1408](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1408>)；`avignon`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1409](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1409>)；`nice`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1410](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1410>)；`marseille`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1411](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1411>)；`london`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1412](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1412>)；`bruges`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1413](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1413>)；`constantinople`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1414](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1414>)；`rodos`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1415](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1415>)；`nicosia_cyp`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1416](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1416>)；`jerusalem`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1417](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1417>)；`florence`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1419](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1419>)；`naples`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1420](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1420>)；`rodos`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1421](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1421>)；`avignon`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1422](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1422>)。

### barcelona_royal_shipyard — 巴塞罗那王家造船厂

原版定义：[in_game/common/building_types/unique_buildings.txt:1500](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:1500>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `build_time = large_port_building_time`
- `country_potential = { always = no }`
- `allow = { always = no }`

行为或条件引用：

- `flavor_ara.104`：巴塞罗那王家造船厂；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_ARA.txt:2220](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_ARA.txt:2220>)。

1337 开局实例：`barcelona`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2000](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2000>)。

### bardic_school — 吟游诗人学院

原版定义：[in_game/common/building_types/unique_buildings.txt:48](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:48>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `country_potential = { has_reform = government_reform:celtic_traditions_reform }`
- `allow = { }`
- `build_time = guild_build_time`

行为或条件引用：

- `location_has_active_bardic_school_trigger`：location_has_active_bardic_school_trigger；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_IRE.txt:7](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_IRE.txt:7>)。

1337 开局实例：`carbery`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1538](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1538>)；`armagh`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1539](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1539>)；`tralee`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1540](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1540>)；`sligo`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1541](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1541>)。

### bavarian_academy_of_sciences — 科学与人文学院

原版定义：[in_game/common/building_types/event_only_buildings.txt:3336](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/event_only_buildings.txt:3336>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `country_potential = { custom_tooltip = { text = bavarian_academy_of_sciences_why has_or_had_tag = BAV } }`
- `allow = { always = no }`
- `build_time = cultural_building_time`
- `location_potential = { counts_as_capital = yes }`

行为或条件引用：

- [flavor_bav.23](ED_Vanilla_Wonder_Construction_Actions.md#flavor_bav-23-912-75be1b)：[target_country.GetAdjectiveWithNoTooltip]科学与人文学院的诞生；construct_building；[in_game/events/DHE/flavor_bav.txt:912](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_bav.txt:912>)。

### belvedere_palace — 美景宫

原版定义：[in_game/common/building_types/event_only_buildings.txt:3185](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/event_only_buildings.txt:3185>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `build_time = large_cultural_building_time`
- `country_potential = { always = no }`
- `allow = { always = no }`
- `custom_tags = { unique_palace }`

行为或条件引用：

- [flavor_hab.101](ED_Vanilla_Wonder_Construction_Actions.md#flavor_hab-101-5708-a07f59)：美景宫；construct_building；[in_game/events/DHE/flavor_HAB.txt:5708](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_HAB.txt:5708>)。

### berlin_palace — 柏林宫

原版定义：[in_game/common/building_types/event_only_buildings.txt:445](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/event_only_buildings.txt:445>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `build_time = cultural_building_time`
- `country_potential = { always = no }`
- `allow = { always = no }`
- `custom_tags = { unique_palace }`

行为或条件引用：

- [flavor_brapru.1100](ED_Vanilla_Wonder_Construction_Actions.md#flavor_brapru-1100-2992-4fbbec)：[ROOT.GetCountry.GetGovernment.GetRulerTitle]新府邸；construct_building；[in_game/events/DHE/flavor_brapru.txt:2992](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_brapru.txt:2992>)。

### bey_fortress — 贝伊堡垒

原版定义：[in_game/common/building_types/unique_buildings.txt:4517](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:4517>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `build_time = small_fort_building`
- `country_potential = { always = no }`
- `on_built = { if = { limit = { location = location:izmit location.owner = { NOT = { has_variable = izmit_variable } } } location.owner = { trigger_event_non_silently = rise_of_the_ottomans.200 set_variable = izmit_variable } } else_if = { limit = { location = location:bursa location.owner = { NOT = { has_variable = bursa_variable } } } location.owner = { trigger_event_non_silently = rise_of_the_ottomans.201 set_variable = bursa_variable } } else_if = { limit = { location = location:konya location.owner = { NOT = { has_variable = konya_variable } } } location.owner = { trigger_event_non_silently = rise_of_the_ottomans.202 set_variable = konya_variable } } else_if = { limit = { location = location:ankara location.owner = { NOT = { has_variable = ankara_variable } } } location.owner = { trigger_event_non_silently = rise_of_the_ottomans.203 set_variable = ankara_variable } } else_if = { limit = { location = location:kayseri location.owner = { NOT = { has_variable = kayseri_variable } } } location.owner = { trigger_event_non_silently = rise_of_the_ottomans.204 set_variable = kayseri_variable } } else_if = { limit = { location = location:sivas location.owner = { NOT = { has_variable = sivas_variable } } } location.owner = { trigger_event_non_silently = rise_of_the_ottomans.205 set_variable = sivas_variable } } else_if = { limit = { location = location:smyrna location.owner = { NOT = { has_variable = smyrna_variable } } } location.owner = { trigger_event_non_silently = rise_of_the_ottomans.206 set_variable = smyrna_variable } } else = { location = { trigger_event_non_silently = rise_of_the_ottomans.207 } } }`

行为或条件引用：

- [raise_bey_fortress](ED_Vanilla_Wonder_Construction_Actions.md#raise_bey_fortress-291-fe089c)：建立贝伊堡垒；construct_building；[in_game/common/generic_actions/rise_of_the_ottomans.txt:291](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/generic_actions/rise_of_the_ottomans.txt:291>)。
- [on_siege_lost](ED_Vanilla_Wonder_Construction_Actions.md#on_siege_lost-447-fff745)：on_siege_lost；门槛/关联引用；需看上下文；[in_game/common/on_action/_hardcoded.txt:447](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/on_action/_hardcoded.txt:447>)。
- [on_took_location_in_peace_treaty](ED_Vanilla_Wonder_Construction_Actions.md#on_took_location_in_peace_treaty-2713-fff745)：on_took_location_in_peace_treaty；门槛/关联引用；需看上下文；[in_game/common/on_action/_hardcoded.txt:2713](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/on_action/_hardcoded.txt:2713>)。
- [on_location_changed_owner](ED_Vanilla_Wonder_Construction_Actions.md#on_location_changed_owner-4851-fff745)：on_location_changed_owner；destroy_building；[in_game/common/on_action/_hardcoded.txt:4851](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/on_action/_hardcoded.txt:4851>)。
- [rise_of_the_ottomans](ED_Vanilla_Wonder_Construction_Actions.md#rise_of_the_ottomans-1-8c1963)：土耳其人的崛起；门槛/关联引用；需看上下文；[in_game/common/situations/rise_of_the_ottomans.txt:1](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/situations/rise_of_the_ottomans.txt:1>)。

### bibliotheca_corviniana — 科尔温图书馆

原版定义：[in_game/common/building_types/event_only_buildings.txt:1627](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/event_only_buildings.txt:1627>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `build_time = cultural_building_time`
- `country_potential = { custom_tooltip = { text = unlocked_bibliotheca_corviniana_tt has_variable = unlocked_bibliotheca_corviniana } }`
- `allow = { always = no }`

行为或条件引用：

- [hun_bibliotheca_corviniana_decision](ED_Vanilla_Wonder_Construction_Actions.md#hun_bibliotheca_corviniana_decision-1565-a14531)：科尔温图书馆；construct_building；[in_game/common/decisions/flavor_decisions_various.txt:1565](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/decisions/flavor_decisions_various.txt:1565>)。

### bodrum_castle — 圣伯多禄城堡

原版定义：[in_game/common/building_types/event_only_buildings.txt:1386](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/event_only_buildings.txt:1386>)。

- `is_special = yes`
- `max_levels = 1`
- `build_time = generic_event_building`
- `country_potential = { always = no }`
- `allow = { always = no }`
- `is_foreign = yes`
- `on_built = { location = { add_core = owner } }`
- `on_destroyed = { location = { remove_core = owner } }`

行为或条件引用：

- [flavor_kni.150](ED_Vanilla_Wonder_Construction_Actions.md#flavor_kni-150-1598-95906a)：[target_location.GetNameWithNoTooltip]城堡；construct_building；[in_game/events/DHE/flavor_kni.txt:1598](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_kni.txt:1598>)。
- [flavor_kni.151](ED_Vanilla_Wonder_Construction_Actions.md#flavor_kni-151-1689-95906a)：境外势力在[target_location.GetNameWithNoTooltip]筑城；construct_building；[in_game/events/DHE/flavor_kni.txt:1689](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_kni.txt:1689>)。

### bolshoi_theater — 莫斯科大剧院

原版定义：[in_game/common/building_types/event_only_buildings.txt:1276](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/event_only_buildings.txt:1276>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `country_potential = { OR = { has_or_had_tag = MOS has_or_had_tag = RUS } }`
- `allow = { custom_tooltip = { text = bolshoi_theater_why always = no } }`
- `build_time = cultural_building_time`

行为或条件引用：

- [flavor_rus.56](ED_Vanilla_Wonder_Construction_Actions.md#flavor_rus-56-4553-201f60)：看得起的表演；destroy_building；[in_game/events/DHE/flavor_RUS.txt:4553](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_RUS.txt:4553>)。
- [flavor_rus.58](ED_Vanilla_Wonder_Construction_Actions.md#flavor_rus-58-4793-201f60)：莫斯科大剧院；construct_building；[in_game/events/DHE/flavor_RUS.txt:4793](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_RUS.txt:4793>)。
- `flavor_rus.65`：莫斯科大剧院芭蕾舞团；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_RUS.txt:5553](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_RUS.txt:5553>)。

### brethren_marsh — 沼泽兄弟会

原版定义：[in_game/common/building_types/unique_buildings.txt:1711](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:1711>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `allow = { owner = { OR = { culture ?= culture:basque culture ?= culture:castilian } } }`
- `location_potential = { is_port = yes OR = { dominant_culture ?= culture:basque province_definition = province_definition:montana_province } }`
- `country_potential = { culture ?= culture:basque }`
- `build_time = medium_port_building_time`

未在本次行为定义中发现显式同名引用；仍可能由建筑自身条件、科技/改革解锁或引擎常规建设入口提供。

1337 开局实例：`bilbao`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2018](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2018>)；`laredo`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2019](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2019>)；`san_vicente_barquera`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2020](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2020>)；`santander`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2021](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2021>)；`san_sebastian`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2022](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2022>)；`tolosa`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2023](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2023>)。

### bridge_infrastructure — 桥梁

原版定义：[in_game/common/building_types/common_buildings.txt:49](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/common_buildings.txt:49>)。

- `is_foreign = no`
- `max_levels = 1`
- `build_time = infrastructure_build_time`
- `location_potential = { has_river = yes num_roads > 0 }`
- `allow = { }`

行为或条件引用：

- [flavor_eng.203](ED_Vanilla_Wonder_Construction_Actions.md#flavor_eng-203-19706-cfcf19)：[target_location.GetNameWithNoTooltip]大桥垮下来；destroy_building；[in_game/events/DHE/flavor_ENG.txt:19706](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_ENG.txt:19706>)。
- [flavor_mlo.19](ED_Vanilla_Wonder_Construction_Actions.md#flavor_mlo-19-923-b6cb55)：[ROOT.GetCountry.GetGovernment.GetRuler.GetNameWithNoTooltip]桥；construct_building；[in_game/events/DHE/flavor_mlo.txt:923](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_mlo.txt:923>)。

1337 开局实例：`london`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1532](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1532>)。

### bubu_building — 鱼笼

原版定义：[in_game/common/building_types/unique_buildings.txt:4990](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:4990>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 2`
- `location_potential = { raw_material = goods:fish }`
- `build_time = rural_build_time`

行为或条件引用：

- [maj_bubu_and_jala](ED_Vanilla_Wonder_Construction_Actions.md#maj_bubu_and_jala-3-ef86ee)：鱼笼与撇网；unlock_building；[in_game/common/advances/country_maj.txt:3](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/advances/country_maj.txt:3>)。

### bulgarian_administration_center — $bulgaria_area$行政中心

原版定义：[in_game/common/building_types/event_only_buildings.txt:4095](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/event_only_buildings.txt:4095>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `build_time = generic_town_build_time`
- `country_potential = { always = no }`
- `allow = { always = no }`
- `remove_if = { location = { "culture_percentage(culture:bulgarian)" = 0 } }`

行为或条件引用：

- [flavor_tur.199](ED_Vanilla_Wonder_Construction_Actions.md#flavor_tur-199-15802-bf9554)：斯雷代茨的地位；construct_building；[in_game/events/DHE/flavor_TUR.txt:15802](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_TUR.txt:15802>)。

### bund — 水坝

原版定义：[in_game/common/building_types/unique_buildings.txt:3448](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:3448>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = bund_cap`
- `location_potential = { OR = { has_river = yes is_adjacent_to_lake = yes } }`
- `build_time = infrastructure_build_time`

行为或条件引用：

- [vij_the_bunds](ED_Vanilla_Wonder_Construction_Actions.md#vij_the_bunds-37-c19b16)：水坝；unlock_building；[in_game/common/advances/country_vij.txt:37](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/advances/country_vij.txt:37>)。

### calmecac — 卡尔梅卡克学校

原版定义：[in_game/common/building_types/unique_buildings.txt:2000](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:2000>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `build_time = government_build_time`
- `country_potential = { culture = { has_culture_group = culture_group:nahua_group } }`
- `location_potential = { counts_as_capital = yes }`
- `allow = { is_capital = yes country_has_no_other_copy_of_building = { type = calmecac } }`

行为或条件引用：

- [warrior_societies](ED_Vanilla_Wonder_Construction_Actions.md#warrior_societies-10-f0f87f)：战士社会；unlock_building；[in_game/common/advances/country_tnc.txt:10](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/advances/country_tnc.txt:10>)。

1337 开局实例：`tenochtitlan`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2515](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2515>)。

### camara_comptos — 纳瓦拉审计院

原版定义：[in_game/common/building_types/event_only_buildings.txt:718](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/event_only_buildings.txt:718>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `location_potential = { counts_as_capital = yes }`
- `allow = { is_capital = yes country_has_no_other_copy_of_building = { type = camara_comptos } }`
- `country_potential = { custom_tooltip = { text = camara_comptos_why has_variable = unlocked_camara_de_comptos } OR = { culture ?= culture:basque has_or_had_tag = NAV } }`
- `remove_if = { is_no_longer_capital = yes }`
- `build_time = government_build_time`

行为或条件引用：

- [nav_camara_comptos_decision](ED_Vanilla_Wonder_Construction_Actions.md#nav_camara_comptos_decision-1511-a14531)：纳瓦拉审计院；construct_building；[in_game/common/decisions/flavor_decisions_various.txt:1511](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/decisions/flavor_decisions_various.txt:1511>)。

### cantonments — 军队营房

原版定义：[in_game/common/building_types/event_only_buildings.txt:1](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/event_only_buildings.txt:1>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `build_time = generic_event_building`
- `country_potential = { always = no }`
- `allow = { always = no }`

行为或条件引用：

- [random_event.26](ED_Vanilla_Wonder_Construction_Actions.md#random_event-26-1194-f69e59)：建立军队营房；change_building_level_in_location；[in_game/events/random_event.txt:1194](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/random_event.txt:1194>)。

### caravan_stop — 骆驼驿站

原版定义：[in_game/common/building_types/unique_buildings.txt:769](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:769>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `country_potential = { has_advance = west_african_caravan_stop_advance }`
- `allow = { OR = { region = region:persia_region region = region:arabia_region region = region:egypt_region region = region:maghreb_region region = region:sahel_region } }`
- `build_time = trade_post_build_time`

行为或条件引用：

- [west_african_caravan_stop_advance](ED_Vanilla_Wonder_Construction_Actions.md#west_african_caravan_stop_advance-12-8838a6)：撒哈拉$caravan_stop$；unlock_building；[in_game/common/advances/culture_west_african.txt:12](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/advances/culture_west_african.txt:12>)。

### caravanserai — 车队驿站

原版定义：[in_game/common/building_types/unique_buildings.txt:713](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:713>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `country_potential = { has_advance = caravanserai_advance }`
- `allow = { OR = { region = region:khorasan_region region = region:xinjiang_region region = region:mongolia_region region = region:steppes_region } }`
- `build_time = trade_post_build_time`

行为或条件引用：

- [caravanserai_advance](ED_Vanilla_Wonder_Construction_Actions.md#caravanserai_advance-54-a83aa2)：车队驿站；unlock_building；[in_game/common/advances/government_steppe_horde.txt:54](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/advances/government_steppe_horde.txt:54>)。

1337 开局实例：`sarai_al_jadid`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1310](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1310>)；`almaliq`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1311](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1311>)；`gorgan`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1312](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1312>)。

### cas_royal_mint_of_segovia — 塞哥维亚皇家铸币厂

原版定义：[in_game/common/building_types/event_only_buildings.txt:4454](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/event_only_buildings.txt:4454>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `country_potential = { always = no }`
- `allow = { always = no }`
- `build_time = generic_town_build_time`

行为或条件引用：

- [flavor_cas.153](ED_Vanilla_Wonder_Construction_Actions.md#flavor_cas-153-9269-9abc78)：资助王室铸币厂；construct_building；[in_game/events/DHE/flavor_CAS.txt:9269](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_CAS.txt:9269>)。

### castel_sant_angelo — 圣天使堡

原版定义：[in_game/common/building_types/event_only_buildings.txt:2765](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/event_only_buildings.txt:2765>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `country_potential = { always = no }`
- `allow = { always = no }`
- `build_time = small_fort_building`
- `location_potential = { this = location:rome }`

行为或条件引用：

- [flavor_pap.25](ED_Vanilla_Wonder_Construction_Actions.md#flavor_pap-25-1573-09eb6b)：加固圣天使堡；construct_building；[in_game/events/DHE/flavor_pap.txt:1573](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_pap.txt:1573>)。

### castle — 城堡

原版定义：[in_game/common/building_types/forts.txt:51](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/forts.txt:51>)。

- `is_foreign = no`
- `max_levels = 1`
- `obsolete = stockade`
- `build_time = medium_fort_building`

行为或条件引用：

- [castle_advance](ED_Vanilla_Wonder_Construction_Actions.md#castle_advance-967-3be8a5)：城堡；unlock_building；[in_game/common/advances/1_building_unlocks.txt:967](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/advances/1_building_unlocks.txt:967>)。
- [mos_build_kremlin_decision](ED_Vanilla_Wonder_Construction_Actions.md#mos_build_kremlin_decision-131-f996cd)：建造克里姆林宫；destroy_building；[in_game/common/decisions/flavor_decisions_rus.txt:131](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/decisions/flavor_decisions_rus.txt:131>)。
- [prepare_defenses_hw_action](ED_Vanilla_Wonder_Construction_Actions.md#prepare_defenses_hw_action-335-c0a892)：准备防御；construct_building；[in_game/common/generic_actions/hussite_wars_actions.txt:335](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/generic_actions/hussite_wars_actions.txt:335>)。
- [on_ending_war](ED_Vanilla_Wonder_Construction_Actions.md#on_ending_war-2039-fff745)：on_ending_war；门槛/关联引用；需看上下文；[in_game/common/on_action/_hardcoded.txt:2039](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/on_action/_hardcoded.txt:2039>)。
- `turn_japanese_clan_into_normal_tag`：turn_japanese_clan_into_normal_tag；门槛/关联引用；需看上下文；[in_game/common/scripted_effects/country_effects.txt:754](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/scripted_effects/country_effects.txt:754>)。
- [construct_latest_fort_building](ED_Vanilla_Wonder_Construction_Actions.md#construct_latest_fort_building-486-e48ed0)：construct_latest_fort_building；construct_building；[in_game/common/scripted_effects/location_effects.txt:486](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/scripted_effects/location_effects.txt:486>)。
- `teu_event_6_trigger`：teu_event_6_trigger；门槛/关联引用；需看上下文；[in_game/common/scripted_triggers/location_triggers.txt:167](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/scripted_triggers/location_triggers.txt:167>)。
- `artist_events.38`：利用矿产资源；门槛/关联引用；需看上下文；[in_game/events/character/artist_events.txt:2121](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/character/artist_events.txt:2121>)。
- [flavor_bav.1100](ED_Vanilla_Wonder_Construction_Actions.md#flavor_bav-1100-1620-75be1b)：英戈尔施塔特要塞；construct_building；[in_game/events/DHE/flavor_bav.txt:1620](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_bav.txt:1620>)。
- [flavor_bav.1101](ED_Vanilla_Wonder_Construction_Actions.md#flavor_bav-1101-1678-75be1b)：英戈尔施塔特[reginar_solms_scope.GetNameWithNoTooltip]；destroy_building；[in_game/events/DHE/flavor_bav.txt:1678](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_bav.txt:1678>)。
- [flavor_byz.28](ED_Vanilla_Wonder_Construction_Actions.md#flavor_byz-28-2088-64397c)：将[ROOT.GetCountry.GetGovernment.GetCourtTitle]迁往[ShowAreaNameWithNoTooltip('morea_area')]；construct_building；[in_game/events/DHE/flavor_BYZ.txt:2088](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_BYZ.txt:2088>)。
- [flavor_cas.125](ED_Vanilla_Wonder_Construction_Actions.md#flavor_cas-125-7743-9abc78)：[ShowRegionNameWithNoTooltip('caribbean_region')]的海盗；construct_building, destroy_building；[in_game/events/DHE/flavor_CAS.txt:7743](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_CAS.txt:7743>)。
- [flavor_dan.42](ED_Vanilla_Wonder_Construction_Actions.md#flavor_dan-42-2610-6355b4)：拆毁阿布萨隆城堡；destroy_building；[in_game/events/DHE/flavor_dan.txt:2610](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_dan.txt:2610>)。
- [flavor_dlh.21](ED_Vanilla_Wonder_Construction_Actions.md#flavor_dlh-21-2106-b76ea9)：[target_location.GetNameWithNoTooltip]要塞化；construct_building；[in_game/events/DHE/flavor_DLH.txt:2106](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_DLH.txt:2106>)。
- [flavor_eng.10](ED_Vanilla_Wonder_Construction_Actions.md#flavor_eng-10-897-cfcf19)：高塔寓所；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_ENG.txt:897](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_ENG.txt:897>)。
- [flavor_eng.11](ED_Vanilla_Wonder_Construction_Actions.md#flavor_eng-11-1005-cfcf19)：反复易手的特威德河畔[target_location.GetNameWithNoTooltip]；construct_building；[in_game/events/DHE/flavor_ENG.txt:1005](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_ENG.txt:1005>)。
- `flavor_eng.96`：[john_thornton.GetNameWithNoTooltip]；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_ENG.txt:8543](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_ENG.txt:8543>)。
- [flavor_gen.19](ED_Vanilla_Wonder_Construction_Actions.md#flavor_gen-19-1156-55f1ae)：巴斯蒂亚的建成；change_building_level_in_location；[in_game/events/DHE/flavor_GEN.txt:1156](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_GEN.txt:1156>)。
- [flavor_geo.15](ED_Vanilla_Wonder_Construction_Actions.md#flavor_geo-15-1013-260218)：[target_location.GetNameWithNoTooltip]堡垒；construct_building；[in_game/events/DHE/flavor_geo.txt:1013](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_geo.txt:1013>)。
- [flavor_hab.2201](ED_Vanilla_Wonder_Construction_Actions.md#flavor_hab-2201-9361-a07f59)：[ShowAreaNameWithNoTooltip('austria_area')]的安防；destroy_building；[in_game/events/DHE/flavor_HAB.txt:9361](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_HAB.txt:9361>)。
- [flavor_hun.520](ED_Vanilla_Wonder_Construction_Actions.md#flavor_hun-520-2853-0c02c5)：布兰城堡；construct_building；[in_game/events/DHE/flavor_HUN.txt:2853](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_HUN.txt:2853>)。
- [flavor_jap.162](ED_Vanilla_Wonder_Construction_Actions.md#flavor_jap-162-3470-b3bd1b)：大坂城的建造；construct_building, destroy_building；[in_game/events/DHE/flavor_JAP.txt:3470](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_JAP.txt:3470>)。
- [flavor_lub.1](ED_Vanilla_Wonder_Construction_Actions.md#flavor_lub-1-3-5f4a7f)：[target_location.GetNameWithNoTooltip]城门；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_LUB.txt:3](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_LUB.txt:3>)。
- [flavor_mal.22](ED_Vanilla_Wonder_Construction_Actions.md#flavor_mal-22-1342-bbb082)：重夺[target_location.GetNameWithNoTooltip]；change_building_level_in_location, construct_building；[in_game/events/DHE/flavor_MAL.txt:1342](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_MAL.txt:1342>)。
- [flavor_nor.3](ED_Vanilla_Wonder_Construction_Actions.md#flavor_nor-3-138-3963de)：瓦尔德胡斯要塞；construct_building；[in_game/events/DHE/flavor_NOR.txt:138](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_NOR.txt:138>)。
- `flavor_pol.29`：[target_character.GetShortNameWithNoTooltip]的繁荣改革；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_pol.txt:1954](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_pol.txt:1954>)。
- `flavor_sco.16`：蒙斯梅格大炮；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_SCO.txt:897](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_SCO.txt:897>)。
- [flavor_ser.130](ED_Vanilla_Wonder_Construction_Actions.md#flavor_ser-130-1829-15d4f1)：斯梅代雷沃的要塞；construct_building, destroy_building；[in_game/events/DHE/flavor_ser.txt:1829](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_ser.txt:1829>)。
- [flavor_ser.230](ED_Vanilla_Wonder_Construction_Actions.md#flavor_ser-230-2327-15d4f1)：筑防于戈卢巴茨；change_building_level_in_location；[in_game/events/DHE/flavor_ser.txt:2327](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_ser.txt:2327>)。
- [flavor_teu.6](ED_Vanilla_Wonder_Construction_Actions.md#flavor_teu-6-352-8fc2ec)：[target_location.GetNameWithNoTooltip]的[ShowReligionAdjectiveWithNoTooltip('romuva')]异教徒；construct_building；[in_game/events/DHE/flavor_teu.txt:352](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_teu.txt:352>)。
- [flavor_tim_governor.14](ED_Vanilla_Wonder_Construction_Actions.md#flavor_tim_governor-14-990-3b62ae)：[target_location.GetNameWithNoTooltip]要塞化；construct_building；[in_game/events/DHE/flavor_timurid_governor.txt:990](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_timurid_governor.txt:990>)。
- [flavor_tur.106](ED_Vanilla_Wonder_Construction_Actions.md#flavor_tur-106-7614-bf9554)：耶路撒冷的修缮；change_building_level_in_location, construct_building；[in_game/events/DHE/flavor_TUR.txt:7614](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_TUR.txt:7614>)。
- [flavor_tur.143](ED_Vanilla_Wonder_Construction_Actions.md#flavor_tur-143-10887-bf9554)：铁城堡；change_building_level_in_location, construct_building；[in_game/events/DHE/flavor_TUR.txt:10887](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_TUR.txt:10887>)。
- [flavor_tur.1003](ED_Vanilla_Wonder_Construction_Actions.md#flavor_tur-1003-17478-bf9554)：[ShowProvinceDefinitionNameWithNoTooltip('albania_province')]的[ShowSubjectTypeNameWithNoTooltip('uc_bey')]；construct_building；[in_game/events/DHE/flavor_TUR.txt:17478](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_TUR.txt:17478>)。
- [flavor_ven.65](ED_Vanilla_Wonder_Construction_Actions.md#flavor_ven-65-3109-888d6c)：沿海堡垒；construct_building；[in_game/events/DHE/flavor_VEN.txt:3109](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_VEN.txt:3109>)。
- [earthquake_events.1000](ED_Vanilla_Wonder_Construction_Actions.md#earthquake_events-1000-5330-77de80)：[target_location.GetNameWithNoTooltip]地震；destroy_building；[in_game/events/earthquake_events.txt:5330](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/earthquake_events.txt:5330>)。
- [rise_of_the_ottomans.200](ED_Vanilla_Wonder_Construction_Actions.md#rise_of_the_ottomans-200-1192-798ec8)：帝国的旧首都；门槛/关联引用；需看上下文；[in_game/events/situations/rise_of_the_ottomans.txt:1192](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/situations/rise_of_the_ottomans.txt:1192>)。
- [rise_of_the_ottomans.201](ED_Vanilla_Wonder_Construction_Actions.md#rise_of_the_ottomans-201-1364-798ec8)：[target_location.GetNameWithNoTooltip]-命运与历史；门槛/关联引用；需看上下文；[in_game/events/situations/rise_of_the_ottomans.txt:1364](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/situations/rise_of_the_ottomans.txt:1364>)。
- [rise_of_the_ottomans.202](ED_Vanilla_Wonder_Construction_Actions.md#rise_of_the_ottomans-202-1537-798ec8)：[target_location.GetNameWithNoTooltip]-塞尔柱之影；门槛/关联引用；需看上下文；[in_game/events/situations/rise_of_the_ottomans.txt:1537](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/situations/rise_of_the_ottomans.txt:1537>)。
- [rise_of_the_ottomans.203](ED_Vanilla_Wonder_Construction_Actions.md#rise_of_the_ottomans-203-1710-798ec8)：[target_location.GetNameWithNoTooltip]-易帜之城；门槛/关联引用；需看上下文；[in_game/events/situations/rise_of_the_ottomans.txt:1710](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/situations/rise_of_the_ottomans.txt:1710>)。
- [rise_of_the_ottomans.204](ED_Vanilla_Wonder_Construction_Actions.md#rise_of_the_ottomans-204-1883-798ec8)：[target_location.GetNameWithNoTooltip]-文化十字路口；门槛/关联引用；需看上下文；[in_game/events/situations/rise_of_the_ottomans.txt:1883](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/situations/rise_of_the_ottomans.txt:1883>)。
- [rise_of_the_ottomans.205](ED_Vanilla_Wonder_Construction_Actions.md#rise_of_the_ottomans-205-2056-798ec8)：[target_location.GetNameWithNoTooltip]-东方的遗孑；门槛/关联引用；需看上下文；[in_game/events/situations/rise_of_the_ottomans.txt:2056](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/situations/rise_of_the_ottomans.txt:2056>)。
- [rise_of_the_ottomans.206](ED_Vanilla_Wonder_Construction_Actions.md#rise_of_the_ottomans-206-2233-798ec8)：[target_location.GetNameWithNoTooltip]-异教徒之城；门槛/关联引用；需看上下文；[in_game/events/situations/rise_of_the_ottomans.txt:2233](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/situations/rise_of_the_ottomans.txt:2233>)。
- [rise_of_the_ottomans.207](ED_Vanilla_Wonder_Construction_Actions.md#rise_of_the_ottomans-207-2406-798ec8)：崛起中的强权；门槛/关联引用；需看上下文；[in_game/events/situations/rise_of_the_ottomans.txt:2406](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/situations/rise_of_the_ottomans.txt:2406>)。

1337 开局实例：`stockholm`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1184](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1184>)；`kalmar`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1185](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1185>)；`abo`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1186](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1186>)；`tavastehus`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1187](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1187>)；`vyborg`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1188](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1188>)；`oslo`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1190](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1190>)；`konghalla`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1191](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1191>)；`kobenhavn`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1194](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1194>)；`odense`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1195](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1195>)；`viborg`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1196](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1196>)；`izborsk`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1241](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1241>)；`oreshek`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1242](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1242>)；`riga`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1243](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1243>)；`aluksne`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1245](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1245>)；`daugavpils`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1246](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1246>)；`london`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1427](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1427>)；`dover`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1428](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1428>)；`alnwick`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1429](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1429>)；`carlisle`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1430](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1430>)；`chester`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1431](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1431>)；`coventry`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1432](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1432>)；`windsor`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1433](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1433>)；`leeds`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1434](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1434>)；`pontefract`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1435](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1435>)；`edinburgh`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1444](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1444>)；`stirling`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1445](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1445>)；`roxburgh`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1446](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1446>)；`cardiff`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1484](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1484>)；`harlech`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1485](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1485>)；`carnarvon`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1486](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1486>)；`conwy`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1487](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1487>)；`caerphilly`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1488](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1488>)；`pembroke`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1489](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1489>)；`dublin`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1547](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1547>)；`carrickfergus`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1548](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1548>)；`fingal`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1549](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1549>)；`cork`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1550](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1550>)；`braganca`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1796](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1796>)；`elvas`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1797](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1797>)；`laguardia`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1798](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1798>)；`olite`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1799](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1799>)；`pinhel`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1801](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1801>)；`portalegre`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1802](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1802>)；`saint_jean_pied_de_port`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1803](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1803>)；`viana_do_castelo`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1805](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1805>)；`malbork`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2130](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2130>)；`szczytno`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2131](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2131>)；`insterburg`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2132](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2132>)；`ostroda`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2133](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2133>)；`olsztyn`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2134](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2134>)；`lubawa`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2135](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2135>)；`kwidzyn`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2136](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2136>)；`grudziadz`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2137](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2137>)；`tuchola`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2138](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2138>)；`poznan`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2139](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2139>)；`plock`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2140](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2140>)；`krakow`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2141](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2141>)；`vilnius`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2142](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2142>)；`kaunas`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2143](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2143>)；`wielun`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2144](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2144>)；`luxembourg`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2161](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2161>)；`schwerin`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2178](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2178>)；`dresden`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2179](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2179>)；`klagenfurt`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2180](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2180>)；`merano`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2181](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2181>)；`landshut`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2182](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2182>)；`amberg`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2183](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2183>)；`coblenz`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2184](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2184>)；`bienne`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2201](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2201>)；`lausanne`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2202](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2202>)；`neuchatel`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2203](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2203>)；`burgdorf_emmental`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2204](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2204>)；`basel`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2205](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2205>)；`lucerne`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2206](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2206>)；`frutigen`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2207](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2207>)；`sarnen`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2208](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2208>)；`sion`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2209](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2209>)；`chur`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2210](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2210>)；`altdorf`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2211](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2211>)；`schwyz`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2212](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2212>)；`werdenberg`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2213](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2213>)；`st_gallen`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2214](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2214>)；`solothurn`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2215](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2215>)；`mozhaysk`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2235](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2235>)；`vyazma`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2236](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2236>)；`bely`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2237](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2237>)；`roslavl`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2238](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2238>)；`gorokhovets`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2239](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2239>)；`zubtsov`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2240](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2240>)；`klin`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2241](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2241>)；`myrhorod`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2279](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2279>)；`lviv`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2280](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2280>)；`sanok`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2281](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2281>)；`volodymyr`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2282](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2282>)；`gallipoli`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2353](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2353>)；`rodos`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2368](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2368>)；`kozelj`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2369](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2369>)；`kucevo`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2370](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2370>)；`trgoviste_SER`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2371](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2371>)；`ankober`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2430](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2430>)；`gonder`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2431](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2431>)；`kubar`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2432](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2432>)；`indrapura`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2512](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2512>)；`gutti`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3659](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3659>)；`anegandi`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3660](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3660>)；`udayagiri`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3661](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3661>)；`basavapattana`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3662](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3662>)；`baniyas`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3814](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3814>)；`ouarzazate`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3826](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3826>)；`pursat`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3869](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3869>)。

### cathedral — 大教堂

原版定义：[in_game/common/building_types/estate_buildings.txt:400](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/estate_buildings.txt:400>)。

- `is_foreign = no`
- `max_levels = 1`
- `build_time = large_religious_building_time`

行为或条件引用：

- [cathedral_advance](ED_Vanilla_Wonder_Construction_Actions.md#cathedral_advance-5-3be8a5)：主教座堂；unlock_building；[in_game/common/advances/1_building_unlocks.txt:5](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/advances/1_building_unlocks.txt:5>)。
- [sponsor_a_cathedral_decision](ED_Vanilla_Wonder_Construction_Actions.md#sponsor_a_cathedral_decision-2-57c555)：赞助主教座堂；construct_building；[in_game/common/decisions/generic_age_decisions.txt:2](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/decisions/generic_age_decisions.txt:2>)。
- `request_cardinal_seat`：请求任命枢机；门槛/关联引用；需看上下文；[in_game/common/generic_actions/catholic.txt:238](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/generic_actions/catholic.txt:238>)。
- `perform_reduction`：削减阶层力量；门槛/关联引用；需看上下文；[in_game/common/generic_actions/estates.txt:208](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/generic_actions/estates.txt:208>)。
- [estate_cooperation](ED_Vanilla_Wonder_Construction_Actions.md#estate_cooperation-1-821312)：阶层合作；门槛/关联引用；需看上下文；[in_game/common/missions/generic_estate_cooperation_mission_pack.txt:1](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/missions/generic_estate_cooperation_mission_pack.txt:1>)。
- [sponsor_a_cathedral](ED_Vanilla_Wonder_Construction_Actions.md#sponsor_a_cathedral-90-7dea4a)：赞助$cathedral$；construct_building；[in_game/common/parliament_issues/04_clergy_estate_parliament_issues.txt:90](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/parliament_issues/04_clergy_estate_parliament_issues.txt:90>)。
- `artist_events.32`：[target_location.GetNameWithNoTooltip]的新圣像展览；门槛/关联引用；需看上下文；[in_game/events/character/artist_events.txt:1776](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/character/artist_events.txt:1776>)。
- [flavor_bav.9](ED_Vanilla_Wonder_Construction_Actions.md#flavor_bav-9-618-75be1b)：玛丽亚圣母小教堂；construct_building；[in_game/events/DHE/flavor_bav.txt:618](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_bav.txt:618>)。
- [flavor_bav.1200](ED_Vanilla_Wonder_Construction_Actions.md#flavor_bav-1200-1809-75be1b)：泰阿蒂尼修会教堂；construct_building；[in_game/events/DHE/flavor_bav.txt:1809](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_bav.txt:1809>)。
- [flavor_boh.27](ED_Vanilla_Wonder_Construction_Actions.md#flavor_boh-27-1435-eb1e43)：圣维笃大教堂；construct_building；[in_game/events/DHE/flavor_BOH.txt:1435](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_BOH.txt:1435>)。
- `flavor_eng.96`：[john_thornton.GetNameWithNoTooltip]；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_ENG.txt:8543](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_ENG.txt:8543>)。
- [flavor_flo.28](ED_Vanilla_Wonder_Construction_Actions.md#flavor_flo-28-441-82835e)：佛罗伦萨大教堂；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_flo.txt:441](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_flo.txt:441>)。
- `flavor_hab.10`：慷慨的格拉茨市民；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_HAB.txt:384](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_HAB.txt:384>)。
- [flavor_lit.17](ED_Vanilla_Wonder_Construction_Actions.md#flavor_lit-17-1387-a1868c)：[ShowLocationNameWithNoTooltip('vilnius')\|U]大教堂；construct_building；[in_game/events/DHE/flavor_LIT.txt:1387](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_LIT.txt:1387>)。
- [flavor_maj.13](ED_Vanilla_Wonder_Construction_Actions.md#flavor_maj-13-695-ceab17)：老鼠寺；construct_building；[in_game/events/DHE/flavor_maj.txt:695](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_maj.txt:695>)。
- [flavor_maj.14](ED_Vanilla_Wonder_Construction_Actions.md#flavor_maj-14-773-ceab17)：苏腊瓦纳寺；construct_building；[in_game/events/DHE/flavor_maj.txt:773](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_maj.txt:773>)。
- [flavor_mlo.24](ED_Vanilla_Wonder_Construction_Actions.md#flavor_mlo-24-1324-b6cb55)：[target_location.GetNameWithNoTooltip]大教堂；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_mlo.txt:1324](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_mlo.txt:1324>)。
- [flavor_mos.28](ED_Vanilla_Wonder_Construction_Actions.md#flavor_mos-28-2275-c719bc)：诞神女安息大教堂；construct_building；[in_game/events/DHE/flavor_MOS.txt:2275](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_MOS.txt:2275>)。
- [flavor_mos.58](ED_Vanilla_Wonder_Construction_Actions.md#flavor_mos-58-6067-c719bc)：伊凡大帝钟楼；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_MOS.txt:6067](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_MOS.txt:6067>)。
- [flavor_nav.60](ED_Vanilla_Wonder_Construction_Actions.md#flavor_nav-60-1568-def420)：女王的遗愿；construct_building；[in_game/events/DHE/flavor_NAV.txt:1568](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_NAV.txt:1568>)。
- [flavor_nov.30](ED_Vanilla_Wonder_Construction_Actions.md#flavor_nov-30-1750-51d2dc)：圣智大教堂；change_building_level_in_location；[in_game/events/DHE/flavor_NOV.txt:1750](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_NOV.txt:1750>)。
- [flavor_pap.14](ED_Vanilla_Wonder_Construction_Actions.md#flavor_pap-14-726-09eb6b)：西斯廷礼拜堂；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_pap.txt:726](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_pap.txt:726>)。
- [flavor_sco.18](ED_Vanilla_Wonder_Construction_Actions.md#flavor_sco-18-1167-b81a33)：[wolf_origin.GetNameWithNoTooltip]之狼；construct_building, destroy_building；[in_game/events/DHE/flavor_SCO.txt:1167](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_SCO.txt:1167>)。
- `parliaments.46`：荣誉归于谁？；门槛/关联引用；需看上下文；[in_game/events/government/parliaments.txt:2963](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/government/parliaments.txt:2963>)。
- [church_aspects.7](ED_Vanilla_Wonder_Construction_Actions.md#church_aspects-7-234-3a383e)：[ROOT.GetCountry.GetGovernment.GetEstateNameWithNoTooltip('burghers_estate')]用他们所得进行投资；construct_building；[in_game/events/religion/church_aspects.txt:234](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/religion/church_aspects.txt:234>)。
- `hussite_loc_root_region_with_temple_or_cathedral`：hussite_loc_root_region_with_temple_or_cathedral；门槛/关联引用；需看上下文；[in_game/events/religion/hussite_flavor.txt:15](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/religion/hussite_flavor.txt:15>)。
- [miaphysite_flavor.32](ED_Vanilla_Wonder_Construction_Actions.md#miaphysite_flavor-32-709-53c86d)：新的时代；门槛/关联引用；需看上下文；[in_game/events/religion/miaphsyite_flavor.txt:709](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/religion/miaphsyite_flavor.txt:709>)。
- `patriarch_events.2`：圣礼的影响；门槛/关联引用；需看上下文；[in_game/events/religion/patriarch_events.txt:56](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/religion/patriarch_events.txt:56>)。
- `patriarch_events.3`：为[local_see_province.GetNameWithNoTooltip]修建大教堂；门槛/关联引用；需看上下文；[in_game/events/religion/patriarch_events.txt:107](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/religion/patriarch_events.txt:107>)。

1337 开局实例：`konigsberg`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1255](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1255>)；`elgin`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1464](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1464>)；`st_andrews`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1465](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1465>)；`aberdeen`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1466](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1466>)；`glasgow`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1467](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1467>)；`stranraer`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1468](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1468>)；`inverary`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1469](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1469>)；`dundee`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1470](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1470>)；`perth`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1471](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1471>)；`dornoch`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1472](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1472>)；`orkney`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1473](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1473>)；`london`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1574](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1574>)；`york`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1575](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1575>)；`canterbury`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1576](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1576>)；`wells`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1577](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1577>)；`tamworth`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1578](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1578>)；`lincoln`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1579](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1579>)；`dublin`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1580](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1580>)；`chichester`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1581](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1581>)；`exeter`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1582](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1582>)；`ely`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1583](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1583>)；`hereford`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1584](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1584>)；`norwich`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1585](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1585>)；`rochester`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1586](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1586>)；`salisbury`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1587](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1587>)；`winchester`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1588](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1588>)；`worcester`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1589](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1589>)；`carlisle`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1590](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1590>)；`durham`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1591](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1591>)；`anglesey`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1592](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1592>)；`cardiff`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1593](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1593>)；`pembroke`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1594](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1594>)；`conwy`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1595](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1595>)；`astorga`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1809](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1809>)；`avila`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1810](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1810>)；`badajoz`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1811](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1811>)；`baeza`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1812](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1812>)；`barcelona`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1813](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1813>)；`benabarre`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1814](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1814>)；`burgo_de_osma`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1815](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1815>)；`burgos`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1816](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1816>)；`cadiz`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1817](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1817>)；`calahorra`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1818](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1818>)；`cartagena`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1819](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1819>)；`ciudad_rodrigo`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1820](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1820>)；`coimbra`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1821](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1821>)；`cordoba`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1822](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1822>)；`coria`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1823](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1823>)；`cuenca`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1824](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1824>)；`evora`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1825](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1825>)；`girona`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1826](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1826>)；`guarda`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1827](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1827>)；`guimaraes`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1828](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1828>)；`huesca`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1829](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1829>)；`jaca`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1830](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1830>)；`lamego`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1831](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1831>)；`leon`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1832](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1832>)；`lisbon`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1833](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1833>)；`lleida`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1834](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1834>)；`lugo`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1835](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1835>)；`mondonedo`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1836](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1836>)；`najera`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1837](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1837>)；`ourense`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1838](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1838>)；`oviedo`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1839](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1839>)；`palencia`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1840](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1840>)；`palma`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1841](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1841>)；`pamplona`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1842](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1842>)；`plasencia`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1843](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1843>)；`porto`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1844](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1844>)；`salamanca`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1845](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1845>)；`santiago_compostela`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1846](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1846>)；`segovia`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1847](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1847>)；`seu_durgell`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1848](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1848>)；`sevilla`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1849](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1849>)；`siguenza`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1850](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1850>)；`tarazona`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1851](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1851>)；`tarragona`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1852](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1852>)；`toledo`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1853](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1853>)；`tudela`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1854](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1854>)；`tuy`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1855](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1855>)；`valencia`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1856](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1856>)；`viseu`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1857](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1857>)；`zamora`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1858](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1858>)；`zaragoza`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1859](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1859>)；`fehervar`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2043](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2043>)；`ghent`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2163](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2163>)；`liege`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2164](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2164>)；`utrecht`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2165](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2165>)；`tournai`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2166](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2166>)；`novgorod`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2250](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2250>)；`smolensk`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2251](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2251>)；`murom`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2252](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2252>)；`ryazan`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2253](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2253>)；`suzdal`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2254](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2254>)；`vladimir`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2255](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2255>)；`tver`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2256](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2256>)；`kyiv`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2292](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2292>)；`polotsk`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2293](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2293>)；`halych`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2294](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2294>)；`chernihiv`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2295](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2295>)；`volodymyr`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2296](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2296>)；`pinsk`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2297](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2297>)；`novogrudok`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2298](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2298>)；`agde`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2320](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2320>)；`agen`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2321](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2321>)；`aire`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2322](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2322>)；`aix_en_provence`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2323](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2323>)；`albi`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2324](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2324>)；`amiens`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2325](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2325>)；`angers`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2326](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2326>)；`angouleme`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2327](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2327>)；`apt`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2328](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2328>)；`arles`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2329](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2329>)；`arras`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2330](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2330>)；`autun`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2331](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2331>)；`auxerre`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2332](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2332>)；`avignon`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2333](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2333>)；`avranches`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2334](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2334>)；`cambrai`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2335](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2335>)；`foix`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2336](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2336>)；`grasse`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2337](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2337>)；`paris`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2338](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2338>)；`saint_malo`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2339](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2339>)；`saint_omer`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2340](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2340>)；`constantinople`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2357](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2357>)；`thessaloniki`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2358](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2358>)；`edirne`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2359](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2359>)；`monemvasia`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2360](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2360>)；`mystras`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2361](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2361>)；`larissa`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2362](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2362>)；`mitilene`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2363](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2363>)；`chios`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2364](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2364>)；`lemnos`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2365](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2365>)；`tarnovo`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2395](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2395>)；`plovdiv`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2396](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2396>)；`drastar`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2397](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2397>)；`varna`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2398](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2398>)；`sredets`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2399](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2399>)；`vidin`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2400](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2400>)；`ohrid`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2401](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2401>)；`peja`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2402](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2402>)；`prizren`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2403](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2403>)；`skopje`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2404](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2404>)；`trebizond`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2405](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2405>)；`rome`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3876](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3876>)；`tivoli`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3877](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3877>)；`palestrina`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3878](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3878>)；`velletri`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3879](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3879>)；`toulouse`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3881](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3881>)；`bazas`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3882](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3882>)；`lyon`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3883](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3883>)；`langres`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3884](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3884>)；`viviers`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3885](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3885>)；`bourges`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3886](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3886>)；`narbonne`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3888](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3888>)；`auxerre`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3889](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3889>)；`manfredonia`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3891](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3891>)；`naples`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3892](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3892>)；`cologne`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3895](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3895>)；`mainz`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3896](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3896>)；`trier`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3897](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3897>)；`salzburg`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3898](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3898>)；`prague`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3899](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3899>)；`magdeburg`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3900](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3900>)；`bremervorde`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3901](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3901>)；`besancon`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3902](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3902>)；`gniezno`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3903](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3903>)；`esztergom`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3904](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3904>)；`kalocsa`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3905](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3905>)；`lund`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3906](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3906>)；`uppsala`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3907](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3907>)；`nidaros`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3908](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3908>)；`riga`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3909](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3909>)；`halych`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3910](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3910>)；`dubrovnik`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3911](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3911>)；`split`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3912](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3912>)；`aquileia`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3913](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3913>)；`milano`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3914](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3914>)；`ravenna`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3915](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3915>)；`genoa`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3916](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3916>)；`vienne`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3917](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3917>)；`nicosia_cyp`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3918](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3918>)；`candia`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3919](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3919>)；`reims`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3920](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3920>)；`rouen`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3921](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3921>)；`tours`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3922](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3922>)；`bordeaux`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3923](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3923>)；`pisa`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3924](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3924>)；`benevento`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3925](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3925>)；`salerno`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3926](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3926>)；`reggiocal`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3927](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3927>)；`palermo`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3928](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3928>)。

### cawa_barracks — 恰瓦军营

原版定义：[in_game/common/building_types/unique_buildings.txt:1809](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:1809>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = janissary_barracks_size`
- `build_time = soldier_building`

行为或条件引用：

- [cawa_advance](ED_Vanilla_Wonder_Construction_Actions.md#cawa_advance-122-2e1f7f)：恰瓦军团；unlock_building；[in_game/common/advances/country_eth.txt:122](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/advances/country_eth.txt:122>)。

1337 开局实例：`ankober`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2428](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2428>)。

### central_bank — 中央银行

原版定义：[in_game/common/building_types/capital_buildings.txt:1204](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/capital_buildings.txt:1204>)。

- `is_foreign = no`
- `max_levels = 1`
- `build_time = large_capital_build_time`
- `allow = { custom_tooltip = { text = central_bank_tt is_capital = yes NOR = { has_building = building_type:wisselbank has_building = building_type:riksbank } } country_has_no_other_copy_of_building = { type = central_bank } owner = scope:actor }`
- `location_potential = { counts_as_capital = yes NOR = { has_building = building_type:wisselbank has_building = building_type:riksbank } }`
- `remove_if = { is_no_longer_capital = yes }`

行为或条件引用：

- [central_bank_advance](ED_Vanilla_Wonder_Construction_Actions.md#central_bank_advance-31-680093)：中央银行；unlock_building；[in_game/common/advances/0_age_of_absolutism.txt:31](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/advances/0_age_of_absolutism.txt:31>)。
- [flavor_eng.28](ED_Vanilla_Wonder_Construction_Actions.md#flavor_eng-28-3081-cfcf19)：新银行的建立；change_building_level_in_location；[in_game/events/DHE/flavor_ENG.txt:3081](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_ENG.txt:3081>)。
- [flavor_swe.60](ED_Vanilla_Wonder_Construction_Actions.md#flavor_swe-60-3033-211578)：瑞典国家银行；destroy_building；[in_game/events/DHE/flavor_SWE.txt:3033](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_SWE.txt:3033>)。

### charite_of_berlin — 沙里泰慈善院

原版定义：[in_game/common/building_types/event_only_buildings.txt:4339](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/event_only_buildings.txt:4339>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `build_time = large_cultural_building_time`
- `country_potential = { always = no }`
- `allow = { always = no }`

行为或条件引用：

- [flavor_brapru.36](ED_Vanilla_Wonder_Construction_Actions.md#flavor_brapru-36-2427-4fbbec)：抗击瘟疫；construct_building；[in_game/events/DHE/flavor_brapru.txt:2427](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_brapru.txt:2427>)。

### chi_macau_port — 澳门条约港

原版定义：[in_game/common/building_types/event_only_buildings.txt:1480](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/event_only_buildings.txt:1480>)。

- `is_special = yes`
- `is_foreign = yes`
- `max_levels = guild_max_level`
- `country_potential = { always = no }`
- `allow = { always = no }`
- `build_time = trade_post_build_time`

行为或条件引用：

- [flavor_chi_por.1](ED_Vanilla_Wonder_Construction_Actions.md#flavor_chi_por-1-3-e7bc0c)：$china$港口租借；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_chi_por.txt:3](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_chi_por.txt:3>)。
- [flavor_chi_por.2](ED_Vanilla_Wonder_Construction_Actions.md#flavor_chi_por-2-76-e7bc0c)：租借[target_location.GetNameWithNoTooltip]的请求；construct_building；[in_game/events/DHE/flavor_chi_por.txt:76](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_chi_por.txt:76>)。

### chi_missionary_building — 方济会传道所

原版定义：[in_game/common/building_types/event_only_buildings.txt:1522](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/event_only_buildings.txt:1522>)。

- `is_special = yes`
- `is_foreign = yes`
- `max_levels = 1`
- `country_potential = { always = no }`
- `allow = { always = no }`
- `build_time = colonise_build_time`

行为或条件引用：

- `flavor_chi_pap.1`：[target_country.GetNameWithNoTooltip]使团来访；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_chi_pap.txt:3](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_chi_pap.txt:3>)。
- `flavor_chi_pap.2`：[ShowContinentNameWithNoTooltip('europe')]访问使团归来；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_chi_pap.txt:117](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_chi_pap.txt:117>)。

1337 开局实例：`dadu`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3697](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3697>)。

### cinque_port — 海峡五港

原版定义：[in_game/common/building_types/unique_buildings.txt:890](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:890>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `country_potential = { has_or_had_tag = ENG }`
- `location_potential = { is_port = yes }`
- `allow = { always = no }`
- `build_time = medium_port_building_time`

行为或条件引用：

- [flavor_eng.12](ED_Vanilla_Wonder_Construction_Actions.md#flavor_eng-12-1101-cfcf19)：五港总督的庆典；destroy_building；[in_game/events/DHE/flavor_ENG.txt:1101](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_ENG.txt:1101>)。
- [flavor_eng.70](ED_Vanilla_Wonder_Construction_Actions.md#flavor_eng-70-6327-cfcf19)：海峡五港的衰落；destroy_building；[in_game/events/DHE/flavor_ENG.txt:6327](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_ENG.txt:6327>)。

1337 开局实例：`hastings`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1600](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1600>)；`dover`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1601](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1601>)；`hythe`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1602](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1602>)；`rochester`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1603](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1603>)；`canterbury`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1604](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1604>)。

### city_of_victory — 胜利之城

原版定义：[in_game/common/building_types/event_only_buildings.txt:2223](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/event_only_buildings.txt:2223>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `build_time = religious_building_time`
- `country_potential = { always = no }`
- `allow = { always = no }`

行为或条件引用：

- [flavor_vij.17](ED_Vanilla_Wonder_Construction_Actions.md#flavor_vij-17-901-2f8e63)：[target_location.GetNameWithNoTooltip]，胜利之城；construct_building；[in_game/events/DHE/flavor_vij.txt:901](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_vij.txt:901>)。
- [flavor_vij.18](ED_Vanilla_Wonder_Construction_Actions.md#flavor_vij-18-966-2f8e63)：[target_location.GetNameWithNoTooltip]的陷落；destroy_building；[in_game/events/DHE/flavor_vij.txt:966](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_vij.txt:966>)。

### city_walls — 市镇城墙

原版定义：[in_game/common/building_types/forts.txt:249](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/forts.txt:249>)。

- `is_foreign = no`
- `max_levels = 1`
- `build_time = huge_unique_build_time`
- `allow = { NOT = { has_building = building_type:theodosian_walls } NOT = { has_building = building_type:walls_of_lucca } }`

行为或条件引用：

- [pa_construct_city_walls](ED_Vanilla_Wonder_Construction_Actions.md#pa_construct_city_walls-1016-cf85e0)：要求$city_walls$；construct_building；[in_game/common/parliament_agendas/03_buildings.txt:1016](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/parliament_agendas/03_buildings.txt:1016>)。
- [flavor_luc.5](ED_Vanilla_Wonder_Construction_Actions.md#flavor_luc-5-231-b9dd70)：$lucca$城墙；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_LUC.txt:231](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_LUC.txt:231>)。

1337 开局实例：`thessaloniki`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2355](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2355>)；`dadu`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3931](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3931>)；`thang_long`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3932](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3932>)；`rome`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3933](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3933>)；`hangzhou`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3934](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3934>)；`jingzhao`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3935](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3935>)；`kaifeng`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3936](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3936>)；`ghent`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3937](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3937>)；`kano`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3938](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3938>)；`angkor`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3939](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3939>)；`mayapan`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3940](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3940>)；`florence`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3941](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3941>)；`samarkand`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3942](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3942>)；`cologne`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3943](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3943>)；`bologna`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3944](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3944>)；`tabriz`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3945](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3945>)；`pisa`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3946](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3946>)；`sevilla`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3947](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3947>)；`xiangyang`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3948](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3948>)；`bruges`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3949](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3949>)；`milano`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3950](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3950>)；`sukhothai`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3951](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3951>)；`antwerp`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3952](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3952>)；`herat`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3953](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3953>)；`paris`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3954](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3954>)；`nuremberg`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3955](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3955>)；`lubeck`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3956](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3956>)；`buda`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3957](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3957>)；`genoa`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3958](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3958>)；`vienna`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3959](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3959>)；`naples`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3960](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3960>)；`norwich`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3961](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3961>)；`rodos`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3962](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3962>)；`yazd`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3963](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3963>)；`visby`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3964](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3964>)；`krakow`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3965](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3965>)；`york`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3966](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3966>)；`carcassonne`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3967](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3967>)；`tarnovo`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3968](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3968>)；`hormuz`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3969](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3969>)；`waterford`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3970](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3970>)；`riga`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3971](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3971>)；`sopron`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3972](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3972>)；`limerick`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3973](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3973>)；`dubrovnik`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3974](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3974>)；`dublin`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3975](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3975>)；`cork`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3976](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3976>)。

### clan_family_shrine — 氏神神社

原版定义：[in_game/common/building_types/unique_buildings.txt:2978](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:2978>)。

- `is_special = yes`
- `is_foreign = yes`
- `max_levels = 1`
- `location_potential = { dominant_culture = { has_culture_group = culture_group:japanese_group } }`
- `country_potential = { OR = { AND = { has_reform = government_reform:japanese_imperial_family country_type = building } has_reform = government_reform:japanese_clan } }`
- `build_time = estate_build_time`
- `allow = { dominant_culture = { has_culture_group = culture_group:japanese_group } any_foreign_building_countries_in_location = { this = scope:actor } }`

未在本次行为定义中发现显式同名引用；仍可能由建筑自身条件、科技/改革解锁或引擎常规建设入口提供。

1337 开局实例：`kyoto`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2621](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2621>)；`watarai`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2627](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2627>)；`nukanobu`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2763](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2763>)；`taki`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2775](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2775>)；`koma_kai`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3044](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3044>)；`kamiina`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3054](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3054>)；`ikaruga`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3084](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3084>)；`nakata`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3171](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3171>)；`ooita`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3380](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3380>)；`satsuma`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3468](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3468>)；`shioya`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3514](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3514>)；`suwa`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3567](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3567>)；`suzuka`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3582](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3582>)。

### clan_shipyards — 水军砦

原版定义：[in_game/common/building_types/unique_buildings.txt:2921](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:2921>)。

- `is_special = yes`
- `is_foreign = yes`
- `max_levels = japanese_clan_building_cap`
- `location_potential = { dominant_culture = { has_culture_group = culture_group:japanese_group } is_port = yes }`
- `country_potential = { OR = { AND = { has_reform = government_reform:japanese_imperial_family country_type = building } has_reform = government_reform:japanese_clan } }`
- `build_time = estate_build_time`
- `allow = { dominant_culture = { has_culture_group = culture_group:japanese_group } any_foreign_building_countries_in_location = { this = scope:actor } }`

未在本次行为定义中发现显式同名引用；仍可能由建筑自身条件、科技/改革解锁或引擎常规建设入口提供。

1337 开局实例：`nukanobu`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2764](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2764>)；`taki`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2774](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2774>)；`akita`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2793](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2793>)；`chiba`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2852](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2852>)；`kariwa`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3006](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3006>)；`kamo`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3022](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3022>)；`nakata`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3170](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3170>)；`akou`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3197](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3197>)；`ochi`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3339](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3339>)；`mitoyo`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3354](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3354>)；`ooita`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3381](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3381>)；`nakatsu`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3402](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3402>)；`mikasa`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3404](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3404>)；`akita_kumamoto`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3406](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3406>)；`shimoagata`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3408](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3408>)；`higashimatsuura`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3422](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3422>)；`aimi`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3431](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3431>)；`satsuma`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3466](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3466>)；`kagoshima`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3473](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3473>)；`iyo`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3536](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3536>)；`kamiagata`，level=`2`，[main_menu/setup/1337/07_cities_and_buildings.txt:3562](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3562>)；`agawa`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3577](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3577>)；`suzuka`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3583](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3583>)；`nyuu`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3589](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3589>)。

### coastal_settlements — 沿海定居点

原版定义：[in_game/common/building_types/unique_buildings.txt:4665](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:4665>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `country_potential = { has_unlocked_building_trigger = { type = coastal_settlements } }`
- `location_potential = { is_coastal = yes }`
- `remove_if = { location = { OR = { location_rank = location_rank:city location_rank = location_rank:megalopolis } } }`
- `build_time = colonise_build_time`

行为或条件引用：

- [flavor_oma.16](ED_Vanilla_Wonder_Construction_Actions.md#flavor_oma-16-1120-85fa5f)：沿海移民计划；unlock_building_effect；[in_game/events/DHE/flavor_OMA.txt:1120](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_OMA.txt:1120>)。

### college_of_poets — 诗人与数学家学院

原版定义：[in_game/common/building_types/event_only_buildings.txt:1569](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/event_only_buildings.txt:1569>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `country_potential = { OR = { has_or_had_tag = HAB has_or_had_tag = TIR has_or_had_tag = STY } }`
- `allow = { custom_tooltip = { text = college_of_poets_why always = no } }`
- `build_time = cultural_building_time`

行为或条件引用：

- [flavor_hab.1301](ED_Vanilla_Wonder_Construction_Actions.md#flavor_hab-1301-6774-a07f59)：[target_character.GetNameWithNoTooltip]提议设立诗人与数学家学院；construct_building；[in_game/events/DHE/flavor_HAB.txt:6774](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_HAB.txt:6774>)。

### confucian_academy — 书院

原版定义：[in_game/common/building_types/culture_buildings.txt:162](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/culture_buildings.txt:162>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `build_time = cultural_building_time`
- `allow = { is_core_of = owner }`

行为或条件引用：

- [confucian_academy_advance](ED_Vanilla_Wonder_Construction_Actions.md#confucian_academy_advance-1042-3be8a5)：书院；unlock_building；[in_game/common/advances/1_building_unlocks.txt:1042](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/advances/1_building_unlocks.txt:1042>)。
- [sponsor_a_confucian_academy](ED_Vanilla_Wonder_Construction_Actions.md#sponsor_a_confucian_academy-2-7dea4a)：赞助$confucian_academy$；construct_building；[in_game/common/parliament_issues/04_clergy_estate_parliament_issues.txt:2](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/parliament_issues/04_clergy_estate_parliament_issues.txt:2>)。
- `imperial_examination_events.7`：人中翘楚；门槛/关联引用；需看上下文；[in_game/events/imperial_examination_events.txt:608](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/imperial_examination_events.txt:608>)。

### constantinople_observatory — 塔基丁天文台

原版定义：[in_game/common/building_types/event_only_buildings.txt:2733](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/event_only_buildings.txt:2733>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `build_time = large_cultural_building_time`
- `country_potential = { always = no }`
- `allow = { always = no }`

行为或条件引用：

- [flavor_tur.103](ED_Vanilla_Wonder_Construction_Actions.md#flavor_tur-103-7390-bf9554)：[taqi_ad_din.GetNameWithNoTooltip]的天文台；construct_building；[in_game/events/DHE/flavor_TUR.txt:7390](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_TUR.txt:7390>)。
- [flavor_tur.104](ED_Vanilla_Wonder_Construction_Actions.md#flavor_tur-104-7443-bf9554)：[GetCurrentYear]年大彗星；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_TUR.txt:7443](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_TUR.txt:7443>)。
- [flavor_tur.105](ED_Vanilla_Wonder_Construction_Actions.md#flavor_tur-105-7516-bf9554)：天文台的终结；destroy_building；[in_game/events/DHE/flavor_TUR.txt:7516](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_TUR.txt:7516>)。

### construction_center — 建造部门

原版定义：[in_game/common/building_types/town_buildings.txt:37](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/town_buildings.txt:37>)。

- `is_foreign = no`
- `max_levels = construction_center_max_level`
- `build_time = government_build_time`

行为或条件引用：

- [construction_center_advance](ED_Vanilla_Wonder_Construction_Actions.md#construction_center_advance-24-3be8a5)：建造部门；unlock_building；[in_game/common/advances/1_building_unlocks.txt:24](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/advances/1_building_unlocks.txt:24>)。

### copenhagen_dockyard — 哥本哈根造船厂

原版定义：[in_game/common/building_types/unique_buildings.txt:658](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:658>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `location_potential = { counts_as_capital = yes }`
- `allow = { is_capital = yes country_has_no_other_copy_of_building = { type = copenhagen_dockyard } }`
- `build_time = large_port_building_time`

行为或条件引用：

- [dan_expanded_dockyards](ED_Vanilla_Wonder_Construction_Actions.md#dan_expanded_dockyards-89-15413c)：哥本哈根造船厂；unlock_building；[in_game/common/advances/country_dan.txt:89](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/advances/country_dan.txt:89>)。
- `flavor_dan.66`：扩建哥本哈根造船厂；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_dan.txt:3795](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_dan.txt:3795>)。

### corporation_of_london — 市法团

原版定义：[in_game/common/building_types/event_only_buildings.txt:325](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/event_only_buildings.txt:325>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `build_time = generic_town_build_time`
- `country_potential = { always = no }`
- `allow = { always = no }`

行为或条件引用：

- [flavor_eng.10](ED_Vanilla_Wonder_Construction_Actions.md#flavor_eng-10-897-cfcf19)：高塔寓所；destroy_building；[in_game/events/DHE/flavor_ENG.txt:897](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_ENG.txt:897>)。

1337 开局实例：`london`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1528](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1528>)。

### darussifa — 达尔谢法医馆

原版定义：[in_game/common/building_types/event_only_buildings.txt:4186](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/event_only_buildings.txt:4186>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `build_time = generic_town_build_time`
- `country_potential = { always = no }`
- `allow = { always = no }`

行为或条件引用：

- [flavor_tur.220](ED_Vanilla_Wonder_Construction_Actions.md#flavor_tur-220-17148-bf9554)：阿马西亚的达尔谢法医馆；construct_building；[in_game/events/DHE/flavor_TUR.txt:17148](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_TUR.txt:17148>)。

### debere_meshwae — 献祭山大教堂

原版定义：[in_game/common/building_types/event_only_buildings.txt:2841](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/event_only_buildings.txt:2841>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `build_time = large_cultural_building_time`
- `allow = { always = no }`
- `country_potential = { religion ?= religion:miaphysite }`
- `location_potential = { always = no }`

行为或条件引用：

- [flavor_eth.163](ED_Vanilla_Wonder_Construction_Actions.md#flavor_eth-163-1775-2d218a)：献祭山大教堂；construct_building；[in_game/events/DHE/flavor_ETH.txt:1775](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_ETH.txt:1775>)。

### delhi_tomb — 苏丹陵寝

原版定义：[in_game/common/building_types/event_only_buildings.txt:2970](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/event_only_buildings.txt:2970>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `build_time = religious_building_time`
- `country_potential = { always = no }`
- `allow = { always = no }`

行为或条件引用：

- [construct_delhi_tombs](ED_Vanilla_Wonder_Construction_Actions.md#construct_delhi_tombs-1811-b76ea9)：construct_delhi_tombs；construct_building；[in_game/events/DHE/flavor_DLH.txt:1811](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_DLH.txt:1811>)。
- [flavor_dlh.17](ED_Vanilla_Wonder_Construction_Actions.md#flavor_dlh-17-1820-b76ea9)：[target_character.GetNameWithNoTooltip]的陵墓；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_DLH.txt:1820](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_DLH.txt:1820>)。
- [flavor_dlh.18](ED_Vanilla_Wonder_Construction_Actions.md#flavor_dlh-18-1874-b76ea9)：[target_character.GetNameWithNoTooltip]之死；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_DLH.txt:1874](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_DLH.txt:1874>)。
- [flavor_dlh.19](ED_Vanilla_Wonder_Construction_Actions.md#flavor_dlh-19-1934-b76ea9)：[target_character.GetNameWithNoTooltip]之墓；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_DLH.txt:1934](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_DLH.txt:1934>)。

### dip_vatican_library — 梵蒂冈图书馆：外交侧

原版定义：[in_game/common/building_types/event_only_buildings.txt:1117](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/event_only_buildings.txt:1117>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `build_time = large_cultural_building_time`
- `country_potential = { always = no }`

行为或条件引用：

- [flavor_pap.13](ED_Vanilla_Wonder_Construction_Actions.md#flavor_pap-13-661-09eb6b)：梵蒂冈图书馆；change_building_level_in_location；[in_game/events/DHE/flavor_pap.txt:661](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_pap.txt:661>)。

### doges_palace — 总督宫

原版定义：[in_game/common/building_types/event_only_buildings.txt:2154](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/event_only_buildings.txt:2154>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `country_potential = { has_variable = unlocked_the_doges_palace }`
- `allow = { always = no }`
- `build_time = large_cultural_building_time`
- `custom_tags = { unique_palace }`

行为或条件引用：

- [ven_doges_palace_decision](ED_Vanilla_Wonder_Construction_Actions.md#ven_doges_palace_decision-1204-a14531)：扩建总督宫；construct_building；[in_game/common/decisions/flavor_decisions_various.txt:1204](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/decisions/flavor_decisions_various.txt:1204>)。

### dun_fort — 氏族堡寨

原版定义：[in_game/common/building_types/unique_buildings.txt:2426](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:2426>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `build_time = small_fort_building`
- `country_potential = { modifier:allow_dun_fort = yes }`
- `location_potential = { OR = { dominant_culture.language = language:gaelic_language dominant_culture = { has_culture_group = culture_group:scottish_group } } }`

未在本次行为定义中发现显式同名引用；仍可能由建筑自身条件、科技/改革解锁或引擎常规建设入口提供。

1337 开局实例：`islay`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3615](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3615>)；`lewis`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3616](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3616>)；`harris`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3617](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3617>)；`durness`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3618](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3618>)；`dingwall`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3619](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3619>)；`inverary`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3620](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3620>)。

### dutch_trade_outpost — 出岛荷兰商馆

原版定义：[in_game/common/building_types/event_only_buildings.txt:1826](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/event_only_buildings.txt:1826>)。

- `is_special = yes`
- `is_foreign = yes`
- `max_levels = 1`
- `country_potential = { always = no }`
- `allow = { always = no }`
- `build_time = trade_post_build_time`

行为或条件引用：

- [flavor_ned.5](ED_Vanilla_Wonder_Construction_Actions.md#flavor_ned-5-370-711d97)：[ShowRegionNameWithNoTooltip('japan_region')]贸易；construct_building；[in_game/events/DHE/flavor_ned.txt:370](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_ned.txt:370>)。

### eghabho_nore_mansion — 地头治所

原版定义：[in_game/common/building_types/unique_buildings.txt:5152](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:5152>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = eghabho_nore_mansion_max_level`
- `build_time = religious_building_time`
- `country_potential = { has_unlocked_building_trigger = { type = eghabho_nore_mansion } }`

行为或条件引用：

- [flavor_ben.2](ED_Vanilla_Wonder_Construction_Actions.md#flavor_ben-2-3-3f4044)：城镇管理权；unlock_building_effect；[in_game/events/DHE/flavor_ben.txt:3](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_ben.txt:3>)。

### el_escorial_palace — 埃斯科里亚尔修道院

原版定义：[in_game/common/building_types/event_only_buildings.txt:3663](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/event_only_buildings.txt:3663>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `build_time = large_cultural_building_time`
- `country_potential = { always = no }`
- `allow = { always = no }`

行为或条件引用：

- [flavor_cas.46](ED_Vanilla_Wonder_Construction_Actions.md#flavor_cas-46-2887-9abc78)：埃斯科里亚尔修道院宫；construct_building；[in_game/events/DHE/flavor_CAS.txt:2887](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_CAS.txt:2887>)。
- `flavor_cas.69`：[target_character.GetNameWithNoTooltip]；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_CAS.txt:4244](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_CAS.txt:4244>)。
- [flavor_cas.117](ED_Vanilla_Wonder_Construction_Actions.md#flavor_cas-117-7342-9abc78)：圣老楞佐修道院图书馆；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_CAS.txt:7342](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_CAS.txt:7342>)。

### enderun_academy — 恩德伦内廷学院

原版定义：[in_game/common/building_types/event_only_buildings.txt:530](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/event_only_buildings.txt:530>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `build_time = soldier_building`
- `country_potential = { always = no }`
- `allow = { always = no }`

行为或条件引用：

- [tur_enderun_academy_decision](ED_Vanilla_Wonder_Construction_Actions.md#tur_enderun_academy_decision-1-cd3e74)：恩德伦内廷学院；construct_building；[in_game/common/decisions/flavor_decisions_tur.txt:1](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/decisions/flavor_decisions_tur.txt:1>)。

### eng_royal_forest — 王室保留地

原版定义：[in_game/common/building_types/unique_buildings.txt:936](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:936>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `country_potential = { has_or_had_tag = ENG }`
- `location_potential = { is_core_of = scope:actor development < 20 NOR = { vegetation = farmland } }`
- `allow = { }`
- `build_time = rural_build_time`

未在本次行为定义中发现显式同名引用；仍可能由建筑自身条件、科技/改革解锁或引擎常规建设入口提供。

1337 开局实例：`lymington`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1607](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1607>)；`retford`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1608](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1608>)；`chelmsford`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1609](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1609>)；`windsor`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1610](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1610>)；`gloucester`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1611](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1611>)；`okehampton`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1612](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1612>)；`penrith`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1613](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1613>)。

### fondaco — 商馆

原版定义：[in_game/common/building_types/unique_buildings.txt:215](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:215>)。

- `is_special = yes`
- `is_foreign = yes`
- `max_levels = guild_max_level`
- `country_potential = { OR = { AND = { is_merchant_republic = yes culture = { has_culture_group = culture_group:italian_group } } has_policy = ara_consulate_sea } }`
- `allow = { within_naval_range_of = scope:actor owner = { giving_scripted_relation = { type = relation_type:fondaco_rights target = scope:actor } } }`
- `build_time = trade_post_build_time`

未在本次行为定义中发现显式同名引用；仍可能由建筑自身条件、科技/改革解锁或引擎常规建设入口提供。

1337 开局实例：`kaffa`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2117](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2117>)；`soldaia`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2118](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2118>)；`tana`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2119](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2119>)；`vosporo`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2120](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2120>)。

### forbidden_city — 紫禁城

原版定义：[in_game/common/building_types/event_only_buildings.txt:1439](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/event_only_buildings.txt:1439>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `build_time = cultural_building_time`
- `country_potential = { always = no }`
- `allow = { always = no }`

行为或条件引用：

- [flavor_chi.53](ED_Vanilla_Wonder_Construction_Actions.md#flavor_chi-53-3783-52d64e)：紫禁城；change_building_level_in_location；[in_game/events/DHE/flavor_chi.txt:3783](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_chi.txt:3783>)。
- [flavor_chi.54](ED_Vanilla_Wonder_Construction_Actions.md#flavor_chi-54-3854-52d64e)：$flavor_chi.53.title$落成；change_building_level_in_location；[in_game/events/DHE/flavor_chi.txt:3854](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_chi.txt:3854>)。

### fortezza_di_sant_andrea — 圣安德烈亚要塞

原版定义：[in_game/common/building_types/event_only_buildings.txt:234](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/event_only_buildings.txt:234>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `build_time = generic_town_build_time`
- `country_potential = { always = no }`
- `allow = { always = no }`

行为或条件引用：

- [flavor_ven.9](ED_Vanilla_Wonder_Construction_Actions.md#flavor_ven-9-337-888d6c)：圣安德肋要塞；construct_building；[in_game/events/DHE/flavor_VEN.txt:337](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_VEN.txt:337>)。

### fortress — 要塞

原版定义：[in_game/common/building_types/forts.txt:198](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/forts.txt:198>)。

- `is_foreign = no`
- `max_levels = 1`
- `obsolete = star_fort`
- `build_time = large_fort_building`

行为或条件引用：

- [fortress_advance](ED_Vanilla_Wonder_Construction_Actions.md#fortress_advance-997-3be8a5)：要塞；unlock_building；[in_game/common/advances/1_building_unlocks.txt:997](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/advances/1_building_unlocks.txt:997>)。
- [construct_latest_fort_building](ED_Vanilla_Wonder_Construction_Actions.md#construct_latest_fort_building-486-e48ed0)：construct_latest_fort_building；construct_building；[in_game/common/scripted_effects/location_effects.txt:486](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/scripted_effects/location_effects.txt:486>)。
- `teu_event_6_trigger`：teu_event_6_trigger；门槛/关联引用；需看上下文；[in_game/common/scripted_triggers/location_triggers.txt:167](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/scripted_triggers/location_triggers.txt:167>)。
- `artist_events.38`：利用矿产资源；门槛/关联引用；需看上下文；[in_game/events/character/artist_events.txt:2121](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/character/artist_events.txt:2121>)。
- [flavor_tur.1003](ED_Vanilla_Wonder_Construction_Actions.md#flavor_tur-1003-17478-bf9554)：[ShowProvinceDefinitionNameWithNoTooltip('albania_province')]的[ShowSubjectTypeNameWithNoTooltip('uc_bey')]；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_TUR.txt:17478](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_TUR.txt:17478>)。
- [earthquake_events.1000](ED_Vanilla_Wonder_Construction_Actions.md#earthquake_events-1000-5330-77de80)：[target_location.GetNameWithNoTooltip]地震；destroy_building；[in_game/events/earthquake_events.txt:5330](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/earthquake_events.txt:5330>)。

### fortress_church — 城堡教堂

原版定义：[in_game/common/building_types/religion_buildings.txt:63](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/religion_buildings.txt:63>)。

- `is_foreign = no`
- `max_levels = 1`
- `build_time = religious_building_time`
- `country_potential = { OR = { modifier:can_have_monasteries = yes has_reform = government_reform:shield_of_the_faith_reform religion ?= religion:orthodox } }`
- `location_potential = { OR = { location_building_level = { building_type = building_type:monastery value > 0 } location_building_level = { building_type = building_type:orthodox_monastery value > 0 } owner ?= { has_reform = government_reform:shield_of_the_faith_reform } } }`
- `remove_if = { location = { NOT = { has_building = building_type:monastery } NOT = { has_building = building_type:orthodox_monastery } } NOT = { location.owner = { has_reform = government_reform:shield_of_the_faith_reform } } }`

行为或条件引用：

- [fortress_church_advance](ED_Vanilla_Wonder_Construction_Actions.md#fortress_church_advance-1299-3be8a5)：城堡教堂；unlock_building；[in_game/common/advances/1_building_unlocks.txt:1299](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/advances/1_building_unlocks.txt:1299>)。

### fortress_granary — 粮仓要塞

原版定义：[in_game/common/building_types/town_buildings.txt:163](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/town_buildings.txt:163>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `build_time = medium_fort_building`
- `country_potential = { culture ?= { has_culture_group = culture_group:maghrebi_group } }`
- `location_potential = { }`

未在本次行为定义中发现显式同名引用；仍可能由建筑自身条件、科技/改革解锁或引擎常规建设入口提供。

### fra_louvre_museum — 卢浮宫博物馆

原版定义：[in_game/common/building_types/event_only_buildings.txt:3259](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/event_only_buildings.txt:3259>)。

- `is_foreign = no`
- `max_levels = 1`
- `build_time = large_capital_build_time`
- `country_potential = { always = no }`
- `allow = { always = no }`

行为或条件引用：

- [flavor_fra.550](ED_Vanilla_Wonder_Construction_Actions.md#flavor_fra-550-15724-387b9f)：卢浮宫的开放；construct_building；[in_game/events/DHE/flavor_FRA.txt:15724](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_FRA.txt:15724>)。

### free_economic_society — 自由经济协会

原版定义：[in_game/common/building_types/unique_buildings.txt:3865](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:3865>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `country_potential = { custom_tooltip = { text = free_economic_society_why OR = { tag = MOS tag = RUS } has_variable = free_economic_society } }`
- `allow = { always = no }`
- `build_time = government_build_time`
- `location_potential = { this = location:neva }`

行为或条件引用：

- [rus_free_economic_society_decision](ED_Vanilla_Wonder_Construction_Actions.md#rus_free_economic_society_decision-1977-f996cd)：自由经济协会；construct_building；[in_game/common/decisions/flavor_decisions_rus.txt:1977](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/decisions/flavor_decisions_rus.txt:1977>)。
- `flavor_rus.47`：[mikhail_speransky.GetNameWithNoTooltip]；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_RUS.txt:3704](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_RUS.txt:3704>)。

### friesland_admiralty — 弗里斯兰海军部

原版定义：[in_game/common/building_types/event_only_buildings.txt:1867](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/event_only_buildings.txt:1867>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `build_time = large_port_building_time`
- `country_potential = { always = no }`
- `location_potential = { this = location:harlingen is_capital = no }`

行为或条件引用：

- [ned_unified_dutch_admiralties_decision](ED_Vanilla_Wonder_Construction_Actions.md#ned_unified_dutch_admiralties_decision-2096-a14531)：建立五大海军部；construct_building；[in_game/common/decisions/flavor_decisions_various.txt:2096](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/decisions/flavor_decisions_various.txt:2096>)。

### fulani_cattle_rearing_pen — 牛栏

原版定义：[in_game/common/building_types/unique_buildings.txt:5027](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:5027>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = fulani_cattle_rearing_pen_max_level`
- `country_potential = { has_unlocked_building_trigger = { type = fulani_cattle_rearing_pen } }`
- `location_potential = { raw_material = goods:livestock region = region:guinea_region any_pop = { culture ?= culture:fulbe } }`
- `build_time = rural_build_time`

行为或条件引用：

- [flavor_mal.23](ED_Vanilla_Wonder_Construction_Actions.md#flavor_mal-23-1424-bbb082)：[ShowCultureNameWithNoTooltip('fulbe')]人的[ShowGoodsNameWithNoTooltip('livestock')]养殖；unlock_building_effect；[in_game/events/DHE/flavor_MAL.txt:1424](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_MAL.txt:1424>)。

### galata — 加拉塔

原版定义：[in_game/common/building_types/unique_buildings.txt:3289](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:3289>)。

- `is_special = yes`
- `is_foreign = yes`
- `max_levels = italian_merchant_quarters_max_level`
- `country_potential = { tag = GEN }`
- `location_potential = { this = location:constantinople }`
- `remove_if = { owner = { NOT = { tag = GEN } } }`
- `allow = { within_naval_range_of = scope:actor }`
- `build_time = trade_post_build_time`

行为或条件引用：

- `flavor_byz.35`：[target_character2.GetNameWithNoTooltip]；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_BYZ.txt:2610](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_BYZ.txt:2610>)。
- [flavor_byz.54](ED_Vanilla_Wonder_Construction_Actions.md#flavor_byz-54-4697-64397c)：处理[ShowCultureGroupNameWithNoTooltip('italian_group')]商人；destroy_building；[in_game/events/DHE/flavor_BYZ.txt:4697](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_BYZ.txt:4697>)。
- [flavor_byz.1301](ED_Vanilla_Wonder_Construction_Actions.md#flavor_byz-1301-6618-64397c)：重建[target_location.GetNameWithNoTooltip]；change_building_level_in_location；[in_game/events/DHE/flavor_BYZ.txt:6618](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_BYZ.txt:6618>)。
- [flavor_tur.6](ED_Vanilla_Wonder_Construction_Actions.md#flavor_tur-6-258-bf9554)：关于君士坦丁堡商人的问题；destroy_building；[in_game/events/DHE/flavor_TUR.txt:258](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_TUR.txt:258>)。

1337 开局实例：`constantinople`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3624](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3624>)。

### galley_barracks — 划桨奴隶营房

原版定义：[in_game/common/building_types/unique_buildings.txt:1119](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:1119>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 5`
- `location_potential = { is_port = yes }`
- `build_time = medium_port_building_time`

行为或条件引用：

- [genoese_maritime_diplomacy](ED_Vanilla_Wonder_Construction_Actions.md#genoese_maritime_diplomacy-20-63480f)：骄傲之城；unlock_building；[in_game/common/advances/culture_ligurian.txt:20](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/advances/culture_ligurian.txt:20>)。

1337 开局实例：`genoa`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2123](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2123>)。

### gallowglass_sept — 外乡人氏族地

原版定义：[in_game/common/building_types/unique_buildings.txt:388](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:388>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = guild_max_level`
- `location_potential = { OR = { any_pop = { culture ?= culture:norse_gael OR = { pop_type = pop_type:soldiers pop_type = pop_type:peasants pop_type = pop_type:tribesmen } } } }`
- `country_potential = { }`
- `build_time = soldier_building`

行为或条件引用：

- `unit_gallowglass_pop_trigger`：unit_gallowglass_pop_trigger；门槛/关联引用；需看上下文；[in_game/common/scripted_triggers/unit_triggers.txt:114](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/scripted_triggers/unit_triggers.txt:114>)。
- `ireland_50_target_location_trigger`：ireland_50_target_location_trigger；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_IRE.txt:389](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_IRE.txt:389>)。
- `ireland_50_origin_location_trigger`：ireland_50_origin_location_trigger；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_IRE.txt:396](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_IRE.txt:396>)。
- [ireland.50](ED_Vanilla_Wonder_Construction_Actions.md#ireland-50-411-3656ab)：外乡勇士；construct_building；[in_game/events/DHE/flavor_IRE.txt:411](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_IRE.txt:411>)。

1337 开局实例：`harris`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1501](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1501>)；`lewis`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1502](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1502>)；`uist`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1503](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1503>)；`skye`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1504](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1504>)；`arran`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1505](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1505>)；`mull`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1506](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1506>)；`islay`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1507](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1507>)；`kintyre`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1508](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1508>)；`stranraer`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1509](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1509>)；`ayr`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1510](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1510>)；`kirkcudbright`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1511](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1511>)；`irvine`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1512](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1512>)；`mann`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1513](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1513>)；`inishowen`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1514](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1514>)。

### general_archive_of_simancas — 锡曼卡斯总档案馆

原版定义：[in_game/common/building_types/event_only_buildings.txt:3629](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/event_only_buildings.txt:3629>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `country_potential = { always = no }`
- `allow = { always = no }`
- `build_time = cultural_building_time`

行为或条件引用：

- [flavor_cas.44](ED_Vanilla_Wonder_Construction_Actions.md#flavor_cas-44-2775-9abc78)：[ROOT.GetCountry.GetFlavorRank]档案馆；construct_building；[in_game/events/DHE/flavor_CAS.txt:2775](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_CAS.txt:2775>)。

### german_mountain_toll_castle — 山地关卡堡垒

原版定义：[in_game/common/building_types/unique_buildings.txt:6085](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:6085>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `location_potential = { topography = mountains num_roads > 0 }`
- `country_potential = { has_advance = german_mountain_toll_castle_advance }`
- `build_time = trade_post_build_time`

行为或条件引用：

- [german_mountain_toll_castle_advance](ED_Vanilla_Wonder_Construction_Actions.md#german_mountain_toll_castle_advance-185-8fb8f1)：山地关卡堡垒；unlock_building；[in_game/common/advances/culture_group_german.txt:185](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/advances/culture_group_german.txt:185>)。

### german_river_toll_castle — 河流关卡堡垒

原版定义：[in_game/common/building_types/unique_buildings.txt:6043](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:6043>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `location_potential = { has_river = yes }`
- `country_potential = { has_advance = german_river_toll_castle_advance }`
- `build_time = trade_post_build_time`

行为或条件引用：

- [german_river_toll_castle_advance](ED_Vanilla_Wonder_Construction_Actions.md#german_river_toll_castle_advance-171-8fb8f1)：河流关卡堡垒；unlock_building；[in_game/common/advances/culture_group_german.txt:171](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/advances/culture_group_german.txt:171>)。

### ghilman_barracks — $a_ghilman$兵营

原版定义：[in_game/common/building_types/unique_buildings.txt:1261](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:1261>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `build_time = soldier_building`

行为或条件引用：

- [ira_the_ghilman](ED_Vanilla_Wonder_Construction_Actions.md#ira_the_ghilman-187-cd7a6f)：古拉姆；unlock_building；[in_game/common/advances/country_ira.txt:187](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/advances/country_ira.txt:187>)。
- `flavor_ira.1100`：[ROOT.GetCountry.GetNameWithNoTooltip]的[ShowUnitDefinitionNameWithNoTooltip('a_ghilman')]士兵；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_ira.txt:4048](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_ira.txt:4048>)。

### globe_theatre — 环球剧场

原版定义：[in_game/common/building_types/event_only_buildings.txt:824](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/event_only_buildings.txt:824>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `country_potential = { custom_tooltip = globe_theatre_why OR = { has_or_had_tag = ENG has_or_had_tag = GBR } }`
- `allow = { custom_tooltip = { text = globe_theatre_why always = no } }`
- `build_time = cultural_building_time`

行为或条件引用：

- [flavor_eng.163](ED_Vanilla_Wonder_Construction_Actions.md#flavor_eng-163-15810-cfcf19)：环球剧场；construct_building；[in_game/events/DHE/flavor_ENG.txt:15810](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_ENG.txt:15810>)。
- [flavor_eng.166](ED_Vanilla_Wonder_Construction_Actions.md#flavor_eng-166-16147-cfcf19)：[ROOT.GetCountry.GetGovernment.GetRuler.GetNameWithNoTooltip]洪峰；destroy_building；[in_game/events/DHE/flavor_ENG.txt:16147](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_ENG.txt:16147>)。
- `flavor_eng.197`：[aphra_behn.GetNameWithNoTooltip]；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_ENG.txt:19255](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_ENG.txt:19255>)。
- `flavor_eng.206`：美才女奈尔；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_ENG.txt:19981](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_ENG.txt:19981>)。

### gosho — 御所

原版定义：[in_game/common/building_types/unique_buildings.txt:2532](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:2532>)。

- `is_special = yes`
- `is_foreign = yes`
- `max_levels = 1`
- `location_potential = { dominant_culture = { has_culture_group = culture_group:japanese_group } }`
- `country_potential = { has_reform = government_reform:japanese_imperial_family }`
- `build_time = soldier_building`
- `allow = { dominant_culture = { has_culture_group = culture_group:japanese_group } OR = { this = location:kyoto AND = { scope:actor = { country_type = building } any_foreign_building_countries_in_location = { this = scope:actor } } } }`

行为或条件引用：

- [peace_expand_clan_influence](ED_Vanilla_Wonder_Construction_Actions.md#peace_expand_clan_influence-1-19f6b9)：扩张大名影响力；construct_building；[in_game/common/peace_treaties/expand_clan_influence.txt:1](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/peace_treaties/expand_clan_influence.txt:1>)。
- [nanbokuchou_end_event_emperor_effect](ED_Vanilla_Wonder_Construction_Actions.md#nanbokuchou_end_event_emperor_effect-134-82cc76)：nanbokuchou_end_event_emperor_effect；change_building_level_in_location；[in_game/events/situations/nanbokuchou.txt:134](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/situations/nanbokuchou.txt:134>)。
- [sengoku.2](ED_Vanilla_Wonder_Construction_Actions.md#sengoku-2-63-8043e0)：战国时代的终结；destroy_building；[in_game/events/situations/sengoku.txt:63](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/situations/sengoku.txt:63>)。

1337 开局实例：`kyoto`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2619](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2619>)；`yoshino`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2623](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2623>)。

### granary — 谷仓

原版定义：[in_game/common/building_types/town_buildings.txt:120](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/town_buildings.txt:120>)。

- `is_foreign = no`
- `max_levels = guild_max_level`
- `build_time = government_build_time`

行为或条件引用：

- [expand_food_stockpiles](ED_Vanilla_Wonder_Construction_Actions.md#expand_food_stockpiles-476-3f3a5d)：扩大食物储备；construct_building；[in_game/common/parliament_issues/06_peasants_estate_parliament_issues.txt:476](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/parliament_issues/06_peasants_estate_parliament_issues.txt:476>)。
- `flavor_cas.132`：阿尔洪迪加的兴起；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_CAS.txt:8223](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_CAS.txt:8223>)。
- [flavor_mam.77](ED_Vanilla_Wonder_Construction_Actions.md#flavor_mam-77-4980-3a1e35)：地中海的粮仓；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_MAM.txt:4980](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_MAM.txt:4980>)。
- [flavor_nov.28](ED_Vanilla_Wonder_Construction_Actions.md#flavor_nov-28-1682-51d2dc)：[target_location.GetNameWithNoTooltip]建城；change_building_level_in_location；[in_game/events/DHE/flavor_NOV.txt:1682](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_NOV.txt:1682>)。

### grand_apartment — 大寓所

原版定义：[in_game/common/building_types/event_only_buildings.txt:362](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/event_only_buildings.txt:362>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `build_time = generic_town_build_time`
- `country_potential = { always = no }`
- `allow = { always = no }`

行为或条件引用：

- [flavor_eng.10](ED_Vanilla_Wonder_Construction_Actions.md#flavor_eng-10-897-cfcf19)：高塔寓所；construct_building；[in_game/events/DHE/flavor_ENG.txt:897](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_ENG.txt:897>)。

### grand_palace — 豪华宫殿

原版定义：[in_game/common/building_types/event_only_buildings.txt:41](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/event_only_buildings.txt:41>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `build_time = large_capital_build_time`
- `country_potential = { always = no }`
- `allow = { always = no }`
- `remove_if = { is_no_longer_capital = yes }`
- `custom_tags = { unique_palace }`

行为或条件引用：

- [construct_a_grand_palace_decision](ED_Vanilla_Wonder_Construction_Actions.md#construct_a_grand_palace_decision-187-57c555)：委托建造一座新宫殿；construct_building；[in_game/common/decisions/generic_age_decisions.txt:187](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/decisions/generic_age_decisions.txt:187>)。
- [random_event.34](ED_Vanilla_Wonder_Construction_Actions.md#random_event-34-1678-f69e59)：修建[ShowBuildingTypeNameWithNoTooltip('grand_palace')\|U]；construct_building；[in_game/events/random_event.txt:1678](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/random_event.txt:1678>)。

### grand_shipyard — 大船厂

原版定义：[in_game/common/building_types/port_buildings.txt:156](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/port_buildings.txt:156>)。

- `is_foreign = no`
- `max_levels = 1`
- `obsolete = shipyard`
- `location_potential = { is_port = yes }`
- `build_time = large_port_building_time`

行为或条件引用：

- [grand_shipyard_advance](ED_Vanilla_Wonder_Construction_Actions.md#grand_shipyard_advance-870-3be8a5)：大船厂；unlock_building；[in_game/common/advances/1_building_unlocks.txt:870](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/advances/1_building_unlocks.txt:870>)。
- `expand_docks`：扩建造船厂；门槛/关联引用；需看上下文；[in_game/common/parliament_issues/05_burghers_estate_parliament_issues.txt:673](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/parliament_issues/05_burghers_estate_parliament_issues.txt:673>)。
- `expand_dry_docks`：扩建造船厂；门槛/关联引用；需看上下文；[in_game/common/parliament_issues/05_burghers_estate_parliament_issues.txt:758](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/parliament_issues/05_burghers_estate_parliament_issues.txt:758>)。
- [expand_shipyards](ED_Vanilla_Wonder_Construction_Actions.md#expand_shipyards-844-428301)：扩建造船厂；门槛/关联引用；需看上下文；[in_game/common/parliament_issues/05_burghers_estate_parliament_issues.txt:844](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/parliament_issues/05_burghers_estate_parliament_issues.txt:844>)。
- [expand_grand_shipyards](ED_Vanilla_Wonder_Construction_Actions.md#expand_grand_shipyards-928-428301)：扩建造船厂；construct_building；[in_game/common/parliament_issues/05_burghers_estate_parliament_issues.txt:928](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/parliament_issues/05_burghers_estate_parliament_issues.txt:928>)。
- `has_dock_infrastructure`：has_dock_infrastructure；门槛/关联引用；需看上下文；[in_game/common/scripted_triggers/location_triggers.txt:150](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/scripted_triggers/location_triggers.txt:150>)。
- `unit_war_galleon_location_trigger`：unit_war_galleon_location_trigger；门槛/关联引用；需看上下文；[in_game/common/scripted_triggers/unit_triggers.txt:488](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/scripted_triggers/unit_triggers.txt:488>)。
- `flavor_mos.100`：第一位海军上将；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_MOS.txt:10031](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_MOS.txt:10031>)。

### great_enclosure — 大围场

原版定义：[in_game/common/building_types/unique_buildings.txt:4755](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:4755>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `location_potential = { counts_as_capital = yes this = location:great_zimbabwe }`
- `allow = { is_capital = yes country_has_no_other_copy_of_building = { type = great_enclosure } }`
- `country_potential = { has_or_had_tag = ZMW }`
- `build_time = huge_unique_build_time`

未在本次行为定义中发现显式同名引用；仍可能由建筑自身条件、科技/改革解锁或引擎常规建设入口提供。

1337 开局实例：`great_zimbabwe`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2454](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2454>)。

### great_hill_complex — 大丘墟

原版定义：[in_game/common/building_types/unique_buildings.txt:4789](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:4789>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `location_potential = { counts_as_capital = yes this = location:great_zimbabwe }`
- `allow = { is_capital = yes country_has_no_other_copy_of_building = { type = great_hill_complex } }`
- `country_potential = { has_or_had_tag = ZMW }`
- `build_time = huge_unique_build_time`

未在本次行为定义中发现显式同名引用；仍可能由建筑自身条件、科技/改革解锁或引擎常规建设入口提供。

1337 开局实例：`great_zimbabwe`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2455](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2455>)。

### great_madrasa — 大伊斯兰学院

原版定义：[in_game/common/building_types/event_only_buildings.txt:87](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/event_only_buildings.txt:87>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `build_time = religious_building_time`
- `country_potential = { always = no }`
- `allow = { always = no }`
- `remove_if = { location = { owner ?= { religion.group != religion_group:muslim } } }`

行为或条件引用：

- [sponsor_a_great_madrasa_decision](ED_Vanilla_Wonder_Construction_Actions.md#sponsor_a_great_madrasa_decision-99-57c555)：资助一座大伊斯兰学院；construct_building；[in_game/common/decisions/generic_age_decisions.txt:99](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/decisions/generic_age_decisions.txt:99>)。
- [progress_and_literacy](ED_Vanilla_Wonder_Construction_Actions.md#progress_and_literacy-1-4e560e)：进步与识字；门槛/关联引用；需看上下文；[in_game/common/missions/generic_progress_and_literacy_mission_pack.txt:1](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/missions/generic_progress_and_literacy_mission_pack.txt:1>)。
- [flavor_bng.5](ED_Vanilla_Wonder_Construction_Actions.md#flavor_bng-5-229-b36963)：潘杜阿的阿迪纳清真寺；construct_building；[in_game/events/DHE/flavor_bng.txt:229](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_bng.txt:229>)。
- `generic_mission_events.18`：[target_location.GetNameWithNoTooltip]的学者们；门槛/关联引用；需看上下文；[in_game/events/missionevents/generic_mission_events.txt:1312](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/missionevents/generic_mission_events.txt:1312>)。
- [muslim_school_events.3](ED_Vanilla_Wonder_Construction_Actions.md#muslim_school_events-3-121-8529b1)：新的伊斯兰学院；change_building_level_in_location；[in_game/events/religion/muslim_school_events.txt:121](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/religion/muslim_school_events.txt:121>)。

### great_temple_of_tenochtitlan — 特诺奇蒂特兰大神庙

原版定义：[in_game/common/building_types/event_only_buildings.txt:273](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/event_only_buildings.txt:273>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 7`
- `build_time = religious_building_time`
- `country_potential = { has_or_had_tag = TNC }`
- `allow = { owner = { has_unlocked_building_trigger = { type = great_temple_of_tenochtitlan } } }`
- `remove_if = { owner ?= { NOT = { religion ?= religion:nahuatl } } }`

行为或条件引用：

- [flavor_azt.70](ED_Vanilla_Wonder_Construction_Actions.md#flavor_azt-70-3-cdd86c)：特诺奇蒂特兰大金字塔；construct_building, unlock_building_effect；[in_game/events/DHE/flavor_AZT.txt:3](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_AZT.txt:3>)。
- `flavor_azt.80`：[target_character.GetNameWithNoTooltip]；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_AZT.txt:82](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_AZT.txt:82>)。
- [flavor_azt.200](ED_Vanilla_Wonder_Construction_Actions.md#flavor_azt-200-781-cdd86c)：特诺奇蒂特兰大神庙的重建；change_building_level_in_location；[in_game/events/DHE/flavor_AZT.txt:781](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_AZT.txt:781>)。

### great_valley_complex — 大谷邑

原版定义：[in_game/common/building_types/unique_buildings.txt:4823](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:4823>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `location_potential = { counts_as_capital = yes this = location:great_zimbabwe }`
- `allow = { is_capital = yes country_has_no_other_copy_of_building = { type = great_valley_complex } }`
- `country_potential = { has_or_had_tag = ZMW }`
- `build_time = huge_unique_build_time`

未在本次行为定义中发现显式同名引用；仍可能由建筑自身条件、科技/改革解锁或引擎常规建设入口提供。

1337 开局实例：`great_zimbabwe`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2456](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2456>)。

### greek_latin_academy — 希腊‑拉丁学院

原版定义：[in_game/common/building_types/unique_buildings.txt:3611](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:3611>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `country_potential = { custom_tooltip = { text = greek_latin_academy_why OR = { tag = MOS tag = RUS } has_variable = greek_latin_academy } }`
- `allow = { always = no }`
- `build_time = cultural_building_time`
- `location_potential = { this = location:moscow }`

行为或条件引用：

- [mos_greek_latin_academy_decision](ED_Vanilla_Wonder_Construction_Actions.md#mos_greek_latin_academy_decision-1238-f996cd)：建立$greek_latin_academy$；construct_building；[in_game/common/decisions/flavor_decisions_rus.txt:1238](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/decisions/flavor_decisions_rus.txt:1238>)。

### guich_garrison — 吉什戍营

原版定义：[in_game/common/building_types/event_only_buildings.txt:3290](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/event_only_buildings.txt:3290>)。

- `is_special = yes`
- `max_levels = 1`
- `build_time = small_fort_building`
- `country_potential = { has_unlocked_building_trigger = { type = guich_garrison } }`

行为或条件引用：

- [flavor_mor.31](ED_Vanilla_Wonder_Construction_Actions.md#flavor_mor-31-2053-587bc4)：建立吉什戍营；unlock_building_effect；[in_game/events/DHE/flavor_MOR.txt:2053](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_MOR.txt:2053>)。

### gurgaddi — 上师教坛

原版定义：[in_game/common/building_types/unique_buildings.txt:5334](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:5334>)。

- `is_special = yes`
- `max_levels = 1`
- `is_foreign = yes`
- `country_potential = { tag = SIKH }`
- `build_time = religious_building_time`

行为或条件引用：

- [sikhism.1](ED_Vanilla_Wonder_Construction_Actions.md#sikhism-1-61-6cddfc)：[ShowReligionAdjectiveWithNoTooltip('sikhism')]信仰；change_building_level_in_location；[in_game/events/religion/sikhism.txt:61](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/religion/sikhism.txt:61>)。
- [sikhism.5](ED_Vanilla_Wonder_Construction_Actions.md#sikhism-5-478-6cddfc)：[target_character.GetNameWithNoTooltip]；change_building_level_in_location；[in_game/events/religion/sikhism.txt:478](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/religion/sikhism.txt:478>)。
- [sikhism.13](ED_Vanilla_Wonder_Construction_Actions.md#sikhism-13-1096-6cddfc)：$character_title_guru$的消失；change_building_level_in_location；[in_game/events/religion/sikhism.txt:1096](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/religion/sikhism.txt:1096>)。

### gymnasium_building — 文理学院

原版定义：[in_game/common/building_types/unique_buildings.txt:6221](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:6221>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `country_potential = { has_reform = government_reform:study_of_the_classics }`
- `build_time = large_cultural_building_time`
- `location_potential = { counts_as_capital = yes }`
- `allow = { is_capital = yes country_has_no_other_copy_of_building = { type = gymnasium_building } }`
- `remove_if = { location.owner ?= { NOT = { has_reform = government_reform:study_of_the_classics } } }`

未在本次行为定义中发现显式同名引用；仍可能由建筑自身条件、科技/改革解锁或引擎常规建设入口提供。

### hanseatic_kontor — 汉萨商栈

原版定义：[in_game/common/building_types/unique_buildings.txt:89](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:89>)。

- `is_special = yes`
- `is_foreign = yes`
- `max_levels = hanseatic_kontor_max_level`
- `country_potential = { modifier:allows_hanseatic_federation_buildings = yes }`
- `build_time = trade_post_build_time`

行为或条件引用：

- `spread_reformation_through_trade`：通过贸易传播宗教改革；门槛/关联引用；需看上下文；[in_game/common/generic_actions/reformation.txt:1](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/generic_actions/reformation.txt:1>)。
- `disband_kontor`：拆除汉萨商栈；destroy_building_forcefully；[in_game/common/peace_treaties/disband_kontor.txt:1](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/peace_treaties/disband_kontor.txt:1>)。
- [flavor_brapru.9](ED_Vanilla_Wonder_Construction_Actions.md#flavor_brapru-9-490-4fbbec)：[ROOT.GetCountry.GetNameWithNoTooltip]的新都；destroy_all_buildings_of_type；[in_game/events/DHE/flavor_brapru.txt:490](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_brapru.txt:490>)。
- `flavor_hsa.5`：汉萨同盟印章；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_HSA.txt:249](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_HSA.txt:249>)。
- `flavor_hsa.7`：[target_country.GetAdjectiveWithNoTooltip]市政厅；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_HSA.txt:489](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_HSA.txt:489>)。
- [flavor_lit.1000](ED_Vanilla_Wonder_Construction_Actions.md#flavor_lit-1000-3548-a1868c)：[target_country2.GetAdjectiveWithNoTooltip]在考纳斯的影响力；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_LIT.txt:3548](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_LIT.txt:3548>)。
- [flavor_lit.1001](ED_Vanilla_Wonder_Construction_Actions.md#flavor_lit-1001-3618-a1868c)：[target_country2.GetAdjectiveWithNoTooltip]在[ShowLocationNameWithNoTooltip('kaunas')]的影响力；construct_building；[in_game/events/DHE/flavor_LIT.txt:3618](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_LIT.txt:3618>)。

1337 开局实例：`lubeck`，level=`3`，[main_menu/setup/1337/07_cities_and_buildings.txt:1318](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1318>)；`visby`，level=`2`，[main_menu/setup/1337/07_cities_and_buildings.txt:1319](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1319>)；`riga`，level=`2`，[main_menu/setup/1337/07_cities_and_buildings.txt:1320](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1320>)；`hamburg`，level=`2`，[main_menu/setup/1337/07_cities_and_buildings.txt:1321](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1321>)；`goslar`，level=`2`，[main_menu/setup/1337/07_cities_and_buildings.txt:1322](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1322>)；`bremen`，level=`2`，[main_menu/setup/1337/07_cities_and_buildings.txt:1323](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1323>)；`rostock`，level=`2`，[main_menu/setup/1337/07_cities_and_buildings.txt:1324](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1324>)；`wismar`，level=`2`，[main_menu/setup/1337/07_cities_and_buildings.txt:1325](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1325>)；`stralsund`，level=`2`，[main_menu/setup/1337/07_cities_and_buildings.txt:1327](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1327>)；`kiel`，level=`2`，[main_menu/setup/1337/07_cities_and_buildings.txt:1331](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1331>)；`wittenberg`，level=`2`，[main_menu/setup/1337/07_cities_and_buildings.txt:1332](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1332>)；`luneburg`，level=`2`，[main_menu/setup/1337/07_cities_and_buildings.txt:1333](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1333>)；`wolgast`，level=`2`，[main_menu/setup/1337/07_cities_and_buildings.txt:1336](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1336>)；`magdeburg`，level=`2`，[main_menu/setup/1337/07_cities_and_buildings.txt:1339](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1339>)；`stettin`，level=`2`，[main_menu/setup/1337/07_cities_and_buildings.txt:1345](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1345>)；`gdansk`，level=`2`，[main_menu/setup/1337/07_cities_and_buildings.txt:1348](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1348>)；`brunswick`，level=`2`，[main_menu/setup/1337/07_cities_and_buildings.txt:1350](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1350>)；`konigsberg`，level=`2`，[main_menu/setup/1337/07_cities_and_buildings.txt:1351](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1351>)；`cologne`，level=`2`，[main_menu/setup/1337/07_cities_and_buildings.txt:1353](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1353>)；`dortmund`，level=`2`，[main_menu/setup/1337/07_cities_and_buildings.txt:1354](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1354>)；`bruges`，level=`2`，[main_menu/setup/1337/07_cities_and_buildings.txt:1355](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1355>)；`antwerp`，level=`2`，[main_menu/setup/1337/07_cities_and_buildings.txt:1356](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1356>)；`berlin`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1357](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1357>)；`leipzig`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1359](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1359>)；`erfurt`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1367](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1367>)；`frankfurt`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1368](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1368>)；`paderborn`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1369](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1369>)；`dusseldorf`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1373](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1373>)；`osnabruck`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1375](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1375>)；`munster`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1376](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1376>)；`tallinn`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1380](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1380>)；`tartu`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1381](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1381>)；`london`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1382](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1382>)；`novgorod`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1383](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1383>)；`torun`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1384](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1384>)。

### hanseatic_shipwright_guild — 汉萨同盟造船公会

原版定义：[in_game/common/building_types/unique_buildings.txt:128](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:128>)。

- `is_special = yes`
- `is_foreign = yes`
- `max_levels = hanseatic_shipwright_guild_max_level`
- `country_potential = { modifier:allows_hanseatic_federation_buildings = yes }`
- `location_potential = { owner = { is_subject_of = c:HSA } is_port = yes }`
- `build_time = medium_port_building_time`

行为或条件引用：

- `flavor_hsa.7`：[target_country.GetAdjectiveWithNoTooltip]市政厅；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_HSA.txt:489](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_HSA.txt:489>)。

1337 开局实例：`hamburg`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1387](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1387>)；`lubeck`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1388](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1388>)。

### hanseatic_town_hall — 汉萨市政厅

原版定义：[in_game/common/building_types/unique_buildings.txt:164](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:164>)。

- `is_special = yes`
- `is_foreign = yes`
- `max_levels = 2`
- `location_potential = { this = c:HSA.capital }`
- `country_potential = { modifier:allows_hanseatic_federation_buildings = yes }`
- `build_time = large_capital_build_time`
- `remove_if = { owner = { NOT = { country_type = building } } }`

行为或条件引用：

- `flavor_hsa.7`：[target_country.GetAdjectiveWithNoTooltip]市政厅；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_HSA.txt:489](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_HSA.txt:489>)。

1337 开局实例：`lubeck`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1391](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1391>)。

### herrenchiemsee_abbey — 海伦基姆湖修道院

原版定义：[in_game/common/building_types/event_only_buildings.txt:3391](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/event_only_buildings.txt:3391>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `build_time = large_capital_build_time`
- `country_potential = { custom_tooltip = { text = herrenchiemsee_abbey_potential OR = { has_or_had_tag = BAV has_or_had_tag = LBV has_or_had_tag = UBV } } }`
- `allow = { always = no }`
- `location_potential = { this = location:munich }`

行为或条件引用：

- [flavor_bav.33](ED_Vanilla_Wonder_Construction_Actions.md#flavor_bav-33-1392-75be1b)：海伦基姆湖修道院的重建；construct_building；[in_game/events/DHE/flavor_bav.txt:1392](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_bav.txt:1392>)。

### hexamilion_wall — 六里墙

原版定义：[in_game/common/building_types/event_only_buildings.txt:1668](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/event_only_buildings.txt:1668>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `build_time = small_fort_building`
- `country_potential = { has_unlocked_building_trigger = { type = hexamilion_wall } }`
- `location_potential = { this = location:corinth }`

行为或条件引用：

- [flavor_byz.38](ED_Vanilla_Wonder_Construction_Actions.md#flavor_byz-38-2821-64397c)：六里墙；construct_building, unlock_building_effect；[in_game/events/DHE/flavor_BYZ.txt:2821](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_BYZ.txt:2821>)。

### hippodrome — 竞技场

原版定义：[in_game/common/building_types/unique_buildings.txt:6128](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:6128>)。

- `is_foreign = no`
- `max_levels = 1`
- `build_time = huge_unique_build_time`
- `country_potential = { has_dlc = "d008_fate_of_the_phoenix" OR = { has_or_had_tag = BYZ has_or_had_tag = ROM } }`
- `location_potential = { this = location:constantinople }`
- `allow = { custom_tooltip = { text = won_fate_of_the_phoenix_disaster_tt scope:actor = { has_variable = won_fate_of_the_phoenix_disaster_variable } } }`

未在本次行为定义中发现显式同名引用；仍可能由建筑自身条件、科技/改革解锁或引擎常规建设入口提供。

### hsa_burgtor — 城堡门

原版定义：[in_game/common/building_types/unique_buildings.txt:6281](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:6281>)。

- `is_special = yes`
- `is_foreign = yes`
- `max_levels = 2`
- `build_time = small_fort_building`
- `location_potential = { custom_tooltip = { text = location_owner_same_culture_group_as_us_tt owner ?= { culture = { any_culture_group = { any_culture_in_culture_group = { this = c:HSA.culture } } } } } }`
- `remove_if = { OR = { location.owner ?= { culture = { any_culture_group = { NOT = { any_culture_in_culture_group = { this = c:HSA.culture } } } } } location = { has_owner = no } location.owner ?= { is_at_war_with = root.owner } } }`

行为或条件引用：

- [hsa_hanseatic_fortifications](ED_Vanilla_Wonder_Construction_Actions.md#hsa_hanseatic_fortifications-57-fbe9b8)：$HSA_ADJ$要塞；unlock_building；[in_game/common/advances/country_hsa.txt:57](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/advances/country_hsa.txt:57>)。
- [flavor_lub.1](ED_Vanilla_Wonder_Construction_Actions.md#flavor_lub-1-3-5f4a7f)：[target_location.GetNameWithNoTooltip]城门；construct_building；[in_game/events/DHE/flavor_LUB.txt:3](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_LUB.txt:3>)。
- [flavor_lub.2](ED_Vanilla_Wonder_Construction_Actions.md#flavor_lub-2-84-5f4a7f)：[target_country2.GetNameWithNoTooltip]请求财政援助；construct_building；[in_game/events/DHE/flavor_LUB.txt:84](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_LUB.txt:84>)。
- [flavor_lub.3](ED_Vanilla_Wonder_Construction_Actions.md#flavor_lub-3-149-5f4a7f)：[target_country.GetNameWithNoTooltip]的回应；construct_building；[in_game/events/DHE/flavor_LUB.txt:149](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_LUB.txt:149>)。

### husuni_kubwa — 胡苏尼库布瓦宫

原版定义：[in_game/common/building_types/event_only_buildings.txt:2574](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/event_only_buildings.txt:2574>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `build_time = market_build_time`
- `country_potential = { custom_tooltip = { text = unlocked_husuni_kubwa_tt has_variable = unlocked_husuni_kubwa_variable } }`

行为或条件引用：

- [zan_husuni_kubwa_decision](ED_Vanilla_Wonder_Construction_Actions.md#zan_husuni_kubwa_decision-1390-a14531)：胡苏尼库布瓦宫；construct_building；[in_game/common/decisions/flavor_decisions_various.txt:1390](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/decisions/flavor_decisions_various.txt:1390>)。

### ibadat_khana — 敬拜辩论大殿

原版定义：[in_game/common/building_types/unique_buildings.txt:3512](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:3512>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `build_time = cultural_building_time`
- `country_potential = { does_not_own_any_copy_of_building_type = { type = ibadat_khana } }`

行为或条件引用：

- [mug_mughal_ibadat_khana](ED_Vanilla_Wonder_Construction_Actions.md#mug_mughal_ibadat_khana-24-b7cf8f)：敬拜辩论大殿；unlock_building；[in_game/common/advances/country_mug.txt:24](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/advances/country_mug.txt:24>)。
- [flavor_mug.10](ED_Vanilla_Wonder_Construction_Actions.md#flavor_mug-10-565-a6a566)：[target_location.GetNameWithNoTooltip]的敬拜辩论大殿；construct_building；[in_game/events/DHE/flavor_mug.txt:565](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_mug.txt:565>)。

### imperial_academy_of_arts — 帝国艺术学院

原版定义：[in_game/common/building_types/unique_buildings.txt:3927](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:3927>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `country_potential = { custom_tooltip = { text = imperial_academy_of_arts_why OR = { tag = MOS tag = RUS } has_variable = imperial_academy_of_arts } }`
- `allow = { always = no }`
- `build_time = cultural_building_time`
- `location_potential = { this = location:neva }`

行为或条件引用：

- [rus_imperial_academy_arts_decision](ED_Vanilla_Wonder_Construction_Actions.md#rus_imperial_academy_arts_decision-2107-f996cd)：帝国艺术学院；construct_building；[in_game/common/decisions/flavor_decisions_rus.txt:2107](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/decisions/flavor_decisions_rus.txt:2107>)。
- `flavor_rus.52`：皇家学会院士；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_RUS.txt:4269](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_RUS.txt:4269>)。
- [flavor_rus.70](ED_Vanilla_Wonder_Construction_Actions.md#flavor_rus-70-6009-201f60)：[yury_felten.GetNameWithNoTooltip]的精心改进；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_RUS.txt:6009](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_RUS.txt:6009>)。

### imperial_city_of_hue — $hue_location$皇城

原版定义：[in_game/common/building_types/event_only_buildings.txt:2646](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/event_only_buildings.txt:2646>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `build_time = large_cultural_building_time`
- `country_potential = { always = no }`
- `allow = { always = no }`

行为或条件引用：

- [flavor_dai.4](ED_Vanilla_Wonder_Construction_Actions.md#flavor_dai-4-276-cc4215)：皇城；construct_building；[in_game/events/DHE/flavor_dai.txt:276](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_dai.txt:276>)。

### imperial_halic_shipyards — 帝国造船厂

原版定义：[in_game/common/building_types/event_only_buildings.txt:582](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/event_only_buildings.txt:582>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `build_time = large_port_building_time`
- `country_potential = { always = no }`
- `allow = { always = no }`

行为或条件引用：

- [flavor_tur.15](ED_Vanilla_Wonder_Construction_Actions.md#flavor_tur-15-522-bf9554)：帝国造船厂；construct_building；[in_game/events/DHE/flavor_TUR.txt:522](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_TUR.txt:522>)。

### incamisana — 印加水庙

原版定义：[in_game/common/building_types/unique_buildings.txt:2218](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:2218>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `location_potential = { }`
- `build_time = rural_build_time`

行为或条件引用：

- [incamisana_advance](ED_Vanilla_Wonder_Construction_Actions.md#incamisana_advance-20-8aa708)：印加水庙；unlock_building；[in_game/common/advances/culture_andean.txt:20](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/advances/culture_andean.txt:20>)。

### institute_of_noble_maidens — 贵族女子学院

原版定义：[in_game/common/building_types/unique_buildings.txt:4045](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:4045>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `country_potential = { custom_tooltip = { text = institute_of_noble_maidens_why OR = { tag = MOS tag = RUS } has_variable = institute_of_noble_maidens } }`
- `allow = { always = no }`
- `build_time = cultural_building_time`
- `location_potential = { OR = { this = location:neva counts_as_capital = yes } }`

行为或条件引用：

- [rus_institute_of_noble_maidens_decision](ED_Vanilla_Wonder_Construction_Actions.md#rus_institute_of_noble_maidens_decision-2345-f996cd)：贵族女子学院；construct_building；[in_game/common/decisions/flavor_decisions_rus.txt:2345](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/decisions/flavor_decisions_rus.txt:2345>)。

### irrigation_systems — 灌溉系统

原版定义：[in_game/common/building_types/common_buildings.txt:1](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/common_buildings.txt:1>)。

- `is_foreign = no`
- `max_levels = irrigant_cap`
- `location_potential = { OR = { has_river = yes is_adjacent_to_lake = yes } or = { owner ?= { is_ai = no } raw_material ?= { is_food = yes } } }`
- `build_time = infrastructure_build_time`

行为或条件引用：

- [estate_cooperation](ED_Vanilla_Wonder_Construction_Actions.md#estate_cooperation-1-821312)：阶层合作；门槛/关联引用；需看上下文；[in_game/common/missions/generic_estate_cooperation_mission_pack.txt:1](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/missions/generic_estate_cooperation_mission_pack.txt:1>)。
- [generic_traditional_economy](ED_Vanilla_Wonder_Construction_Actions.md#generic_traditional_economy-1-1372be)：传统经济；门槛/关联引用；需看上下文；[in_game/common/missions/generic_traditional_economy_mission_pack.txt:1](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/missions/generic_traditional_economy_mission_pack.txt:1>)。
- [iberian_culture.25](ED_Vanilla_Wonder_Construction_Actions.md#iberian_culture-25-1554-54b62e)：维护灌溉系统；construct_building；[in_game/events/culture/culture_iberian.txt:1554](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/culture/culture_iberian.txt:1554>)。
- [flavor_dlh.34](ED_Vanilla_Wonder_Construction_Actions.md#flavor_dlh-34-2974-b76ea9)：帮助亚穆纳运河沿岸的地点；construct_building；[in_game/events/DHE/flavor_DLH.txt:2974](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_DLH.txt:2974>)。
- [flavor_nav.30](ED_Vanilla_Wonder_Construction_Actions.md#flavor_nav-30-1381-def420)：图德拉灌溉工程；construct_building；[in_game/events/DHE/flavor_NAV.txt:1381](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_NAV.txt:1381>)。
- [flavor_vij.24](ED_Vanilla_Wonder_Construction_Actions.md#flavor_vij-24-1334-2f8e63)：[target_location.GetNameWithNoTooltip]对水源的需求；construct_building；[in_game/events/DHE/flavor_vij.txt:1334](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_vij.txt:1334>)。
- [flavor_zan.6](ED_Vanilla_Wonder_Construction_Actions.md#flavor_zan-6-336-4912e7)：[target_country.GetNameWithNoTooltip]的崛起；construct_building；[in_game/events/DHE/flavor_ZAN.txt:336](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_ZAN.txt:336>)。
- [fall_of_delhi.17](ED_Vanilla_Wonder_Construction_Actions.md#fall_of_delhi-17-1465-c3cd9c)：亚穆纳河流域灌溉工程；construct_building；[in_game/events/situations/fall_of_delhi.txt:1465](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/situations/fall_of_delhi.txt:1465>)。

1337 开局实例：`cairo`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3816](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3816>)；`beng_mealea`，level=`2`，[main_menu/setup/1337/07_cities_and_buildings.txt:3849](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3849>)。

### janissary_barracks — 耶尼切里军营

原版定义：[in_game/common/building_types/unique_buildings.txt:1157](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:1157>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = janissary_barracks_size`
- `build_time = soldier_building`

行为或条件引用：

- [janissaries_advance](ED_Vanilla_Wonder_Construction_Actions.md#janissaries_advance-222-081e0a)：耶尼切里；unlock_building；[in_game/common/advances/country_tur.txt:222](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/advances/country_tur.txt:222>)。
- `tur_new_order_army_decision`：新秩序陆军；门槛/关联引用；需看上下文；[in_game/common/decisions/flavor_decisions_tur.txt:653](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/decisions/flavor_decisions_tur.txt:653>)。
- `flavor_tur.131`：狼群中的羊；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_TUR.txt:10054](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_TUR.txt:10054>)。
- `flavor_tur.180`：[target_location.GetNameWithNoTooltip]事变；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_TUR.txt:14353](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_TUR.txt:14353>)。

### jewish_district — 犹太区

原版定义：[in_game/common/building_types/event_only_buildings.txt:4141](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/event_only_buildings.txt:4141>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `build_time = large_cultural_building_time`
- `country_potential = { always = no }`
- `allow = { always = no }`
- `remove_if = { location = { "religion_percentage(religion:judaism)" = 0 } }`

行为或条件引用：

- [flavor_tur.206](ED_Vanilla_Wonder_Construction_Actions.md#flavor_tur-206-16247-bf9554)：[ShowReligionAdjectiveWithNoTooltip('judaism')]民族在塞萨洛尼基；construct_building；[in_game/events/DHE/flavor_TUR.txt:16247](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_TUR.txt:16247>)。

### kalari — 武术学校

原版定义：[in_game/common/building_types/unique_buildings.txt:3489](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:3489>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `build_time = soldier_building`
- `allow = { owner = { has_primary_or_accepted_culture = prev.dominant_culture } }`
- `remove_if = { NOT = { owner = { has_primary_or_accepted_culture = prev.location.dominant_culture } } }`

行为或条件引用：

- [kalaripayattu_advance](ED_Vanilla_Wonder_Construction_Actions.md#kalaripayattu_advance-39-5c02b9)：卡拉里帕亚特；unlock_building；[in_game/common/advances/culture_indian.txt:39](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/advances/culture_indian.txt:39>)。

### kastellet — 卡斯特雷特要塞

原版定义：[in_game/common/building_types/event_only_buildings.txt:2495](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/event_only_buildings.txt:2495>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `country_potential = { always = no }`
- `allow = { always = no }`
- `build_time = small_fort_building`
- `location_potential = { this = location:kobenhavn }`

行为或条件引用：

- [flavor_dan.29](ED_Vanilla_Wonder_Construction_Actions.md#flavor_dan-29-1986-6355b4)：卡斯特雷特要塞；construct_building；[in_game/events/DHE/flavor_dan.txt:1986](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_dan.txt:1986>)。

### khmer_baray — 人工湖

原版定义：[in_game/common/building_types/unique_buildings.txt:4902](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:4902>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `location_potential = { dominant_culture ?= culture:khmer_culture }`
- `country_potential = { OR = { tag = KHM culture ?= culture:khmer_culture } }`
- `build_time = huge_unique_build_time`

行为或条件引用：

- [flavor_khm.1000](ED_Vanilla_Wonder_Construction_Actions.md#flavor_khm-1000-3-53399f)：[target_location.GetNameWithNoTooltip]人工湖；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_khm.txt:3](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_khm.txt:3>)。
- [flavor_khm.1001](ED_Vanilla_Wonder_Construction_Actions.md#flavor_khm-1001-61-53399f)：吴哥水库失修；destroy_building；[in_game/events/DHE/flavor_khm.txt:61](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_khm.txt:61>)。

1337 开局实例：`angkor`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3848](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3848>)。

### kings_manor — 国王庄园

原版定义：[in_game/common/building_types/unique_buildings.txt:1841](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:1841>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `country_potential = { custom_tooltip = { text = kings_manor_why has_or_had_tag = ENG has_variable = council_of_the_north } }`
- `allow = { always = no }`
- `build_time = government_build_time`
- `location_potential = { is_capital = no is_historical_capital = no has_proximity_source_building = no }`

行为或条件引用：

- [eng_council_of_the_north_decision](ED_Vanilla_Wonder_Construction_Actions.md#eng_council_of_the_north_decision-184-b67bf8)：北方议会；construct_building；[in_game/common/decisions/flavor_decisions_eng.txt:184](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/decisions/flavor_decisions_eng.txt:184>)。

### kokufu — 国府

原版定义：[in_game/common/building_types/unique_buildings.txt:2473](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:2473>)。

- `is_special = yes`
- `is_foreign = yes`
- `max_levels = 1`
- `location_potential = { dominant_culture = { has_culture_group = culture_group:japanese_group } }`
- `country_potential = { OR = { AND = { has_reform = government_reform:japanese_imperial_family country_type = building } has_reform = government_reform:japanese_clan } }`
- `build_time = soldier_building`
- `allow = { custom_tooltip = { text = kokufu_why_tt always = no } }`

行为或条件引用：

- [grant_shugo_office](ED_Vanilla_Wonder_Construction_Actions.md#grant_shugo_office-1-1388a6)：授予守护之职；change_building_level_in_location；[in_game/common/generic_actions/japanese_shogunate.txt:1](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/generic_actions/japanese_shogunate.txt:1>)。
- [revoke_shugo_office](ED_Vanilla_Wonder_Construction_Actions.md#revoke_shugo_office-136-1388a6)：撤销守护之职；destroy_building；[in_game/common/generic_actions/japanese_shogunate.txt:136](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/generic_actions/japanese_shogunate.txt:136>)。
- [claim_shugo_office](ED_Vanilla_Wonder_Construction_Actions.md#claim_shugo_office-251-1388a6)：宣称守护之职；change_building_level_in_location；[in_game/common/generic_actions/japanese_shogunate.txt:251](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/generic_actions/japanese_shogunate.txt:251>)。
- [peace_expand_clan_influence](ED_Vanilla_Wonder_Construction_Actions.md#peace_expand_clan_influence-1-19f6b9)：扩张大名影响力；门槛/关联引用；需看上下文；[in_game/common/peace_treaties/expand_clan_influence.txt:1](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/peace_treaties/expand_clan_influence.txt:1>)。

1337 开局实例：`takaichi`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2629](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2629>)；`izumi`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2630](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2630>)；`osaka`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2631](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2631>)；`iga`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2632](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2632>)；`suzuka`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2633](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2633>)；`shima`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2634](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2634>)；`nakajima`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2635](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2635>)；`hoi`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2636](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2636>)；`toyoda`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2637](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2637>)；`abe`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2638](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2638>)；`tagata`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2639](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2639>)；`yatsushiro`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2640](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2640>)；`tama`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2642](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2642>)；`awa`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2643](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2643>)；`ichihara`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2644](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2644>)；`katsushika`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2645](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2645>)；`ibaraki`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2646](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2646>)；`kurita`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2647](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2647>)；`fuwa_mino`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2648](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2648>)；`kamioono`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2649](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2649>)；`tsukama`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2650](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2650>)；`gunma`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2651](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2651>)；`tsuga`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2652](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2652>)；`miyagi`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2653](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2653>)；`kamiura`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2654](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2654>)；`onyuu`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2655](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2655>)；`nyuu`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2656](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2656>)；`nomi`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2657](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2657>)；`noto_jap`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2658](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2658>)；`imizu`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2659](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2659>)；`higashikubiki`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2660](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2660>)；`sawata`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2661](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2661>)；`kuwada`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2662](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2662>)；`kasa`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2663](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2663>)；`keta_tajima`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2664](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2664>)；`houmi`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2665](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2665>)；`kume_houki`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2666](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2666>)；`ou`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2667](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2667>)；`naka_iwami`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2668](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2668>)；`oki`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2669](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2669>)；`shikama`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2670](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2670>)；`joutou`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2672](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2672>)；`kaya`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2673](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2673>)；`ashida`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2674](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2674>)；`aki`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2675](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2675>)；`saba`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2676](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2676>)；`toyoura`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2677](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2677>)；`kaisou`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2678](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2678>)；`awaji`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2679](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2679>)；`nakata`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2680](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2680>)；`aya`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2681](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2681>)；`ochi`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2682](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2682>)；`nagaoka`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2683](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2683>)；`mikasa`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2684](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2684>)；`mii`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2685](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2685>)；`nakatsu`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2686](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2686>)；`ooita`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2687](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2687>)；`saga`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2688](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2688>)；`akita_kumamoto`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2689](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2689>)；`koyu`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2690](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2690>)；`soo`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2691](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2691>)；`satsuma`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2692](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2692>)；`shimoagata`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2694](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2694>)。

### korean_barracks — 朝鲜训局

原版定义：[in_game/common/building_types/00_unique_buildings_to_make_obsolete.txt:48](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/00_unique_buildings_to_make_obsolete.txt:48>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `build_time = soldier_building`
- `allow = { owner = { has_primary_or_accepted_culture = prev.dominant_culture } }`
- `remove_if = { NOT = { owner = { has_primary_or_accepted_culture = prev.location.dominant_culture } } }`

行为或条件引用：

- [kor_korean_barracks_advance](ED_Vanilla_Wonder_Construction_Actions.md#kor_korean_barracks_advance-24-405998)：朝鲜训局；unlock_building；[in_game/common/advances/country_kor.txt:24](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/advances/country_kor.txt:24>)。

### korean_gunnery_coastal_defense — 朝鲜海防炮台

原版定义：[in_game/common/building_types/unique_buildings.txt:3057](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:3057>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `build_time = small_fort_building`
- `allow = { has_fort = yes NOT = { has_building = building_type:korean_gunnery_land_defense } }`
- `location_potential = { is_port = yes }`

行为或条件引用：

- [kor_korean_gunnery](ED_Vanilla_Wonder_Construction_Actions.md#kor_korean_gunnery-65-405998)：朝鲜火炮台；unlock_building；[in_game/common/advances/country_kor.txt:65](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/advances/country_kor.txt:65>)。

### korean_gunnery_land_defense — 朝鲜陆防炮台

原版定义：[in_game/common/building_types/unique_buildings.txt:3032](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:3032>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `build_time = small_fort_building`
- `allow = { has_fort = yes NOT = { has_building = building_type:korean_gunnery_coastal_defense } }`

行为或条件引用：

- [kor_korean_gunnery](ED_Vanilla_Wonder_Construction_Actions.md#kor_korean_gunnery-65-405998)：朝鲜火炮台；unlock_building；[in_game/common/advances/country_kor.txt:65](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/advances/country_kor.txt:65>)。

### kremlin — 克里姆林宫

原版定义：[in_game/common/building_types/unique_buildings.txt:3086](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:3086>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = kremlin_max_level`
- `country_potential = { custom_tooltip = { text = kremlin_why OR = { tag = MOS tag = RUS } has_variable = kremlin } }`
- `location_potential = { this = location:moscow }`
- `build_time = huge_unique_build_time`

行为或条件引用：

- [mos_build_kremlin_decision](ED_Vanilla_Wonder_Construction_Actions.md#mos_build_kremlin_decision-131-f996cd)：建造克里姆林宫；construct_building；[in_game/common/decisions/flavor_decisions_rus.txt:131](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/decisions/flavor_decisions_rus.txt:131>)。
- [flavor_mos.28](ED_Vanilla_Wonder_Construction_Actions.md#flavor_mos-28-2275-c719bc)：诞神女安息大教堂；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_MOS.txt:2275](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_MOS.txt:2275>)。
- [flavor_mos.34](ED_Vanilla_Wonder_Construction_Actions.md#flavor_mos-34-2786-c719bc)：[ridolfo_fioravanti.GetNameWithNoTooltip]；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_MOS.txt:2786](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_MOS.txt:2786>)。
- `flavor_mos.35`：[marco_ruffo.GetNameWithNoTooltip]；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_MOS.txt:2906](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_MOS.txt:2906>)。
- [flavor_mos.37](ED_Vanilla_Wonder_Construction_Actions.md#flavor_mos-37-3217-c719bc)：莫斯科大火；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_MOS.txt:3217](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_MOS.txt:3217>)。
- [flavor_mos.57](ED_Vanilla_Wonder_Construction_Actions.md#flavor_mos-57-5947-c719bc)：扩建克里姆林宫；change_building_level_in_location；[in_game/events/DHE/flavor_MOS.txt:5947](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_MOS.txt:5947>)。
- [flavor_mos.58](ED_Vanilla_Wonder_Construction_Actions.md#flavor_mos-58-6067-c719bc)：伊凡大帝钟楼；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_MOS.txt:6067](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_MOS.txt:6067>)。
- [flavor_mos.62](ED_Vanilla_Wonder_Construction_Actions.md#flavor_mos-62-6462-c719bc)：圣瓦西里大教堂；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_MOS.txt:6462](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_MOS.txt:6462>)。

### kronborg — 克龙堡

原版定义：[in_game/common/building_types/event_only_buildings.txt:2534](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/event_only_buildings.txt:2534>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `country_potential = { always = no }`
- `allow = { always = no }`
- `build_time = small_fort_building`
- `location_potential = { this = location:helsingor }`

行为或条件引用：

- [flavor_dan.31](ED_Vanilla_Wonder_Construction_Actions.md#flavor_dan-31-2087-6355b4)：克龙堡；construct_building；[in_game/events/DHE/flavor_dan.txt:2087](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_dan.txt:2087>)。

### kurmina_headquarter — 库尔米纳治所

原版定义：[in_game/common/building_types/unique_buildings.txt:4714](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:4714>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = kurmina_headquarter_max_level`
- `build_time = medium_soldier_building`
- `country_potential = { modifier:can_build_kurmina_headquarter = yes }`
- `remove_if = { root.owner = { modifier:can_build_kurmina_headquarter = no } }`

未在本次行为定义中发现显式同名引用；仍可能由建筑自身条件、科技/改革解锁或引擎常规建设入口提供。

### kurultai — 忽里勒台

原版定义：[in_game/common/building_types/unique_buildings.txt:326](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:326>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = kurultai_max_level`
- `country_potential = { has_advance = kurultai_advance government_type ?= government_type:steppe_horde }`
- `location_potential = { custom_tooltip = { text = dominant_culture_is_of_steppe_group dominant_culture = { has_culture_group = culture_group:steppe_group } } }`
- `remove_if = { OR = { NOT = { owner = { has_advance = kurultai_advance } } owner = { government_type != government_type:steppe_horde } } }`
- `build_time = soldier_building`

行为或条件引用：

- [kurultai_advance](ED_Vanilla_Wonder_Construction_Actions.md#kurultai_advance-23-a83aa2)：忽里勒台大会；unlock_building；[in_game/common/advances/government_steppe_horde.txt:23](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/advances/government_steppe_horde.txt:23>)。
- [on_shatter_country](ED_Vanilla_Wonder_Construction_Actions.md#on_shatter_country-6239-fff745)：on_shatter_country；destroy_building；[in_game/common/on_action/_hardcoded.txt:6239](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/on_action/_hardcoded.txt:6239>)。
- [flavor_chb.1](ED_Vanilla_Wonder_Construction_Actions.md#flavor_chb-1-3-b43787)：[target_character.GetNameWithNoTooltip]反叛；construct_building；[in_game/events/DHE/flavor_chb.txt:3](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_chb.txt:3>)。
- [flavor_tim.8](ED_Vanilla_Wonder_Construction_Actions.md#flavor_tim-8-445-272e59)：[target_character.GetShortNameWithNoTooltip]的崛起；construct_building；[in_game/events/DHE/flavor_tim.txt:445](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_tim.txt:445>)。
- `steppe_horde.7`：权力所在地；门槛/关联引用；需看上下文；[in_game/events/government/steppe_horde.txt:299](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/government/steppe_horde.txt:299>)。

1337 开局实例：`sarai_al_jadid`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1267](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1267>)；`astrakhan`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1268](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1268>)；`chimgi_tura`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1269](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1269>)；`kazan`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1270](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1270>)；`majar`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1271](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1271>)；`sarayjuk`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1272](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1272>)；`almaliq`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1274](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1274>)；`almaty`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1275](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1275>)；`balasagun`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1276](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1276>)；`gorgan`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1278](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1278>)；`nishapur`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1279](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1279>)；`basra`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1280](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1280>)；`samarra`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1282](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1282>)；`tabriz`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1283](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1283>)；`baghdad`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1284](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1284>)；`darab`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1285](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1285>)；`qatruyeh`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1286](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1286>)；`ghazni`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1287](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1287>)；`kabul`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1288](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1288>)；`deh_kundi`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1289](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1289>)；`maymana`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1290](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1290>)；`andkhoy`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1291](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1291>)；`balkh`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1292](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1292>)；`akhsisek`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1293](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1293>)；`samarkand`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1294](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1294>)；`vakhs`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1295](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1295>)；`khujand`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1296](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1296>)；`kashgar`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1297](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1297>)；`naomao`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1298](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1298>)；`khar_balgas`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1299](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1299>)；`zavkhan`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1300](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1300>)；`bulgan`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1301](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1301>)；`balj`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1302](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1302>)；`qingzhou_mongol`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1304](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1304>)；`taizhou_jurchen`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1305](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1305>)；`boorj`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1306](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1306>)；`kurchum`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1308](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1308>)。

### library — 图书馆

原版定义：[in_game/common/building_types/culture_buildings.txt:54](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/culture_buildings.txt:54>)。

- `is_foreign = no`
- `max_levels = 1`
- `build_time = cultural_building_time`
- `allow = { trigger_if = { limit = { has_dlc = "d009_across_the_pillars" this = location:cordoba has_building = building_type:library_cordoba } NOT = { has_building = building_type:library_cordoba } } }`

行为或条件引用：

- [library_advance](ED_Vanilla_Wonder_Construction_Actions.md#library_advance-1011-3be8a5)：图书馆；unlock_building；[in_game/common/advances/1_building_unlocks.txt:1011](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/advances/1_building_unlocks.txt:1011>)。
- [progress_and_literacy](ED_Vanilla_Wonder_Construction_Actions.md#progress_and_literacy-1-4e560e)：进步与识字；门槛/关联引用；需看上下文；[in_game/common/missions/generic_progress_and_literacy_mission_pack.txt:1](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/missions/generic_progress_and_literacy_mission_pack.txt:1>)。
- `scholars_calling`：学者；门槛/关联引用；需看上下文；[in_game/common/religious_order_callings/00_monastic.txt:44](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/religious_order_callings/00_monastic.txt:44>)。
- [flavor_byz.29](ED_Vanilla_Wonder_Construction_Actions.md#flavor_byz-29-2197-64397c)：普世博学馆；construct_building；[in_game/events/DHE/flavor_BYZ.txt:2197](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_BYZ.txt:2197>)。
- [flavor_cas.117](ED_Vanilla_Wonder_Construction_Actions.md#flavor_cas-117-7342-9abc78)：圣老楞佐修道院图书馆；construct_building；[in_game/events/DHE/flavor_CAS.txt:7342](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_CAS.txt:7342>)。
- `flavor_flo.36`：[target_artist.GetNameWithNoTooltip]；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_flo.txt:1004](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_flo.txt:1004>)。
- [flavor_pap.13](ED_Vanilla_Wonder_Construction_Actions.md#flavor_pap-13-661-09eb6b)：梵蒂冈图书馆；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_pap.txt:661](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_pap.txt:661>)。
- [flavor_plc.12](ED_Vanilla_Wonder_Construction_Actions.md#flavor_plc-12-749-8d2ab7)：扎武斯基图书馆；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_plc.txt:749](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_plc.txt:749>)。
- [flavor_tur.147](ED_Vanilla_Wonder_Construction_Actions.md#flavor_tur-147-11400-bf9554)：智慧之屋；change_building_level_in_location, construct_building；[in_game/events/DHE/flavor_TUR.txt:11400](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_TUR.txt:11400>)。
- `flavor_ven.32`：[ShowInstitutionNameWithNoTooltip('renaissance')]时期的[ROOT.GetCountry.GetNameWithNoTooltip]；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_VEN.txt:1518](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_VEN.txt:1518>)。
- `imperial_examination_events.7`：人中翘楚；门槛/关联引用；需看上下文；[in_game/events/imperial_examination_events.txt:608](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/imperial_examination_events.txt:608>)。
- `generic_mission_events.22`：[target_location.GetNameWithNoTooltip]图书馆；门槛/关联引用；需看上下文；[in_game/events/missionevents/generic_mission_events.txt:1640](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/missionevents/generic_mission_events.txt:1640>)。
- [war_of_religions.18](ED_Vanilla_Wonder_Construction_Actions.md#war_of_religions-18-1187-ce2cf2)：[target_location.GetNameWithNoTooltip]之掠；门槛/关联引用；需看上下文；[in_game/events/situations/war_of_religions.txt:1187](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/situations/war_of_religions.txt:1187>)。

### library_of_vijayanagar — $vijayanagar$大图书馆

原版定义：[in_game/common/building_types/event_only_buildings.txt:2194](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/event_only_buildings.txt:2194>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `build_time = large_cultural_building_time`
- `country_potential = { always = no }`
- `allow = { always = no }`

行为或条件引用：

- [flavor_vij.16](ED_Vanilla_Wonder_Construction_Actions.md#flavor_vij-16-850-2f8e63)：博学之城；construct_building；[in_game/events/DHE/flavor_vij.txt:850](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_vij.txt:850>)。
- [flavor_vij.17](ED_Vanilla_Wonder_Construction_Actions.md#flavor_vij-17-901-2f8e63)：[target_location.GetNameWithNoTooltip]，胜利之城；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_vij.txt:901](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_vij.txt:901>)。

### lieutenancy — 副王治所

原版定义：[in_game/common/building_types/unique_buildings.txt:1344](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:1344>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `build_time = government_build_time`
- `location_potential = { trigger_if = { limit = { exists = owner } is_capital = no is_historical_capital = no has_proximity_source_building = no trigger_if = { limit = { has_dlc = "d009_across_the_pillars" } OR = { AND = { is_in_scripted_geography = scripted_geography:castile_geography owner = { has_bureaucracy_of_type = bureaucracy_type:spa_council_of_castile_bureaucracy } } AND = { is_in_scripted_geography = scripted_geography:aragon_geography owner = { has_bureaucracy_of_type = bureaucracy_type:spa_council_of_aragon_bureaucracy } } AND = { is_in_scripted_geography = scripted_geography:portugal_geography owner = { has_bureaucracy_of_type = bureaucracy_type:spa_council_of_portugal_bureaucracy } } AND = { is_in_scripted_geography = scripted_geography:spanish_netherlands_geography owner = { has_bureaucracy_of_type = bureaucracy_type:spa_council_of_flanders_bureaucracy } } AND = { region = region:italy_region owner = { has_bureaucracy_of_type = bureaucracy_type:spa_council_of_italy_bureaucracy } } } } trigger_else = { has_road_to_capital = yes } } trigger_else = { always = no } }`
- `country_potential = { culture = { has_culture_group = culture_group:iberian_group } OR = { government_type ?= government_type:monarchy government_type ?= government_type:theocracy government_type ?= government_type:republic } }`
- `allow = { trigger_if = { limit = { has_dlc = "d009_across_the_pillars" } custom_tooltip = { text = lieutenancy_dlc_tt scope:actor = { total_building_levels_including_construction:lieutenancy < modifier:num_lieutenancy } } } trigger_else = { custom_tooltip = { text = lieutenancy_tt scope:actor = { total_building_levels_including_construction:local_governor < { value = effective_num_local_governors subtract = total_building_levels_including_construction:lieutenancy subtract = total_building_levels_including_construction:itinerant_court_seat subtract = total_building_levels_including_construction:kings_manor } } } } owner = scope:actor }`
- `remove_if = { trigger_if = { limit = { has_dlc = "d009_across_the_pillars" } NOT = { OR = { AND = { location = { is_in_scripted_geography = scripted_geography:castile_geography } owner = { has_bureaucracy_of_type = bureaucracy_type:spa_council_of_castile_bureaucracy } } AND = { location = { is_in_scripted_geography = scripted_geography:aragon_geography } owner = { has_bureaucracy_of_type = bureaucracy_type:spa_council_of_aragon_bureaucracy } } AND = { location = { is_in_scripted_geography = scripted_geography:portugal_geography } owner = { has_bureaucracy_of_type = bureaucracy_type:spa_council_of_portugal_bureaucracy } } AND = { location = { is_in_scripted_geography = scripted_geography:spanish_netherlands_geography } owner = { has_bureaucracy_of_type = bureaucracy_type:spa_council_of_flanders_bureaucracy } } AND = { location = { region = region:italy_region } owner = { has_bureaucracy_of_type = bureaucracy_type:spa_council_of_italy_bureaucracy } } } } } trigger_else = { location = { has_road_to_capital = no } NOT = { owner = { at_war = yes } } NOT = { owner = { in_civil_war = yes } } } }`

行为或条件引用：

- [lieutenancy_advance](ED_Vanilla_Wonder_Construction_Actions.md#lieutenancy_advance-123-046a45)：副王；unlock_building；[in_game/common/advances/region_iberia.txt:123](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/advances/region_iberia.txt:123>)。

### lighthouse_of_alexandria — 亚历山大灯塔

原版定义：[in_game/common/building_types/event_only_buildings.txt:2891](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/event_only_buildings.txt:2891>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `build_time = small_fort_building`
- `country_potential = { always = no }`
- `allow = { always = no }`

行为或条件引用：

- [flavor_mam.40](ED_Vanilla_Wonder_Construction_Actions.md#flavor_mam-40-2273-3a1e35)：亚历山大的骄傲；construct_building；[in_game/events/DHE/flavor_MAM.txt:2273](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_MAM.txt:2273>)。

### llotja_seda — 丝绸交易厅

原版定义：[in_game/common/building_types/event_only_buildings.txt:673](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/event_only_buildings.txt:673>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `build_time = guild_build_time`
- `country_potential = { always = no }`
- `allow = { always = no }`

行为或条件引用：

- [flavor_ara.106](ED_Vanilla_Wonder_Construction_Actions.md#flavor_ara-106-2349-e41b99)：丝绸交易厅；construct_building；[in_game/events/DHE/flavor_ARA.txt:2349](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_ARA.txt:2349>)。

### local_shrine — 地方神庙

原版定义：[in_game/common/building_types/estate_buildings.txt:499](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/estate_buildings.txt:499>)。

- `is_foreign = no`
- `max_levels = estate_building_single_level`
- `build_time = estate_build_time`
- `country_potential = { }`

行为或条件引用：

- [pa_remove_local_shrine](ED_Vanilla_Wonder_Construction_Actions.md#pa_remove_local_shrine-876-cf85e0)：处理关于$local_shrine$的投诉；change_building_level_in_location；[in_game/common/parliament_agendas/03_buildings.txt:876](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/parliament_agendas/03_buildings.txt:876>)。

### maghreb_palm_irrigation — 杈状灌溉网络

原版定义：[in_game/common/building_types/unique_buildings.txt:825](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:825>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `country_potential = { OR = { culture = { has_culture_group = culture_group:maghrebi_group } culture = { has_culture_group = culture_group:amazigh_group } } }`
- `allow = { climate = arid OR = { vegetation = desert vegetation = sparse } OR = { region = region:maghreb_region region = region:sahel_region } }`
- `build_time = trade_post_build_time`

行为或条件引用：

- [maghrebi_culture.7](ED_Vanilla_Wonder_Construction_Actions.md#maghrebi_culture-7-379-2ffcc5)：[target_location.GetNameWithNoTooltip]的棕榈式灌溉渠；construct_building；[in_game/events/culture/culture_maghrebi.txt:379](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/culture/culture_maghrebi.txt:379>)。
- [maghrebi_culture.11](ED_Vanilla_Wonder_Construction_Actions.md#maghrebi_culture-11-671-2ffcc5)：[target_location.GetNameWithNoTooltip]的繁荣农业；门槛/关联引用；需看上下文；[in_game/events/culture/culture_maghrebi.txt:671](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/culture/culture_maghrebi.txt:671>)。

### magistrato_alla_sanita — 卫生法庭

原版定义：[in_game/common/building_types/event_only_buildings.txt:2620](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/event_only_buildings.txt:2620>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `build_time = large_cultural_building_time`
- `country_potential = { always = no }`
- `allow = { always = no }`

行为或条件引用：

- [flavor_ven.72](ED_Vanilla_Wonder_Construction_Actions.md#flavor_ven-72-3508-888d6c)：卫生法庭；construct_building；[in_game/events/DHE/flavor_VEN.txt:3508](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_VEN.txt:3508>)。

### mahmud_gawan_madrasa — 马茂德·加万回学院

原版定义：[in_game/common/building_types/event_only_buildings.txt:3112](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/event_only_buildings.txt:3112>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `build_time = large_cultural_building_time`
- `country_potential = { always = no }`
- `allow = { always = no }`
- `remove_if = { location = { owner ?= { religion.group != religion_group:muslim } } }`

行为或条件引用：

- [flavor_bah.1](ED_Vanilla_Wonder_Construction_Actions.md#flavor_bah-1-5-5e4c27)：马茂德·加万回学院；construct_building；[in_game/events/DHE/flavor_bah.txt:5](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_bah.txt:5>)。

### mamluk_barracks — $mamluk$军营

原版定义：[in_game/common/building_types/unique_buildings.txt:4618](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:4618>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 3`
- `build_time = soldier_building`
- `country_potential = { modifier:can_build_mamluk_barracks = yes }`

未在本次行为定义中发现显式同名引用；仍可能由建筑自身条件、科技/改革解锁或引擎常规建设入口提供。

1337 开局实例：`cairo`，level=`3`，[main_menu/setup/1337/07_cities_and_buildings.txt:3808](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3808>)；`alexandria`，level=`2`，[main_menu/setup/1337/07_cities_and_buildings.txt:3809](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3809>)；`damietta`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3810](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3810>)；`mansoura`，level=`2`，[main_menu/setup/1337/07_cities_and_buildings.txt:3811](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3811>)；`jerusalem`，level=`3`，[main_menu/setup/1337/07_cities_and_buildings.txt:3812](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3812>)。

### maniot_toll_guards — 马尼人卡哨

原版定义：[in_game/common/building_types/event_only_buildings.txt:4051](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/event_only_buildings.txt:4051>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `build_time = estate_build_time`
- `country_potential = { always = no }`
- `allow = { always = no }`

行为或条件引用：

- `flavor_tur.191`：马尼人；construct_estate_building；[in_game/events/DHE/flavor_TUR.txt:15244](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_TUR.txt:15244>)。

### miaphysite_monastery — 合性派修道院

原版定义：[in_game/common/building_types/religion_buildings.txt:278](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/religion_buildings.txt:278>)。

- `is_foreign = no`
- `max_levels = 1`
- `build_time = religious_building_time`
- `country_potential = { religion ?= religion:miaphysite }`

行为或条件引用：

- [pa_construct_monastery](ED_Vanilla_Wonder_Construction_Actions.md#pa_construct_monastery-914-cf85e0)：要求新修道院；construct_building；[in_game/common/parliament_agendas/03_buildings.txt:914](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/parliament_agendas/03_buildings.txt:914>)。
- [fund_monastery_network](ED_Vanilla_Wonder_Construction_Actions.md#fund_monastery_network-834-9aef90)：资助修道院体系；construct_building；[in_game/common/parliament_issues/07_expansion_parliament_issues.txt:834](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/parliament_issues/07_expansion_parliament_issues.txt:834>)。
- [flavor_eth.100](ED_Vanilla_Wonder_Construction_Actions.md#flavor_eth-100-724-2d218a)：修士会；change_building_level_in_location；[in_game/events/DHE/flavor_ETH.txt:724](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_ETH.txt:724>)。
- [flavor_eth.153](ED_Vanilla_Wonder_Construction_Actions.md#flavor_eth-153-1372-2d218a)：埃格齐亚贝尔山大教堂；construct_building；[in_game/events/DHE/flavor_ETH.txt:1372](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_ETH.txt:1372>)。
- [build_miaphysite_monastery](ED_Vanilla_Wonder_Construction_Actions.md#build_miaphysite_monastery-1941-2d218a)：build_miaphysite_monastery；construct_building；[in_game/events/DHE/flavor_ETH.txt:1941](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_ETH.txt:1941>)。
- [if_exists_destroy_monastery](ED_Vanilla_Wonder_Construction_Actions.md#if_exists_destroy_monastery-2163-2d218a)：if_exists_destroy_monastery；destroy_building；[in_game/events/DHE/flavor_ETH.txt:2163](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_ETH.txt:2163>)。
- [flavor_eth.202](ED_Vanilla_Wonder_Construction_Actions.md#flavor_eth-202-2173-2d218a)：[ewostatewos.GetNameWithNoTooltip]的七位门徒；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_ETH.txt:2173](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_ETH.txt:2173>)。
- [flavor_eth.203](ED_Vanilla_Wonder_Construction_Actions.md#flavor_eth-203-2282-2d218a)：加深的裂痕；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_ETH.txt:2282](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_ETH.txt:2282>)。
- [flavor_eth.204](ED_Vanilla_Wonder_Construction_Actions.md#flavor_eth-204-2392-2d218a)：[ewostatewos.GetNameWithNoTooltip]之家；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_ETH.txt:2392](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_ETH.txt:2392>)。
- [flavor_eth.240](ED_Vanilla_Wonder_Construction_Actions.md#flavor_eth-240-2701-2d218a)：天空中闪耀的新光；change_building_level_in_location；[in_game/events/DHE/flavor_ETH.txt:2701](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_ETH.txt:2701>)。
- [miaphysite_flavor.31](ED_Vanilla_Wonder_Construction_Actions.md#miaphysite_flavor-31-669-53c86d)：白色修道院；change_building_level_in_location；[in_game/events/religion/miaphsyite_flavor.txt:669](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/religion/miaphsyite_flavor.txt:669>)。

1337 开局实例：`senafe`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2420](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2420>)；`debre_libanos`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2421](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2421>)；`shire`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2422](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2422>)；`yeha`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2423](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2423>)；`kubar`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2424](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2424>)；`hayq`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2425](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2425>)；`keren`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2426](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2426>)。

### mil_vatican_library — 梵蒂冈图书馆：军事侧

原版定义：[in_game/common/building_types/event_only_buildings.txt:1146](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/event_only_buildings.txt:1146>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `build_time = large_cultural_building_time`
- `country_potential = { always = no }`

行为或条件引用：

- [flavor_pap.13](ED_Vanilla_Wonder_Construction_Actions.md#flavor_pap-13-661-09eb6b)：梵蒂冈图书馆；change_building_level_in_location；[in_game/events/DHE/flavor_pap.txt:661](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_pap.txt:661>)。

### monastery — 修道院

原版定义：[in_game/common/building_types/religion_buildings.txt:1](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/religion_buildings.txt:1>)。

- `is_foreign = no`
- `max_levels = 1`
- `build_time = religious_building_time`
- `country_potential = { modifier:can_have_monasteries = yes }`
- `on_built = { if = { limit = { location.owner = { religion = { has_sects = yes } is_member_of_international_organization_of_type = { type = sect } } } location.owner = { random_international_organizations_member_of = { limit = { international_organization_type = international_organization_type:sect NOT = { any_international_organization_enemy = { this = root.owner } } NOT = { has_location = root.location } } add_location_to_international_organization = root.location } } } }`

行为或条件引用：

- `eng_austere_monastic_life_decision`：修道院改革；门槛/关联引用；需看上下文；[in_game/common/decisions/flavor_decisions_eng.txt:249](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/decisions/flavor_decisions_eng.txt:249>)。
- `austere_monastic_life`：修道院苦修生活；门槛/关联引用；需看上下文；[in_game/common/estate_privileges/clergy_estate.txt:502](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/estate_privileges/clergy_estate.txt:502>)。
- [dissolve_monasteries](ED_Vanilla_Wonder_Construction_Actions.md#dissolve_monasteries-3-16cc8a)：解散修会；change_building_level_in_location；[in_game/common/generic_actions/church_power.txt:3](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/generic_actions/church_power.txt:3>)。
- `support_the_krstjani_monasteries`：支持$bosnian_church_ADJ$修道院；门槛/关联引用；需看上下文；[in_game/common/generic_actions/church_power.txt:890](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/generic_actions/church_power.txt:890>)。
- `abbey_reform`：修会；门槛/关联引用；需看上下文；[in_game/common/government_reforms/theocracy.txt:35](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/government_reforms/theocracy.txt:35>)。
- [pa_construct_monastery](ED_Vanilla_Wonder_Construction_Actions.md#pa_construct_monastery-914-cf85e0)：要求新修道院；construct_building；[in_game/common/parliament_agendas/03_buildings.txt:914](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/parliament_agendas/03_buildings.txt:914>)。
- [fund_monastery_network](ED_Vanilla_Wonder_Construction_Actions.md#fund_monastery_network-834-9aef90)：资助修道院体系；construct_building；[in_game/common/parliament_issues/07_expansion_parliament_issues.txt:834](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/parliament_issues/07_expansion_parliament_issues.txt:834>)。
- `contemplatives_calling`：冥思者；门槛/关联引用；需看上下文；[in_game/common/religious_order_callings/00_monastic.txt:1](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/religious_order_callings/00_monastic.txt:1>)。
- `scholars_calling`：学者；门槛/关联引用；需看上下文；[in_game/common/religious_order_callings/00_monastic.txt:44](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/religious_order_callings/00_monastic.txt:44>)。
- `cultivators_calling`：耕作者；门槛/关联引用；需看上下文；[in_game/common/religious_order_callings/00_monastic.txt:106](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/religious_order_callings/00_monastic.txt:106>)。
- [reformation](ED_Vanilla_Wonder_Construction_Actions.md#reformation-1-e4f75f)：宗教改革；门槛/关联引用；需看上下文；[in_game/common/situations/reformation.txt:1](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/situations/reformation.txt:1>)。
- `flavor_bos.4`：斯特罗伊尼奇议会召开；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_BOS.txt:249](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_BOS.txt:249>)。
- [flavor_cas.21](ED_Vanilla_Wonder_Construction_Actions.md#flavor_cas-21-1244-9abc78)：夺得[GetCountry('POR').GetNameWithNoTooltip]王位；change_building_level_in_location；[in_game/events/DHE/flavor_CAS.txt:1244](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_CAS.txt:1244>)。
- [flavor_cas_rio_salado.6](ED_Vanilla_Wonder_Construction_Actions.md#flavor_cas_rio_salado-6-374-f2ed60)：[target_ruler.GetNameWithNoTooltip]的一次拜访；construct_building；[in_game/events/DHE/flavor_cas_rio_salado.txt:374](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_cas_rio_salado.txt:374>)。
- [flavor_cas_rio_salado.7](ED_Vanilla_Wonder_Construction_Actions.md#flavor_cas_rio_salado-7-450-f2ed60)：纪念胜利；construct_building；[in_game/events/DHE/flavor_cas_rio_salado.txt:450](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_cas_rio_salado.txt:450>)。
- [flavor_dan.3](ED_Vanilla_Wonder_Construction_Actions.md#flavor_dan-3-216-6355b4)：嘉勒修女会求助；construct_building；[in_game/events/DHE/flavor_dan.txt:216](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_dan.txt:216>)。
- [flavor_nov.35](ED_Vanilla_Wonder_Construction_Actions.md#flavor_nov-35-1965-51d2dc)：[target_location.GetNameWithNoTooltip]修道院的建立；change_building_level_in_location；[in_game/events/DHE/flavor_NOV.txt:1965](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_NOV.txt:1965>)。
- [flavor_por.23](ED_Vanilla_Wonder_Construction_Actions.md#flavor_por-23-1261-f14e68)：巴塔利亚修道院；construct_building；[in_game/events/DHE/flavor_por.txt:1261](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_por.txt:1261>)。
- `parliaments.32`：修道院市场；门槛/关联引用；需看上下文；[in_game/events/government/parliaments.txt:1934](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/government/parliaments.txt:1934>)。
- `parliaments.48`：上帝的田地与农民的犁；门槛/关联引用；需看上下文；[in_game/events/government/parliaments.txt:3132](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/government/parliaments.txt:3132>)。
- `buddhism_events.4`：怯战；门槛/关联引用；需看上下文；[in_game/events/religion/buddhism_events.txt:190](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/religion/buddhism_events.txt:190>)。
- `buddhism_events.9`：继承纠纷；门槛/关联引用；需看上下文；[in_game/events/religion/buddhism_events.txt:429](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/religion/buddhism_events.txt:429>)。
- `buddhism_events.12`：律师们意见不一；门槛/关联引用；需看上下文；[in_game/events/religion/buddhism_events.txt:650](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/religion/buddhism_events.txt:650>)。
- `buddhism_events.16`：[ROOT.GetCountry.GetNameWithNoTooltip]寺庙影响力减弱；门槛/关联引用；需看上下文；[in_game/events/religion/buddhism_events.txt:883](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/religion/buddhism_events.txt:883>)。
- `buddhism_events.17`：僧人破戒；门槛/关联引用；需看上下文；[in_game/events/religion/buddhism_events.txt:929](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/religion/buddhism_events.txt:929>)。
- `buddhism_events.18`：[ROOT.GetCountry.GetNameWithNoTooltip]的僧院；门槛/关联引用；需看上下文；[in_game/events/religion/buddhism_events.txt:1006](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/religion/buddhism_events.txt:1006>)。
- `buddhism_events.20`：农民的牺牲；门槛/关联引用；需看上下文；[in_game/events/religion/buddhism_events.txt:1124](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/religion/buddhism_events.txt:1124>)。
- `catholic_flavor.2`：一座繁荣的修道院；门槛/关联引用；需看上下文；[in_game/events/religion/catholic_flavor.txt:51](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/religion/catholic_flavor.txt:51>)。
- `catholic_flavor.3`：修道院陷入困境；门槛/关联引用；需看上下文；[in_game/events/religion/catholic_flavor.txt:105](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/religion/catholic_flavor.txt:105>)。
- `location_catholic_flavor_8_trigger`：location_catholic_flavor_8_trigger；门槛/关联引用；需看上下文；[in_game/events/religion/catholic_flavor.txt:367](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/religion/catholic_flavor.txt:367>)。
- `church_aspects.21`：[location_monastery.GetNameWithNoTooltip]受益于修道院；门槛/关联引用；需看上下文；[in_game/events/religion/church_aspects.txt:746](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/religion/church_aspects.txt:746>)。
- `church_aspects.22`：对地下天主教徒的担忧；门槛/关联引用；需看上下文；[in_game/events/religion/church_aspects.txt:801](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/religion/church_aspects.txt:801>)。
- [reformation.15](ED_Vanilla_Wonder_Construction_Actions.md#reformation-15-954-0585f6)：修道院加入了宗教改革；construct_building, destroy_building；[in_game/events/situations/reformation.txt:954](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/situations/reformation.txt:954>)。

1337 开局实例：`vadstena`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1206](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1206>)；`alvastra`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1207](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1207>)；`riseberga`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1208](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1208>)；`nidaros`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1209](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1209>)；`tonsberg`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1210](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1210>)；`kirkcudbright`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1456](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1456>)；`dunfermline`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1457](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1457>)；`roxburgh`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1458](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1458>)；`selkirk`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1459](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1459>)；`essen`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1460](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1460>)；`disentis`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1461](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1461>)；`cashel`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1552](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1552>)；`ardagh`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1553](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1553>)；`clogher`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1558](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1558>)；`armagh`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1559](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1559>)；`clifden`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1560](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1560>)；`monmouth`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1562](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1562>)；`cardigan`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1563](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1563>)；`flint`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1564](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1564>)；`swansea`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1565](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1565>)；`pembroke`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1566](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1566>)；`york`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1567](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1567>)；`wells`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1568](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1568>)；`bedale`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1569](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1569>)；`london`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1570](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1570>)；`skipton`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1571](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1571>)；`elgin`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1615](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1615>)；`st_andrews`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1616](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1616>)；`mull`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1617](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1617>)；`aguilar_de_campoo`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1892](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1892>)；`aranda_de_duero`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1893](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1893>)；`barcelona`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1894](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1894>)；`barcelos`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1895](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1895>)；`bilbao`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1896](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1896>)；`briviesca`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1897](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1897>)；`buitrago_de_lozoya`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1898](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1898>)；`burgos`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1899](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1899>)；`calatayud`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1900](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1900>)；`coimbra`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1901](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1901>)；`crato`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1902](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1902>)；`esgueira`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1903](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1903>)；`estella`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1904](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1904>)；`guimaraes`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1905](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1905>)；`huelva`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1906](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1906>)；`jaca`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1907](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1907>)；`alcobaca`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1908](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1908>)；`leon`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1909](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1909>)；`lerma`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1910](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1910>)；`lisbon`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1911](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1911>)；`najera`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1912](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1912>)；`medinaceli`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1913](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1913>)；`monforte_de_lemos`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1914](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1914>)；`monzon_campos`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1915](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1915>)；`navia_de_suarna`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1916](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1916>)；`ocana`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1917](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1917>)；`ribadavia`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1918](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1918>)；`sahagun`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1919](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1919>)；`salamanca`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1920](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1920>)；`potes`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1921](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1921>)；`salvatierra`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1922](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1922>)；`sanguesa`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1923](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1923>)；`montblanc`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1924](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1924>)；`tomar`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1925](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1925>)；`tudela`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1926](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1926>)；`ripoll`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1927](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1927>)；`villaviciosa`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1928](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1928>)；`viseu`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1929](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1929>)；`vitoria`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1930](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1930>)；`hasselt`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2168](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2168>)；`luxembourg`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2169](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2169>)；`borgloon`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2170](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2170>)；`stavelot`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2171](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2171>)；`weert`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2172](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2172>)；`nivelles`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2173](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2173>)；`meissen`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2191](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2191>)；`tirschenreuth`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2408](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2408>)；`prum`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2409](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2409>)；`hoxter`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2410](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2410>)；`zeven`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2411](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2411>)；`mouzon`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2413](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2413>)；`saint_claude`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2414](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2414>)；`ellwangen`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2415](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2415>)；`vu_ninh`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2505](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2505>)；`thai_binh`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2506](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2506>)；`thang_long`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2507](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2507>)；`simhapura`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2508](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2508>)；`kauthara`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2509](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2509>)；`panduranga`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2510](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2510>)。

### monument_bou_inania_madrasa — 伊纳尼耶回学院

原版定义：[in_game/common/building_types/unique_buildings.txt:5696](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:5696>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `build_time = religious_building_time`
- `location_potential = { this = location:fez }`
- `country_potential = { has_advance = mor_marinid_takeover }`
- `allow = { }`

未在本次行为定义中发现显式同名引用；仍可能由建筑自身条件、科技/改革解锁或引擎常规建设入口提供。

### monument_chellah — 切拉赫圣陵

原版定义：[in_game/common/building_types/unique_buildings.txt:5729](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:5729>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `build_time = cultural_building_time`
- `location_potential = { this = location:rabat }`
- `country_potential = { has_advance = mor_marinid_takeover }`
- `allow = { }`

未在本次行为定义中发现显式同名引用；仍可能由建筑自身条件、科技/改革解锁或引擎常规建设入口提供。

### monument_consulado_de_bilbao — 毕尔巴鄂仲裁庭

原版定义：[in_game/common/building_types/unique_buildings.txt:4394](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:4394>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `build_time = small_capital_build_time`
- `location_potential = { this = location:bilbao }`
- `country_potential = { has_dlc = "d009_across_the_pillars" has_or_had_tag = NAV current_age_or_later = { age = age_3_discovery } has_estate_privilege = estate_privilege:basque_universidad_mercaderes_bilbao }`
- `allow = { }`

未在本次行为定义中发现显式同名引用；仍可能由建筑自身条件、科技/改革解锁或引擎常规建设入口提供。

### monument_dar_al_makhzen — 行署之家

原版定义：[in_game/common/building_types/unique_buildings.txt:5764](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:5764>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `build_time = large_capital_build_time`
- `location_potential = { this = location:fez }`
- `country_potential = { always = no }`
- `allow = { always = no }`

未在本次行为定义中发现显式同名引用；仍可能由建筑自身条件、科技/改革解锁或引擎常规建设入口提供。

1337 开局实例：`fez`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3831](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3831>)。

### monument_great_mosque_algiers — 阿尔及尔大清真寺

原版定义：[in_game/common/building_types/unique_buildings.txt:5800](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:5800>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `build_time = religious_building_time`
- `location_potential = { this = location:algiers }`
- `country_potential = { always = no }`
- `allow = { always = no }`

未在本次行为定义中发现显式同名引用；仍可能由建筑自身条件、科技/改革解锁或引擎常规建设入口提供。

1337 开局实例：`algiers`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3836](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3836>)。

### monument_hassan_tower — 哈桑塔

原版定义：[in_game/common/building_types/unique_buildings.txt:5834](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:5834>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `build_time = cultural_building_time`
- `location_potential = { this = location:rabat }`
- `country_potential = { always = no }`
- `allow = { always = no }`

未在本次行为定义中发现显式同名引用；仍可能由建筑自身条件、科技/改革解锁或引擎常规建设入口提供。

1337 开局实例：`rabat`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3833](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3833>)。

### monument_kairouan_mosque — 凯鲁万大清真寺

原版定义：[in_game/common/building_types/unique_buildings.txt:5870](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:5870>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `build_time = religious_building_time`
- `location_potential = { this = location:kairouan }`
- `country_potential = { always = no }`
- `allow = { always = no }`

未在本次行为定义中发现显式同名引用；仍可能由建筑自身条件、科技/改革解锁或引擎常规建设入口提供。

1337 开局实例：`kairouan`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3837](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3837>)。

### monument_kasbah_udayas — 乌达雅老城堡

原版定义：[in_game/common/building_types/unique_buildings.txt:5906](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:5906>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `build_time = generic_town_build_time`
- `location_potential = { this = location:rabat }`
- `country_potential = { always = no }`
- `allow = { always = no }`

未在本次行为定义中发现显式同名引用；仍可能由建筑自身条件、科技/改革解锁或引擎常规建设入口提供。

1337 开局实例：`rabat`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3834](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3834>)。

### monument_ksar_ait_benhaddou — 阿伊特本哈杜城

原版定义：[in_game/common/building_types/unique_buildings.txt:5939](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:5939>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `build_time = generic_town_build_time`
- `location_potential = { this = location:ait_benhaddou }`
- `country_potential = { has_or_had_tag = MOR current_age_or_later = { age = age_5_absolutism } }`
- `allow = { }`

未在本次行为定义中发现显式同名引用；仍可能由建筑自身条件、科技/改革解锁或引擎常规建设入口提供。

### monument_llotja_de_mar_barcelona — 海事交易厅

原版定义：[in_game/common/building_types/unique_buildings.txt:4251](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:4251>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `build_time = small_capital_build_time`
- `location_potential = { this = location:barcelona }`
- `country_potential = { has_or_had_tag = CAT current_age_or_later = { age = age_2_renaissance } }`
- `allow = { }`

未在本次行为定义中发现显式同名引用；仍可能由建筑自身条件、科技/改革解锁或引擎常规建设入口提供。

### monument_mansourah_tlemcen — 曼苏拉清真寺

原版定义：[in_game/common/building_types/unique_buildings.txt:5973](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:5973>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `build_time = generic_town_build_time`
- `location_potential = { this = location:tlemcen }`
- `country_potential = { always = no }`
- `allow = { always = no }`

未在本次行为定义中发现显式同名引用；仍可能由建筑自身条件、科技/改革解锁或引擎常规建设入口提供。

1337 开局实例：`tlemcen`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3835](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3835>)。

### monument_palau_generalitat — 加泰罗尼亚政府宫

原版定义：[in_game/common/building_types/unique_buildings.txt:4208](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:4208>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `build_time = government_build_time`
- `location_potential = { this = location:barcelona }`
- `country_potential = { has_advance = cat_generalitat }`
- `allow = { }`

未在本次行为定义中发现显式同名引用；仍可能由建筑自身条件、科技/改革解锁或引擎常规建设入口提供。

### monument_qarawiyyin — 卡拉维因大学

原版定义：[in_game/common/building_types/unique_buildings.txt:6007](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:6007>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `build_time = religious_building_time`
- `location_potential = { this = location:fez }`
- `country_potential = { always = no }`
- `allow = { always = no }`

未在本次行为定义中发现显式同名引用；仍可能由建筑自身条件、科技/改革解锁或引擎常规建设入口提供。

1337 开局实例：`fez`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3832](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3832>)。

### monument_sa_llotja_de_palma — 帕尔马交易厅

原版定义：[in_game/common/building_types/unique_buildings.txt:4299](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:4299>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `build_time = small_capital_build_time`
- `location_potential = { this = location:palma }`
- `country_potential = { has_or_had_tag = MLL current_age_or_later = { age = age_3_discovery } }`
- `allow = { }`

未在本次行为定义中发现显式同名引用；仍可能由建筑自身条件、科技/改革解锁或引擎常规建设入口提供。

### monument_torre_de_hercules — 埃库莱斯灯塔

原版定义：[in_game/common/building_types/unique_buildings.txt:4347](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:4347>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `build_time = government_build_time`
- `location_potential = { this = location:coruna }`
- `country_potential = { always = no }`
- `allow = { always = no }`

未在本次行为定义中发现显式同名引用；仍可能由建筑自身条件、科技/改革解锁或引擎常规建设入口提供。

1337 开局实例：`coruna`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1807](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1807>)。

### moscow_artillery_yard — 莫斯科火炮厂

原版定义：[in_game/common/building_types/unique_buildings.txt:3385](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:3385>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `build_time = big_soldier_building`
- `country_potential = { custom_tooltip = { text = moscow_artillery_yard_why OR = { tag = MOS tag = RUS } has_variable = moscow_artillery_yard } }`
- `location_potential = { this = location:moscow }`
- `allow = { always = no }`

行为或条件引用：

- [mos_moscow_artillery_yard_decision](ED_Vanilla_Wonder_Construction_Actions.md#mos_moscow_artillery_yard_decision-1033-f996cd)：莫斯科炮场；construct_building；[in_game/common/decisions/flavor_decisions_rus.txt:1033](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/decisions/flavor_decisions_rus.txt:1033>)。
- `flavor_rus.43`：[grigory_orlov.GetNameWithNoTooltip]；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_RUS.txt:3258](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_RUS.txt:3258>)。

### moscow_orphanage — 莫斯科孤儿院

原版定义：[in_game/common/building_types/unique_buildings.txt:3985](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:3985>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `country_potential = { custom_tooltip = { text = moscow_orphanage_why OR = { tag = MOS tag = RUS } has_variable = moscow_orphanage } }`
- `allow = { always = no }`
- `build_time = cultural_building_time`
- `location_potential = { this = location:moscow }`

行为或条件引用：

- [mos_moscow_orphanage_decision](ED_Vanilla_Wonder_Construction_Actions.md#mos_moscow_orphanage_decision-2210-f996cd)：善意的孤儿院；construct_building；[in_game/common/decisions/flavor_decisions_rus.txt:2210](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/decisions/flavor_decisions_rus.txt:2210>)。
- [flavor_rus.56](ED_Vanilla_Wonder_Construction_Actions.md#flavor_rus-56-4553-201f60)：看得起的表演；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_RUS.txt:4553](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_RUS.txt:4553>)。

### munich_residenz_baroque_expansion — $munich$王宫‑巴洛克式宫殿

原版定义：[in_game/common/building_types/event_only_buildings.txt:3571](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/event_only_buildings.txt:3571>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `build_time = large_capital_build_time`
- `country_potential = { custom_tooltip = { text = munich_residenz_baroque_expansion_potential OR = { has_or_had_tag = BAV has_or_had_tag = LBV has_or_had_tag = UBV } } }`
- `allow = { always = no }`
- `location_potential = { this = location:munich has_building = building_type:munich_residenz_renaissance_expansion }`

行为或条件引用：

- [flavor_bav.1402](ED_Vanilla_Wonder_Construction_Actions.md#flavor_bav-1402-2427-75be1b)：[target_location.GetNameWithNoTooltip]王宫的巴洛克式扩建；construct_building；[in_game/events/DHE/flavor_bav.txt:2427](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_bav.txt:2427>)。

### munich_residenz_founding — $munich$王宫‑中世纪城堡

原版定义：[in_game/common/building_types/event_only_buildings.txt:3460](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/event_only_buildings.txt:3460>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `build_time = large_capital_build_time`
- `country_potential = { custom_tooltip = { text = munich_residenz_founding_potential OR = { has_or_had_tag = BAV has_or_had_tag = LBV has_or_had_tag = UBV } } }`
- `allow = { always = no }`
- `location_potential = { this = location:munich }`

行为或条件引用：

- [flavor_bav.1400](ED_Vanilla_Wonder_Construction_Actions.md#flavor_bav-1400-2324-75be1b)：[target_location.GetNameWithNoTooltip]王宫的奠基；construct_building；[in_game/events/DHE/flavor_bav.txt:2324](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_bav.txt:2324>)。
- [flavor_bav.1401](ED_Vanilla_Wonder_Construction_Actions.md#flavor_bav-1401-2374-75be1b)：[target_location.GetNameWithNoTooltip]王宫的[ShowInstitutionNameWithNoTooltip('renaissance')]式扩建；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_bav.txt:2374](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_bav.txt:2374>)。

### munich_residenz_renaissance_expansion — $munich$王宫‑$renaissance$老王宫

原版定义：[in_game/common/building_types/event_only_buildings.txt:3517](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/event_only_buildings.txt:3517>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `build_time = large_capital_build_time`
- `country_potential = { custom_tooltip = { text = munich_residenz_renaissance_expansion_potential OR = { has_or_had_tag = BAV has_or_had_tag = LBV has_or_had_tag = UBV } } }`
- `allow = { always = no }`
- `location_potential = { this = location:munich has_building = building_type:munich_residenz_founding }`

行为或条件引用：

- [flavor_bav.1401](ED_Vanilla_Wonder_Construction_Actions.md#flavor_bav-1401-2374-75be1b)：[target_location.GetNameWithNoTooltip]王宫的[ShowInstitutionNameWithNoTooltip('renaissance')]式扩建；construct_building；[in_game/events/DHE/flavor_bav.txt:2374](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_bav.txt:2374>)。
- [flavor_bav.1402](ED_Vanilla_Wonder_Construction_Actions.md#flavor_bav-1402-2427-75be1b)：[target_location.GetNameWithNoTooltip]王宫的巴洛克式扩建；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_bav.txt:2427](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_bav.txt:2427>)。

### nobled_sponsored_temple — 贵族赞助的神殿

原版定义：[in_game/common/building_types/estate_buildings.txt:355](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/estate_buildings.txt:355>)。

- `is_foreign = no`
- `max_levels = estate_building_single_level`
- `build_time = estate_build_time`

未在本次行为定义中发现显式同名引用；仍可能由建筑自身条件、科技/改革解锁或引擎常规建设入口提供。

### north_sea_shipyards — 北海造船厂

原版定义：[in_game/common/building_types/unique_buildings.txt:1069](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:1069>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `build_time = large_port_building_time`
- `location_potential = { is_port = yes region = region:north_german_region }`
- `country_potential = { has_advance = netherlandish_ship_building }`

行为或条件引用：

- [netherlandish_ship_building](ED_Vanilla_Wonder_Construction_Actions.md#netherlandish_ship_building-25-9637be)：尼德兰造船业；unlock_building；[in_game/common/advances/culture_netherlands.txt:25](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/advances/culture_netherlands.txt:25>)。

### novodevichy_convent — 新圣女修道院

原版定义：[in_game/common/building_types/unique_buildings.txt:3331](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:3331>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `build_time = small_fort_building`
- `country_potential = { custom_tooltip = { text = novodevichy_convent_why OR = { tag = MOS tag = RUS } has_variable = novodevichy_convent } religion ?= religion:orthodox }`
- `location_potential = { this = location:moscow }`
- `allow = { always = no }`

行为或条件引用：

- [mos_novodevichy_convent_decision](ED_Vanilla_Wonder_Construction_Actions.md#mos_novodevichy_convent_decision-761-f996cd)：新圣女修道院；construct_building；[in_game/common/decisions/flavor_decisions_rus.txt:761](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/decisions/flavor_decisions_rus.txt:761>)。
- [rus_institute_of_noble_maidens_decision](ED_Vanilla_Wonder_Construction_Actions.md#rus_institute_of_noble_maidens_decision-2345-f996cd)：贵族女子学院；门槛/关联引用；需看上下文；[in_game/common/decisions/flavor_decisions_rus.txt:2345](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/decisions/flavor_decisions_rus.txt:2345>)。

### oma_falaj — 法拉吉

原版定义：[in_game/common/building_types/event_only_buildings.txt:1763](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/event_only_buildings.txt:1763>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 2`
- `build_time = small_fort_building`
- `country_potential = { has_unlocked_building_trigger = { type = oma_falaj } }`
- `allow = { is_coastal = no vegetation = desert climate = arid }`

行为或条件引用：

- [flavor_oma.9](ED_Vanilla_Wonder_Construction_Actions.md#flavor_oma-9-560-85fa5f)：确保[target_location.GetNameWithNoTooltip]供水；construct_building；[in_game/events/DHE/flavor_OMA.txt:560](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_OMA.txt:560>)。
- [flavor_oma.16](ED_Vanilla_Wonder_Construction_Actions.md#flavor_oma-16-1120-85fa5f)：沿海移民计划；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_OMA.txt:1120](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_OMA.txt:1120>)。
- [flavor_oma.17](ED_Vanilla_Wonder_Construction_Actions.md#flavor_oma-17-1233-85fa5f)：扩建坎儿井系统；unlock_building_effect；[in_game/events/DHE/flavor_OMA.txt:1233](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_OMA.txt:1233>)。

### oma_nizwa_fort — 奈兹瓦要塞

原版定义：[in_game/common/building_types/event_only_buildings.txt:1794](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/event_only_buildings.txt:1794>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `build_time = small_fort_building`
- `country_potential = { always = no }`
- `allow = { always = no }`

行为或条件引用：

- [flavor_oma.10](ED_Vanilla_Wonder_Construction_Actions.md#flavor_oma-10-620-85fa5f)：[target_location.GetNameWithNoTooltip]的兴盛；construct_building；[in_game/events/DHE/flavor_OMA.txt:620](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_OMA.txt:620>)。

### order_commandery — 骑士团辖地

原版定义：[in_game/common/building_types/unique_buildings.txt:483](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:483>)。

- `is_special = yes`
- `is_foreign = yes`
- `max_levels = 1`
- `location_potential = { custom_tooltip = { text = order_commandery_tt owner = { giving_scripted_relation = { type = relation_type:military_sponsorship target = scope:actor } } } }`
- `country_potential = { modifier:target_of_military_sponsorships = yes religion ?= religion:catholic }`
- `build_time = soldier_building`
- `allow = { owner = { within_diplomatic_range = scope:actor } dominant_religion ?= religion:catholic }`
- `remove_if = { OR = { location = { dominant_religion != religion:catholic } owner = { OR = { modifier:target_of_military_sponsorships = no religion != religion:catholic } } } }`
- `on_built = { if = { limit = { location.owner != root.owner } location.owner = { add_opinion = { target = root.owner modifier = opinion_reformation_diplomacy } } } }`

行为或条件引用：

- `flavor_teu.8`：经济下行；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_teu.txt:526](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_teu.txt:526>)。

1337 开局实例：`tortosa`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1686](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1686>)；`pamplona`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1688](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1688>)；`vodable`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1691](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1691>)；`consuegra`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1694](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1694>)；`alcazar_de_san_juan`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1695](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1695>)；`crato`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1697](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1697>)；`proenca_nova`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1698](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1698>)；`serpa`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1699](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1699>)；`moura`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1700](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1700>)；`london`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1703](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1703>)；`dublin`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1705](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1705>)；`edinburgh`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1707](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1707>)；`poitiers`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1710](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1710>)；`chatillon_sur_seine`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1712](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1712>)；`paris`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1714](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1714>)；`harderwijk`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1717](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1717>)；`szadzko`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1720](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1720>)；`opava`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1722](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1722>)；`poznan`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1724](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1724>)；`odense`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1726](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1726>)；`strangnas`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1727](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1727>)；`buda`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1729](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1729>)；`andria`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1732](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1732>)；`caserta`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1734](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1734>)；`messina`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1736](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1736>)；`rome`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1738](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1738>)；`pisa`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1740](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1740>)；`asti`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1742](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1742>)；`venice`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1744](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1744>)；`nimes`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1747](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1747>)；`toulouse`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1749](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1749>)；`vienna`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1753](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1753>)；`borgloon`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1755](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1755>)；`usti_nad_labem`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1757](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1757>)；`epinal`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1759](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1759>)；`weissenburg`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1761](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1761>)；`modon`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1763](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1763>)；`marburg`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1765](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1765>)；`coblenz`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1767](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1767>)；`treviso`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1769](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1769>)；`trier`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1771](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1771>)；`viterbo`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1773](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1773>)；`manfredonia`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1775](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1775>)；`brunswick`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1777](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1777>)；`bremen`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1778](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1778>)；`lubeck`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1779](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1779>)；`girgenti`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1781](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1781>)；`toro`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1783](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1783>)；`ravensburg`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1785](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1785>)；`apolda`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1787](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1787>)；`bolzano`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1789](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1789>)；`utrecht`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1791](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1791>)；`munster`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1793](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1793>)。

### order_stronghold — 骑士团要塞

原版定义：[in_game/common/building_types/unique_buildings.txt:439](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:439>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `country_potential = { has_reform = government_reform:military_order_reform }`
- `build_time = soldier_building`

行为或条件引用：

- `teu_event_6_trigger`：teu_event_6_trigger；门槛/关联引用；需看上下文；[in_game/common/scripted_triggers/location_triggers.txt:167](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/scripted_triggers/location_triggers.txt:167>)。
- [flavor_por.25](ED_Vanilla_Wonder_Construction_Actions.md#flavor_por-25-1373-f14e68)：基督骑士团的新驻地；change_building_level_in_location, destroy_building；[in_game/events/DHE/flavor_por.txt:1373](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_por.txt:1373>)。

1337 开局实例：`cesis`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1655](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1655>)；`viljandi`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1656](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1656>)；`rodos`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1657](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1657>)；`malbork`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1659](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1659>)；`elk`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1660](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1660>)；`konigsberg`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1661](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1661>)；`tuchola`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1662](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1662>)；`calatrava`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1665](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1665>)；`huete`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1668](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1668>)；`alcacer_do_sal`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1673](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1673>)；`tavira`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1674](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1674>)；`alcazar_de_san_juan`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1675](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1675>)；`crato`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1676](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1676>)；`alcantara`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1677](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1677>)；`avis`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1679](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1679>)；`ayora`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1681](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1681>)。

### ori_portuguese_quarters — 葡萄牙区

原版定义：[in_game/common/building_types/event_only_buildings.txt:3076](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/event_only_buildings.txt:3076>)。

- `is_special = yes`
- `is_foreign = yes`
- `max_levels = 1`
- `country_potential = { always = no }`
- `allow = { always = no }`
- `build_time = trade_post_build_time`

行为或条件引用：

- [flavor_ori.1001](ED_Vanilla_Wonder_Construction_Actions.md#flavor_ori-1001-1168-91f915)：邀请[GetCountry('POR').GetAdjectiveWithNoTooltip]商人；construct_building；[in_game/events/DHE/flavor_ori.txt:1168](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_ori.txt:1168>)。
- [flavor_ori.1002](ED_Vanilla_Wonder_Construction_Actions.md#flavor_ori-1002-1227-91f915)：邀请[GetCountry('POR').GetAdjectiveWithNoTooltip]商人；construct_building；[in_game/events/DHE/flavor_ori.txt:1227](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_ori.txt:1227>)。

### orthodox_monastery — 东正教修道院

原版定义：[in_game/common/building_types/religion_buildings.txt:236](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/religion_buildings.txt:236>)。

- `is_foreign = no`
- `max_levels = 1`
- `build_time = religious_building_time`
- `country_potential = { religion ?= religion:orthodox }`

行为或条件引用：

- `office_of_new_converts`：监督新皈依者办公室；门槛/关联引用；需看上下文；[in_game/common/cabinet_actions/office_of_new_converts.txt:1](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/cabinet_actions/office_of_new_converts.txt:1>)。
- `mos_monastic_reformation_decision`：将索拉的尼尔的教诲制度化；门槛/关联引用；需看上下文；[in_game/common/decisions/flavor_decisions_rus.txt:496](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/decisions/flavor_decisions_rus.txt:496>)。
- [patronize_orthodox_monastery](ED_Vanilla_Wonder_Construction_Actions.md#patronize_orthodox_monastery-734-ed91e7)：赞助$orthodox_monastery$；门槛/关联引用；需看上下文；[in_game/common/generic_actions/D008_fate_of_the_phoenix_actions.txt:734](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/generic_actions/D008_fate_of_the_phoenix_actions.txt:734>)。
- [pa_construct_monastery](ED_Vanilla_Wonder_Construction_Actions.md#pa_construct_monastery-914-cf85e0)：要求新修道院；construct_building；[in_game/common/parliament_agendas/03_buildings.txt:914](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/parliament_agendas/03_buildings.txt:914>)。
- [fund_monastery_network](ED_Vanilla_Wonder_Construction_Actions.md#fund_monastery_network-834-9aef90)：资助修道院体系；construct_building；[in_game/common/parliament_issues/07_expansion_parliament_issues.txt:834](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/parliament_issues/07_expansion_parliament_issues.txt:834>)。
- `culture_greek.22`：[target_location.GetNameWithNoTooltip]的诞神女节庆；门槛/关联引用；需看上下文；[in_game/events/culture/culture_greek.txt:2263](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/culture/culture_greek.txt:2263>)。
- `culture_greek.29`：东正教修道院寻求帮助；门槛/关联引用；需看上下文；[in_game/events/culture/culture_greek.txt:3008](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/culture/culture_greek.txt:3008>)。
- [flavor_mos.5](ED_Vanilla_Wonder_Construction_Actions.md#flavor_mos-5-286-c719bc)：拉多奈哲的塞尔吉；construct_building；[in_game/events/DHE/flavor_MOS.txt:286](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_MOS.txt:286>)。
- [flavor_mos.6](ED_Vanilla_Wonder_Construction_Actions.md#flavor_mos-6-392-c719bc)：塞尔吉圣三一修道院；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_MOS.txt:392](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_MOS.txt:392>)。
- [flavor_mos.27](ED_Vanilla_Wonder_Construction_Actions.md#flavor_mos-27-2151-c719bc)：[maria_borovsk.GetNameWithNoTooltip]；construct_building；[in_game/events/DHE/flavor_MOS.txt:2151](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_MOS.txt:2151>)。
- [flavor_nov.35](ED_Vanilla_Wonder_Construction_Actions.md#flavor_nov-35-1965-51d2dc)：[target_location.GetNameWithNoTooltip]修道院的建立；change_building_level_in_location；[in_game/events/DHE/flavor_NOV.txt:1965](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_NOV.txt:1965>)。
- [flavor_rus.67](ED_Vanilla_Wonder_Construction_Actions.md#flavor_rus-67-5647-201f60)：皮鞭下的受洗；construct_building；[in_game/events/DHE/flavor_RUS.txt:5647](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_RUS.txt:5647>)。
- [flavor_ser.90](ED_Vanilla_Wonder_Construction_Actions.md#flavor_ser-90-1522-15d4f1)：马纳西亚修道院；construct_building；[in_game/events/DHE/flavor_ser.txt:1522](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_ser.txt:1522>)。
- `flavor_ser.91`：雷萨瓦学院；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_ser.txt:1591](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_ser.txt:1591>)。
- `flavor_ser.190`：希兰达尔修道院；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_ser.txt:2179](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_ser.txt:2179>)。
- `patriarch_events.5`：修道院在[monastic_province.GetNameWithNoTooltip]蓬勃发展；门槛/关联引用；需看上下文；[in_game/events/religion/patriarch_events.txt:201](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/religion/patriarch_events.txt:201>)。

1337 开局实例：`novgorod`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2258](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2258>)；`novgorod`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2259](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2259>)；`pskov`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2260](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2260>)；`moscow`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2261](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2261>)；`bryansk`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2262](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2262>)；`kostroma`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2263](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2263>)；`nizhny_novgorod`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2264](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2264>)；`kyiv`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2300](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2300>)；`volodymyr`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2301](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2301>)；`lutsk`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2302](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2302>)；`lviv`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2303](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2303>)；`sambir`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2304](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2304>)；`novhorod_siverskyi`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2305](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2305>)；`chernihiv`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2306](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2306>)；`polotsk`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2307](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2307>)；`turov`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2308](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2308>)；`novogrudok`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2309](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2309>)；`belgrad`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2381](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2381>)；`gjakova`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2382](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2382>)；`debrc`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2383](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2383>)；`gradac`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2384](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2384>)；`kucevo`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2385](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2385>)；`peja`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2386](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2386>)；`prijepolje`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2387](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2387>)；`pristina`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2388](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2388>)；`prokuplje`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2389](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2389>)；`visesav`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2390](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2390>)；`vranje`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2391](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2391>)；`zica`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2392](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2392>)；`livadeia`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2393](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2393>)；`mount_athos`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2394](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2394>)。

### ostrog — 木板营寨

原版定义：[in_game/common/building_types/unique_buildings.txt:1593](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:1593>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `build_time = government_build_time`
- `country_potential = { culture = { has_culture_group = culture_group:russian_group } }`
- `location_potential = { is_capital = no is_historical_capital = no has_proximity_source_building = no has_river = yes OR = { region = region:ural_region region = region:west_siberia_region region = region:east_siberia_region } }`
- `allow = { proximity < 25 scope:actor = { total_building_levels_including_construction:ostrog < modifier:num_ostrogs } }`

行为或条件引用：

- [ostrog_advance](ED_Vanilla_Wonder_Construction_Actions.md#ostrog_advance-74-c5744b)：木板营寨；unlock_building；[in_game/common/advances/culture_russian.txt:74](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/advances/culture_russian.txt:74>)。

### panaqa_building — 帕纳卡领地

原版定义：[in_game/common/building_types/unique_buildings.txt:2046](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:2046>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `build_time = instant_build_time`
- `country_potential = { modifier:has_panaqas = yes }`
- `location_potential = { has_building = building_type:panaqa_building }`
- `remove_if = { owner = { modifier:has_panaqas = no } }`

行为或条件引用：

- [on_location_changed_owner](ED_Vanilla_Wonder_Construction_Actions.md#on_location_changed_owner-4851-fff745)：on_location_changed_owner；destroy_building；[in_game/common/on_action/_hardcoded.txt:4851](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/on_action/_hardcoded.txt:4851>)。
- [flavor_csu.100](ED_Vanilla_Wonder_Construction_Actions.md#flavor_csu-100-4-60023b)：[ROOT.GetCountry.GetNameWithNoTooltip]的帕纳卡领地；change_building_level_in_location；[in_game/events/DHE/flavor_CSU.txt:4](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_CSU.txt:4>)。

### papal_archives — 教廷档案馆

原版定义：[in_game/common/building_types/event_only_buildings.txt:1054](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/event_only_buildings.txt:1054>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `country_potential = { always = no }`
- `allow = { owner_owns_no_copies_of_building = { type = papal_archives } }`
- `build_time = cultural_building_time`

行为或条件引用：

- [flavor_pap.101](ED_Vanilla_Wonder_Construction_Actions.md#flavor_pap-101-2632-09eb6b)：[from_location.GetNameWithNoTooltip]的[ROOT.GetCountry.GetAdjectiveWithNoTooltip]档案馆；change_building_level_in_location, construct_building, destroy_building；[in_game/events/DHE/flavor_pap.txt:2632](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_pap.txt:2632>)。

1337 开局实例：`assisi`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2069](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2069>)。

### peel_towers — 边境哨塔

原版定义：[in_game/common/building_types/unique_buildings.txt:2375](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:2375>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `build_time = small_fort_building`
- `country_potential = { has_advance = peel_towers_advance }`
- `location_potential = { region = region:great_britain_region is_border = yes }`

行为或条件引用：

- [peel_towers_advance](ED_Vanilla_Wonder_Construction_Actions.md#peel_towers_advance-82-6869eb)：边境哨塔；unlock_building；[in_game/common/advances/country_sco.txt:82](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/advances/country_sco.txt:82>)。

1337 开局实例：`dunbar`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3611](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3611>)；`dumfries`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3612](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3612>)。

### phanariot_district — 法那尔人社区

原版定义：[in_game/common/building_types/event_only_buildings.txt:4011](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/event_only_buildings.txt:4011>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `build_time = large_cultural_building_time`
- `country_potential = { always = no }`
- `allow = { always = no }`

行为或条件引用：

- [flavor_tur.189](ED_Vanilla_Wonder_Construction_Actions.md#flavor_tur-189-15106-bf9554)：法那尔人；construct_building；[in_game/events/DHE/flavor_TUR.txt:15106](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_TUR.txt:15106>)。

### piazza_san_marco — 圣马尔谷广场

原版定义：[in_game/common/building_types/event_only_buildings.txt:2343](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/event_only_buildings.txt:2343>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `country_potential = { custom_tooltip = { text = unlocked_piazza_san_marco_tt has_variable = unlocked_piazza_san_marco } }`
- `allow = { always = no }`
- `build_time = large_cultural_building_time`

行为或条件引用：

- [ven_piazza_san_marco_decision](ED_Vanilla_Wonder_Construction_Actions.md#ven_piazza_san_marco_decision-1247-a14531)：圣马尔谷广场；construct_building；[in_game/common/decisions/flavor_decisions_various.txt:1247](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/decisions/flavor_decisions_various.txt:1247>)。
- `flavor_ven.52`：圣马尔谷钟楼；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_VEN.txt:2451](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_VEN.txt:2451>)。

### polders — 圩田

原版定义：[in_game/common/building_types/unique_buildings.txt:1908](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:1908>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = polders_max_level`
- `build_time = infrastructure_build_time`
- `location_potential = { OR = { is_coastal = yes is_adjacent_to_lake = yes } topography = wetlands }`

行为或条件引用：

- [polders_advance](ED_Vanilla_Wonder_Construction_Actions.md#polders_advance-15-9637be)：圩田；unlock_building；[in_game/common/advances/culture_netherlands.txt:15](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/advances/culture_netherlands.txt:15>)。
- [flavor_ned.12](ED_Vanilla_Wonder_Construction_Actions.md#flavor_ned-12-810-711d97)：[target_artist.GetNameWithNoTooltip]；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_ned.txt:810](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_ned.txt:810>)。

### pomor_outpost — 波莫尔哨站

原版定义：[in_game/common/building_types/unique_buildings.txt:1658](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:1658>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = rural_building_cap`
- `build_time = rural_build_time`
- `country_potential = { culture = { has_culture_group = culture_group:russian_group } }`
- `location_potential = { OR = { raw_material = goods:fur raw_material = goods:fish } }`
- `remove_if = { location = { NOR = { raw_material = goods:fur raw_material = goods:fish } } }`

行为或条件引用：

- [siberian_frontier](ED_Vanilla_Wonder_Construction_Actions.md#siberian_frontier-61-c5744b)：西伯利亚拓荒区；unlock_building；[in_game/common/advances/culture_russian.txt:61](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/advances/culture_russian.txt:61>)。

### por_feitoria — 葡萄牙官厂

原版定义：[in_game/common/building_types/unique_buildings.txt:5236](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:5236>)。

- `is_special = yes`
- `is_foreign = yes`
- `max_levels = 1`
- `location_potential = { is_port = yes custom_tooltip = { text = not_on_same_continent_as_capital continent != scope:actor.capital.continent } }`
- `allow = { OR = { is_coastal_within_range = yes is_adjacent_to_owned_or_subject_owns = yes } }`
- `build_time = trade_post_build_time`

行为或条件引用：

- [por_feitorias](ED_Vanilla_Wonder_Construction_Actions.md#por_feitorias-179-9268f8)：葡萄牙官厂；unlock_building；[in_game/common/advances/country_por.txt:179](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/advances/country_por.txt:179>)。
- [establish_cape_route_post](ED_Vanilla_Wonder_Construction_Actions.md#establish_cape_route_post-25-38f140)：establish_cape_route_post；construct_building；[in_game/common/scripted_effects/expedition_effects.txt:25](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/scripted_effects/expedition_effects.txt:25>)。
- [establish_feitoria_effect](ED_Vanilla_Wonder_Construction_Actions.md#establish_feitoria_effect-4179-f14e68)：establish_feitoria_effect；construct_building；[in_game/events/DHE/flavor_por.txt:4179](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_por.txt:4179>)。
- [flavor_por.55](ED_Vanilla_Wonder_Construction_Actions.md#flavor_por-55-4198-f14e68)：[target_location.GetNameWithNoTooltip]的葡萄牙官厂；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_por.txt:4198](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_por.txt:4198>)。
- [flavor_por.56](ED_Vanilla_Wonder_Construction_Actions.md#flavor_por-56-4259-f14e68)：[target_location.GetNameWithNoTooltip]的葡萄牙官厂；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_por.txt:4259](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_por.txt:4259>)。
- [flavor_por.57](ED_Vanilla_Wonder_Construction_Actions.md#flavor_por-57-4328-f14e68)：保护在[target_location.GetNameWithNoTooltip]的贸易；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_por.txt:4328](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_por.txt:4328>)。
- [flavor_por.58](ED_Vanilla_Wonder_Construction_Actions.md#flavor_por-58-4410-f14e68)：[target_location.GetNameWithNoTooltip]的防御工事；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_por.txt:4410](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_por.txt:4410>)。
- [flavor_por.59](ED_Vanilla_Wonder_Construction_Actions.md#flavor_por-59-4490-f14e68)：控制[target_location.GetNameWithNoTooltip]海峡；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_por.txt:4490](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_por.txt:4490>)。
- [flavor_por.64](ED_Vanilla_Wonder_Construction_Actions.md#flavor_por-64-4825-f14e68)：保卫[target_location.GetNameWithNoTooltip]；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_por.txt:4825](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_por.txt:4825>)。

### por_trading_post — 葡萄牙贸易站

原版定义：[in_game/common/building_types/unique_buildings.txt:5292](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:5292>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `country_potential = { always = no }`
- `allow = { always = no }`
- `build_time = trade_post_build_time`

行为或条件引用：

- [establish_cape_route_post](ED_Vanilla_Wonder_Construction_Actions.md#establish_cape_route_post-25-38f140)：establish_cape_route_post；construct_building；[in_game/common/scripted_effects/expedition_effects.txt:25](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/scripted_effects/expedition_effects.txt:25>)。

### porto_pisano — 比萨港

原版定义：[in_game/common/building_types/unique_buildings.txt:6170](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:6170>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = porto_pisano_max_level`
- `location_potential = { this = location:pisa }`
- `country_potential = { has_or_had_tag = PIS }`
- `build_time = huge_port_building_time`

行为或条件引用：

- `flavor_pis.5`：重心转移；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_PIS.txt:269](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_PIS.txt:269>)。

1337 开局实例：`pisa`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:4518](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:4518>)。

### pounamou_carver — 绿玉雕刻坊

原版定义：[in_game/common/building_types/unique_buildings.txt:1](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:1>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = guild_max_level`
- `build_time = rural_build_time`
- `location_potential = { dominant_culture ?= culture:maori_culture }`
- `country_potential = { culture ?= culture:maori_culture }`
- `allow = { market = { is_produced_in_market = goods:gems } }`

未在本次行为定义中发现显式同名引用；仍可能由建筑自身条件、科技/改革解锁或引擎常规建设入口提供。

### pound_lock_canal_infrastructure — 船闸运河

原版定义：[in_game/common/building_types/common_buildings.txt:85](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/common_buildings.txt:85>)。

- `is_foreign = no`
- `max_levels = 1`
- `build_time = infrastructure_build_time`
- `location_potential = { OR = { is_coastal = yes has_river = yes is_adjacent_to_lake = yes } development >= 20 }`
- `allow = { }`

行为或条件引用：

- [pound_lock_canals_advance](ED_Vanilla_Wonder_Construction_Actions.md#pound_lock_canals_advance-505-0fbdd0)：船闸运河；unlock_building；[in_game/common/advances/0_age_of_renaissance.txt:505](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/advances/0_age_of_renaissance.txt:505>)。
- [estate_cooperation](ED_Vanilla_Wonder_Construction_Actions.md#estate_cooperation-1-821312)：阶层合作；门槛/关联引用；需看上下文；[in_game/common/missions/generic_estate_cooperation_mission_pack.txt:1](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/missions/generic_estate_cooperation_mission_pack.txt:1>)。

### protected_harbor — 泊地

原版定义：[in_game/common/building_types/port_buildings.txt:263](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/port_buildings.txt:263>)。

- `is_foreign = no`
- `max_levels = 1`
- `location_potential = { is_port = yes }`
- `build_time = medium_port_building_time`

行为或条件引用：

- [protected_harbor_advance](ED_Vanilla_Wonder_Construction_Actions.md#protected_harbor_advance-802-3be8a5)：泊地；unlock_building；[in_game/common/advances/1_building_unlocks.txt:802](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/advances/1_building_unlocks.txt:802>)。

### provincial_garrison — 戍营

原版定义：[in_game/common/building_types/00_unique_buildings_to_make_obsolete.txt:70](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/00_unique_buildings_to_make_obsolete.txt:70>)。

- `is_foreign = no`
- `max_levels = 1`
- `build_time = soldier_building`
- `country_potential = { OR = { AND = { exists = international_organization:middle_kingdom is_leader_of_international_organization = international_organization:middle_kingdom } culture ?= { has_culture_group = culture_group:chinese_group } } }`
- `location_potential = { }`

未在本次行为定义中发现显式同名引用；仍可能由建筑自身条件、科技/改革解锁或引擎常规建设入口提供。

### pukara_building — 普卡拉山堡

原版定义：[in_game/common/building_types/unique_buildings.txt:2088](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:2088>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `build_time = small_fort_building`
- `country_potential = { culture = { has_culture_group = culture_group:andean_group } }`
- `location_potential = { OR = { topography = mountains topography = plateau topography = hills } }`

行为或条件引用：

- [pukara_advance](ED_Vanilla_Wonder_Construction_Actions.md#pukara_advance-1-8aa708)：普卡拉山堡；unlock_building；[in_game/common/advances/culture_andean.txt:1](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/advances/culture_andean.txt:1>)。

### qalat_al_mashwar — 梅舒阿尔城堡

原版定义：[in_game/common/building_types/unique_buildings.txt:5660](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:5660>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 2`
- `location_potential = { this = location:tlemcen counts_as_capital = yes }`
- `allow = { is_capital = yes }`
- `build_time = cultural_building_time`

行为或条件引用：

- [qalat_al_mashwar_advance](ED_Vanilla_Wonder_Construction_Actions.md#qalat_al_mashwar_advance-248-892e32)：梅舒阿尔城堡；unlock_building；[in_game/common/advances/country_tle.txt:248](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/advances/country_tle.txt:248>)。

1337 开局实例：`tlemcen`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3827](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3827>)。

### quirinal_palace — 奎里纳尔宫

原版定义：[in_game/common/building_types/event_only_buildings.txt:2805](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/event_only_buildings.txt:2805>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `country_potential = { has_variable = has_unlocked_quirinal_palace }`
- `allow = { always = no }`
- `build_time = large_cultural_building_time`
- `custom_tags = { unique_palace }`

行为或条件引用：

- [pap_quirinal_palace_decision](ED_Vanilla_Wonder_Construction_Actions.md#pap_quirinal_palace_decision-1447-a14531)：教宗的夏宫；construct_building；[in_game/common/decisions/flavor_decisions_various.txt:1447](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/decisions/flavor_decisions_various.txt:1447>)。

### rahdar — 治安驿站

原版定义：[in_game/common/building_types/event_only_buildings.txt:2999](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/event_only_buildings.txt:2999>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `build_time = cultural_building_time`
- `country_potential = { has_unlocked_building_trigger = { type = rahdar } }`
- `location_potential = { has_road_to_capital = yes }`
- `remove_if = { location = { has_road_to_capital = no } NOT = { owner = { at_war = yes } } NOT = { owner = { in_civil_war = yes } } }`

行为或条件引用：

- [flavor_mug.5](ED_Vanilla_Wonder_Construction_Actions.md#flavor_mug-5-264-a6a566)：保护陆路贸易；unlock_building_effect；[in_game/events/DHE/flavor_mug.txt:264](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_mug.txt:264>)。

### ranganathaswamy_temple_building — $ranganathaswamy_temple$

原版定义：[in_game/common/building_types/event_only_buildings.txt:2250](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/event_only_buildings.txt:2250>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `build_time = religious_building_time`
- `country_potential = { always = no }`
- `allow = { always = no }`
- `remove_if = { location = { NOT = { owner = { religion ?= religion:hindu } } } }`

行为或条件引用：

- [flavor_vij.28](ED_Vanilla_Wonder_Construction_Actions.md#flavor_vij-28-1671-2f8e63)：扩建$ranganathaswamy_temple$；construct_building；[in_game/events/DHE/flavor_vij.txt:1671](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_vij.txt:1671>)。

### red_fort — 红堡

原版定义：[in_game/common/building_types/event_only_buildings.txt:3037](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/event_only_buildings.txt:3037>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `build_time = generic_town_build_time`
- `country_potential = { always = no }`
- `allow = { always = no }`

行为或条件引用：

- [flavor_mug.11](ED_Vanilla_Wonder_Construction_Actions.md#flavor_mug-11-631-a6a566)：[target_location.GetNameWithNoTooltip]红堡；construct_building；[in_game/events/DHE/flavor_mug.txt:631](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_mug.txt:631>)。

### repaired_great_wall_of_china — 万里长城

原版定义：[in_game/common/building_types/unique_buildings.txt:3820](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:3820>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `obsolete = ruined_great_wall_of_china`
- `build_time = huge_unique_build_time`
- `country_potential = { tag = CHI }`
- `allow = { OR = { has_building = building_type:ruined_great_wall_of_china is_historical_route_of_great_wall = yes } }`

行为或条件引用：

- [upgrade_great_wall](ED_Vanilla_Wonder_Construction_Actions.md#upgrade_great_wall-110-52d64e)：upgrade_great_wall；construct_building；[in_game/events/DHE/flavor_chi.txt:110](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_chi.txt:110>)。

### ribat — 里巴特

原版定义：[in_game/common/building_types/unique_buildings.txt:5195](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:5195>)。

- `is_special = yes`
- `max_levels = 1`
- `build_time = small_fort_building`

行为或条件引用：

- [kbo_ribat_fortifications](ED_Vanilla_Wonder_Construction_Actions.md#kbo_ribat_fortifications-48-3a57e3)：里巴特堡垒；unlock_building；[in_game/common/advances/country_kbo.txt:48](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/advances/country_kbo.txt:48>)。

### ribeira_das_naus — 里贝拉造船厂

原版定义：[in_game/common/building_types/event_only_buildings.txt:1002](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/event_only_buildings.txt:1002>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `build_time = generic_event_building`
- `country_potential = { always = no }`
- `allow = { always = no }`

行为或条件引用：

- [flavor_por.33](ED_Vanilla_Wonder_Construction_Actions.md#flavor_por-33-2699-f14e68)：里贝拉造船厂；construct_building；[in_game/events/DHE/flavor_por.txt:2699](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_por.txt:2699>)。

### riksbank — 瑞典国家银行

原版定义：[in_game/common/building_types/event_only_buildings.txt:1226](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/event_only_buildings.txt:1226>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `build_time = generic_town_build_time`
- `country_potential = { always = no }`
- `allow = { always = no }`

行为或条件引用：

- [flavor_swe.60](ED_Vanilla_Wonder_Construction_Actions.md#flavor_swe-60-3033-211578)：瑞典国家银行；construct_building；[in_game/events/DHE/flavor_SWE.txt:3033](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_SWE.txt:3033>)。

### rock_of_monaco — 摩纳哥岩

原版定义：[in_game/common/building_types/event_only_buildings.txt:633](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/event_only_buildings.txt:633>)。

- `is_special = yes`
- `is_foreign = yes`
- `max_levels = 1`
- `build_time = generic_town_build_time`
- `country_potential = { always = no }`
- `allow = { always = no }`

行为或条件引用：

- [flavor_gen.28](ED_Vanilla_Wonder_Construction_Actions.md#flavor_gen-28-1865-55f1ae)：摩纳哥巨岩；change_building_level_in_location；[in_game/events/DHE/flavor_GEN.txt:1865](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_GEN.txt:1865>)。

### rotterdam_admiralty — 鹿特丹海军部

原版定义：[in_game/common/building_types/event_only_buildings.txt:1947](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/event_only_buildings.txt:1947>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `build_time = large_port_building_time`
- `country_potential = { always = no }`
- `location_potential = { this = location:rotterdam is_capital = no }`

行为或条件引用：

- [ned_unified_dutch_admiralties_decision](ED_Vanilla_Wonder_Construction_Actions.md#ned_unified_dutch_admiralties_decision-2096-a14531)：建立五大海军部；construct_building；[in_game/common/decisions/flavor_decisions_various.txt:2096](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/decisions/flavor_decisions_various.txt:2096>)。

### royal_academy_of_arts — 皇家艺术学会

原版定义：[in_game/common/building_types/unique_buildings.txt:2318](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:2318>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `country_potential = { custom_tooltip = { text = royal_academy_of_arts_why OR = { tag = ENG tag = GBR } has_variable = royal_academy_of_arts } }`
- `allow = { always = no }`
- `build_time = cultural_building_time`
- `location_potential = { counts_as_capital = yes }`

行为或条件引用：

- [eng_royal_academy_of_arts_decision](ED_Vanilla_Wonder_Construction_Actions.md#eng_royal_academy_of_arts_decision-915-b67bf8)：皇家艺术学会；construct_building；[in_game/common/decisions/flavor_decisions_eng.txt:915](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/decisions/flavor_decisions_eng.txt:915>)。

### royal_atarazanas_seville — 塞维利亚王家造船厂

原版定义：[in_game/common/building_types/unique_buildings.txt:4109](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:4109>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `country_potential = { always = no }`
- `allow = { always = no }`

未在本次行为定义中发现显式同名引用；仍可能由建筑自身条件、科技/改革解锁或引擎常规建设入口提供。

1337 开局实例：`sevilla`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2003](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2003>)。

### royal_audience_and_chancery — 皇家审问院

原版定义：[in_game/common/building_types/event_only_buildings.txt:4306](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/event_only_buildings.txt:4306>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `build_time = large_cultural_building_time`
- `country_potential = { always = no }`
- `allow = { always = no }`

行为或条件引用：

- `the_exchequer`：财政部；门槛/关联引用；需看上下文；[in_game/common/advances/country_nrm.txt:36](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/advances/country_nrm.txt:36>)。
- [progress_and_literacy](ED_Vanilla_Wonder_Construction_Actions.md#progress_and_literacy-1-4e560e)：进步与识字；门槛/关联引用；需看上下文；[in_game/common/missions/generic_progress_and_literacy_mission_pack.txt:1](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/missions/generic_progress_and_literacy_mission_pack.txt:1>)。
- [flavor_cas.137](ED_Vanilla_Wonder_Construction_Actions.md#flavor_cas-137-8523-9abc78)：设立皇家审问院；construct_building；[in_game/events/DHE/flavor_CAS.txt:8523](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_CAS.txt:8523>)。
- [flavor_cas.138](ED_Vanilla_Wonder_Construction_Actions.md#flavor_cas-138-8574-9abc78)：扩大皇家审问院；construct_building；[in_game/events/DHE/flavor_CAS.txt:8574](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_CAS.txt:8574>)。

### royal_garden — 御花园

原版定义：[in_game/common/building_types/capital_buildings.txt:579](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/capital_buildings.txt:579>)。

- `is_foreign = no`
- `max_levels = 1`
- `build_time = large_capital_build_time`
- `location_potential = { counts_as_capital = yes }`
- `allow = { is_capital = yes country_has_no_other_copy_of_building = { type = royal_garden } }`
- `country_potential = { government_type ?= government_type:monarchy }`

行为或条件引用：

- [estate_cooperation](ED_Vanilla_Wonder_Construction_Actions.md#estate_cooperation-1-821312)：阶层合作；门槛/关联引用；需看上下文；[in_game/common/missions/generic_estate_cooperation_mission_pack.txt:1](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/missions/generic_estate_cooperation_mission_pack.txt:1>)。

1337 开局实例：`fez`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3822](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3822>)；`angkor`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3845](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3845>)。

### royal_society — 皇家学会

原版定义：[in_game/common/building_types/unique_buildings.txt:2251](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:2251>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `country_potential = { custom_tooltip = { text = royal_society_why OR = { tag = ENG tag = GBR } has_variable = royal_society } }`
- `allow = { always = no }`
- `build_time = government_build_time`
- `location_potential = { counts_as_capital = yes }`

行为或条件引用：

- [eng_royal_society_decision](ED_Vanilla_Wonder_Construction_Actions.md#eng_royal_society_decision-844-b67bf8)：皇家学会；construct_building；[in_game/common/decisions/flavor_decisions_eng.txt:844](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/decisions/flavor_decisions_eng.txt:844>)。
- `flavor_eng.199`：自然科学会报；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_ENG.txt:19371](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_ENG.txt:19371>)。
- `flavor_eng.211`：萨弗里蒸汽机；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_ENG.txt:20411](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_ENG.txt:20411>)。
- `flavor_eng.224`：[thomas_paine.GetNameWithNoTooltip]发表《常识》；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_ENG.txt:21703](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_ENG.txt:21703>)。
- `flavor_mos.101`：异彩纷呈的大使团；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_MOS.txt:10158](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_MOS.txt:10158>)。

### ruined_great_wall_of_china — 中国古长城

原版定义：[in_game/common/building_types/unique_buildings.txt:3779](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:3779>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `build_time = huge_unique_build_time`
- `country_potential = { always = no }`
- `allow = { always = no }`

行为或条件引用：

- [upgrade_great_wall](ED_Vanilla_Wonder_Construction_Actions.md#upgrade_great_wall-110-52d64e)：upgrade_great_wall；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_chi.txt:110](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_chi.txt:110>)。
- [flavor_chi.2](ED_Vanilla_Wonder_Construction_Actions.md#flavor_chi-2-138-52d64e)：修缮中国古长城；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_chi.txt:138](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_chi.txt:138>)。

1337 开局实例：`yangguan`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3700](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3700>)；`shazhou`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3701](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3701>)；`kuyu_shazhou`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3702](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3702>)；`chijin`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3703](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3703>)；`jinta`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3704](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3704>)；`suzhou_gansu`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3705](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3705>)；`gaotai`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3706](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3706>)；`ganzhou`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3707](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3707>)；`shandan`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3708](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3708>)；`yongchang_ganzhou`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3709](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3709>)；`xiliang`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3710](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3710>)；`gulang`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3711](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3711>)；`longxi_gongchang`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3712](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3712>)；`tongwei`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3713](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3713>)；`jingning`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3714](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3714>)；`sanchuan`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3715](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3715>)；`kaicheng_guyuan`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3716](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3716>)；`baimachen`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3717](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3717>)；`huanzhou_qingyang`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3718](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3718>)；`anbian`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3719](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3719>)；`jingbian`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3720](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3720>)；`huaiyuan_mizhi`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3721](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3721>)；`yulin`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3722](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3722>)；`kaiguang`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3723](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3723>)；`shenmu`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3724](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3724>)；`fugu`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3725](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3725>)；`hebin`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3726](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3726>)；`yinshan`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3727](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3727>)；`wuchuan`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3728](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3728>)；`pingdi`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3729](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3729>)；`jining`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3730](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3730>)；`erdao`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3731](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3731>)；`weining`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3732](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3732>)；`xuanping`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3733](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3733>)；`xuande`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3734](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3734>)；`longmen_chicheng`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3735](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3735>)；`dushikou`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3736](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3736>)；`yixingzhou`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3737](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3737>)；`liuyuan`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3738](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3738>)；`songzhou`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3739](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3739>)；`quanning`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3740](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3740>)；`naiman`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3741](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3741>)；`yizhou_jurchen`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3742](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3742>)；`kaicheng`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3743](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3743>)。

### sacred_council — 圣堂

原版定义：[in_game/common/building_types/capital_buildings.txt:638](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/capital_buildings.txt:638>)。

- `is_foreign = no`
- `max_levels = 1`
- `build_time = large_capital_build_time`
- `location_potential = { counts_as_capital = yes }`
- `allow = { is_capital = yes country_has_no_other_copy_of_building = { type = sacred_council } }`
- `country_potential = { government_type ?= government_type:theocracy }`
- `remove_if = { OR = { is_no_longer_capital = yes location.owner ?= { government_type != government_type:theocracy } } }`

未在本次行为定义中发现显式同名引用；仍可能由建筑自身条件、科技/改革解锁或引擎常规建设入口提供。

### safaviyya_order_hall — 萨法维教团圣所

原版定义：[in_game/common/building_types/unique_buildings.txt:1190](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:1190>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 2`
- `build_time = soldier_building`
- `allow = { dominant_culture = { has_culture_group = culture_group:iranian_group } dominant_religion ?= religion:shia }`

行为或条件引用：

- [ira_safaviyya_order_hall](ED_Vanilla_Wonder_Construction_Actions.md#ira_safaviyya_order_hall-141-cd7a6f)：萨法维教团圣所；unlock_building；[in_game/common/advances/country_ira.txt:141](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/advances/country_ira.txt:141>)。

### sanssouci — 无忧宫

原版定义：[in_game/common/building_types/event_only_buildings.txt:405](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/event_only_buildings.txt:405>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `build_time = cultural_building_time`
- `country_potential = { always = no }`
- `allow = { always = no }`
- `custom_tags = { unique_palace }`

行为或条件引用：

- [flavor_brapru.1400](ED_Vanilla_Wonder_Construction_Actions.md#flavor_brapru-1400-3269-4fbbec)：无忧无虑；construct_building；[in_game/events/DHE/flavor_brapru.txt:3269](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_brapru.txt:3269>)。
- `flavor_brapru.1401`：无忧宫落成；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_brapru.txt:3341](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_brapru.txt:3341>)。

### schonbrunn_palace — 美泉宫

原版定义：[in_game/common/building_types/event_only_buildings.txt:2068](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/event_only_buildings.txt:2068>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `build_time = large_cultural_building_time`
- `country_potential = { always = no }`
- `allow = { always = no }`
- `custom_tags = { unique_palace }`

行为或条件引用：

- [flavor_hab.25](ED_Vanilla_Wonder_Construction_Actions.md#flavor_hab-25-1256-a07f59)：美泉宫；construct_building；[in_game/events/DHE/flavor_HAB.txt:1256](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_HAB.txt:1256>)。

### school_of_salamanca — 萨拉曼卡大学

原版定义：[in_game/common/building_types/event_only_buildings.txt:3701](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/event_only_buildings.txt:3701>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `build_time = large_cultural_building_time`
- `country_potential = { always = no }`
- `allow = { always = no }`

行为或条件引用：

- [flavor_cas.47](ED_Vanilla_Wonder_Construction_Actions.md#flavor_cas-47-2943-9abc78)：萨拉曼卡学派；construct_building；[in_game/events/DHE/flavor_CAS.txt:2943](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_CAS.txt:2943>)。

### schwaz_mine — 施瓦茨银矿

原版定义：[in_game/common/building_types/event_only_buildings.txt:888](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/event_only_buildings.txt:888>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `country_potential = { always = no }`
- `allow = { always = no }`
- `build_time = infrastructure_build_time`

行为或条件引用：

- [flavor_hab.1201](ED_Vanilla_Wonder_Construction_Actions.md#flavor_hab-1201-6588-a07f59)：施瓦茨银矿；change_building_level_in_location；[in_game/events/DHE/flavor_HAB.txt:6588](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_HAB.txt:6588>)。

### sco_palace_of_holyroodhouse — 荷里路德宫

原版定义：[in_game/common/building_types/event_only_buildings.txt:3226](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/event_only_buildings.txt:3226>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `build_time = large_capital_build_time`
- `country_potential = { always = no }`
- `allow = { always = no }`

行为或条件引用：

- [flavor_sco.207](ED_Vanilla_Wonder_Construction_Actions.md#flavor_sco-207-2674-b81a33)：荷里路德宫；construct_building；[in_game/events/DHE/flavor_SCO.txt:2674](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_SCO.txt:2674>)。

### seat_of_cardinal — 枢机座堂

原版定义：[in_game/common/building_types/unique_buildings.txt:996](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:996>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `allow = { always = no }`
- `country_potential = { custom_tooltip = { text = seat_of_cardinal_why always = no } }`
- `build_time = religious_building_time`
- `remove_if = { NOT = { owner = { religion ?= religion:catholic } } }`
- `on_built = { location = { set_up_cardinal = yes } }`
- `on_destroyed = { location = { cardinal = { remove_cardinal_variables = yes } } }`

行为或条件引用：

- `request_cardinal_seat`：请求任命枢机；门槛/关联引用；需看上下文；[in_game/common/generic_actions/catholic.txt:238](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/generic_actions/catholic.txt:238>)。
- `appoint_dynasty_cardinal`：任命家族枢机；门槛/关联引用；需看上下文；[in_game/common/generic_actions/catholic.txt:380](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/generic_actions/catholic.txt:380>)。
- `remove_cardinal_seat`：移除枢机座堂；destroy_building_forcefully；[in_game/common/generic_actions/catholic.txt:513](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/generic_actions/catholic.txt:513>)。
- [on_game_start](ED_Vanilla_Wonder_Construction_Actions.md#on_game_start-1-fff745)：on_game_start；门槛/关联引用；需看上下文；[in_game/common/on_action/_hardcoded.txt:1](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/on_action/_hardcoded.txt:1>)。
- `on_character_changed_religion`：on_character_changed_religion；门槛/关联引用；需看上下文；[in_game/common/on_action/_hardcoded.txt:6031](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/on_action/_hardcoded.txt:6031>)。
- [on_character_death](ED_Vanilla_Wonder_Construction_Actions.md#on_character_death-2-31b1ea)：on_character_death；门槛/关联引用；需看上下文；[in_game/common/on_action/character_death_pulses.txt:2](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/on_action/character_death_pulses.txt:2>)。
- `western_schism_resolution`：西方教会大分裂；destroy_building_forcefully；[in_game/common/resolutions/western_schism.txt:1](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/resolutions/western_schism.txt:1>)。
- `set_papal_states_schism_cardinal`：set_papal_states_schism_cardinal；门槛/关联引用；需看上下文；[in_game/common/scripted_effects/religious_effects.txt:218](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/scripted_effects/religious_effects.txt:218>)。
- [reinstate_the_pope](ED_Vanilla_Wonder_Construction_Actions.md#reinstate_the_pope-519-26d8ea)：reinstate_the_pope；change_building_level_in_location；[in_game/common/scripted_effects/religious_effects.txt:519](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/scripted_effects/religious_effects.txt:519>)。
- [flavor_pol.49](ED_Vanilla_Wonder_Construction_Actions.md#flavor_pol-49-3263-779f20)：前途远大之人；change_building_level_in_location；[in_game/events/DHE/flavor_pol.txt:3263](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_pol.txt:3263>)。
- `grand_tour_events.38`：有用的引见；门槛/关联引用；需看上下文；[in_game/events/expeditions/grand_tour_events.txt:5147](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/expeditions/grand_tour_events.txt:5147>)。
- [catholic_flavor.100](ED_Vanilla_Wonder_Construction_Actions.md#catholic_flavor-100-961-67b17f)：侄子枢机；门槛/关联引用；需看上下文；[in_game/events/religion/catholic_flavor.txt:961](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/religion/catholic_flavor.txt:961>)。
- [catholic_flavor.101](ED_Vanilla_Wonder_Construction_Actions.md#catholic_flavor-101-1053-67b17f)：[GetCountry('PAP').GetGovernment.GetRulerTitle]派来的侄子枢机；change_building_level_in_location；[in_game/events/religion/catholic_flavor.txt:1053](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/religion/catholic_flavor.txt:1053>)。
- [catholic_flavor.1001](ED_Vanilla_Wonder_Construction_Actions.md#catholic_flavor-1001-1197-67b17f)：[SCOPE.sCountry('actor').GetNameWithNoTooltip]的枢机座堂；construct_building；[in_game/events/religion/catholic_flavor.txt:1197](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/religion/catholic_flavor.txt:1197>)。
- [holy_war.9](ED_Vanilla_Wonder_Construction_Actions.md#holy_war-9-455-3a64a2)：提供枢机席位；construct_building；[in_game/events/religion/holy_war_events.txt:455](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/religion/holy_war_events.txt:455>)。

### segovia_artillery_academy — 塞哥维亚炮兵学院

原版定义：[in_game/common/building_types/event_only_buildings.txt:3733](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/event_only_buildings.txt:3733>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `build_time = soldier_building`
- `country_potential = { always = no }`
- `allow = { always = no }`

行为或条件引用：

- [flavor_cas.63](ED_Vanilla_Wonder_Construction_Actions.md#flavor_cas-63-3872-9abc78)：塞哥维亚炮兵学院；construct_building；[in_game/events/DHE/flavor_CAS.txt:3872](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_CAS.txt:3872>)。

### seljuk_mint — 塞尔柱铸币厂

原版定义：[in_game/common/building_types/unique_buildings.txt:5507](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:5507>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 4`
- `build_time = large_capital_build_time`
- `country_potential = { culture ?= { OR = { this = culture:turkish_culture this = culture:turkoman_culture } } OR = { owns = location:konya owns = location:sivas } }`
- `location_potential = { is_capital = no is_historical_capital = no OR = { this = location:konya this = location:sivas } }`
- `allow = { OR = { has_building = building_type:seljuk_mint has_proximity_source_building = no } }`
- `remove_if = { owner = { NOT = { culture = { OR = { this = culture:turkish_culture this = culture:turkoman_culture } } } } }`

行为或条件引用：

- [rise_of_the_ottomans](ED_Vanilla_Wonder_Construction_Actions.md#rise_of_the_ottomans-1-8c1963)：土耳其人的崛起；门槛/关联引用；需看上下文；[in_game/common/situations/rise_of_the_ottomans.txt:1](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/situations/rise_of_the_ottomans.txt:1>)。

### sevilla_bullfighting_school — 塞维利亚斗牛学校

原版定义：[in_game/common/building_types/event_only_buildings.txt:4273](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/event_only_buildings.txt:4273>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `build_time = large_cultural_building_time`
- `country_potential = { always = no }`
- `allow = { always = no }`

行为或条件引用：

- [flavor_cas.118](ED_Vanilla_Wonder_Construction_Actions.md#flavor_cas-118-7412-9abc78)：塞维利亚斗牛学校；construct_building；[in_game/events/DHE/flavor_CAS.txt:7412](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_CAS.txt:7412>)。
- [flavor_cas.119](ED_Vanilla_Wonder_Construction_Actions.md#flavor_cas-119-7484-9abc78)：反对塞维利亚斗牛学校；destroy_building；[in_game/events/DHE/flavor_CAS.txt:7484](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_CAS.txt:7484>)。

### shipyard — 船厂

原版定义：[in_game/common/building_types/port_buildings.txt:103](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/port_buildings.txt:103>)。

- `is_foreign = no`
- `max_levels = 1`
- `obsolete = dry_dock`
- `location_potential = { is_port = yes }`
- `build_time = large_port_building_time`

行为或条件引用：

- [shipyard_advance](ED_Vanilla_Wonder_Construction_Actions.md#shipyard_advance-847-3be8a5)：船厂；unlock_building；[in_game/common/advances/1_building_unlocks.txt:847](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/advances/1_building_unlocks.txt:847>)。
- `expand_docks`：扩建造船厂；门槛/关联引用；需看上下文；[in_game/common/parliament_issues/05_burghers_estate_parliament_issues.txt:673](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/parliament_issues/05_burghers_estate_parliament_issues.txt:673>)。
- `expand_dry_docks`：扩建造船厂；门槛/关联引用；需看上下文；[in_game/common/parliament_issues/05_burghers_estate_parliament_issues.txt:758](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/parliament_issues/05_burghers_estate_parliament_issues.txt:758>)。
- [expand_shipyards](ED_Vanilla_Wonder_Construction_Actions.md#expand_shipyards-844-428301)：扩建造船厂；construct_building；[in_game/common/parliament_issues/05_burghers_estate_parliament_issues.txt:844](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/parliament_issues/05_burghers_estate_parliament_issues.txt:844>)。
- `has_dock_infrastructure`：has_dock_infrastructure；门槛/关联引用；需看上下文；[in_game/common/scripted_triggers/location_triggers.txt:150](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/scripted_triggers/location_triggers.txt:150>)。
- `unit_war_galleon_location_trigger`：unit_war_galleon_location_trigger；门槛/关联引用；需看上下文；[in_game/common/scripted_triggers/unit_triggers.txt:488](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/scripted_triggers/unit_triggers.txt:488>)。
- `flavor_mos.100`：第一位海军上将；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_MOS.txt:10031](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_MOS.txt:10031>)。
- [fate_of_the_phoenix.2](ED_Vanilla_Wonder_Construction_Actions.md#fate_of_the_phoenix-2-62-8b63b9)：收复[target_location.GetName]！；construct_building；[in_game/events/disaster/D008_fate_of_the_phoenix.txt:62](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/disaster/D008_fate_of_the_phoenix.txt:62>)。

### shoen — 庄园

原版定义：[in_game/common/building_types/unique_buildings.txt:2728](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:2728>)。

- `is_special = yes`
- `is_foreign = yes`
- `max_levels = japanese_clan_building_cap`
- `location_potential = { dominant_culture = { has_culture_group = culture_group:japanese_group } }`
- `country_potential = { OR = { AND = { has_reform = government_reform:japanese_imperial_family country_type = building } has_reform = government_reform:japanese_clan } }`
- `build_time = estate_build_time`
- `allow = { dominant_culture = { has_culture_group = culture_group:japanese_group } OR = { any_foreign_building_countries_in_location = { this = scope:actor } custom_tooltip = { text = we_are_shugo_tt AND = { NOR = { this = location:izumi this = location:iga this = location:awa this = location:oki this = location:awaji } province_definition = { any_location_in_province_definition = { any_foreign_buildings_in_location = { owner ?= scope:actor building_type = building_type:kokufu } } } } } } }`

行为或条件引用：

- [peace_expand_clan_influence](ED_Vanilla_Wonder_Construction_Actions.md#peace_expand_clan_influence-1-19f6b9)：扩张大名影响力；construct_building；[in_game/common/peace_treaties/expand_clan_influence.txt:1](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/peace_treaties/expand_clan_influence.txt:1>)。
- `turn_japanese_clan_into_normal_tag`：turn_japanese_clan_into_normal_tag；门槛/关联引用；需看上下文；[in_game/common/scripted_effects/country_effects.txt:754](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/scripted_effects/country_effects.txt:754>)。
- [turn_japanese_clan_into_building_based](ED_Vanilla_Wonder_Construction_Actions.md#turn_japanese_clan_into_building_based-817-d574b2)：turn_japanese_clan_into_building_based；change_building_level_in_location；[in_game/common/scripted_effects/country_effects.txt:817](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/scripted_effects/country_effects.txt:817>)。

1337 开局实例：`funai`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2620](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2620>)；`yoshino`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2625](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2625>)；`saba`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2698](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2698>)；`ashida`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2702](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2702>)；`joutou`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2706](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2706>)；`tsuga`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2710](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2710>)；`kurita`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2714](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2714>)；`kamioono`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2717](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2717>)；`sawata`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2719](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2719>)；`miyagi`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2723](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2723>)；`awa`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2726](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2726>)；`kamiura`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2728](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2728>)；`onyuu`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2730](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2730>)；`nyuu`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2732](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2732>)；`abe`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2736](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2736>)；`tagata`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2738](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2738>)；`iga`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2742](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2742>)；`kuwada`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2744](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2744>)；`takaichi`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2748](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2748>)；`hoi`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2751](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2751>)；`tama`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2753](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2753>)；`ichihara`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2755](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2755>)；`higashikubiki`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2757](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2757>)；`nukanobu`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2761](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2761>)；`shimokita`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2766](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2766>)；`kamikita`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2768](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2768>)；`taki`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2772](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2772>)；`shima`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2779](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2779>)；`hiraka_aomori`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2781](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2781>)；`miyagi`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2783](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2783>)；`watarai`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2785](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2785>)；`ichishi`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2787](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2787>)；`akita`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2791](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2791>)；`hanawa`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2795](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2795>)；`inaka`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2801](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2801>)；`nishiokitama`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2805](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2805>)；`tama`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2807](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2807>)；`date_loc`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2811](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2811>)；`shinobu`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2814](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2814>)；`shimohei`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2818](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2818>)；`kamihei`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2822](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2822>)；`aki`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2824](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2824>)；`yamamoto`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2828](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2828>)；`iwate`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2830](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2830>)；`waga`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2834](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2834>)；`hienuki`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2838](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2838>)；`tome`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2842](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2842>)；`isawa`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2844](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2844>)；`oshika`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2846](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2846>)；`chiba`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2850](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2850>)；`katsushika`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2854](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2854>)；`iwai`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2856](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2856>)；`musa`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2858](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2858>)；`katori`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2860](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2860>)；`chiba`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2862](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2862>)；`shiwa`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2866](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2866>)；`kurokawa`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2868](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2868>)；`kawabe`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2872](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2872>)；`yuza`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2874](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2874>)；`murayama`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2878](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2878>)；`tagawa`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2882](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2882>)；`namekata`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2886](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2886>)；`uda_mutsu`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2888](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2888>)；`tsukuba`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2890](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2890>)；`souma`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2892](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2892>)；`minamiaizu`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2896](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2896>)；`tachibana`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2902](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2902>)；`iwase`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2904](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2904>)；`tamura`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2908](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2908>)；`yama_jap`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2912](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2912>)；`shirakawa`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2916](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2916>)；`kitaaizu`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2920](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2920>)；`kawanuma`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2922](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2922>)；`niihari`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2926](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2926>)；`kuji_kanto`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2930](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2930>)；`ibaraki`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2932](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2932>)；`tsukuba`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2936](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2936>)；`naka`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2940](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2940>)；`kashima`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2944](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2944>)；`haga`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2948](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2948>)；`kawachi`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2952](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2952>)；`nasu`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2956](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2956>)；`seta`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2960](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2960>)；`nitta`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2964](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2964>)；`ashigara`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2967](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2967>)；`nomi`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2969](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2969>)；`hiki`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2973](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2973>)；`kaisou`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2976](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2976>)；`fugeshi`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2978](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2978>)；`adachi_kanto`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2982](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2982>)；`aikou`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2986](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2986>)；`toshima_kanto`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2992](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2992>)；`kariwa`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2996](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2996>)；`nishikanbara`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2998](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2998>)；`takata`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3002](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3002>)；`kariwa`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3005](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3005>)；`kamo_mikawa`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3010](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3010>)；`nakajima`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3012](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3012>)；`nutari`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3014](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3014>)；`koshi`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3016](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3016>)；`kamo`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3020](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3020>)；`niikawa`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3026](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3026>)；`keta_tajima`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3028](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3028>)；`tonami`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3030](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3030>)；`nei`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3032](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3032>)；`nomi`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3036](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3036>)；`kaga`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3038](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3038>)；`koma_kai`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3042](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3042>)；`yatsushiro`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3046](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3046>)；`aki`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3048](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3048>)；`kamiina`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3052](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3052>)；`tsukama`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3056](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3056>)；`sarashina`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3058](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3058>)；`oochi`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3060](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3060>)；`mima`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3062](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3062>)；`awa_shikoku`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3064](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3064>)；`miyoshi_shikoku`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3066](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3066>)；`chiisagata`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3070](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3070>)；`azumi`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3072](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3072>)；`saku`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3076](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3076>)；`minochi`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3078](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3078>)；`ikaruga`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3082](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3082>)；`gunma`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3086](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3086>)；`kasa`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3088](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3088>)；`nishikubiki`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3090](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3090>)；`toki`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3094](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3094>)；`fuwa_mino`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3097](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3097>)；`katagata`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3099](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3099>)；`mugi`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3101](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3101>)；`ikeda`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3103](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3103>)；`ena`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3107](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3107>)；`gujou`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3111](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3111>)；`yoshiki`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3115](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3115>)；`toyoda`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3119](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3119>)；`ihara`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3122](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3122>)；`fuchi`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3126](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3126>)；`kuma`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3130](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3130>)；`kitou`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3132](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3132>)；`shitara`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3136](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3136>)；`houmi`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3138](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3138>)；`niwa`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3142](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3142>)；`tsuru`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3146](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3146>)；`mie`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3152](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3152>)；`gamou`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3156](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3156>)；`echi`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3158](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3158>)；`takashima`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3162](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3162>)；`awa_shikoku`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3165](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3165>)；`nakata`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3168](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3168>)；`naga`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3173](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3173>)；`awaji`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3175](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3175>)；`aya`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3177](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3177>)；`nagaoka`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3179](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3179>)；`kuse`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3181](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3181>)；`hekikai`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3185](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3185>)；`kasa`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3189](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3189>)；`saga`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3191](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3191>)；`akou`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3195](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3195>)；`shikama`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3199](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3199>)；`osaka`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3201](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3201>)；`akashi`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3203](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3203>)；`hikami`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3205](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3205>)；`nishimuro`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3209](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3209>)；`kaisou`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3213](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3213>)；`takakusa`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3217](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3217>)；`kume_houki`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3221](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3221>)；`kume_houki`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3224](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3224>)；`keta_tajima`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3227](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3227>)；`hino`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3230](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3230>)；`ou`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3234](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3234>)；`oki`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3236](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3236>)；`izumo`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3242](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3242>)；`nita`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3246](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3246>)；`iishi`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3250](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3250>)；`eso`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3254](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3254>)；`noto_jap`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3258](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3258>)；`imizu`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3260](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3260>)；`kanoashi`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3262](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3262>)；`yoshiki_suou`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3268](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3268>)；`nima`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3271](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3271>)；`tagata`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3275](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3275>)；`koyu`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3277](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3277>)；`wake`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3279](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3279>)；`aita`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3283](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3283>)；`aichi`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3287](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3287>)；`naka_iwami`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3289](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3289>)；`kaya`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3295](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3295>)；`asakuchi`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3299](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3299>)；`aki`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3303](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3303>)；`toyota`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3307](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3307>)；`yamagata`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3311](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3311>)；`sera`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3317](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3317>)；`miyoshi`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3321](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3321>)；`tsuno`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3325](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3325>)；`abu`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3329](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3329>)；`toyoura`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3332](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3332>)；`asa`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3335](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3335>)；`ochi`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3338](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3338>)；`mitoyo`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3353](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3353>)；`miki`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3358](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3358>)；`nii`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3362](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3362>)；`aki_shikoku`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3366](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3366>)；`takaoka`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3370](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3370>)；`usa`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3374](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3374>)；`ooita`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3378](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3378>)；`saga`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3383](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3383>)；`koyu`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3385](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3385>)；`kunisaki`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3391](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3391>)；`naoiri`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3393](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3393>)；`onga`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3397](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3397>)；`nakatsu`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3400](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3400>)；`mikasa`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3403](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3403>)；`akita_kumamoto`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3405](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3405>)；`shimoagata`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3407](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3407>)；`asakura`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3412](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3412>)；`kishima`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3416](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3416>)；`higashimatsuura`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3420](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3420>)；`takaki`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3426](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3426>)；`aimi`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3430](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3430>)；`yatsushiro_higo`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3433](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3433>)；`mii`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3436](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3436>)；`mike`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3438](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3438>)；`hita`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3442](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3442>)；`izumi_satsuma`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3444](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3444>)；`higashiusuki`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3448](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3448>)；`miyazaki`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3450](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3450>)；`naka_hyuuga`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3452](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3452>)；`kimotsuki`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3456](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3456>)；`kitamorokata`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3458](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3458>)；`minamimorokata`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3460](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3460>)；`soo`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3463](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3463>)；`satsuma`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3465](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3465>)；`ibusuki`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3470](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3470>)；`kagoshima`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3472](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3472>)；`kuwabara`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3477](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3477>)；`hishikari`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3481](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3481>)；`souma`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3485](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3485>)；`aso`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3491](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3491>)；`mashiki`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3493](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3493>)；`yabu`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3497](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3497>)；`sakai_echizen`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3500](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3500>)；`kitamogami`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3504](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3504>)；`minamiuonuma`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3508](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3508>)；`shioya`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3512](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3512>)；`mashita`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3518](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3518>)；`takaichi`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3522](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3522>)；`mino`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3527](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3527>)；`kita_shikoku`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3531](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3531>)；`iyo`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3535](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3535>)；`uwa`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3540](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3540>)；`ukena`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3544](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3544>)；`nishimatsuura`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3548](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3548>)；`koushi`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3552](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3552>)；`kagoshima`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3556](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3556>)；`kamiagata`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3560](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3560>)；`suwa`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3566](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3566>)；`nuka`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3571](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3571>)；`tosa`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3575](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3575>)；`suzuka`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3581](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3581>)；`nyuu`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3587](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3587>)。

### sie_sienese_port — 锡耶纳港

原版定义：[in_game/common/building_types/event_only_buildings.txt:4418](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/event_only_buildings.txt:4418>)。

- `is_special = yes`
- `max_levels = 1`
- `country_potential = { always = no }`
- `allow = { always = no }`
- `build_time = generic_town_build_time`

行为或条件引用：

- [expand_siena_ports](ED_Vanilla_Wonder_Construction_Actions.md#expand_siena_ports-272-c38786)：expand_siena_ports；construct_building；[in_game/events/DHE/flavor_SIE.txt:272](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_SIE.txt:272>)。

### sofa_barracks — 索法兵营

原版定义：[in_game/common/building_types/unique_buildings.txt:1775](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:1775>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `build_time = soldier_building`
- `country_potential = { has_advance = sofa_levies_advance }`

行为或条件引用：

- [sofa_levies_advance](ED_Vanilla_Wonder_Construction_Actions.md#sofa_levies_advance-101-59f9d8)：索法征召兵；unlock_building；[in_game/common/advances/country_mal.txt:101](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/advances/country_mal.txt:101>)。

### sofa_stockade — 索法土寨

原版定义：[in_game/common/building_types/00_unique_buildings_to_make_obsolete.txt:2](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/00_unique_buildings_to_make_obsolete.txt:2>)。

- `is_special = yes`
- `max_levels = 1`
- `build_time = small_fort_building`
- `country_potential = { has_advance = sofa_levies_advance }`

行为或条件引用：

- [sofa_levies_advance](ED_Vanilla_Wonder_Construction_Actions.md#sofa_levies_advance-101-59f9d8)：索法征召兵；unlock_building；[in_game/common/advances/country_mal.txt:101](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/advances/country_mal.txt:101>)。

### stannary_court — 锡矿区法院

原版定义：[in_game/common/building_types/unique_buildings.txt:1285](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:1285>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `country_potential = { custom_tooltip = { text = stannary_court_why has_or_had_tag = ENG has_variable = stannary_law } }`
- `allow = { always = no }`
- `build_time = government_build_time`
- `location_potential = { }`

行为或条件引用：

- [flavor_eng.66](ED_Vanilla_Wonder_Construction_Actions.md#flavor_eng-66-6031-cfcf19)：锡矿区法院；construct_building；[in_game/events/DHE/flavor_ENG.txt:6031](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_ENG.txt:6031>)。
- [flavor_eng.67](ED_Vanilla_Wonder_Construction_Actions.md#flavor_eng-67-6116-cfcf19)：锡矿采掘的商业化；destroy_building；[in_game/events/DHE/flavor_ENG.txt:6116](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_ENG.txt:6116>)。

1337 开局实例：`exeter`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1517](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1517>)；`plymouth`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1518](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1518>)；`barnstaple`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1519](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1519>)；`okehampton`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1520](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1520>)；`bampton`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1521](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1521>)；`bideford`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1522](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1522>)；`launceston`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1523](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1523>)；`truro`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1524](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1524>)；`bodmin`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1525](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1525>)。

### stroganov_school_of_iconic_art — 斯特罗加诺夫圣像画学校

原版定义：[in_game/common/building_types/unique_buildings.txt:3141](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:3141>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `country_potential = { custom_tooltip = { text = stroganov_school_of_iconic_art_why OR = { tag = MOS tag = RUS } religion ?= religion:orthodox has_variable = stroganov_school_of_iconic_art } }`
- `remove_if = { NOT = { owner = { religion ?= religion:orthodox } } }`
- `allow = { always = no }`
- `build_time = cultural_building_time`
- `location_potential = { this = location:moscow }`

行为或条件引用：

- [mos_stroganov_school_decision](ED_Vanilla_Wonder_Construction_Actions.md#mos_stroganov_school_decision-654-f996cd)：建立斯特罗加诺夫画派；construct_building；[in_game/common/decisions/flavor_decisions_rus.txt:654](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/decisions/flavor_decisions_rus.txt:654>)。
- `flavor_mos.85`：[simon_ushakov.GetNameWithNoTooltip]；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_MOS.txt:8273](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_MOS.txt:8273>)。
- `flavor_mos.95`：赞助人[bogdan_khitrovo.GetNameWithNoTooltip]；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_MOS.txt:9437](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_MOS.txt:9437>)。

### sufi_mosque — 苏菲派清真寺

原版定义：[in_game/common/building_types/unique_buildings.txt:5376](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:5376>)。

- `is_special = yes`
- `max_levels = 1`
- `country_potential = { always = no }`
- `build_time = religious_building_time`

行为或条件引用：

- [flavor_maj.16](ED_Vanilla_Wonder_Construction_Actions.md#flavor_maj-16-945-ceab17)：[target_religion.GetGroup.GetNameWithNoTooltip]登陆；construct_building；[in_game/events/DHE/flavor_maj.txt:945](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_maj.txt:945>)。
- [death_of_hayan_wuruk.6](ED_Vanilla_Wonder_Construction_Actions.md#death_of_hayan_wuruk-6-207-5166af)：[ShowReligionGroupNameWithNoTooltip('muslim')]传播到[GetCountry('MAJ').GetNameWithNoTooltip]；construct_building；[in_game/events/disaster/death_of_hayan_wuruk.txt:207](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/disaster/death_of_hayan_wuruk.txt:207>)。

### sukharev_tower — 苏哈列夫塔

原版定义：[in_game/common/building_types/unique_buildings.txt:3671](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:3671>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `country_potential = { custom_tooltip = { text = sukharev_tower_why OR = { tag = MOS tag = RUS } has_variable = sukharev_tower } }`
- `allow = { always = no }`
- `build_time = large_port_building_time`
- `location_potential = { this = location:moscow }`

行为或条件引用：

- [mos_sukharev_tower_decision](ED_Vanilla_Wonder_Construction_Actions.md#mos_sukharev_tower_decision-1449-f996cd)：苏哈列夫塔；construct_building；[in_game/common/decisions/flavor_decisions_rus.txt:1449](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/decisions/flavor_decisions_rus.txt:1449>)。

### swi_collegium_helveticum — 赫尔维蒂学院

原版定义：[in_game/common/building_types/event_only_buildings.txt:2423](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/event_only_buildings.txt:2423>)。

- `is_special = yes`
- `is_foreign = yes`
- `max_levels = 1`
- `country_potential = { OR = { has_or_had_tag = SWI has_or_had_tag = BCH has_or_had_tag = STG has_or_had_tag = ZUR has_or_had_tag = SYZ has_or_had_tag = GLR has_or_had_tag = URI has_or_had_tag = OBW has_or_had_tag = LCU has_or_had_tag = SIT has_or_had_tag = BRN has_or_had_tag = SLT has_or_had_tag = NEU has_or_had_tag = BAS has_or_had_tag = LSA has_or_had_tag = KYB has_or_had_tag = TRN has_or_had_tag = GNV has_or_had_tag = SCL has_or_had_tag = WER } }`
- `allow = { custom_tooltip = { text = swi_collegium_helveticum_why always = no } }`
- `build_time = cultural_building_time`

行为或条件引用：

- [flavor_swi.1200](ED_Vanilla_Wonder_Construction_Actions.md#flavor_swi-1200-1392-b1a415)：赫尔维蒂学院；construct_building；[in_game/events/DHE/flavor_swi.txt:1392](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_swi.txt:1392>)。
- `flavor_swi.1201`：赫尔维蒂学院毕业生；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_swi.txt:1474](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_swi.txt:1474>)。

### tambo — 山地驿站

原版定义：[in_game/common/building_types/unique_buildings.txt:2177](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:2177>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `location_potential = { num_roads > 0 }`
- `build_time = infrastructure_build_time`

行为或条件引用：

- [tambo_advance](ED_Vanilla_Wonder_Construction_Actions.md#tambo_advance-71-1ecb36)：山地驿站；unlock_building；[in_game/common/advances/country_inc.txt:71](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/advances/country_inc.txt:71>)。

### tatara — 吹踏炉

原版定义：[in_game/common/building_types/unique_buildings.txt:2854](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:2854>)。

- `is_special = yes`
- `is_foreign = yes`
- `max_levels = japanese_clan_building_cap`
- `location_potential = { dominant_culture = { has_culture_group = culture_group:japanese_group } }`
- `country_potential = { OR = { AND = { has_reform = government_reform:japanese_imperial_family country_type = building } has_reform = government_reform:japanese_clan } }`
- `build_time = estate_build_time`
- `allow = { dominant_culture = { has_culture_group = culture_group:japanese_group } any_foreign_building_countries_in_location = { this = scope:actor } }`

未在本次行为定义中发现显式同名引用；仍可能由建筑自身条件、科技/改革解锁或引擎常规建设入口提供。

1337 开局实例：`yoshino`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2626](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2626>)；`kurita`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2715](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2715>)；`miyagi`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2724](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2724>)；`takaichi`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2749](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2749>)；`nukanobu`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2762](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2762>)；`taki`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2773](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2773>)；`akita`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2792](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2792>)；`date_loc`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2812](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2812>)；`chiba`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2851](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2851>)；`nitta`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2965](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2965>)；`hiki`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2974](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2974>)；`takata`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3003](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3003>)；`kamo`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3021](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3021>)；`koma_kai`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3043](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3043>)；`kamiina`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3053](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3053>)；`ikaruga`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3083](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3083>)；`toki`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3095](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3095>)；`toyoda`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3120](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3120>)；`nakata`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3169](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3169>)；`akou`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3196](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3196>)；`keta_tajima`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3228](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3228>)；`yoshiki_suou`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3269](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3269>)；`ooita`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3379](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3379>)；`nakatsu`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3401](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3401>)；`higashimatsuura`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3421](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3421>)；`satsuma`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3467](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3467>)；`yabu`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3498](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3498>)；`shioya`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3513](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3513>)；`takaichi`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3523](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3523>)；`kamiagata`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3561](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3561>)；`tosa`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3576](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3576>)；`nyuu`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3588](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3588>)。

### teatro_san_cassiano — 圣卡夏诺剧院

原版定义：[in_game/common/building_types/event_only_buildings.txt:2109](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/event_only_buildings.txt:2109>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `country_potential = { custom_tooltip = { text = unlocked_teatro_san_cassiano_tt has_variable = unlocked_teatro_san_cassiano } }`
- `allow = { always = no }`
- `build_time = large_cultural_building_time`

行为或条件引用：

- [ven_teatro_san_cassiano_decision](ED_Vanilla_Wonder_Construction_Actions.md#ven_teatro_san_cassiano_decision-1295-a14531)：圣卡夏诺剧院；construct_building；[in_game/common/decisions/flavor_decisions_various.txt:1295](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/decisions/flavor_decisions_various.txt:1295>)。

### telpochcalli — 特尔波奇卡利学校

原版定义：[in_game/common/building_types/unique_buildings.txt:1955](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:1955>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `build_time = soldier_building`
- `country_potential = { culture = { has_culture_group = culture_group:nahua_group } }`
- `location_potential = { counts_as_capital = yes }`
- `allow = { is_capital = yes country_has_no_other_copy_of_building = { type = telpochcalli } }`

行为或条件引用：

- [warrior_societies](ED_Vanilla_Wonder_Construction_Actions.md#warrior_societies-10-f0f87f)：战士社会；unlock_building；[in_game/common/advances/country_tnc.txt:10](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/advances/country_tnc.txt:10>)。

1337 开局实例：`tenochtitlan`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2516](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2516>)。

### temple — 神庙

原版定义：[in_game/common/building_types/town_buildings.txt:1](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/town_buildings.txt:1>)。

- `is_foreign = no`
- `max_levels = 1`
- `build_time = religious_building_time`

行为或条件引用：

- [sponsor_a_great_madrasa_decision](ED_Vanilla_Wonder_Construction_Actions.md#sponsor_a_great_madrasa_decision-99-57c555)：资助一座大伊斯兰学院；门槛/关联引用；需看上下文；[in_game/common/decisions/generic_age_decisions.txt:99](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/decisions/generic_age_decisions.txt:99>)。
- [estate_cooperation](ED_Vanilla_Wonder_Construction_Actions.md#estate_cooperation-1-821312)：阶层合作；门槛/关联引用；需看上下文；[in_game/common/missions/generic_estate_cooperation_mission_pack.txt:1](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/missions/generic_estate_cooperation_mission_pack.txt:1>)。
- `cultural_event.11`：[ShowModifierWithNoTooltip('south_german_organ_tradition')]；门槛/关联引用；需看上下文；[in_game/events/culture/cultural_event.txt:302](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/culture/cultural_event.txt:302>)。
- [flavor_ayu.8](ED_Vanilla_Wonder_Construction_Actions.md#flavor_ayu-8-481-62f2b4)：佛陀的足迹；construct_building；[in_game/events/DHE/flavor_ayu.txt:481](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_ayu.txt:481>)。
- `flavor_dan.25`：冲击圣母教堂；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_dan.txt:1755](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_dan.txt:1755>)。
- `flavor_dan.67`：埃尔梅隆德壁画；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_dan.txt:3843](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_dan.txt:3843>)。
- [flavor_eth.50](ED_Vanilla_Wonder_Construction_Actions.md#flavor_eth-50-306-2d218a)：德布雷伯尔汉——光明之山；change_building_level_in_location；[in_game/events/DHE/flavor_ETH.txt:306](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_ETH.txt:306>)。
- [flavor_eth.240](ED_Vanilla_Wonder_Construction_Actions.md#flavor_eth-240-2701-2d218a)：天空中闪耀的新光；construct_building；[in_game/events/DHE/flavor_ETH.txt:2701](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_ETH.txt:2701>)。
- [flavor_hab.40](ED_Vanilla_Wonder_Construction_Actions.md#flavor_hab-40-2201-a07f59)：弗劳恩施泰因慈悲圣母像；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_HAB.txt:2201](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_HAB.txt:2201>)。
- [flavor_ira.24](ED_Vanilla_Wonder_Construction_Actions.md#flavor_ira-24-1474-f0bbd0)：[target_location.GetNameWithNoTooltip]；construct_building；[in_game/events/DHE/flavor_ira.txt:1474](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_ira.txt:1474>)。
- [flavor_jap.145](ED_Vanilla_Wonder_Construction_Actions.md#flavor_jap-145-2672-b3bd1b)：相国寺；construct_building；[in_game/events/DHE/flavor_JAP.txt:2672](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_JAP.txt:2672>)。
- [flavor_maj.13](ED_Vanilla_Wonder_Construction_Actions.md#flavor_maj-13-695-ceab17)：老鼠寺；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_maj.txt:695](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_maj.txt:695>)。
- [flavor_maj.14](ED_Vanilla_Wonder_Construction_Actions.md#flavor_maj-14-773-ceab17)：苏腊瓦纳寺；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_maj.txt:773](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_maj.txt:773>)。
- `flavor_mam.23`：[target_character.GetNameWithNoTooltip]的清真寺学院；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_MAM.txt:1201](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_MAM.txt:1201>)。
- [flavor_nov.12](ED_Vanilla_Wonder_Construction_Actions.md#flavor_nov-12-712-51d2dc)：救主变容教堂；change_building_level_in_location；[in_game/events/DHE/flavor_NOV.txt:712](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_NOV.txt:712>)。
- [flavor_ori.7](ED_Vanilla_Wonder_Construction_Actions.md#flavor_ori-7-435-91f915)：迦毗罗娑伐罗[ShowGodNameWithNoTooltip('shiva_god')]庙；construct_building；[in_game/events/DHE/flavor_ori.txt:435](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_ori.txt:435>)。
- `flavor_ori.15`：赞助羯陵伽建筑；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_ori.txt:921](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_ori.txt:921>)。
- [flavor_pol.57](ED_Vanilla_Wonder_Construction_Actions.md#flavor_pol-57-3840-779f20)：[target_character.GetNameWithNoTooltip]；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_pol.txt:3840](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_pol.txt:3840>)。
- [flavor_tim.14](ED_Vanilla_Wonder_Construction_Actions.md#flavor_tim-14-1123-272e59)：[target_region.GetNameWithNoTooltip]的明珠；construct_building；[in_game/events/DHE/flavor_tim.txt:1123](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_tim.txt:1123>)。
- [flavor_ven.29](ED_Vanilla_Wonder_Construction_Actions.md#flavor_ven-29-1341-888d6c)：圣若望及保禄大殿；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_VEN.txt:1341](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_VEN.txt:1341>)。
- [treasure_fleet_events.44](ED_Vanilla_Wonder_Construction_Actions.md#treasure_fleet_events-44-2380-12721f)：清真寺修建请求；construct_building；[in_game/events/expeditions/treasure_fleet_events.txt:2380](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/expeditions/treasure_fleet_events.txt:2380>)。
- `location_catholic_flavor_9_trigger`：location_catholic_flavor_9_trigger；门槛/关联引用；需看上下文；[in_game/events/religion/catholic_flavor.txt:425](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/religion/catholic_flavor.txt:425>)。
- [hellenism_religion.14](ED_Vanilla_Wonder_Construction_Actions.md#hellenism_religion-14-1332-1e4990)：[target_province.GetNameWithNoTooltip]忽视了[target_god.GetNameWithNoTooltip]；destroy_building；[in_game/events/religion/hellenism_religion.txt:1332](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/religion/hellenism_religion.txt:1332>)。
- `hellenism_religion.23`：宗教用地扩建；门槛/关联引用；需看上下文；[in_game/events/religion/hellenism_religion.txt:2049](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/religion/hellenism_religion.txt:2049>)。
- `hindu_events.2500`：太阳神殿；门槛/关联引用；需看上下文；[in_game/events/religion/hindu_events.txt:2105](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/religion/hindu_events.txt:2105>)。
- `hindu_events.2600`：季节变换；门槛/关联引用；需看上下文；[in_game/events/religion/hindu_events.txt:2176](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/religion/hindu_events.txt:2176>)。
- `hussite_loc_root_region_with_temple_or_cathedral`：hussite_loc_root_region_with_temple_or_cathedral；门槛/关联引用；需看上下文；[in_game/events/religion/hussite_flavor.txt:15](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/religion/hussite_flavor.txt:15>)。
- [ikko_ikki.3](ED_Vanilla_Wonder_Construction_Actions.md#ikko_ikki-3-228-8858cf)：[target_io.GetNameWithNoTooltip]；construct_building；[in_game/events/religion/ikko_ikki.txt:228](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/religion/ikko_ikki.txt:228>)。
- `ikko_ikki.4`：寺内町；门槛/关联引用；需看上下文；[in_game/events/religion/ikko_ikki.txt:407](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/religion/ikko_ikki.txt:407>)。
- [miaphysite_flavor.32](ED_Vanilla_Wonder_Construction_Actions.md#miaphysite_flavor-32-709-53c86d)：新的时代；construct_building；[in_game/events/religion/miaphsyite_flavor.txt:709](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/religion/miaphsyite_flavor.txt:709>)。
- [muslim_school_events.3](ED_Vanilla_Wonder_Construction_Actions.md#muslim_school_events-3-121-8529b1)：新的伊斯兰学院；门槛/关联引用；需看上下文；[in_game/events/religion/muslim_school_events.txt:121](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/religion/muslim_school_events.txt:121>)。
- [nahuatl_events.29](ED_Vanilla_Wonder_Construction_Actions.md#nahuatl_events-29-1139-013d7a)：[ROOT.GetCountry.GetCapital.GetNameWithNoTooltip]主庙的扩张；门槛/关联引用；需看上下文；[in_game/events/religion/nahuatl_events.txt:1139](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/religion/nahuatl_events.txt:1139>)。
- `orthodox_icon_events.5`：圣尼古拉的三件礼物；门槛/关联引用；需看上下文；[in_game/events/religion/orthodox_icon_events.txt:122](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/religion/orthodox_icon_events.txt:122>)。
- [propagate_religion_events.5](ED_Vanilla_Wonder_Construction_Actions.md#propagate_religion_events-5-440-4e45a2)：[target_location.GetNameWithNoTooltip]的清真寺落成；change_building_level_in_location；[in_game/events/religion/propagate_religion_events.txt:440](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/religion/propagate_religion_events.txt:440>)。

### temple_militia — 教会卫队驻地

原版定义：[in_game/common/building_types/manpower_buildings.txt:468](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/manpower_buildings.txt:468>)。

- `is_foreign = no`
- `max_levels = 1`
- `build_time = medium_soldier_building`
- `location_potential = { counts_as_capital = yes }`
- `allow = { is_capital = yes country_has_no_other_copy_of_building = { type = temple_militia } }`
- `country_potential = { government_type ?= government_type:theocracy NOT = { has_reform = government_reform:military_order_reform } }`
- `remove_if = { OR = { is_no_longer_capital = yes location.owner ?= { has_reform = government_reform:military_order_reform } } }`

未在本次行为定义中发现显式同名引用；仍可能由建筑自身条件、科技/改革解锁或引擎常规建设入口提供。

### terraces — 梯田

原版定义：[in_game/common/building_types/unique_buildings.txt:2135](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:2135>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `location_potential = { OR = { topography = mountains topography = plateau topography = hills } }`
- `build_time = infrastructure_build_time`

行为或条件引用：

- [terraces_advance](ED_Vanilla_Wonder_Construction_Actions.md#terraces_advance-10-8aa708)：梯田；unlock_building；[in_game/common/advances/culture_andean.txt:10](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/advances/culture_andean.txt:10>)。

1337 开局实例：`teyuna`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2572](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2572>)；`chunsua`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2573](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2573>)；`hatunqulla`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2574](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2574>)；`chucuito`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2575](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2575>)。

### the_bock_fortifications — 博克城墙

原版定义：[in_game/common/building_types/unique_buildings.txt:3729](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:3729>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = bock_max_level`
- `country_potential = { always = no }`
- `allow = { always = no }`
- `location_potential = { this = location:luxembourg }`
- `build_time = medium_fort_building`

未在本次行为定义中发现显式同名引用；仍可能由建筑自身条件、科技/改革解锁或引擎常规建设入口提供。

1337 开局实例：`luxembourg`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2175](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2175>)。

### the_cipher_secretary — 密码秘书处

原版定义：[in_game/common/building_types/event_only_buildings.txt:3977](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/event_only_buildings.txt:3977>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `build_time = large_cultural_building_time`
- `country_potential = { always = no }`
- `allow = { always = no }`

行为或条件引用：

- [flavor_ven.99](ED_Vanilla_Wonder_Construction_Actions.md#flavor_ven-99-5359-888d6c)：密码秘书处；construct_building；[in_game/events/DHE/flavor_VEN.txt:5359](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_VEN.txt:5359>)。

### theater — 剧场

原版定义：[in_game/common/building_types/culture_buildings.txt:258](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/culture_buildings.txt:258>)。

- `is_foreign = no`
- `max_levels = 1`
- `build_time = cultural_building_time`

行为或条件引用：

- [theater_advance](ED_Vanilla_Wonder_Construction_Actions.md#theater_advance-1085-3be8a5)：剧场；unlock_building；[in_game/common/advances/1_building_unlocks.txt:1085](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/advances/1_building_unlocks.txt:1085>)。
- [estate_cooperation](ED_Vanilla_Wonder_Construction_Actions.md#estate_cooperation-1-821312)：阶层合作；门槛/关联引用；需看上下文；[in_game/common/missions/generic_estate_cooperation_mission_pack.txt:1](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/missions/generic_estate_cooperation_mission_pack.txt:1>)。
- [progress_and_literacy](ED_Vanilla_Wonder_Construction_Actions.md#progress_and_literacy-1-4e560e)：进步与识字；门槛/关联引用；需看上下文；[in_game/common/missions/generic_progress_and_literacy_mission_pack.txt:1](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/missions/generic_progress_and_literacy_mission_pack.txt:1>)。
- `flavor_cas.92`：[target_character.GetNameWithNoTooltip]；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_CAS.txt:5798](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_CAS.txt:5798>)。
- `flavor_cas.93`：智慧的凤凰；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_CAS.txt:5864](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_CAS.txt:5864>)。
- `flavor_dan.22`：[target_artist.GetNameWithNoTooltip]；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_dan.txt:1491](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_dan.txt:1491>)。
- `flavor_dan.23`：[target_artist.GetNameWithNoTooltip]的剧作；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_dan.txt:1556](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_dan.txt:1556>)。
- `flavor_eng.139`：[christopher_marlowe.GetNameWithNoTooltip]；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_ENG.txt:12932](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_ENG.txt:12932>)。
- `flavor_eng.153`：[ROOT.GetCountry.GetGovernment.GetRuler.GetNameWithNoTooltip]的剧团；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_ENG.txt:14533](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_ENG.txt:14533>)。
- `flavor_eng.197`：[aphra_behn.GetNameWithNoTooltip]；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_ENG.txt:19255](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_ENG.txt:19255>)。
- `flavor_eng.206`：美才女奈尔；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_ENG.txt:19981](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_ENG.txt:19981>)。
- [flavor_pap.42](ED_Vanilla_Wonder_Construction_Actions.md#flavor_pap-42-2546-09eb6b)：筹建首座剧场；construct_building；[in_game/events/DHE/flavor_pap.txt:2546](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_pap.txt:2546>)。
- [flavor_rus.56](ED_Vanilla_Wonder_Construction_Actions.md#flavor_rus-56-4553-201f60)：看得起的表演；destroy_building；[in_game/events/DHE/flavor_RUS.txt:4553](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_RUS.txt:4553>)。
- `flavor_rus.57`：[michael_maddox.GetNameWithNoTooltip]；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_RUS.txt:4701](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_RUS.txt:4701>)。

### theodosian_walls — 狄奥多西城墙

原版定义：[in_game/common/building_types/unique_buildings.txt:4441](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:4441>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = theodosian_walls_max_level`
- `build_time = huge_unique_build_time`
- `location_potential = { this = location:constantinople }`
- `country_potential = { owns = location:constantinople }`
- `allow = { owner = { or = { is_ai = no not = { has_or_had_tag = TUR } and = { has_or_had_tag = TUR c:TUR.religion = location:constantinople.dominant_religion } } } }`
- `remove_if = { root.owner = { is_ai = yes has_or_had_tag = TUR not = { c:TUR.religion = location:constantinople.dominant_religion } } }`

行为或条件引用：

- [pa_construct_city_walls](ED_Vanilla_Wonder_Construction_Actions.md#pa_construct_city_walls-1016-cf85e0)：要求$city_walls$；门槛/关联引用；需看上下文；[in_game/common/parliament_agendas/03_buildings.txt:1016](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/parliament_agendas/03_buildings.txt:1016>)。
- [flavor_byz.53](ED_Vanilla_Wonder_Construction_Actions.md#flavor_byz-53-4629-64397c)：加固狄奥多西城墙；change_building_level_in_location；[in_game/events/DHE/flavor_BYZ.txt:4629](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_BYZ.txt:4629>)。

1337 开局实例：`constantinople`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2354](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2354>)。

### tibetan_great_monastery — 藏式大佛寺

原版定义：[in_game/common/building_types/event_only_buildings.txt:146](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/event_only_buildings.txt:146>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `build_time = religious_building_time`
- `country_potential = { always = no }`
- `allow = { always = no }`
- `remove_if = { location = { NOT = { owner = { religion ?= religion:tibetan_buddhism } } } }`

行为或条件引用：

- [buddhism_events.1201](ED_Vanilla_Wonder_Construction_Actions.md#buddhism_events-1201-1472-664d94)：信使从[ShowRegionNameWithNoTooltip('tibet_region')]归来；change_building_level_in_location；[in_game/events/religion/buddhism_events.txt:1472](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/religion/buddhism_events.txt:1472>)。
- `buddhism_events.1202`：喇嘛圆寂；门槛/关联引用；需看上下文；[in_game/events/religion/buddhism_events.txt:1530](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/religion/buddhism_events.txt:1530>)。

### toll_castle — 关卡堡垒

原版定义：[in_game/common/building_types/estate_buildings.txt:3](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/estate_buildings.txt:3>)。

- `is_foreign = no`
- `max_levels = estate_building_single_level`
- `build_time = estate_build_time`

行为或条件引用：

- [pa_remove_toll_castle](ED_Vanilla_Wonder_Construction_Actions.md#pa_remove_toll_castle-513-cf85e0)：处理关于$toll_castle$的投诉；change_building_level_in_location；[in_game/common/parliament_agendas/03_buildings.txt:513](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/parliament_agendas/03_buildings.txt:513>)。
- [random_event.94](ED_Vanilla_Wonder_Construction_Actions.md#random_event-94-4839-f69e59)：本地[ROOT.GetCountry.GetGovernment.GetEstateNameWithNoTooltip('nobles_estate')]势力膨胀；destroy_building；[in_game/events/random_event.txt:4839](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/random_event.txt:4839>)。

### tower_of_belem — 贝伦塔

原版定义：[in_game/common/building_types/event_only_buildings.txt:196](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/event_only_buildings.txt:196>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `build_time =generic_town_build_time`
- `country_potential = { always = no }`
- `allow = { always = no }`

行为或条件引用：

- [flavor_por.5](ED_Vanilla_Wonder_Construction_Actions.md#flavor_por-5-193-f14e68)：贝伦塔；construct_building；[in_game/events/DHE/flavor_por.txt:193](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_por.txt:193>)。

### trade_company_harbor — 公司物流港

原版定义：[in_game/common/building_types/trade_company_buildings.txt:233](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/trade_company_buildings.txt:233>)。

- `is_foreign = yes`
- `max_levels = trade_company_building_max_level`
- `build_time = trade_company_build_time`
- `location_potential = { scope:actor = { has_variable_list = trade_company_regions is_target_in_variable_list = { name = trade_company_regions target = root.region } } }`
- `country_potential = { OR = { total_effective_building_levels:trade_company_headquarters > 0 any_subject = { total_effective_building_levels:trade_company_headquarters > 0 } } }`
- `allow = { is_port = yes market = { in_trade_range_of = scope:actor } can_build_satellite_trade_building = { BUILDING_TYPE = trade_company_harbor } }`
- `custom_tags = { trade_company_building satellite_trade_building }`
- `on_built = { owner = { if = { limit = { NOT = { has_variable = trade_company_home_region } } save_temporary_scope_as = owner_scope random_in_list = { variable = trade_company_subjects limit = { has_variable = trade_company_home_region var:trade_company_home_region = { save_temporary_scope_as = target_region } scope:owner_scope = { is_target_in_variable_list = { name = trade_company_regions target = scope:target_region } } } save_scope_as = trade_company_country } if = { limit = { exists = scope:trade_company_country } root = { change_building_owner = scope:trade_company_country } } else = { root.location = { destroy_building = root } } } } }`

行为或条件引用：

- [trade_companies_advance](ED_Vanilla_Wonder_Construction_Actions.md#trade_companies_advance-207-68d0f2)：贸易公司；unlock_building；[in_game/common/advances/0_age_of_reformation.txt:207](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/advances/0_age_of_reformation.txt:207>)。

### trans_saharan_trade_outposts — 跨撒哈拉驿站

原版定义：[in_game/common/building_types/unique_buildings.txt:4857](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:4857>)。

- `is_special = yes`
- `is_foreign = yes`
- `max_levels = 1`
- `country_potential = { custom_tooltip = { text = son_unlocked_trans_saharan_outposts_tt has_variable = son_trans_saharan_trade_building_variable } }`
- `allow = { OR = { this = location:cairo this = location:fez this = location:tunis } }`
- `build_time = trade_post_build_time`

未在本次行为定义中发现显式同名引用；仍可能由建筑自身条件、科技/改革解锁或引擎常规建设入口提供。

### tribes_of_galway — 戈尔韦氏族部落

原版定义：[in_game/common/building_types/unique_buildings.txt:613](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:613>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `build_time = small_capital_build_time`
- `country_potential = { always = no }`
- `allow = { always = no }`

未在本次行为定义中发现显式同名引用；仍可能由建筑自身条件、科技/改革解锁或引擎常规建设入口提供。

1337 开局实例：`galway`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1557](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1557>)。

### tur_kodjabashi_office — 科贾巴瑟治所

原版定义：[in_game/common/building_types/unique_buildings.txt:5598](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:5598>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `build_time = large_capital_build_time`
- `country_potential = { has_unlocked_building_trigger = { type = tur_kodjabashi_office } }`
- `location_potential = { custom_tooltip = { text = tur_kodjabashi_office_is_in_balkans region = region:balkan_region } OR = { integration_level = conquered integration_level = integrated } custom_tooltip = { text = tur_kodjabashi_office_is_not_capital is_capital = no } }`

行为或条件引用：

- [flavor_tur.186](ED_Vanilla_Wonder_Construction_Actions.md#flavor_tur-186-14938-bf9554)：[ShowRegionNameWithNoTooltip('balkan_region')]科贾巴瑟阶层的崛起；unlock_building_effect；[in_game/events/DHE/flavor_TUR.txt:14938](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_TUR.txt:14938>)。

### uffizi — 乌菲齐公馆

原版定义：[in_game/common/building_types/unique_buildings.txt:1552](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:1552>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `build_time = small_capital_build_time`
- `location_potential = { counts_as_capital = yes }`
- `allow = { is_capital = yes country_has_no_other_copy_of_building = { type = uffizi } }`

行为或条件引用：

- [tuscan_uffizi](ED_Vanilla_Wonder_Construction_Actions.md#tuscan_uffizi-43-e80cbe)：乌菲齐；unlock_building；[in_game/common/advances/country_tus.txt:43](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/advances/country_tus.txt:43>)。

### university — 大学

原版定义：[in_game/common/building_types/culture_buildings.txt:1](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/culture_buildings.txt:1>)。

- `is_foreign = no`
- `max_levels = 1`
- `build_time = large_cultural_building_time`
- `allow = { is_core_of = owner owner = { modifier:university_construction_blocked = no } }`

行为或条件引用：

- [university_advance](ED_Vanilla_Wonder_Construction_Actions.md#university_advance-1067-3be8a5)：大学；unlock_building；[in_game/common/advances/1_building_unlocks.txt:1067](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/advances/1_building_unlocks.txt:1067>)。
- [eng_royal_society_decision](ED_Vanilla_Wonder_Construction_Actions.md#eng_royal_society_decision-844-b67bf8)：皇家学会；门槛/关联引用；需看上下文；[in_game/common/decisions/flavor_decisions_eng.txt:844](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/decisions/flavor_decisions_eng.txt:844>)。
- `clergy_lecture_oaths`：讲学之誓；门槛/关联引用；需看上下文；[in_game/common/estate_privileges/clergy_estate.txt:114](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/estate_privileges/clergy_estate.txt:114>)。
- `education_elites_law`：精英的教育；门槛/关联引用；需看上下文；[in_game/common/laws/01_common.txt:2](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/laws/01_common.txt:2>)。
- [por_estudo_geral_law](ED_Vanilla_Wonder_Construction_Actions.md#por_estudo_geral_law-468-0dfc4e)：通识学院；change_building_level_in_location, destroy_building；[in_game/common/laws/02_country_specific.txt:468](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/laws/02_country_specific.txt:468>)。
- [progress_and_literacy](ED_Vanilla_Wonder_Construction_Actions.md#progress_and_literacy-1-4e560e)：进步与识字；门槛/关联引用；需看上下文；[in_game/common/missions/generic_progress_and_literacy_mission_pack.txt:1](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/missions/generic_progress_and_literacy_mission_pack.txt:1>)。
- [sponsor_a_university](ED_Vanilla_Wonder_Construction_Actions.md#sponsor_a_university-2-428301)：赞助$university$；construct_building；[in_game/common/parliament_issues/05_burghers_estate_parliament_issues.txt:2](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/parliament_issues/05_burghers_estate_parliament_issues.txt:2>)。
- `scholars_calling`：学者；门槛/关联引用；需看上下文；[in_game/common/religious_order_callings/00_monastic.txt:44](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/religious_order_callings/00_monastic.txt:44>)。
- `renaissance_plausible_location`：renaissance_plausible_location；门槛/关联引用；需看上下文；[in_game/common/scripted_triggers/institution_triggers.txt:6](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/scripted_triggers/institution_triggers.txt:6>)。
- `printing_press_plausible_location`：printing_press_plausible_location；门槛/关联引用；需看上下文；[in_game/common/scripted_triggers/institution_triggers.txt:81](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/scripted_triggers/institution_triggers.txt:81>)。
- `scientific_revolution_plausible_location`：scientific_revolution_plausible_location；门槛/关联引用；需看上下文；[in_game/common/scripted_triggers/institution_triggers.txt:190](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/scripted_triggers/institution_triggers.txt:190>)。
- `enlightenment_plausible_location`：enlightenment_plausible_location；门槛/关联引用；需看上下文；[in_game/common/scripted_triggers/institution_triggers.txt:223](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/scripted_triggers/institution_triggers.txt:223>)。
- [reformation](ED_Vanilla_Wonder_Construction_Actions.md#reformation-1-e4f75f)：宗教改革；门槛/关联引用；需看上下文；[in_game/common/situations/reformation.txt:1](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/situations/reformation.txt:1>)。
- `cultural_event.14`：资助[target_location.GetNameWithNoTooltip]的大学；门槛/关联引用；需看上下文；[in_game/events/culture/cultural_event.txt:434](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/culture/cultural_event.txt:434>)。
- `culture_greek.10`：[target_location.GetNameWithNoTooltip]的新一代；门槛/关联引用；需看上下文；[in_game/events/culture/culture_greek.txt:1122](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/culture/culture_greek.txt:1122>)。
- [italian_renaissance_culture.28](ED_Vanilla_Wonder_Construction_Actions.md#italian_renaissance_culture-28-1807-6b7489)：建立欢乐之家；construct_building；[in_game/events/culture/culture_italian.txt:1807](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/culture/culture_italian.txt:1807>)。
- `flavor_ara.7`：[target_character.GetNameWithNoTooltip]；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_ARA.txt:207](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_ARA.txt:207>)。
- `flavor_ara.9`：[target_character.GetNameWithNoTooltip]；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_ARA.txt:350](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_ARA.txt:350>)。
- [ara_university_event_rewards](ED_Vanilla_Wonder_Construction_Actions.md#ara_university_event_rewards-1846-e41b99)：ara_university_event_rewards；construct_building；[in_game/events/DHE/flavor_ARA.txt:1846](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_ARA.txt:1846>)。
- [flavor_arm.1](ED_Vanilla_Wonder_Construction_Actions.md#flavor_arm-1-3-fd199c)：知识的遗失；destroy_building；[in_game/events/DHE/flavor_arm.txt:3](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_arm.txt:3>)。
- `flavor_arm.2`：塔泰夫大学；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_arm.txt:60](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_arm.txt:60>)。
- [flavor_bav.27](ED_Vanilla_Wonder_Construction_Actions.md#flavor_bav-27-1081-75be1b)：[target_location.GetNameWithNoTooltip]大学奠基；construct_building；[in_game/events/DHE/flavor_bav.txt:1081](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_bav.txt:1081>)。
- [flavor_boh.20](ED_Vanilla_Wonder_Construction_Actions.md#flavor_boh-20-991-eb1e43)：布拉格大学；construct_building；[in_game/events/DHE/flavor_BOH.txt:991](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_BOH.txt:991>)。
- `flavor_boh.45`：发现伏尼契手稿；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_BOH.txt:2362](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_BOH.txt:2362>)。
- [flavor_brapru.11](ED_Vanilla_Wonder_Construction_Actions.md#flavor_brapru-11-576-4fbbec)：柯尼斯堡大学；construct_building；[in_game/events/DHE/flavor_brapru.txt:576](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_brapru.txt:576>)。
- `flavor_brapru.12`：《普鲁士星历表》；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_brapru.txt:638](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_brapru.txt:638>)。
- [flavor_brapru.18](ED_Vanilla_Wonder_Construction_Actions.md#flavor_brapru-18-1093-4fbbec)：法兰克福大学；construct_building；[in_game/events/DHE/flavor_brapru.txt:1093](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_brapru.txt:1093>)。
- `flavor_brapru.22`：[target_artist.GetNameWithNoTooltip]呼吁改革教育；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_brapru.txt:1357](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_brapru.txt:1357>)。
- `flavor_byz.27`：[target_character.GetDynasty.GetNameWithNoTooltip]文艺复兴的衰落；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_BYZ.txt:1959](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_BYZ.txt:1959>)。
- `flavor_cas.33`：建立孔普卢滕西斯大学；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_CAS.txt:1997](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_CAS.txt:1997>)。
- [flavor_cas.47](ED_Vanilla_Wonder_Construction_Actions.md#flavor_cas-47-2943-9abc78)：萨拉曼卡学派；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_CAS.txt:2943](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_CAS.txt:2943>)。
- `flavor_cas.129`：[target_character.GetNameWithNoTooltip]的法庭案件；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_CAS.txt:8019](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_CAS.txt:8019>)。
- `flavor_cas.130`：[target_character.GetNameWithNoTooltip]；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_CAS.txt:8086](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_CAS.txt:8086>)。
- `flavor_cas.150`：康普鲁顿合参本圣经；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_CAS.txt:9129](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_CAS.txt:9129>)。
- [flavor_dan.2](ED_Vanilla_Wonder_Construction_Actions.md#flavor_dan-2-146-6355b4)：[GetCountry('PAP').GetAdjectiveWithNoTooltip]御准高等教育；construct_building；[in_game/events/DHE/flavor_dan.txt:146](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_dan.txt:146>)。
- [flavor_dan.58](ED_Vanilla_Wonder_Construction_Actions.md#flavor_dan-58-3437-6355b4)：[ROOT.GetCountry.GetGovernment.GetAdjective\|U]美术学院；change_building_level_in_location；[in_game/events/DHE/flavor_dan.txt:3437](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_dan.txt:3437>)。
- [flavor_dlh.24](ED_Vanilla_Wonder_Construction_Actions.md#flavor_dlh-24-2353-b76ea9)：赞助[ShowReligionGroupNameWithNoTooltip('muslim')]学术；construct_building；[in_game/events/DHE/flavor_DLH.txt:2353](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_DLH.txt:2353>)。
- `flavor_eng.57`：[geoffrey_chaucer.GetNameWithNoTooltip]；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_ENG.txt:5468](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_ENG.txt:5468>)。
- `flavor_eng.75`：圣思嘉日暴动；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_ENG.txt:6987](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_ENG.txt:6987>)。
- `flavor_eng.157`：《地磁论》；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_ENG.txt:15043](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_ENG.txt:15043>)。
- `flavor_eng.174`：[christopher_wren.GetNameWithNoTooltip]；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_ENG.txt:16920](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_ENG.txt:16920>)。
- [flavor_fra.2013](ED_Vanilla_Wonder_Construction_Actions.md#flavor_fra-2013-6078-387b9f)：普瓦捷的大学；construct_building；[in_game/events/DHE/flavor_FRA.txt:6078](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_FRA.txt:6078>)。
- [flavor_gen.31](ED_Vanilla_Wonder_Construction_Actions.md#flavor_gen-31-2020-55f1ae)：热那亚大学；change_building_level_in_location；[in_game/events/DHE/flavor_GEN.txt:2020](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_GEN.txt:2020>)。
- [flavor_hab.30](ED_Vanilla_Wonder_Construction_Actions.md#flavor_hab-30-1508-a07f59)：维恩大学；construct_building；[in_game/events/DHE/flavor_HAB.txt:1508](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_HAB.txt:1508>)。
- [flavor_hab.1301](ED_Vanilla_Wonder_Construction_Actions.md#flavor_hab-1301-6774-a07f59)：[target_character.GetNameWithNoTooltip]提议设立诗人与数学家学院；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_HAB.txt:6774](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_HAB.txt:6774>)。
- `flavor_hab.1303`：才华横溢的[target_character.GetNameWithNoTooltip]；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_HAB.txt:6907](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_HAB.txt:6907>)。
- `flavor_hab.1500`：[target_artist.GetNameWithNoTooltip]；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_HAB.txt:7319](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_HAB.txt:7319>)。
- [flavor_hol.1](ED_Vanilla_Wonder_Construction_Actions.md#flavor_hol-1-4-5d5ce3)：[target_location.GetNameWithNoTooltip]大学；construct_building；[in_game/events/DHE/flavor_hol.txt:4](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_hol.txt:4>)。
- `flavor_hol.24`：[target_character.GetNameWithNoTooltip]；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_hol.txt:1134](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_hol.txt:1134>)。
- `flavor_hol.25`：[target_character.GetNameWithNoTooltip]；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_hol.txt:1208](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_hol.txt:1208>)。
- [flavor_hun.120](ED_Vanilla_Wonder_Construction_Actions.md#flavor_hun-120-156-0c02c5)：伊斯特罗波利坦学院；change_building_level_in_location；[in_game/events/DHE/flavor_HUN.txt:156](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_HUN.txt:156>)。
- [flavor_hun.400](ED_Vanilla_Wonder_Construction_Actions.md#flavor_hun-400-1835-0c02c5)：[location_scope.GetNameWithNoTooltip]大学；change_building_level_in_location；[in_game/events/DHE/flavor_HUN.txt:1835](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_HUN.txt:1835>)。
- [flavor_kie.1](ED_Vanilla_Wonder_Construction_Actions.md#flavor_kie-1-3-98122e)：基辅文化学院；construct_building；[in_game/events/DHE/flavor_kie.txt:3](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_kie.txt:3>)。
- [flavor_kor.31](ED_Vanilla_Wonder_Construction_Actions.md#flavor_kor-31-2125-7487ad)：成均馆；construct_building；[in_game/events/DHE/flavor_KOR.txt:2125](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_KOR.txt:2125>)。
- [flavor_mam.41](ED_Vanilla_Wonder_Construction_Actions.md#flavor_mam-41-2315-3a1e35)：爱资哈尔大学；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_MAM.txt:2315](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_MAM.txt:2315>)。
- [flavor_mei.160](ED_Vanilla_Wonder_Construction_Actions.md#flavor_mei-160-1302-53561d)：建立琉科雷亚大学；construct_building；[in_game/events/DHE/flavor_MEI.txt:1302](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_MEI.txt:1302>)。
- [flavor_mei.170](ED_Vanilla_Wonder_Construction_Actions.md#flavor_mei-170-1371-53561d)：弗赖贝格大学；construct_building；[in_game/events/DHE/flavor_MEI.txt:1371](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_MEI.txt:1371>)。
- `flavor_mlo.22`：[target_location.GetNameWithNoTooltip]大学；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_mlo.txt:1141](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_mlo.txt:1141>)。
- `flavor_mos.101`：异彩纷呈的大使团；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_MOS.txt:10158](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_MOS.txt:10158>)。
- `flavor_mos.109`：黑人仆从；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_MOS.txt:11112](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_MOS.txt:11112>)。
- [flavor_pal.1](ED_Vanilla_Wonder_Construction_Actions.md#flavor_pal-1-4-5a12a5)：明智之选；construct_building；[in_game/events/DHE/flavor_pal.txt:4](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_pal.txt:4>)。
- [flavor_pis.1100](ED_Vanilla_Wonder_Construction_Actions.md#flavor_pis-1100-746-c47c2f)：《论至高的尊荣》；construct_building；[in_game/events/DHE/flavor_PIS.txt:746](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_PIS.txt:746>)。
- [flavor_pis.1101](ED_Vanilla_Wonder_Construction_Actions.md#flavor_pis-1101-832-c47c2f)：《论至高的尊荣》；construct_building；[in_game/events/DHE/flavor_PIS.txt:832](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_PIS.txt:832>)。
- `flavor_plc.7`：贵族学院；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_plc.txt:407](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_plc.txt:407>)。
- [flavor_pol.4](ED_Vanilla_Wonder_Construction_Actions.md#flavor_pol-4-286-779f20)：维尔纽斯大学；construct_building；[in_game/events/DHE/flavor_pol.txt:286](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_pol.txt:286>)。
- [flavor_pol.25](ED_Vanilla_Wonder_Construction_Actions.md#flavor_pol-25-1735-779f20)：[target_location.GetNameWithNoTooltip]大学；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_pol.txt:1735](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_pol.txt:1735>)。
- `flavor_pol.28`：翻修[target_location.GetNameWithNoTooltip]大学；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_pol.txt:1907](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_pol.txt:1907>)。
- [flavor_pol.1101](ED_Vanilla_Wonder_Construction_Actions.md#flavor_pol-1101-4192-779f20)：扎莫伊斯基学院；construct_building；[in_game/events/DHE/flavor_pol.txt:4192](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_pol.txt:4192>)。
- `flavor_por.34`：迁移[current_location.GetNameWithNoTooltip]的大学；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_por.txt:2746](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_por.txt:2746>)。
- [flavor_rus.34](ED_Vanilla_Wonder_Construction_Actions.md#flavor_rus-34-2631-201f60)：[mikhail_lomonosov.GetNameWithNoTooltip]；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_RUS.txt:2631](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_RUS.txt:2631>)。
- [flavor_rus.46](ED_Vanilla_Wonder_Construction_Actions.md#flavor_rus-46-3616-201f60)：莫斯科公报的意识形态编辑；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_RUS.txt:3616](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_RUS.txt:3616>)。
- `flavor_rus.47`：[mikhail_speransky.GetNameWithNoTooltip]；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_RUS.txt:3704](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_RUS.txt:3704>)。
- `flavor_rus.51`：慷慨的赞助者；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_RUS.txt:4134](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_RUS.txt:4134>)。
- `flavor_rus.52`：皇家学会院士；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_RUS.txt:4269](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_RUS.txt:4269>)。
- `flavor_rus.61`：[alexander_radishchev.GetNameWithNoTooltip]的批评；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_RUS.txt:5172](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_RUS.txt:5172>)。
- `flavor_rus.74`：[nikolay_novikov.GetNameWithNoTooltip]的令人不快的真相；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_RUS.txt:6321](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_RUS.txt:6321>)。
- [flavor_sco.204](ED_Vanilla_Wonder_Construction_Actions.md#flavor_sco-204-2500-b81a33)：成立阿伯丁大学；construct_building；[in_game/events/DHE/flavor_SCO.txt:2500](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_SCO.txt:2500>)。
- [flavor_swe.50](ED_Vanilla_Wonder_Construction_Actions.md#flavor_swe-50-2503-211578)：[ShowLocationNameNoTooltip('uppsala')]大学；construct_building；[in_game/events/DHE/flavor_SWE.txt:2503](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_SWE.txt:2503>)。
- `flavor_teu.17`：[target_character.GetNameWithNoTooltip]；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_teu.txt:1053](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_teu.txt:1053>)。
- [flavor_tim.3](ED_Vanilla_Wonder_Construction_Actions.md#flavor_tim-3-98-272e59)：[target_heir.GetNameWithNoTooltip]的天文台；construct_building；[in_game/events/DHE/flavor_tim.txt:98](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_tim.txt:98>)。
- `flavor_ven.38`：洛雷丹学院；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_VEN.txt:1785](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_VEN.txt:1785>)。
- `flavor_ven.87`：逆境中的学者；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_VEN.txt:4463](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_VEN.txt:4463>)。
- `flavor_ven.92`：帕多瓦植物园；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_VEN.txt:4853](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_VEN.txt:4853>)。
- `building_1_old_university_trigger`：building_1_old_university_trigger；门槛/关联引用；需看上下文；[in_game/events/economy/building_events.txt:5](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/economy/building_events.txt:5>)。
- `building_1_new_university_trigger`：building_1_new_university_trigger；门槛/关联引用；需看上下文；[in_game/events/economy/building_events.txt:13](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/economy/building_events.txt:13>)。
- [building.1](ED_Vanilla_Wonder_Construction_Actions.md#building-1-29-a00f23)：[new_university.GetNameWithNoTooltip]大学；construct_building；[in_game/events/economy/building_events.txt:29](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/economy/building_events.txt:29>)。
- `building_2_university_trigger`：building_2_university_trigger；门槛/关联引用；需看上下文；[in_game/events/economy/building_events.txt:107](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/economy/building_events.txt:107>)。
- `building.2`：城校不和；门槛/关联引用；需看上下文；[in_game/events/economy/building_events.txt:111](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/economy/building_events.txt:111>)。
- `grand_tour_events.28`：一个学习机会；门槛/关联引用；需看上下文；[in_game/events/expeditions/grand_tour_events.txt:4427](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/expeditions/grand_tour_events.txt:4427>)。
- `latinization_vs_hellenization.5`：[target_location.GetNameWithNoTooltip]的课程之争；门槛/关联引用；需看上下文；[in_game/events/government/D008_latinization_vs_hellenization.txt:527](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/government/D008_latinization_vs_hellenization.txt:527>)。
- `parliaments.5`：[target_location.GetNameWithNoTooltip]赢得辩论；门槛/关联引用；需看上下文；[in_game/events/government/parliaments.txt:299](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/government/parliaments.txt:299>)。
- `parliaments.18`：[target_location.GetNameWithNoTooltip]的期望被满足；门槛/关联引用；需看上下文；[in_game/events/government/parliaments.txt:1049](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/government/parliaments.txt:1049>)。
- `imperial_examination_events.7`：人中翘楚；门槛/关联引用；需看上下文；[in_game/events/imperial_examination_events.txt:608](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/imperial_examination_events.txt:608>)。
- `innovativeness_events.7`：[university_province.GetNameWithNoTooltip]大学；门槛/关联引用；需看上下文；[in_game/events/innovativeness_events.txt:125](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/innovativeness_events.txt:125>)。
- `generic_mission_events.18`：[target_location.GetNameWithNoTooltip]的学者们；门槛/关联引用；需看上下文；[in_game/events/missionevents/generic_mission_events.txt:1312](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/missionevents/generic_mission_events.txt:1312>)。
- [church_aspects.7](ED_Vanilla_Wonder_Construction_Actions.md#church_aspects-7-234-3a383e)：[ROOT.GetCountry.GetGovernment.GetEstateNameWithNoTooltip('burghers_estate')]用他们所得进行投资；construct_building；[in_game/events/religion/church_aspects.txt:234](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/religion/church_aspects.txt:234>)。
- `hellenism_religion.3`：[target_location.GetNameWithNoTooltip]的哲学之翼；门槛/关联引用；需看上下文；[in_game/events/religion/hellenism_religion.txt:392](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/religion/hellenism_religion.txt:392>)。
- [orthodox_flavor.101](ED_Vanilla_Wonder_Construction_Actions.md#orthodox_flavor-101-503-820dca)：牧首巡行团抵达；construct_building；[in_game/events/religion/orthodox_flavor.txt:503](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/religion/orthodox_flavor.txt:503>)。
- `black_death.103`：从瘟疫中学习；门槛/关联引用；需看上下文；[in_game/events/situations/black_death.txt:227](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/situations/black_death.txt:227>)。
- `reformation.14`：大学中的异端讲师；门槛/关联引用；需看上下文；[in_game/events/situations/reformation.txt:889](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/situations/reformation.txt:889>)。

1337 开局实例：`bologna`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1632](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1632>)；`paris`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1633](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1633>)；`oxford`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1634](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1634>)；`vicenza`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1635](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1635>)；`cambridge`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1636](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1636>)；`salamanca`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1637](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1637>)；`padova`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1638](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1638>)；`naples`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1639](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1639>)；`toulouse`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1640](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1640>)；`orleans`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1641](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1641>)；`siena`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1642](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1642>)；`valladolid`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1643](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1643>)；`montpellier`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1644](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1644>)；`macerata`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1645](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1645>)；`coimbra`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1646](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1646>)；`alcala_de_henares`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1647](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1647>)；`lleida`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1648](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1648>)；`rome`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1649](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1649>)；`perugia`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1650](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1650>)；`dublin`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1651](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1651>)；`florence`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1652](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1652>)；`constantinople`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:1653](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:1653>)；`gladzor`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3842](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3842>)。

### urban_parliament_seat — 城镇议席

原版定义：[in_game/common/building_types/event_only_buildings.txt:945](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/event_only_buildings.txt:945>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `country_potential = { always = no }`
- `allow = { always = no }`
- `remove_if = { location = { OR = { NOT = { integration_level = core } owner = { has_parliament = no } owner = { modifier:has_a_parliamentary_system = no } } } }`
- `build_time = generic_event_building`

行为或条件引用：

- [disempower_the_parliament_decision](ED_Vanilla_Wonder_Construction_Actions.md#disempower_the_parliament_decision-560-57c555)：挑战议会权利；destroy_building；[in_game/common/decisions/generic_age_decisions.txt:560](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/decisions/generic_age_decisions.txt:560>)。
- [parliaments.1](ED_Vanilla_Wonder_Construction_Actions.md#parliaments-1-15-1694ec)：[target_city.GetRank.GetNameWithNoTooltip]要求[ROOT.GetCountry.GetGovernment.GetParliament.GetName]席位；change_building_level_in_location；[in_game/events/government/parliaments.txt:15](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/government/parliaments.txt:15>)。
- [parliaments.2](ED_Vanilla_Wonder_Construction_Actions.md#parliaments-2-94-1694ec)：腐败选区；change_building_level_in_location；[in_game/events/government/parliaments.txt:94](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/government/parliaments.txt:94>)。
- [parliaments.24](ED_Vanilla_Wonder_Construction_Actions.md#parliaments-24-1412-1694ec)：财政援助；change_building_level_in_location；[in_game/events/government/parliaments.txt:1412](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/government/parliaments.txt:1412>)。

### usa_academy_of_arts_and_sciences — 美国文理科学院

原版定义：[in_game/common/building_types/event_only_buildings.txt:3773](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/event_only_buildings.txt:3773>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `country_potential = { always = no }`
- `allow = { custom_tooltip = { text = usa_academy_of_arts_and_sciences_why always = no } }`
- `build_time = cultural_building_time`

行为或条件引用：

- [flavor_usa.8](ED_Vanilla_Wonder_Construction_Actions.md#flavor_usa-8-377-224cdd)：美国文理科学院；construct_building；[in_game/events/DHE/flavor_usa.txt:377](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_usa.txt:377>)。

### usa_national_bank — 美利坚第一银行

原版定义：[in_game/common/building_types/event_only_buildings.txt:3883](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/event_only_buildings.txt:3883>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `country_potential = { always = no }`
- `allow = { custom_tooltip = { text = usa_national_bank_why always = no } }`
- `build_time = generic_town_build_time`

行为或条件引用：

- [flavor_usa.14](ED_Vanilla_Wonder_Construction_Actions.md#flavor_usa-14-778-224cdd)：美利坚第一银行；construct_building；[in_game/events/DHE/flavor_usa.txt:778](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_usa.txt:778>)。

### usa_national_mint — 美国铸币局

原版定义：[in_game/common/building_types/event_only_buildings.txt:3930](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/event_only_buildings.txt:3930>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `country_potential = { always = no }`
- `allow = { custom_tooltip = { text = usa_national_mint_why always = no } }`
- `build_time = generic_town_build_time`

行为或条件引用：

- [flavor_usa.16](ED_Vanilla_Wonder_Construction_Actions.md#flavor_usa-16-883-224cdd)：美国铸币局；construct_building；[in_game/events/DHE/flavor_usa.txt:883](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_usa.txt:883>)。

### usa_philosophical_society — 美国哲学学会

原版定义：[in_game/common/building_types/event_only_buildings.txt:3827](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/event_only_buildings.txt:3827>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `country_potential = { always = no }`
- `allow = { custom_tooltip = { text = usa_philosophical_society_why always = no } }`
- `build_time = cultural_building_time`

行为或条件引用：

- [flavor_usa.11](ED_Vanilla_Wonder_Construction_Actions.md#flavor_usa-11-552-224cdd)：美国哲学学会；construct_building；[in_game/events/DHE/flavor_usa.txt:552](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_usa.txt:552>)。

### venetian_arsenal — 威尼斯军械库

原版定义：[in_game/common/building_types/unique_buildings.txt:272](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:272>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `location_potential = { counts_as_capital = yes is_port = yes }`
- `allow = { is_capital = yes country_has_no_other_copy_of_building = { type = venetian_arsenal } }`
- `country_potential = { has_advance = ven_stato_da_mar }`
- `build_time = huge_port_building_time`

行为或条件引用：

- [ven_stato_da_mar](ED_Vanilla_Wonder_Construction_Actions.md#ven_stato_da_mar-22-ba3150)：海上领土；unlock_building；[in_game/common/advances/culture_venetian.txt:22](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/advances/culture_venetian.txt:22>)。
- `flavor_ven.28`：威尼斯军械库；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_VEN.txt:1309](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_VEN.txt:1309>)。
- `grand_tour_events.2`：[target_location.GetNameWithNoTooltip]，最尊贵共和国；门槛/关联引用；需看上下文；[in_game/events/expeditions/grand_tour_events.txt:56](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/expeditions/grand_tour_events.txt:56>)。

1337 开局实例：`venice`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2072](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2072>)。

### venetian_palaces — 威尼斯宫殿

原版定义：[in_game/common/building_types/unique_buildings.txt:3206](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:3206>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = venetian_palaces_max_level`
- `location_potential = { counts_as_capital = yes }`
- `allow = { is_capital = yes country_has_no_other_copy_of_building = { type = venetian_palaces } }`
- `build_time = cultural_building_time`

行为或条件引用：

- [ven_gothic_architecture](ED_Vanilla_Wonder_Construction_Actions.md#ven_gothic_architecture-86-ba3150)：哥特式建筑；unlock_building；[in_game/common/advances/culture_venetian.txt:86](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/advances/culture_venetian.txt:86>)。

### venetian_quarter — 威尼斯特区

原版定义：[in_game/common/building_types/unique_buildings.txt:3250](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:3250>)。

- `is_special = yes`
- `is_foreign = yes`
- `max_levels = italian_merchant_quarters_max_level`
- `country_potential = { tag = VEN }`
- `location_potential = { this = location:constantinople }`
- `allow = { within_naval_range_of = scope:actor }`
- `remove_if = { owner = { NOT = { tag = VEN } } }`
- `build_time = trade_post_build_time`

行为或条件引用：

- [flavor_byz.54](ED_Vanilla_Wonder_Construction_Actions.md#flavor_byz-54-4697-64397c)：处理[ShowCultureGroupNameWithNoTooltip('italian_group')]商人；destroy_building；[in_game/events/DHE/flavor_BYZ.txt:4697](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_BYZ.txt:4697>)。
- [flavor_byz.1301](ED_Vanilla_Wonder_Construction_Actions.md#flavor_byz-1301-6618-64397c)：重建[target_location.GetNameWithNoTooltip]；change_building_level_in_location；[in_game/events/DHE/flavor_BYZ.txt:6618](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_BYZ.txt:6618>)。
- [flavor_tur.6](ED_Vanilla_Wonder_Construction_Actions.md#flavor_tur-6-258-bf9554)：关于君士坦丁堡商人的问题；destroy_building；[in_game/events/DHE/flavor_TUR.txt:258](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_TUR.txt:258>)。

1337 开局实例：`constantinople`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3623](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3623>)。

### venkateswara_temple — 文卡特斯瓦拉神庙

原版定义：[in_game/common/building_types/event_only_buildings.txt:2299](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/event_only_buildings.txt:2299>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 7`
- `build_time = large_religious_building_time`
- `country_potential = { always = no }`
- `allow = { always = no }`
- `remove_if = { location = { NOT = { owner = { religion ?= religion:hindu } } } }`

行为或条件引用：

- [flavor_vij.30](ED_Vanilla_Wonder_Construction_Actions.md#flavor_vij-30-1780-2f8e63)：蒂鲁帕蒂‑蒂鲁马拉寺庙群；construct_building；[in_game/events/DHE/flavor_vij.txt:1780](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_vij.txt:1780>)。

### versailles — 凡尔赛宫

原版定义：[in_game/common/building_types/event_only_buildings.txt:486](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/event_only_buildings.txt:486>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `build_time = cultural_building_time`
- `country_potential = { always = no }`
- `allow = { always = no }`
- `custom_tags = { unique_palace }`

行为或条件引用：

- `fra_versailles_residence_decision`：[ROOT.GetCountry.GetGovernment.GetEstateNameWithNoTooltip('nobles_estate')]与凡尔赛宫；门槛/关联引用；需看上下文；[in_game/common/decisions/flavor_decisions_fra.txt:564](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/decisions/flavor_decisions_fra.txt:564>)。
- `fra_versailles_permanent_decision`：为[ROOT.GetCountry.GetGovernment.GetEstateNameWithNoTooltip('nobles_estate')]设立永久驻地；门槛/关联引用；需看上下文；[in_game/common/decisions/flavor_decisions_fra.txt:651](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/decisions/flavor_decisions_fra.txt:651>)。
- [flavor_fra.10](ED_Vanilla_Wonder_Construction_Actions.md#flavor_fra-10-521-387b9f)：建造凡尔赛宫；construct_building；[in_game/events/DHE/flavor_FRA.txt:521](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_FRA.txt:521>)。
- `flavor_fra.426`：赞助[ROOT.GetCountry.GetGovernment.GetCourtTitle]官员；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_FRA.txt:12973](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_FRA.txt:12973>)。
- `flavor_fra.428`：皇家舞蹈学院；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_FRA.txt:13114](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_FRA.txt:13114>)。

### village_granary — 村镇粮仓

原版定义：[in_game/common/building_types/rural_buildings.txt:774](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/rural_buildings.txt:774>)。

- `is_foreign = no`
- `max_levels = 1`
- `build_time = rural_build_time`

未在本次行为定义中发现显式同名引用；仍可能由建筑自身条件、科技/改革解锁或引擎常规建设入口提供。

### wali_songo_shrine — 吾里圣陵

原版定义：[in_game/common/building_types/unique_buildings.txt:5413](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:5413>)。

- `is_special = yes`
- `max_levels = 1`
- `country_potential = { always = no }`
- `allow = { always = no }`
- `build_time = religious_building_time`

行为或条件引用：

- [flavor_maj.18](ED_Vanilla_Wonder_Construction_Actions.md#flavor_maj-18-1143-ceab17)：吾里之死；construct_building；[in_game/events/DHE/flavor_maj.txt:1143](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_maj.txt:1143>)。

### walls_of_benin — $benin$墙

原版定义：[in_game/common/building_types/unique_buildings.txt:5072](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:5072>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `build_time = huge_unique_build_time`
- `location_potential = { this = location:benin }`
- `country_potential = { owns = location:benin }`

未在本次行为定义中发现显式同名引用；仍可能由建筑自身条件、科技/改革解锁或引擎常规建设入口提供。

### walls_of_lucca — $lucca$城墙

原版定义：[in_game/common/building_types/event_only_buildings.txt:4365](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/event_only_buildings.txt:4365>)。

- `is_foreign = no`
- `max_levels = 1`
- `build_time = huge_unique_build_time`
- `country_potential = { always = no }`
- `allow = { always = no }`

行为或条件引用：

- [flavor_luc.5](ED_Vanilla_Wonder_Construction_Actions.md#flavor_luc-5-231-b9dd70)：$lucca$城墙；construct_building；[in_game/events/DHE/flavor_LUC.txt:231](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_LUC.txt:231>)。

### walls_of_ston — 斯通城墙

原版定义：[in_game/common/building_types/event_only_buildings.txt:2383](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/event_only_buildings.txt:2383>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `build_time = small_fort_building`
- `country_potential = { has_variable = has_unlocked_walls_of_ston }`
- `location_potential = { this = location:dubrovnik }`

行为或条件引用：

- [ven_walls_of_ston_decision](ED_Vanilla_Wonder_Construction_Actions.md#ven_walls_of_ston_decision-1338-a14531)：加强杜布罗夫尼克的防御；construct_building；[in_game/common/decisions/flavor_decisions_various.txt:1338](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/decisions/flavor_decisions_various.txt:1338>)。

### warrior_lodge — 战帮营帐

原版定义：[in_game/common/building_types/unique_buildings.txt:1219](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:1219>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `build_time = medium_soldier_building`
- `country_potential = { OR = { government_type ?= government_type:tribe government_type ?= government_type:monarchy } NOT = { is_capital_mesoamerica = yes } NOT = { is_capital_in_south_america_or_carribean = yes } capital ?= { continent = continent:america } }`

行为或条件引用：

- [north_american_warrior_societies](ED_Vanilla_Wonder_Construction_Actions.md#north_american_warrior_societies-178-fc293c)：战士社团；unlock_building；[in_game/common/advances/region_north_america.txt:178](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/advances/region_north_america.txt:178>)。

### warrior_temple — 勇士神庙

原版定义：[in_game/common/building_types/manpower_buildings.txt:44](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/manpower_buildings.txt:44>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `build_time = medium_soldier_building`
- `country_potential = { religion ?= religion:nahuatl }`

未在本次行为定义中发现显式同名引用；仍可能由建筑自身条件、科技/改革解锁或引擎常规建设入口提供。

1337 开局实例：`tenochtitlan`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2517](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2517>)。

### wat_chaiwatthanaram_temple_building — 柴瓦塔那兰寺

原版定义：[in_game/common/building_types/event_only_buildings.txt:2675](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/event_only_buildings.txt:2675>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `country_potential = { always = no }`
- `allow = { always = no }`
- `build_time = large_religious_building_time`
- `remove_if = { location = { owner = { NOR = { religion ?= religion:theravada religion ?= religion:mahayana religion ?= religion:tibetan_buddhism } } } }`

行为或条件引用：

- [flavor_ayu.6](ED_Vanilla_Wonder_Construction_Actions.md#flavor_ayu-6-362-62f2b4)：柴瓦塔那兰寺；construct_building；[in_game/events/DHE/flavor_ayu.txt:362](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_ayu.txt:362>)。

### west_friesland_admiralty — 西弗里斯兰海军部

原版定义：[in_game/common/building_types/event_only_buildings.txt:1906](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/event_only_buildings.txt:1906>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `build_time = large_port_building_time`
- `country_potential = { always = no }`
- `location_potential = { this = location:hoorn is_capital = no }`

行为或条件引用：

- [ned_unified_dutch_admiralties_decision](ED_Vanilla_Wonder_Construction_Actions.md#ned_unified_dutch_admiralties_decision-2096-a14531)：建立五大海军部；construct_building；[in_game/common/decisions/flavor_decisions_various.txt:2096](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/decisions/flavor_decisions_various.txt:2096>)。

### wisselbank — 阿姆斯特丹汇兑银行

原版定义：[in_game/common/building_types/event_only_buildings.txt:1176](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/event_only_buildings.txt:1176>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `build_time = generic_town_build_time`
- `country_potential = { always = no }`
- `allow = { always = no }`

行为或条件引用：

- [flavor_hol.13](ED_Vanilla_Wonder_Construction_Actions.md#flavor_hol-13-631-5d5ce3)：阿姆斯特丹银行与国际资本市场；destroy_building；[in_game/events/DHE/flavor_hol.txt:631](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_hol.txt:631>)。
- `flavor_hol.17`：阿姆斯特丹证券交易所的创立；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_hol.txt:817](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_hol.txt:817>)。
- [flavor_hol.28](ED_Vanilla_Wonder_Construction_Actions.md#flavor_hol-28-1361-5d5ce3)：阿姆斯特丹汇兑银行；construct_building；[in_game/events/DHE/flavor_hol.txt:1361](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_hol.txt:1361>)。

### woodhenge_of_cahokia — 卡霍基亚木环阵

原版定义：[in_game/common/building_types/event_only_buildings.txt:4219](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/event_only_buildings.txt:4219>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `country_potential = { always = no }`
- `allow = { custom_tooltip = { text = cahokia_woodhenge_why always = no } }`
- `build_time = cultural_building_time`

行为或条件引用：

- [flavor_chk.3](ED_Vanilla_Wonder_Construction_Actions.md#flavor_chk-3-116-a30f87)：扩建修复后的木环阵；construct_building；[in_game/events/DHE/flavor_CHK.txt:116](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_CHK.txt:116>)。
- `flavor_chk.6`：[ROOT.GetCountry.GetAdjectiveWithNoTooltip]精英阶层的复兴；门槛/关联引用；需看上下文；[in_game/events/DHE/flavor_CHK.txt:286](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_CHK.txt:286>)。

### yakata — 居馆

原版定义：[in_game/common/building_types/unique_buildings.txt:2681](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:2681>)。

- `is_special = yes`
- `is_foreign = yes`
- `max_levels = 1`
- `location_potential = { dominant_culture = { has_culture_group = culture_group:japanese_group } }`
- `country_potential = { has_reform = government_reform:japanese_clan }`
- `build_time = soldier_building`
- `allow = { dominant_culture = { has_culture_group = culture_group:japanese_group } any_foreign_building_countries_in_location = { this = scope:actor } }`

行为或条件引用：

- [claim_shugo_office](ED_Vanilla_Wonder_Construction_Actions.md#claim_shugo_office-251-1388a6)：宣称守护之职；门槛/关联引用；需看上下文；[in_game/common/generic_actions/japanese_shogunate.txt:251](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/generic_actions/japanese_shogunate.txt:251>)。
- [peace_expand_clan_influence](ED_Vanilla_Wonder_Construction_Actions.md#peace_expand_clan_influence-1-19f6b9)：扩张大名影响力；construct_building；[in_game/common/peace_treaties/expand_clan_influence.txt:1](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/peace_treaties/expand_clan_influence.txt:1>)。

1337 开局实例：`saba`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2697](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2697>)；`ashida`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2701](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2701>)；`joutou`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2705](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2705>)；`tsuga`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2709](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2709>)；`kurita`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2713](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2713>)；`miyagi`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2722](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2722>)；`abe`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2735](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2735>)；`iga`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2741](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2741>)；`takaichi`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2747](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2747>)；`nukanobu`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2760](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2760>)；`taki`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2771](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2771>)；`akita`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2790](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2790>)；`inaka`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2800](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2800>)；`nishiokitama`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2804](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2804>)；`date_loc`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2810](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2810>)；`shimohei`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2817](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2817>)；`kamihei`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2821](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2821>)；`yamamoto`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2827](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2827>)；`waga`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2833](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2833>)；`hienuki`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2837](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2837>)；`tome`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2841](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2841>)；`chiba`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2849](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2849>)；`shiwa`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2865](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2865>)；`kawabe`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2871](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2871>)；`murayama`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2877](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2877>)；`tagawa`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2881](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2881>)；`namekata`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2885](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2885>)；`minamiaizu`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2895](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2895>)；`tachibana`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2901](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2901>)；`tamura`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2907](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2907>)；`yama_jap`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2911](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2911>)；`shirakawa`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2915](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2915>)；`kitaaizu`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2919](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2919>)；`niihari`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2925](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2925>)；`kuji_kanto`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2929](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2929>)；`tsukuba`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2935](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2935>)；`naka`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2939](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2939>)；`kashima`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2943](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2943>)；`haga`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2947](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2947>)；`kawachi`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2951](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2951>)；`nasu`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2955](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2955>)；`seta`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2959](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2959>)；`nitta`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2963](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2963>)；`hiki`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2972](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2972>)；`adachi_kanto`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2981](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2981>)；`kamakura`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2985](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2985>)；`toshima_kanto`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2991](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2991>)；`kariwa`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2995](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2995>)；`takata`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3001](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3001>)；`kamo_mikawa`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3009](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3009>)；`kamo`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3019](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3019>)；`niikawa`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3025](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3025>)；`nomi`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3035](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3035>)；`koma_kai`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3041](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3041>)；`kamiina`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3051](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3051>)；`chiisagata`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3069](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3069>)；`saku`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3075](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3075>)；`ikaruga`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3081](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3081>)；`toki`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3093](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3093>)；`ena`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3106](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3106>)；`gujou`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3110](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3110>)；`yoshiki`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3114](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3114>)；`toyoda`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3118](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3118>)；`fuchi`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3125](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3125>)；`kuma`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3129](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3129>)；`shitara`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3135](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3135>)；`niwa`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3141](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3141>)；`tsuru`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3145](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3145>)；`mie`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3151](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3151>)；`gamou`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3155](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3155>)；`takashima`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3161](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3161>)；`nakata`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3167](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3167>)；`hekikai`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3184](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3184>)；`akou`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3194](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3194>)；`nishimuro`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3208](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3208>)；`kaisou`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3212](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3212>)；`takakusa`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3216](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3216>)；`kume_houki`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3220](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3220>)；`keta_tajima`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3226](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3226>)；`ou`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3233](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3233>)；`izumo`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3241](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3241>)；`nita`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3245](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3245>)；`iishi`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3249](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3249>)；`eso`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3253](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3253>)；`noto_jap`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3257](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3257>)；`yoshiki_suou`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3267](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3267>)；`tagata`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3274](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3274>)；`aita`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3282](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3282>)；`aichi`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3286](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3286>)；`kaya`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3294](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3294>)；`asakuchi`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3298](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3298>)；`aki`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3302](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3302>)；`toyota`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3306](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3306>)；`yamagata`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3310](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3310>)；`sera`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3316](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3316>)；`miyoshi`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3320](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3320>)；`tsuno`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3324](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3324>)；`abu`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3328](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3328>)；`asa`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3334](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3334>)；`mitoyo`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3352](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3352>)；`miki`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3357](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3357>)；`nii`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3361](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3361>)；`aki_shikoku`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3365](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3365>)；`takaoka`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3369](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3369>)；`usa`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3373](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3373>)；`ooita`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3377](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3377>)；`onga`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3396](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3396>)；`nakatsu`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3399](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3399>)；`asakura`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3411](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3411>)；`kishima`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3415](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3415>)；`higashimatsuura`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3419](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3419>)；`takaki`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3425](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3425>)；`aimi`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3429](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3429>)；`mii`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3435](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3435>)；`hita`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3441](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3441>)；`higashiusuki`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3447](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3447>)；`kimotsuki`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3455](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3455>)；`satsuma`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3464](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3464>)；`kuwabara`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3476](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3476>)；`hishikari`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3480](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3480>)；`souma`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3484](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3484>)；`aso`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3490](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3490>)；`yabu`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3496](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3496>)；`kitamogami`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3503](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3503>)；`minamiuonuma`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3507](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3507>)；`shioya`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3511](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3511>)；`mashita`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3517](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3517>)；`takaichi`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3521](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3521>)；`mino`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3526](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3526>)；`kita_shikoku`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3530](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3530>)；`iyo`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3534](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3534>)；`uwa`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3539](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3539>)；`ukena`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3543](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3543>)；`nishimatsuura`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3547](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3547>)；`koushi`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3551](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3551>)；`kagoshima`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3555](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3555>)；`kamiagata`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3559](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3559>)；`suwa`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3565](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3565>)；`nuka`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3570](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3570>)；`tosa`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3574](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3574>)；`ichishi`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3580](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3580>)；`nyuu`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3586](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3586>)。

### yamashiro — 山城

原版定义：[in_game/common/building_types/unique_buildings.txt:2588](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:2588>)。

- `is_special = yes`
- `is_foreign = yes`
- `max_levels = 1`
- `location_potential = { dominant_culture = { has_culture_group = culture_group:japanese_group } }`
- `country_potential = { OR = { AND = { has_reform = government_reform:japanese_imperial_family country_type = building } has_reform = government_reform:japanese_clan } }`
- `build_time = soldier_building`
- `allow = { dominant_culture = { has_culture_group = culture_group:japanese_group } trigger_if = { limit = { any_foreign_building_countries_in_location = { count > 0 } } OR = { any_foreign_building_countries_in_location = { OR = { this = scope:actor has_mutual_scripted_relation = { type = relation_type:alliance target = scope:actor } } } custom_tooltip = { text = we_are_shugo_tt AND = { NOR = { this = location:izumi this = location:iga this = location:awa this = location:oki this = location:awaji } province_definition = { any_location_in_province_definition = { any_foreign_buildings_in_location = { owner ?= scope:actor building_type = building_type:kokufu } } } } } } } }`

行为或条件引用：

- [claim_shugo_office](ED_Vanilla_Wonder_Construction_Actions.md#claim_shugo_office-251-1388a6)：宣称守护之职；门槛/关联引用；需看上下文；[in_game/common/generic_actions/japanese_shogunate.txt:251](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/generic_actions/japanese_shogunate.txt:251>)。
- [peace_expand_clan_influence](ED_Vanilla_Wonder_Construction_Actions.md#peace_expand_clan_influence-1-19f6b9)：扩张大名影响力；construct_building；[in_game/common/peace_treaties/expand_clan_influence.txt:1](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/peace_treaties/expand_clan_influence.txt:1>)。
- `turn_japanese_clan_into_normal_tag`：turn_japanese_clan_into_normal_tag；门槛/关联引用；需看上下文；[in_game/common/scripted_effects/country_effects.txt:754](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/scripted_effects/country_effects.txt:754>)。
- [turn_japanese_clan_into_building_based](ED_Vanilla_Wonder_Construction_Actions.md#turn_japanese_clan_into_building_based-817-d574b2)：turn_japanese_clan_into_building_based；change_building_level_in_location；[in_game/common/scripted_effects/country_effects.txt:817](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/scripted_effects/country_effects.txt:817>)。
- `culture_japan.1200`：[target_shogunate.GetLongNameWithNoTooltip]式徽；门槛/关联引用；需看上下文；[in_game/events/culture/culture_japan.txt:1736](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/culture/culture_japan.txt:1736>)。
- [culture_japan.1203](ED_Vanilla_Wonder_Construction_Actions.md#culture_japan-1203-1920-1a4074)：[target_clan.GetLongNameWithNoTooltip]为援助要求补偿；门槛/关联引用；需看上下文；[in_game/events/culture/culture_japan.txt:1920](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/culture/culture_japan.txt:1920>)。
- [culture_japan.1204](ED_Vanilla_Wonder_Construction_Actions.md#culture_japan-1204-1971-1a4074)：悬赏[target_location.GetNameWithNoTooltip]支配权；construct_building；[in_game/events/culture/culture_japan.txt:1971](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/culture/culture_japan.txt:1971>)。
- [culture_japan.1300](ED_Vanilla_Wonder_Construction_Actions.md#culture_japan-1300-2080-1a4074)：[target_shogunate.GetLongNameWithNoTooltip]式徽；门槛/关联引用；需看上下文；[in_game/events/culture/culture_japan.txt:2080](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/culture/culture_japan.txt:2080>)。
- [culture_japan.1301](ED_Vanilla_Wonder_Construction_Actions.md#culture_japan-1301-2152-1a4074)：[target_clan.GetNameWithNoTooltip]要求加封；construct_building；[in_game/events/culture/culture_japan.txt:2152](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/culture/culture_japan.txt:2152>)。
- [culture_japan.1303](ED_Vanilla_Wonder_Construction_Actions.md#culture_japan-1303-2234-1a4074)：悬赏[target_location.GetNameWithNoTooltip]支配权；construct_building；[in_game/events/culture/culture_japan.txt:2234](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/culture/culture_japan.txt:2234>)。

1337 开局实例：`yoshino`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2624](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2624>)；`saba`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2696](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2696>)；`ashida`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2700](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2700>)；`joutou`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2704](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2704>)；`tsuga`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2708](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2708>)；`kurita`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2712](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2712>)；`kamioono`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2716](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2716>)；`sawata`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2718](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2718>)；`miyagi`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2721](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2721>)；`awa`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2725](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2725>)；`kamiura`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2727](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2727>)；`onyuu`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2729](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2729>)；`nyuu`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2731](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2731>)；`abe`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2734](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2734>)；`tagata`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2737](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2737>)；`iga`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2740](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2740>)；`kuwada`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2743](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2743>)；`takaichi`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2746](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2746>)；`hoi`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2750](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2750>)；`tama`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2752](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2752>)；`ichihara`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2754](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2754>)；`higashikubiki`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2756](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2756>)；`nukanobu`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2759](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2759>)；`shimokita`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2765](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2765>)；`kamikita`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2767](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2767>)；`taki`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2770](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2770>)；`shima`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2778](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2778>)；`hiraka_aomori`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2780](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2780>)；`miyagi`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2782](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2782>)；`watarai`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2784](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2784>)；`ichishi`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2786](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2786>)；`akita`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2789](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2789>)；`hanawa`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2794](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2794>)；`inaka`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2799](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2799>)；`nishiokitama`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2803](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2803>)；`tama`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2806](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2806>)；`date_loc`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2809](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2809>)；`shinobu`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2813](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2813>)；`shimohei`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2816](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2816>)；`kamihei`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2820](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2820>)；`aki`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2823](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2823>)；`yamamoto`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2826](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2826>)；`iwate`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2829](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2829>)；`waga`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2832](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2832>)；`hienuki`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2836](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2836>)；`tome`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2840](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2840>)；`isawa`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2843](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2843>)；`oshika`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2845](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2845>)；`chiba`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2848](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2848>)；`katsushika`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2853](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2853>)；`iwai`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2855](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2855>)；`musa`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2857](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2857>)；`katori`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2859](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2859>)；`chiba`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2861](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2861>)；`shiwa`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2864](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2864>)；`kurokawa`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2867](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2867>)；`kawabe`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2870](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2870>)；`yuza`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2873](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2873>)；`murayama`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2876](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2876>)；`tagawa`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2880](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2880>)；`namekata`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2884](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2884>)；`uda_mutsu`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2887](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2887>)；`tsukuba`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2889](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2889>)；`souma`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2891](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2891>)；`minamiaizu`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2894](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2894>)；`tachibana`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2900](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2900>)；`iwase`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2903](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2903>)；`tamura`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2906](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2906>)；`yama_jap`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2910](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2910>)；`shirakawa`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2914](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2914>)；`kitaaizu`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2918](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2918>)；`kawanuma`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2921](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2921>)；`niihari`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2924](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2924>)；`kuji_kanto`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2928](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2928>)；`ibaraki`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2931](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2931>)；`tsukuba`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2934](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2934>)；`naka`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2938](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2938>)；`kashima`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2942](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2942>)；`haga`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2946](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2946>)；`kawachi`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2950](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2950>)；`nasu`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2954](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2954>)；`seta`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2958](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2958>)；`nitta`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2962](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2962>)；`ashigara`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2966](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2966>)；`nomi`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2968](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2968>)；`hiki`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2971](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2971>)；`kaisou`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2975](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2975>)；`fugeshi`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2977](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2977>)；`adachi_kanto`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2980](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2980>)；`aikou`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2984](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2984>)；`toshima_kanto`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2990](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2990>)；`kariwa`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2994](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2994>)；`nishikanbara`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:2997](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:2997>)；`takata`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3000](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3000>)；`kariwa`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3004](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3004>)；`kamo_mikawa`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3008](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3008>)；`nakajima`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3011](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3011>)；`nutari`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3013](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3013>)；`koshi`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3015](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3015>)；`kamo`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3018](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3018>)；`niikawa`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3024](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3024>)；`keta_tajima`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3027](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3027>)；`tonami`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3029](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3029>)；`nei`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3031](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3031>)；`nomi`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3034](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3034>)；`kaga`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3037](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3037>)；`koma_kai`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3040](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3040>)；`yatsushiro`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3045](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3045>)；`aki`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3047](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3047>)；`kamiina`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3050](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3050>)；`tsukama`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3055](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3055>)；`sarashina`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3057](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3057>)；`oochi`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3059](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3059>)；`mima`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3061](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3061>)；`awa_shikoku`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3063](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3063>)；`miyoshi_shikoku`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3065](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3065>)；`chiisagata`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3068](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3068>)；`azumi`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3071](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3071>)；`saku`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3074](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3074>)；`minochi`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3077](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3077>)；`ikaruga`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3080](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3080>)；`gunma`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3085](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3085>)；`kasa`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3087](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3087>)；`nishikubiki`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3089](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3089>)；`toki`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3092](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3092>)；`fuwa_mino`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3096](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3096>)；`katagata`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3098](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3098>)；`mugi`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3100](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3100>)；`ikeda`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3102](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3102>)；`ena`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3105](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3105>)；`gujou`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3109](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3109>)；`yoshiki`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3113](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3113>)；`toyoda`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3117](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3117>)；`ihara`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3121](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3121>)；`fuchi`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3124](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3124>)；`kuma`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3128](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3128>)；`kitou`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3131](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3131>)；`shitara`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3134](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3134>)；`houmi`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3137](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3137>)；`niwa`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3140](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3140>)；`tsuru`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3144](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3144>)；`mie`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3150](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3150>)；`gamou`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3154](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3154>)；`echi`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3157](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3157>)；`takashima`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3160](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3160>)；`awa_shikoku`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3164](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3164>)；`nakata`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3166](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3166>)；`naga`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3172](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3172>)；`awaji`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3174](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3174>)；`aya`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3176](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3176>)；`nagaoka`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3178](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3178>)；`kuse`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3180](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3180>)；`hekikai`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3183](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3183>)；`kasa`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3188](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3188>)；`saga`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3190](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3190>)；`akou`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3193](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3193>)；`shikama`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3198](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3198>)；`osaka`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3200](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3200>)；`akashi`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3202](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3202>)；`hikami`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3204](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3204>)；`nishimuro`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3207](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3207>)；`kaisou`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3211](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3211>)；`takakusa`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3215](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3215>)；`kume_houki`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3219](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3219>)；`kume_houki`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3223](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3223>)；`keta_tajima`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3225](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3225>)；`hino`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3229](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3229>)；`ou`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3232](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3232>)；`oki`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3235](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3235>)；`izumo`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3240](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3240>)；`nita`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3244](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3244>)；`iishi`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3248](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3248>)；`eso`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3252](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3252>)；`noto_jap`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3256](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3256>)；`imizu`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3259](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3259>)；`kanoashi`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3261](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3261>)；`yoshiki_suou`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3266](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3266>)；`nima`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3270](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3270>)；`tagata`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3273](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3273>)；`koyu`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3276](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3276>)；`wake`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3278](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3278>)；`aita`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3281](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3281>)；`aichi`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3285](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3285>)；`naka_iwami`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3288](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3288>)；`kaya`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3293](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3293>)；`asakuchi`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3297](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3297>)；`aki`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3301](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3301>)；`toyota`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3305](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3305>)；`yamagata`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3309](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3309>)；`sera`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3315](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3315>)；`miyoshi`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3319](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3319>)；`tsuno`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3323](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3323>)；`abu`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3327](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3327>)；`toyoura`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3331](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3331>)；`asa`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3333](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3333>)；`ochi`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3337](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3337>)；`mitoyo`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3351](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3351>)；`miki`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3356](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3356>)；`nii`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3360](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3360>)；`aki_shikoku`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3364](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3364>)；`takaoka`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3368](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3368>)；`usa`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3372](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3372>)；`ooita`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3376](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3376>)；`saga`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3382](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3382>)；`koyu`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3384](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3384>)；`kunisaki`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3390](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3390>)；`naoiri`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3392](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3392>)；`onga`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3395](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3395>)；`asakura`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3410](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3410>)；`kishima`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3414](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3414>)；`higashimatsuura`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3418](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3418>)；`takaki`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3424](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3424>)；`aimi`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3428](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3428>)；`yatsushiro_higo`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3432](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3432>)；`mike`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3437](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3437>)；`hita`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3440](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3440>)；`izumi_satsuma`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3443](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3443>)；`higashiusuki`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3446](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3446>)；`miyazaki`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3449](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3449>)；`naka_hyuuga`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3451](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3451>)；`kimotsuki`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3454](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3454>)；`kitamorokata`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3457](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3457>)；`minamimorokata`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3459](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3459>)；`soo`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3462](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3462>)；`ibusuki`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3469](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3469>)；`kagoshima`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3471](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3471>)；`kuwabara`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3475](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3475>)；`hishikari`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3479](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3479>)；`souma`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3483](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3483>)；`aso`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3489](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3489>)；`mashiki`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3492](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3492>)；`yabu`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3495](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3495>)；`sakai_echizen`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3499](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3499>)；`kitamogami`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3502](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3502>)；`minamiuonuma`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3506](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3506>)；`shioya`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3510](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3510>)；`mashita`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3516](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3516>)；`takaichi`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3520](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3520>)；`mino`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3525](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3525>)；`kita_shikoku`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3529](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3529>)；`iyo`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3533](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3533>)；`uwa`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3538](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3538>)；`ukena`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3542](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3542>)；`nishimatsuura`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3546](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3546>)；`koushi`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3550](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3550>)；`kagoshima`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3554](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3554>)；`kamiagata`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3558](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3558>)；`suwa`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3564](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3564>)；`nuka`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3569](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3569>)；`tosa`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3573](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3573>)；`suzuka`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3579](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3579>)；`nyuu`，level=`1`，[main_menu/setup/1337/07_cities_and_buildings.txt:3585](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/07_cities_and_buildings.txt:3585>)。

### zazzau_walls — $zazzau$城墙

原版定义：[in_game/common/building_types/unique_buildings.txt:5113](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:5113>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `build_time = small_fort_building`
- `country_potential = { always = no }`

行为或条件引用：

- [flavor_zzz.1](ED_Vanilla_Wonder_Construction_Actions.md#flavor_zzz-1-3-8d53e2)：[target_location.GetNameWithNoTooltip]墙；construct_building；[in_game/events/DHE/flavor_zzz.txt:3](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_zzz.txt:3>)。

### zeeland_admiralty — 泽兰海军部

原版定义：[in_game/common/building_types/event_only_buildings.txt:1986](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/event_only_buildings.txt:1986>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `build_time = large_port_building_time`
- `country_potential = { always = no }`
- `location_potential = { this = location:middelburg is_capital = no }`

行为或条件引用：

- [ned_unified_dutch_admiralties_decision](ED_Vanilla_Wonder_Construction_Actions.md#ned_unified_dutch_admiralties_decision-2096-a14531)：建立五大海军部；construct_building；[in_game/common/decisions/flavor_decisions_various.txt:2096](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/decisions/flavor_decisions_various.txt:2096>)。

### zhixian — 县衙

原版定义：[in_game/common/building_types/unique_buildings.txt:5453](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/unique_buildings.txt:5453>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `build_time = small_capital_build_time`
- `country_potential = { exists = international_organization:middle_kingdom is_leader_of_international_organization = international_organization:middle_kingdom }`
- `location_potential = { }`
- `remove_if = { owner = { NOT = { is_leader_of_international_organization = international_organization:middle_kingdom } } }`

未在本次行为定义中发现显式同名引用；仍可能由建筑自身条件、科技/改革解锁或引擎常规建设入口提供。

### zwinger — 茨温格宫

原版定义：[in_game/common/building_types/event_only_buildings.txt:772](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/building_types/event_only_buildings.txt:772>)。

- `is_special = yes`
- `is_foreign = no`
- `max_levels = 1`
- `location_potential = { counts_as_capital = yes }`
- `country_potential = { OR = { has_or_had_tag = MEI has_or_had_tag = SAX } }`
- `allow = { always = no }`
- `build_time = cultural_building_time`

行为或条件引用：

- [flavor_mei.110](ED_Vanilla_Wonder_Construction_Actions.md#flavor_mei-110-740-53561d)：茨温格宫；construct_building；[in_game/events/DHE/flavor_MEI.txt:740](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/events/DHE/flavor_MEI.txt:740>)。

## 建筑型艺术品的原生可用性

以下类型均在原版 `artist_work/00_default.txt` 中要求建筑师，且 `captured = no`。`temple_tower` 还检查所在地的 temple/cathedral。类型条件是另一个入口，不能只查历史事件。

### mansion

[in_game/common/artist_work/00_default.txt:179](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/artist_work/00_default.txt:179>)

```text
mansion = {
	captured = no
	allow = {
		artist_type = architect
	}
	woa_type_worth = -1
	woa_age_gold_per_year = 0
	woa_tradition_multiplier = 1.0
	woa_influence_multiplier = 0.3
	woa_age_tradition_per_year = 0
	woa_age_influence_per_year = 0
}
```

### monument

[in_game/common/artist_work/00_default.txt:192](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/artist_work/00_default.txt:192>)

```text
monument = {
	captured = no
	allow = {
		artist_type = architect
	}
	woa_type_worth = -1
	woa_age_gold_per_year = 0
	woa_tradition_multiplier = 2.5
	woa_influence_multiplier = 1.0
	woa_age_tradition_per_year = 0
	woa_age_influence_per_year = 0
}
```

### palace

[in_game/common/artist_work/00_default.txt:205](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/artist_work/00_default.txt:205>)

```text
palace = {
	captured = no
	allow = {
		artist_type = architect
	}
	woa_type_worth = -1
	woa_age_gold_per_year = 0
	woa_tradition_multiplier = 2.0
	woa_influence_multiplier = 0.8
	woa_age_tradition_per_year = 0
	woa_age_influence_per_year = 0
}
```

### temple_tower

[in_game/common/artist_work/00_default.txt:218](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/in_game/common/artist_work/00_default.txt:218>)

```text
temple_tower = {
	captured = no
	allow = {
		artist_type = architect
		location = {
			OR = {
				has_building_with_at_least_one_level = temple
				has_building_with_at_least_one_level = cathedral
			}
		}
	}
	woa_type_worth = -1
	woa_age_gold_per_year = 0
	woa_tradition_multiplier = 2.0
	woa_influence_multiplier = 0.5
	woa_age_tradition_per_year = 0
	woa_age_influence_per_year = 0
}
```

## 1337 已存在的建筑型艺术品

此处是初始化，不是游戏中施工。保留这些对象用于定位修复、替换、毁坏、转换等生命周期入口。

| 对象 key / 原版中文名 | 类型 | 地点 | 初始化证据 |
|---|---|---|---|
| `chiesa_san_gottardo_in_corte_tower` / 科尔特的圣高特赫教堂塔楼 | `temple_tower` | `milano` | [main_menu/setup/1337/11_art.txt:14](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/11_art.txt:14>) |
| `torrazzo_di_cremona` / 克雷莫纳的塔楼 | `temple_tower` | `cremona` | [main_menu/setup/1337/11_art.txt:15](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/11_art.txt:15>) |
| `lalibela_church_st_george_work_of_art` /  | `monument` | `lalibela` | [main_menu/setup/1337/11_art.txt:19](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/11_art.txt:19>) |
| `king_ezana_stele` / 埃扎纳王石柱 | `monument` | `axum` | [main_menu/setup/1337/11_art.txt:20](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/11_art.txt:20>) |
| `lanterna_di_genoa` / 热那亚灯塔 | `monument` | `genoa` | [main_menu/setup/1337/11_art.txt:22](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/11_art.txt:22>) |
| `palazzo_san_giorgio` / 圣乔治宫 | `palace` | `genoa` | [main_menu/setup/1337/11_art.txt:23](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/11_art.txt:23>) |
| `yaroslavs_court` / 雅罗斯拉夫宫 | `palace` | `novgorod` | [main_menu/setup/1337/11_art.txt:26](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/11_art.txt:26>) |
| `house_of_holy_wisdom` / 圣智大教堂 | `monument` | `novgorod` | [main_menu/setup/1337/11_art.txt:27](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/11_art.txt:27>) |
| `saint_george_in_yuriev` / 尤里耶夫的圣格奥尔吉修道院 | `monument` | `novgorod` | [main_menu/setup/1337/11_art.txt:30](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/11_art.txt:30>) |
| `palma_cathedral` / 帕尔马主教座堂 | `monument` | `palma` | [main_menu/setup/1337/11_art.txt:32](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/11_art.txt:32>) |
| `ripoll_abbey` / 里波尔修道院 | `monument` | `vic` | [main_menu/setup/1337/11_art.txt:35](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/11_art.txt:35>) |
| `montserrat_work_of_art` /  | `monument` | `barcelona` | [main_menu/setup/1337/11_art.txt:36](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/11_art.txt:36>) |
| `poblet_abbey` / 波夫莱特修道院 | `monument` | `tarragona` | [main_menu/setup/1337/11_art.txt:37](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/11_art.txt:37>) |
| `zaragoza_basilica_del_pilar_work_of_art` /  | `monument` | `zaragoza` | [main_menu/setup/1337/11_art.txt:38](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/11_art.txt:38>) |
| `aljaferia_palace` / 阿尔哈费里亚宫 | `palace` | `zaragoza` | [main_menu/setup/1337/11_art.txt:39](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/11_art.txt:39>) |
| `santa_maria_del_mar` / 海洋圣母教堂 | `monument` | `barcelona` | [main_menu/setup/1337/11_art.txt:41](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/11_art.txt:41>) |
| `djenne_mosque` / 杰内大清真寺 | `monument` | `djenne` | [main_menu/setup/1337/11_art.txt:49](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/11_art.txt:49>) |
| `sankore_madrasa` / 桑科雷大学 | `temple_tower` | `timbuktu` | [main_menu/setup/1337/11_art.txt:50](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/11_art.txt:50>) |
| `djinguereber_mosque` / 津加雷贝尔清真寺 | `monument` | `timbuktu` | [main_menu/setup/1337/11_art.txt:51](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/11_art.txt:51>) |
| `zica_studenica_monasteries` / 日查‑斯图代尼察修道院 | `monument` | `zica` | [main_menu/setup/1337/11_art.txt:59](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/11_art.txt:59>) |
| `basilica_of_the_assumption_virgin_mary` / 童贞荣福玛利亚升天宗座圣殿 | `monument` | `fehervar` | [main_menu/setup/1337/11_art.txt:62](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/11_art.txt:62>) |
| `collegiate_roncesvalles` / 龙塞斯瓦列斯王家协同教堂 | `monument` | `roncesvalles` | [main_menu/setup/1337/11_art.txt:70](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/11_art.txt:70>) |
| `la_oliva_abbey` / 拉奥利瓦圣母玛利亚修道院 | `monument` | `tudela` | [main_menu/setup/1337/11_art.txt:71](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/11_art.txt:71>) |
| `pohyonsa` / 普贤寺 | `monument` | `huicheon` | [main_menu/setup/1337/11_art.txt:82](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/11_art.txt:82>) |
| `saint_mark_basilica` / 圣马尔谷宗座圣殿 | `monument` | `venice` | [main_menu/setup/1337/11_art.txt:85](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/11_art.txt:85>) |
| `palais_des_papes` / 教宗宫 | `palace` | `avignon` | [main_menu/setup/1337/11_art.txt:89](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/11_art.txt:89>) |
| `convent_christ` / 基督修道院 | `monument` | `tomar` | [main_menu/setup/1337/11_art.txt:91](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/11_art.txt:91>) |
| `alcobaca_monastery` / 阿尔科巴萨修道院 | `monument` | `alcobaca` | [main_menu/setup/1337/11_art.txt:92](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/11_art.txt:92>) |
| `hagia_irene` / 圣伊里尼教堂 | `monument` | `constantinople` | [main_menu/setup/1337/11_art.txt:94](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/11_art.txt:94>) |
| `hagia_sophia` / 圣索菲亚大教堂 | `monument` | `constantinople` | [main_menu/setup/1337/11_art.txt:95](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/11_art.txt:95>) |
| `theodosian_walls` / 狄奥多西城墙 | `monument` | `constantinople` | [main_menu/setup/1337/11_art.txt:96](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/11_art.txt:96>) |
| `roskilde_cathedral` / 罗斯基勒主教座堂 | `monument` | `roskilde` | [main_menu/setup/1337/11_art.txt:111](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/11_art.txt:111>) |
| `tournai_cathedral` / 图尔奈主教座堂 | `monument` | `tournai` | [main_menu/setup/1337/11_art.txt:113](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/11_art.txt:113>) |
| `notre_dame_de_paris` / $ORIGIN$圣母院 | `monument` | `paris` | [main_menu/setup/1337/11_art.txt:114](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/11_art.txt:114>) |
| `sainte_chapelle` / 圣礼拜堂 | `monument` | `paris` | [main_menu/setup/1337/11_art.txt:115](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/11_art.txt:115>) |
| `vezelay_abbey` / 韦兹莱修道院 | `monument` | `avallon` | [main_menu/setup/1337/11_art.txt:116](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/11_art.txt:116>) |
| `mont_saint_michel` / 圣米歇尔山 | `monument` | `avranches` | [main_menu/setup/1337/11_art.txt:117](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/11_art.txt:117>) |
| `reims_cathedral` / 兰斯大教堂 | `monument` | `reims` | [main_menu/setup/1337/11_art.txt:118](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/11_art.txt:118>) |
| `cluny_abbey` / 克吕尼修道院 | `monument` | `macon` | [main_menu/setup/1337/11_art.txt:119](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/11_art.txt:119>) |
| `aachen_cathedral` / 亚琛大教堂 | `monument` | `aachen` | [main_menu/setup/1337/11_art.txt:121](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/11_art.txt:121>) |
| `gravensteen_castle` / 伯爵城堡 | `monument` | `ghent` | [main_menu/setup/1337/11_art.txt:123](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/11_art.txt:123>) |
| `belfry_bruges` / 布鲁日钟楼 | `monument` | `bruges` | [main_menu/setup/1337/11_art.txt:124](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/11_art.txt:124>) |
| `mosque_cordoba` / 科尔多瓦大清真寺教堂 | `monument` | `cordoba` | [main_menu/setup/1337/11_art.txt:131](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/11_art.txt:131>) |
| `giralda` / 吉拉达钟楼 | `temple_tower` | `sevilla` | [main_menu/setup/1337/11_art.txt:132](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/11_art.txt:132>) |
| `santiago_de_compostela_work_of_art` /  | `monument` | `santiago_compostela` | [main_menu/setup/1337/11_art.txt:137](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/11_art.txt:137>) |
| `alcazar_segovia` / 塞哥维亚城堡 | `palace` | `segovia` | [main_menu/setup/1337/11_art.txt:138](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/11_art.txt:138>) |
| `alhambra_palace` / 阿尔罕布拉 | `palace` | `granada` | [main_menu/setup/1337/11_art.txt:142](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/11_art.txt:142>) |
| `marienkapelle` / 玛利亚小教堂 | `monument` | `munich` | [main_menu/setup/1337/11_art.txt:144](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/11_art.txt:144>) |
| `sahib_ata_kulliyesi` / 萨希卜阿塔建筑群 | `monument` | `konya` | [main_menu/setup/1337/11_art.txt:151](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/11_art.txt:151>) |
| `gokmedrese` / 天蓝神学院 | `monument` | `sivas` | [main_menu/setup/1337/11_art.txt:153](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/11_art.txt:153>) |
| `ulu_beden` / 乌鲁‑贝登塔 | `temple_tower` | `diyarbekir` | [main_menu/setup/1337/11_art.txt:155](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/11_art.txt:155>) |
| `yedi_kardes` / 七兄弟塔 | `temple_tower` | `diyarbekir` | [main_menu/setup/1337/11_art.txt:156](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/11_art.txt:156>) |
| `great_iwan` / 伊万大殿 | `monument` | `cairo` | [main_menu/setup/1337/11_art.txt:159](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/11_art.txt:159>) |
| `qalawun_complex` / 盖拉温建筑群 | `monument` | `cairo` | [main_menu/setup/1337/11_art.txt:160](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/11_art.txt:160>) |
| `al_nasir_mosque` / 纳西尔·穆罕默德清真寺 | `monument` | `cairo` | [main_menu/setup/1337/11_art.txt:161](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/11_art.txt:161>) |
| `al_karimi_mosque` / 卡里姆清真寺 | `monument` | `damascus` | [main_menu/setup/1337/11_art.txt:162](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/11_art.txt:162>) |
| `ait_ben_haddou` / 埃本哈杜堡垒 | `monument` | `ait_benhaddou` | [main_menu/setup/1337/11_art.txt:165](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/11_art.txt:165>) |
| `koutoubia_marrakesh_work_of_art` /  | `temple_tower` | `marrakesh` | [main_menu/setup/1337/11_art.txt:166](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/11_art.txt:166>) |
| `ben_youssef_mosque` / 伊本·优素福清真寺 | `monument` | `marrakesh` | [main_menu/setup/1337/11_art.txt:167](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/11_art.txt:167>) |
| `rock_of_gibraltar` / 直布罗陀之岩 | `monument` | `gibraltar` | [main_menu/setup/1337/11_art.txt:168](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/11_art.txt:168>) |
| `qarawiyyin_fez_work_of_art` /  | `monument` | `fez` | [main_menu/setup/1337/11_art.txt:169](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/11_art.txt:169>) |
| `qutb_minar` / 库特卜塔 | `monument` | `delhi` | [main_menu/setup/1337/11_art.txt:180](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/11_art.txt:180>) |
| `great_mosque_of_samarra` / $ORIGIN$大清真寺 | `monument` | `samarra` | [main_menu/setup/1337/11_art.txt:184](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/11_art.txt:184>) |
| `stonehenge` / 巨石阵 | `monument` | `amesbury` | [main_menu/setup/1337/11_art.txt:185](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/11_art.txt:185>) |
| `colosseum_of_rome` / $ORIGIN$斗兽场 | `monument` | `rome` | [main_menu/setup/1337/11_art.txt:186](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/11_art.txt:186>) |
| `parthenon_of_athens_work_of_art` /  | `monument` | `athens` | [main_menu/setup/1337/11_art.txt:187](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/11_art.txt:187>) |
| `pyramid_art_key` / $ORIGIN$金字塔 | `monument` | `giza` | [main_menu/setup/1337/11_art.txt:188](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/11_art.txt:188>) |
| `sanchi_stupa` / 桑奇佛塔 | `monument` | `bhopal` | [main_menu/setup/1337/11_art.txt:189](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/11_art.txt:189>) |
| `leshan_giant_buddha` / 乐山大佛 | `monument` | `longyou_jiading` | [main_menu/setup/1337/11_art.txt:190](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/11_art.txt:190>) |
| `teotihuacan_temple_work_of_art` /  | `monument` | `tehotihuacan` | [main_menu/setup/1337/11_art.txt:191](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/11_art.txt:191>) |
| `melk_abbey` / $ORIGIN$修道院 | `monument` | `melk` | [main_menu/setup/1337/11_art.txt:193](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/11_art.txt:193>) |
| `dormition_cathedral_vladimir` / 圣母安息大教堂 | `monument` | `vladimir` | [main_menu/setup/1337/11_art.txt:195](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/11_art.txt:195>) |
| `ivanovsky_monastery` / 伊万诺夫斯基修道院 | `monument` | `pskov` | [main_menu/setup/1337/11_art.txt:197](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/11_art.txt:197>) |
| `kyiv_pechersk_lavra_work_of_art` /  | `monument` | `kyiv` | [main_menu/setup/1337/11_art.txt:199](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/11_art.txt:199>) |
| `gaocheng_astronomical_observatory` / 告成观星台 | `monument` | `dengfeng` | [main_menu/setup/1337/11_art.txt:202](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/11_art.txt:202>) |
| `pagoda_of_fogong_temple` / 佛宫寺释迦塔 | `monument` | `jincheng` | [main_menu/setup/1337/11_art.txt:204](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/11_art.txt:204>) |
| `giant_wild_goose_pagoda` / 大雁塔 | `monument` | `jingzhao` | [main_menu/setup/1337/11_art.txt:205](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/11_art.txt:205>) |
| `rila_monastery_work_of_art` /  | `monument` | `dupnitsa` | [main_menu/setup/1337/11_art.txt:207](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/11_art.txt:207>) |
| `euphrasian_basilica` / 尤弗拉西苏斯大教堂 | `monument` | `rovinj` | [main_menu/setup/1337/11_art.txt:210](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/11_art.txt:210>) |
| `carta_monastery` / 克尔察修道院 | `monument` | `fagaras` | [main_menu/setup/1337/11_art.txt:211](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/11_art.txt:211>) |
| `leaning_tower_of_pisa` / 比萨斜塔 | `monument` | `pisa` | [main_menu/setup/1337/11_art.txt:212](<C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/main_menu/setup/1337/11_art.txt:212>) |

## 泛用建筑基础设施与引擎边界

可从建筑列表、科技 `unlock_building`、改革/政策、自动扩建和脚本操作多路进入。表中列出建筑自身所有显式建造条件；外部同名引用的穷尽检索还见宽口径筛查附录。引擎内置队列、自动建设、艺术家每月随机开工不会全部展开成原版事件脚本，不能凭“没有建造事件”否定其可建性。
