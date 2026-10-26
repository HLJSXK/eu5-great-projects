# ED：原版奇观控制行为接管设计

> 状态：已实施并归档（用户决定，2026-10-22）；历史实机检查项不列为当前待办，仅在用户重新提出时重开。实施交接见
> [ED_Vanilla_Wonder_Takeover_Handoff.md](../technical/ED_Vanilla_Wonder_Takeover_Handoff.md)。
> 输入：worker 交付的 [扫描总览](../technical/ED_Vanilla_Wonder_Construction_Audit.md)、
> [逐项证据](../technical/ED_Vanilla_Wonder_Construction_Actions.md)、
> [候选实体](../technical/ED_Vanilla_Wonder_Construction_Entities.md)、
> [宽口径附录](../technical/ED_Vanilla_Wonder_Construction_Screening.md)。
> 依赖：[外部升降级接口](Wonder_Level_Change_Interface.md)（唯一等级写入口）、
> [苏伊士原生运河接入](../technical/EU5_1.4_Suez_Canal_Integration.md)、
> [ED 易主](../technical/ED_Wonder_Ownership.md)。
> 本稿的位点计数来自 `.eu5-base/reference_game_files`（2026-10 同步镜像）复核；worker 文档以本机安装
> buildid 26043558 为准。两者行号可能略有偏移，实施时以生成器重新扫描为准。

## 0. 结论

需要接管的只有一类行为：**原版对“具名、定址奇观”的身份载体进行写入（建、升、修、损、拆、迁），
以及原版对该载体是否存在、达到几级的判断**。另有一条横向缺口：原版通用灾害效果会直接降低
ED 最终建筑的等级，绕过外部接口。

清单中其余部分（泛用建筑、机构型独有建筑、泛用艺术品系统、运河运营状态、宗教用途与圣地登记、
科技解锁、单纯排定事件的 on_action/pulse）不接管，理由见第 2.4 节。

按当前 ED 池（136 座独特工程）与原版的重合程度：

| 分组 | 数量 | 处理 |
| --- | --- | --- |
| 立即接管 | 36 座 ED 工程 | 2.1 节逐项列出载体与位点 |
| 映射待定 | 9 组 | 2.2 节给出建议，默认按建议执行 |
| 原版有、ED 尚无 | 约 190 个原版身份 | 2.3 节编目；不声明即原样放行 |

接管由五个机制完成，全部由数据驱动、生成器产出，不手写原版副本：

1. **载体声明**：在 ED 工程数据上声明它对应的原版载体；未声明的工程不改动任何原版文件。
2. **写入转接**：把原版入口中的载体写入改写为外部升降级接口调用（替换式或附加式），带归属门与回落。
3. **存在读取转接**：原版对载体存在/等级的判断改为对 ED 等级的判断。
4. **载体封存与开局对齐**：已接管的原版建筑不能再手动建造；开局把已由 ED 表示的原版载体移除。
5. **通用损毁分流**：替换三个共享的灾害降级效果，命中 ED 最终建筑时改走降级接口。

ED 池将来扩张时，只需给新工程补一段载体声明并重新生成；原版事件、决议的改写随之出现，
其他未声明工程保持现状。

## 1. 判定口径

### 1.1 什么是“原版奇观”

同时满足以下三点的原版对象视为奇观身份：

- **具名**：有固定 key（`create_art` 的 `key`、建筑类型名、专用效果/修正名），不是随机生成的作品名。
- **定址**：固定在某个地点（`location_potential` 指定地点、事件写死 `location:x`），或固定在某国首都。
- **纪念性本体**：身份是建筑物本身，而不是机构、职能或可移动器物。

ED 池收录的对象直接视为奇观（例如恩德伦学院、孔雀宝座），即使按上面的口径属于机构或器物。

### 1.2 载体种类

| 种类 | 原版形态 | 例 |
| --- | --- | --- |
| `art` | 建筑型艺术品（monument / palace / temple_tower / mansion）；ED 收录的其他类型 | `taj_mahal`、`peacock_throne`（regalia） |
| `building` | 独有/事件建筑 | `kremlin`、`forbidden_city` |
| `effect` | 原版专用脚本效果，承载网络型或状态型工程 | `upgrade_great_wall`、`destroy_grand_canal_china` |
| `modifier` | 原版专用修正，承载状态型工程 | `louvre_palace_renovations` |

### 1.3 纳入与排除的行为

纳入：载体的创建、开工即完工式建造、等级变化、拆除、损伤、修复；对载体存在、等级、满级的读取；
开局剧本中已存在的载体。

排除：资助与工期修正（如圣彼得大殿的 120 年资助修正、泰姬陵维护需求）、单纯排定候选事件的
on_action/pulse/situation、作品质量修改（`change_art_quality`）、用途或宗教转换、圣地登记、科技或变量解锁。
资助、维护等仍是原版代价，保持原样；排定入口不需要改，因为被排定的事件本身会被改写。

## 2. 清单判定

### 2.1 立即接管

“写入点”“读取点”均按事件/决议 id 列出。所有 ED 工程都是独特工程，调用
`tv_wonder_raise/lower_unique_level_effect`。

**艺术品载体（替换式）**

