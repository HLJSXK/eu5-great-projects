# ED 原版奇观接管：实施交接

> 仓库边界更新（2026-10-25）：Eureka 已迁至独立的 `eu5-eureka`；本文涉及它的旧目录和“四个根目录”描述保留为历史记录。当前入口见[仓库边界](Repository_Boundaries.md)。

> 状态：已归档（用户决定，2026-10-22）。实现、审计及剩余实机检查均不再列为当前待办；仅在用户重新提出问题或明确要求时重开。以下契约、进度与未验证项保留为历史记录，不表示未验证项已通过。

> 本文件是实施者的**唯一工作来源**：做什么、做到哪、不做什么、怎样算完成。
> 设计理由见 [ED_Vanilla_Wonder_Takeover_Design.md](../design/ED_Vanilla_Wonder_Takeover_Design.md)（下称“设计稿”）。
> 两者冲突时以本文件为准，并停下报告冲突，不要自行调和。
> 编写日期：2026-10-22。所有决策已由用户确认。

## 0. 使用方法

1. 先读完本文件第 1–3 章，再开工。第 4 章以后边做边查。
2. 严格按第 3 章的工作包（WP）顺序做。一个 WP 未验收前不开下一个。
3. 遇到第 9 章列出的情况立即停下报告，不要猜。第 10 章是常见疑问的预先答复，先查那里。
4. 每个 WP 完成后在本文件第 11 章的进度表里打勾，并写一行验证结果。不要另建进度文档。
5. 运行 Python 一律使用 `C:\Users\Hades\anaconda3\envs\eu5\python.exe`，不要用 `conda run`。
6. 编辑前按仓库规则运行 `scripts\ai_context.py --files <目标文件>`，并遵守其列出的 risk card。

## 1. 已定决策（不得重开、不得“改进”）

| 编号 | 决策 |
| --- | --- |
| D1 | 接管方式是**改写原版入口**（复制原版定义后改写），不用 `on_work_of_art_created` / `on_building_built` 等钩子捕获 |
| D2 | 所有 ED 等级变化只调用外部接口 `tv_wonder_raise/lower_unique_level_effect`（及灾害分流中的 generic 版），不直接写最终建筑等级 |
| D3 | 被替换的 `construct_building` 的隐含造价和工期不补偿；原版事件里写明的金钱、修正、需求、延时事件全部保留 |
| D4 | 通用灾害（三个共享降级效果）命中 ED 工程时只降一级；1 级工程不受影响；不记可修复损伤 |
| D5 | 开局移除已由 ED 表示的原版载体（归属门通过时） |
| D6 | `unique_notre_dame_de_paris`、`unique_leaning_tower_of_pisa` 的 `initial_level` 改为 1 |
| D7 | 地点：圣米歇尔山 `avranches`；特奥蒂瓦坎 `tehotihuacan`；巨石阵 `amesbury`；三一修道院 `pushkino`；凡尔赛 `paris`；大运河 `shanyang_huaian`。长城、孔雀宝座、法塔赫布尔西克里**不改** |
| D8 | `sacred_mountain` 场地规则临时加入 `topography = wetlands`；不改圣米歇尔山的基底 |
| D9 | `world_monument_group` 场地规则改为：本地是首都/城市，或任一紧邻地点是首都/城市（`any_neighbor_location`）。用户已确认 `tehotihuacan` 与 `tetzcoco` 相邻 |
| D10 | 删除 `unique_bastille`（id 198）。id 198 留空，不复用，不重排其他 id |
| D11 | **每个地点最多 3 座独特工程**，是硬约束 |
| D12 | 映射待定项中接管 7 项（见 2.2），不接管 `unique_bank_of_saint_george` 与 `unique_vatican_archives` |
| D13 | 本地化只写英文与简体中文 |

## 2. 范围

### 2.1 做（全部列在这里，没列的就是不做）

1. 数据修正：D6、D7、D8、D9、D10 及其连带的数据、生成物、测试计数。
2. 在 `data/unique_wonders.yaml` 中为第 6 章列出的 42 座工程写载体声明。
3. 实现原版扫描、改写、产出的生成器与测试（第 4、5 章契约）。
4. 产出：原版事件副本、原版决议 `REPLACE:`、原版建筑 `REPLACE:`（封存）、原版三个灾害效果 `REPLACE:`、
   新的接管效果与触发器、开局对齐 on_action、一个本地化键。
5. 更新文档：本文件进度表、设计稿状态行、`docs/design/Wonder_Level_Change_Interface.md` 第 7 节加一行指向本文件。

### 2.2 本次接管的 42 座工程

- 设计稿 2.1 的 36 座（删去巴士底狱不影响此清单）。
- 设计稿 2.2 中按建议接管的 7 项：`unique_cahokia_mounds`、`unique_angkor_hydraulic_system`、
  `unique_kairouan_holy_city`、`unique_isfahan_square`、`unique_fatehpur_sikri`、`unique_dresden_art_gallery`，
  以及 `unique_louvre_palace` 追加的翻修修正载体。卢浮宫本身已在 36 座内，所以共 36 + 6 = 42 座工程，
  映射待定项接管 7 项。

逐项载体与位点见第 6 章，那张表是唯一清单。

### 2.3 不做（明确禁止）

- 不处理设计稿 2.3“预备编目”和 2.4“不接管”中的任何对象，即使扫描器扫到它们。
- 不修改外部升降级接口、易主劫掠、苏伊士运河接入的现有行为与名称。
- 不重构任何现有生成器；只允许在 `_core.py` 的独特工程字段白名单中加入两个新字段（见 WP-2）。
- 不改原版文件。原实施范围不改 `.eu5-base/`；本轮用户审计要求的例外仅为纠正两条共享规则、同步共享视图并重建基础 BRIEF，不修改参考原版。
- 不给原版建筑、艺术品新增 ED 外的平衡改动；不调整 ED 工程的效果、造价、仪式。
- 不为 `sacred_mountain` 做“更好”的方案（D8 是临时修正，以后由别人单独做）。
- 不补造不存在的剧本内容。1658 的城市/建筑及艺术品文件通过 `include` 复用 1337 的同一组 20 个实例声明；本地声明为空不等于游戏不载入载体。
- 不编辑 `assets/historical/review/**`、`assets/archives/**`（历史评审记录与归档，保持原样）。
- 不为英文、简中之外的语言补本地化。唯一例外见 WP-1 第 5 步：允许从其他语言文件中**删除**巴士底狱的键。
- 不做实机测试；第 7.3 节列出的实机项交给用户。
- 不在 GUI、tooltip、月度读取等路径加任何修复性回退分支（仓库规则：未发布项目不做兼容修复）。

## 3. 工作包

| WP | 名称 | 依赖 | 主要接触文件 |
| --- | --- | --- | --- |
| WP-1 | ED 数据修正与删除巴士底狱 | — | `data/unique_wonders.yaml`、`data/wonder_site_rules.yaml`、`data/wonder_site_requirement_baseline.yaml`、仪式数据、图片清单、测试计数 |
| WP-2 | 载体声明字段 | WP-1 | `_core.py` 白名单与校验、`data/unique_wonders.yaml` |
| WP-3 | 原版扫描库与覆盖报告 | WP-2 | `scripts_engineering_department/vanilla_takeover/`（新） |
| WP-4 | 接管效果与触发器 | WP-3 | 新 scripted_effects / scripted_triggers 输出 |
| WP-5 | 原版入口改写（事件、决议） | WP-4 | 新事件副本、决议 `REPLACE:` 输出 |
| WP-6 | 建筑封存与开局对齐 | WP-4 | 新建筑 `REPLACE:`、on_action、`data/pulse_registry.yaml`、本地化 |
| WP-7 | 通用灾害分流 | WP-4 | 新 `REPLACE:` 三个灾害效果 |
| WP-8 | 测试、校验与文档收尾 | WP-1–7 | `tests/test_vanilla_wonder_takeover.py`（新）、文档 |

