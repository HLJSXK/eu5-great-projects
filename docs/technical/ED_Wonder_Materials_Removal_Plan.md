# 工程部：移除"建材"与"建材工坊"实施计划

- 模块：Engineering Department（`src/`、`scripts_engineering_department/`）
- 状态：已实施；待进游戏确认过滤器行为和实际月度维护费
- 编写日期：2026-10-18
- 目标：彻底移除商品 `tv_wonder_materials`（建材）和建筑 `tv_wonder_material_dispatch_point`（建材工坊），工地 `tv_wonder_labor_camp` 改为直接用原版商品维护。

项目未发布：不保留旧变量、旧键名、兼容分支或旧存档修复逻辑。

---

## 1. 已定决策

| 编号 | 议题 | 决定 |
|---|---|---|
| D1 | 工地维护配方 | 精简配方：每级 **工具 10、木材 20、砖石 20**（按原版默认价约 30 + 30 + 20 = 80） |
| D2 | 生产方式数量 | 只保留一个生产方式 `tv_wonder_labor_camp_maintenance` |
| D3 | 缺货惩罚 | 沿用现有规则：先用 `is_lacking_goods` 判断，再对三种投入的市场供需比取**算术平均** |
| D4 | 成本补偿 | 工地价格 `tv_wonder_labor_camp_price` 从 80 金提到 **200 金**；维护量不再额外提高 |
| D5 | 物流进度条 | **移除**。面板"物流"区块只有工坊进度条和工坊按钮，移除后区块为空，标题一并删除 |
| D6 | "建设工地"按钮 | 新增 building_type 脚本过滤器，按钮跳转到该过滤器 |
| D7 | 9 种非中英语言 | 删除的键直接删；改写的键按新英文**翻译** |
| D8 | 范围外文件 | **全部更新**：`.eu5-base` 知识库、本仓库技术文档、营销文档、原始设计文档、测试夹具 |

---

## 2. 现状摘要（实施前基线）

| 部件 | 位置 | 内容 |
|---|---|---|
| 商品 | `in_game/common/goods/tv_wonder_goods.txt` | `tv_wonder_materials`：加工品，默认价 5；整个文件只有这一个定义 |
| 工坊建筑 | `in_game/common/building_types/tv_engineering_department_buildings.txt:55` | `tv_wonder_material_dispatch_point`；`guild_max_level`；`important_for_AI = yes` |
| 工坊生产方式 | `in_game/common/production_methods/tv_engineering_department_production_methods.txt:7,17` | 标准版和无大理石版，产出建材 |
| 工地生产方式 | 同上 `:1` | `tv_wonder_labor_camp_maintenance`：工具 10、建材 20 |
| 价格 | `in_game/common/prices/tv_engineering_department_prices.txt:1,5` | 工地 80 金；工坊 200 金 |
| 建造需求 | `in_game/common/goods_demand/tv_engineering_department_construction_costs.txt:9` | 工坊建造需求 |
| 进度计算 | `in_game/common/scripted_effects/tv_engineering_department_effects.txt:1556` | `tv_wonder_update_logistics_metrics_effect`：建材比与工具比取平均，写入材料短缺损失 |
| 清理块 | 同上 `:1782` 附近（`tv_wonder_clear_current_survey_effect`）和 `:2600` 附近 | 删除工坊和材料相关变量 |
| 月度显示 | `in_game/common/international_organizations/tv_engineering_department.txt:171` | `monthly_change` 中的减项 `TV_WONDER_MATERIAL_INPUT_SHORTAGE_CONSTRUCTION_PROGRESS` |
| 面板 | `in_game/gui/panels/organization/tv_engineering_department.gui:2928-3020` | 工地按钮（过滤器 `uses_tv_wonder_materials`）、物流标题、工坊进度条、工坊按钮 |
| 面板帮助文本 | 同上 `:2598-2650` | 物流帮助小节，使用 `ORG_LOG_HELP_LOGISTICS_TEXT_1..3` |
| 百科 | `in_game/gui/encyclopedia_lateralview.gui:877,894` | 建材卡片，由生成加合并流程产出 |
| 修正类型和图标 | `main_menu/common/modifier_type_definitions/…:9,81-150`；`modifier_icons/…:5,41-80` | 1 条工坊价格修正，加 11 条商品自动修正 |
| 命名颜色 | `main_menu/common/named_colors/tv_engineering_department_named_colors.txt:4` | `goods_tv_wonder_materials` |
| 游戏概念 | `main_menu/common/game_concepts/tv_engineering_department_game_concepts.txt:21` | `tv_wonder_materials` |
| 图标 | 3 个 dds、3 个 `data/generated_icons/*.json`、`generate_dds_icon_config.json:168` | 商品图标、商品插图（放在主模组 `src/`）、工坊建筑图标 |

