# ED 伟大工程仪式诠释：独立审计与游戏内实施计划

审计日期：2026-10-21（Asia/Shanghai）。目标：工作区声明的 EU5 1.4 beta。

本次交付是实施计划和静态审计，未修改游戏数据、生成器或运行脚本，未启动游戏。原稿 [Wonder_Ritual_Interpretation_Design.md](Wonder_Ritual_Interpretation_Design.md) 是设计输入；其中“已确认”不构成脚本已实现或引擎行为已验证的证据。本文的“建议”也是待采纳方案，不冒充已经确认的新需求。

配套 [逐工程审计清单](Wonder_Ritual_Interpretation_Audit_Inventory.json) 列出全部 192 个工程的 ID、类型、大小、流程、旧倾向、删除倾向后的基础国家效果、内容缺口及关键源文件 SHA-256。未知点以第 10 节的编号追踪；未经验证的机制不以“应该可以”关闭。

## 1. 审计结论与首版边界

这个方向可以实现，但不能只做“基础层删倾向 + 增加三个按钮”。最先必须处理的是**风格、流程、物理建筑、奖励和完成记录目前共用一套身份**。直接扩充 style 会让独特工程仍无法选择、跳过照常领奖、扩建重复冲击、易主后显示与效果不一致。

建议首版形成以下完整行为：

1. 基础工程不直接推动社会价值；所有正式诠释的方向都提前可见。
2. 完工进入“待诠释”，玩家选择三种诠释之一，或者“简朴落成”。选择预览可改，正式确认后锁定。
3. 正式诠释成功时统一结算：一次冲击、十年纪念期、持有期间遗产、一个主题奖励。流程和奖励载体分别定义。
4. 简朴落成不走仪式奖励分发器，保留工程基础功能。CMM“跳过仪式”仍是方便玩家的快速结算功能，必须与简朴落成区分。
5. 扩建只支付新增等级对应的冲击额度，不重新发放整套仪式奖励、不续十年纪念期。拆除重建和转手不能重置原国家的领奖额度。
6. 易主和彻底拆毁清理相关持续国家效果；旧诠释历史保存在地点。首版不提供有惩罚、有新分支的改奉玩法，但必须规定新所有者能得到什么。
7. 134 个共享八阶段仪式沿用共享流程；法罗斯和圣索菲亚保留专属玩法，通过适配入口接入三种诠释和统一结算，不能悄悄退回共享模板。

首版不增加赞助阶层、顺逆势差价、随机诠释争议、征服者改奉事件链。**AI、扩建幂等、初始工程、易主最低规则和条件轴失效处理不能推迟**，否则这是只在理想新建路径中可用的半套机制。

## 2. 证据及原稿修正

以下是实际读取的关键证据。行号用于本次审计定位，后续修改后以符号名为准。

| 编号 | 源码或数据 | 直接证明的事实 |
|---|---|---|
| E01 | `data/wonders.yaml`、`data/unique_wonders.yaml`，通过 `load_all_wonder_mechanics()` 加载 | 56 通用 + 136 独特 = 192；需要 576 个新诠释内容项。目前新结构为 0 项，旧仪式内容不能算作已完成的诠释 |
| E02 | `data/wonder_base_modifiers.yaml`；`_core.py:2201` 的 `wonder_base_country_modifiers()` | 56 条 `monthly_towards_*`，按等级及 unique 倍率缩放。删除后 27 个基础模板的国家效果为空，影响 92 个工程类型；其中全部 84 个 small 工程类型都没有剩余基础国家效果，但地方基础效果仍在 |
| E03 | `scripts_engineering_department/wonder_mechanics/_core.py:1423,1734,1912` | `ceremony_styles()` 从 `final_buildings` 取选项；136 个 unique 都仅 `[1]`；校验器强制 unique 单风格；134 个有 `ceremony` 的 unique 实际用通用 style 1 覆盖自己的国家奖励 |
| E04 | `src/in_game/common/scripted_effects/tv_engineering_department_effects.txt:2242,2283`；`.../scripted_triggers/tv_engineering_department_triggers.txt:423` | 完工初始化 unique 为 style 1 并锁定；共享仪式自动开始；选择 trigger 排除 unique。仅增加 unique 数据选项无法改变这些路径 |
| E05 | `scripts_engineering_department/wonder_ceremony_lib.py:26,65,71`；`.../gen_tv_wonder_ceremony_effects.py:107,124,147` | 134 个共享八阶段工程；第 2 阶段送对应 generic style 3 一次性奖励，第 4 阶段免费建对应 generic 附属建筑，第 8 阶段另发国家奖励。真实事件是 `.9300–.9307`，注释中的 121 座、10000–10007 已过时 |
| E06 | `.../gen_tv_engineering_department_wonder_mechanics_effects.py:1954–2100` | 正常、强制、即时、CMM skip 有多条领奖入口；skip 会送附属建筑、即时奖励和国家奖励。unique 的 CMM skip 由 E04 强制完成 |
| E07 | 同一生成器 `append_location_display_final_building_projection()`、`append_country_auto_level_map_effect()`；生成的 `tv_wonder_module_effects.txt` 中 `tv_wonder_detect_existing_wonder_at_saved_site_effect` | 建筑类型反查 style；generic 显示默认视作仪式完成；unique 依赖国家 completed map；基础国家 auto map 对同种工程取最高等级，不是逐实例相加 |
| E08 | `.../gen_tv_wonder_ownership_events.py:63`；`.../gen_tv_engineering_department_wonder_mechanics_effects.py:969` | 易主事件和彻底拆除会移除旧的单个仪式国家 modifier；已存在“仍持有同类工程则保留”的判断。新增三种诠释与纪念期不能只接在旧单 modifier 函数上 |
| E09 | `.../gen_tv_engineering_department_wonder_mechanics_triggers.py:54` | small 没有同类工程的全国唯一性限制；当前有 24 个通用 small 类型。因此国家级 `wonder_id` 不能代表所有工程实例 |
| E10 | `src/in_game/common/scripted_effects/tv_engineering_department_ai_effects.txt:355`；`docs/design/Engineering_Department_AI_Plan.md` | AI 当前固定选 style 1；操作由 ED 国家驱动器执行，原生 generic-action AI 未承担此职责；共享阶段事件推进概率固定 100 |
| E11 | `.eu5-base/reference_game_files/game/in_game/common/societal_values/00_default.txt` | 3 条时代轴、3 条有 allow 的轴；不是仅有 DLC 判断。汉化轴有文化、首都区域、附属/组织条件；神秘轴依赖 `allow_mysticism_vs_jurisprudence`；拉丁化轴同时要求 DLC 和曾为 BYZ |
| E12 | 原版 `main_menu/common/script_values/default_values.txt:405–425`、`loading_screen/common/defines/00_defines.txt:169–171`、`in_game/common/scripted_effects/country_effects.txt:1136`；官方 `docs/effects.log:1092`、`docs/triggers.log:5986` | country scope 支持 `change_societal_value = { type = 轴 value = 数值 }`、`has_societal_value`；向左是负，向右是正；范围 -100…100；惯性参数 100；标准月推力 0.1，tiny 0.025，large 0.2。**未证明实际位移等于月份乘推力** |
| E13 | `scripts_engineering_department/wonder_mechanics/_core.py:2248` | 附属建筑还会自动附加对应人口阶层的地方权力 +0.5；只改作者填写的奖励表会遗漏这项效果 |
| E14 | `tv_engineering_department_effects.txt` 中 `tv_wonder_apply_finalization_visible_rewards_effect` 及其 helpers | 仪式外还有统治者/工程师属性、国家/地方庆祝修正、繁荣和国内支持兑换奖励；“无仪式奖励”的范围必须明确 |
| E15 | `data/generated_files.yaml`、编辑器 `services/wonder/{fields,model,options,localization}.py`、`unique_wonders_site/scripts/build/build_wonders.py` | 多个生成器、编辑器和图鉴读取旧 style 结构；内容数据改形后这些消费者必须同步 |