### WP-1 ED 数据修正与删除巴士底狱

步骤：

1. `data/unique_wonders.yaml`：按 D7 改 `location`；按 D6 改 `initial_level`。
2. `data/wonder_site_rules.yaml`：
   - `sacred_mountain.trigger_script` 的 `OR` 中加一行 `topography = wetlands`，其余不动。
   - `world_monument_group.trigger_script` 改为设计稿 8.2 的代码块，原样照抄。
3. 仪式与本地化数据中引用旧地点的条目改为新地点：在 `data/unique_wonder_ritual_designs.yaml`、
   `..._designs_zh.yaml`、`..._specs.yaml`、`..._design_matrix.yaml`、`..._feasibility.yaml`、`..._prompts.yaml`、
   `data/wonder_localization.yaml` 中，只替换这 6 座工程条目内的地点 key 与地名文字。
   不改仪式机制、不改无关条目。地名文字对照：

   | 工程 | 旧 | 新（英 / 中） |
   | --- | --- | --- |
   | 圣米歇尔山 | vire / Vire / 维尔 | avranches / Avranches / 阿夫朗什 |
   | 特奥蒂瓦坎 | tenochtitlan（仅本工程条目内） | tehotihuacan / Teotihuacan / 特奥蒂瓦坎 |
   | 巨石阵 | salisbury（地点 key） | amesbury / Amesbury / 埃姆斯伯里；文本“Salisbury Plain / 索尔兹伯里平原”**保留** |
   | 三一修道院 | moscow（仅本工程条目内） | pushkino / Pushkino / 普希金诺（叙事中的“谢尔吉耶夫”字样保留） |
   | 凡尔赛 | mantes / Mantes / 芒特 | paris / Paris / 巴黎 |
   | 大运河 | shangyuan / Nanjing / 南京 | shanyang_huaian / Shanyang / 山阳（原版地名；叙述中可称淮安） |

4. `data/wonder_site_requirement_baseline.yaml`：
   先改数据再跑审计脚本，然后按下表处理。实际状态与“期望”不同时，停下报告（第 9 章第 6 条）。

   | 工程 | 期望审计状态 | 基线处理 |
   | --- | --- | --- |
   | `unique_versailles_palace`（巴黎，城市） | PASS | 删除原有 FAIL 条目 |
   | `unique_mont_saint_michel`（阿夫朗什，湿地） | PASS | 无 |
   | `unique_stonehenge`、`unique_trinity_lavra` | PASS（规则 `always = yes`） | 无 |
   | `unique_grand_canal`（山阳） | UNKNOWN（`has_river` / `is_adjacent_to_lake` 无静态数据） | 保留原 UNKNOWN 条目，rationale 改为“山阳（淮安）毗邻洪泽湖（用户确认 2026-10-22）”，删掉“Nanjing terminus”说法 |
   | `unique_teotihuacan`（特奥蒂瓦坎） | UNKNOWN（`any_neighbor_location` 无静态数据） | 新增 UNKNOWN 条目，rationale 写“tehotihuacan 与 tetzcoco 相邻（用户确认 2026-10-22），tetzcoco 为 1337 城市与 TTZ 首都” |

   审计“通过”的定义：脚本退出码为 0，且输出中没有 `BASELINE DRIFT` 段。若脚本因无法解析 `any_neighbor_location`
   而报错退出，停下报告，不要改审计脚本。
5. 删除巴士底狱：
   - 数据条目（只删 `unique_bastille` 的条目，不动其他）：`data/unique_wonders.yaml`（id 198）、
     `data/unique_wonder_ritual_designs.yaml`、`..._designs_zh.yaml`、`..._specs.yaml`、`..._design_matrix.yaml`、
     `..._feasibility.yaml`、`..._prompts.yaml`（若有）、`data/wonder_localization.yaml`、
     `data/historical_wonder_images.json`、`data/wonder_image_crops.json`、
     `docs/design/Wonder_Ritual_Interpretation_Audit_Inventory.json`。
   - 删除以下文件（逐个列出，没有通配）：
     - `data/generated_icons/tv_wonder_unique_bastille_inaugurated.json`
     - `data/generated_wonders/tv_wonder_unique_bastille.json`
     - `assets/generated_icons/tv_wonder_unique_bastille_inaugurated.png`
     - `assets/generated_wonders/tv_wonder_unique_bastille.png`
     - `src/main_menu/gfx/interface/icons/buildings/tv_wonder_unique_bastille_inaugurated.dds`
     - `src/main_menu/gfx/interface/icons/towards_victory/wonders/tv_wonder_unique_bastille.dds`
     - `src/main_menu/gfx/interface/icons/towards_victory/wonders/tv_wonder_unique_bastille_cropped.dds`
     - `unique_wonders_site/dist/images/wonders/tv_wonder_unique_bastille.png`（若网站构建后仍残留）
   - 英文、简中本地化由生成器重新生成。其他 10 种语言（braz_por、french、german、japanese、korean、polish、
     russian、spanish、turkish 等）的 `src/main_menu/localization/<语言>/*.yml` 没有可用的生成器：
     删除**键名**中含 `bastille`（不分大小写）的整行，以及**值中引用** `unique_bastille` / `tv_wonder_bastille` 的整行；不改其他任何行，不新增翻译（用户授权修正，2026-10-22）。
   - `scripts_engineering_department/test_wonder_mechanics_rules.py` 第 1717 行附近：136 改 135，
     断言文字改为 `"must have exactly 135 unique wonders (Bastille removed 2026-10-22)"`。
     同一函数的 `expected_unique_ids` 若含 198，删去该项。
   - 写死计数只改这一处文档：`README.md` 第 79 行 “All 136 unique wonders” → 135。
     **不改**：`docs/technical/ED_Wonder_Ownership.md` 的验证记录（那是历史验证结果）、`docs/marketing/**`、
     `docs/design/Asia_Wonder_Expansion_Plan.md` 等计划与指南、`.editor_state/**`。在进度表中列出这些文件，交用户决定。
6. 重新生成（按此顺序，不得手改任何生成物）：
   1. `data/generated_files.yaml` 中 data 字段含 `unique_wonders.yaml` 的全部 ED 生成器；
   2. `scripts_engineering_department/in_game/gui/merge_tv_encyclopedia_wonders_cards_gui.py`
      （把卡片片段并入 `encyclopedia_lateralview.gui`）；
   3. `scripts/compat/gen_tv_prosper_or_perish_encyclopedia_lateralview.py`；
   4. `unique_wonders_site/scripts/build/build_site.py`；
   5. `scripts/gen_index.py`。

验收：

- 全仓搜索 `unique_bastille`、`tv_wonder_bastille` 零命中。搜索时排除：`.git/`、`.tmp/`、`tmp/`、`.editor_state/`、
  `assets/historical/review/`、`assets/archives/`、`docs/design/ED_Vanilla_Wonder_Takeover_Design.md`、
  本文件。排除范围内的命中不处理。
- 用第 7 章命令统计：每个地点的独特工程数 ≤ 3；巴黎恰为 notre_dame_de_paris、louvre_palace、versailles_palace。
- `audit_unique_wonder_site_requirements.py`、`test_wonder_mechanics_rules.py` 通过。

### WP-2 载体声明字段

步骤：

1. `scripts_engineering_department/wonder_mechanics/_core.py` 约第 1261 行独特工程的 `optional` 集合中加入
   `vanilla_carriers`、`vanilla_waivers`，并在同处写**形状**校验（第 4.1 节的枚举、必填、重复规则）。
   “key 在参考原版中存在”**不在** `_core.py` 里校验（`_core.py` 被许多生成器和 Web 编辑器加载，不应读原版），
   改由 WP-3 的扫描器与 7.2 第 11 条测试负责。不改其他字段的校验。
2. 在 `data/unique_wonders.yaml` 的 42 座工程上逐项写声明，内容严格照第 6 章表格。
3. 若 `great_projects_editor_web` 的 wonder 服务或契约测试因未知字段失败，只做“原样保留并回写这两个字段”的最小修复，
   不加 UI。

