# ED 伟大工程仪式重写：实施方案

> 日期：2026-10-23　状态：决策清单 D01–D38 已全部裁定，方案已同步；本轮采用 B 卷宗式界面，代码与生成物已实施；WP11 游戏内验收未执行
> 实施记录：[实现与验收报告](../technical/ED_Ritual_Rework_Implementation.md)
> 2026-10-29 用户修订：扩建一律重新自由选择三种仪式或朴素落成，按正常仪式结算费用、时长与奖励；旧仪式在本次落成时替换。此修订覆盖下文 D22、“沿用／结果 9”、扩建不重复结算及相关旧验收条目。当前实现契约见 `docs/knowledge/risk_cards/wonder_ceremony.md`。
> 配套文件：[决策清单](Wonder_Ritual_Rework_Decisions.md)，[UI 方案](../../ai_gui_assessment/mockups/ritual_rework/README.md)
> 本方案内凡是写着“建议”“默认”的地方，在决策清单中都有编号。用户裁定之前，实施方按决策清单里的推荐项理解，不要自己另选方案。

## 0. 与旧文档的关系

本方案取代下列内容，实施时以本文为准：

- `Wonder_Ritual_Interpretation_Design.md`（2026-10-21）中“136 个独特 + 56 个通用 × 3，逐工程手写约 576 种诠释”的首版范围，以及“落成冲击 + 十年纪念期 + 遗产”三段式中的**纪念期**。
- `Wonder_Ritual_Interpretation_Implementation_Plan.md` 中的实例状态、highwater 冲击额度、全国上限聚合、承接旧诠释、条件轴暂停等规则。本方案的生命周期更简单：易主、拆毁、遗忘都一律回到朴素，不需要承接，也不需要额度。
- `Wonder_Construction_Rework_TODO.md` 第 10 条中“扩建锁定原风格／原建筑变体”和“每次扩建重走仪式”。

以下内容继续沿用：价值观倾向移出基础层；每种风格自带一个价值观方向；单一物理成品；共享仪式阶段旧赠品（第 2、4 阶段）必须清除；外部升降级必须走 `Wonder_Level_Change_Interface.md` 的接口。

## 1. 需求与本方案的对应

| 编号 | 用户需求（原文要点） | 本方案落点 |
|---|---|---|
| R1 | 独特奇观继承通用奇观的三种仪式奖励，效果相同，文本不同 | §4.2 继承规则，§4.4 独特文本 |
| R2 | 三选一；奖励仍分国家 modifier、地点 modifier、即时奖励三类，但三类与三种仪式不再一一绑定；本轮奖励列表不变，生成器要允许以后自由组合 | §4.1 schema，§5 归一化 |
| R3 | 可选朴素；每种风格自带价值观倾向；完成时一次性移动 + 永久倾向；取消定时强化倾向；buff modifier 与价值观 modifier 合并 | §6.1 合并 modifier，§10 价值观 |
| R4 | 仪式完成状态脱离建筑，有独立生命周期，始终与仪式 modifier 同步；失去奇观即失去；掠夺不继承；显示为永久，内部 100 年计时，到期事件后淡忘；失去后进入朴素；朴素可随时重新仪式化 | §3 状态模型，§6 生命周期，§8 |
| R5 | 仪式阶段不再每月消耗国内支持度；建设结束事件说明反对派已闭嘴 | §11 |
| R6 | 奇观建筑不再按仪式分三个变体，只保留一种，只有一种 modifier | §4.3，§7.1 |
| R7 | 朴素等同于未完成仪式，不算续建；空壳 = 建成但未朴素，算续建；空壳只给文化传统；朴素与完整共用一个建筑，朴素只少仪式奖励；开局历史奇观为朴素 | §3，§7.6 |
| R8 | 工程部处于构思状态且国内有朴素奇观时，可用决议重新仪式化：事件选奇观 → 锁定项目 → 直接进入仪式阶段；专用落成事件只给 buff 和 10 威望 | §8 |
| R9 | 阶层意愿：阶层总是支持建造自己地点建筑的风格；其余按历史逻辑硬编码；没有明显偏好时在仪式阶段开始时随机；支持者忠诚上升，反对者下降，没有中立 | §9 |

**本轮不做：** 逐工程手写诠释内容；顺势／逆势成本；阶段事件；征服者改奉；纪念期；全国推力上限。

## 2. 现状审计摘要

下列事实已在源码中核对（行号为约数，以符号名为准）。凡是重写时必须拆除或改写的点都已标出。

### 2.1 阶段与流程

- 国家变量 `tv_wonder_stage`：0 = 构思／提案，1 = 辩论，2 = 勘测，3 = 建设，4 = 仪式，5 = 已落成。构思状态的严格判定是 `stage = 0` 加上 `has_variable = tv_wonder_concept_in_progress`；`tv_wonder_in_conception_trigger` 只判断 `stage = 0`。
- 建设结束：`tv_wonder_finish_construction_effect`（`src/in_game/common/scripted_effects/tv_engineering_department_effects.txt`）。它设置 `stage = 4`，给国内支持度 +20，然后调用 `tv_wonder_initialize_ceremony_runtime_state_effect`：独特奇观在这里被强制锁定为风格 1，并自动开始 8 阶段仪式。1 天后触发 `tv_engineering_department.202`“工程矗立”，文本让玩家去选风格。
- 风格选择：手写动作 `tv_wonder_choose_ceremony_style_1/2/3`。触发器 `tv_wonder_can_choose_ceremony_style_trigger` 把独特奇观排除在外。确认动作有三种：`tv_wonder_confirm_ceremony`（免费确认，覆盖风格 1 计时、风格 2 附属建筑、艺术品或无费用的风格 3，以及 CMM 跳过）、`_scaled_gold`、`_prestige`。
- 通用奇观的三种风格实际上是三套流程：风格 1 计时一年并施加 burden modifier（祝福值 ×−2）；风格 2 正常建造附属建筑 `tv_wonder_<key>_ritual_annex`，建成即完成；风格 3 即时结算，付艺术品、5×scaled gold 或 50 威望。
- 独特奇观：133 座走共享 8 阶段（ID 103–236，没有 198，法罗斯和圣索菲亚除外），由 `wonder_ceremony_lib.py`、`gen_tv_wonder_ceremony_effects.py` 和事件 `.9300–.9307` 实现，每 3 个月一个事件。第 2 阶段会送出对应通用风格 3 的即时奖励，第 4 阶段会免费建出通用附属建筑，第 8 阶段再给通用风格 1 的国家 modifier（`ritual_plan_for_style()` 会用通用风格 1 覆盖独特奇观自己的 `country_modifier`）。法罗斯（101）和圣索菲亚（102）各有专属流程（`unique_wonder_ritual_content/`）。
- 完成后进入落成：`tv_wonder_finalize_effect` 设置 `stage = 5`，然后触发 `.5000+id`。选项依次建出该风格的最终建筑、执行 `tv_wonder_apply_finalization_visible_rewards_effect`（工程师 +10 三属性、君主 +5、按等级的全国与地点庆祝 modifier、繁荣、剩余支持度兑换成稳定／正统／威望），再经由隐藏事件 `.6999` 清理并广播 `.6000+id`。

### 2.2 记录与建筑

- 通用奇观在 `data/wonders.yaml` 中有 3 个最终建筑（`final_buildings: {1,2,3}`，名字各不相同，例如 `tv_wonder_golden_sanctuary`）；独特奇观只有 `{1: tv_wonder_unique_<key>_inaugurated}`。三个通用变体的 modifier 完全相同，只在 `category`、`pop_type`、`rural_settlement`、维护方式和“直接建造入口”上有差异。
- “仪式已完成”没有独立记录。通用奇观靠“建筑类型 → 风格”反查（全局 map `tv_wonder_final_building_type_to_ritual_style`）；独特奇观靠国家 map `tv_wonder_unique_ritual_completed`。地点显示对通用奇观一律当作已完成，所以外部建出或开局预置的通用建筑也会显示成“仪式完成”，这是现有 bug。
- 附属建筑除了风格 2 的地点 modifier 外，还会按 `pop_type` 自动加上 +0.5 地方阶层权力（`RITUAL_AUXILIARY_ESTATE_POWER_BY_POP_TYPE`，`_core.py` 约 450 行；soldiers 被映射为 crown，而原版把 soldiers 归入 peasants 阶层）。易主和拆毁都不会处理附属建筑，新主人会白拿旧主人的风格 2 奖励。
- 易主：`on_location_changed_owner` → `tv_wonder_ownership_handle_location_owner_changed_effect`。旧主的风格 modifier 只在其名下没有同 ID 工程时才移除（按 wonder id 判断，不分风格）。新主不会获得 modifier。随后是“保留／劫掠”事件（`.8000+id`）。
- 开局：`tv_wonder_initialize_existing_unique_wonders_effect` 为 65 座 `initial_level > 0` 的独特奇观免费建出 1 级最终建筑，不写任何仪式状态。这已经符合“朴素”的定义。
- 价值观倾向：只存在于 `data/wonder_base_modifiers.yaml` 的 56 条 `monthly_towards_*`，经由 auto modifier `tv_wonder_auto_<key>` 随等级缩放生效。除此之外，运行时没有任何价值观逻辑。

### 2.3 国内支持度

IO 变量 `tv_wonder_domestic_support`（0–200）。`international_organizations/tv_engineering_department.txt` 的 `monthly_change` 从辩论结束一直到 `tv_wonder_finalized` 为止每月 −1，**仪式阶段也在扣**。降到 0 时，`tv_engineering_department_support_resolution_monthly_pulse` 在仪式阶段无法“提前结束建设”，只能触发 `.20` 项目崩溃（阶层满意度 −10%、处死工程师、−20 威望）。也就是说，玩家可能在建成之后因为仪式拖太久而失去整个项目。

### 2.4 计时与决议

- ED 现有代码里，延迟事件最长 1 天，计时变量最长 1 年，没有任何存储日期的做法。
- 原版支持 `trigger_event_silently = { id = X years = N }`（官方 effects.log 标注 `Supported Scopes: none/any`），也有 `type = location_event` 的事件（原版 20 处）。`set_variable` 与 `add_to_variable_map` 都支持 `days/months/years` 时限。
- ED 当前只有 `in_game/common/decisions/tv_vw_vanilla_decision_overrides.txt`（4 个原版 REPLACE）。原版决议结构是 `potential / allow / ai_will_do / option = { effect = {...} }`，顶层没有 `effect`。

## 3. 新状态模型

### 3.1 奇观实例状态

“实例”指“某地点上的某个 wonder id”。状态不存放在国家上，而是从地点建筑和地点变量推导出来。

