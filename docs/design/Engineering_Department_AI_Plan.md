# 工程部 AI 建造伟大工程：实现计划

> 当前状态：已归档（用户决定，2026-10-22）。实现、观察者问题及剩余验收均不再列为当前待办；仅在用户重新提出问题或明确要求时重开。以下计划与验证状态保留为历史记录。

> 状态：计划已独立提交（`a6136902`），游戏侧代码已实现并通过静态验证（2026-10-19）；2026-10-21 已完成 9d1f 观察者档案的部分运行验收，完整 WP7 场景尚未全部覆盖。§11 优先于前文，交付记录见 `docs/technical/ED_AI_Implementation.md`，档案核对见 `docs/technical/ED_AI_Observer_Audit_9d1f.md`。
> 范围：`src/` 独立模组，以及它在 `scripts_engineering_department/`、`data/` 中的生成器和数据。
> 方针：AI 不自由决策，也不使用工程部面板或 generic action。由一个集中的“AI 驱动器”脚本，在固定条件下直接调用玩家点击背后的同一批 scripted effect，从而走完和玩家完全相同的状态机。

## 1. 建造流程全景（现状）

工程部（ED）是每个国家开局都自动拥有的非唯一 IO（`tv_engineering_department_standalone_on_action.txt`）。所有进度都存在国家变量 `tv_wonder_stage` 和 IO 变量上（`tv_wonder_concept_progress` / `tv_wonder_domestic_support` / `tv_wonder_survey_progress` / `tv_wonder_construction_progress`）。

| 阶段 | `tv_wonder_stage` | 玩家操作（generic action → effect） | 自动推进部分 | AI 目前的情况 |
|---|---|---|---|---|
| 任命总工程师 | 0 | `tv_appoint_engineering_leader`（选角色，`scope:target`），效果内联在生成的 action 里，然后调用 `tv_engineering_on_great_engineer_appointed_effect` | — | 独立 ED：永不任命。主模组里 AI 建立繁荣胜利 IO 时会经 `tv_establish_prosperity_io_effect` 自动任命 |
| 构思 | 0 | 无 | IO `tv_wonder_concept_progress` 每月 +工程师 adm×0.2；满 100 时月度脉冲触发 `.30`（单选项），执行 `tv_wonder_complete_concept_effect`：重建可行卡组，抽 1–3 个提案槽 | 能自动走完 |
| 提案 | 0 | `tv_wonder_select_proposal_slot_N` → `tv_wonder_accept_proposal_effect`；或否决（`refute`，-10 威望）/ 贿赂（`bribe`，-1 scaled gold）后重新构思（reason 2） | 若有可续建/扩建的优先项目，`tv_wonder_select_saved_priority_proposal_effect` 会自动填入 `tv_wonder_proposal` 并设 `proposal_mode` | **卡死**：接受提案的 action 的 `ai_will_do = -100`。已进入繁荣胜利的 AI 会永远停在这里 |
| 辩论 | 1 | 对三阶层诉求逐个接受（+20 支持度）/ 否决（-10 威望，重抽）/ 贿赂（-1 scaled gold，重抽）；支持度 ≥100 后 `tv_wonder_end_debate` | 每月 6% 概率随机事件 `.100–.105`（±20）；支持度满 200 时自动结束 | 卡死 |
| 勘测 | 2 | `tv_wonder_start_survey`（选地点，`scope:target`）→ `tv_wonder_mechanics_start_survey_effect`；可 `rerun`；完成后 `tv_wonder_select_construction_site_effect` | IO 勘测进度每月 +工程师 mil×0.1；三项能力（规模/后勤/组织）向目标值增长；满 100 自动完成，触发 `.300`；每月 9% 勘测事件（`.320–.322` 为双选项） | 卡死。优先项目（续建/扩建）直接跳过勘测 |
| 施工 | 3 | 用原版建造按钮在工地建 `tv_wonder_labor_camp`（AI 和自动化都被禁止建造）；可手动 `begin_*` 切换部件；可提前 `finish_construction`（等级须 > 基础等级） | 月度脉冲自动选部件、累进进度、完成单元；`.200/.201/.204–.206`（单选项）建造模块和辅助建筑；等级达到规模层级时自动完工；10%/月随机事件 `.7000–.7211`（130 个双选项）；支持度归零：等级 ≥1 时自动完工，否则 `.20` 强制放弃 | 没有劳工营，进度为 0，卡死 |
| 仪式（通用奇观） | 4 | 选风格 `choose_ceremony_style_1/2/3` → `confirm_ceremony`（免费）/ `_scaled_gold` / `_prestige`（action 的 `price` 扣费，effect 本身不扣） | 风格 1：计时一年；风格 2：非即时建附属建筑（500/800/1200 金），建成后自动完成；风格 3：即时，代价为艺术品 / 5×scaled gold / 50 威望 | 卡死 |
| 仪式（唯一奇观 103–236） | 4 | 无（完工时自动锁定风格 1 并开始） | 8 阶段，每 3 个月一个事件 `.9300–.9307`：a 付费推进，b 拒绝（3 个月后重来）；没有 ai_chance，也没有可负担性检查 | 能推进，但取决于 AI 怎么选事件选项（见 §2.4） |
| 仪式（Hagia Sophia 102） | 4 | `confirm_ceremony` 启动，然后 8 步 `hagia_assign_step_N`（选角色，`scope:target`） | 每步 3 个月后触发 `.630N`（a/b） | 卡死 |
| 仪式（Pharos 101） | 4 | `confirm_ceremony`（建附属建筑，800 金） | 其后全自动：海盗事件 `.7301–.7303`（a/b）、8 条航线；无主航线会停滞 | 卡死 |
| 落成 | 5 | 无 | `tv_wonder_finalize_effect` → `.50NN/.51NN`（单选项）：建最终建筑、发奖励、向**所有其他国家**广播 `.60NN/.61NN`、清空项目、自动以 reason 3 重新开始构思 | 能自动走完 |