| ED 工程 | 原版载体 | 写入点 | 读取点 | 备注 |
| --- | --- | --- | --- | --- |
| `unique_taj_mahal` | `taj_mahal` | flavor_mug.6 | — | 维护需求保留 |
| `unique_st_peters_basilica` | `saint_peters_basilica` | flavor_pap.1501（两个选项） | — | 1500 资助、1502 中止保持原版 |
| `unique_porcelain_tower_of_nanjing` | `porcelain_tower` | flavor_chi.52 | — | chi.51 付款与延时保持原版 |
| `unique_st_basils_cathedral` | `st_basil_cathedral` | flavor_mos.62 | flavor_mos.62 | |
| `unique_trinity_lavra` | `trinity_lavra_st_sergius_work_of_art` | flavor_mos.6 | flavor_mos.7/11/12/38 | ED 地点改为 `pushkino`（8.1） |
| `unique_winter_palace` | `winter_palace` | flavor_mos.92 | flavor_mos.92、flavor_rus.70 | 同事件的 `catherine_palace` 不接管 |
| `unique_milan_cathedral` | `milan_cathedral` | flavor_mlo.24 | — | |
| `unique_santa_maria_del_fiore` | `duomo_di_firenze` | flavor_flo.28 | — | |
| `unique_peacock_throne` | `peacock_throne`（regalia） | flavor_mug.8 | — | 原版建在首都；首都不在德里或不拥有德里时回落 |

**建筑载体（替换式 + 读取转接 + 封存）**

| ED 工程 | 原版载体 | 写入点 | 读取点 | 开局 |
| --- | --- | --- | --- | --- |
| `unique_kremlin` | `kremlin` | mos_build_kremlin_decision（两处）、flavor_mos.57 | flavor_mos.28/34/35/37/57/58/62 | ED 已 1 级，`present_at_level = 2` |
| `unique_forbidden_city` | `forbidden_city` | flavor_chi.53（`show_as_tooltip` 预览）、flavor_chi.54（两个选项） | — | |
| `unique_red_fort_delhi` | `red_fort` | flavor_mug.11 | — | |
| `unique_versailles_palace` | `versailles` | flavor_fra.10 | flavor_fra.426/428、fra_versailles_residence_decision、fra_versailles_permanent_decision | ED 地点改为 `paris`（8.3） |
| `unique_pharos_lighthouse` | `lighthouse_of_alexandria` | flavor_mam.40 | — | |
| `unique_belem_tower` | `tower_of_belem` | flavor_por.5 | — | |
| `unique_escorial_monastery` | `el_escorial_palace` | flavor_cas.46 | flavor_cas.69/117 | |
| `unique_schoenbrunn_palace` | `schonbrunn_palace` | flavor_hab.25 | — | |
| `unique_enderun_palace_school` | `enderun_academy` | tur_enderun_academy_decision | — | |
| `unique_louvre_palace` | `fra_louvre_museum` | flavor_fra.550 | — | 另见 2.2 的翻修修正 |
| `unique_hanseatic_town_hall` | `hanseatic_town_hall` | 无事件写入；可手动升到 2 级 | flavor_hsa.7（含 `is_at_max_level`） | 1337 吕贝克已有 |
| `unique_venetian_arsenal` | `venetian_arsenal` | 无事件写入；`ven_stato_da_mar` 解锁 | flavor_ven.28、grand_tour_events.2 | 1337 威尼斯已有 |
| `unique_alhambra` | `alhambra`；另有 1337 艺术品 `alhambra_palace` | — | flavor_gra.14 | 1337 两者均有 |
| `unique_great_zimbabwe` | `great_enclosure`、`great_hill_complex`、`great_valley_complex` | — | — | 1337 均有 |

**状态载体（附加式）**

| ED 工程 | 原版载体 | 写入点 | 运算 |
| --- | --- | --- | --- |
| `unique_ming_great_wall` | `upgrade_great_wall` | flavor_chi.2 选项 b/c/d | raise |
| `unique_grand_canal` | `destroy_grand_canal_china` / `repair_grand_canal_china` | flavor_chi.30 / flavor_chi.87、flavor_chi.124 | damage / restore |

长城的 `ruined/repaired_great_wall_of_china` 与大运河沿线的 `chi_grand_canal*` 修正是原版的网络型基础设施，
分布在数十个地点，不是 ED 单址工程的载体。它们保持原版，ED 只在同一事件里附加一次等级运算。

**仅开局已存在的艺术品（开局对齐）**

| ED 工程 | 原版 1337 艺术品 | 说明 |
| --- | --- | --- |
| `unique_hagia_sophia` | `hagia_sophia` | 清真寺转换变量 `hagia_sophia_now_mosque` 不接管（ED 读取/同语义写入的身份转化提案见 [ED_Wonder_Identity_Conversion_Design.md](ED_Wonder_Identity_Conversion_Design.md)） |
| `unique_notre_dame_de_paris` | `notre_dame_de_paris` | **数据冲突**：ED 初始 0 级 |
| `unique_leaning_tower_of_pisa` | `leaning_tower_of_pisa` | **数据冲突**：ED 初始 0 级；flavor_pis.4 读取 |
| `unique_stonehenge` | `stonehenge` | ED 地点改为 `amesbury`（8.1） |
| `unique_mont_saint_michel` | `mont_saint_michel` | ED 地点改为 `avranches`（8.1） |
| `unique_aachen_cathedral` | `aachen_cathedral` | |
| `unique_lalibela_churches` | `lalibela_church_st_george_work_of_art` | flavor_eth.220 的圣地创建不接管 |
| `unique_teotihuacan` | `teotihuacan_temple_work_of_art` | ED 地点改为 `tehotihuacan`（8.1） |
| `unique_great_mosque_of_djenne` | `djenne_mosque` | |
| `unique_sankore_university` | `sankore_madrasa` | |
| `unique_cave_monastery` | `kyiv_pechersk_lavra_work_of_art` | |