| 状态 | 判定 | 物理建筑 | 效果 |
|---|---|---|---|
| 无 | 没有最终建筑，也没有 ≥1 级主体 | — | — |
| 建设中 | 当前项目在此地点，`stage = 3` | 模块／主体（`tv_wonder_<key>_<part>`、`tv_wonder_<key>`） | 只有文化传统 |
| **空壳** | 最终建筑等级为 0，主体 `tv_wonder_<key>` ≥ 1 级 | 主体 | 只有文化传统（主体现有的 0.4/级） |
| 仪式中 | 当前项目在此地点，`stage = 4`，`tv_wonder_ritual_in_progress` 已设置 | 新建项目：主体；扩建／重新仪式化：最终建筑 | 与其物理状态相同 |
| **朴素** | 最终建筑 ≥ 1 级，地点 map `tv_wonder_ritual_style_by_id` 中没有该 id | 唯一最终建筑 | 完整的基础效果（地方 + 全国 auto） |
| **完整（风格 n）** | 最终建筑 ≥ 1 级，map 中该 id 的值为 n ∈ {1,2,3} | 唯一最终建筑 | 基础效果 + 风格 n 的合并国家 modifier + 风格 n 的地点 modifier |

空壳不另设标志，直接由“主体 ≥1、成品 = 0”判定。它与现有“未完工剩余主体”本来就是同一种物理状态，现有优先候选机制已经把它当作续建（模式 1）。只有一处要改：续建空壳时，不必再建新的一级就允许宣布建成（决策 D20），见 §7.6。

### 3.2 状态转移

| 从 | 事件 | 到 | 说明 |
|---|---|---|---|
| 建设中 | 宣布建成（`finish_construction`） | 空壳（仪式阶段） | `stage = 4`，开放“朴素／三风格”选择 |
| 空壳（仪式阶段） | 选朴素 | 朴素 | 立即落成：建出最终建筑，发放落成奖励（D15） |
| 空壳（仪式阶段） | 确认风格 n → 计时完成 | 完整(n) | 正常落成事件，加上授予与一次性结算 |
| 空壳（仪式阶段） | 项目中止（失地、放弃） | 空壳 | 留在地图上，作为续建候选 |
| 朴素 | 重新仪式化完成 | 完整(n) | 专用落成事件，见 §8 |
| 朴素（扩建） | 扩建施工结束 | 仪式阶段（朴素 / 三风格） | D23 |
| 完整(n)（扩建） | 扩建施工结束 | 完整(n) | 跳过仪式阶段，直接落成（D22） |
| 完整(n) | 易主（任何原因，含被征服、劫掠、释放、继承） | 朴素 | 新旧主人都不保留 |
| 完整(n) | 最终建筑降到 0 | 无（或空壳，若主体仍在） | 状态随之清除 |
| 完整(n) | 降级但仍 ≥ 1 | 完整(n) | 保留（D24） |
| 完整(n) | 100 年计时到期 | 朴素 | 触发“淡忘”通知事件 |
| 朴素 / 完整 | 被外部接口建出（原版事件、调试） | 朴素 | 外部接口永不授予仪式 |

**不变量：**

1. 国家拥有 modifier `tv_wonder_<key>_ritual_<n>_modifier`，当且仅当它名下至少有一个地点的 `tv_wonder_ritual_style_by_id[id] = n`。
2. 地点拥有 `tv_wonder_<key>_ritual_<n>_location_modifier`，当且仅当该地点 `tv_wonder_ritual_style_by_id[id] = n`。
3. 一次性结算只在两个时刻各发生一次：阶层满意度在“举行仪式”（确认）时结算；价值观冲击和即时奖励在“完成仪式”时结算。扩建、读档、易主或重算都不会再次触发。
4. 地点变量 `tv_wonder_ritual_style_by_id` 只由两个生成的效果写入：授予（grant）和撤销（revoke）。其他代码一律调用这两个效果，不直接写 map。

### 3.3 项目模式

现有 `tv_wonder_project_mode`：1 = 新建／续建，2 = 扩建。新增 **3 = 重新仪式化**。模式 3 没有辩论、勘测和建设，锁定后直接进入 `stage = 4`。

## 4. 数据与 Schema

### 4.1 `data/wonder_generic_rituals.yaml`（改写）

删除 `style_1/2/3` 的固定形状，改为 `rituals` 列表。每项奖励可以是三类载体的任意组合。本轮做纯数据迁移：旧 `style_1.country_modifier` 迁入风格 1 的 `country_modifier`，旧 `style_2.local_modifier` 迁入风格 2 的 `location_modifier`，旧 `style_3.reward` 迁入风格 3 的 `one_shot`。数值一律不改，只有 D34 的三处修正：`great_assembly_hall` 风格 2 `local_max_literacy: 10`、`giant_dam_project` 风格 3 `site_prosperity: 0.5`、`great_sculpture_group` 风格 2 `local_monthly_prosperity: 0.004`。

```yaml
generic_rituals:
  sacred_mountain:
    estate_preferences:            # 见 §9；地点奖励所属阶层（此例为 clergy_estate）由生成器推导，不在此填写
      nobles_estate: 1
      burghers_estate: random
      peasants_estate: 3
      dhimmi_estate: random
      tribes_estate: 2
      cossacks_estate: random
    rituals:
    - style: 1
      societal_value: { axis: spiritualist_vs_humanist, direction: spiritualist }
      reward:
        country_modifier: { revoke_privilege_cost_modifier: -0.2 }
    - style: 2
      societal_value: { axis: centralization_vs_decentralization, direction: decentralization }
      reward:
        location_modifier: { local_clergy_desired_pop: 1 }
    - style: 3
      societal_value: { axis: traditionalist_vs_innovative, direction: traditionalist }
      reward:
        one_shot:
        - { type: stability, value: 21 }
```

（示例中的方向和阶层偏好只是为了说明结构，并非已经评审过的内容；内容由 WP7 产出。）

字段规则：

- `style` 恰为 1、2、3 各一项（决策 D01：固定三种）。
- `reward` 的键限定为 `country_modifier`、`location_modifier`、`one_shot`，每个键都可省略，但三者不能全空（价值观移动本身不算奖励，D01 附注）。`country_modifier` 只能用 country 类 modifier，`location_modifier` 只能用 location 类 modifier。`one_shot` 的词汇表沿用现有的 `STYLE_3_REWARD_EFFECTS`（`_core.py` 约 161 行，改名为 `ONE_SHOT_REWARD_EFFECTS`）：现有风格 3 用到的 `all_estate_satisfaction`、`diplomats`、`gold`、`legitimacy`、`ruler_adm/dip/mil`、`site_prosperity` 都不在 `data/cost_reward_units.yaml` 的奖励目录里，如果改用该目录作为词汇表，就必须先把这些类型补进去，否则“奖励原样迁移”无法成立。`gen_wonder_editor_catalog.py` 也引用了这个常量。
- 删除 `cost_type`。费用由规则表统一决定（D09）。
- `societal_value.axis` 必须是原版轴，`direction` 必须是该轴的某一端。允许全部 17 条原版轴（D12）；全表中时代轴方向与无条件轴方向的比例约为 1 : 2，校验器只输出统计，不报错。同一机制内三个方向两两不同，且至少跨两条轴（D13）。
- `estate_preferences`：键为阶层，值为 1/2/3 或 `random`。必须覆盖全部 7 个原版阶层（nobles、clergy、burghers、peasants、dhimmi、tribes、cossacks），只有地点奖励所属的那个阶层除外：它由生成器自动加入（指向带 `location_modifier` 的风格），作者不能手填，以免冲突（§9.2）。

### 4.2 `data/unique_wonders.yaml`

- 删除每个条目的 `ritual:` 和 `ceremony:`（共 135 条，含 133 套 8 阶段文本）。
- 仪式奖励、价值观方向和阶层偏好全部经由 `mechanic_key` 从通用机制继承（R1）。生成器为每座独特奇观生成**自己的** modifier key（`tv_wonder_unique_<x>_ritual_<n>_modifier`），内容与通用机制的风格 n 逐项相同，名称和描述则使用独特文本。
- 新增 `ritual_text`：独特奇观三种风格各自的名称与描述（§4.4）。
- `final_buildings: {1: ...}` 改为 `final_building: ...`（单值）。
- `base_effect_multiplier: 2` 仍只作用于基础效果，不作用于仪式奖励（与现状一致）。

### 4.3 `data/wonders.yaml` 与 `data/wonder_final_buildings.yaml`

- `final_buildings: {1,2,3}` 改为 `final_building: <key>`。56 个通用机制各自只保留一个成品（命名规则见 D08）。
- 成品的效果本来就与仪式无关：三个变体的 `modifier` 块完全相同，只含随等级缩放的基础效果。`final_local` 在建筑上直接生效；国家级基础效果写在建筑上只用于显示，实际由 `tv_wonder_auto_<key>`（`scales_with` 国家等级 map）生效。这部分机制不变，唯一的变化是 `monthly_towards_*` 随基础层一起删除。仪式奖励一律不写在建筑上（见 §6.1）。
- 三个变体之间真正不同的只有非效果字段：`category`、`pop_type`、`rural_settlement`、维护生产方式（`wonder_final_buildings.yaml` 中按建筑名区分的 `final_maintenance` / `final_attributes`），以及“直接建造入口”（目前只有风格 3 和独特奇观的成品带有 `country_potential = { has_global_variable = tv_engineering_department_direct_build }`）。合并后这些字段改为按机制给一个值；直接建造入口必须放在唯一成品上，否则调试直接建造功能会消失。11 个机制的非效果字段存在差异，合并规则见 D08。

  以 triumphal_axis 为例，现状是三个效果完全相同的建筑：

  | 建筑 | category | pop_type | 直接建造入口 | modifier |
  |---|---|---|---|---|
  | `tv_wonder_sun_king_axis` | government | nobles | 无 | 相同 |
  | `tv_wonder_military_city` | military | nobles | 无 | 相同 |
  | `tv_wonder_civic_capital` | government | burghers | 有 | 相同 |

  重写后只保留一个（按 D08 推荐，沿用风格 1 的键与属性，加上直接建造入口），另外两个删除：

  ```
  tv_wonder_sun_king_axis = {
    pop_type = nobles
    category = government_category
    rural_settlement = no
    country_potential = { has_global_variable = tv_engineering_department_direct_build }
    ...
    modifier = {
        local_cultural_tradition = 0.5        # 所有成品共有，本地，按级
        local_cultural_influence = 0.5        # 同上
        local_crown_estate_power = 0.5        # final_local，本地直接生效，按级
        monthly_political_influence = 0.05    # 国家级，仅显示；实际由 tv_wonder_auto_triumphal_axis 生效
        # monthly_towards_centralization 删除：价值观改由仪式的合并 modifier 提供
    }
    possible_production_methods = { tv_wonder_axis_monument_maintenance }
  }
  ```

  `tv_wonder_auto_triumphal_axis` 只删除 `monthly_towards_centralization`，保留 `monthly_political_influence = 0.05` 和 `scales_with`。如果完成了“凯旋中轴·风格 1”的仪式，国家另外获得 `tv_wonder_triumphal_axis_ritual_1_modifier`（`subject_income_modifier = 0.2` 加上该风格的 `monthly_towards_*`）。这个 modifier 由仪式状态授予和撤销，与建筑等级无关。
