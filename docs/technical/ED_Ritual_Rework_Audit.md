# ED 仪式重写：审计报告

> 审计对象：`docs/design/Wonder_Ritual_Rework_Implementation_Plan.md`（下称“方案”）、`docs/design/Wonder_Ritual_Rework_Decisions.md`（下称“决策”）、`docs/technical/ED_Ritual_Rework_Implementation.md`（下称“实现报告”）所描述的工作区改动集。
> 审计性质：只读审计。本文件之外未做任何编辑。
> 审计日期：2026-10-23。
> 结论：**有条件通过**。运行时契约（状态模型、单一写入者、合并 modifier、易主/拆毁/淡忘、阶层偏好、支持度冻结、重新仪式化）经独立复核与实现一致，数量、继承与符号关系逐项对账无误。但存在 1 项内容交付缺口（168 条模板说明）、1 项文档与实现不一致（方案 §8.1 的缓存策略）、1 批未清理的退役本地化键，以及 2 项只能在实机关闭的界面/出口风险。逐条见第 3 章。

## 1. 审计范围与方法

### 1.1 验证环境

`.eu5-base` 在本沙箱中是不可读的链接（`Input/output error`），`scripts/validate.py` 因此无法启动：

```
OSError: [Errno 5] Input/output error: '.../eu5-towards-victory/.eu5-base'
```

实现报告的“静态验证 200 个变化文件，0 错误 0 警告”与“878 项通过、6 项失败”无法在此环境复现，本审计不采信，也不否定，只登记为待复跑项。替代手段是直接在源数据与生成物上做独立对账（第 1.3 节）。其余脚本（编译器、GUI 渲染、浏览器用例）同样未在本环境运行。

### 1.2 审计方法

不读取 worker 的实现报告作为证据，只把实现报告当作被审对象。所有结论由下列独立检查产生：

- 数据层对账：`data/wonder_generic_rituals.yaml`、`wonders.yaml`、`unique_wonders.yaml`、`wonder_ritual_rules.yaml`、`wonder_societal_axes.yaml` 用 Python 直接解析后与生成物逐项比对。
- 生成物对账：`static_modifiers`、`scripted_effects`、`events`、`gui` 用正则切块后与数据逐条核对。
- 本地化闭包：99 个 ED 本地化文件全部按二进制检查 BOM，按键名统计中英闭包，并反查代码引用。
- 渲染路径扫描：按 `docs/knowledge/risk_cards/wonder_gui.md` 与 `feedback_no_location_scans_in_render_paths` 的规则，扫描决议、事件选项 `trigger` 与选项内直接执行的效果。

### 1.3 独立复核结果（全部通过）

| 检查 | 结果 |
| --- | --- |
| 单一成品 | 191 个（56 通用 + 135 独特），与 191 个 wonder id 一一对应 |
| 合并国家 modifier | 573 个（191 × 3），全部 `category = country`，全部含且仅含一条 `monthly_towards_* = 0.1` |
| 地点 modifier | 191 个（每机制/每独特奇观风格 2 一个），全部 `category = location`，全部带 `local_*_estate_power` 0.5（D07） |
| 独特继承 | 405 个独特国家 modifier 与所属机制逐一相同；135 个独特地点 modifier 与机制相同；两者 key 命名不同 |
| 方向合法性 | 168 个方向全部命中 17 条原版轴；方向两两不同、至少跨两条轴（D13） |
| 方向与冲击符号 | 168 个 `settle_effect` 的轴、正负号与 `wonder_societal_axes.yaml` 的 `left_sign`/`right_sign` 全部一致；冲击全部为 ±20 |
| 时代轴比例 | 时代/条件轴 57，无条件轴 111，比值 1 : 1.95（D12 目标 1 : 2） |
| 阶层偏好覆盖 | 56 套偏好，补上地点奖励所属阶层后 7 个原版阶层齐备；191 个掷偏好分支中，地点奖励所属阶层 100% 指向带地点 modifier 的风格（§9.2 优先级 1） |
| 状态写入者 | `tv_wonder_ritual_style_by_id` 的全部写入都在 `tv_wonder_ritual_state_effects.txt`（生成物）内，无手写文件直写 |
| 渲染路径无地点遍历 | 决议文件与 `.2001–.2003`、`.2010` 的 `trigger` 中 `any/every/ordered/random_owned_location` 出现 0 次；唯一遍历在 `.2002` 隐藏事件的 `immediate` |
| 支持度冻结局 | IO `monthly_change` 与 `support_resolution_monthly_pulse` 均含 `NOT = { var:tv_wonder_stage ?= 4 }` |
| 事件 ID | 387 个（2001–2004、2010、3001–3236、4001–4236），去重后仍为 387；与 ED 其余事件无冲突；`.9300–.9307` 等退役区段不再存在 |
| 本地化 | 573 个风格 NAME/DESC 键中英各 573 个，191 个 id 全覆盖，BOM 99/99 |
| D34 三项修正 | `local_max_literacy: 10`、`site_prosperity: 0.5`、`local_monthly_prosperity: 0.004` 均已落地，旧值（0.1 / 50 / 0.4）零残留 |