### 2.2 映射待定

身份有交叠但不完全相同。实施时默认按“建议”执行；用户否决的项保持原样放行。

| ED 工程 | 原版载体与入口 | 建议 | 理由 |
| --- | --- | --- | --- |
| `unique_cahokia_mounds` | `woodhenge_of_cahokia`：flavor_chk.2 资助修复、flavor_chk.3 建成、flavor_chk.6 读取 | 接管 | 木环阵是卡霍基亚遗址的组成部分 |
| `unique_angkor_hydraulic_system` | `khmer_baray`：1337 吴哥已有；flavor_khm.1000 读取、flavor_khm.1001 拆除 | 接管 | 人工湖属于吴哥水利系统；1001 的拆除即 ED −1 |
| `unique_kairouan_holy_city` | `monument_kairouan_mosque`：1337 已有 | 接管 | 大清真寺是圣城核心 |
| `unique_isfahan_square` | `ali_qapu_palace`：flavor_ira.38 | 接管 | 阿里卡普宫是广场的组成建筑 |
| `unique_fatehpur_sikri` | `ibadat_khana`：flavor_mug.10 建造与读取，莫卧儿科技解锁 | 接管 | 敬拜堂位于法塔赫布尔西克里 |
| `unique_dresden_art_gallery` | `zwinger`：flavor_mei.110 | 接管 | 茨温格宫是画廊所在 |
| `unique_louvre_palace` | `louvre_palace_renovations` 修正：flavor_fra.305 选项 a | 附加式 raise | 翻修与博物馆各算一次升级；“保留要塞”选项不动 |
| `unique_bank_of_saint_george` | 1337 艺术品 `palazzo_san_giorgio`，flavor_gen.46/50 等 7 处读取 | 不接管 | 宫殿早于银行存在，ED 初始 0 级；接管会在开局抹掉一个原版已有的宫殿 |
| `unique_vatican_archives` | `papal_archives`（1337 在 `assisi`，flavor_pap.101 迁至罗马）或梵蒂冈图书馆三件套（flavor_pap.13） | 暂不接管 | 档案馆与图书馆身份不一，且原版有迁址；需先定身份 |

### 2.3 原版有、ED 尚无（预备编目）

以下原版奇观身份符合 1.1 节口径，但 ED 池暂无对应工程。它们**不需要现在写任何数据**；ED 新增工程时，
从这里取载体声明即可。宽口径附录中其余命中不在编目内，除非未来人工提升。

- **事件创建的建筑型艺术品**：batalha_monastery_work_of_art、beijing_mosque、blue_mosque、brandenburger_tor、
  ca_foscari、capilla_de_los_reyes_nuevos、catherine_palace、christiansborg_palace、christianstad_trinity_church、
  church_of_saint_nicholas、dakhil_darwaza、doges_palace_genoa、el_badi_palace、equestrian_statue、firoz_minar、
  frauenkirche、gatchina_palace、goharshad_mosque、golden_roof、gur_e_amir、hampton_court、hana_no_gosho_palace、
  hisar_e_firoza、hofburg、huis_ten_bosch、imamzadeh_hossein、kapilesvara_siva_temple、kinkaku_ji、koskmedrese、
  kusumba_mosque、landtafel、lateran_palace、lodi_gardens、old_town_hall_leipzig、palace_monastery_of_santa_clara、
  palace_of_caserta、palazzo_reale_di_milano、pol_royal_column、san_zanipolo、shokoku_ji、sistine_chapel、
  st_andrew_church、st_pauls、st_peter_and_paul、st_stephens_cathedral、sulaymaniyya_takiyya、swe_makalos、
  the_great_bell_tower、the_iron_bridge、the_soyembika_tower、theatinerkirche_art、timbuktu_palace、
  tomb_of_the_first_emperor、uspensky_sobor、visconti_palace、vladislav_hall、whitehall、yuanmingyuan。
- **纪念性独有建筑**：ablaq_palace、ambras_castle、bajang_ratu、belvedere_palace、berlin_palace、bodrum_castle、
  castel_sant_angelo、city_of_victory、debere_meshwae、delhi_tomb、doges_palace、fortezza_di_sant_andrea、
  great_temple_of_tenochtitlan、herrenchiemsee_abbey、hexamilion_wall、hippodrome、hsa_burgtor、husuni_kubwa、
  imperial_city_of_hue、kastellet、kronborg、llotja_seda、mahmud_gawan_madrasa、munich_residenz_*（三阶段同一身份）、
  novodevichy_convent、oma_nizwa_fort、piazza_san_marco、qalat_al_mashwar、quirinal_palace、
  ranganathaswamy_temple_building、rock_of_monaco、sanssouci、sco_palace_of_holyroodhouse、sukharev_tower、
  the_bock_fortifications、theodosian_walls（另有同名 1337 艺术品）、uffizi、venkateswara_temple、walls_of_lucca、
  walls_of_ston、wali_songo_shrine、wat_chaiwatthanaram_temple_building、zazzau_walls，以及其余 14 个
  `monument_*` 马格里布/伊比利亚纪念建筑。