- 删除 `tv_wonder_<key>_ritual_annex` 附属建筑（D06；56 个通用 + 法罗斯 1 个，共 57 个），以及它们的价格 `tv_wonder_ritual_annex_{small,medium,large}_price`、对应的 `*_price_cost_modifier` modifier 类型与图标，以及显示 modifier。

### 4.4 文本

| 文本 | 键（建议） | 来源 |
|---|---|---|
| 通用风格名称 | `TV_WONDER_RITUAL_<KEY>_<N>_NAME` | 迁移现有 `TV_ENGINEERING_CEREMONY_<BUILDING>_BUTTON`（现有文本按建筑名取键，单一建筑后必须改为按风格取键） |
| 通用风格说明 | `TV_WONDER_RITUAL_<KEY>_<N>_DESC` | 迁移现有 `.500.d_<x>_<n>` 的首句，或新写（D03） |
| 独特风格 1 名称 | 同上，`<KEY>` 为独特键 | 迁移现有 `game_concept_tv_wonder_display_<id>_ritual_1` 的源文本 |
| 独特风格 1 说明，风格 2、3 名称与说明 | 同上 | 已写好（D03），见 [`../../data/unique_wonders.yaml`](../../data/unique_wonders.yaml)，WP1 并入 `ritual_text` 后删除该草稿 |
| 合并 modifier 名称 | `STATIC_MODIFIER_NAME_tv_wonder_<key>_ritual_<n>_modifier` | 与风格名称一致 |
| 地点 modifier 名称 | `STATIC_MODIFIER_NAME_tv_wonder_<key>_ritual_<n>_location_modifier` | 同上 |
| 落成描述 | `tv_engineering_department.500.d_<x>_<n>`、新增 `.500.d_<x>_plain` | 通用沿用现有 3 段；朴素用一段共享文本；独特风格 2、3 新写 |

所有 YAML 仍需 UTF-8 BOM 和直引号。GUI 中路由风格名称时继续使用数字 id（`tv_wonder_display_<id>_ritual_<n>` 概念），不得拼接 flag 名。

### 4.5 新增 `data/wonder_ritual_rules.yaml`（数值单一来源）

```yaml
ritual_rules:
  duration_months: 24                                         # D09：统一 24 个月
  cost: { catalog: country_reward, type: scaled_gold, value: { small: 2, medium: 3, large: 5 } }  # D09
  societal_value:
    shock: 20        # change_societal_value 一次性；通用与独特相同，不随等级变化（D11 已定）
    monthly: 0.1     # 合并 modifier 中的 monthly_towards_<dir>（D11 已定）
  memory_years: 100
  estate_satisfaction: { support: 0.10, oppose: -0.05 }   # 举行仪式时结算（D17 时机已定，数值待定）
  reritual_prestige: 10
```

生成器、编辑器预览和图鉴都只从这里读取数值。

### 4.6 新增 `data/wonder_societal_axes.yaml`（校验用目录）

列出 17 条原版轴、左右端点、`monthly_towards_<端点>` 名、左负右正的符号、时代或 `allow` 限制，以及左右图标路径（`gfx/interface/icons/societal_values/<axis>_left.dds` / `_right.dds`，游戏中已核实存在）。由脚本从 `reference_game_files/game/in_game/common/societal_values/00_default.txt` 抽取，人工确认后提交。

## 5. Python 归一化层

在 `scripts_engineering_department/wonder_mechanics/_core.py` 中：

- 删除 `ritual_plan_for_style()`、`ceremony_styles()`、`unique_ritual()`、`normalize_unique_ritual()`、`normalize_unique_ceremony()`、`_validate_ceremony*`、`ceremony_modifier_for_style()`、`persistent_ritual_country_modifier_name()`、`ritual_blessing/burden_modifier_name()`、`ritual_auxiliary_*`、`RITUAL_AUXILIARY_ESTATE_POWER_BY_POP_TYPE`、`WONDER_RITUAL_COST_TYPE_IDS`，以及 timed / auxiliary_building / immediate 三种 mode 的相关常量。
- 新增：

```python
def ritual_styles(wonder, mechanics) -> list[dict]:
    """恰好返回 3 项，style 依次为 1/2/3。独特奇观经由 mechanic_key 继承。"""
    # 每项：
    # {
    #   "style": n, "ritual_id": wonder_id*100+n,
    #   "modifier": "tv_wonder_<key>_ritual_<n>_modifier",
    #   "location_modifier": "tv_wonder_<key>_ritual_<n>_location_modifier" | None,
    #   "country_modifier": {...},            # 奖励 + monthly_towards_<dir>
    #   "location_modifier_values": {...},    # 可能为空
    #   "one_shot": [...],
    #   "societal_value": {"axis", "direction", "sign", "shock", "monthly"},
    #   "estate_preferences": {estate: n | "random"},   # 已加入地点奖励所属阶层
    #   "name_key", "desc_key", "final_desc_key",
    # }

def final_building(wonder) -> str
def location_reward_estate(wonder) -> str | None   # pop_type → 阶层，soldiers 的归属见 D18
def ritual_rules(mechanics) -> dict
```

- 价值观数值在这一层注入 `country_modifier`：`monthly_towards_<direction> = rules.monthly`。这就是 R3 要求的“buff modifier 与价值观 modifier 合并”：每个 (奇观, 风格) 只有一个国家 modifier。
- 校验：§4.1 的全部字段规则；独特奇观的 `ritual_text` 三项齐全；`wonder_base_modifiers.yaml` 中不得再出现 `monthly_towards_*`（删除 56 条后，旧规则“small 只能有倾向类基础 modifier”应改为“small 不得有基础国家 modifier”）；同一 `base_key` 下方向组合重复只输出报告，不报错。
- `naming.py`、`rituals.py`、`schema.py`、`io.py` 中的重新导出要同步更新，否则编辑器和图鉴会在导入时就报错。

## 6. 仪式状态生命周期（运行时）

### 6.1 生成的静态 modifier

由 `in_game/common/static_modifiers/gen_tv_engineering_department_wonder_mechanics_modifiers.py` 生成：

- `tv_wonder_<key>_ritual_<n>_modifier`：`game_data = { category = country }`，内容为奖励 `country_modifier` 加上 `monthly_towards_<dir>`。191 × 3 = 573 个（56 个通用 + 135 个独特）。
- `tv_wonder_<key>_ritual_<n>_location_modifier`：只为带 `location_modifier` 的风格生成（本轮为每个机制的风格 2，共 191 个）。是否保留 +0.5 地方阶层权力见 D07。
- 删除：`_ritual_blessing_modifier`、`_ritual_burden_modifier`、`_ceremony_modifier`、圣索菲亚的游行 modifier、`tv_wonder_ceremony_cost_{country,local}_modifier_*`、附属建筑显示 modifier。

### 6.2 地点变量

| 名称 | 作用域 | 键 | 值 | 写入者 |
|---|---|---|---|---|
| `tv_wonder_ritual_style_by_id` | 地点 | wonder id | 1/2/3 | 仅 grant / revoke |
| `tv_wonder_ritual_memory_by_id` | 地点 | wonder id | 1，带 `days = 36500` 时限 | 仅 grant |

写 map 时沿用项目现有做法：键用生成的整数字面量，先删除再写入，不把迭代器 scope 直接当右值（`variable_map` 必读规则）。

### 6.3 生成的效果（每个奇观一组）

全部由 `gen_tv_engineering_department_wonder_mechanics_effects.py` 的新函数 `append_ritual_state_effects()` 生成，输出到新文件 `tv_wonder_ritual_state_effects.txt`（需在 `data/generated_files.yaml` 中登记）。

```
# 地点作用域；调用方保证 owner 存在，且此地点有该奇观的最终建筑
tv_wonder_<key>_ritual_<n>_grant_effect = {
    remove_from_variable_map = { name = tv_wonder_ritual_style_by_id key = <id> }
    add_to_variable_map = { name = tv_wonder_ritual_style_by_id key = <id> value = <n> }
    remove_from_variable_map = { name = tv_wonder_ritual_memory_by_id key = <id> }
    add_to_variable_map = { name = tv_wonder_ritual_memory_by_id key = <id> value = 1 days = 36500 }
    trigger_event_silently = { id = tv_engineering_department.<3000+id> days = 36501 }
    add_location_modifier = { modifier = tv_wonder_<key>_ritual_<n>_location_modifier years = -1 mode = replace }   # 仅当有地点奖励
    owner = { add_country_modifier = { modifier = tv_wonder_<key>_ritual_<n>_modifier years = -1 mode = replace } }
}

# 地点作用域；读取当前风格并逐支撤销；$loser$ 由调用方保存为 scope（易主时是旧主，否则是 owner）
tv_wonder_<key>_ritual_revoke_effect = {
    if = { limit = { 当前 map 值 = 1 } remove_location_modifier = ..._1_location_modifier }
    else_if = ... 2 / 3
    remove_from_variable_map = { name = tv_wonder_ritual_style_by_id key = <id> }
    remove_from_variable_map = { name = tv_wonder_ritual_memory_by_id key = <id> }
    scope:tv_wonder_ritual_sync_country ?= { tv_wonder_<key>_ritual_sync_country_effect = yes }
}

# 国家作用域：按不变量 1 加减 3 个 modifier；一次只看一个 wonder id 的 3 个风格
tv_wonder_<key>_ritual_sync_country_effect = {
    if = { limit = { any_owned_location = { <map 值 = 1> } } add_country_modifier = { ..._1_modifier years = -1 mode = replace } }
    else = { remove_country_modifier = ..._1_modifier }
    ... 2 / 3
}

# 国家作用域；只在仪式完成那一刻调用一次
tv_wonder_<key>_ritual_<n>_settle_effect = {
    change_societal_value = { type = <axis> value = <±shock> }
    # 阶层满意度不在这里：它在举行仪式（确认）时结算，见 §7.2、§9.3
    <one_shot 奖励行，沿用 cost_reward_units 目录的渲染器>
}
```

要点：