验收：加载器能读入 42 份声明；故意写错一个 `kind` 或重复一个载体 key 时，加载器报错（写成单元测试）。

### WP-3 原版扫描库与覆盖报告

新建包 `scripts_engineering_department/vanilla_takeover/`，只放库代码：

- `parse.py`：从 `.eu5-base/reference_game_files/game` 读文件（`utf-8-sig`），按大括号配对提取顶层定义块，
  正确跳过 `#` 注释与引号内的大括号。顶层定义有三种开头，都要识别：`NAME = {`、`scripted_effect NAME = {`、
  `scripted_trigger NAME = {`（后两种出现在事件文件里，如 `scripted_effect upgrade_great_wall = {`）。
  `namespace = x` 行不是定义块，但要记录每个事件所属的命名空间。可参考 `scripts/victory_task_codegen.py` 的 `_extract_top_level_block`，
  但新写一份放在本包内，不 import 主 mod 的代码（ED 根目录独立）。
- `scan.py`：对每个已声明载体，找出全部写入、读取、开局实例位点（规则见第 5.1 节），返回
  （文件、所在顶层定义 id、定义类型、行号、位点类型、所在块路径）。扫描范围：`in_game/events/**`、
  `in_game/common/**`（不含 `building_types` 中载体自身的定义）、`main_menu/setup/*/`。
  开局实例的识别：`<剧本>/11_art.txt` 中形如 `<类型> = { location = X ... key = <A> ... }` 的行；
  `<剧本>/07_cities_and_buildings.txt` 中形如 `<B> = { tag = T level = N location = X }` 的行。
  扫描器同时检查每个声明的 key 确实出现在参考原版中（艺术品 key 出现于 `create_art`/开局；建筑类型在 `building_types` 中有定义；
  effect 有 `scripted_effect`/顶层定义；modifier 有定义），找不到即报错。
  扫描位点统计的是物理声明。另记录 setup 文件的直接 `include` 来源；不展开 include 链，也不解释剧本覆盖/合并语义。
  因此 1658 继承的实例列在 1337 的定义处；原版增加本地覆盖后，必须复核有效实例，不能把物理声明统计当作运行时全集。
- `report.py`：命令行入口（须能以 `python scripts_engineering_department\vanilla_takeover\report.py` 直接运行，
  自行处理 `sys.path`，写法参照 `audit_unique_wonder_site_requirements.py` 开头），打印覆盖报告：每个载体 → 位点列表 → 处理方式（改写 / 豁免 / 开局对齐 / 未处理）。

验收（WP-3 只验扫描，不验改写；此时报告中的“处理方式”可全部为“未处理”）：

- 报告列出的位点与第 6 章逐项一致：第 6 章每个位点都在；
- 报告中出现第 6 章没有的位点 → 停下报告（第 9 章第 1 条），不要自行写豁免。

### WP-4 接管效果与触发器

生成器与输出（1 个生成器对应 1 个输出文件，登记到 `data/generated_files.yaml`，文件头写 `@Generated` 说明）：

| 生成器 | 输出 |
| --- | --- |
| `scripts_engineering_department/in_game/common/scripted_triggers/gen_tv_vw_vanilla_takeover_triggers.py` | `src/in_game/common/scripted_triggers/tv_vw_vanilla_takeover_triggers.txt` |
| `scripts_engineering_department/in_game/common/scripted_effects/gen_tv_vw_vanilla_takeover_effects.py` | `src/in_game/common/scripted_effects/tv_vw_vanilla_takeover_effects.txt` |

内容严格按第 4.2、4.3 节契约。验收：每座工程都有 `gate` 触发器；`present_here` / `present_owned` / `present_anywhere`
只为第 6 章“读取”列中实际需要的工程生成（需要哪种由 5.3 的作用域规则决定）；op 效果只生成声明用到的；名字与契约逐字一致。

### WP-5 原版入口改写（事件、决议）

| 生成器 | 输出 |
| --- | --- |
| `scripts_engineering_department/in_game/events/gen_tv_vw_vanilla_event_overrides.py` | `src/in_game/events/0000_tv_vw_vanilla_event_overrides.txt` |
| `scripts_engineering_department/in_game/common/decisions/gen_tv_vw_vanilla_decision_overrides.py` | `src/in_game/common/decisions/tv_vw_vanilla_decision_overrides.txt` |

规则见第 5 章。要点：一个原版定义只复制一次，同一次复制内完成写入改写与读取改写；事件用裸 id
（不加 `REPLACE:`），决议用 `REPLACE:`。

验收：覆盖报告中所有事件/决议位点状态为“改写”或“豁免”；第 7 章单一归属测试通过。

### WP-6 建筑封存与开局对齐

| 生成器 | 输出 |
| --- | --- |
| `scripts_engineering_department/in_game/common/building_types/gen_tv_vw_vanilla_building_overrides.py` | `src/in_game/common/building_types/tv_vw_vanilla_building_overrides.txt` |
| `scripts_engineering_department/in_game/common/on_action/gen_tv_vw_vanilla_takeover_on_action.py` | `src/in_game/common/on_action/tv_vw_vanilla_takeover_on_action.txt` |

另：on_action 名为 `tv_wonder_vw_startup_reconcile_on_game_start`（名字必须含 `wonder`：
`scripts/in_game/common/on_action/gen_tv_pulse_registry.py` 按名字是否含 `engineering_department` 或 `wonder`
把条目分流到 ED 的 `tv_engineering_department_pulse_bridges.txt`，否则会进主 mod）。把它登记在
`data/pulse_registry.yaml` 的 `bridges:` → `on_game_start:` 列表（主 mod 与 ED 共用的那一个列表）中，
紧跟在 `tv_wonder_initialize_existing_unique_wonders_on_game_start` 之后；然后运行 `gen_tv_pulse_registry.py`，
确认它出现在 ED 的 bridges 文件中、不在主 mod 的文件中。不登记 `on_game_load`。不改该生成器。本地化键 `TV_VW_CARRIER_LOCKED_TT` 写入
`src/main_menu/localization/{english,simp_chinese}/tv_engineering_department_l_*.yml` 末尾
（UTF-8 BOM，ASCII 直双引号）：

- EN：`"Only buildable here when the Engineering Department cannot host this wonder (the builder does not own its site)."`
- 简中：`"仅当本国无法由工程部承接该奇观（不拥有其工程地点）时，才能在此建造。"`

规则见第 4.4、4.5 节。

### WP-7 通用灾害分流

| 生成器 | 输出 |
| --- | --- |
| `scripts_engineering_department/in_game/common/scripted_effects/gen_tv_vw_vanilla_damage_overrides.py` | `src/in_game/common/scripted_effects/tv_vw_vanilla_damage_overrides.txt` |

规则见第 4.6 节。

### WP-8 测试、校验与文档收尾

1. 新建 `tests/test_vanilla_wonder_takeover.py`，至少包含第 7.2 节列出的测试。
2. 跑第 7.1 节全部命令，全部通过。
3. 更新本文件第 11 章进度表；设计稿顶部状态行改为“已实施，待实机验收”；
   `Wonder_Level_Change_Interface.md` 第 7 节加一行：“原生奇观事件接入已实施，见 ED_Vanilla_Wonder_Takeover_Handoff.md”。

## 4. 契约

`<K>` 表示独特工程 key（如 `unique_kremlin`），`<S>` 表示其 `location`，`<B>` 为原版建筑类型，`<A>` 为原版艺术品 key。

### 4.1 数据字段

```yaml
vanilla_carriers:            # 列表，至少 1 项
- kind: art                  # 必填：art | building | effect | modifier
  key: taj_mahal             # 必填：原版 key（存在性由 WP-3 扫描器校验，不在 _core.py 校验）
  mode: replace              # 必填：replace | augment
  op: raise                  # 仅 augment 必填：raise | lower | damage | restore；replace 禁止写
  present_at_level: 2        # 可选，仅 art/building；省略时按 5.4 推导
vanilla_waivers:             # 可选；本次实施中应全部为空，字段只为将来预留
- site: flavor_xxx.1         # 原版顶层定义 id
  carrier: some_key          # 必须是本工程已声明的载体 key
  reason: 说明
```