- **状态型工程链**：米兰家族图书馆（flavor_mlo.52–54、on_milanese_library_occupied）、维也纳城墙
  （flavor_hab.52/53）、奥得—施普雷运河（flavor_brapru.1500/1501）、德里陵墓（flavor_dlh.17–19 →
  construct_delhi_tombs，由 on_ruler_death_delhi_tombs_construction 排定）。
- **1337 已存在的建筑型艺术品**：除 2.1、2.2 已列者外的其余约 65 件（见候选实体文档“1337 已存在的建筑型艺术品”）。

### 2.4 不接管

| worker 清单中的部分 | 结论 | 理由 |
| --- | --- | --- |
| 宽口径筛查附录（2507 项） | 不接管 | 普通建筑、文本命中、间接引用与 debug；不构成奇观身份 |
| 科技 `advances` 全部 | 不接管 | 只解锁不建造；已接管建筑由机制四封存，解锁自然失效 |
| `commission_art` 与建筑师随机作品 | 不接管 | 无固定身份，无法对应独特工程；映射到通用工程会绕过 ED 的勘测与提案流程 |
| 泛用宏伟建筑：sponsor_a_cathedral/great_madrasa、construct_a_grand_palace、议会议题与议程、修道院网络、灌溉、道路 | 不接管 | 可在任意合格地点建造的泛用建筑，不属于原版奇观池 |
| 机构型独有建筑：学院、银行、海军部、法院、军营、铸币厂、治所、商站、日本氏族建筑、官厂、好望角驿站、贝伊堡垒/帕纳卡 | 不接管 | 身份是机构或职能；ED 池收录时再按 1.1 节例外处理 |
| 网络型建筑：长城各段、汉萨商栈（67 处）、引水系统、圩田、梯田、水坝、驿站 | 不接管 | 多地点分布的基础设施；长城只在其专用事件上附加 ED 运算 |
| 苏伊士运河、巴拿马运河 | 不接管 | 苏伊士已按用户决定接入原生运河机制并保留原版决议；巴拿马无 ED 工程 |
| canal_passage 开放/限制决议、on_ending_war 解除限制 | 不接管 | 运营状态，不是建设 |
| 圣索菲亚清真寺转换、圣地创建（flavor_eth.220、third_rome、lat_restore_the_holy_patriarchate）、枢机座堂、上师教坛 | 不接管 | 宗教用途与登记，不改变工程等级 |
| 可移动艺术品与泛用艺术品处理：雕像、礼器（孔雀宝座除外）、书画圣像圣髑；出售、求购、宗教献祭、damage_the_crown、laws.0018/0020 雕像、叛军索要、artist_events 损坏/替换、改质量 | 不接管 | 器物系统；对已接管载体而言载体已不存在，这些操作自然落空 |
| 单纯排定候选事件的 on_action、pulse、situation、disaster | 不改 | 被排定的事件会被改写，入口无需改 |
| on_location_changed_owner 中的易主处理 | 不改 | ED 易主劫掠已独立实现 |
| `000_johan_debug` | 不改 | 调试文件 |

## 3. 机制

### 3.1 机制一：载体声明

载体声明写在 ED 工程自己的数据条目上（`data/unique_wonders.yaml`），不另建平行注册表。
没有 `vanilla_carriers` 的工程不产生任何原版改写，这就是对“ED 池尚未覆盖”现状的兼容方式。

```yaml
- id: 130
  key: unique_kremlin
  vanilla_carriers:
  - kind: building          # art | building | effect | modifier
    key: kremlin
    mode: replace           # replace | augment
    present_at_level: 2     # 可省略，见 3.3
  vanilla_waivers:          # 生成器扫描到、但有意不改写的位点
  - site: flavor_mos.92
    reason: 同事件的 catherine_palace 不属于本工程
```

附加式条目额外写 `op`（`raise` / `lower` / `damage` / `restore`），例如：

```yaml
  vanilla_carriers:
  - { kind: effect, key: destroy_grand_canal_china, mode: augment, op: damage }
  - { kind: effect, key: repair_grand_canal_china, mode: augment, op: restore }
```

约束：一个原版载体只能属于一座 ED 工程；一座 ED 工程可有多个载体。生成器在加载期校验这两条，
并校验声明的 key 确实存在于参考原版中。通用工程（`wonders.yaml`）不接受载体声明，理由见 2.4 节。

### 3.2 机制二：写入转接

**识别的写入**

| 种类 | 写入形态 | 运算 |
| --- | --- | --- |
| art | `create_art = { key = K }`，以及 `create_work_of_art_with_artist_input = { key = K }` 一类带参包装 | raise |
| art | `destroy_art = work_of_art:K` | lower |
| building | `construct_building = { building_type = building_type:B }`；`change_building_level_in_location = { building = building_type:B value > 0 }` | raise |
| building | `change_building_level_in_location` 取负值；`destroy_building` / `destroy_building_forcefully` 指向 B | lower |
| effect | `E = yes` 调用点（含事件文件内辅助效果） | 声明的 op |
| modifier | `add_country_modifier` / `add_location_modifier` 等加入 M | 声明的 op |

**两种模式**

- 替换式：删除原写入，改为“通过归属门则调用 ED 运算，否则执行原写入”。载体不再由原版产生。
- 附加式：保留原写入，在其后追加“通过归属门则调用 ED 运算”。用于网络型、状态型载体。