- 独特奇观只有一个固定地点，`sync_country_effect` 可以直接判断那个地点。通用奇观要遍历 `any_owned_location`，但只在生命周期点执行，不放在 GUI 或月度读取路径上。
- 同类型、同风格的多个实例只对应一个 modifier，不叠加（D36）。撤销其中一个时，`sync` 会保留 modifier，直到最后一个实例消失。
- grant 中的 `add_country_modifier years = -1` 会在落成选项的 tooltip 里显示为“永久”，满足 R4 的“授予时显示为永久”。100 年计时完全不在界面上显示（D29）。

### 6.4 100 年淡忘

- 计时器是生成的隐藏地点事件 `tv_engineering_department.<3000+id>`（`type = location_event`，`hidden = yes`）。grant 时从地点发出，延迟 36501 天。
- 事件 `immediate` 中：如果此地点 `tv_wonder_ritual_style_by_id` 有该 id，**并且** `tv_wonder_ritual_memory_by_id` 中已经没有该 id（记忆时限已到），则把 owner 存为 `scope:tv_wonder_ritual_sync_country`，调用 revoke，再对 owner 触发可见的国家事件 `tv_engineering_department.2010`（“<奇观>的<仪式>已被淡忘”，通过 saved scope 传入地点）。
- 用记忆 map 做令牌：如果这期间状态曾被清除又重新授予，新的 grant 会把记忆时限重置为 100 年，旧计时器到期时看到记忆仍在，就什么也不做；新计时器会在新的 100 年后到期。这样不需要存日期，也不需要取消已排队的事件。
- 记忆时限（36500 天）比事件延迟（36501 天）少一天，避免同日结算的先后顺序问题。日历天数和 location_event 读档后是否保留，列为引擎验证项 M02 / M03。
- 淡忘事件只是通知，没有惩罚（D30）。之后该奇观处于朴素状态，可以重新仪式化。

### 6.5 生命周期接线

| 生命周期点 | 现有入口 | 改动 |
|---|---|---|
| 易主 | `tv_wonder_ownership_handle_location_owner_changed_effect`（`gen_tv_wonder_ownership_effects.py`） | 在旧主清理之前，对此地点上有仪式状态的每个奇观调用 revoke，sync 目标为 `scope:loser`。删除 `tv_wonder_ownership_cleanup_loss_effect`（`append_loss_cleanup_effect`）中移除仪式 modifier 和 `tv_wonder_unique_ritual_completed` 的分支（改由 sync 负责）；`tv_wonder_ownership_compute_loss_retains_same_wonder_effect` 只用于计算“保留同类”标志，如果不再有其他用途，一并删除。新主不做任何仪式相关的事。“保留／劫掠”事件不变 |
| 拆毁 / 降到 0 | `tv_wonder_<key>_handle_final_building_level_changed_effect`（`append_final_building_level_changed_effects`） | 最终建筑不存在时调用 revoke（sync 目标为 owner），替换现有按 wonder id 保留 modifier 的逻辑和 `tv_wonder_unique_ritual_completed` 的删除 |
| 降级（仍 ≥1） | 同上 | 不改变状态 |
| 100 年到期 | 新事件 `.3000+id` | 见 §6.4 |
| 正常落成 | `.5000+id` 选项 | 结果为风格 n 时：建造或升级成品 → grant → settle |
| 重新仪式化落成 | 新事件 `.4000+id` | grant → settle → +10 威望 |
| 开局 | `tv_wonder_initialize_existing_unique_wonders_effect` | 只把建筑键改为单一成品；不写仪式状态（朴素） |
| 外部升降级 | `gen_tv_wonder_level_change_effects.py` | 删除 `tv_wonder_raise_generic_level_effect` 的 `style` 参数（原版接管目前并不调用它，只有定义和 `test_wonder_mechanics_rules.py` 引用；同步修改 `Wonder_Level_Change_Interface.md`）；`vanilla_takeover/render.py` 的 `final_dispatch()` 改用 `final_building()`。建出来的一律是朴素；降到 0 时走上面的拆毁路径 |

删除：国家 map `tv_wonder_unique_ritual_completed`，全局 map `tv_wonder_final_building_type_to_ritual_style`、`tv_wonder_id_to_style_{1,2,3}_final_building_type`，`tv_wonder_ritual_key_to_id` 以及 `tv_wonder_ritual_id_to_*` 系列 map（模式、费用类型、监听器）。

## 7. 仪式阶段流程（项目内）

### 7.1 建设结束（`tv_wonder_finish_construction_effect`）

- 保留：`stage = 4`、国内支持度 +20、移除施工地点 modifier。
- 删除 `tv_wonder_initialize_ceremony_runtime_state_effect` 本身（不再强制独特奇观选风格 1，也不再自动开始 8 阶段），以及它的全部调用点：`finish_construction`、`tv_wonder_initialize_building_state_light_effect`、`tv_wonder_reinitialize_building_state_core_effect`，以及主 mod 的重新初始化动作 `src/in_game/common/generic_actions/tv_reinitialize_actions.txt`。重新初始化路径如果处在仪式阶段，改为调用 `tv_wonder_ritual_enter_phase_effect` 的显示缓存刷新部分（不重新掷随机偏好）。
- 新增 `tv_wonder_ritual_enter_phase_effect`：
  - 如果此地点已经是完整状态（扩建模式 2）：直接调用 `tv_wonder_finalize_effect`，结果记为“沿用”（D22）。
  - 否则：清空 `tv_wonder_ritual_choice`，按 §9.3 掷出随机阶层偏好，刷新仪式显示缓存（§13.2）。
- `.202` 事件文本改写（§11）。

### 7.2 玩家操作（stage 4，`tv_wonder_ritual_in_progress` 未设置）

| 动作（generic action） | 条件 | 效果 |
|---|---|---|
| `tv_wonder_ritual_preview_1/2/3` | 仪式阶段，尚未确认 | 设置 `tv_wonder_ritual_choice = n`，刷新预览缓存。可以任意切换 |
| `tv_wonder_ritual_confirm` | 已选 n；付得起费用 | 支付 `price:tv_wonder_ritual_<size>_price`（scaled gold，D09），调用 `tv_wonder_ritual_settle_estates_effect = { style = n }` 结算阶层满意度（§9.3），设置 `tv_wonder_ritual_in_progress`、`tv_wonder_ritual_months_completed = 0`、`tv_wonder_ritual_duration_months`。CMM“跳过仪式”打开时，免费并立即完成（D31） |
| `tv_wonder_ritual_choose_plain` | 仪式阶段，尚未确认，且项目模式 ≠ 3 | 所有参与阶层加 `oppose`（D16，§9.3），结果 = 朴素，调用 `tv_wonder_finalize_effect` |
| `tv_wonder_ritual_cancel_reritual` | 项目模式 3，尚未确认 | 清理项目并回到构思，没有惩罚（D26） |

`tv_wonder_choose_ceremony_style_*`、`tv_wonder_confirm_ceremony*`、`tv_wonder_hagia_assign_step_*` 全部删除。现有动作价格文件中，ritual annex 和风格 3 的价格条目同样删除，改为新增 `tv_wonder_ritual_{small,medium,large}_price`（按照风险卡，`common/prices/` 只能写静态数值）。

### 7.3 仪式进行中

- 月度 pulse `tv_engineering_department_ritual_monthly_pulse` 保留名称，主体换成 `tv_wonder_ritual_monthly_effect`：月数 +1，更新 `tv_wonder_ritual_progress_pct`，到达 `duration_months` 时调用 `tv_wonder_ritual_complete_effect`。
- 删除 ruler death、pre-winning war、ending war 三个仪式监听器，以及它们在 `data/pulse_registry.yaml` 中的登记。
- 进行中没有 burden modifier，也没有阶段事件（D10）。
- 确认之后不能更改风格。放弃仪式只能走项目放弃（§7.7）。

### 7.4 落成（正常项目，模式 1 / 2）

- `tv_wonder_finalize_effect` 保留结构，把条件 `tv_wonder_has_selected_ceremony_trigger` 改为 `tv_wonder_ritual_outcome_ready_trigger`（已选朴素，或者仪式已完成，或者模式 2 沿用完整状态）。结果写入 `tv_wonder_finalization_outcome`：0 = 朴素，1–3 = 风格，9 = 沿用完整状态。
- `.5000+id` 事件，每个奇观一个，不再按风格区分：
  - 描述：`triggered_desc` 按结果选 `.500.d_<x>_plain` 或 `.500.d_<x>_<n>`；结果为 9 时使用扩建描述。
  - 选项：`tv_wonder_<key>_construct_final_building_effect`（单一成品，取代 `_style_N_` 版本）→ `tv_wonder_apply_finalization_visible_rewards_effect`（落成奖励包，朴素同样获得，见 D15）→ 结果为 1–3 时执行 `tv_wonder_ritual_apply_choice_effect`（即依次执行 site 上的 `tv_wonder_<key>_ritual_<n>_grant_effect` 和 `tv_wonder_<key>_ritual_<n>_settle_effect`；仪式卡的效果预览渲染的也是这个效果，见 §13.1）→ 隐藏事件 `.6999`。
  - 按风险卡要求，重型工作放在隐藏事件的 `immediate` 中。grant 和 settle 写状态、加 modifier，选项 tooltip 需要显示它们，所以放在选项里，但都是常数开销（一个 wonder id 的 3 个分支），不遍历全世界。
- 广播事件 `.6000+id` 只在模式 1 时发出。

### 7.5 扩建（模式 2）

- 成品为完整状态：建设结束后直接落成，状态和 modifier 保持不变，没有新的冲击或阶层结算。落成奖励包照旧发放（与现有“每次扩建都能领取落成奖励”的设计一致）。
- 成品为朴素状态：进入和新建项目一样的选择（D23）。在仪式期间，成品维持原等级，主体建在旁边；落成时升级成品并销毁主体（现有逻辑）。
- 删除 `tv_wonder_detect_existing_wonder_at_saved_site_effect` 中写 `tv_wonder_ceremony_style` / `ceremony_locked` 的部分，以及“扩建锁定风格”的提示文本 `TV_ENGINEERING_CEREMONY_LOCKED_BY_EXPANSION_TEXT`。

### 7.6 空壳续建