---

## 3. 实施步骤

### 第 0 步：准备

```powershell
C:\Users\Hades\anaconda3\envs\eu5\python.exe scripts\ai_context.py --files `
  src/in_game/common/production_methods/tv_engineering_department_production_methods.txt `
  src/in_game/common/scripted_effects/tv_engineering_department_effects.txt `
  src/in_game/common/international_organizations/tv_engineering_department.txt `
  src/in_game/gui/panels/organization/tv_engineering_department.gui `
  src/main_menu/localization/english/tv_engineering_department_l_english.yml
```

读取风险卡：`wonders.md`、`wonder_buildings.md`、`wonder_gui.md`、`international_organizations.md`、`localization.md`。

### 第 1 步：脚本层

**1.1 删除商品**
- 删除文件 `in_game/common/goods/tv_wonder_goods.txt`。

**1.2 删除工坊建筑**
- 在 `building_types/tv_engineering_department_buildings.txt` 删除 `tv_wonder_material_dispatch_point = { … }` 整块（`:55` 到文件末尾）。

**1.3 生产方式**（`production_methods/tv_engineering_department_production_methods.txt`）
- 删除 `tv_wonder_material_dispatch_point_production` 和 `tv_wonder_material_dispatch_point_production_no_marble`。
- 工地维护改为：

```
tv_wonder_labor_camp_maintenance = {
	tools = 10
	lumber = 20
	masonry = 20
	category = building_maintenance
}
```

  工地的 `possible_production_methods` 保持只有这一个。

**1.4 价格和建造需求**
- `prices/tv_engineering_department_prices.txt`：
  - `tv_wonder_labor_camp_price` 的 `gold = 80` 改为 `gold = 200`。
  - 删除 `tv_wonder_material_dispatch_point_price`。
- `goods_demand/tv_engineering_department_construction_costs.txt`：删除 `tv_wonder_material_dispatch_point_construction`。

**1.5 改写 `tv_wonder_update_logistics_metrics_effect`**（`tv_engineering_department_effects.txt:1556`）

删除以下变量（包括 set、clamp、remove）：
- `tv_wonder_effective_material_workshop_levels`
- `tv_wonder_material_workshop_need`
- `tv_wonder_material_workshop_need_display`

改名（未发布，不保留旧名）：

| 旧名 | 新名 |
|---|---|
| 全局 `tv_wonder_material_input_shortage_construction_progress` | `tv_wonder_worksite_input_shortage_construction_progress` |
| 局部 `tv_wonder_material_input_efficiency` | `tv_wonder_worksite_input_efficiency` |
| 局部 `tv_wonder_material_adjusted_monthly_construction_progress` | `tv_wonder_input_adjusted_monthly_construction_progress` |
| 局部 `tv_wonder_tools_input_efficiency` | 删除，改用下面的累加方式 |

缺货效率改为三种投入取算术平均：
- 只在 `local_var:tv_wonder_worksite_input_shortage_exists > 0` 时计算；否则效率为 1。
- 局部变量 `tv_wonder_worksite_input_ratio_sum` 初始为 0。
- 新增参数化辅助 effect `tv_wonder_accumulate_worksite_input_ratio_effect = { goods = <key> }`，依次对 `tools`、`lumber`、`masonry` 调用。每次在工地所在市场作用域里：
  - 需求大于 0 时，累加 `goods_supply_in_market(goods:$goods$) / goods_demand_in_market(goods:$goods$)`，结果限定在 [0, 1]；
  - 需求为 0 时累加 1。
- 最后 `tv_wonder_worksite_input_efficiency = ratio_sum / 3`，限定在 [0, 1]。
- 实施前先确认参数替换在引号函数字符串里有效。已知原版 `___test_effects.txt:128` 有 `value = goods:$goods$` 的用法，引号字符串内的用法要再确认一次。如果无效，就把三段计算直接展开写，不用辅助 effect。
- 辅助 effect 放在 `tv_engineering_department_effects.txt`，紧挨主 effect 之前；文件头注释写明"投入列表必须与 `tv_wonder_labor_camp_maintenance` 一致"。

其他修改：
- 文件头注释 `scale + logistics - materials - labor` 改为 `scale + logistics - worksite inputs - labor`。
- 保留 `# @validate_local_variable_cleanup` 标记，新增的局部变量要在结尾 `remove_local_variable`。