**归属门**：事件或决议的 `root` 国家拥有 ED 工程地点（`location:<site>.owner ?= root`）。
外部接口本身只看地点是否有主，不看是谁触发；归属门防止甲国的原版事件给乙国境内的工程升级。
原版写入发生在别的地点（凡尔赛在巴黎、三一修道院在 `pushkino`、孔雀宝座在首都）时，只要同一国家
拥有 ED 地点就照常接管。`root` 不是国家的调用点（个别 on_action 直调）由生成器报出，人工处理。

回落只在替换式中存在：归属门不通过时原样执行原版写入，玩家仍拿到原版奖励。由此产生的原版载体
由机制三的读取兼容。

**运算语义**（建立在外部接口之上，不另写等级）

| op | 行为 |
| --- | --- |
| raise | `tv_wonder_raise_unique_level_effect`；0 级新建、活跃项目 +1、达上限无效果，全部沿用接口规则 |
| lower | `tv_wonder_lower_unique_level_effect`；1 级时拆除 |
| damage | 仅当 ED 等级 ≥ 2 时降一级，并在工程地点记一笔可修复损伤；1 级时不变、不记账 |
| restore | 仅当有可修复损伤时升一级并销一笔；没有账则无效果 |

`damage/restore` 解决“原版可逆损伤”：大运河被淹后又修复，ED 等级应回到原值，而不是被拆除后
重新以未完成仪式的 1 级建成。

**同块合并**：同一选项或 `immediate` 内对同一工程的多次运算先求和。净值为 0（例如先 `destroy_art`
再 `create_art` 的重建写法）时不调用接口；净值绝对值大于 1 时按 ±1 处理并在生成期警告。
原因是接口每次只改一级，同日重复调用读到的是改变前的等级。

**预览一致**：`show_as_tooltip` 内的写入同样改写（flavor_chi.53），选项悬停看到的就是接口自带的
`custom_description`，不另加手写说明。

**代价**：原版显式代价（金钱、修正、市场需求、延时事件）全部保留。替换掉的 `construct_building`
原本隐含的建筑造价和工期不再发生，ED 等级立即按接口生效。这与接口“不发奖励、奖励由调用方决定”
的边界一致：原版事件给出的奖励就是这一级工程。

**延时工程链**：只改完工点（圣彼得 1501、琉璃塔 chi.52、紫禁城 chi.54），开工、资助、中止事件保持原版；
归属门在完工时判定。

**产出形态**：生成器从参考原版中定位每个位点，复制整个所在定义再改写：

- 事件：写入早于原版加载的 `src/in_game/events/0000_tv_vw_<namespace>.txt`，
  按命名空间分组，开头重复原版 `namespace`。重复事件 id 的报错是预期的。
- 事件文件内的辅助效果（`upgrade_great_wall`、`destroy/repair_grand_canal_china` 等）以 `tv_vw_` 前缀
  另存一份，改写后的事件改调这份；不重定义原名，以免破坏仍由原版文件加载的其他事件。
- 决议、通用脚本效果、建筑类型：用 `REPLACE:` 写入 ED 根目录的对应文件夹，保留完整原块。

先例：`scripts/victory_task_codegen.py` 已按同一方式生成 `0000_tv_victory_path_task_price_events.txt`。
所有输出登记到 `data/generated_files.yaml`，全部位于 ED 独立根目录，不依赖主 mod。

**覆盖校验**：测试读取参考原版，对每个声明载体枚举全部写入与读取位点，断言每一处要么已改写，
要么在 `vanilla_waivers` 中写明理由；同时断言同一原版定义只被一个 TV 生成器复制。参考原版重新同步后
（正式版、DLC 更新）先跑这项测试，再看是否需要调整声明。

### 3.3 机制三：存在读取转接

替换式接管后原版载体不再出现，原版后续事件对它的判断必须改为看 ED。

| 原版读取 | 改写为 |
| --- | --- |
| `exists = work_of_art:K`、`this = work_of_art:K`、`any_work_of_art_in_location = { this = work_of_art:K }` | `tv_vw_<工程>_present_trigger` |
| `has_building` / `has_building_with_at_least_one_level = B` | 同上 |
| `location_building_level = { building_type = B value >= n }`、`total_effective_building_levels:B`、`is_at_max_level` | 同上，带等级参数 |

`present_trigger` 在两种情形下成立：ED 工程等级达到 `present_at_level + n − 1`；或该处确有原版载体
（来自回落）。在地点作用域中判断“此地就是 ED 地点”，在国家作用域中判断“拥有 ED 地点”。
`is_at_max_level` 按原版建筑的 `max_levels` 换算为 n。

`present_at_level` 由生成器推导，必要时手写覆盖：开局剧本中原版载体已存在时为 1（双方开局一致）；
不存在时为 ED `initial_level + 1`。例如克里姆林 ED 开局 1 级代表旧克里姆林，原版的 `kremlin`
建筑要靠决议才出现，所以取 2：玩家无论通过原版决议还是 ED 项目把它升到 2 级，原版后续事件都会认为
克里姆林已建成。这里不记录升级来源，与苏伊士接入的既定原则一致。

直接进入载体作用域的写法（`work_of_art:K = { change_art_quality = 10 }`、按 key 筛选后 `save_scope_as`）
一律改为 `?=` 可选作用域：载体不存在时安静落空，不转译为 ED 等级。

### 3.4 机制四：载体封存与开局对齐

**封存**：对 `building` 载体，生成 `REPLACE:` 版原版建筑类型，在 `allow` 中追加一条带
`custom_tooltip` 的条件：建造者不拥有对应 ED 地点。效果是：