## 2. 影响方案的关键发现

1. **可以完整复用状态机。** 除下列少数例外，所有玩家操作背后的 effect 都只依赖国家作用域，可以在月度脉冲里直接调用。人类接管 AI 国家（多人中途加入、换国）时，状态可以原样交接，不需要任何迁移。
2. **有三处依赖 generic action 才有的作用域：**
   - `tv_wonder_location_can_host_locked_wonder_trigger`（生成文件，WMT:36012）读取 `scope:actor`，没有它时恒为假；
   - `tv_wonder_mechanics_start_survey_effect`（survey_effects:12032）读取 `scope:target`（地点）；
   - Hagia 的 `tv_wonder_hagia_assign_step_N_effect` 读取 `scope:target`（角色）。
   
   此外，总工程师任命的效果内联在生成的 action 里，没有可调用的 scripted effect。主模组的 `tv_establish_prosperity_io_effect` 里已经复制了第三份。
3. **项目规则冲突。** `docs/knowledge/risk_cards/on_action.md` 第 5 条和反模式 `on_action_simulates_generic_action_actor_context` 写明“不要在广域脉冲里模拟 generic action AI”。已决定修订规则（D1）。
4. **AI 怎么选事件选项未经验证。** 所有 ED 事件都没有 `ai_chance`（主模组已有 `ai_chance = { factor = N }` 的先例，见 `tv_arts_exhibition_events.txt`）。单选项事件没有影响；但双选项事件（唯一奇观 8 阶段、Hagia、Pharos、130 个施工事件、3 个勘测事件）的结果取决于引擎默认行为。若 AI 总选 b，唯一奇观仪式会永远停滞；若总选 a，会无视可负担性一直付费。
5. **劳工营是最大的障碍。** 它的 `important_for_AI = no`、`automation_build_allowed = no`，`allow = { owner = scope:actor }`，`max_levels` 由 `tv_wonder_organization_site_level_cap` 决定（组织能力 ÷5，上限 20）。进度只计算有人上工的等级（需要工地有劳工人口），还受工具/木材/石料市场供需影响。
6. **CMM 的 skip / unlimited 设置都是全局的**，会在进入各阶段时复制成国家旗标 `tv_wonder_cmm_skip_*`。也就是说，玩家开启“跳过施工”会让所有 AI 的奇观也瞬间完工。
7. **现有缺口（玩家也存在）：** 施工中如果失去工地，`tv_wonder_construction_site_selected_trigger` 变为假，项目会永久停住，没有任何处理。
8. **对胜利路线没有直接影响。** 主模组的胜利路线不统计奇观数量，只会通过奇观的修正和落成奖励（繁荣度、稳定、正统）间接影响。
9. **工期估算**（以工程师 adm/mil 50、三项能力约 50 为例：组织上限 10 级、后勤 100%、规模层级 3，即 12 个单元）：