**1.6 清理块**
- `tv_wonder_clear_current_survey_effect`（约 `:1782`）和约 `:2600` 处的清理块：
  - 删除三个工坊变量的 `remove_variable`；
  - 把 `tv_wonder_material_input_shortage_construction_progress` 换成新名。

**1.7 月度显示**（`international_organizations/tv_engineering_department.txt:171`）
- `subtract` 块的 `desc` 改为 `TV_WONDER_WORKSITE_INPUT_SHORTAGE_CONSTRUCTION_PROGRESS`。
- `has_variable` 和 `value` 里的变量换成新名。
- 不改动 IO 的其他规则（`monthly_change`、`leader_change_trigger_type = none` 保持不变）。

**1.8 修正类型和图标**
- `main_menu/common/modifier_type_definitions/tv_engineering_department_modifier_types.txt` 删除 12 条：
  - `tv_wonder_material_dispatch_point_price_cost_modifier`
  - `can_extract_`、`ban_exports_of_`、`ban_imports_of_`、`local_…_output_modifier`、`local_…_establishment_speed`、`global_…_output_modifier`、`global_…_establishment_speed`、`global_…_pop_demand`、`…_impacts_inflation`、`…_used_for_minting`（均为 `tv_wonder_materials` 系列）
- `main_menu/common/modifier_icons/tv_engineering_department_modifier_icons.txt` 删除对应的 12 条。

**1.9 颜色和游戏概念**
- 删除命名颜色 `goods_tv_wonder_materials`。如果删除后文件为空，就删除整个文件。
- 删除游戏概念 `tv_wonder_materials`（`game_concepts/tv_engineering_department_game_concepts.txt:21`）。

**1.10 全局搜索补漏**
- 检查 `auto_modifiers`、`biases`、`generic_action_ai_lists`、`scripted_guis`、`on_action`、CMM 效果文件里有没有对工坊或建材的引用。实施前的扫描结果是没有，实施时再确认一次。

### 第 2 步：界面

**2.1 新建过滤器** `src/in_game/gui/filters/tv_engineering_department_filters.txt`（UTF-8 BOM）：

```
# BUILDING_TYPE
# root is the building_type
# scope:target is the country to filter

tv_wonder_labor_camp_only = {
	scope = building_type
	tag = building
	trigger = {
		this = building_type:tv_wonder_labor_camp
	}
}
```

依据：
- 原版建造界面 `production_lateralview.gui:467,864` 使用 `WithFilterTags('building')`。
- 原版 `filters/58_building_type.txt` 的 building_type 过滤器都带 `tag = building`。
- 作用域相等比较 `this = goods:lumber` 在原版 `generic_capital_economy_mission_pack.txt:380` 中有用例。