校验：同一载体 key 在全部工程中至多出现一次；`kind`、`mode`、`op` 取值严格枚举；`replace` 不得有 `op`。

### 4.2 触发器（`tv_vw_vanilla_takeover_triggers.txt`）

记号：`<F>` 为该工程的最终建筑类型（独特工程 `final_buildings` 中的那一个，如 `tv_wonder_unique_kremlin_inaugurated`）。
调用处一律由生成器写出**最终数字**，触发器内部不做算术：

- `ed_level` = `present_at_level + n − 1`（n 见 5.3）；
- `vanilla_level` = n。

| 名称 | 作用域 | 参数 | 主体（语义模板） |
| --- | --- | --- | --- |
| `tv_vw_<K>_gate_trigger` | 任意 | 无 | `location:<S>.owner ?= root`（与原版 flavor_mug.6 的 `location:agra.owner ?= root` 同式） |
| `tv_vw_<K>_present_here_trigger` | 地点 | `ed_level`、`vanilla_level` | `OR = { AND = { this = location:<S>  location_building_level = { building_type = building_type:<F> value >= $ed_level$ } }  <本地有原版载体> }` |
| `tv_vw_<K>_present_owned_trigger` | 国家 | 同上 | `OR = { AND = { owns = location:<S>  location:<S> = { location_building_level = { building_type = building_type:<F> value >= $ed_level$ } } }  any_owned_location = { <本地有原版载体> } }` |
| `tv_vw_<K>_present_anywhere_trigger` | 任意 | `ed_level` | `OR = { location:<S> = { location_building_level = { building_type = building_type:<F> value >= $ed_level$ } }  exists = work_of_art:<A> }`；只为 art 载体生成 |

`<本地有原版载体>` 的写法（一座工程有多个载体时，每个载体一条，放在同一个 `OR` 里）：

- art：`any_work_of_art_in_location = { this ?= work_of_art:<A> }`
- building：`location_building_level = { building_type = building_type:<B> value >= $vanilla_level$ }`

带参数的 scripted trigger 在 ED 中已有先例（`tv_wonder_location_has_active_project_for_trigger = { wonder_id = 130 }`），照该写法。

### 4.3 运算效果（`tv_vw_vanilla_takeover_effects.txt`）

| 名称 | 行为 |
| --- | --- |
| `tv_vw_<K>_raise_effect` | `tv_wonder_raise_unique_level_effect = { wonder = <K> }` |
| `tv_vw_<K>_lower_effect` | `tv_wonder_lower_unique_level_effect = { wonder = <K> }` |
| `tv_vw_<K>_damage_effect` | 在 `location:<S>` 上：若最终建筑等级 ≥ 2，则调用 lower，并把地点变量 `tv_vw_<K>_damage_debt` +1；否则无效果 |
| `tv_vw_<K>_restore_effect` | 在 `location:<S>` 上：若 `tv_vw_<K>_damage_debt` > 0，则调用 raise 并 −1（为 0 时移除变量）；否则无效果 |
| `tv_vw_startup_reconcile_effect` | 见 4.5 |

只生成该工程声明中实际用到的 op 效果。效果内不加 `custom_tooltip` 说明（接口自带）。

### 4.4 建筑封存（`tv_vw_vanilla_building_overrides.txt`）

对每个 `kind: building` 载体：复制原版建筑完整定义，前缀 `REPLACE:`，并在其 `allow` 块内追加：

```pdx
custom_tooltip = {
	text = TV_VW_CARRIER_LOCKED_TT
	NOT = { owner ?= location:<S>.owner }
}
```

- 原版没有 `allow` 块时新建一个；有则在原块内追加，**不得**出现第二个 `allow` 块。
- 其余内容逐字保留。
- 一个原版建筑类型只能被一个 TV 生成器 `REPLACE:`（7.2 单一归属测试覆盖）。

### 4.5 开局对齐

`tv_wonder_vw_startup_reconcile_on_game_start`（on_action）只调用 `tv_vw_startup_reconcile_effect`。该效果对第 6 章
“开局”列中的每个实例执行一次：

- 艺术品：若 `work_of_art:<A>` 存在，且其所在地点的所有者 = `location:<S>.owner`，执行 `destroy_art = work_of_art:<A>`。
- 建筑：在 setup 指定的地点上，若该地点所有者 = `location:<S>.owner`，移除该建筑。移除指令的写法必须取自参考原版中的现成用例
  （如 `destroy_building = "building(building_type:<B>|owner)"`）；若原版没有可用的强制移除写法，停下报告。
- 不调用升级接口，不改 ED 等级。

建筑外层地点取剧本实例 `s.location`，比较目标取独立的工程地点 `wonder.location`；艺术品左侧地点从实时作品对象取得。
当前 20 个声明（12 件艺术品、8 个建筑）都与对应 ED 地点相同，因此目前的所有者比较确实只筛掉无主地点，这是当前数据的结果。
这两个地点字段不合并；异地同主时清理，异地异主或无主时保留，已用构造的不同地点/所有者回归覆盖。
1337 与通过 include 复用它的 1658 均由同一 `on_game_start` 钩子清理；调用包在 `hidden_effect` 中，不注册 `on_game_load`。

### 4.6 通用灾害分流（`tv_vw_vanilla_damage_overrides.txt`）

对 `common/scripted_effects/location_effects.txt` 中的
`minor_destroy_building_levels_in_location`、`major_destroy_building_levels_in_location`、
`catastrophic_destroy_building_levels_in_location`：复制完整原块，前缀 `REPLACE:`，结构改为：

```pdx
REPLACE:minor_destroy_building_levels_in_location = {
	if = {
		limit = { <prev.building_type 是 ED 最终建筑> }
		<按建筑类型分派：prev.building_level >= 2 时调用对应工程的 lower 接口；否则无效果>
	}
	else = {
		<原版内容逐字保留>
	}
}
```

- “是 ED 最终建筑”的判定用 ED 已有的全局映射 `tv_wonder_final_building_type_to_wonder_id`
  （写法参照 `tv_wonder_ownership_on_action.txt` 的 `is_key_in_global_variable_map`）。
- 分派为生成的 `if / else_if` 链：每个最终建筑类型一支（删除巴士底狱后共 303 个类型：135 个独特 + 168 个通用风格变体，
  以生成后 `tv_wonder_final_building_type_to_wonder_id` 的实际条目数为准），独特工程调用 `tv_wonder_lower_unique_level_effect`，
  通用工程在地点作用域调用 `tv_wonder_lower_generic_level_effect = { wonder = <通用 key> }`。合计覆盖 191 座工程。
- 三个效果的 ED 分支完全相同，原版分支各自保留原文。

## 5. 改写规则

### 5.1 位点识别

| 种类 | 写入（raise） | 写入（lower） | 读取 |
| --- | --- | --- | --- |
| art | `create_art = { ... key = <A> ... }`；任意以 `key = <A>` 为参数调用的包装效果 | `destroy_art = work_of_art:<A>` | `exists = work_of_art:<A>`、`this = work_of_art:<A>`；`work_of_art:<A> = { ... }` 或 `?= { ... }`（作用域进入，见 5.3） |
| building | `construct_building = { building_type = building_type:<B> }`；`change_building_level_in_location = { building = building_type:<B> value = 正数 }` | `change_building_level_in_location` 取负数；`destroy_building` / `destroy_building_forcefully` 指向 `<B>` | `has_building = (building_type:)<B>`、`has_building_with_at_least_one_level = <B>`、`location_building_level = { building_type = building_type:<B> value ... }`、`any_buildings_in_location = { building_type = building_type:<B> ... }`、`total_effective_building_levels:<B>`、`is_at_max_level`（与 `<B>` 同块） |
| effect | `<E> = yes` | — | — |
| modifier | `add_*_modifier = { modifier = <M> ... }` | — | — |