上述 `.../gen_*.py` 均指 `scripts_engineering_department/in_game/common/` 下对应目录中的生成源；完整模块名见第 8 节。

对原稿的具体裁定：

| 原稿主张 | 审计意见 |
|---|---|
| 192 × 3 约 576 | 数量正确；应按恰好 576 个有效内容项验收，而不是“约”或生成占位即完成 |
| 独特工程八阶段只需重写第 8 阶段 | 仅对 134 个共享流程有条件成立；还必须删除第 2、4 阶段旧通用赠品。法罗斯没有这套八阶段结构；圣索菲亚的八步是另一个系统 |
| 简朴落成复用现有 skip | 不成立；现有 skip 的含义是免等待/免成本领奖。应复用重型落成调度器，不复用 skip 奖励链 |
| 6 级 unique 十年 33，旧 72 | 在原始输入累计的口径下：18 + 0.1×120 + 0.025×120 = 33，旧 0.6×120 = 72。33 包含十年内遗产已同时生效；若遗产十年后才启动则是 30。两者都不是实测位移 |
| 遗产仅旧值 1/24，叠加不会锁轴 | 1/24 仅比较一座 6 级 unique 的 0.025 与 0.6。与 1 级 generic 比是 1/2；24 个来源又是 0.6；若不失去工程，100 年单来源原始输入为 30。没有全国聚合规则，无法承诺不锁轴 |
| 每种奖励约两个基础等级，三种等强 | 仅是目标；国家固定效果、地方随级缩放、一次性资源不能靠相同数值或相同字段数证明等强。small 删除倾向后的国家基础单位还是空的 |
| 同 base_key 不能出现相同方向集合 | 能检测重复，不能证明历史合理性或玩法差异。完全禁止会诱导为凑组合编故事；建议重复进入人工审查，可用证据说明例外，不能机械换轴 |
| AI 首版简单处理即可 | 算法可以简单，但 AI 选择、成本可付性、无有效目标和事件延期处理均是首版交付项 |
| `estate` 暂存但不生效 | 不应预先填充无效玩法字段。若保留作作者元数据，必须明确不是成本/权力/满意度效果；旧 annex 自动 +0.5 也必须显式迁移或删除 |

现有 `test_wonder_mechanics_rules.py` 本次运行通过：192 wonders、136 unique。该结果只证明旧架构符合旧测试。测试甚至明确要求 unique 只有 style 1、skip 送奖励、shared stage 2/4 发赠品，不能拿来证明新设计正确。

## 3. 玩家在游戏里实际怎样操作

### 3.1 新建与初次诠释

施工阶段照常。宣布建成后的国内支持 +20 作为施工结果保留；随后显示“选择落成方式”，**不自动开仪式、不默认替玩家确认 style 1**。

顶部一直显示工程名、地点、等级、当前基础效果，以及“基础功能已由工程等级决定；落成方式决定社会价值和额外奖励”的说明。三张互斥卡至少展示：

- 诠释名称与一段当前统治者可采用的仪式说明；历史依据放在展开说明。
- 轴的两端、当前位置、所选方向。左右方向不能仅靠绿色/红色暗示强弱。
- 本次可用冲击额度，纪念期强度/期限，持有遗产强度；受全国上限影响后的实际贡献另列。
- 全部主题奖励、适用范围、是否随等级增长，以及已有同类奖励导致本次不能重复领取的提示。
- 总成本、分阶段成本、预计最短耗时和暂不可选原因。条件不满足的卡保留可见且禁用。

卡片选择只做预览。正式按钮显示“以【诠释名】举行仪式”，第二步确认列出成本和锁定含义。三卡之外始终有“简朴落成”；其确认明确“基础功能完整保留；不获冲击、纪念期、遗产或额外仪式奖励”。

### 3.2 正式仪式进程

建议试运行时：通用工程统一采用 12 次月度推进的轻量流程；同一工程三种诠释使用相同启动成本，初始成本取 1 个目录中的 `scaled_gold` 单位。它是试验参数，并不把 `scaled_gold` 当成月结余；确切换算沿用现有 `change_gold_effect` 定义并在 UI 显示。此调整会替换旧 generic 三种不同耗时/代价，必须在 P0 明确采纳。

134 个共享 unique 保留八阶段，每阶段最快间隔 3 次月度推进，理论最短约 24 个月另加事件延迟。第 1–7 阶段机械成本三种诠释共用；第 8 阶段成本也共用，标题、描述、支付/延期选项按所选诠释变化。删除旧第 2 阶段通用奖励、第 4 阶段通用 annex，防止一座工程同时领多个风格包。

法罗斯和圣索菲亚保留原有挑战、角色和事件；在其开始前选择诠释，成功完成后使用诠释终章。法罗斯应使用“完成航线挑战后的终章”，不硬称“第八阶段”。专属过程中的既有额外收益列账审查，不能在新主题奖励之外无记录地保留。

各阶段“稍后再办”不收费，不增加阶段，不产生奖励；三个月后重新提示。支付选项必须检查真实资源/人物存在，不能只靠一段成本 tooltip；可付性不成立时禁用支付选项且保留延期。一个阶段同时最多存在一条待处理事件，避免暂停、保存读取或多次 pulse 造成重复付费。

### 3.3 中断、完成与界面反馈

普通玩家在确认前可以任意换诠释。确认后不允许通过切卡改变方向；主动放弃可回到简朴落成，已支付费用和已承担的五年负面修正不返还。无主题收益提前发放，不能先领第 2 阶段奖励再放弃。

若条件轴在仪式中消失：暂停在当前阶段，提供“改选其余可用诠释”或“简朴落成”，保留已支付阶段，不额外罚费；此例外必须显式记录，不能后台自动换轴。若条件轴在完成后消失：其价值观纪念期/遗产暂停，原十年到期日继续走；若恢复且未到期则恢复剩余纪念期。主题奖励与该轴是否存在分别判断，不重新给冲击。

最终确认后显示真实变化、贡献上限、奖励与期限；地点面板保存所选诠释、现任受益者和剩余纪念期。国别社会价值 tooltip 显示 ED 的净推力及来源数，包含正反方向抵消；不能只显示原始 0.1/0.025 而让玩家误以为全部叠加。

## 4. 建议采用的数值与重复收益规则

### 4.1 三段式的精确定义

| 项目 | 建议试验值 | 开始与结束 | 等级/重复规则 |
|---|---|---|---|
| 一次冲击 | generic 每新增计奖等级 2；unique 每新增计奖等级 3 | 最终结算成功时发生 | 下述全国同类型最高已计奖等级；不是每次 L×系数重发 |
| 纪念期 | 每有效来源向该方向 0.1/月，10 年 | 首次正式完成时开始；十年后终止 | 同来源扩建不续期；不随级；同类型同方向全国至多一个贡献 |
| 遗产 | 每有效来源向该方向 0.025/月 | 完成当日即开始，与纪念期并行；所有权丢失/彻底拆毁停用 | 不随级；同类型同方向全国至多一个贡献 |
| 全国纪念期上限 | 每方向 0.2/月 | 由有效来源聚合 | 两端各自封顶，然后相减；仅限制 ED 自己的贡献 |
| 全国遗产上限 | 每方向 0.1/月 | 同上 | 不限制原版与其他 mod 的贡献；不能据此保证最终不达 ±100 |