## 2. 未验证项

实现报告第 70–72 节已如实登记 M01–M09 未做游戏内观测，本审计确认这一表述准确，并补一条：本环境下连静态验证脚本都无法启动，因此“静态验证 0 错误”属于**未经第三方复核的自述**。

## 3. 问题清单

### P1-01　168 条通用仪式说明是模板占位，不是交付文本

`src/main_menu/localization/english/tv_engineering_department_wonder_mechanics_l_english.yml:6553` 起：

```
TV_WONDER_RITUAL_DESC_1_1:0 "The Royal Sacrifice branch of the Sacred Mountain."
TV_WONDER_RITUAL_DESC_2_1:0 "The Meditation Ceremony branch of the Sacred Mountain."
```

168 条（56 × 3）全部是 `The <风格名> branch of the <机制名>.` 的机械拼接，中文本地化同构。D03 的适用范围是**独特**奇观（135 套，实测已是真实文本），方案 §4.4 对通用风格说明写的是“迁移现有 `.500.d_<x>_<n>` 的首句，或新写（D03）”。落成事件 `tv_engineering_department.500.d_sacred_mountain_1` 的正文同样是同一句模板：

```
tv_engineering_department.500.d_sacred_mountain_1:0 "The Royal Sacrifice branch of the Sacred Mountain.\n\n#weak Construction ..."
```

即玩家在仪式卡和落成事件里读到的都是同一句没有信息量的句子。实现报告第 10 行称“168 个方向与 56 套阶层偏好已按既有仪式主题逐项编排”，这条只覆盖方向与偏好，未声明说明文本仍是占位；第 27 行“英 / 简中仪式内容完整”容易让读者以为包含说明。**建议**：要么按 D03 的做法补齐 168 条（工作量与 135 座独特风格 2/3 同量级），要么在数据里显式标 `placeholder: true` 并由校验器统计（D03 选项 A 的原始机制），二者择一，不要保持当前“看起来完整”的状态。

### P1-02　方案 §8.1 写的“增量补充”没有实现，实际改用整表重建

方案 §8.1 要求：朴素落成（§7.4 结果 0）与淡忘（§6.4）时**直接**写入 `tv_wonder_plain_level_by_wonder_id` / `tv_wonder_has_plain_wonder`，作为月度重建之外的即时补充（“新出现的朴素奇观通常靠增量补充立即可见”）。

实测没有这条增量写入。缓存只有一处写入点与一处删除：

- 写入：`tv_wonder_location_display_effects.txt:9192–9224`，即 `tv_wonder_mechanics_refresh_country_auto_level_map_effect` 的整表重建
- 删除：`tv_wonder_ritual_phase_effects.txt:14756`（锁定失败时剔除非候选键）

实现改用“在生命周期点上直接调整表重建”代替增量写入，两处都调了：朴素/风格落成在 `tv_wonder_finalization_effects.txt:1162` 的 `finalization_hidden_effect`，淡忘在 `.3001` 的 `immediate`（`tv_wonder_ritual_lifecycle_events.txt:1954` 起）。因此**玩家可见的时效与方案意图一致**（决策立即生效），这一点不构成缺陷。