- 修改 `tv_wonder_can_finish_construction_trigger`：在现有“`tv_wonder_level > tv_wonder_project_base_level`”之外，再允许“站点上没有该奇观的最终建筑，且 `tv_wonder_level >= 1`”（D20）。这样续建一个空壳时，玩家可以在锁定站点后立刻宣布建成进入仪式阶段，也可以先多建几级。
- 连带影响：`tv_engineering_department_support_resolution_monthly_pulse` 在支持度归零时也会调用 `can_finish_construction` 自动宣布建成，放宽后，续建空壳的项目在支持度归零时会直接进入仪式阶段，这与空壳的定义一致。AI 的 `tv_wonder_ai_can_finish_construction_trigger`（`ai_triggers.txt`）要求“基础等级 + 2”，必须同步加入空壳分支，否则 AI 续建空壳时永远不会宣布建成。
- 空壳既然算续建，就继续使用现有的候选模式 1（`tv_wonder_set_current_project_priority_candidate_mode_effect` 无需修改）。只需把续建提案文本“完成造了一半的 xx”扩展出空壳专用的一句：“xx 已经完工，但仍是一座未经落成的空壳”。

### 7.7 中止

- 现有“放弃项目”在仪式阶段仍可用，惩罚不变。空壳留在原地；如果是模式 3，奇观仍是朴素。是否新增一个“搁置仪式”的无惩罚出口，见 D21。
- 由于仪式阶段不再扣支持度，`tv_engineering_department_support_resolution_monthly_pulse` 必须在 `stage = 4` 时直接跳过，不再触发 `.20` 项目崩溃。

## 8. 重新仪式化（R8）

### 8.1 朴素奇观缓存（月度脉冲）

决议的 `allow` 会在 tooltip 和决议面板中反复求值，选择事件的选项 `trigger` 也会在渲染时求值。因此这些地方**不得遍历拥有的地点**，只能读取国家变量。遍历只放在月度脉冲中进行，而且不新增一次遍历：现有的 `tv_engineering_department_wonder_auto_cache_monthly_pulse` → `tv_wonder_mechanics_refresh_country_auto_level_map_effect` 每月已经对拥有地点的 `tv_wonder_final_building_level_by_type` 逐键走一遍，并在局部变量中拿到 wonder id 和等级。只需在同一个循环里多做一次判断：

```
# 刷新开始时
clear_variable_map = tv_wonder_plain_level_by_wonder_id
remove_variable = tv_wonder_has_plain_wonder
...
# 在现有的“每个成品键”分支内（地点 scope 已存为 scope:tv_wonder_auto_cache_location）
if = {
    limit = {
        scope:tv_wonder_auto_cache_location = {
            NOT = { is_key_in_variable_map = { name = tv_wonder_ritual_style_by_id target = local_var:tv_wonder_auto_cache_wonder_id } }
        }
    }
    # 与 auto level map 相同的“保留最大等级”写法，写入 tv_wonder_plain_level_by_wonder_id
    set_variable = { name = tv_wonder_has_plain_wonder value = 1 }
}
```

- 缓存内容：国家变量 map `tv_wonder_plain_level_by_wonder_id`（键为 wonder id，值为该类型朴素实例中的最高等级，只存数字，不存 scope），以及标量 `tv_wonder_has_plain_wonder`。
- 增量补充（只增不减，开销都是常数）：朴素落成（§7.4 结果为 0）和淡忘（§6.4）时，直接对当前国家写入对应的键。授予、易主、拆毁不做增量删除，等月度重建；可能残留的过期条目由 §8.3 的锁定事件重新校验。
- 实现契约：只更新已知 wonder id，并保留该键的较大等级，不得用较低等级覆盖其他朴素实例的最高值。落成使用尚未清除的项目等级，同时增量更新全国基础效果等级缓存；淡忘只在当前地点检查该成品的 6 个等级分支，再补入当前 owner 的朴素缓存。两处均不调用整表重建；重新仪式化收尾也不为删除缓存而重建。这里的“常数”仅指缓存补充，不包括通用奇观 revoke 原有的国家 modifier 去重查询。
- 时效：缓存最多滞后一个月。新出现的朴素奇观通常靠增量补充立即可见；失去的奇观在锁定时被拦下，不会锁错。
- AI（§12 第 4 条）同样只读取这个缓存。
- 写法与 `variable_map` 必读规则一致：键使用已经存好的局部变量，先删除再写入。

### 8.2 决议

新文件 `src/in_game/common/decisions/tv_engineering_department_decisions.txt`（手写）：

```
tv_wonder_reritualize_decision = {
    decision_category = <D33>
    potential = { has_variable = tv_engineering_department_member }
    allow = {
        var:tv_wonder_stage ?= 0
        has_variable = tv_wonder_concept_in_progress      # 严格的构思状态（D38）
        custom_tooltip = {
            text = TV_WONDER_RERITUAL_HAS_PLAIN_TT
            has_variable = tv_wonder_has_plain_wonder      # 只读缓存，不遍历
        }
    }
    ai_will_do = { value = 0 }      # AI 由 ED 驱动器处理（§12）
    option = {
        name = tv_wonder_reritualize_decision.a
        effect = { trigger_event_non_silently = tv_engineering_department.2001 }
    }
}
```

### 8.3 选择事件 `.2001` 与锁定事件 `.2002`

- `.2001` 由生成器生成，每个 wonder id 一个选项（D27 推荐方案 A）。选项 `trigger` 只读缓存：`is_key_in_variable_map = { name = tv_wonder_plain_level_by_wonder_id target = <id> }`。选项名使用奇观名；等级从缓存读取后显示在选项说明中。独特奇观的地点固定，选项说明可以直接写出地点名；通用奇观只显示“最高等级为 N 的一座”。
- 末尾固定一个“暂不”选项，无效果。
- 选项效果只做两件事：设置 `tv_wonder_reritual_pending_id = <id>`，然后触发隐藏事件 `.2002`（`days = 0`）。tooltip 用 `custom_tooltip` 说明“锁定这座奇观并进入仪式阶段”，不在选项里执行查找，也不执行锁定（风险卡要求：选项 `hidden_effect` 保持轻量，重活放进隐藏事件的 `immediate`）。
- `.2002` 的 `immediate`（`tv_wonder_reritual_lock_effect`），按 pending id 分支生成：
  1. 找到地点。独特奇观：`location:<固定地点>`，校验仍归本国所有、有成品、没有仪式状态。通用奇观：`ordered_owned_location`，筛选条件为该类型成品等级 ≥ 1 且没有仪式状态，按成品等级降序取第一个。这是唯一需要遍历地点的步骤，只在玩家点击后执行一次，且只检查一个 wonder id。
  2. 找不到（缓存已过期）时：从缓存中删除该键，触发通知事件 `.2003`（“这座奇观已不再符合条件”），构思状态保持不变。
  3. 找到时：将地点存为 `scope:tv_wonder_reritual_site`；设置 `tv_wonder_locked = <id>`、`tv_wonder_site`、`tv_wonder_project_mode = 3`、`tv_wonder_construction_complete = 1`、`tv_wonder_stage = 4`；结束构思：清掉 `tv_wonder_concept_in_progress`，不保存构思进度（D28：完成后构思从头开始）；最后调用 `tv_wonder_index_refresh_country_cache_effect` 和 `tv_wonder_ritual_enter_phase_effect`。
  4. 删除 `tv_wonder_reritual_pending_id`。
- 模式 3 在仪式阶段的界面里不显示“朴素”按钮，改为显示“取消重新仪式化”。

### 8.4 专用落成 `.4000+id`

- `tv_wonder_ritual_complete_effect` 在模式 3 时不调用 `tv_wonder_finalize_effect`，而是触发 `.4000+id`。
- 选项：执行 `tv_wonder_ritual_apply_choice_effect`（模式 3 下即 grant → settle → `add_prestige = 10`，与仪式卡预览相同）。没有落成奖励包，不建造或升级建筑，没有广播，也不注册优先候选。
- 隐藏收尾：`tv_wonder_clear_project_state_core_effect` → `tv_wonder_start_concept_effect = { reason = 4 }`（新的 reason，用于提示“重新仪式化已完成”）。构思从零开始（D28）。
- 即时奖励是否属于这里所说的“buff”，见 D25。

## 9. 阶层意愿（R9）

### 9.1 术语

EU5 中阶层的数值叫**满意度**（satisfaction，`add_estate_satisfaction`，0–1）。“忠诚度”在原版中指附庸。界面使用“满意度”，与原版保持一致。

### 9.2 偏好来源（按优先级）

1. **地点奖励所属阶层**：奇观 `pop_type` 对应的阶层，总是支持带 `location_modifier` 的那个风格。映射为 clergy → clergy_estate，nobles → nobles_estate，burghers → burghers_estate，laborers → peasants_estate，soldiers → 待定（D18，推荐 peasants_estate，与原版 `pop_types` 一致）。由生成器推导，不在数据里填写。如果某机制有不止一个风格带地点奖励（将来允许的组合），校验器会要求作者在 `estate_preferences` 中为该阶层明确指定。
2. **硬编码偏好**：`estate_preferences` 中写死 1/2/3 的阶层，依据是风格的历史主题（例如宫廷献祭 → 贵族，商人行会 → 市民，边地军屯 → 哥萨克）。
3. **`random`**：逻辑上没有明显偏好的阶层，在每次进入仪式阶段时随机选一个风格。

7 个原版阶层（含 dhimmi、tribes、cossacks）都按这套优先级处理，数据必须逐一给出。现有奇观的 `pop_type` 只有 clergy / nobles / burghers / laborers / soldiers 五种，所以第 1 条不会落到 dhimmi、tribes、cossacks 上；这三个阶层只能走第 2、3 条。

**只有国家实际拥有的阶层才参与**（`country_has_estate = estate_type:<x>`）。不拥有的阶层不掷偏好、不在界面显示、不参与结算。“不存在中立”只针对参与的阶层。

独特奇观继承所属机制的偏好。

### 9.3 运行时

- `tv_wonder_ritual_enter_phase_effect` 只为 `country_has_estate` 为真的阶层写入国家变量 `tv_wonder_estate_pref_<estate>`（1–3），不拥有的阶层不写。固定偏好直接写值；`random` 用 `random_list` 在 1/2/3 中均匀抽取。偏好在本次仪式阶段内保持不变。界面中每个阶层的显示条件就是该变量是否已设置（`GetVariable(...).IsSet`），因此不拥有的阶层自动隐藏，GUI 不需要自己判断阶层是否存在。
- 结算 `tv_wonder_ritual_settle_estates_effect = { style = n }`（手写，国家作用域）：对每个**同时满足**“`country_has_estate` 为真”和“`tv_wonder_estate_pref_<estate>` 已设置”的阶层，偏好等于 n 的加 `support`，否则加 `oppose`（数值见 D17）。没有中立。
- 结算时机：**举行仪式（确认）时**（D17 已定），由 `tv_wonder_ritual_confirm` 在扣费之后调用。结算发生在仪式进入计时之前，所以界面预览与实际结算总是一致；仪式期间获得或失去阶层不再影响结算。确认后中止仪式（项目放弃、重新仪式化取消）不退回满意度变化，与费用不退一致。CMM“跳过仪式”同样在确认时结算。
- 阶层满意度因此不属于完成效果，不出现在仪式卡的效果区；它显示在“举行仪式”按钮的原生动作 tooltip（`UIAction.GetEffects`）中，与费用并列。
- 朴素（D16）：玩家执行 `tv_wonder_ritual_choose_plain` 时，所有同时满足“`country_has_estate` 为真”和“偏好变量已设置”的阶层一律加 `oppose`，没有支持者。效果为 `tv_wonder_ritual_settle_estates_plain_effect`，显示在“以朴素方式落成”按钮的原生动作 tooltip 中。开局历史奇观、外部接口建出、淡忘后回到朴素，这些都不是玩家的选择，不结算。
- 偏好变量在项目清理时删除（加进 `tv_wonder_clear_project_state_core_effect`）。