| 环节 | 时长 |
|---|---|
| 构思 | 约 10 个月 |
| 辩论 | 取决于策略：通用奇观需约 5 次接受；唯一奇观起始已有 50 支持度，约需 3 次 |
| 勘测 | 约 20 个月 |
| 施工（10 级满员、原料充足，每月 1 万进度） | 小型约 10 年，中型约 20 年，大型约 30 年 |
| 仪式 | 风格 1 一年；唯一奇观约 2 年起 |

## 3. 已定决断（2026-10-19）

| # | 决断 |
|---|---|
| D1 | 修订规则。`on_action.md` 第 5 条原本只是要求 AI 不行动；改为允许一个集中的 AI 驱动器调用 scripted effect，但仍禁止在脉冲里复刻 generic action 的 allow/select 流程。同步修改反模式 `on_action_simulates_generic_action_actor_context` 的说明，并重新生成 BRIEF |
| D2 | `tv_wonder_location_can_host_locked_wonder_trigger` 改为读 `owner` |
| D3 | 把总工程师任命抽成共享 scripted effect，供 action、繁荣胜利和 AI 三处共用 |
| D4 | 每个 AI 每月最多执行一步 |
| D5 | 首批只用月盈余门槛（必须是结余，见 Q1）：300–600 杜卡特优先小型，600–900 优先中型，900 以上优先大型。不足 300 不入场，也不接受任何提案（Q2）。更细的资格条件留作后续优化 |
| D6 | 首批不设数量控制，后续通过优化 D5 条件来自然控制频率 |
| D7 | 全部开放，包括唯一奇观、Hagia 和 Pharos |
| D8 | 续建 > 扩建 > 新建 |
| D9 | AI 承受和玩家相同的失败成本 |
| D10 | 按 adm+mil 选最优角色；没有可选角色时，用脚本创建一个并立即任命 |
| D11 | 续建和扩建提案直接接受（D8）。新建提案按 Q3 的规模顺序固定选第一个命中项；都不命中时才重抽：国库 ≥ 1000 就贿赂，否则威望 ≥ 10 就否决，都不满足就跳过，等下个月 |
| D12 | 目标把支持度推到 200（满 200 时辩论自动结束）。不接受诉求 1、2、3、4、9，接受 5、6、7、8、10、11、12。每月从所有可接受诉求里随机接受一个；没有可接受的诉求时，随机挑一个阶层：有钱就贿赂，否则威望 ≥ 10 就否决，再不行就等随机事件 |
| D13 | 从所有可承载的地点里随机选一个勘测，完成后总是直接确认，不重勘 |
| D14 | 脚本控制劳工营建造。用一个变量记录目标数量：小型 5、中型 10、大型 15，不超过组织适性上限。未达标时，每有 1000 杜卡特允许开工一座；建造由脚本直接开工，并按常规扣费。原料压力由 AI 自己的经济逻辑去消化 |
| D15 | 每个项目最多提高两个工程等级。劳工不足导致支持度耗尽时，会按现有机制提前终止 |
| D16 | 通用奇观永远选风格 1 |
| D17 | 用原生 `ai_chance`，固定选能推进进度的选项，即使代价很高 |
| D18 | Hagia 由脚本替 AI 选人 |
| D19 | 用原生 `ai_chance`，固定选保守选项 |
| D20 | 首批不处理支持度危机。以后 ED 会加一个通用的一次性紧急补支持度机制，届时 AI 固定选择补支持度 |
| D21 | 先修通用缺口：失去工地时自动触发失败事件，写明原因是失去工程地点，并自动登记为续建优先项；AI 走同一逻辑。勘测前的停滞无害，可以忽略；勘测后的停滞会因支持度耗尽自然失败，也可以忽略。因此不需要看门狗 |
| D22 | 所有 CMM 设置只作用于人类，AI 走自己的设置 |
| D23 | 只加一个 AI 总开关。关闭后停止脚本代操作；既有自动进度与事件继续（2026-10-19 用户确认） |
| D24 | 照常通知玩家 |
| D25 | AI 与玩家严格同规则 |
| D26 | 人类接管时项目原样交接 |
| D27 | 不做 AI 奇观的可见性界面 |
| D28 | 首批不做调试开关 |