- 能由 ED 承接时，玩家和 AI 都不能从建造菜单造原版建筑（克里姆林、汉萨市政厅的手动升级、
  解锁后的威尼斯军械库），杜绝“造原版建筑刷 ED 等级”的路径，也避免同一身份出现两份。
- ED 不能承接时（例如巴黎的主人不拥有 `mantes`），原版建筑照旧可建，与回落一致。

科技与变量解锁不改，它们在封存下自然失去作用。

**开局对齐**：在 ED 开局初始化完成后，对每个声明载体在开局剧本中的实例执行一次：剧本所有者拥有
ED 地点时移除原版载体（艺术品 `destroy_art`，建筑 `destroy_building_forcefully`），否则保留。
ED 的 `initial_level` 是开局等级的唯一来源，这一步不调用升级接口。worker 只扫描了 1337 剧本，
生成器需同时扫描 `main_menu/setup/` 下的全部剧本。

**数据冲突**（生成期报错，必须先改数据）：开局剧本已有原版载体、ED `initial_level` 却为 0。当前为
`unique_notre_dame_de_paris` 与 `unique_leaning_tower_of_pisa`，建议改为 1。与原版地点不一致的工程
按第 8 节裁定修改 ED 数据；裁定后剩余的不一致只报警告，由归属门处理。

### 3.5 机制五：通用损毁分流

原版用三个共享效果按比例降低地点内建筑等级：`minor_/major_/catastrophic_destroy_building_levels_in_location`
（`common/scripted_effects/location_effects.txt`）。地震、火山、城市火灾、小冰期、城镇特权事件，以及八个国家
事件文件中的十九处，都通过 `ordered_buildings_in_location = { order_by = building_level ... }` 调用它们。ED 最终建筑最高
6 级，几乎总会被选中；而这三个效果直接调用 `change_building_level_in_location`，绕过外部接口，
ED 的等级表、扩建候选和国家修正都可能与实际建筑脱节。

处理：以 `REPLACE:` 改写这三个效果。`prev.building_type` 是 ED 最终建筑（查
`tv_wonder_final_building_type_to_wonder_id` 全局映射）时，按工程 id 生成的分派链调用对应降级接口；
否则执行原版内容。规则：

- 任何灾害只降一级，不按比例；1 级工程不受影响（灾害损伤而不抹除）。
- 不记可修复损伤，因为原版没有对应的修复事件。
- 这样不复制任何调用事件，三十余个位点一次覆盖。

不经这三个效果的直接破坏保持原版：war_of_religions.17 的“夷平城市”拆除地点内全部建筑，`dismantle_fort`
只针对 `defense_category`（ED 最终建筑不用该类别）。整座拆除会触发 ED 最终建筑的 `on_destroyed`，
由现有生命周期重同步；这一点列入实机验证。

## 4. 典型链落地

| 链 | 原版 | 接管后 |
| --- | --- | --- |
| 泰姬陵 | flavor_mug.6 在阿格拉创建 monument 艺术品 | 拥有阿格拉：泰姬陵 +1（0 级则新建）；建筑师入籍、维护需求照旧 |
| 圣彼得大殿 | 1500 资助 120 年 → 1501 创建艺术品；1502 失去罗马中止 | 只改 1501：圣彼得 +1；资助修正与中止逻辑不变 |
| 紫禁城 | chi.53 付款并预览，10–20 年后 chi.54 升级建筑 | 两处都改为紫禁城 +1；chi.53 悬停即显示接口文本；迁都照旧 |
| 克里姆林 | 决议 construct_building；mos.57 再升一级；7 个事件读取 | 两处写入改为克里姆林 +1（开局 1 级 → 2 级）；读取按 `present_at_level = 2`；原版建筑不能手动建造 |
| 威尼斯军械库 | 1337 已有；科技解锁；ven.28、grand_tour 读取 | 开局移除原版建筑（ED 已 1 级）；读取转 ED；解锁后也不能再建原版建筑 |
| 大运河 | chi.30 洪水改沿线修正并置全局变量；chi.87/124 修复 | 原版沿线修正照旧；洪水时 ED ≥ 2 级才降一级并记账；修复时有账才升回 |
| 长城 | chi.2 选一省修复各段长城 | 各段修复照旧；另给长城 +1（须拥有固原宁夏） |
| 孔雀宝座 | flavor_mug.8 在首都创建 regalia | 拥有德里：孔雀宝座 +1；否则原版宝座照常生成 |
| 地震 | 降低最高等级的若干建筑 | 命中 ED 工程时 −1（不低于 1），其余建筑照原版比例 |

## 5. 被否决的方案

- **钩子捕获**（`on_work_of_art_created` / `on_building_built` 后销毁载体再升 ED）：不改原版文件，
  但选项悬停仍显示“获得艺术品/建造建筑”，与接口“悬停即真实预览”的设计冲突；建筑钩子无法阻止施工，
  玩家可反复造原版建筑刷 ED 等级；还需另写防循环标记处理销毁事件。
- **保留原版载体作为凭证**：省去读取转接，但同一身份出现两份，艺术品传统值与建筑修正重复计算，
  ED 降级后原版仍认为奇观存在。
- **未覆盖奇观落到通用工程**（如蓝色清真寺 → 天穹大神殿）：日后加入独特工程时身份会变，且绕过 ED 的
  勘测、规模与提案流程。
- **状态轮询**（月度比较原版变量）：所有现有状态链都有明确的写入事件，附加式改写更直接，也能正确预览。

## 6. 风险与实机验证