注意 `has_building = building_type:<B>` 是读取，不是写入（`building = building_type:` 前面有 `has_`）。

### 5.2 写入改写

replace 模式，把原写入语句整体替换为：

```pdx
if = {
	limit = { tv_vw_<K>_gate_trigger = yes }
	tv_vw_<K>_raise_effect = yes        # lower 写入则为 _lower_effect
}
else = {
	<原写入语句，逐字>
}
```

augment 模式，原语句保留，紧接其后插入：

```pdx
if = {
	limit = { tv_vw_<K>_gate_trigger = yes }
	tv_vw_<K>_<op>_effect = yes
}
```

附加规则：

- `show_as_tooltip = { ... }` 内的写入同样改写（flavor_chi.53）。
- 同一个效果块（一个 `option`、`immediate`、`after` 或决议 `effect`）内对同一工程出现两处及以上写入：停下报告。
  第 6 章中唯一的同块多处是“不同选项”（如 flavor_pap.1501 两个选项各一处），那不算同块，各自正常改写。
- `change_building_level_in_location` 的 `value` 不是字面数字时，停下报告。
- 一个效果块内同时写多个不同工程的载体（如 flavor_mos.92 的 winter_palace 与未声明的 catherine_palace）：只改声明的，其他原样。

### 5.3 读取改写

逐条按下表处理；表中没有的读取形态，停下报告。“地点作用域”指该读取所在的最近作用域块是地点
（如 `location:moscow = { ... }`、地点迭代器的 `limit`、`capital = { ... }`）；“国家作用域”指事件/决议的
`trigger`、`potential`、`allow` 顶层（root 为国家）。

| 原版写法 | 所在作用域 | 改写为 |
| --- | --- | --- |
| `has_building = building_type:<B>`、`has_building = <B>`、`has_building_with_at_least_one_level = <B>` | 地点 | `tv_vw_<K>_present_here_trigger = { ed_level = P vanilla_level = 1 }` |
| `location_building_level = { building_type = building_type:<B> value >= m }`（或 `> m`，取 m+1） | 地点 | 同上，n = m（或 m+1） |
| `any_buildings_in_location = { building_type = building_type:<B> is_at_max_level = yes }`（块内只有这两行） | 地点 | 整个迭代器块替换为 present_here，n = 原版建筑的 `max_levels`（必须是数字） |
| `total_effective_building_levels:<B> > 0` 或 `>= 1` | 国家 | `tv_vw_<K>_present_owned_trigger = { ed_level = P vanilla_level = 1 }` |
| `total_effective_building_levels:<B> < 1` | 国家 | `NOT = { tv_vw_<K>_present_owned_trigger = { ed_level = P vanilla_level = 1 } }` |
| `any_work_of_art_in_location = { this = work_of_art:<A> }`（`this ?=` 同） | 地点 | 整个迭代器块替换为 present_here，n = 1 |
| `any_work_of_art_in_location = { OR = { this = work_of_art:<A>  this = work_of_art:<未声明> ... } }` | 地点 | `OR = { tv_vw_<K>_present_here_trigger = { ... }  any_work_of_art_in_location = { OR = { <只剩未声明的那几行> } } }`；只剩一行时去掉内层 `OR` |
| `exists = work_of_art:<A>` | 任意 | `tv_vw_<K>_present_anywhere_trigger = { ed_level = P }` |
| `work_of_art:<A> ?= { owner ?= ROOT }`（或 `root`，块内只有这一行） | 国家（trigger 中） | `tv_vw_<K>_present_owned_trigger = { ed_level = P vanilla_level = 1 }` |
| `work_of_art:<A> = { ... }`（效果中进入作用域，如 `change_art_quality`） | 效果 | 改为 `work_of_art:<A> ?= { ... }`，内部不动；已是 `?=` 的不动 |
| `random_work_of_art_in_location = { limit = { this = work_of_art:<A> } ... }`（含 `?=` 与 `OR` 形式） | 效果 | **不改**（载体不存在时自然落空）；覆盖报告中标“保持” |

表中 P = `present_at_level`（第 6 章给出）。`NOT = { 读取 }` 的外层 `NOT` 保留，只替换内层读取。
同一 `OR` 中并列的其他建筑（如 flavor_hsa.7 的 `hanseatic_kontor`、`hanseatic_shipwright_guild`）原样保留，只替换声明的那一行。

### 5.4 `present_at_level`

默认：开局剧本中存在该载体 → 1；否则 → 工程 `initial_level + 1`（以 WP-1 修改后的值为准）。
第 6 章已为有读取的载体写出期望值，生成器算出的值必须与之一致，不一致停下报告。

### 5.5 复制规则

- 事件：复制整个事件块到 `0000_tv_vw_vanilla_event_overrides.txt`，按命名空间分组，每组开头写原版 `namespace = <ns>`，
  事件用原 id，不加前缀。原版加载时出现的重复事件 id 报错是预期的。
- 事件文件内定义的辅助 `scripted_effect` / `scripted_trigger`：凡被复制事件（直接或间接）引用的，
  以 `tv_vw_<原名>` 复制到同一输出文件，并把复制事件中的引用改成新名；**不得**重定义原名。
  例：`upgrade_great_wall` → `tv_vw_upgrade_great_wall`，大运河两个辅助效果同理。
  augment 的 ED 调用插在**调用点**（事件选项内 `tv_vw_upgrade_great_wall = yes` 之后），不插进辅助效果内部。
- 决议：复制整块，前缀 `REPLACE:`，写入 `tv_vw_vanilla_decision_overrides.txt`。
- 建筑 `REPLACE:` 中复制的 `unique_production_methods` 子项必须改为 `tv_vw_<原名>`，避免与原版全局注册重名；只改子项 ID，定义内容逐字保留，并为新 ID 补齐本地化。
- 除改写点外，复制内容**必须**逐字保留（包括缩进、注释、空行）。
- 原版位点在 `in_game/common/on_action` 中且 root 不是国家：不改，停下报告。

## 6. 载体与位点清单（唯一清单）

位点用原版顶层定义 id 标识；×n 表示同一定义内有 n 处。生成器扫描结果必须包含这些位点。

### 6.1 艺术品（replace）

| 工程 | 载体 | 写入 | 读取 | 开局 | present_at_level |
| --- | --- | --- | --- | --- | --- |
| `unique_taj_mahal` | `taj_mahal` | flavor_mug.6 | — | — | — |
| `unique_st_peters_basilica` | `saint_peters_basilica` | flavor_pap.1501 ×2 | — | — | — |
| `unique_porcelain_tower_of_nanjing` | `porcelain_tower` | flavor_chi.52（地点来自上游 flavor_chi.51，见表后说明） | — | — | — |
| `unique_st_basils_cathedral` | `st_basil_cathedral` | flavor_mos.62 | flavor_mos.62（`random_work_of_art_in_location`，保持） | — | — |
| `unique_trinity_lavra` | `trinity_lavra_st_sergius_work_of_art` | flavor_mos.6 | 改写：flavor_mos.7、.11 ×5、.12 ×2、.38 ×2（其中一处 `exists`）；保持：flavor_mos.11 ×1（`random_work_of_art_in_location`） | — | 1 |
| `unique_winter_palace` | `winter_palace` | flavor_mos.92 | 改写：flavor_rus.70 ×1（与 `catherine_palace` 同在 `OR`）；保持：flavor_mos.92、flavor_rus.70 ×1（`random_work_of_art_in_location`） | — | 1 |
| `unique_milan_cathedral` | `milan_cathedral` | flavor_mlo.24 | — | — | — |
| `unique_santa_maria_del_fiore` | `duomo_di_firenze` | flavor_flo.28 | — | — | — |
| `unique_peacock_throne` | `peacock_throne` | flavor_mug.8 | — | — | — |
| `unique_isfahan_square` | `ali_qapu_palace` | flavor_ira.38 | — | — | — |
| `unique_hagia_sophia` | `hagia_sophia` | — | — | 1337 | 1 |
| `unique_notre_dame_de_paris` | `notre_dame_de_paris` | — | — | 1337 | 1 |
| `unique_leaning_tower_of_pisa` | `leaning_tower_of_pisa` | — | flavor_pis.4 ×2（trigger 中 `?= { owner ?= ROOT }` → present_owned；选项中 `= { change_art_quality }` → `?=`） | 1337 | 1 |
| `unique_stonehenge` | `stonehenge` | — | — | 1337 | 1 |
| `unique_mont_saint_michel` | `mont_saint_michel` | — | — | 1337 | 1 |
| `unique_aachen_cathedral` | `aachen_cathedral` | — | — | 1337 | 1 |
| `unique_lalibela_churches` | `lalibela_church_st_george_work_of_art` | — | — | 1337 | 1 |
| `unique_teotihuacan` | `teotihuacan_temple_work_of_art` | — | — | 1337 | 1 |
| `unique_great_mosque_of_djenne` | `djenne_mosque` | — | — | 1337 | 1 |
| `unique_sankore_university` | `sankore_madrasa` | — | — | 1337 | 1 |
| `unique_cave_monastery` | `kyiv_pechersk_lavra_work_of_art` | — | — | 1337 | 1 |
| `unique_alhambra` | `alhambra_palace` | — | — | 1337 | 1 |