还需要做两件事：
- 补本地化 `search_filter_tv_wonder_labor_camp_only_name` / `_desc`，所有 11 种语言都要有。
- 如果 `group` 不能省略，就填一个不与原版冲突的值，并去掉 `exclusive_group`。

**2.2 面板** `tv_engineering_department.gui`
- `:2937` 工地按钮的 on_action 改为 `"[OpenLateralViewWithFilter('production', 'tv_wonder_labor_camp_only')]"`。
- 删除"物流"区块（`:2952-3020`）：标题 widget、工坊图标和进度条 hbox、`TV_ENGINEERING_BUILD_MATERIAL_WORKSHOP_BUTTON` 按钮。
- 帮助小节（`:2598-2650`）的物流标题和三行帮助文本保留，文本内容在第 3 步改写。
- 删除区块后检查外层 vbox 的固定尺寸。面板里有写死的 `size`，删除后可能留下空白，需要收紧。

**2.3 百科**
1. 从 `scripts_engineering_department/in_game/gui/gen_tv_encyclopedia_wonders_cards_gui.py:55,79` 去掉 `"tv_wonder_materials"`。
2. 运行生成器，重新生成 `data/generated_fragments/tv_encyclopedia_wonders_cards.gui`。
3. 运行 `merge_tv_encyclopedia_wonders_cards_gui.py`，把结果合并进 `encyclopedia_lateralview.gui`。
4. 运行 `scripts/compat/gen_tv_prosper_or_perish_encyclopedia_lateralview.py`，重新生成 `submods/tv_prosper_or_perish_compat/in_game/gui/encyclopedia_lateralview.gui`。

### 第 3 步：本地化（11 种语言）

语言列表：english、simp_chinese、braz_por、french、german、japanese、korean、polish、russian、spanish、turkish。
- 所有 YAML 保持 UTF-8 BOM 和 ASCII 直双引号。
- 中文写得平实，不加修饰。
- 工地名称用 `$tv_wonder_labor_camp$` 或 `[ShowBuildingTypeName('tv_wonder_labor_camp')]`，不要写成 `[tv_wonder_labor_camp|E]`（反模式 `engineering_building_loc_used_as_game_concept`）。

**3.1 直接删除的键**（`tv_engineering_department_l_*.yml`）
- 商品：`tv_wonder_materials`、`tv_wonder_materials_desc`
- 工坊：`tv_wonder_material_dispatch_point`、`_desc`、`_price`、`_construction`、`_production`、`_production_no_marble`
- 修正类型：12 条修正类型各自的 `MODIFIER_TYPE_NAME_*` 和 `MODIFIER_TYPE_DESC_*`，共 24 个键
- 界面：`TV_ENGINEERING_BUILD_MATERIAL_WORKSHOP_BUTTON`、`TV_ENGINEERING_MATERIAL_WORKSHOP_PROGRESS_TT`
- 如果"物流"标题 `TV_ENGINEERING_LOGISTICS_SECTION_TITLE` 在 2.2 之后仍被帮助小节使用（`:2598`），就**保留**这个键

`tv_engineering_department_game_concepts_l_*.yml` 删除：
- `game_concept_tv_wonder_materials`、`_desc`、`_europedia_desc`

**3.2 改名的键**
- `TV_WONDER_MATERIAL_INPUT_SHORTAGE_CONSTRUCTION_PROGRESS` 改为 `TV_WONDER_WORKSITE_INPUT_SHORTAGE_CONSTRUCTION_PROGRESS`。
  - 英文："Worksite Goods Shortage"
  - 中文："工地物资短缺"

**3.3 改写的键**（删除建材和工坊链接，内容改为新机制）