全国上限是本次**新增建议**，原稿没有这一规则。0.2/0.1 仅取原版量级作为试验上限，仍需 M01 长期实验决定。原稿的无上限方案应作为对照实验，不应作为“不锁轴”的已证实方案发布。

每轴每方向先将同一 `wonder_id` 的多个有效实例取最大贡献，再对不同类型求和并封顶：

```text
commem[d] = min(0.2, Σ_type max_instance(active_commem × 0.1))
legacy[d] = min(0.1, Σ_type max_instance(active_legacy × 0.025))
ED 向某端的输入 = commem[d] + legacy[d]
```

正反两端分别算；两个端点都不为空时允许抵消，界面显示抵消结果。纪念期从正式完成日起计时；占领不等于所有权变更，不因单纯被占领暂停，避免把军事控制与法定所有权混用。

### 4.2 扩建、拆建及小工程

保留项目级完成记录，并额外在国家保存 `shock_highwater[wonder_id]`，范围 0–6。结算等级为 L，冲击只支付 `max(0, L - highwater) × 系数`，随后写入 `max(highwater,L)`。额度跨同类型不同地点和诠释共用，拆毁、失地、改名/标签变化不主动清除；不以当前 slider 位移倒算“有没有领到”。

这样 1→6 的 unique 总冲击是 3+15=18；直接 6 是 18；连续提交同一 6 级、拆掉重建、同类 small 再建一座，均不能再次领取相同额度。达到 ±100 后溢出不兑换资源、不回存额度；UI 提前提示可能截断。

每个实例的主题奖励只结算一次；扩建不重领一次性资源、不续庆祝、不续纪念期。永久主题奖励按一次设计完整给付，地方 annex 固定 1 级，其值按目标“两基础等级”预先写入，不随主体 L 放大。

这里“只结算一次”指取得奖励资格一次，不是永久载体只能创建一次。拆至 0 后在同地重建，应恢复该实例原诠释的持有收益和必要载体，不再发送一次性奖励或重开纪念期；必须区分 `theme_entitlement_granted` 与 `theme_source_active`。已正式诠释工程被他国获得时，该国的 highwater 至少抬至所获等级但不发冲击；以后 3→4 的扩建只能支付新增一级，不能因新国家的计奖表原为空而补发四级冲击。未诠释既存工程的首次正式仪式不适用这条承接规则。

24 种可重复 generic small 另有套利风险：建议首版它们的三种主题奖励**统一使用各自地点的永久效果**，每实例一个 1 级载体，禁止一次性国家资源/永久国家主题奖励。这仍允许每种工程手工写三种主题，避免把一次性国家奖励刷取和国家同名 modifier 不叠加的问题混入首版；是需要采纳的内容限制，不是已有规则。若坚持为这些工程提供国家/一次性奖励，必须先替换为明确的全国同类型奖励预算，不能简单逐地点发放。

92 个移除倾向后基础国家表为空的工程，应显示“无基础国家效果”，继续显示其地方效果。不要为了填空再塞回新的不可选倾向，也不要用空 modifier 强行生成一个国家增益。

### 4.3 主题奖励预算

同一工程三诠释优先使用相同载体；必要时允许不同载体，但需单独审核范围、生命周期和机会成本。以每级原有**非倾向**基础单位作为可参考量级，不能拿已删除的倾向当数值兑换率。

国家奖励、地点奖励、一次性奖励分别建预算，不直接相加比较。至少检查早/中/晚三种经济与人口规模、L=1/3/6、短期与十年持有、地方收益/国家税收区别、解锁类布尔值是否真有价值。small 无国家基础单位时用地方基础单位；无相应单位的效果必须给原版参照与设计理由。原稿列的 10,000 金等奖励不得自动按旧数搬入。

《Great_Project_Unique_Buff_Proposal.md》的“136 工程各一个全局不重复国家 modifier key”与本方案 408 个 unique 主题、且可选不同载体存在范围冲突。建议不把严格 key 唯一性作为诠释首版硬门槛，改为主题与收益组合去同质化；如仍要保留严格唯一，必须先完成可用原版 modifier 供给/分配审计，不能一边声称实现一边默默放弃。

旧 annex 自动阶层权力 +0.5 不再自动追加；需要保留的由作者写入主题奖励预算。原稿保留的 `estate` 只可作为元数据，首版不读取执行。初始 `monthly_towards_*` 只能由诠释聚合层输出，主题奖励不得暗藏第二条社会价值推力；原版某些社会价值端点自身引发的其他轴推力另行说明，不由 ED 伪装消除。

## 5. 状态模型、结算与生命周期

### 5.1 必须拆开的身份

| 身份 | 建议存储 | 意义与不变量 |
|---|---|---|
| 工程类型 | 现有 `wonder_id` | 1–56、101–236；保留，不重排 |
| 工程实例 | 地点 + `wonder_id` | 支持同地多工程、同类多地点；禁止只在国家保存一个 style |
| 物理成品 | 每类型一个 `final_building` | 同种工程三诠释和简朴共享基础物理工程；不再用建筑 key 证明诠释 |
| 诠释 | 实例记录 `interpretation_id` | 0=简朴，1/2/3=正式；未选择单独用状态表示，不能把 0 同时当 unset |
| 进程 | `state`、阶段、pending token、process key | `awaiting_choice / in_progress / finalization_pending / settled / interrupted` |
| 已结算收益 | 实例 `theme_paid`、`settled_level`；国家 `shock_highwater` | 已选风格、开始流程、完成结算分别记录，不能共用一个 locked/completed 布尔量 |
| 受益所有者 | 实例 `beneficiary_country` | 历史诠释与现任受益国家分离；不从旧 country completed map 推断历史 |
| 纪念期 | 实例起始与到期信息 | 持久化，扩建、读档和收复不重置；具体日历 API 由 M03 验证 |
| 跨拆毁记录 | 地点实例计奖记录、国家额度 | 最后一级拆除仍保留防刷记录；可见历史可以消失，计奖额度不能消失 |

单一 `final_building` 是建议的数据重构，避免 unique 为三种观点复制三座相同工程，再为 neutral 复制第四座。generic 当前三个成品的 `final_attributes`、维护和允许地点有差异，必须逐类型审查，确定统一后的属性；不能随手选 style 1 作为成品然后宣称基础功能全保留。

在当前脚本实现中，可用 location 的多张 `variable_map` 以数字 `wonder_id` 作 key 承载实例字段；不同字段不同 map，避免 GUI 运行时拼接 key。临时项目保留选定地点与 ID，但持久记录落在 location。country maps 仅存全国额度和聚合缓存。精确读写语法先核对官方参考并沿用“保存 scope/local value、先删后写”的现有路径，不把 iterator scope 直接当 RHS。

### 5.2 结算只有一个入口

建议新增规范入口 `tv_wonder_settle_interpretation_effect`，所有正式完成、专属完成、CMM 快进均调用它。简朴使用同一事务调度，但走 `interpretation_id=0` 分支，完全不调用奖励包。名字为实施建议，不是当前已存在的 effect。

结算步骤：