真正的问题是文档与代码不一致：方案 §8.1 的三段描述（增量补充、只增不减、“消耗常数开销”）在代码里都不成立，而这套“整表重建”的开销与 §8.1 声称的“不新增一次遍历”不同——它是把已有的月度遍历按需再跑一遍，代价是一次 `every_owned_location`，不是常数。实现报告第 14 行没有提这处替代。**建议**：把方案 §8.1 改写为“生命周期点触发整表重建”，并把这处额外遍历计入 P2-03 的耗时观测。

### P2-01　606 个退役本地化键仍随生成物发布

`tv_engineering_department_wonder_mechanics_l_english.yml` 中仍有 606 个 `TV_ENGINEERING_CEREMONY_*` / `TV_ENGINEERING_ACTIVE_RITUAL_*` 键（简中同构），内容还是旧八阶段的“Confirm the Royal Sacrifice ceremony for the Sacred Mountain. +20% …”。反查 83 个 ED 脚本/GUI 文件，**引用数 0**；`scripts_engineering_department/` 下也没有任何 Python 再生成它们。

这说明生成器已经不再产出这批键，但输出文件里是旧生成物残留（该文件被 `data/generated_files.yaml:488–490` 登记，正常的 `--fix` 重建应当把它们清掉）。方案 §14 把“旧八阶段”列为删除对象，实现报告第 27 行称“旧八阶段……已退役”。**建议**：重跑该本地化生成器并确认 606 个键消失；若重跑后仍在，说明有第二条写入路径，需要定位。

风险面：当前无引用，不影响运行；但它会误导后续维护者（尤其是查找“仪式文案在哪”的人和编辑器/图鉴的本地化扫描），也违反“未发布项目不留旧 schema”的核心规则。

### P2-02　`.2001` 单事件 191 个选项，界面容量只能在实机关闭

`.2001`（`tv_wonder_ritual_lifecycle_events.txt:8`）为每个 wonder id 生成一个选项，实测 191 个候选选项 + 1 个“暂不”。D27 推荐的就是这一方案，M05 把“选项很多时的事件 UI”列为待验证，方案 §17.3 与实现报告都保留了这条。

审阅范围内的静态事实：选项 `trigger` 只读缓存（合规），渲染成本是 191 次 map 查询（可接受）；不可预期的是引擎对超长选项列表的滚动/截断行为。一个大国可能同时拥有几十座朴素奇观，此时选项数不变（仍是 191），但可见选项会接近上限。**这是本审计认定的最高优先级实机项**，因为它的失败形态是“玩家看不到某个候选”，而不是报错。M05 的记录应写明：可滚动、无截断、按选项顺序稳定。

### P2-03　`tv_wonder_ritual_sync_country_effect` 的扫描次数比方案描述的更贵

方案 §6.3 说“一次只看一个 wonder id 的 3 个风格”，§18 说“开销可控”。实测每个 `sync_country_effect` 对同一 wonder id 做 **3 次** `any_owned_location` 全量扫描（3 个风格各一次，见 `tv_wonder_ritual_state_effects.txt:90–110` 的 sacred_mountain 样本）。易主路径 `tv_wonder_ownership_handle_location_owner_changed_effect` 会对该地点上的每个有仪式状态的奇观各调一次 revoke，每次 revoke 各触发一次 sync；`revoke_location_effect` 本身是一次 191 分支的串行检查。

同一天发生大规模征服（一次和平割让上百地点）时，最坏路径是“地点数 × 有仪式状态的奇观数 × 3 次全量扫描”。方案 §18 已把它列为 WP11 的月结耗时观测项，但没有给出上限估计。**建议**：把“一次征服中最多触发多少次 sync”写进 WP11 的验收记录（用日志计数即可），若超过可接受阈值，改为按 wonder id 聚合后一次扫描。

### P2-04　`.4001` 的完成选项是一次性的，关闭后无法再打开

`tv_engineering_department.4001`（`tv_wonder_ritual_lifecycle_events.txt:1978`）的选项条件是“模式 3 + 风格未写入 + 地点仍有成品”，点击后才执行 `apply_choice` 与 `.2004` 收尾。若玩家在 24 个月计时结束后、点击选项前存档并放弃这个事件（例如直接关闭弹窗），项目会停在 `stage = 4` 且 `tv_wonder_ritual_completed` 已设置：既不能重新确认（`can_preview` 要求未设置 `ritual_completed`），也不会再有事件。