| 键 | 改写要点 |
|---|---|
| `TV_ENGINEERING_CONSTRUCTION_TAB_TOOLTIP` | "建立建材供应"改为"保证工地所需的工具、木材和砖石" |
| `TV_ENGINEERING_HEADER_GUIDANCE_BUILD` | 同上 |
| `TV_ENGINEERING_SURVEY_COST_TT` | 物流能力衡量的是"物资运抵工地的顺畅程度"，不再提建材 |
| `TV_ENGINEERING_ORG_LOG_HELP_LOGISTICS_TEXT_1` | 每级工地每月消耗工具、木材、砖石，从工地所在市场购买 |
| `TV_ENGINEERING_ORG_LOG_HELP_LOGISTICS_TEXT_2` | 任一种物资短缺时，工地进度缩放至三种物资供需满足率的平均值 |
| `TV_ENGINEERING_ORG_LOG_HELP_LOGISTICS_TEXT_3` | 可以靠本地生产或贸易进口补足这三种原版商品 |
| `TV_ENGINEERING_ORG_LOG_HELP_ORGANIZATION_TEXT_4` | 当前仍显示约 25 金；需按新配方在游戏里实测后回填 |
| `TV_ENGINEERING_WORKSITE_PROGRESS_TT` | 检查一遍；预计不需要改 |
| `game_concept_tv_wonder_construction_desc` / `_europedia_desc` | 删除建材和工坊的描述，改为"工地消耗原版建筑商品" |
| `game_concept_tv_wonder_logistics_competence_desc` | "让建材在匠人需要时抵达工地"改为"让物资……" |
| `tv_engineering_department.202.d` | "最后一批建材的账目"改为"最后一批物资的账目"，去掉概念链接 |
| `tv_engineering_department.312.d`、`.313.d`、`.321.d`、`.322.d` | 删除 `[tv_wonder_materials|e]` 链接，改成普通用词（"物资""木石"等） |

以上为扫描到的完整清单。实施时以 `grep -E "tv_wonder_materials|material_dispatch"` 搜出的结果为准；搜出的每一行都要么删除，要么改写。

**3.4 施工事件本地化**
- 中英文生成器 `gen_tv_wonder_construction_events_l_{english,simp_chinese}.py:31-42`：删除 12 个 `TV_*_WONDER_MATERIALS_STOCKPILE` 键。已确认没有脚本引用它们，是死键。删除后重新生成。
- 另外 9 种语言的 `tv_wonder_construction_events_l_*.yml`：手工删除同样的 12 个键。

**3.5 新增键**
- 第 2.1 步过滤器的 `search_filter_tv_wonder_labor_camp_only_name` / `_desc`，11 种语言都要有。

**3.6 翻译**
- 9 种语言按中英文终稿翻译：改写的键、改名的键、新增的键。
- 术语与各语言文件里已有的"工地"、"物流能力"等译名保持一致。

### 第 4 步：美术资源

删除以下文件：
- `src/main_menu/gfx/interface/icons/trade_goods/icon_goods_tv_wonder_materials.dds`
- `src/main_menu/gfx/interface/icons/trade_goods/illustrations/icon_goods_tv_wonder_materials.dds`
- `src/main_menu/gfx/interface/icons/buildings/tv_wonder_material_dispatch_point.dds`
- `data/generated_icons/icon_goods_tv_wonder_materials_trade_good_icon.json`
- `data/generated_icons/icon_goods_tv_wonder_materials_trade_good_illustration.json`
- `data/generated_icons/tv_wonder_material_dispatch_point_building_icon.json`

另外删除 `generate_dds_icon_config.json:168` 的 `tv_wonder_material_dispatch_point` 条目。

### 第 5 步：范围外文件（D8 全部更新）

**5.1 `.eu5-base`（独立仓库 `HLJSXK/eu5-modding-base`，单独提交）**
- `docs/knowledge/anti_patterns.yaml`：
  - `:254`（`building_efficiency_not_input_goods_access` 的 notes）："两种固定投入 `tv_wonder_materials` 和 `tools`"改为"三种固定投入 `tools`、`lumber`、`masonry`"。
  - `:837`：颜色示例改用仍然存在的商品颜色键。实施时从本仓库 `named_colors` 中选一个。
  - `:1229`（`engineering_building_loc_used_as_game_concept`）：正则改为 `\[(tv_wonder_labor_camp)\|[Ee]\]`，删除已不存在的 `tv_wonder_material_depot` 和 `tv_wonder_material_dispatch_point`。
  - `:4643`：利润示例改成不依赖已删除建筑的通用写法，保留"输出价值 5、投入超过 3.8462"这个数值说明。