1. 核对国家、地点现任 owner、工程类型、等级、正式选择、过程终点和 pending token；校验当前 `has_societal_value`。过期/重复事件直接结束，既不扣钱也不发奖。
2. 建立待结算快照：地点、类型、诠释、等级、已计奖等级、费用及结果摘要。事件延期期间不允许新项目覆盖这些值。
3. 显示轻量实际效果预览；最终确认只调度隐藏事件。重型建筑转换、地图状态、聚合刷新在隐藏事件 `immediate` 中执行，不把 `hidden_effect` 当作悬停隔离边界。
4. 隐藏事件重新验证 token 和 owner，完成成品建筑/附属载体操作；确认没有落到错误地点后，写入不可重复的结算记录，发放本次差额冲击和首次奖励，设定纪念期，再刷新 ED 聚合缓存。
5. 完成通知从已持久化的结算结果读取；清理施工临时状态，保留实例历史/额度。日志写一次。

Jomini 没有在此已证实的数据库事务回滚；不能许诺真正原子。M02 必须验证同帧事件串行、同链变量可见性、建筑完成后记录时序。如果真实构建失败，不能仍发奖/消耗额度；不能以重复执行整个奖励块修复建筑。必要时拆为 `prepared → building_confirmed → rewards_committed` 三个持久提交步骤，每步只做自己的效果。

旧 `tv_wonder_mechanics_maybe_complete_active_ritual_effect`、`force_complete`、`apply_immediate` 的直接奖励逻辑改为提交该入口；旧 static modifier 分发器不再自行授予完成身份。施工 `on_built` 不能作为唯一完成信号，沿用已有 `on_construction_ended` + 隐藏完成同步结构。

### 5.3 易主、初始状态与失败矩阵

| 场景 | 建议首版行为 |
|---|---|
| 新游戏预置工程 | 不追授原作者的政治立场。初始化为“既存、尚未由本国诠释”，基础效果正常；允许一次“为既存工程举行仪式”，即使已满 6 级，不能强迫先扩建才有选项 |
| 初始选择简朴 | 正式关闭本实例首次仪式机会；首版没有以后免费再办的按钮；不能通过扩建解锁重新挑选 |
| 同一所有者扩建 | 沿用本实例诠释或 neutral；只更新基础等级、结算冲击新增额度；不重走八阶段/两种专属挑战、不重发主题包、不续期 |
| 仪式中失去地点 | 中断本项目，沿用现有施工失败代价；不给最终包。旧事件验证 owner/token 后失效；未完成工程和 surviving work 仍由现有工程续建链管理 |
| 完成后失去所有权 | 从旧国家聚合中移除此实例的纪念/遗产及国家主题来源；一次冲击、已得资源、已承担成本不倒扣。地点主题载体随土地保留（作为历史资产），不会复制到旧国家 |
| 新所有者获得正式诠释过的工程 | 首版自动承接历史诠释的持有收益：遗产和永久主题、未过期纪念期的剩余时间；不获新冲击和一次性奖励。不提供换风格，完成通知说明承接规则 |
| 新所有者获得 neutral/未诠释工程 | neutral 仍 neutral；未诠释可以走首次仪式。不得将“当前国家未领奖”误判成“全世界此实例从未诠释” |
| 原国家收复 | 恢复持有收益和原未过期纪念；不重发首次包，国家 highwater 保留。十年已过则只恢复遗产 |
| 部分等级拆除 | 基础效果降低；已取得主题和持有遗产不随级缩放；计奖 highwater 不降，不能降级再升刷差额 |
| 最后一级拆除 | 停止该实例所有持续效果，清除附属收益载体；计奖记录保留防刷。其他地点同类同方向仍有效的必须继续贡献 |
| 另建同类 small | 每地点可选诠释；地方主题一次；冲击共享全国同类型额度；纪念/遗产同类型同方向最多一个贡献，并受全国上限约束 |
| 通用/unique 过程取消 | 已付不退；未付不扣。可选择简朴落成；不从任何阶段回调漏出收益 |
| 政体/宗教/文化/首都/DLC 条件变化 | 复核可用轴；在途暂停并允许受控改选；完成后暂停不适用的轴推力，持续期限不冻结，主题按自身适用条件处理 |
| 国家灭亡、复国、合并、释放属国、形成新标签 | 按实际 location-owner 事件重绑来源；国家对象/变量是否保留属 M04，不能只依赖可见国名；一次性收益不能因改旗重领 |
| 读档/多人相继点击/旧事件弹窗 | 读持久实例状态；token 匹配才执行；load 不发奖、不延长日期。无读路径补状态的旧存档兼容层 |

“自动承接旧诠释”的最低易主规则是本次建议，区别于原稿留待未来的“改奉新诠释”。若设计方要求新所有者只拿基础效果而不承接，必须在 P0 选择另一规则，并同步地点 annex 的所有权效果；不能让国家奖励不转移而地方奖励自动转移却称三种等强。

继承的地方永久效果是地点资产；其国家奖励按当前 owner 的同类型来源重新聚合。布尔解锁不得按来源数相加。同一国家拥有同类型不同诠释时，国家主题的每个解释 ID 至多生效一次；medium/large 的重复通常来自征服，仍必须支持。

原有“仍持有同类工程就保留 modifier”的判断必须细化到对应主题/方向的有效来源；保留一座不同诠释的同类建筑，不能替已经失去的诠释续奖。聚合刷新挂在结算、owner 变化、建筑同步和到期等生命周期点；条件轴相关政体/宗教等变化若没有可靠回调，至少在 ED 月度维护复核，并在 M06 中记录最长生效延迟，不能靠 GUI 悬停触发修复。

## 6. 数据、内容与可用性契约

### 6.1 数据建议

不在旧 `style_1/2/3` 外再造一层兼容 alias。建议统一以下结构，字段名在 P0 固化：

```yaml
# data/wonder_interpretation_rules.yaml（新建，数值单一来源）
rules:
  shock_per_new_level: { generic: 2, unique: 3 }
  commem_monthly: 0.1
  commem_years: 10
  legacy_monthly: 0.025
  commem_cap_per_direction: 0.2
  legacy_cap_per_direction: 0.1
  shock_budget_scope: country_wonder_type
  instance_key: location_wonder_type

# data/unique_wonders.yaml 中单个条目；下例展示结构，不是已通过史实审查的内容
final_building: tv_wonder_unique_hagia_sophia_inaugurated
ritual_process: { kind: bespoke, key: justinianic_synaxis_of_the_great_church }
interpretations:
  - id: 1
    axis: spiritualist_vs_humanist
    direction: spiritualist
    name: { en: Patriarchal Consecration, zh: 牧首祝圣 }
    description: { en: "...", zh: "..." }
    rationale: "537 年开放及其宗教功能的历史依据；人物细节另证。"
    evidence:
      - source_id: hagia_opening_537
        url: https://www.ktb.gov.tr/EN-113776/ayasofya-hagia-sophia.html
        claim: "现存建筑于 537 年开放；不能据此证明梅纳斯主持细节。"
        checked_on: 2026-10-21
    reward:
      kind: country_modifier  # 三种载体之一
      modifiers: { tolerance_own: 1 } # 仅举结构；不是平衡定稿
    final_stage:
      title: { en: "...", zh: "..." }
      description: { en: "...", zh: "..." }
      option_pay: { en: "...", zh: "..." }
      option_delay: { en: "...", zh: "..." }
      icon: religion
# id 2、3 必须完整，省略号不能进入正式数据
```

generic 在 `data/wonder_generic_rituals.yaml` 中使用相同 `interpretations`，并保存与主题奖励独立的 `ritual_process`、`cost`。unique 的旧 `ritual` 应拆成纯专属过程定义和诠释奖励；保留 listeners、runtime_variables、过程 hooks，删除与新统一结算重叠的 `country_modifier/reward` 字段，或迁移到作者明确标记的过程收益表。不能把一整个旧 ritual 包复制三次后叠加领取。