## 10. 价值观（R3）

- **一次性移动**：settle 中执行 `change_societal_value = { type = <axis> value = <±20> }`，左端取负，右端取正。通用与独特相同，不随等级变化（D11）。
- **永久倾向数值**：`monthly_towards_<direction> = 0.1`，通用与独特相同（D11）。它并入全国净月度推力；单独看，它让该方向的推进上限增加 10 点（100 × 0.1）。
- **永久倾向**：合并 modifier 中的 `monthly_towards_<direction>`。它随仪式状态同步：失去奇观、淡忘、易主时都会消失。
- **取消**：十年纪念期，以及 `wonder_base_modifiers.yaml` 中全部 56 条 `monthly_towards_*`。删除后，基础国家表为空的机制（27 个基础模板只含倾向，删除后为空，影响 91 个工程类型：27 个通用 + 64 个独特，其中包括全部 24 个 small）在界面上显示“无基础国家效果”，不要为了填空塞别的东西进去。
- **轴的可用性**：允许全部 17 条轴，不做特殊处理（D12）。没有 `has_societal_value` 禁用判断，也没有“至少两种风格可选”的校验。时代轴尚未出现时，该风格的一次性移动和月度倾向对国家暂时无效，玩家看到的就是一个“不带价值观”的风格；进入相应时代后，modifier 中的月度倾向自然生效。仪式 100 年后淡忘，可以重选。AI 对齐度（§12）对尚未出现的轴取 0。
- **AI 与 tooltip**：`change_societal_value` 和 modifier 的 tooltip 由引擎生成，界面不手写数值。

## 11. 国内支持度（R5）

- `international_organizations/tv_engineering_department.txt`，`tv_wonder_domestic_support` 的 `monthly_change`：在 `limit` 里的 `leader_country ?= { ... }` 块**内部**加入 `NOT = { var:tv_wonder_stage ?= 4 }`（stage 是国家变量）。描述键 `TV_WONDER_DOMESTIC_SUPPORT_DECAY` 不变。
- `tv_engineering_department_support_resolution_monthly_pulse`：`stage = 4` 时跳过（§7.7）。
- 落成时剩余支持度兑换奖励的规则不变，但支持度现在冻结在进入仪式阶段时的数值。
- `.202` 改写，要点如下（中文为草稿，英文同步撰写）：
  - 标题：“[tv_wonder_construction|E]：工程矗立”（不变）
  - 描述：“……主体已经完工。[tv_wonder_ceremony|e]如今成了这座工程的最后一步，朝中那些反对者再也找不到理由——奇观已经立在那里，再说下去只会显得自己目光短浅。宫廷里那些反对的声音，终于都闭嘴了。\n\n#weak 进入仪式阶段后，国内支持度不再每月下降。你可以选择一种仪式风格，也可以直接以朴素方式落成。#!”
  - 选项“准备仪式吧。”（不变），`.a.tt` 增加一行：“国内支持度在仪式阶段不再流失。”

## 12. AI

在 ED 国家驱动器 `tv_engineering_department_ai_effects.txt` 中替换现有的全部仪式分支：固定选风格 1（规则 10）、免费确认（规则 11）、scaled gold / 威望确认分支（约 362–371 行），以及圣索菲亚指派 `tv_wonder_ai_hagia_assign_effect`（规则 12）。同时删除触发器 `tv_wonder_ai_hagia_candidate_trigger` 和 `tv_wonder_ai_can_afford_ritual_building_trigger`，并从 `generic_action_ai_lists/tv_engineering_department_list.txt` 中移除 6 个旧的选择/确认动作。新规则如下：

1. 进入仪式阶段后，为每个风格计算对齐度：当前该轴的数值归一到 [−1, 1]，与方向符号相乘。数值读取方式需验证（M09）。
2. 选择对齐度最高的风格，同分时取风格编号较小的那个。确定性的规则，不使用随机。
3. 付得起就确认；付不起就等待，等满 24 个月仍付不起则选朴素（模式 3 则取消）。
4. 重新仪式化：AI 处在构思状态、`tv_wonder_has_plain_wonder` 已设置、且月结余能负担费用时，按固定概率启动。从缓存 map 中按等级最高选取 wonder id，写入 `tv_wonder_reritual_pending_id` 后调用与 `.2002` 相同的锁定效果，不通过决议的 `ai_will_do`（D32）。
5. 删除 `.9300–.9307`、圣索菲亚和法罗斯的 `ai_chance` 规则（这些事件都会被删除）。

## 13. 界面

### 13.1 工程部面板：仪式卡

三套独立的设计稿见 [`ai_gui_assessment/mockups/ritual_rework/README.md`](../../ai_gui_assessment/mockups/ritual_rework/README.md)。不论选哪一套，数据契约都相同：

| 显示内容 | 数据来源 |
|---|---|
| 风格名称 / 说明 | 数字路由概念 `tv_wonder_display_<id>_ritual_<n>`（现有机制，键改为按风格） |
| 价值观方向与图标 | 生成的显示变量 `tv_wonder_ritual_display_axis_<n>`（轴编号）和 `_dir_<n>`（±1），图标按编号路由到 `gfx/interface/icons/societal_values/<axis>_<left|right>.dds` |
| 奖励预览 | 原生效果渲染 `ShowScriptedEffectForScope('tv_wonder_ritual_apply_choice_effect', ...)`（按风格时为 `tv_wonder_ritual_apply_style_<n>_effect`），由 `text_multi.raw_text` 接收。被渲染的就是仪式完成时实际执行的效果（grant + settle，模式 3 另加 10 威望）。不手写效果文本，不写只用于 tooltip 的包装效果；grant 中的 map 写入和计时器放进 `hidden_effect`。效果区以外不重复写效果数值 |
| 阶层支持 / 反对 | `tv_wonder_estate_pref_<estate>` 与当前风格比较 |
| 费用、时长 | `price:` 与 `tv_wonder_ritual_duration_months` |
| 进度 | `tv_wonder_ritual_months_completed`、`tv_wonder_ritual_progress_pct` |
| 模式 3 横幅 | `tv_wonder_project_mode = 3` |

删除：生成块 `TV_WONDER_MECHANICS_CEREMONY_STYLE_{1,2,3}_BUTTONS`、`TV_WONDER_MECHANICS_ACTIVE_RITUAL_TEXTS`（含法罗斯、圣索菲亚控件）、`TV_WONDER_MECHANICS_HOLD_BUTTONS`，以及 `tv_wonder_ceremony_cards.gui` 片段和它的合并脚本。新的仪式卡由 `gen_tv_engineering_department_wonder_mechanics_gui.py` 生成一个新的标记块 `TV_WONDER_RITUAL_CARD`，由合并脚本放入面板。

### 13.2 显示缓存

`tv_wonder_ritual_enter_phase_effect` 和 `tv_wonder_ritual_preview_*` 负责刷新显示变量（轴、方向、风格是否带地点奖励、当前对齐度）。GUI 只读变量，不在悬停或渲染路径上重算（`wonder_gui` 风险卡第 6 条）。

### 13.3 地点窗口

`gen_location_window.py` 与 `append_location_display_final_building_projection()`：

- `tv_wonder_display_slot_<k>_ritual_style` 改为读取地点 map `tv_wonder_ritual_style_by_id`（0 = 朴素）。删除“通用奇观一律视为已完成”的分支，修复 §2.2 中的显示 bug。
- 新增空壳投影：主体 ≥1、成品 = 0 时显示“空壳”和主体等级。
- 徽记文本：空壳 / 朴素 / 风格名；tooltip 显示合并 modifier 与地点 modifier 的效果，不显示剩余年限。

### 13.4 百科、图鉴、编辑器

- `gen_tv_encyclopedia_wonders_cards_gui.py`：仪式区改为三种风格，每种显示奖励、价值观方向和阶层偏好。
- `unique_wonders_site/scripts/build/build_wonders.py`：`append_ritual_plan_sections` 改为读取 `ritual_styles()`。
- 编辑器 `great_projects_editor_web/services/wonder/`：`fields.py` 删除 `unique_ritual_editor` 和 `unique_ceremony_editor`，通用风格编辑器改为 `rituals[n].reward.{country_modifier, location_modifier, one_shot}`、`societal_value` 和 `estate_preferences`；新增独特奇观 `ritual_text` 编辑器。`model.py`、`values.py`、`options.py`、`localization.py`、`static/wonder_fields.js`、`static/wonder_values.js` 同步修改。规则表 `wonder_ritual_rules.yaml` 只读显示。

## 14. 删除清单

项目尚未发布，不保留旧 schema、迁移代码或兼容分支。