- `docs/technical/EU5_Modding_Knowledge_Base.md:121,520`：示例同步替换。
- `docs/knowledge/MIGRATION_COVERAGE.yaml:5568,5872,6403,9377`：这是迁移来源的历史快照，文件描述为 "Complete source snapshots"。按 D8 一并更新时，需要和 `anti_patterns.yaml` 的修改保持逐字一致；更新前确认 `scripts/knowledge_loader.py` 和 `reclassify_shared_entries.py` 不会因为快照与来源不一致而报错。
- 修改后运行 `.eu5-base` 自身的校验或测试（如果有）。

**5.2 本仓库技术文档**
- `docs/technical/EU5_Modding_Knowledge_Base.md:123,522`：同 5.1 替换示例。实施时确认这份文件和 `.eu5-base` 那份是否属于重复内容；如果是，按最近提交"clean up duplications"的方向处理。

**5.3 营销文档**
| 文件 | 修改 |
|---|---|
| `docs/marketing/steam_page_zh.md:31,36` | "将建材投入四个部分"改为"用工具、木材和砖石推进四个部分" |
| `docs/marketing/github_wiki_zh.md:76` / `github_wiki_en.md:76` | "劳工营地 + 物料仓库 + 建材"改为"工地 + 原版建筑商品"；同时改正已过时的"劳工营地 / Labor Camp"名称 |
| `docs/marketing/great_project_video_script.md:66,69,71` | 删除"建材工坊"的台词，改成"工地需要工具、木材和砖石，缺货就会降低效率"；第 71 行"之前的奖励和建材"按新机制改写 |
| `docs/marketing/discord_update_260805_en.md` | 检查是否提到建材或工坊（实施前扫描只命中"工地"相关内容）；有就改 |

**5.4 设计文档**
- `docs/design/Original_Design.md:150`（"物资派出点"）：保留原文，在后面加一行说明"已于 2026-10 移除，工地改为直接消耗原版商品，见本计划"。这份文档记录的是原始设计。

**5.5 不改的命中项**
以下文件里的"建材"指的是原版或其他系统，不属于本次范围：
- `docs/knowledge/EU5_Gameplay_Reference.md:51`
- `docs/knowledge/gameplay/Official_Updates.md:94`
- `docs/knowledge/gameplay/Player_Cases.md:231`
- `data/victory_paths.yaml:1672-1688` 和 `src/main_menu/localization/simp_chinese/towards_victory_l_simp_chinese.yml:1070-1074`（科学院的建造需求）

**5.6 测试**
- `tests/fixtures/anti_patterns/gui_select_location_to_build_string/bad.gui:5`：键名换成 `tv_wonder_labor_camp`。
- 在 `scripts_engineering_department/test_wonder_mechanics_rules.py` 新增两条规则：
  1. `tv_wonder_labor_camp_maintenance` 的投入商品集合，必须等于 `tv_wonder_update_logistics_metrics_effect`（或其辅助 effect 的调用）里出现的商品集合；
  2. `src/` 下不得再出现 `tv_wonder_materials` 和 `tv_wonder_material_dispatch_point`。

### 第 6 步：索引和简报
- 运行 `scripts/gen_index.py`，重建 `data/index/*`（含 `modifier_localization.json`、`trigger_localization.json`、`loc_keys_en.txt`、`static_modifiers.txt`、`scripted_triggers.txt`）。
- 如果改了知识库或工作流文件（`anti_patterns.yaml` 在 `.eu5-base`；本仓库的风险卡如果涉及也算），运行 `scripts/gen_brief.py`。
- 检查 `data/generated_files.yaml` 有没有登记已删除文件的条目。实施前扫描没有发现。