奖励可取 `country_modifier`、`local_annex`、`one_shot`；严格判别联合类型，只允许一个主载体。一次性奖励继续用带作用域的目录条目，不接受未经审查的自由 effect 文本。国家奖励限定 country 类 key，地方奖励限定 location 类 key；非本国 ruler/artist、无适用政府资源、已满科研/人力等情形必须有专门规则。

轴、端点、向左/右符号、年龄、allow 证据放到一个生成/校验用轴目录中，从本地原版提取并人工确认。运行时统一检查 `has_societal_value = societal_value_type:<axis>`，不要给三个地方分别手写不同的 allow 逻辑。axis 与 direction 不一致直接报错。

### 6.2 自动审计与人工审计分开

**自动硬门槛：**

1. 192 个类型各恰好 3 项；id 1/2/3 唯一；无旧 style schema；无缺失双语或占位文本。
2. 三个方向两两不同，至少两条轴；至少两个选项所用轴在当前目标原版无 age/allow 限制。另做真实国家条件矩阵，防止奖励前置把“无条件轴”变成无可用仪式。
3. 有效轴、端点、scope、modifier、图标、价格、event ID、本地化键、资源单位；所有新依赖都在 standalone ED 根或声明依赖中。
4. `rationale` 和 `evidence` 完整、claims 不为空。自动化只验证记录存在，**不声称验证史实为真**。
5. `monthly_towards_*` 在基础国家、最终建筑、主题 payload、旧仪式赠品中全部为零；只允许专门社会价值聚合输出。检测 generator 正文，不能用全项目字符串简单计数，因为文档/目录会含合法名称。
6. 总奖励预算、small 载体限制、annex 1 级、预算额度及持续时长、无意外 +0.5；确认所有旧奖励入口已替换，所有结束路径可达唯一结算入口。
7. 同 base_key 方向组合重复、文本和奖励组合近似出报告；人工说明未通过则不算内容验收。
8. 事件号全命名空间去重并符合 0–9999；不照旧注释分配到 10000 以上。图鉴/GUI/事件共用数字路由，不能运行时拼 flag 当 key。
9. 中断、重复结算、扩建、neutral 和 owner 变化符合状态契约，清理覆盖全部新增运行变量；保存/读取期间不重复初始化已完成实例。

**人工硬门槛：**每项“历史事实是否支持仪式叙述”“事实到方向/奖励的推导是否合理”“三项是否确有不同玩法”分别签审。三方向不同不代表三个奖励有差异，历史确有一场典礼也不代表它天然支持某个社会价值。

### 6.3 内容工作量与历史问题

范围是 576 张诠释卡、408 个 unique 终章（含两种专属流程的终章），双语文本；134×7=938 个共享前置阶段也要逐项审查是否真的能与三种诠释共用。现有 136 份 bespoke 设计/spec 不是 136 个已加载的专属系统，更不是本次 408 项内容已经完成。