| 类别 | 删除对象 |
|---|---|
| 数据 | `unique_wonders.yaml` 中的 `ritual` / `ceremony`；`wonder_base_modifiers.yaml` 中的 56 条 `monthly_towards_*`；`wonder_generic_rituals.yaml` 中的 `style_*` 与 `cost_type`；多余的最终建筑名及其属性 |
| 生成器 | `wonder_ceremony_lib.py`、`gen_tv_wonder_ceremony_effects.py`、`gen_tv_wonder_ceremony_events.py`、`gen_tv_wonder_ceremony_cards_gui.py` 与合并脚本、`gen_tv_wonder_ceremony_options.py`、`gen_tv_wonder_ceremony_l_{english,simp_chinese}.py`、`gen_tv_wonder_ceremony_cost_{country,local}_modifiers.py`、`merge_ceremony_cost_options.py`、`gen_tv_ceremony_font_icons_gui.py`（如果只服务于阶段卡）、附属建筑 modifier 生成器；`append_ritual_effects()` 中 timed、auxiliary、immediate、skip、listener 的分支 |
| 专属仪式 | `gen_unique_wonder_rituals.py`、`unique_wonder_ritual_content/{pharos,hagia}.py` 及其生成物（D04 已定：退役） |
| 独特仪式设计数据 | `unique_wonder_ritual_{specs,designs,designs_zh,design_matrix,archetypes,capabilities,codegen_templates,feasibility,prompts}.yaml` 及其 harness、审计脚本、编辑器设计浏览器（D05 决定删除还是归档） |
| 运行时 | 风格选择与确认动作、圣索菲亚步骤动作、三个仪式监听器、`tv_wonder_unique_ritual_completed`、风格相关全局 map、`tv_wonder_ceremony_*` 变量、`.9300–.9307`、`.6301–.6308`、`.7300–.7308` |
| 外围接线 | CMM“跳过仪式”设置的旧描述（`tv_engineering_department_cmm_effects.txt` 约 244–306 行与 `tv_engineering_department_cmm_l_*.yml`，按 D31 重写而非删除）；首席提醒 `tv_engineering_department_ceremony_style_alert_trigger`（`tv_engineering_department_chief_alert_trigger.txt`）及 `chief_alert_effects.txt` 中对应分支和 11 种语言的提醒文本（改为“仪式阶段待选择”）；`scripts/gen_messagetypes.py` 中 `PERFORM_tv_wonder_choose/confirm_ceremony*` 与圣索菲亚控件的消息类型；`generic_action_ai_lists/tv_engineering_department_list.txt` 中的旧动作；modifier 类型与图标中 `tv_wonder_ritual_annex_*_price_cost_modifier`、`tv_wonder_ritual_style_3_*_price_cost_modifier`（换成新价格对应的条目） |
| 旧生成物 | `gen_tv_wonder_ritual_effects.py` 与 `tv_wonder_ritual_effects.txt`（由新的状态与流程生成器取代，更新 `data/generated_files.yaml`）；`on_action/tv_engineering_department_pulse_bridges.txt`（由 `pulse_registry.yaml` 重新生成）；`tv_engineering_department_on_action.txt` 约 267–329 行的监听器 pulse 主体；索引缓存变量 `tv_wonder_selected_ritual_*`（`gen_tv_wonder_index_effects.py` 约 54–86 行，面板 GUI 也在读取） |
| 独特仪式工具脚本 | `translate_unique_wonder_ritual_designs_google.py`、`gen_unique_wonder_ritual_specs.py`、`allocate_unique_wonder_ritual_event_ids.py`、`wonder_unique_ritual_harness.py`、`audit_unique_wonder_ritual_*.py`（随 D05） |
| 修复残留 | `tv_wonder_repair_stuck_expansion_ceremony_finalized_effect` 及其读档 pulse（旧存档修复，按“不保留修复路径”的规则删除） |
| 文档 / 测试 | `risk_cards/wonder_unique_rituals.md`（改写或删除）、`wonder_ceremony.md`（改写）；`test_wonder_mechanics_rules.py` 中有关单风格、跳过送奖、阶段 2/4 赠品的断言 |

## 15. 按文件改动清单

以 `in_game/`、`main_menu/` 开头的 `gen_*.py` 位于 `scripts_engineering_department/` 下，以 `src/` 下的同名路径输出；其余路径以仓库根为准。只修改数据和生成源，再运行生成器；不要手改生成出来的 txt / gui / yml。

| 工作面 | 文件 | 改动 |
|---|---|---|
| Schema / 归一化 | `scripts_engineering_department/wonder_mechanics/_core.py`，`naming.py`、`rituals.py`、`schema.py`、`io.py` | §5 |
| 数据 | `data/wonder_generic_rituals.yaml`、`wonders.yaml`、`unique_wonders.yaml`、`wonder_final_buildings.yaml`、`wonder_base_modifiers.yaml`、`wonder_localization.yaml`；新增 `wonder_ritual_rules.yaml`、`wonder_societal_axes.yaml` | §4 |
| 建筑 | `in_game/common/building_types/gen_tv_engineering_department_wonder_mechanics_buildings.py` | 每个奇观一个成品；删除附属建筑 |
| 静态 modifier | `in_game/common/static_modifiers/gen_tv_engineering_department_wonder_mechanics_modifiers.py`；删除 `main_menu/common/static_modifiers/gen_tv_engineering_department_wonder_ritual_auxiliary_location_modifiers.py` 及两个阶段费用生成器 | §6.1 |
| 状态效果 | `in_game/common/scripted_effects/gen_tv_engineering_department_wonder_mechanics_effects.py`（新增 `append_ritual_state_effects`、`append_ritual_phase_effects`，删除 `append_ritual_effects` 的旧内容），新输出 `tv_wonder_ritual_state_effects.txt` | §6.3、§7 |
| 落成 | `gen_tv_wonder_finalization_effects.py`、`in_game/events/gen_tv_wonder_finalization_events.py` | 单一成品；按结果选描述；grant + settle |
| 淡忘 / 重新仪式化事件 | 新生成器 `in_game/events/gen_tv_wonder_ritual_lifecycle_events.py` → `.2001–.2003`、`.2010`、`.3000+id`、`.4000+id` | §6.4、§8 |
| 易主 / 拆毁 | `gen_tv_wonder_ownership_effects.py`、`append_final_building_level_changed_effects()` | §6.5 |
| 外部接口 | `gen_tv_wonder_level_change_effects.py`、`vanilla_takeover/render.py` 及 `gen_tv_vw_*` | 删除 style 参数；`final_dispatch()` 改用 `final_building()` |
| 索引 / 模块 | `gen_tv_wonder_index_effects.py`、`gen_tv_wonder_module_effects.py`、`gen_tv_wonder_location_display_effects.py` | 删除风格相关 map；单一成品的反查 |
| 触发器 | `gen_tv_engineering_department_wonder_mechanics_triggers.py`；手写 `tv_engineering_department_triggers.txt` | 新的 outcome / 仪式阶段 / 朴素存在触发器；`can_finish_construction`（§7.6） |
| 手写效果 | `tv_engineering_department_effects.txt` | `finish_construction`、`finalize`、`clear_project_state`、阶层结算、重新仪式化锁定 |
| 动作 | `tv_engineering_department_actions.txt`；`gen_tv_engineering_department_wonder_mechanics_actions.py`；`tv_engineering_department_prices.txt` | §7.2 |
| 决议 | 新增 `in_game/common/decisions/tv_engineering_department_decisions.txt` | §8.2 |
| 朴素缓存 | `gen_tv_engineering_department_wonder_mechanics_effects.py` 的 `append_country_auto_level_map_effect()`（输出 `tv_wonder_mechanics_refresh_country_auto_level_map_effect`） | 在现有月度遍历中顺带写入 `tv_wonder_plain_level_by_wonder_id` / `tv_wonder_has_plain_wonder`（§8.1） |
| IO / on_action | `international_organizations/tv_engineering_department.txt`；`on_action/tv_engineering_department_on_action.txt`；`data/pulse_registry.yaml` | §11；删除监听器 |
| 事件 | `in_game/events/tv_engineering_department_events.txt`（`.202`）；手写本地化 yml | §11 |
| AI | `tv_engineering_department_ai_effects.txt` 及 AI 触发器；`docs/design/Engineering_Department_AI_Plan.md` | §12 |
| GUI | `gen_tv_engineering_department_wonder_mechanics_gui.py` 与合并脚本；`in_game/gui/gen_location_window.py`；百科卡片生成器 | §13 |
| 本地化 | `wonder_localization_lib.py`；`gen_tv_engineering_department_wonder_mechanics_l_*.py`；概念生成器 `gen_tv_engineering_department_wonder_mechanics_concepts.py` | §4.4 |
| 消费者 | 编辑器 `services/wonder/*`、`static/wonder_fields.js`、`wonder_values.js`；图鉴 `build_wonders.py`；`gen_wonder_editor_catalog.py` | §13.4 |
| 测试 | `test_wonder_mechanics_rules.py`；`tests/test_wonder_resource_contract.py`、`test_wonder_payload_loading.py`、`test_engineering_department_ai.py`、`test_generation_plan.py`、`test_wonder_field_preview.py`、`test_wonder_priority_proposals.py`；`ai_gui_assessment/tests/test_engineering.py` 与 `engineering.py` 的场景 | §17 |
| 地点显示变量与兼容子模组 | `gen_tv_engineering_department_wonder_mechanics_effects.py` 中的 `tv_wonder_display_slot_<k>_ritual_style/_completed`、`tv_wonder_tooltip_slot_<k>_ritual_style/_completed`、`tv_wonder_location_display_ritual_style/_completed`；消费者除 `gen_location_window.py` 外，还有 `submods/tv_standard_of_living_compat`、`submods/tv_meiou_and_taxes_compat` 的 `location_window.gui` 与 `submods/tv_prosper_or_perish_compat/in_game/gui/encyclopedia_lateralview.gui`（用已登记的兼容合并器重新生成） | §13.3 |
| 基础 auto modifier | `in_game/common/auto_modifiers/gen_tv_engineering_department_wonder_mechanics_auto_modifiers.py` | 删除倾向后，空的基础国家表不再生成 auto modifier（不输出空块） |
| 概念与多语言文本 | `main_menu/common/game_concepts/tv_engineering_department_game_concepts.txt`（`tv_wonder_ceremony` 概念说明）；`.202` 与提醒文本的 11 种语言版本 | §11 |
| 编辑器（补充） | `static/wonder_rituals.js`、`wonder_localization.js`、`wonder_drafts.js`、`server.py` 的仪式设计路由（约 409–419 行）、`services/wonder/sources.py`、`services/wonder_resource.py`、`services/wonder_generation.py`、`services/cost_reward.py` | §13.4、D05 |
| 测试（补充） | `tests/test_cost_reward_resource_contract.py`、`tests/wonder_values.cjs`、`tests/wonder_fields_browser.cjs`、`tests/closeout_browser.cjs`、`ai_gui_assessment/fixtures/ceremony_prestige.json` | §17 |
| 登记 / 知识 | `data/generated_files.yaml`；风险卡 `wonders.md`、`wonder_ceremony.md`、`wonder_buildings.md`、`wonder_gui.md`、`wonder_unique_rituals.md`；`context_routes.yaml`；BRIEF 重新生成 | §16 |

## 16. 工作包与顺序