现有兜底：`handle_final_building_level_changed_effect` 在成品被拆时会取消模式 3 项目；AI 由驱动器处理，不受影响。玩家的唯一出口是“放弃项目”（有惩罚）。这与 D21“不提供无惩罚搁置”不冲突，但与 R8“重新仪式化只奖励 buff 和 10 威望”的体验描述有落差。**建议**：要么在仪式卡上对“`stage = 4` 且 `ritual_completed` 已设置”显示一个“完成仪式”按钮（复用 `.4001` 选项的条件），要么把 `.4001` 改成每月重发的可重复通知事件。

### P3-01　职业阶层权力的 `crown` 映射与 D18 的口径不一致（历史遗留，非本轮引入）

`world_embassy_quarter` 与 `ayutthaya_foreign_quarters` 的地点 modifier 用 `local_crown_estate_power = 1`（`tv_engineering_department_wonder_mechanics_modifiers.txt:1406`、`:8380`）。D18 已裁定 soldiers → `peasants_estate`，但 D18 只约束**满意度**归属（§9.2），不约束 D07 的“地点阶层权力”。因此当前实现与决策不冲突；仅提示：这两条是 191 条地点 modifier 中唯一用 crown 的，若后续有人把“地点阶层权力”也接到 D18 上，会得到两套口径。

### P3-02　模式 3 的锁定只清构思进行中，不清构思完成待定

`tv_wonder_reritual_lock_effect` 对每个 wonder id 分支都执行 `remove_variable = tv_wonder_concept_in_progress`，但没有清 `tv_wonder_concept_completion_pending`。这个变量在 IO 的构思进度 `monthly_change` 里是“停止推进”的开关（`international_organizations/tv_engineering_department.txt` 的第 63 行附近），并参与构思完成事件的触发条件。

能走到决议的前提是“构思进行中”，而构思完成待定另有 `tv_wonder_concept_completion_pending` 的独立判定（`can_finish` 链），所以正常时序下两者不会同时成立。此处仅提示：若将来把“完成待定”也算作可发起重新仪式化的状态，必须先清这个变量，否则构思进度会静默停滞。当前不构成缺陷。

## 4. 符合性对照