## 4. 架构

- **入口**：全部受 CMM 全局变量 `tv_engineering_department_ai_enabled`（D23）控制，并且只对 `is_ai = yes` 且是 ED 成员的国家运行。
- **年度脉冲** `tv_engineering_department_ai_yearly_pulse`：
  - 条件：`stage = 0`，没有工程师，月盈余 ≥ 300（D5）。
  - 满足时任命工程师（D10），构思随之自动开始。
- **月度脉冲** `tv_engineering_department_ai_monthly_pulse`：
  - 便宜的条件先判断：`is_ai`、开关、成员、`tv_wonder_stage` 已存在且项目非空闲。
  - 按 §5 的顺序执行**第一个**满足条件的分支，然后结束（D4）。
- **不设项目旗标，也不设看门狗**（D6、D21）。ED 的现有状态变量本身就是 AI 状态。新增的 AI 专用变量只有一个，即 `tv_wonder_ai_labor_camp_target`（D14）。
- **新增手写文件**：
  - `common/scripted_effects/tv_engineering_department_ai_effects.txt`
  - `common/scripted_triggers/tv_engineering_department_ai_triggers.txt`
  - `common/on_action/tv_engineering_department_ai_on_action.txt`
  - 脉冲注册写进 `data/pulse_registry.yaml`，再重新生成 bridge。
- **日志**：用 `cmf_log_with_args` 记录 AI 的每一步，便于观察者模式核对。D28 决定不做调试开关，但日志成本很低，保留。

## 5. 月度驱动器分支（从上往下，命中第一个就执行并结束）

| # | 条件 | 动作 |
|---|---|---|
| 1 | `stage ≥ 1` 且没有在世的工程师 | 重新任命工程师（D10）。施工和仪式阶段不需要工程师，但勘测需要；为简单起见统一补任 |
| 2 | 有开放提案，已设置 `tv_wonder_priority_found`，且月盈余 ≥ 300（Q2） | 调用 `tv_wonder_accept_proposal_effect`。续建优先于扩建，由现有的 `tv_wonder_select_saved_priority_proposal_effect` 保证（D8）；不看规模偏好 |
| 3 | 有开放提案，`tv_wonder_proposal` 为空，且月盈余 ≥ 300 | 按 Q3 从 `slot_1..3` 里选：命中就调用 `tv_wonder_select_proposal_slot_N_effect`；不命中则在国库 ≥ 1000 时调用 `tv_wonder_bribe_proposal_effect`，否则在威望 ≥ 10 时调用 `tv_wonder_refute_proposal_effect`，都不满足就本月不动 |
| 4 | 有开放提案，`tv_wonder_proposal` 已设置，且月盈余 ≥ 300 | 调用 `tv_wonder_accept_proposal_effect`。盈余跌破 300 时停在这里等待 |
| 5 | `stage = 1`（辩论） | 按 D12 处理：随机接受一个白名单诉求，或者贿赂/否决 |
| 6 | `stage = 2`，勘测已完成 | 调用 `tv_wonder_select_construction_site_effect`（D13 总是确认）。续建和扩建项目在这里直接跳过勘测 |
| 7 | `stage = 2`，还没开始勘测 | `random_owned_location`，limit 为 can_host（D2 改造后），存为 `scope:target`，再调用 `tv_wonder_start_survey_effect` |
| 8 | `stage = 3`，`tv_wonder_level ≥ tv_wonder_project_base_level + 2` | 调用 `tv_wonder_finish_construction_effect`（D15）。达到规模层级时，现有逻辑会自动完工 |
| 9 | `stage = 3`，劳工营未达标，国库 ≥ 1000 | 刷新 `tv_wonder_ai_labor_camp_target = min(5/10/15, tv_wonder_organization_site_level_cap)`，在同一步里开工 `min(floor(国库/1000), 目标 − 现有等级 − 在建等级)` 座，并按常规扣费（Q5） |
| 10 | `stage = 4`，通用奇观，可以选风格，且风格不是 1 | 调用 `tv_wonder_choose_ceremony_style_effect = { style = 1 }`（D16） |
| 11 | `stage = 4`，`tv_wonder_ceremony_ready_for_free_confirmation_trigger` 成立 | 调用 `tv_wonder_confirm_ceremony_effect`。通用奇观风格 1、Hagia 启动、Pharos 建附属建筑都走这一步 |
| 12 | `stage = 4`，Hagia，某一步可指派 | 从合格角色里随机选一个（排除总工程师），没有就造人，第 7 步造贵族阶层角色；存为 `scope:target` 后调用 `tv_wonder_hagia_assign_step_N_effect`（Q8） |
| — | 其余情况 | 什么都不做：构思、勘测、施工进度、唯一奇观 8 阶段（事件）、落成都自动推进 |