---

## 4. 验证

### 4.1 静态检查

```powershell
C:\Users\Hades\anaconda3\envs\eu5\python.exe scripts\validate.py --changed --fix --ai-report
C:\Users\Hades\anaconda3\envs\eu5\python.exe -m pytest scripts_engineering_department tests
```

残留搜索（应该没有结果）：

```bash
git grep -n -I -E "tv_wonder_materials|material_dispatch|material_workshop|material_input|MATERIAL_INPUT|WONDER_MATERIALS_STOCKPILE" -- . ':!data/index' ':!docs/technical/ED_Wonder_Materials_Removal_Plan.md'
```

### 4.2 进游戏检查

| # | 检查项 | 通过标准 |
|---|---|---|
| 1 | 启动 | `error.log` 里没有未知商品、建筑、修正、本地化键或颜色的报错 |
| 2 | 工地 | 建造费用显示 200 金；维护界面显示工具 10、木材 20、砖石 20 |
| 3 | 维护费 | 记录每级工地的实际月维护费，回填 `ORG_LOG_HELP_ORGANIZATION_TEXT_4` |
| 4 | 缺货惩罚 | 制造某种商品短缺时，IO 月度进度出现"工地物资短缺"减项，数值约等于 基础进度 × (1 − 三项满足率平均) |
| 5 | 无缺货 | 物资充足时没有这个减项 |
| 6 | 按钮 | "建设工地"按钮打开建造界面，并且只列出工地 |
| 7 | 面板 | 物流区块已移除，没有空白或布局错位；帮助小节文字正确 |
| 8 | 百科 | 伟大工程页没有建材卡片，也没有空卡片 |
| 9 | 兼容子模组 | 加载 `tv_prosper_or_perish_compat` 后百科正常 |
| 10 | 其他语言 | 至少抽查一种非中英语言，确认没有缺失键 |

### 4.3 按钮失败的备用方案

如果第 6 项失败（自定义过滤器键不被 `OpenLateralViewWithFilter` 接受）：
1. 先尝试改用 `infrastructure_category` 过滤，可以用，但列表会混入原版基础设施；
2. 如果需要精确过滤，改为走带地点 `select_trigger` 的 generic action，见反模式 `gui_select_location_to_build_string` 的修正建议。

决定后回填本节。

---

## 5. 已知影响和风险

1. **需求集中在工地所在市场。** 原来工坊可以建在别的市场，把建材运过来；现在每级工地的 50 份原版商品需求全部落在一个市场。按组织能力上限，工地最多 20 级，可能需要靠贸易进口。验证时观察该市场的价格是否被明显推高。
2. **劳工岗位减少。** 原来每级工地配套约 10 级工坊，相应的劳工岗位都会消失。
3. **AI 行为。** 原来工坊 `important_for_AI = yes`，AI 国家会建工坊并出口建材；移除后不再有这个产业链。AI 自己建工地的逻辑不受影响（工地 `important_for_AI = no`，不允许自动建造）。
4. **两项需要实施时查证：**
   - 过滤器键能否用于 `OpenLateralViewWithFilter`（见 4.3）；
   - 参数替换在引号函数字符串里是否有效（见 1.5）。
5. **`.eu5-base` 是独立仓库。** 需要单独提交和推送，推送前要征得确认；本仓库的提交不包含 `.eu5-base`。

---

## 6. 提交顺序

1. 本仓库提交 A：第 1～4 步、5.2～5.6、第 6 步（游戏内容、界面、本地化、资源、文档、测试、索引）。
2. `.eu5-base` 提交 B：5.1。
3. 进游戏验证后，回填本计划第 3.3 步的维护费数值和第 4.3 节；如果 `docs/technical/Editor_Web_Refactor_Status.md` 或风险卡涉及本次改动，同步更新。