| 需求 / 决策 | 结论 | 证据 |
| --- | --- | --- |
| R1 独特继承通用三风格、效果相同文本不同 | 符合 | 405 国家 + 135 地点 modifier 逐项相同；135 套 `ritual_text` 齐备 |
| R2 三类奖励可组合、本轮值不变 | 符合 | 56 机制各 1 国 1 地 1 即时；仅 D34 三处变动 |
| R3 朴素可选、每风格一价值观、冲击 + 永久倾向合并、取消纪念期 | 符合 | 573 个合并 modifier 各含一条 `monthly_towards_*`；`wonder_base_modifiers.yaml` 中 `monthly_towards` 计数为 0 |
| R4 状态脱离建筑、随易主/拆毁/淡忘回到朴素、不转移、显示永久、100 年计时 | 符合（缓存策略与 §8.1 描述不同，见 P1-02） | grant/revoke 成对；`days = 36500` 记忆 + `days = 36501` 隐藏地点事件；易主与拆毁均调 revoke |
| R5 仪式阶段不扣国内支持度 | 符合 | IO `monthly_change:84` 与 `support_resolution_monthly_pulse:192` 均排除 stage 4 |
| R6 单一成品、单一 modifier | 符合 | 191 成品；无 `_ritual_annex` 引用 |
| R7 空壳 / 朴素 / 完整三分、开局朴素 | 符合 | `tv_wonder_current_site_is_shell_trigger`（`tv_wonder_ritual_triggers.txt:29`）；开局初始化不写状态 |
| R8 构思状态下用决议重新仪式化 | 符合（P2-04 的 UI 出口除外） | 决议 `allow` 严格判 stage 0 + 构思进行中；`.2002` 隐藏事件复核 |
| R9 阶层意愿三级优先、无中立、不拥有者不参与 | 符合 | `country_has_estate` 前置；地点奖励所属阶层 100% 指向地点风格 |
| D01 固定三风格 | 符合 | 56 机制 `style = [1,2,3]` |
| D06/D07 地点奖励改地点 modifier、并入 +0.5 阶层权力 | 符合 | 191 条地点 modifier 全带 `local_*_estate_power` |
| D08 单一成品取风格 1 键与属性 | 符合 | 191 个成品键沿用风格 1（如 `tv_wonder_golden_sanctuary`） |
| D09 24 个月、2/3/5 倍 scaled gold | 符合 | `wonder_ritual_rules.yaml` 与价格文件一致 |
| D11 冲击 20、月度 0.1、不随等级 | 符合 | 168 个 settle 全为 ±20；573 个 modifier 全为 0.1 |
| D15 朴素发放落成奖励包 | 符合 | `.5000` 选项在结果 1–3 之外同样执行 `finalization_visible_effect` |
| D16 朴素时全体反对 | 符合 | `settle_estates_plain_effect` 对 7 个阶层各 −0.05 |
| D17 确认时结算阶层满意度 | 符合 | 结算在 `confirm_effect` 内、扣费之后、进入计时之前；不在完成效果里 |
| D20 空壳可立即宣布建成 | 符合 | `can_finish_construction` 增加“主体 ≥1 且无成品”分支 |
| D22/D23 完整扩建跳过仪式、朴素扩建重选 | 符合 | `enter_phase` 中 outcome 9 直接 finalize，否则掷偏好进选择 |
| D25 重新仪式化发放即时奖励 | 符合 | `.4001` 走同一个 `apply_choice` |
| D28 完成后构思从零开始 | 符合 | `reritual_finish` → `clear_project_state` → `start_concept { reason = 4 }` |
| D31 CMM 跳过仍需选风格、确认后立即完成 | 符合 | `confirm_effect` 免费 + 立即 `complete_effect` |
| D33 决议分类 `other_decisions` | 符合 | 决议文件第 2 行 |
| D36 同类型同风格不叠加 | 符合 | 静态 modifier + `mode = replace`；sync 只在最后一个来源消失时移除 |
| §13.1 效果区渲染真实效果 | 符合 | GUI 直接 `ShowScriptedEffectForScope('tv_wonder_ritual_apply_choice_effect', …)`，三张卡各一处 |
| §13.1 效果区外不重复数值 | 符合 | 方向区只显示轴、方向图标与位置条，不写 20 / 0.1 |
| §14 旧八阶段全部消失 | 部分符合 | 代码与 GUI 零引用，但本地化残留 606 键（P2-01） |
| §17.1 校验第 8 条：渲染路径不遍历地点 | 符合 | 决议与 `.2001–.2003` 的 `trigger` 中地点遍历计数为 0 |

## 5. 结论与后续

**有条件通过**。运行时契约的骨架是完整的：状态只有一个写入者、不变量 1/2 在 grant/revoke/sync 三个入口上成立、易主与拆毁都回到朴素、阶层偏好与阶层结算在数据层可以逐项证明，渲染路径没有地点扫描。这一层不需要返工。

需要在本轮关闭的事项按优先级：

1. **P1-01**：168 条通用仪式说明与落成事件描述仍是模板句。要么补齐，要么显式标记占位并由校验器计数——不能以当前状态当作“内容完整”。
2. **P1-02**：方案 §8.1 的“增量补充”在代码里是“生命周期点整表重建”。行为对玩家正确，但文档、开销描述与实现三者不一致；改文档，并把额外遍历计入耗时观测。
3. **P2-01**：重跑本地化生成器，清掉 606 个退役键；若清不掉，定位第二条写入路径。
4. **P2-02**：M05 必须在实机记录“191 个选项可滚动、无截断”，这是唯一会让玩家看不到候选的失败形态。
5. **P2-03 / P2-04**：把“一次征服触发的 sync 次数”和“`.4001` 被关闭后的出口”写进 WP11 验收；两者都不影响静态契约。
6. **P3-01 / P3-02**：两项均为口径与清理提示，不需要本轮处理，记入后续维护清单。

未复核项（本环境无法执行）：`scripts/validate.py --changed --fix --ai-report`、`rebuild_wonder_mechanics.py --atlas`、pytest / unittest / node 全套。实现报告的“0 错误 0 警告”“878 通过 6 失败”应由能读到 `.eu5-base` 的环境复跑一次并在此文件追加环境与结果。