落成后，现有逻辑会以 reason 3 自动开始下一轮构思，所以 AI 会持续循环建造。按 D6，首批不拦截。

## 6. 需要改动的现有代码

| 改动 | 位置 | 决断 |
|---|---|---|
| 修订规则第 5 条和反模式说明，`wonders.md` 增加“AI 驱动器”小节，重新生成 BRIEF | `docs/knowledge/risk_cards/on_action.md`、`anti_patterns.yaml`、`wonders.md` | D1 |
| `can_host_locked_wonder` 的 192 个分支从 `scope:actor` 改为 `owner ?=`；action 的 `visible` 保持不变 | `gen_tv_engineering_department_wonder_mechanics_triggers.py` | D2 |
| 生成共享效果 `tv_engineering_appoint_great_engineer_effect`（国家作用域，读 `scope:target`）；三个 leader action 和 `tv_establish_prosperity_io_effect` 都改为调用它 | `gen_tv_io_leader_actions.py` + `data/io_leaders.yaml`；主模组 `towards_victory_effects.txt` | D3 |
| 唯一奇观 8 阶段事件 `.9300–.9307`：a 设 `ai_chance = { factor = 100 }`，b 设 `factor = 0` | `gen_tv_wonder_ceremony_events.py` | D17 |
| Hagia `.6301–.6307` 和 Pharos `.7301–.7303` 的双选项：推进项 100，另一项 0 | `gen_unique_wonder_rituals.py` 的 Hagia/Pharos 内容模块 | D17 |
| 施工随机事件的两类双选项，共 130 个（见 Q9） | `gen_tv_wonder_construction_events.py` 的 `render_options` | D19 |
| 勘测事件 `.320–.322`：b（不付费）设 100，a 设 0 | 手写 `tv_engineering_department_events.txt` | D19 |
| CMM 设置只对人类生效：5 处 skip 旗标复制点加 `is_ai = no`；直接读全局变量的地方（unlimited_scale、unlimited_organization、两个 disable_events、三个模块进度需求滑条）对 AI 改用默认值 | 手写 `tv_engineering_department_effects.txt` / `_triggers.txt`；生成的 `tv_wonder_survey_effects.txt`（skip_survey 分支）和 `tv_wonder_module_effects.txt`（unlimited_scale、需求滑条）要改对应生成器 | D22 |
| 新增 CMM bool 设置 `ai_enabled`，加 EN/ZH 本地化 | `tv_engineering_department_cmm_effects.txt`、本地化 | D23 |
| 失去工地：见 §7 | 新 on_action、新事件、优先项登记改造 | D21 |

## 7. 失去工地的通用修复（D21）

1. 在 `on_location_changed_owner` 上新增回调 `tv_wonder_construction_site_lost_on_owner_changed`，通过 pulse_registry 注册。回调的作用域：root 是地点，`scope:loser` / `scope:winner` 是前后两个所有者，和现有的 `tv_wonder_ownership_on_action.txt` 一致。
2. 触发条件：`scope:loser ?= { var:tv_wonder_site ?= root  NOT = { has_variable = tv_wonder_finalized } }`，覆盖施工阶段和仪式阶段。勘测地点的丢失按 D21 忽略。
3. 给 loser 触发失败事件（新编号，例如 `tv_engineering_department.21`），单选项，正文写明“失去工程地点”。选项内容：
   - 先登记续建优先项；
   - 再执行失败清理，惩罚档位见 Q10；
   - 不管地点归谁，都销毁该地点的劳工营。