- 早载事件副本：与其他改同一原版事件的 mod 互斥，生效者取决于加载顺序；需在 mod 说明中列出被复制的事件文件。
- 原版更新：只要重新同步参考原版后重新生成并通过覆盖校验，副本即跟随更新。
- 需实机确认：`REPLACE:` 后的建筑 `allow` 是否同时约束脚本 `construct_building`（只影响回落路径，两种结果都可接受）；
  开局 `destroy_building_forcefully` / `destroy_art` 的时序是否晚于 ED 初始化；夷平城市时 ED 最终建筑的
  `on_destroyed` 是否触发；改写后的 flavor_chi.53 悬停文本。
- 同一天多个不同事件改同一工程：沿用接口“同日读旧等级”的限制，属罕见情形，不另做排队。
- AI：原版事件与决议的 `ai_chance`、`ai_will_do` 不改。

## 7. 已确认决定（2026-10-22）

用户确认全部按建议执行：

1. `construct_building` 的隐含造价与工期不再发生，只保留原版显式代价。
2. 通用灾害对 ED 工程只降一级且不拆除 1 级工程。
3. 2.2 节按“建议”列执行。
4. `unique_notre_dame_de_paris`、`unique_leaning_tower_of_pisa` 的 `initial_level` 改为 1。
5. 开局移除已由 ED 表示的原版载体。
6. 地点冲突按第 8 节执行（8.1–8.3 均已由用户确定）。

## 8. 地点冲突裁定

比较依据：真实地理、原版地图划分（`map_data/definitions.txt`、`location_templates.txt`、`ports.csv`）、
1337 所有者，以及 ED 基底场地规则（`data/wonder_site_rules.yaml`，独特工程运行时同样受其约束，
例如 `tv_wonder_location_meets_unique_mont_saint_michel_base_site_rules_trigger`）。
有几处 ED 选址显然是为了通过基底规则而偏离了实际地点；这种情况应改基底或登记已接受的 FAIL，
而不是牺牲地点。

| 工程 | 原版 | ED 现状 | 裁定 | 需要的配套改动 |
| --- | --- | --- | --- | --- |
| 圣米歇尔山 | `avranches`：同在科唐坦省，`wetlands`，有港口通圣马洛湾 | `vire`：卡昂省内陆丘陵，距海湾约 60 km | **原版更合理** | 基底 `sacred_mountain` 要求山地/高原/丘陵，是选 vire 的原因。改为 `grand_cathedral`（同为 medium / clergy / cultural，场地规则 `always = yes`），`base_key` 与 `mechanic_key` 一并改 |
| 特奥蒂瓦坎 | `tehotihuacan`：特斯科科省的专设地点，1337 属 TTZ | `tenochtitlan`：约 40 km 外的岛城，1337 属 TNC，并已有特诺奇蒂特兰堤道 | **原版更合理** | 场地规则按 8.2 改为“本地或紧邻地点为首都/城市”；静态审计无邻接数据，在场地基线登记 UNKNOWN。开局 1 级的归属由 TNC 变为 TTZ |
| 巨石阵 | `amesbury`：距遗址约 3 km | `salisbury`：同省城镇，约 13 km | **原版更合理** | `megalithic_circle` 无场地限制，两地 1337 同属英格兰，只改地点。仪式文本中的“索尔兹伯里平原”仍正确 |
| 三一修道院 | `pushkino`：莫斯科省东北，位于通往谢尔吉耶夫镇的道路上；地图上没有谢尔吉耶夫镇地点 | `moscow`：距修道院约 70 km，且已有克里姆林、圣瓦西里 | **原版更合理** | `great_monastery` 无场地限制，两地同属莫斯科大公国，只改地点 |
| 凡尔赛宫 | `paris`：原版 flavor_fra.10 要求巴黎为首都并在此建造，两个凡尔赛决议也以巴黎为准 | `mantes`：巴黎西北约 50 km，方向不对；1337 属埃夫勒（EVR）；乡村地点不满足 `triumphal_axis` 的城市要求 | **原版更合理** | 巴黎是离凡尔赛最近的地点，属法国，开局即满足城市要求。场地基线中凡尔赛的 FAIL 记录随之删除。代价是巴黎第四座独特工程（现有三座），以及失去“城外猎苑”的成长叙事 |
| 大运河 | 运河经过 41 个地点（`chinese_canal_geography`：杭州至大都） | `shangyuan`（南京）：位于长江边，不在运河线上 | **原版更合理** | 建议改为 `shanyang_huaian`（淮安：漕运总督驻地，黄、淮、运交汇之处，与原版洪水事件和“漕粮首航”仪式都吻合）；若实机查得其不满足 `large_canal_system` 的河流/湖泊/港口要求，退用 `jiangdu`（扬州）。同时改正场地基线中“南京为运河终点”的说法 |
| 长城 | 44 个 `ruined_great_wall_of_china` 地点构成网络，不含宁夏 | `fuchuan_ningxia`：宁夏镇，九边之一 | **都说得通，略偏原版** | 建议改为 `kaicheng_guyuan`（固原：同为九边之一，三边总制驻地，位于原版长城网络上），使原版修复事件与 ED 工程落在同一条墙上。优先级低 |
| 孔雀宝座 | 不定址：创建于当时首都 | `delhi` | **ED 更合理** | 宝座 1648 年起陈设在德里红堡，直到 1739 年被劫；ED 需要固定地点。保持 |
| 法塔赫布尔西克里（敬拜堂） | 不定址：建于当时首都 | `agra` | **ED 更合理** | 地图上没有西克里地点，阿格拉距其约 37 km，为最近地点。保持 |
| 教廷档案馆 | `assisi`（1337），flavor_pap.101 迁往罗马 | `rome` | 不涉及 | 本稿不接管；ED 的身份与罗马一致 |