原稿示例中，凡尔赛 1664 年盛会的存在可由[凡尔赛宫官方历史页面](https://en.chateauversailles.fr/discover/history/key-dates/party-delights-enchanted-island)核实；“所以朝贵族方向推动”仍属设计推导。圣索菲亚 537 年开放可由[土耳其文化部门资料](https://www.ktb.gov.tr/EN-113776/ayasofya-hagia-sophia.html)核实；这份资料未证明原稿中的牧首人物细节或 1452 合并宣告。威尼斯“一宴造一船”、长城三分支、泰姬陵年祭等本次未取得足以关闭全部相关 claim 的一手/机构证据，保持待核实，不能写成已审核。

还存在时间与身份错置：玩家在 1337 年之后可能提前建凡尔赛，也可能由异教统治者接管旧宗教建筑。共享前置阶段若让早已去世的哈里发现场下诏、强迫不相容宗教祝圣，就不能宣称“第 1–7 阶段三种共用”。建议用“重申旧制/启用/纪念”的当前行动文本，历史人名年代放依据；尚未发生的具体史实只作为作者参考，不写成当前国家已发生。若确需特定身份门槛，必须计入至少两种始终可行方案的审核。

建议先做 8 个垂直样本：通用天空穹顶神庙、星形要塞城市、殖民贸易公司；独特凡尔赛、威尼斯军港、长城；专属圣索菲亚与法罗斯。覆盖 conditional age 轴、small 重复、多载体、existing unique、两种 bespoke。样本通过后，再按 56 个 base 家族扩展，11 座星形要塞和 8 座大教堂单列反同质化审核。

## 7. AI、提示与操作限制

把 AI 选择放进现有 ED 国家驱动器，替换固定 style 1，不开启 native generic-action AI。简单算法也必须可确定、可解释：

1. 筛掉不存在的轴、奖励无适用对象、无法开始/无可付预算的选项；不要为了读当前值先读取不存在的轴。
2. 将 slider 值归一到 [-100,100]；左向 `alignment=-value/100`，右向 `alignment=value/100`。取 alignment 最大者，0 为中性；同分先取已定义的主题适用优先级，再按固定 id 破同分。跨轴比较是 AI 启发式，不是玩家效用证明。
3. 不因下一月偏好变化重新选卡；确认后锁定。预计阶段成本进入预算。阶段支付受约束，不再不管可付性一律 100% 推进。
4. 所有有效正式选项都预算不足时延期；连续等待达到试验值 24 个月后选择简朴，避免占用项目永远卡住。该超时值可调，不能伪装已实测。
5. 玩家全局 CMM 不影响 AI。AI 与玩家共用可用性、付款、结算、日志和 owner/token 防重逻辑；直接 effect 不会自动扣 generic action 的 price，不能漏付或双付。

玩家的 CMM“跳过仪式”建议改为：**仍先选方向**，确认后快速完成相同诠释、相同限额的最终奖励，不自动选 style 1；是否免成本沿用当前该设置的明确说明。它不同于简朴落成，不能被 AI 当作免费收益入口。设置在项目开始时快照，进行中切换不追溯重算已付成本。

基础效果 tooltip、选择卡、事件支付预览、终章、地点卡、百科、完成/易主通知和图鉴必须使用同一 normalized plan。中英双语都说明期限与持有条件，不把所有“向某方向”着色为绿色；价值取舍是中性的。

## 8. 按文件落地的改动清单

路径以仓库根为基准；仅修改生成源及 canonical data，再生成输出，不手改生成 txt/gui/yml。

| 工作面 | 需要修改的入口 | 具体改动 |
|---|---|---|
| Schema 与 normalized plan | `scripts_engineering_department/wonder_mechanics/_core.py`，及 `schema.py/io.py/rituals.py/naming.py` 导出 | `interpretations`、process、reward 联合类型；去掉 unique 仅 style 1 限制；替换按 final_buildings 推导选项的函数；拆分 completion / selection / building naming；空基础国家表合法 |
| Canonical data | `data/wonder_base_modifiers.yaml`、`wonder_generic_rituals.yaml`、`wonders.yaml`、`unique_wonders.yaml`、`wonder_final_buildings.yaml`、`wonder_localization.yaml` | 删除 56 倾向；补 576 项；统一物理成品并审属性；迁移 134 共享奖励和 2 专属 hooks；新增规则/轴目录来源 |
| 运行手写状态与 action | `src/in_game/common/scripted_effects/tv_engineering_department_effects.txt`、`.../scripted_triggers/tv_engineering_department_triggers.txt`、`.../generic_actions/tv_engineering_department_actions.txt` | 完工进入待选；去 unique 自动 style 1；独立 neutral action；按每选项真实条件授权；新建既存工程首次诠释入口；所有 paid action 真实扣费 |
| 仪式和最终结算生成 | `scripts_engineering_department/in_game/common/scripted_effects/gen_tv_engineering_department_wonder_mechanics_effects.py`、`gen_tv_wonder_ritual_effects.py`、`gen_tv_wonder_finalization_effects.py` | 单一提交入口；快照/token/幂等；去多入口发奖；neutral/扩建分支；实例状态与全国聚合；原完成庆祝等包分账 |
| 共享阶段 | `wonder_ceremony_lib.py`、`in_game/common/scripted_effects/gen_tv_wonder_ceremony_effects.py`、`in_game/events/gen_tv_wonder_ceremony_events.py` | 移除 stage 2/4 旧赠品；stage 8 按诠释派发；支付可付性、pending token、延期不付费；纠正过时计数和事件号注释 |
| 专属流程 | `unique_wonder_ritual_content/{hagia,pharos}.py`、`gen_unique_wonder_rituals.py` | 保留挑战，提前选诠释、终章分流、统一完成；列账既有中途奖励、清理变量/listeners、控制角色失效与永久停滞 |
| 成品与附属载体 | `in_game/common/building_types/gen_tv_engineering_department_wonder_mechanics_buildings.py`、`in_game/common/static_modifiers/gen_tv_engineering_department_wonder_mechanics_modifiers.py`、`main_menu/common/static_modifiers/gen_tv_engineering_department_wonder_ritual_auxiliary_location_modifiers.py` | 物理成品与诠释无关；主题载体独立，最多 1 级，去隐性阶层权力；保留原本地方和全国分域 |
| 基础与价值观聚合 | `in_game/common/auto_modifiers/gen_tv_engineering_department_wonder_mechanics_auto_modifiers.py` 及 effect 生成器 | 基础不再含推力；新社会价值贡献读取明确缓存，封顶；不按每次 GUI render 扫世界、不创建 576×等级的静态 modifier 组合 |
| 扩建/检测/展示 | `in_game/common/scripted_effects/gen_tv_wonder_module_effects.py`、`gen_tv_wonder_location_display_effects.py`、`gen_tv_wonder_index_effects.py` 及实际共享实现 | 删除建筑→style 的事实来源；从实例记录恢复诠释；国家计奖额度与地点已付记录分别读取；通用不再默认仪式已完成 |
| 初始化/易主/拆毁 | `gen_tv_wonder_ownership_effects.py`、`in_game/events/gen_tv_wonder_ownership_events.py`、`append_existing_unique_wonders_initialization_effect()`、`append_final_building_level_changed_effects()`、CMF/on_action 接线 | 初始未诠释；转移来源和剩余期限；删除最后来源才撤效果；不清计奖额度；现有未完工程续建/失败代价不丢失 |
| AI 与提醒 | `src/in_game/common/scripted_effects/tv_engineering_department_ai_effects.txt` 及 AI triggers、chief alert | 算分选卡、预算/延期/超时简朴；新待选状态可触发提醒；不继承玩家 CMM 调参 |
| 选择和阶段 GUI | `in_game/gui/panels/organization/gen_tv_engineering_department_wonder_mechanics_gui.py`、`gen_tv_wonder_ceremony_cards_gui.py` 和对应 merge 脚本；location-window 生成源 | 三卡+neutral；禁用原因；扩建锁定标识与首次确认分开；额度/期限/上限展示；专属终章适配；重建 fragment 后重新合入面板 |
| 事件/选项本地化 | `in_game/common/customizable_localization/gen_tv_wonder_ceremony_options.py`、两语 `gen_tv_wonder_ceremony_l_*.py`、`gen_tv_engineering_department_wonder_mechanics_l_*.py`、ownership loc 生成源 | stage 8 路由包含工程 ID+诠释 ID；标题/描述、支付/延期都覆盖；不以全局英文 fallback 掩盖缺项；YAML UTF-8 BOM/ASCII 引号 |
| 百科/图鉴/编辑器 | `in_game/gui/gen_tv_encyclopedia_wonders_cards_gui.py`、对应 merge；`unique_wonders_site/scripts/build/build_wonders.py`；`great_projects_editor_web/services/wonder/` 与 `static/wonder_rituals.js`、`static/wonder_editor.js` | 新 schema 读写、双语及方向证据编辑、奖励/可用性预览、stage 8 对应关系；图鉴不可继续展示自身未生效旧 reward |
| 验证和依赖登记 | `data/generated_files.yaml`、`test_wonder_mechanics_rules.py`、仪式 audits、相关 editor tests、`data/unique_wonder_ritual_specs.yaml` 的生成源 | 注册新 canonical 依赖；替换旧单风格/skip/赠品断言；新增语义场景；明确旧 design-only specs 与当前流程关系，不让 harness 覆写新 schema |
| 兼容与知识 | `scripts/compat/` 相关已登记 UI 合并器；`docs/knowledge/risk_cards/{wonders,wonder_ceremony,wonder_unique_rituals,wonder_gui}.md`、原设计/AI/奖励文档 | 重新生成受到面板修改影响的既有 compat 根；取消相互矛盾的旧规则；若知识源变更则重建 BRIEF |

所有新内容必须由 standalone ED 自己提供。不要把新逻辑写在主 `src/` 让独立 ED 缺 key。项目未发布，不新增旧存档迁移/旧 schema 回退；但新格式存档的保存读取正确性必须验证。

## 9. 工作包、验证与发布门槛

| 包 | 依赖 | 交付与结束条件 |
|---|---|---|
| P0 规格冻结与引擎小样 | 无 | 在第 10 节 D 项记录采纳/替代选择；完成 M01–M05 小样。先确认真实月推力、轴读取、计时、token/变量语义，再批量生成 |
| P1 轴目录、schema、内容审计 | P0 | 严格数据加载；8 样本三诠释有效；576 项覆盖报告按未写/未审/通过区分；不拿占位项补绿 |
| P2 实例与统一结算 | P1 | 初始/neutral/正式/扩建/拆除/易主/CMM 路径跑通；只一处发冲击/主题，原入口无旁路；单次事件重复执行不能多领 |
| P3 三条过程接入 | P2 | generic、134 shared、2 bespoke 都可从选择走到完成；共享旧赠品清零；专属挑战没有因选择方向被复制或丢失 |
| P4 UI、AI、双语 | P3 | 玩家可预测完整结果；AI 可付费推进和退出；禁用原因、剩余期限、继承显示正确；小窗口/中文长文本无溢出 |
| P5 全量内容 | P1 内容规则稳定、P3 样本通过 | 192 个工程/576 项方向+奖励+双语+证据人工通过；938 个前置阶段不冲突；图鉴与编辑器可往返编辑新结构 |
| P6 全局回归和平衡 | P2–P5 | 以下场景无误；无未知 P0 阻塞；依据长局实验定稿数值；生成依赖和知识更新完成 |

不要先把全部 576 篇文案写完再跑引擎小样；若轴推力实际机制或实例模型不成立，会返工全部内容。批次以 base 家族验收，每批明确列出 ID，不能只写“欧洲已做”。

8 样本阶段使用独立数据夹具/开发构建，只加载这 8 种新制工程；正式 192 条数据仍必须满足全覆盖校验，不为部分内容临时增加旧 schema 回退。P5 完成前不把样本构建当成全量发布物。

**静态验证：**数据/脚本/生成器 freshness、所有结束路径奖励审计、namespace event ID 去重、本地化闭包、独立根依赖、轴映射与条件矩阵、奖励目录合法性、同家族同质化报告、编辑器往返。现有命令需要替换旧断言后才能用于新方案：

```powershell
C:\Users\Hades\anaconda3\envs\eu5\python.exe scripts_engineering_department\test_wonder_mechanics_rules.py
C:\Users\Hades\anaconda3\envs\eu5\python.exe scripts_engineering_department\audit_unique_wonder_ritual_mechanic_similarity.py
C:\Users\Hades\anaconda3\envs\eu5\python.exe scripts\validate.py --changed --fix --ai-report
```

生成清单按 `data/generated_files.yaml` 拓扑顺序执行，并包含 fragment 的 merge、百科与相关 compat 合并。精确一键重建命令在 P1 确定，不假装现有某条命令已涵盖所有消费者。

**必须的游戏内验收矩阵：**

| 测试组 | 最低场景与预期 |
|---|---|
| 基础隔离 | 1/3/6 级 generic 与 unique，未选/neutral：ED 基础轴推力 0，地方与其他国家基础功能不丢 |
| 选项可用 | 1337 与相关后续时代；三条 allow 轴各种成立/不成立；无 DLC；至少两个正式选项可用；不存在轴不崩溃、不读取无效数值 |
| 方向与边界 | 左右各一项，slider=-99/0/99，冲击符号正确；±100 截断符合预览；原版端点自身连带推力识别清楚 |
| 月推力实验 M01 | 禁其他 ED 来源；对照/0.025/0.1/0.125，初值 -90/-50/0/50/90；记录首月、12/120 月和十年过期前后；加 1/4/8/24 个来源验证聚合和上限。实验比较输入与真实位移，不只看 tooltip |
| 生命周期计时 M03 | 10 年准确到期；暂停/读档不续期；扩建在第 9 年发生不重置；轴短暂失效/恢复不冻结十年；owner 转移保存原到期日 |
| 幂等 M02 | 同 stage 支付两次、同终章按钮两次、同回调两次、月 pulse 与事件同日、旧弹窗、新工程开始前旧隐藏事件、施工 callback 延迟；费用和包均只结算一次 |
| 扩建 | 1→3→6 unique 总冲击 18；直接 6 同为 18；generic 总计 12；主题一次，纪念期不续；neutral 扩建不变正式 |
| 多实例 | 两个同类 small 不同方向、三个同类同方向、同地多个不同工程；丢一个只减对应来源，丢最后一个才归零；基础同类 max 等级逻辑不被误改成 sum |
| 转手/拆建 M04 | 获得/失去/收复/局部降级/拆至 0/重建/合并国家/标签变化；旧国不留收益，新国不刷冲击；地方/国家主题继承符合统一规则 |
| 流程与费用 | generic 12 tick；shared 8×3 tick；shared stage 2/4 无旧奖；每阶段支付不足可延期；人物死亡/消失、无 artist/作品、研究/资源满值等不会吞费用后无结果 |
| 专属链 | 法罗斯航线无主/角色或路线失效可退出；圣索菲亚角色调派/死亡/八步完成；每个三方向+neutral、CMM 快进都接唯一结算 |
| AI | 当前值同向、反向、全轴中立、conditional 锁、无钱、破产、无工程师、24 月超时，均不会固定选 1 或永久占坑；付款与玩家同价 |
| UI/性能/多人 | 中英、低分辨率/较大 UI scale、悬停无重型反复扫描、多人同时操作同国家/同地点、联机再载入无重复收益；记录帧耗和月结耗时与原基线比较 |
| 部署组合 | standalone ED+声明依赖；主 mod+ED；每个受到 GUI 修改影响的既有 compat 组合；不能主 mod 正常就声称独立版通过 |

最终验收必须附游戏实际构建号、DLC、mod 顺序、起始国家/时代、存档/控制台步骤、观测日志、每个 unresolved 项状态。未实测不能写“惯性已处理”“不会锁轴”“多人安全”。

## 10. 未知点与设计缺口登记

这里的“建议已给”意味着本文给了可执行默认方案，**不表示设计方已经采纳**。“待测”必须取得运行证据；“待内容”必须补作者记录。所有 P0 项在进入全量实现/发布前关闭，P1 项在对应工作包验收前关闭。表外新发现的问题必须增号，不得无记录地用 fallback 隐藏。

### 10.1 产品/规则决策（D）

| ID / 优先级 | 缺口 | 本计划建议及关闭条件 |
|---|---|---|
| D01 / P0 | 三段式是并行遗产还是十年后遗产？ | 第 4 节选当日起并行；据此标记“原始十年输入 33”，采纳后统一文案/公式 |
| D02 / P0 | 全国叠加和“不会锁轴”的依据缺失 | 采纳每方向纪念 0.2、遗产 0.1 上限及同类型去重；M01 后定值，删除无证据保证 |
| D03 / P0 | neutral 是真正零仪式奖励还是少奖？ | 保留宣布施工完成的 +20 支持；不发诠释包、旧最终庆祝/属性/支持兑换包。正式包保留哪些通用庆祝，逐项列账定预算 |
| D04 / P0 | CMM skip 与 neutral 混淆 | CMM 为选后快结算，neutral 单独按钮；对免成本/免等待范围写清并快照 |
| D05 / P0 | 何时锁定、是否可以后悔？ | 预览可改，确认锁定；在途可弃为 neutral；完成后首版无自由改风格。未来政治转向仍可能嫌遗产碍事，是首版明确局限，不声称永久解决所有偏好变化 |
| D06 / P0 | 升级一次冲击发全额还是差额？ | 全国同类型 highwater 差额；拆建/转手不重置；不续期、不重领主题；确认是否接受对重复 small 的限制 |
| D07 / P0 | 已建成/满级初始工程怎样选择？ | 未由本国诠释的既存工程有首次仪式入口；不预填政治方向，不要求扩建；需核实开局批量 UI 压力 |
| D08 / P0 | 同类型多实例的效果怎么叠？ | 国家同类型同方向去重，地方各实例；24 generic small 首版只配地方主题；若拒绝此限制需先定义全国主题/一次性预算 |
| D09 / P0 | 征服者没有再奉献系统时拿到什么？ | 自动承接历史持有收益及剩余纪念，不拿冲击/一次性；neutral 不变；需正式选定，不能按载体各行其是 |
| D10 / P0 | 失地是否保留十年推力？ | 此实例全部持有推力从旧国移除，日期继续；恢复后只恢复剩余时间；冲击/资源不倒扣 |
| D11 / P0 | 条件轴在途/完工后失效 | 第 3.3 节暂停/受控改选规则；不换成近似方向；主题是否自身有条件单独定义 |
| D12 / P0 | 三个奖励载体与流程绑定、generic 时长/费用 | 建议统一 generic 12 tick+1 scaled_gold 单位；unique 共享成本；不让载体决定等待/收费；需确认这一经济调整 |
| D13 / P0 | 两套 bespoke 是否保留、是否强制八阶段 | 保留原挑战，独立终章适配；禁止为凑八阶段重写法罗斯；删除旧 reward 重叠 |
| D14 / P0 | 单物理成品还是复制 3/4 个建筑？ | 建议单成品+实例状态；每个 generic 成品属性差异逐条裁定，不能自动继承 style 1 |
| D15 / P1 | 严格唯一 buff 提案与新内容量冲突 | 建议保留主题差异、取消全局 key 排他硬门槛；如坚持则做 modifier 供给审计并改内容目标 |
| D16 / P1 | 相同 base_key 方向集合完全不重复是否硬性？ | 重复报告+人工证据例外；不得为凑轴制造史实；需更新原稿第 5.4 条 |
| D17 / P1 | 三方向都不合玩家当前战略怎么办？ | neutral 始终可用，明确它放弃额外收益；不承诺每座工程覆盖每条轴/双端，未来全方向自由选不在此首版 |
| D18 / P1 | 后世史实、异宗教/政体仪式的叙事 | 当前可执行行动与史实依据分离；确需 gate 的须保两条通路；不将未来人物写成当前统治者 |
| D19 / P1 | `estate` 无效元数据和 annex 隐性权力 | 默认不实现元数据玩法；旧 +0.5 必须入预算或移除；首版无赞助满意度 |
| D20 / P1 | 满资源/无目标的一次性奖励怎样处理？ | 开始前限制不可用目标；通用政府权力替代特定正统；不允许静默换奖或自动补金币；具体每项在内容表定规则 |
| D21 / P1 | AI“最接近”跨不同轴及无钱怎么办？ | 第 7 节归一 alignment、确定性破同分、预算/延期/24月简朴；样本表现决定超时值 |
| D22 / P1 | 主动取消/失地后的已付费用与临时惩罚 | 已付不退、已承担惩罚到期，不发尚未完成奖励；现有施工失败成本是否与仪式取消双扣须逐路径确认 |

### 10.2 引擎与技术待验证（M）

| ID / 优先级 | 未知 | 验证与结束条件 |
|---|---|---|
| M01 / P0 | 惯性/均衡如何影响月推力、即时冲击是否也受修正 | 第 9 节多初值对照实验；记录真实月值与 tooltip，不仅引用 define；长局验证上限后再定数值 |
| M02 / P0 | 同链变量可见性、事件 pending/隐藏提交的幂等 | 重复支付/完成/回调实验；分步骤提交可证一次；hover 不执行重型结算且预览准确 |
| M03 / P0 | 日期保存、十年精确期限、转手后的剩余期限与 map TTL | 官方 API/原版样例先查，游戏验证闰年/读档/月界；若不能存绝对日期，用单一世界月序号方案并公开精度，不能先承诺十年准确 |
| M04 / P0 | 国家对象的 tag/合并/灭亡/复国变量及 owner 事件顺序 | 跑国家生命周期矩阵；明确额度/受益者身份迁移；旧 owner 清理和新 owner 恢复都发生一次 |
| M05 / P0 | `has_societal_value` 是否对 age/allow 变化立即反映，失效后 modifier 行为 | 六条条件轴逐项实测；不能只复制 allow；在途重验证，完成来源聚合按可用性处理 |
| M06 / P1 | 聚合 auto modifier 更新何时生效、同名 modifier/布尔解锁多来源 | 完成/失地/拆除/到期/条件变化当日及月界记录；如 auto potential 需月界，则 UI 明示延迟，禁止无依据宣称即时 |
| M07 / P1 | 新建最终建筑失败/延迟、最后一级拆毁回调时序 | 在既有隐藏完成同步框架测试；建筑确认前无奖；毁最后来源与毁一处不同表现正确 |
| M08 / P1 | stage 8 工程+诠释双路由、两种 bespoke 动态终章文本 | 本地化/Customizable Localization 真机展示三个方向；名字/desc/支付/延期一致，无变量刚写就读的预览陷阱 |
| M09 / P1 | 多 map 字段与 GUI/弹窗快照在存档和多人中一致 | 保存读档、双客户端重复点击/事件排队；不依赖全局共享临时 scope 或新项目覆盖的变量 |
| M10 / P1 | 576 内容/来源缓存的负担、静态 key 数与潜在 hash 碰撞 | 记录生成符号数、mod 加载时间、月结耗时、悬停帧耗；不生成按6等级笛卡尔积的国家 modifier；复用既有缓存/auto modifier 机制实现新的按轴聚合，不声称现有系统已具备它 |
| M11 / P1 | 运行中修改 CMM/ED 停用、无工程师、专属角色死亡/路线无主 | 每项能恢复、退出或正常简朴；完成的持有收益不因停用操作 AI 就丢；无永远未释放的 in_progress |
| M12 / P1 | 当前镜像对应实际 beta 构建/DLC 与官方 docs 语法一致性 | 记录游戏构建和启用内容；官方日志对 `add_country_modifier` 字段与本地用法可能不同，先实证再写；不宣称已验证线上最新版 |

### 10.3 内容、消费者与验收缺口（C）

| ID / 优先级 | 缺口 | 关闭条件 |
|---|---|---|
| C01 / P0 | 576 项方向/奖励/依据均未按新结构完成 | 192×3 清单完整、无 placeholder；逐项人工签审，见配套 inventory 当前全为 not_authored |
| C02 / P1 | 408 unique 终章及 938 前置阶段兼容性未审 | 双语完整；shared 1–7 不偷偷预设另一诠释、过去/未来人物不穿越；2 bespoke 终章另审 |
| C03 / P1 | 原稿示例历史 claim 与事实→价值推论未全证 | 每条 claim 对应来源段落；史实与设计推导分别记录；本次只部分核实，不能泛称全部例子已通过 |
| C04 / P0 | 三种奖励“两个基础等级”没有跨载体标尺 | 三时代/L1/3/6/持有期预算表、small 无国家单位的替代参照和布尔解锁特审；正式包通用庆祝也计账 |
| C05 / P1 | 旧严格 schema、测试、编辑器写路径阻止新数据 | 所有 producer/consumer 改新结构；旧单风格/skip赠品断言替换，编辑器打开保存往返不丢字段 |
| C06 / P1 | generated registry/harness/design-only specs 可能过期或覆盖 | 新源依赖登记；生成后 freshness 全过；旧生成器不写回旧 ritual 奖励；134/2 当前范围取代码数据不取注释 |
| C07 / P1 | 空基础国家表、统一物理成品的限制/维护差异 | 92 个类型无国家基础时 UI 正确；56 generic 的原三成品属性差异清单逐条裁定；unique native canal 等特殊能力不丢 |
| C08 / P1 | 字体/图标/翻译/tooltip 及小屏空间未知 | 两语真实面板截图、启用/禁用/neutral/扩建/失效态可读；每效果 tooltip 对应实际 scope，不用手写文本替代实际效果预览 |
| C09 / P1 | 初始工程大量待选择提示与 AI 开局负担 | 开局真实国家观察；按需提醒而非批量弹 136 个事件；AI 不在同一 tick 无预算启动多个仪式 |
| C10 / P1 | 独立根与 GUI compat 的覆盖未知 | standalone、主mod、受影响兼容子模组逐组合跑通；不在本任务中偷偷扩展支持未声明的外部消费者 |
| C11 / P1 | 没有新机制的游戏内验收记录 | 第 9 节矩阵附构建/步骤/日志，失败逐号入账；静态验证通过不能代替真机验收 |
| C12 / P1 | 本计划新增规则尚未成为设计基准 | 对 D 项记录采纳/替代，并同步原稿、Original/Construction TODO/Unique Buff/AI 文档和 risk cards；保留证据边界，避免两份相互冲突的“已确认”文档 |

## 11. 本次已完成与没有声称完成的内容

已完成：读取原稿、相关设计/知识卡、canonical 数据、主要生成器与实际生成脚本、编辑器/图鉴消费者以及本地原版/官方脚本文档；核对 192 个工程范围；运行现有机制回归并通过；输出本计划和逐工程 inventory。

未完成且没有据此作实装声明：576 项历史/奖励/双语创作，全部历史 claim 核实，新 schema/脚本/GUI 的编码，游戏内惯性/计时/多人/性能实验，任何数值的最终平衡确认。

实施的首个可交付增量应是“8 个样本在新状态模型下完整走通三种诠释及 neutral，扩建和易主不重奖”的可试玩版本；全量 192 个工程发布必须满足 P6 和第 10 节关闭条件，不能以其余工程暂用无证据默认轴代替。