4. **登记改造**：现有的 `tv_wonder_set_current_project_priority_candidate_mode_effect` / `_commit_...` 以 `tv_wonder_construction_site_selected_trigger` 为门槛，而这个 trigger 要求地点归自己所有，失去地点后会直接跳过登记。需要把这两处门槛改成只检查 `has_variable = tv_wonder_site`，玩家和 AI 共用。登记之后，候选项会因为“地点不归自己”而在校验中自动无效；收复地点后又会自动恢复有效，符合续建语义。

## 8. 工作包

| WP | 内容 | 依赖 |
|---|---|---|
| WP0 | 游戏内验证：对已有劳工营再次 `construct_building` 是否 +1 级；脚本建造是否检查 `allow` / `max_levels`；`random_owned_location` 在国家脉冲里的写法。已经通过官方文档确认的：`monthly_balance` 可用；`construct_building` 有 `payer` 参数（默认由建筑所有者付费），也就是会按常规扣费；`ordered_owned_location` 存在（支持 `order_by` / `position` / `max`）。`ai_chance = { factor = N }` 和 `create_character` 在主模组已有先例。所有双选项事件都会显式写 `ai_chance`，所以引擎默认怎么选不再影响结果 |
| WP1 | D1 规则修订、D2、D3、D22 | — |
| WP2 | D21 失去工地修复（玩家也受益，可以独立上线） | WP1 |
| WP3 | 驱动器骨架：开关、两个脉冲、任命/造人、日志 | WP1 |
| WP4 | 分支 2–7：提案、辩论、勘测 | WP3 |
| WP5 | 分支 8–9：施工和劳工营 | WP0、WP4 |
| WP6 | 分支 10–12：仪式，以及所有事件的 `ai_chance` | WP5 |
| WP7 | 观察者模式全流程测试：通用奇观、唯一奇观、Hagia、Pharos、续建、扩建、工程师死亡、失去工地、支持度归零、关闭开关、人类接管。之后跑 `validate.py --changed --fix --ai-report`、`test_wonder_mechanics_rules.py`，再更新文档 | 全部 |

## 9. 追问的结论

| # | 结论 |
|---|---|
| Q1 | 用结余口径，接口已确认：官方 `triggers.log` 中的 `monthly_balance`（国家作用域，读上个月实际结算的结余，第一个月结算前为 0，是 `last_months_balance` 的别名，支持 `<` `<=` `=` `!=` `>` `>=`）。vanilla 已在 `ask_for_money.txt`、`incite_desertion.txt` 等文件中使用。写法为 `monthly_balance >= 300` |
| Q2 | 每次接受提案时都检查月盈余 ≥ 300，新建、续建、扩建都一样。不足时停在提案处等待 |
| Q3 | 新建提案的规模顺序：偏好规模的第一个 → 较小规模的第一个（大型偏好依次看中型、小型；小型偏好没有更小的）；都不命中就重抽，见 D11 |
| Q4 | 贿赂的“有钱”标准是国库 ≥ 1000 |
| Q5 | 劳工营一步开工 `min(floor(国库/1000), 剩余目标)` 座，按扣费前的国库计算，计数包含在建等级 |
| Q6 | “最多提高两级”以 `tv_wonder_project_base_level` 为基准 |
| Q7 | 锁定风格沿用并正常付费，付不起就等 |
| Q8 | Hagia 随机选人，排除总工程师；没有候选时造人 |
| Q9 | 保守选项保国家。`trade_noneng_for_eng`（65 个）选 b，什么都不做；`choose_eng_or_noneng_loss`（65 个）选 a，损失工程方面；勘测事件 `.320–.322` 选 b |
| Q10 | 失去工地等同强制放弃：三阶层满意度 -10%、杀死总工程师、-20 威望，并登记续建优先项。新的所有者首批不登记 |
| Q11 | 总开关默认开；关闭后停止脚本代操作，既有自动流程继续，不清理（2026-10-19 用户确认） |

## 10. 已知风险（按“AI 很笨”的设计接受，上线后观察）

- **重抽循环。** 偏好小型的 AI 如果只拥有中、大型的唯一奇观地点，而唯一卡组总是先抽，它会反复贿赂或否决。每次重抽都要重新构思，约 10 个月；有钱时每次还要付一次贿赂金，没钱时每次 -10 威望。卡组抽空后会重建，所以循环可能一直持续。若观察到这个问题，可以在 D5 的后续优化里加“连续重抽 N 次后接受较大规模”。
- **随机选址导致工期过长。** 地点劳工不足时，施工进度极低，支持度耗尽后：等级 ≥ 1 会提前完工，等级 0 会强制放弃（杀死工程师）。这是 D13、D15 预期内的结果。
- **Pharos 航线停滞。** 无主航线不会触发事件，仪式可能停在 stage 4，直到支持度耗尽、强制放弃。玩家也有同样的问题，属于 D21 中可以忽略的“勘测后停滞”。