所有改地点的工程都需要同步：`data/unique_wonders.yaml` 的 `location`、独特仪式的设计/规格/矩阵数据、
`data/wonder_localization.yaml` 与场地基线，然后重新生成并运行
`audit_unique_wonder_site_requirements.py` 与 `test_wonder_mechanics_rules.py`。

### 8.1 用户裁定（2026-10-22）

| 工程 | 结论 |
| --- | --- |
| 圣米歇尔山 | 迁至 `avranches`。临时修正：`sacred_mountain` 场地规则加入 `topography = wetlands`，不改基底；以后单独优化 |
| 特奥蒂瓦坎 | 迁至 `tehotihuacan`；`world_monument_group` 场地规则改为“本地或紧邻地点为首都/城市”，见 8.2 |
| 巨石阵、三一修道院 | 直接改地点：`amesbury`、`pushkino` |
| 凡尔赛宫 | 迁至 `paris`。为遵守**每地点最多 3 座独特工程**，删除巴士底狱，见 8.3 |
| 大运河 | 迁至 `shanyang_huaian`（毗邻洪泽湖，满足 `large_canal_system`） |
| 长城 | 保留 `fuchuan_ningxia` |
| 孔雀宝座、法塔赫布尔西克里 | 保留 ED 地点 |

湿地放宽的副作用：通用 `sacred_mountain` 的勘测候选也会包含全部湿地地点。作为临时修正可以接受；
若想把影响收窄，可写成 `AND = { topography = wetlands is_port = yes }`（潮汐岛型），仍能覆盖阿夫朗什。

### 8.2 `world_monument_group` 场地规则（已定）

现规则“首都或城市”把纪念建筑群当成都城建筑，与使用它的三座独特工程不符：卡霍基亚、特奥蒂瓦坎、
耶路撒冷圣城都是附着在一个区域中心旁的建筑群，本身未必是城市。改为“本地或紧邻地点为区域中心”：

```pdx
OR = {
	is_capital = yes
	location_rank ?= location_rank:city
	location_rank ?= location_rank:megalopolis
	any_neighbor_location = {
		OR = {
			is_capital = yes
			location_rank ?= location_rank:city
			location_rank ?= location_rank:megalopolis
		}
	}
}
```

- 特奥蒂瓦坎（`tehotihuacan`）紧邻特斯科科（`tetzcoco`，1337 为城市、TTZ 首都），通过；卡霍基亚（首都）、
  耶路撒冷（城市）不受影响。迁移后开局 1 级归 TTZ。
- 通用工程：可建在首都/城市本身或其紧邻地点；偏好脚本（首都 +10、发展度、识字率）不变，选址仍偏向中心本身。
- `any_neighbor_location` 为地点作用域迭代器（官方 `triggers.log`）。静态审计脚本没有地点邻接数据，
  对含此条件的结果应报 UNKNOWN，不得猜测；特奥蒂瓦坎由用户确认相邻，以 UNKNOWN 记入场地基线并写明依据。

### 8.3 凡尔赛与巴士底狱（已定）

凡尔赛迁至 `paris`：原版 flavor_fra.10 与两个凡尔赛决议均以巴黎为准，巴黎开局即满足 `triumphal_axis`
的城市要求，场地基线中凡尔赛的 FAIL 记录删除；法国拥有巴黎时归属门总是通过。

为守住每地点 3 座独特工程的上限，**删除 `unique_bastille`（id 198）**：巴士底狱作为象征主要是 1789 年之后
的事，在游戏时段内不足以占一个独特工程名额。删除后巴黎为巴黎圣母院、卢浮宫、凡尔赛宫三座。

删除范围（实施时逐项清理，不留兼容残留）：

- 数据源：`data/unique_wonders.yaml` 条目；独特仪式的 designs / designs_zh / specs / matrix / feasibility；
  `data/wonder_localization.yaml`；图片清单 `data/historical_wonder_images.json`、`data/wonder_image_crops.json`、
  `data/generated_icons/tv_wonder_unique_bastille_inaugurated.json` 及对应 DDS/PNG。
- 生成物：ED 根目录 21 个含该 key 的生成文件、Europedia 卡片片段、`submods/tv_prosper_or_perish_compat`
  的 lateralview、`unique_wonders_site` 数据，全部通过各自生成器重新生成，不手改。
- 审阅资料：`Wonder_Ritual_Interpretation_Audit_Inventory.json` 删除该条目；`assets/historical/review/`
  与 `assets/archives/` 是历史记录，保持原样。
- id 198 留空不复用，不重排其他 id（易主、升降级等事件号按 id 派生）。实施前确认生成器与测试不要求 id 连续，
  并更新写死“136 座独特工程 / 192 座工程”的测试与文档计数（改为 135 / 191）。
- 巴士底狱没有原版载体，不影响本稿的接管清单。

迁移后各地点独特工程数：巴黎 3（圣母院、卢浮宫、凡尔赛）、莫斯科 2、特诺奇蒂特兰 1、南京 2、
淮安 1、阿夫朗什 1、埃姆斯伯里 1、普希金诺 1、特奥蒂瓦坎 1，均不超过上限。