琉璃塔的 `scope:target_location` 由 `flavor_chi.51/immediate/location:shangyuan` 保存，随后通过延时事件传给
`flavor_chi.52`；回归测试直接核对参考原版上游地点与 ED 地点一致。将来上游更改保存地点时必须同步复核映射。
孔雀宝座不同：写入点是当前首都，归属门只检查本国是否拥有德里；首都不在德里时也可能通过，随后提升定址德里的 ED 工程。
这由 D7 保留 ED 固定地点与 5.2 的回落规则共同决定，不要求首都等于德里。

### 6.2 建筑（replace + 封存）

| 工程 | 载体 | 写入 | 读取 | 开局 | present_at_level |
| --- | --- | --- | --- | --- | --- |
| `unique_kremlin` | `kremlin` | mos_build_kremlin_decision ×2、flavor_mos.57 | flavor_mos.28、.34、.35 ×2、.37 ×2、.57、.58、.62 | — | **2** |
| `unique_forbidden_city` | `forbidden_city` | flavor_chi.53（show_as_tooltip）、flavor_chi.54 ×2 | — | — | — |
| `unique_red_fort_delhi` | `red_fort` | flavor_mug.11 | — | — | — |
| `unique_versailles_palace` | `versailles` | flavor_fra.10 | flavor_fra.426、flavor_fra.428、fra_versailles_residence_decision、fra_versailles_permanent_decision | — | 1 |
| `unique_pharos_lighthouse` | `lighthouse_of_alexandria` | flavor_mam.40 | — | — | — |
| `unique_belem_tower` | `tower_of_belem` | flavor_por.5 | — | — | — |
| `unique_escorial_monastery` | `el_escorial_palace` | flavor_cas.46 | flavor_cas.69、flavor_cas.117 | — | 1 |
| `unique_schoenbrunn_palace` | `schonbrunn_palace` | flavor_hab.25 | — | — | — |
| `unique_enderun_palace_school` | `enderun_academy` | tur_enderun_academy_decision | — | — | — |
| `unique_louvre_palace` | `fra_louvre_museum` | flavor_fra.550 | — | — | — |
| `unique_hanseatic_town_hall` | `hanseatic_town_hall` | — | flavor_hsa.7 ×3（含 `is_at_max_level`） | 1337 lubeck | 1 |
| `unique_venetian_arsenal` | `venetian_arsenal` | — | flavor_ven.28、grand_tour_events.2 ×3 | 1337 venice | 1 |
| `unique_alhambra` | `alhambra` | — | flavor_gra.14 | 1337 granada | 1 |
| `unique_great_zimbabwe` | `great_enclosure`、`great_hill_complex`、`great_valley_complex`（三个载体） | — | — | 1337 great_zimbabwe | 1 |
| `unique_cahokia_mounds` | `woodhenge_of_cahokia` | flavor_chk.3 | flavor_chk.6 | — | **2** |
| `unique_angkor_hydraulic_system` | `khmer_baray` | flavor_khm.1001（destroy → lower） | flavor_khm.1000 | 1337 angkor | 1 |
| `unique_fatehpur_sikri` | `ibadat_khana` | flavor_mug.10 | flavor_mug.10 | — | 1 |
| `unique_dresden_art_gallery` | `zwinger` | flavor_mei.110 | — | — | — |
| `unique_kairouan_holy_city` | `monument_kairouan_mosque` | — | — | 1337 kairouan | 1 |

科技解锁（`ven_stato_da_mar` 解锁军械库、莫卧儿科技解锁敬拜堂）不改写，由封存使其失效。

### 6.3 状态（augment）

| 工程 | 声明（照抄进 `vanilla_carriers`） | 调用点 |
| --- | --- | --- |
| `unique_ming_great_wall` | `{ kind: effect, key: upgrade_great_wall, mode: augment, op: raise }` | flavor_chi.2 ×3（选项 b/c/d） |
| `unique_grand_canal` | `{ kind: effect, key: destroy_grand_canal_china, mode: augment, op: damage }` | flavor_chi.30 |
| `unique_grand_canal` | `{ kind: effect, key: repair_grand_canal_china, mode: augment, op: restore }` | flavor_chi.87、flavor_chi.124 |
| `unique_louvre_palace` | `{ kind: modifier, key: louvre_palace_renovations, mode: augment, op: raise }` | flavor_fra.305 选项 a |

6.1、6.2 的声明统一为 `{ kind: art|building, key: <载体>, mode: replace }`，`present_at_level` 只在表中该列为粗体
（与推导值不同）时写出，即仅 `unique_kremlin` 与 `unique_cahokia_mounds` 写 `present_at_level: 2`；其余省略。
大津巴布韦写三条 building 声明。阿尔罕布拉写一条 art（`alhambra_palace`）与一条 building（`alhambra`）。

`louvre_fortress`（fra.305 选项 b）、`chk_rebuilding_woodhenge` / `chk_funding_*`（flavor_chk.2）、圣彼得大殿的资助修正、
`taj_mahal_maintenance` 等需求**不声明、不改**。

### 6.4 说明性豁免（只写在本文件，不写进 YAML）

以下对象未被声明为载体，扫描器本来就不会报出。列在这里只是为了回答“要不要处理”：不处理。`vanilla_waivers` 本次应为空。

| 位点 | 对象 | 理由 |
| --- | --- | --- |
| flavor_mos.92 | `catherine_palace` | 同事件另一件艺术品，不属于冬宫 |
| flavor_pap.1500、flavor_pap.1502 | 圣彼得资助/中止修正 | 不是载体写入；只改完工事件 |
| flavor_chi.51 | 琉璃塔付款与延时 | 同上 |
| `on_game_start` → `china_set_up` → `set_as_part_of_grand_canal` | 运河沿线修正 | 原版网络型基础设施初始化，不是载体 |

扫描出 6.1–6.3 之外的位点，按第 9 章第 1 条处理。

## 7. 校验

### 7.1 必跑命令（在仓库根目录）

```powershell
$py = "C:\Users\Hades\anaconda3\envs\eu5\python.exe"
& $py scripts_engineering_department\audit_unique_wonder_site_requirements.py
& $py scripts_engineering_department\test_wonder_mechanics_rules.py
& $py -m pytest tests\test_vanilla_wonder_takeover.py tests\test_shared_rule_ownership.py tests\test_wonder_ownership.py tests\test_engineering_department_ai.py tests\test_wonder_priority_proposals.py -q --basetemp=.tmp\vw-acceptance
& $py scripts\test_victory_path_tasks.py
& $py scripts\validate.py src src src_court_positions src_eureka --fix --ai-report
& $py scripts_engineering_department\vanilla_takeover\report.py
```