| WP | 内容 | 依赖 | 完成标准 |
|---|---|---|---|
| WP0 | 决策冻结；引擎小样 M01–M09 | — | 决策清单逐项有结论；小样有游戏内记录 |
| WP1 | Schema、规则表、轴目录、`ritual_styles()`、校验与单元测试；数据迁移（奖励原样搬入，方向和偏好先用评审过的样本） | WP0 | 加载器严格通过；旧字段为零；`test_wonder_mechanics_rules.py` 换上新断言后通过 |
| WP2 | 单一成品；删除附属建筑；合并 modifier 与地点 modifier 的生成 | WP1 | 191 个成品；573 个合并 modifier；191 个地点 modifier；建筑属性差异表经评审 |
| WP3 | 仪式状态生命周期：grant、revoke、sync、settle、100 年计时、淡忘事件、易主、拆毁、开局、外部接口 | WP2 | §17 状态场景全部通过；不变量 1、2 在所有路径上成立 |
| WP4 | 仪式阶段流程：进入、预览、确认、朴素、月度进度、落成、扩建分支、空壳续建、支持度、`.202` | WP3 | 新建 / 扩建 / 续建三条路径都能走到落成；仪式阶段支持度不变 |
| WP5 | 重新仪式化：决议、`.2001`、锁定、`.4000+id`、取消 | WP4 | 只在构思状态可用；只奖励 buff 和 10 威望；落成后回到构思 |
| WP6 | 阶层意愿：推导、随机、结算、显示变量 | WP4 | 每个阶层恰好支持一个风格；朴素无结算 |
| WP7 | 内容：56 × 3 方向、56 套阶层偏好、135 × 2 独特风格名称与说明、朴素与淡忘文本、双语 | WP1 规则稳定 | 校验通过；人工评审签字 |
| WP8 | AI | WP4、WP5 | §12 的五条规则；不会卡死 |
| WP9 | 界面：采用的设计稿、地点窗口、百科、本地化 | WP4、WP6 | 离线渲染 `--strict` 通过；游戏内中英截图 |
| WP10 | 删除旧系统；编辑器、图鉴、测试、风险卡、BRIEF | WP3–WP9 | 全仓库不再引用 `ceremony_styles`、`ritual_plan_for_style`、`tv_wonder_ceremony_*`；`validate.py` 通过 |
| WP11 | 游戏内验收矩阵 | 全部 | §17 全部记录在案 |

WP7 可以与 WP2–WP6 并行。方向和偏好内容建议先评审 8 个样本机制（例如 sacred_mountain、triumphal_axis、great_port、star_fortress_city、colonial_trade_company、grand_cathedral、national_bank、mining_city），再铺开到全部 56 个。

## 17. 验证

### 17.1 静态验证

```powershell
C:\Users\Hades\anaconda3\envs\eu5\python.exe scripts_engineering_department\test_wonder_mechanics_rules.py
C:\Users\Hades\anaconda3\envs\eu5\python.exe -m pytest tests -q
C:\Users\Hades\anaconda3\envs\eu5\python.exe -m unittest discover -s ai_gui_assessment/tests -v
C:\Users\Hades\anaconda3\envs\eu5\python.exe scripts\validate.py --changed --fix --ai-report
```

新增断言：

1. 每个奇观 `ritual_styles()` 恰好 3 项；独特奇观的奖励与所属机制逐项相同，modifier key 不同。
2. 任何 modifier 中都只有合并 modifier 含 `monthly_towards_*`。
3. 每个风格的 `societal_value` 合法；同一机制内方向两两不同且至少跨两条轴；输出时代轴与无条件轴的方向比例（目标约 1 : 2，只报告）。
4. 阶层偏好：地点奖励所属阶层指向带地点奖励的风格；其余 6 个阶层全部给出，值为 1/2/3 或 `random`；生成的掷偏好、结算和显示代码对每个阶层都带有 `country_has_estate` 判断或以偏好变量是否存在为前提。
5. 生成的 grant / revoke 是 `tv_wonder_ritual_style_by_id` 唯一的写入者（扫描生成源）。
6. 事件 ID：`.2001–.2003`、`.2010`、`.3001–.3236`、`.4001–.4236` 与现有区段不冲突；`.9300–.9307`、`.6301–.6308`、`.7300–.7308` 已经不存在。
7. 生成新鲜度、本地化闭包（双语、BOM）、独立 ED 根依赖。
8. 渲染路径不遍历地点：决议 `potential` / `allow`、事件选项 `trigger`，以及选项内直接执行的效果（含 grant / settle）中，不得出现 `any_owned_location`、`every_owned_location`、`ordered_owned_location`、`random_owned_location`。扫描生成源与手写文件，`sync_country_effect` 和锁定效果只允许出现在 on_action、隐藏事件 `immediate` 和生命周期处理器中。

### 17.2 游戏内验收矩阵

| 组 | 场景与预期 |
|---|---|
| 新建 | 通用 / 独特各一座：建成 → `.202` 新文本 → 支持度在仪式阶段不变 → 选风格 → 举行仪式：扣费 + 阶层满意度立即变化 → 24 个月 → 落成：成品 + 合并 modifier（显示永久）+ 地点 modifier + 价值观移动 20 + 即时奖励；效果区不出现阶层满意度 |
| 朴素 | 选朴素：所有参与阶层立即反对；立即落成，有落成奖励包，没有其他仪式相关的东西；地点窗口显示“朴素” |
| 空壳 | 仪式阶段放弃：空壳留在原地，只给文化传统，作为续建候选出现；续建时锁定后可以立刻宣布建成 |
| 扩建 | 完整状态的成品扩建：直接落成，modifier 不变，没有第二次价值观移动；朴素成品扩建：出现选择 |
| 多实例 | 同种 small 两座都是风格 1：只有一个 modifier；失去一座仍保留，两座都失去才移除；两座不同风格时两个 modifier 各自独立 |
| 易主 | 被征服、劫掠、和平割让、释放附庸：旧主 modifier 按不变量 1 处理，地点 modifier 移除，新主为朴素；收复后仍为朴素 |
| 拆毁 | 降一级：状态保留；降到 0：状态与 modifier 清除 |
| 淡忘 | 用调试手段把计时缩短：到期后状态、modifier 清除，出现通知；期间清除并重新授予过的，旧计时器不起作用 |
| 重新仪式化 | 非构思状态不可用；没有朴素奇观时不可用；选中后直接进入仪式阶段；没有朴素按钮；落成只给 buff 和 10 威望，然后回到构思；构思进度保留 |
| 外部接口 | 原版事件建出的奇观为朴素，不显示“仪式完成” |
| 开局 | 65 座独特奇观为朴素，地点窗口显示正确 |
| AI | 选风格符合对齐度规则；付不起时 24 个月后选朴素；重新仪式化不会卡死 |
| 读档 | 仪式中、计时中读档：进度和 100 年计时不重置，也不重复结算 |
| 部署 | 独立 ED + 依赖；主 mod + ED；受面板改动影响的兼容子模组 |

### 17.3 引擎待验证（M）

| ID | 问题 | 验证方法 |
|---|---|---|
| M01 | `add_to_variable_map` 带 `days` 时限的到期语义；地点 map 以整数字面量为键 | 控制台小样：写入后读档，按天推进 |
| M02 | `location_event` 延迟 36501 天能否跨读档保留；事件 root 是否为该地点 | 小样用短延迟模拟，读档后观察是否触发 |
| M03 | 一年是否固定为 365 天；`days = 36500` 是否恰好等于 100 年 | 读原版定义；设短期小样对比 `years = 1` 与 `days = 365` |
| M04 | `change_societal_value` 冲击后回落到月度上限的速度；`monthly_towards_*` 在静态国家 modifier 中是否计入净推力、上限是否为 100 × 净推力 | 对照实验 |
| M05 | `.2001` 的 191 个候选选项与“稍后”能否完整滚动显示，是否截断或漏掉候选 | 实机检查至少 12 个有效候选及 191 个候选的最大集；按下方标准逐项核对。未执行，不能以静态合规或无报错代替 |
| M06 | `add_country_modifier mode = replace years = -1` 在 tooltip 中是否显示为“永久” | 截图 |
| M07 | `on_location_changed_owner` 中 revoke 与旧主清理的先后顺序，以及 `scope:loser` 的可用性 | 日志 |
| M08 | 决议在 ED 独立根中的分类与显示 | 截图 |
| M09 | 在脚本值中读取 `societal_value:<axis>` 的写法（AI 对齐度与界面对齐度显示） | 官方 triggers.log 与原版用法；小样 |

**M05 实机通过标准（当前未验收）：**

1. 记录游戏版本、启用模组、分辨率、UI 缩放和语言。分别使用至少 12 个有效朴素候选的小样与覆盖 191 个候选的最大集测试存档，进入 stage 0 且构思进行中的国家。
2. 先记录该国 `tv_wonder_plain_level_by_wonder_id` 的候选 ID 清单。通过决议打开 `.2001`，从顶部滚动到末尾，逐项对照清单，所有合格候选均须可见、文字可辨且能点击；确认第一项、列表中部、最后一个候选和“稍后”均可到达。最大集应有 191 个候选，外加 1 个“稍后”按钮。
3. 在中英两种语言、默认缩放及较大可用缩放、常用分辨率及游戏支持的较低分辨率下重复，记录滚动首尾截图或录像。任何候选被裁切、无法滚到、被遮挡或无法点击均判失败，即使错误日志为空。
4. 在有效候选小样中分别从首项和末项进入锁定，确认目标类型正确；同类型多实例时应锁定最高等级的朴素实例。检查完成后取消回到新构思，再验证“稍后”退出。
5. 静态事件数量检查、离线界面渲染及无脚本报错只能作为辅助证据；未取得上述实机记录前，M05 保持未验收。

## 18. 风险

- **内容量**：168 个方向、56 套阶层偏好。独特风格文本已写好（D03），仍需逐条评审。用户明确不想要 AI 堆砌的文本，评审时以具体、可考、不空泛为标准。
- **生命周期遍历**：通用奇观的 sync 需要遍历拥有地点，大国征服时可能在同一天执行多次。只在生命周期点执行，并且一次只处理一个 wonder id 的 3 个分支，开销可控；WP11 需要记录月结耗时。
- **重新仪式化刷取**：如果即时奖励算作 buff（D25），玩家可以通过“送出再拿回”反复刷即时奖励。24 个月工期和费用是天然限制，但仍需评审。
- **价值观数值**：D11 定为一次性 20、每月 0.1。月度推力是全国所有来源的净和，仅靠月度推力能到达的最远位置是净月度推力的 100 倍（`SOCIETAL_VALUE_INERTIA_SCALE = 100`）。所以一座完成仪式的奇观把该方向的上限抬高 10 点，不会随年份无限累积；20 点冲击可以暂时越过这个上限，之后会回到月度推力决定的位置。需要注意的是同向叠加：几座奇观选同一方向时上限按 10 点逐座增加，再加上法律和特权的推力，可能明显改变国家的价值观平衡（M04 实测）。
- **兼容子模组**：面板 GUI 大改后，已登记的兼容合并器需要重新运行。