## 11. 实现前独立复核及修订（优先于前文）

1. **财政门槛有官方接口证据。** `.eu5-base/reference_official_defines/docs/triggers.log` 的 `monthly_balance` 支持国家作用域比较运算，含义为上月实际结余，首月为零，是 `last_months_balance` 的别名。使用 `monthly_balance >= 300`，不以总收入代替。官方接口证据足以编写代码；AI 实际读数仍列入游戏验收，不宣称已经实测。
2. **脚本建造仍走常规队列和费用。** `effects.log` 的 `construct_building` 支持 `instant = no`、owner、payer；不设置费用或需求倍率。驱动器自行限制目标及已建/在建总量，不依赖该命令替我们检查上限，也不调用依赖 `scope:actor` 的建筑选择检查。队列扣费、建材和升级行为必须实机验收。批量次数按开工前国库计算，但每座仍需可支付真实价格，避免优惠/涨价导致透支。
3. **保留失地续建记录需要额外改造。** `tv_wonder_select_saved_priority_proposal_effect` 当前会删除校验失败的候选项，故 §7 所称“收复后自动恢复”并不成立。失地候选暂时跳过，保留持久 map；重新拥有地点时再按真实建筑状态校验。没有任何已完成单元的新工地不虚构可续建进度。
4. **失地失败即时执行且事件只通知。** 所有权回调中校验活动项目，先登记候选、清营及执行原有放弃惩罚，然后显示专用单选通知，避免人类悬置事件后误清理新项目或重复惩罚。施工与仪式都覆盖；新所有者不接收旧主的未完成项目记录。
5. **仪式补齐付费分支。** 可改风格的普通项目选 1；已锁风格沿用。scaled-gold/prestige 确认在驱动器显式 `pay_price` 后调用共享效果。附属建筑先检查真实价格再启动。Hagia 第 4 步由现有效果指派君主，不随机造人；其他步骤复用角色规则，第 7 步要求贵族。
6. **任命与移除分开。** 任命/更换以及繁荣建立入口共用任命效果；移除使用对应移除效果，不能调用任命。保持原有角色条件，工程师按 adm+mil 排序，造人只在无合格候选时发生。
7. **每月一步指主动代操作。** 提案选择与接受按原有两个效果分月进行；白名单诉求仍需满足现有可用性条件。年度招募也须避免同月再代操作。自动工程进度与原生事件不计入主动一步。
8. **CMM 与开关边界。** AI 只读新增总开关；玩家跳阶段、取消上限、事件开关、施工需求倍率不改变 AI 默认规则。关闭只停止主动代操作，固定 `ai_chance` 和原有自动流程继续。主模组原有繁荣入口仍按其既有规则运行。
9. **共享知识只读。** 原反模式位于 `.eu5-base`；本次不修改共享仓库，也不重复注册同名规则。当前仓库 risk card 记录用户明确授权的 ED 驱动器例外，以及禁止伪造 `scope:actor` 的边界。
10. **交付与验证。** 先仅提交本计划。随后实现游戏脚本、生成器及有意义的策略/回归检查；重生成受影响文件，运行机械规则测试和项目验证。当前会话没有已连接的游戏验证接口，不能把静态检查当作 WP0/WP7 的实机通过；交付时明确列出待实机项目。


## 2026-10-23 仪式重写落点

仪式操作已替换为统一对齐度选择：三个方向按当前可用价值观取有符号归一值，最高者胜出，同分取编号小者；未出现的轴取 0。确认使用与玩家相同的付费/阶层效果。资金不足等待 24 次月结后朴素落成，重新仪式化则取消。构思中有朴素缓存且月结余达 300 时，每月以 10% 概率尝试从能支付对应规模仪式费用的最高等级缓存选取重新仪式化项目；锁定时重新验证所有权和状态。旧专属人物指派、固定风格 1 和三类确认分支已删除。