最终静态验收显式指定四个部署目录，不依赖 Git 工作树或镜像是否带 `.git`。`--changed` 仍可用于日常快速检查，
但初次实施记录的“99 文件”只是当时的变更快照，不是稳定验收覆盖数；复核以本节全量命令为准。

地点上限统计（WP-1 验收用）：

```powershell
& $py -c "import yaml,collections;ws=yaml.safe_load(open('data/unique_wonders.yaml',encoding='utf-8-sig'))['unique_wonders'];c=collections.Counter(w['location'] for w in ws);print([x for x in c.items() if x[1]>3] or 'OK')"
```

### 7.2 `tests/test_vanilla_wonder_takeover.py` 至少包含

1. 覆盖：第 6 章每个位点在覆盖报告中为“改写 / 开局对齐 / 豁免”之一；报告中无“未处理”。
2. 单一归属：TV 全部生成物（`src/`、`src/`、`src_court_positions/`、`src_eureka/`）中，
   同一原版事件 id、同一 `REPLACE:` key 至多出现一次。
3. 事件副本不含 `REPLACE:`；决议、建筑、灾害效果副本都以 `REPLACE:` 开头。
4. 每个复制的事件块，去掉改写点后与参考原版块逐字相同（用生成器自己的改写函数反向比对，或比对改写点以外的行）。
5. 复制事件中不再引用任何仅在原版事件文件内定义的辅助名（都已改为 `tv_vw_` 前缀）。
6. 每个封存建筑恰有一个 `allow` 块，且含 `TV_VW_CARRIER_LOCKED_TT`。
7. 三个灾害效果的 ED 分派链与 `tv_wonder_final_building_type_to_wonder_id` 的条目一一对应（预计 303 个类型、191 座工程）。
8. `present_at_level` 推导值与第 6 章一致。
9. 每地点独特工程数 ≤ 3。
10. 两个新字段的负例：错误 `kind`、replace 带 `op`、载体重复，加载器均报错。
11. 每个声明的载体 key 在参考原版中存在（见 WP-3）。
12. `tv_wonder_vw_startup_reconcile_on_game_start` 出现在 ED 的 pulse bridges 文件中，不出现在主 mod 的 `tv_pulse_bridges.txt` 中。

### 7.3 归档的实机检查项（历史记录，不列为当前待办）

- 原版事件副本生效（以泰姬陵 flavor_mug.6、紫禁城 flavor_chi.53 悬停为例）。
- 封存后 `construct_building` 回落路径是否仍可建。
- 开局移除艺术品与建筑的时序在 ED 初始化之后。
- 地震命中 ED 工程只降一级；war_of_religions.17 夷平城市时 ED 生命周期正常重同步。
- 检查 D8 对通用 `sacred_mountain` 全地图湿地候选池的扩大；这是已接受的临时设计副作用，本轮不改其规则。
- 优先确认特奥蒂瓦坎的邻接条件及山阳的河湖条件；两项 UNKNOWN/INTENDED 基于人工确认，未由静态地理数据证明。

## 8. 交付物清单

| 类别 | 文件 |
| --- | --- |
| 数据 | `data/unique_wonders.yaml`、`data/wonder_site_rules.yaml`、`data/wonder_site_requirement_baseline.yaml`、仪式数据 6 个、`data/wonder_localization.yaml`、图片清单 2 个、`data/pulse_registry.yaml`、`data/generated_files.yaml` |
| 库 | `scripts_engineering_department/vanilla_takeover/{__init__,parse,scan,report,render,rewrite}.py` |
| 生成器 | WP-4 至 WP-7 表中 7 个 |
| 生成物 | 对应 7 个输出 + 重新生成的既有 ED 生成物、pulse bridges、兼容子模组 lateralview、网站数据、索引 |
| 代码 | `_core.py` 白名单与校验 |
| 本地化 | EN、简中 `tv_engineering_department_l_*.yml` 各 1 键 |
| 测试 | `tests/test_vanilla_wonder_takeover.py`；`test_wonder_mechanics_rules.py` 计数修改 |
| 文档 | 本文件进度表、设计稿状态行、`Wonder_Level_Change_Interface.md` 一行、写死计数的文档 |

## 9. 必须停下报告的情形

出现以下任一情况，停止当前 WP，在进度表写明现象与位置，等待答复：

1. 扫描结果缺少第 6 章任一位点，或出现 6.1–6.3 之外的新位点（不要自行写豁免）。
2. 位点所在作用域无法判断是地点还是国家，或 root 不是国家。
3. `change_building_level_in_location` 的 `value` 非字面数字；同一效果块内对同一工程有两处及以上写入；`is_at_max_level` 对应的 `max_levels` 不是数字；读取形态不在 5.3 表中。
4. 同一原版定义已被其他 TV 生成器复制或 `REPLACE:`。
5. `present_at_level` 推导值与第 6 章不一致。
6. WP-1 后审计脚本对 WP-1 第 4 步表中工程的状态与“期望”不同，或脚本报错退出。
7. 某条契约写法（参数算术、`?=` 用法、移除建筑指令）在参考原版或官方文档中找不到依据。
8. 任何必须修改第 2.3 节禁止项才能继续的情况。

## 10. 预先答复

| 疑问 | 答复 |
| --- | --- |
| worker 审计文档的行号和参考镜像对不上 | 以参考镜像 + 事件 id 为准，不按行号工作 |
| 原版事件还给了威望/合法性/人物，要不要删 | 不删。只改载体写入 |
| ED 工程已达上限时要不要回落给原版艺术品/建筑 | 不要。接口无效果即可，回落只在归属门不通过时发生 |
| 归属门不通过时生成的原版载体以后要不要并入 ED | 不要 |
| 原版事件的选项文字写“建造某某”，要不要改本地化 | 不改 |
| 要不要给 2.3 预备编目里的对象也写声明 | 不要 |
| 圣索菲亚的清真寺转换变量、圣地创建要不要处理 | 不要 |
| 要不要顺手修 `sacred_mountain` 湿地放宽带来的通用候选扩大 | 不要（D8） |
| 1658 剧本的本地载体声明扫描为空 | 不能据此判定游戏为空；其 include 复用 1337 的 20 个声明，报告会列出直接 include 来源，不展开覆盖语义 |
| 删除巴士底狱后 id 要不要重排 | 不要（D10） |
| 历史评审 JSON/HTML、`.tmp/`、`tmp/`、`ED_Wonder_Ownership.md` 验证记录、营销文案里还有巴士底狱或 136/192 | 保持原样，进度表里列出文件名即可 |
| 其他语言 yml 删掉巴士底狱键后出现空段落注释 | 保留注释，不整理 |
| `random_work_of_art_in_location` 里的读取要不要改成 ED | 不改（5.3 表最后一行） |
| 扫描到某个位点在 `scripted_effect` 内部而不是事件里 | 按 5.5 复制辅助效果并改名；改写点仍按 5.2/5.3 |
| 其他语言本地化缺键 | 正常（D13） |
| 灾害分流要不要也覆盖 `war_of_religions.17` 等直接拆除 | 不要。只改三个共享效果 |
| 能不能用 on_action 钩子代替复制事件，少写点代码 | 不能（D1） |
| 生成器能不能 import 主 mod 的 `scripts/victory_task_codegen.py` | 不能。ED 生成器只依赖 ED 与参考原版 |

## 11. 进度

| WP | 状态 | 验证记录（日期、命令、结果） |
| --- | --- | --- |
| WP-1 | ☑ | 2026-10-22：已完成六处地点、两处初始等级、两条场地规则、场地基线、巴士底狱数据/资产删除及其他语言中键名含 bastille 的行删除；38 个生成/合并/构建/索引步骤全部成功。场地审计退出 0，无 BASELINE DRIFT；机制校验通过（191 座工程、135 座独特工程）；所有地点 ≤3，巴黎恰为圣母院、卢浮宫、凡尔赛。另随删除更新自动仪式测试计数 134→133。用户已授权修正删除范围，额外移除 9 种语言共 135 行仅在值中引用巴士底狱的数字键条目；规定范围搜索零命中，阻断解除。 |
| WP-2 | ☑ | 2026-10-22：加载器读取 42 座工程、47 条载体声明；形状/枚举/重复/豁免负例及 Web 载入回写测试通过（19 passed；沙箱下临时目录使用仓库 .tmp）。 |
| WP-3 | ☑ | 2026-10-22：原版扫描 47 个载体、99 个位点，与第 6 章全部读写/保持/开局实例逐项一致，无新增/缺失；present_at_level 全部吻合。字段/解析/扫描测试 11 passed；report.py 可直接运行。 |
| WP-4 | ☑ | 2026-10-22：生成 42 座工程的 gate、实际需要的存在触发器和实际使用的运算效果；运河损伤债务走外部升降级接口。12 项接管测试通过。 |
| WP-5 | ☑ | 2026-10-22：输出 50 个裸 id 事件、4 个 REPLACE 决议、5 个转接前缀辅助定义；逐字保留未改写区、原版回落、读取门槛、辅助闭包及四个 mod 根目录单一归属检查通过（16 passed）。 |
| WP-6 | ☑ | 2026-10-22：21 种建筑各一个 allow 封存块，原条件及其他字段保留；20 个开局实例按所有者门清理，使用原版 catholic.txt 的强制移除语法。只注册 on_game_start，ED bridge 中紧跟原有初始化，主 mod 无该钩子；英文/简中键带 BOM。19 项测试通过。 |
| WP-7 | ☑ | 2026-10-22：三个灾害效果各自 REPLACE，ED 分支完全一致，303 个最终建筑类型与索引映射一一对应，覆盖 191 座工程；每支只允许 ≥2 级调用一次对应 lower，无损伤债务，原版 else 主体逐字一致。21 项接管测试通过。 |
| WP-8 | ☑ | 2026-10-22 审计复核：287 项回归通过；第 7.1 节显式四目录全量静态校验检查 376 文件，0 errors、0 warnings；场地审计退出 0，无基线漂移；机制校验 191 / 135；胜利任务、AI context 路由与 62 个 lint 样例通过。覆盖仍为 99 个物理位点（75 改写、20 开局对齐、4 保持），无未处理，并列出 1658 include 来源。validate.py 已恢复至 HEAD 的原始字节；共享两条规则及来源在基础库维护，两份 BRIEF 已重建；BOM、七个产物 CRLF、隐藏开局调用和异地/异主/无主守卫回归均已校验。初次“--changed 99 文件”仅留作历史快照，不作为当前验收覆盖证明。实机项仍按 7.3 执行。 |

### WP-8 校验接入说明（2026-10-22）

原先按规则 id 在 `scripts/validate.py` 添加的两处特判和 `_modifier_scope_at` 已全部删除。
规则修正在实际共享根 `C:/Users/Hades/Documents/code/eu5-modding-base` 的
`docs/knowledge/anti_patterns.yaml` 维护，并同步 `anti_patterns_shared.yaml` 视图与基础 BRIEF；
没有在本地规则库中覆盖共享 id。

`yaml_localization_non_ascii_quotes` 以通用 `only_in_paths: [/localization/]` 元数据限定本地化目录。
`eu4_province_modifier_scope` 的语义修正为省份作用域合法、地点/国家作用域不合法，依据官方
`reference_official_defines/docs/effects.log:367-373` 与原版 `flavor_chi.30`。
该条件需要真实类型分析，标为 `needs_parser`，不再以正则无条件报错，也不再猜测保存作用域的名称；
目前不是自动作用域检查器。共享库/本地加载结果、迁移归属和通用路径过滤均由共享规则归属测试覆盖。

审计 3.3 的当前清理结果正确：原实现建筑分支已使用剧本实例地点，并未硬编码为 ED 地点；
新增异地异主、异地同主及无主用例验证其表达力。没有把“必须同址”加成运行时限制。
审计中的其余信息项保持设计：12 种原版已禁止手动建造的建筑仍保留原限制；灾害仍按三份分派链输出；
`present_at_level` 仍按既定契约推导，不将原版建筑等级与 ED 等级强行等同。

校验 API 的临时仓库测试需要共享知识加载器；本次以
`PYTHONPATH=C:\Users\Hades\Documents\code\eu5-towards-victory\.eu5-base\scripts`
运行后 70 项全部通过。沙箱下 pytest 临时目录统一设在仓库 `.tmp/`。
胜利任务文件只有 `main()` 入口，故第 7.1 节命令已改为直接执行实际检查。

本轮改动跨两个根：工作区中的生成器、产物、测试、数据编码、交接与本地 BRIEF；基础根中的
`docs/knowledge/anti_patterns.yaml`、`docs/knowledge/anti_patterns_shared.yaml` 和 `docs/knowledge/BRIEF.md`。
共享规则的基础根加载与工作区合并加载、迁移覆盖和无本地同 id 遮蔽均由
`tests/test_shared_rule_ownership.py` 验证；基础根及工作区的 diff 空白检查通过。

### WP-1 原阻断与解除记录（2026-10-22）

执行 WP-1 第 5 步规定的键名过滤并完成全部重新生成后，按 WP-1 验收排除范围搜索
`unique_bastille` / `tv_wonder_bastille`，剩余命中全部位于：
`src/main_menu/localization/{braz_por,french,german,japanese,korean,polish,russian,spanish,turkish}/tv_engineering_department_wonder_mechanics_l_<语言>.yml`。
每个文件 15 行，均是键名不含 bastille、但值引用 `tv_wonder_unique_bastille` 的条目，例如
`braz_por/tv_engineering_department_wonder_mechanics_l_braz_por.yml:8500` 的
`TV_ENGINEERING_WONDER_PROPOSAL_RESUME_TEXT_198`，以及 `TV_ENGINEERING_WONDER_PROPOSAL_EXPAND_TEXT_198`、
`TV_ENGINEERING_WONDER_LOCKED_TEXT_198`、`STATIC_MODIFIER_NAME_tv_wonder_display_198_*`。
上述是原阻断证据。用户随后明确授权修正规则并继续实施；已将这些 135 行纳入删除范围，其他行及翻译保持原样，零命中验收通过。

已通过的验证：`audit_unique_wonder_site_requirements.py`（退出 0，无基线漂移）、
`test_wonder_mechanics_rules.py`（191 / 135）、
`pytest tests/test_wonder_ownership.py tests/test_engineering_department_ai.py tests/test_wonder_priority_proposals.py -q`
（254 passed）、`python scripts/test_victory_path_tasks.py`（静态检查通过）、`git diff --check`（退出 0）。
`scripts/validate.py --changed --fix --ai-report` 通过：70 个文件，0 errors、0 warnings。
交接中所列 `pytest scripts/test_victory_path_tasks.py -q` 未收集到测试：该文件只有 `main()` 入口，
因此另按其实际入口直接执行并通过，未修改测试组织方式。

按 WP-1 第 5 步及第 10 节保留的旧计数/历史文字文件：
`docs/technical/ED_Wonder_Ownership.md`、`docs/design/Asia_Wonder_Expansion_Plan.md`、
`.editor_state/handoff/accept-A.md`；营销文件
`docs/marketing/discord_modcoop_forum_en.md`、`steam_page_zh.md`、`steam_page_en.md`、
`reddit_post_en.md`、`qq_announcement_zh.md`、`paradox_forum_en.md`、`great_project_video_script.md`、
`github_wiki_zh.md`、`discord_official_release_en.md`、`github_wiki_en.md`。
`assets/historical/review/**`、`assets/archives/**`、`.tmp/**`、`tmp/**` 同样保持在排除范围内。
