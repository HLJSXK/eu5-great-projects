# 伟大工程逐工程展开与代码复杂度审计

审计日期：2026-10-27；代码快照：`ade82a3`。当前数据为 **195 个工程，其中通用 56 个、独特 139 个**。

结论：当前体积是静态数据库条目、同构流程复制、少量必要的静态分派，以及已退役设计残留叠加的结果。不能统一归因于 EU5 不支持参数。仓库已经有可工作的参数化 effect、variable map 和动态 GUI；它们没有贯彻到所有生成器。最值得处理的是候选显示缓存、完工主体、仪式公共流程、按 mechanic 去重和百科卡片；建筑类型、modifier、图片与文字内容则需要分别判断。

## 范围与统计口径

覆盖 `src/` 全部 `.txt/.gui/.yml`、三个兼容补丁的 GUI、两个生成片段，并追溯 `data/generated_files.yaml` 登记的生产者及其公共库。数据表、图片资产、Web 编辑器和图鉴构建记录不是游戏运行时逻辑，不把正常逐记录序列化算作重复算法。原版复制文件也不把整份原版内容归为工程展开。

| 范围 | 文件 | 物理行数 | 说明 |
|---|---:|---:|---|
| 主模组文本合计 | 189 | 597,234 | 包括本地化、GUI 和数据库定义 |
| in_game 中排除 gui 与 gfx 的文本 | 77 | 325,837 | 包括 effects、triggers、events、buildings 等 |
| 主模组 GUI 目录文本 | 6 | 37,500 | 包括过滤器和 widget 注册 |
| 主模组本地化 | 99 | 227,691 | 11 个语言目录；各语言文件集合并不完全相同 |
| main_menu/common 数据库文本 | 5 | 5,720 | concepts 等 |
| 兼容 GUI | 3 | 46,753 | 物理副本；不与主模组相加宣称运行成本 |
| 中间 GUI 片段 | 2 | 21,238 | 已合并进最终 GUI，不是额外运行一份 |

上表中几个子集并未穷举主模组所有目录。全文“文件行数”包括注释和空行；“主体行数”从定义左括号至配对右括号，排除定义之间的空行。行数是体积指标，**不是可删除行数、执行次数或帧率指标**。

伴随的 JSON 保存全部 194 个被扫描文件的路径、SHA-256、行数、生产者，以及脚本顶层定义的名称、起止行和归一化家族。归一化用于定位，不用它判断语义等价；下文重复主体结论另以原文去除定义名称、折叠空白后比较。

[完整文件与定义清单](C:/Users/Hades/Documents/code/eu5-great-projects/docs/technical/audit_data/2026-10-27_expansion_inventory.json)

## 逻辑中的全部主要展开点

表内路径均为当前实际输出；同一行列出的生成器或公共库是修改入口。逐定义家族和定位见末尾附录，不能直接修改生成物。

| 输出与规模 | 展开维度和位置 | 原因与可抽象程度 |
|---|---|---|
| [module effects](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/scripted_effects/tv_wonder_module_effects.txt:63)，31,225 行 | 候选校验 195 分支；候选显示 195 分支 × 4 部件 × 等级；两类中间建筑清理 | 校验调用异构场地 trigger，但外壳相同；显示与清理的建筑类型已有索引 map，可用公共流程。其余约几千行模块同步主要按 4 部件及 0–6 级展开，不能算成逐工程展开 |
| [finalization effects](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/scripted_effects/tv_wonder_finalization_effects.txt:1021)，40,409 行 | 每工程 construction、destroy、broadcast、visible、hidden 五类主体，共 975 个，加 5 个公共入口 | 可见建造采用持久状态和字面量等级差，源于 tooltip 约束；**同一个等级算法复制 195 遍不是该约束的必然结果**。可提参数化公共主体，必要时留每工程薄入口 |
| [mechanics triggers](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/scripted_triggers/tv_engineering_department_wonder_mechanics_triggers.txt:571)，32,694 行 | 13 族 × 195 个 trigger；6 个按 locked ID 分派入口；全工程 OR；适宜性 flag 静态引用 | 场地条件确实不同，建筑占用、上限、host/can_build 外壳同构。建议按 mechanic 共用规则，按工程保留固定地点和身份约束；map 字面量查询可保留很小的适配层 |
| [survey effects](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/scripted_effects/tv_wonder_survey_effects.txt:96)，12,312 行 | 195 个 actuals effect、195 路分派、195 个 site-preference 分支 | 数据已按 mechanic 共享，输出仍按实体展开。195 个 actuals 主体实际只有 **56 种**，这是直接可证的去重机会 |
| [proposal effects](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/scripted_effects/tv_wonder_proposal_effects.txt:11)，839 行 | 每工程 can_build 检查后写候选 deck，195 条 | deck 抽取已经使用 map。异构建造资格保留专门 trigger 合理，公共插入外壳可抽取；改成 map 遍历仍可能要检查全部 195 项，不能直接宣称更快 |
| [ritual state](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/scripted_effects/tv_wonder_ritual_state_effects.txt:6)，21,548 行 | 585 grant、585 settle、585 地点 tooltip、585 catalogue；195 sync、195 revoke；1 个撤销总入口 | 原生奖励展示、每工程风格的 modifier 身份和实例去重需要保留。map 写入、授予、撤销的外壳可公共化；585 settle 主体只有 **81 种**不同内容 |
| [ritual phase](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/scripted_effects/tv_wonder_ritual_phase_effects.txt:6)，13,981 行 | 3×195 奖励分派；195 显示缓存；195 阶层偏好；195 继承检查；195 完成事件分派；195 重新仪式化地点查找 | 统一仪式在 Python 数据模型中实现，但运行脚本还按工程生成大块主体。隐藏的显示缓存/偏好流程适合查表；真实奖励按奖励族或 mechanic 共用；可见奖励不能用手写 loc 代替 |
| [ritual triggers](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/scripted_triggers/tv_wonder_ritual_triggers.txt:30)，227 行 | `tv_wonder_current_site_is_shell_trigger` 中 195 项 OR | 仅为 locked ID 对应 helper/final 建筑身份判断。适合利用已准备好的类型或建立窄适配入口；另外几个仪式资格 trigger 已公共化 |
| [ritual lifecycle events](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/events/tv_wonder_ritual_lifecycle_events.txt:8)，17,791 行 | 195 个重新仪式化选项；195 个淡忘事件；195 个重仪式完成事件，另有 5 个公共事件 | 每工程选项来自已确认的 D27 交互设计。淡忘的长期定时身份必须属于事件实例；可抽公共即时主体，但不能用一个可被后续项目覆盖的国家变量替代排队事件身份 |
| [level change effects](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/scripted_effects/tv_wonder_level_change_effects.txt:206)，9,398 行 | 195 raise-existing，56 generic raise/lower，139 unique raise/lower；公共接口和三个共享 helper | **已经采用参数化 helper**。仍有过厚外壳，并发现所有 195 个工程的同一最终建筑被按三个风格重复列出；具体证据见下文 |
| [level change triggers](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/scripted_triggers/tv_wonder_level_change_triggers.txt:6)，784 行 | 195 个静态 map 查询，每个主体仅 3 行 | 有 10 月 23 日解析错误的明确证据。trigger 不能先写临时变量再读取，保留此窄适配层合理；这不构成其他几万行同构主体无法抽取的依据 |
| [location display effects](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/scripted_effects/tv_wonder_location_display_effects.txt:6)，9,674 行 | 2,340 个显示 modifier 的静态引用；195 个建筑等级变化回调；66 个开局已存在独特工程初始化 | modifier 引用是动态 GUI 查库的配套；等级变化回调、开局初始化外壳可参数化。实际地点投影、全国最高等级聚合已使用 map 遍历 |
| [index effects](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/scripted_effects/tv_wonder_index_effects.txt:6)，10,062 行 | 195 项元数据、helper/4 部件/final 双向类型表、139 个固定地点、56 种 mechanic 的适宜性行 | **这本身就是抽象的数据层**。不应因为它长而删掉：它让消费者不必全部展开。可减少同义路由和初始化冗余，但不能期望不同工程的数据消失 |
| [ownership effects](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/scripted_effects/tv_wonder_ownership_effects.txt:103)，1,668 行 | 两个 195 路 gain/loss 事件分派 | 易主状态处理已统一；静态事件 ID 留下分派。统一事件或统一外壳可继续缩小，但应保留事件快照与 revision 校验 |
| [ownership events](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/events/tv_wonder_ownership_events.txt:11)，19,509 行 | 195 gain + 195 loss 事件 | 图片、静态工程引用和历史事件 ID 是当前外壳差异；gain 的 guard、奖励和通知流程重复。loss 文字已经共用，customizable loc 单独替换不了图片和行为 |
| [finalization events](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/events/tv_wonder_finalization_events.txt:8)，9,780 行 | 195 完工 + 195 世界消息 + 195 等级同步事件，另有 2 个公共事件 | 按工程图片、描述和静态回调实例化。可保留小型事件外壳并抽 option/immediate 主体；若合并事件，需要确认 image 绑定及队列身份，不能只改 title/desc |
| [module buildings](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/building_types/tv_wonder_module_buildings.txt:6)，34,129 行 | 195×(4 部件+1 helper) = **975 个建筑类型** | 现设计用建筑对象持久化每座工程的部件、剩余量、名称与维护信息。这是数据库记录，不是 effect。想消掉需改为 location+工程+部件 map 状态，属于状态模型与玩法载体改造 |
| [final buildings](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/building_types/tv_engineering_department_wonder_mechanics_buildings.txt:6)，14,518 行 | **195 个最终建筑**，含完成/拆毁/直建规则 | 各工程是不同建筑身份；参数化 effect 可抽生命周期回调，不能直接代替数据库条目。保留建筑身份不意味着回调全文也必须复制 |
| [static modifiers](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/static_modifiers/tv_engineering_department_wonder_mechanics_modifiers.txt:6)，17,255 行 | **3,120 定义**：195×6×2 显示镜像 + 585 国家仪式 + 195 地点仪式 | 显示镜像服务于 `ShowModifierEffect`；实际国家仪式按工程和风格去重。复用同数值 modifier 会改变叠加/移除身份，不能只按数值去重；显示镜像可另研替代 API |
| [auto modifiers](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/auto_modifiers/tv_engineering_department_wonder_mechanics_auto_modifiers.txt:6)，1,294 行 | 103 个有国家基础效果的工程，105 个定义（2 个额外 unscaled） | 已通过 `scales_with` 读取最高等级 map，避免按六等级复制实际国家效果。按 modifier 类型汇总可进一步集中，但会把工作转移到聚合缓存并影响布尔效果/最大值语义 |
| [game concepts](C:/Users/Hades/Documents/code/eu5-great-projects/src/main_menu/common/game_concepts/tv_engineering_department_wonder_mechanics_concepts.txt:6)，5,472 行 | 195×7 + 2 = **1,367 定义**：概念、显示、两种图片、三种仪式和身份变体 | 数字 ID 的 GUI 查库桥梁。可消除不再需要的别名/概念，但 `SelectGameConcept`、图片纹理和本地化引用要一并改；customizable loc 不会创建这些数据库对象 |

### 原版接管与身份特例

这些也在逐工程展开范围内，但规模和必要性不同。

| 文件 | 展开方式 | 判断 |
|---|---|---|
| [vanilla damage overrides](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/scripted_effects/tv_vw_vanilla_damage_overrides.txt:5)，2,391 行 | 三种破坏程度各复制同一套 195 建筑分派 | 最直接的公共 helper 候选。保留三个 `REPLACE` 入口和各自原版 fallback，工程分派主体可共用 |
| [takeover triggers](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/scripted_triggers/tv_vw_vanilla_takeover_triggers.txt:5)，309 行 | 按 carrier 工程生成 gate/here/owned/anywhere 判断 | 原版建筑/艺术品语义有差异；保留适配条目，可共用判断外壳 |
| [takeover effects](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/scripted_effects/tv_vw_vanilla_takeover_effects.txt:5)，280 行 | raise/lower/damage/restore 和开局原版载体清理 | 升降级已经调用公共接口；damage debt 及开局对齐可按适配族共用 |
| [vanilla building overrides](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/building_types/tv_vw_vanilla_building_overrides.txt:5)，991 行 | 21 个原版建筑的完整覆盖 | 大部分体积来自必须保留的原版结构，不能当作相同工程算法删掉 |
| [vanilla event overrides](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/events/0000_tv_vw_vanilla_event_overrides.txt:5)，4,474 行；[decision overrides](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/decisions/tv_vw_vanilla_decision_overrides.txt:5)，396 行 | 原版事件/决议的读取、写入位点替换为 GP 接口 | 大量行是原版剧情、条件和选项，抽象重点是插入的适配逻辑，不是重写全部事件 |
| [identity effects](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/scripted_effects/tv_wonder_identity_effects.txt:1) 14 行、[decisions](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/decisions/tv_wonder_identity_decisions.txt:1) 38 行、[on_action](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/on_action/tv_wonder_identity_on_action.txt:1) 21 行、[identity events](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/events/0000_tv_wonder_identity_events.txt:1) 83 行 | 当前只有圣索菲亚身份变体，按 identity 配置生成 | 是有实际内容的特例，不是 195 遍统一流程；保留配置驱动。图片、loc 的身份分支来自同一公共库 |

接管的真正实现入口为 [render.py](C:/Users/Hades/Documents/code/eu5-great-projects/scripts_engineering_department/vanilla_takeover/render.py:37) 和同目录 `rewrite.py`；身份实现为 [wonder_identity.py](C:/Users/Hades/Documents/code/eu5-great-projects/scripts_engineering_department/wonder_identity.py:21) 与 [identity generator](C:/Users/Hades/Documents/code/eu5-great-projects/scripts_engineering_department/in_game/common/scripted_effects/gen_tv_wonder_identity_effects.py:18)。

## GUI 展开点与已经完成的抽象

| 表面 | 当前展开 | 原因与建议 |
|---|---|---|
| [百科](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/gui/encyclopedia_lateralview.gui:414)，20,415 行 | 生成片段 19,996 行，195 张工程卡 + 18 张机制卡；每工程又带三套仪式展示 | 同构布局逐条复制，属于高价值 GUI 去重。[append_card](C:/Users/Hades/Documents/code/eu5-great-projects/scripts_engineering_department/in_game/gui/gen_tv_encyclopedia_wonders_cards_gui.py:101) 只在 Python 层复用。可先抽 GUI type/template 并保留小实例，再以稳定 ID 列表/`GetGlobalMapKeys` datamodel 渲染同一 item；内容差异继续查表/loc |
| [工程部主面板](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/gui/panels/organization/tv_engineering_department.gui:1025)，4,256 行 | 图片、名称、说明、优先列表、适宜性行和仪式卡已动态化；仍有**两套三规模指示器**，每套合计枚举 195 个 ID 的长布尔表达式 | [wonder_size_visible](C:/Users/Hades/Documents/code/eu5-great-projects/scripts_engineering_department/in_game/gui/panels/organization/gen_tv_engineering_department_wonder_mechanics_gui.py:629) 可读现有 `tv_wonder_id_to_size` 或生命周期缓存的 size。这里 6 行表达式有数万字符，用行数会严重低估问题 |
| [工程面板片段](C:/Users/Hades/Documents/code/eu5-great-projects/data/generated_fragments/tv_engineering_department_wonder_mechanics.gui:1)，1,242 行 | 合并进入上一文件 | 同一实现的构建产物，不是独立重复系统 |
| [地点面板](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/gui/location_window.gui:1)，约 11,000 行 | slot、等级/有无效果、布局变体的有限展开；名称、图片、modifier、trigger/effect key 已按数字 ID 拼接；圣索菲亚身份有例外条件 | **没有为每个工程复制整张地点卡**。[slot 路由](C:/Users/Hades/Documents/code/eu5-great-projects/scripts_engineering_department/in_game/gui/gen_location_window.py:125) 已是可复用方案；长度很大是整份原版窗口覆盖的结果 |
| [仪式 GUI](C:/Users/Hades/Documents/code/eu5-great-projects/scripts_engineering_department/wonder_ritual_gui.py:35) | `Localize(prefix + style + id)` 路由、3 风格、7 阶层、有限价值观轴 | 3/7/轴数展开不是 195 工程展开；优先维护共用结构，无需改成一个巨大 customizable loc 分派 |
| [Prosper or Perish 百科兼容](C:/Users/Hades/Documents/code/eu5-great-projects/submods/tv_prosper_or_perish_compat/in_game/gui/encyclopedia_lateralview.gui:1)，21,568 行 | 再嵌入工程百科卡片 | 主百科优化应改片段并重生成此副本；不是另写一套 |
| [M&T 地点兼容](C:/Users/Hades/Documents/code/eu5-great-projects/submods/tv_meiou_and_taxes_compat/in_game/gui/location_window.gui:1) 12,597 行、[SoL 地点兼容](C:/Users/Hades/Documents/code/eu5-great-projects/submods/tv_standard_of_living_compat/in_game/gui/location_window.gui:1) 12,588 行 | 再嵌入共用地点 overlay | GUI 按路径整文件覆盖导致物理复制；不应把三份部署替代品算作三个同时存在的卡片系统 |

百科 datamodel 方案仍需验证全局索引初始化时机、国家不存在的百科上下文、分类与稳定排序，以及效果预览的作用域。抽 GUI type 主要减少维护重复；实例数量是否减少取决于渲染方式，不能等同于虚拟列表。

## 本地化展开与 customizable loc

主要文件为 [英文机制本地化](C:/Users/Hades/Documents/code/eu5-great-projects/src/main_menu/localization/english/tv_engineering_department_wonder_mechanics_l_english.yml:1)（15,950 行）与 [中文机制本地化](C:/Users/Hades/Documents/code/eu5-great-projects/src/main_menu/localization/simp_chinese/tv_engineering_department_wonder_mechanics_l_simp_chinese.yml:1)（15,802 行），再由翻译工具派生其他语言。源是 `data/wonder_localization.yaml`、独特工程 `ritual_text`，公共处理在 [expand_wonder_localization_data](C:/Users/Hades/Documents/code/eu5-great-projects/scripts_engineering_department/wonder_localization_lib.py:369)。

这里包括工程名/建筑名/描述、proposal/locked/preview 路由、concept/image/full-image/display 别名、modifier 名称、三仪式名称与描述、落成/世界消息、阶层偏好和身份变体。英文机制文件共有 15,944 条解析出的键，其中：

| 键族 | 数量 | 含义 |
|---|---:|---|
| `game_concept_*` | 2,762 | 工程内容及多种数字 ID 路由 |
| `STATIC_MODIFIER_NAME*` | 3,383 | 显示镜像、仪式等命名；含文件中的其他条目 |
| `TV_WONDER_RITUAL*` | 2,039 | 仪式正文与派生展示 |
| `TV_ENGINEERING_WONDER*` | 979 | 主面板五类工程文本等 |
| `tv_engineering_department.500*` | 980 | 完工描述与相关键 |
| `tv_engineering_department.600*` | 195 | 世界消息 |

这些键族不是所有条目的穷举。按值逐字比较，文件内有 **6,525 条超出唯一值集合的重复条目**。这不等于 6,525 个键可删除：数据库对象和动态拼接可能需要各自键。可以保留键、把相同正文改为 `$alias$`，或集中公共段落；必须检查动态引用闭包。文件还保留含旧仪式命名的内容，不能仅凭名字判断可删。

另有一项规模很大的遗留：**9 份旧 `tv_wonder_ceremony_l_<language>.yml` 合计 73,353 行**，分布在 braz_por、french、german、japanese、korean、polish、russian、spanish、turkish；英文与中文已没有对应文件。例如 [法语文件](C:/Users/Hades/Documents/code/eu5-great-projects/src/main_menu/localization/french/tv_wonder_ceremony_l_french.yml:8) 仍调用 `tv_wonder_ceremony_stage_1_pay` 等旧 customizable loc，文件头还指向已经不存在的逐语言 ceremony 生成器。当前非本地化源码搜索不到该 Custom 定义或 `.9300` 事件。这是旧八阶段系统的遗留证据，应按旧键族及动态引用闭包核对清理；不能将全部文本默认视为现行仪式所需，也不能不检查就整文件删除。

按文件族汇总，当前 11 语 `wonder_mechanics` 是 133,632 行，9 语旧 `ceremony` 是 73,353 行；施工随机事件本地化是 8,687 行，通用工程部本地化是 9,791 行，其余文本族合计 2,228 行。完整逐语言文件名见 JSON。

为什么没有全部使用 customizable loc：

1. **当前 GUI 已有更直接的数值路由。** 既然知道工程 ID，`Localize(Concatenate(...))` 就能选中名称/描述；改为 195 个条件的 customizable loc 只是把分派搬家，未必更短或更快。
2. **customizable loc 管显示文本，不管动作、建筑、modifier 或事件注册。** 它不能替代 `construct_building`、`add_country_modifier`，也不能让一个普通事件选项自动变成 195 个独立可点击选项。
3. **事件的 title/desc/option 文案有继续集中空间。** 固定的 `option.name` 可以在 loc 值里调用 `[ROOT.Custom('...')]`，不用复制选项行为。共享知识库保留了本项目旧八阶段仪式采用这种方案的记录，说明“从未用过/引擎不支持”不成立；旧机制已退役，不能当作当前仍存在的源文件。见 [历史 customizable loc 规则](C:/Users/Hades/Documents/code/eu5-great-projects/.eu5-base/docs/knowledge/anti_patterns.yaml:1532)。
4. **真实历史文本仍需逐工程 authored data。** 通用函数能消掉结构，不能消掉每个独特工程自己的名称、图片、地点与风格描述。

## 有证据的成因与推断

### 引擎限制确实解释了哪些展开

**引号内的参数不会按普通 scripted 参数替换。** `"variable_map(map|$wonder_id$)"` 是已记录失败的形态；动态 key 应取自现存变量/局部变量。effect 可先 `set_local_variable value = $id$` 再查固定表，纯 trigger 不能先执行赋值。10 月 23 日曾据此把规模检查改成 191 个静态 trigger，现随工程扩充为 195 个。证据是 [故障记录](C:/Users/Hades/Documents/code/eu5-great-projects/docs/technical/ED_Startup_Error_Fixes_2026-10-23.md:13)、[变量表规则](C:/Users/Hades/Documents/code/eu5-great-projects/.eu5-base/docs/technical/EU5_Modding_Knowledge_Base.md:606) 和 [当前生成器注释](C:/Users/Hades/Documents/code/eu5-great-projects/scripts_engineering_department/in_game/common/scripted_effects/gen_tv_wonder_level_change_effects.py:397)。

**参数替换不等于运行时函数指针。** `tv_wonder_$wonder$_effect` 以字面量 key 调用时能形成具体脚本名；不能假定传 `var:locked` 就会把变量里的数值插入函数名。map 能存数字和类型化 scope，不是任意 trigger/effect 的闭包。需要区分字面量参数化、运行时数据读取和静态名称分派三层。

**可见选项的预览不会可靠提交前面的临时状态写入。** 这解释了 0–6 级字面量差值表和部分静态 wrapper。但已有实机记录明确证明：用持久 `tv_wonder_locked` 直接查每部件 map，先捕获 building type，再切到地点，动态建造/拆除可以正常预览。不能把这个限制扩大为“建筑类型必须逐工程硬编码”。见 [动态建筑预览的工作条件](C:/Users/Hades/Documents/code/eu5-great-projects/.eu5-base/docs/technical/EU5_Modding_Knowledge_Base.md:666)、[模块生成器注释](C:/Users/Hades/Documents/code/eu5-great-projects/scripts_engineering_department/in_game/common/scripted_effects/gen_tv_wonder_module_effects.py:60)。

**GUI 展示接口和实际奖励的数据库不同。** 当前 `ShowModifierEffect` 需要静态显示镜像及配套静态引用；auto modifier 不能拿给 `add_country_modifier`。因此“实际国家效果已经 scales_with”并不能直接删掉六等级显示镜像。原生 `ShowScriptedEffectForScope` 也不能用 customizable loc 冒充同一语义。见 [显示镜像依据](C:/Users/Hades/Documents/code/eu5-great-projects/.eu5-base/docs/knowledge/anti_patterns.yaml:2912)。

**类型身份、固定内容和完整覆盖有成本。** 保留每种建筑和 modifier 的身份就需要定义；GUI 全文件覆盖需要维护部署副本。这些是当前对象模型和引擎接口下的必要数据，不应和可共用的控制流混算。

### 设计选择与历史包袱

**逐工程重新仪式化选项是确认过的产品选择。** D27 明确选择每种工程一个选项、只读缓存、点击后隐藏事件查地点，避免显示时扫描所有领地。改变这部分应视作交互方案修改；不能直接以“更抽象”为由改掉。见 [D27 决定](C:/Users/Hades/Documents/code/eu5-great-projects/docs/design/Wonder_Ritual_Rework_Decisions.md:268)。

**运行时架构是分阶段改造的。** 索引、proposal 抽取、模块建造、地点投影、主面板路由已有动态化；新的/重写的仪式生成器又生成逐工程主体。独特工程继承通用 mechanic 的事实已进入数据层，但生成输出没有普遍按 mechanic 共用。这是从当前代码结构得出的解释，不是对某位作者动机的断言。

**确有模型变更后未清理的重复。** [wonder_buildings](C:/Users/Hades/Documents/code/eu5-great-projects/scripts_engineering_department/in_game/common/scripted_effects/gen_tv_wonder_level_change_effects.py:101) 对三个 `ritual_style_ids` 返回同一个 `final_building`。当前 195 个工程全部得到长度 3、唯一值数 1 的列表。[生成输出](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/scripted_effects/tv_wonder_level_change_effects.txt:206) 因此出现三段相同建筑检查：195 个 raise-existing 定义多出 390 个相同分支，56 个 generic lower 多出 112 个相同分支，56 个 generic raise 的 OR 还多出 112 个相同条件。后续同条件 `else_if` 不会提供新行为。这是单一最终建筑重构后的具体遗留，不是引擎限制。

**只能有限回答“当时为什么”。** 当前仓库始于拆分快照，未导入拆分前完整历史；本审计不读取其他 mod checkout。上面标明有故障记录或设计决定的部分可以追溯，其余只能给出当前结构支持的推断。拆分边界见 [历史来源说明](C:/Users/Hades/Documents/code/eu5-great-projects/docs/archive/repository_split/Repository_Split.md:12)。

## 优先处理什么

| 优先级 | 改动方向 | 可量化的当前重复 | 预期收益与边界 |
|---|---|---|---|
| 1 | 清理单最终建筑模型遗留 | 502 个冗余完整分支、112 个冗余 OR 条件 | 改动小，语义最明确；保留对外接口 |
| 1 | 核对并清理旧 ceremony 本地化 | 9 个语言文件、73,353 行 | 旧 Custom 与生成器已缺失；先核对动态键及仍被引用的公共文案，不更动现行仪式正文 |
| 1 | 将候选显示/校验改为共用主体与类型 map | 显示单主体 16,967 行；校验 4,101 行 | 195 工程维度可显著缩小，保留 4 部件/6 等级有限分支；还可能减少每候选一次的线性分派 |
| 1 | 完工流程提取参数化 helper | 建造 195×119 = 23,205 主体行；hidden 195×40 = 7,800 行 | 保留原生预览、事件外壳和静态身份；可先只做源码维护去重，不承诺执行成本同比下降 |
| 1 | 按 mechanic 和奖励主体去重 | 195 actuals → 56 种主体；585 settle → 81 种主体 | 保留需要稳定 ID 的薄入口；优先用有语义的 mechanic/奖励族，不引入不可读的 hash 命名 |
| 2 | 抽百科卡 type，再评估 datamodel | 195 张同构工程卡，每张包含三仪式 | 降低 GUI 生成物维护量；datamodel 的排序、初始化、效果 scope 需要验证 |
| 2 | 主面板规模指示查 size map | 两套各枚举 195 ID 的表达式 | 已有 `tv_wonder_id_to_size`，无需再造全新状态模型 |
| 2 | 三种 vanilla damage 共用工程分派 | 3×195 同套匹配 | 保留各自原版 fallback，仅集中 GP 部分 |
| 2 | 仪式/易主/定时事件薄外壳化 | 585 状态授予、195 撤销、390 易主事件、定时事件主体 | 共用状态过程，但保留 modifier 身份、saved scopes、revision、到期 memory 校验和原生 tooltip |
| 3 | 本地化公共段落与别名集中 | 英文机制文件 6,525 个重复值 | 可减少重复正文；先查动态键，不把键名删除当成文本去重 |
| 单独立项 | 中间建筑状态换成 map、显示镜像改模型 | 975 中间建筑、2,340 显示 modifier | 体积潜力大，但涉及实体、维护、同地多工程、读档及显示语义，不应混在普通 helper 重构里 |

目标架构宜是“工程数据 + 少量静态身份适配 + 共享机制流程 + 共用 GUI”，而非强求零逐工程定义。例如保留 `tv_wonder_<id>_...` 薄入口，但入口只传 `id/building/site/modifier/event` 字面量，公共 effect 负责流程；把必须静态的 quoted-map 查询限制在几行内。

## 性能判断

可以从静态代码指出成本来源，不能从当前审计给出毫秒或百分比收益：

- **初始化成本**：`index_rebuild_global_maps` 的 10,018 主体行挂在 game_start/game_load；它长，但不是每次 hover 都执行。优化时应避免把初始化表的工作搬到读路径。
- **候选列表成本**：[select_saved_priority_proposal](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/scripted_effects/tv_wonder_module_effects.txt:21360) 对每个候选先调用逐工程校验，再调用逐工程显示；这里的候选数×工程分派确有结构性优化空间。
- **月度成本**：[auto cache monthly pulse](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/on_action/tv_engineering_department_on_action.txt:280) 通过全局表存在性 gate，随后进入 [every_owned_location 聚合](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/scripted_effects/tv_wonder_location_display_effects.txt:9362)。这个主体很短但遍历可能比许多万行静态定义更昂贵；是否改成增量更新需单独验证生命周期完整性。
- **GUI 成本**：百科大量卡片和主面板超长 OR 表达式值得测量。提取 type 仍可能实例化相同数量 widget；只有源码缩短不能证明布局成本降低。
- **存储/加载成本**：975 建筑、3,120 modifier 和大批 loc 会增加解析与注册负担；没有引擎 profiler 记录，不能量化其影响。
- **参数化维护收益与性能收益分开验收**：保留静态 wrapper 只抽公共 helper 时，分派次数和实质执行步骤可能不变；scripted 参数还可能在引擎内部实例化。只有取消不必要遍历、分派或重复求值才有更明确的运行时改进方向。

## 排除项与验证边界

`tv_wonder_construction_events.txt` 的 212 个事件及其 triggers/random-list 是按随机施工事件内容展开，不是按 195 工程展开。工程部通用 effects/triggers、AI driver、generic actions、prices、CMM、CMF、production methods、map modes、桥接回调没有另一套覆盖 195 工程的主体；个别特定工程/身份调用已在上文登记。三风格、七阶层、四部件、六等级、slot 数量的固定维度重复单独看待。

完整盘点使用工作树实际文件和领域数据加载器；脚本顶层位置按忽略注释/引号内容的括号深度提取，避免把生成器未缩进的内部 `if` 误计为独立 effect。重复主体比较不改名词、数值或作用域，只移除定义头并折叠空白。JSON 的 `literal_wonder_keys` 只是检索线索，出现一个工程名不等于存在逐工程复制，纯数字分派也可能不出现在该字段。

本轮只新增审计资料，没有修改数据、生成器、游戏逻辑或 GUI，也没有部署、运行游戏或进行性能基准。建议的重构方案不是已经完成实机验证的实现。

审计资料核验：258 个本地链接的文件和行号有效，194 个扫描文件的哈希与清单一致；`scripts/validate.py --changed --fix --ai-report` 返回 pass，0 errors、0 warnings、files_checked = 1。这个结果只覆盖本轮被验证器选中的改动，不代表全量游戏脚本或性能验收。

## 生成器与定义家族定位附录

下面是当前所有主要逐工程输出的生产者及定义家族首例。`{wonder}` / `{n}` 为清单归一化标签，不是 EU5 语法；完整具体名称及起止行在 JSON 中。单一大定义中的分派不能靠家族数体现，已在正文逐项列出。


### tv_engineering_department_wonder_mechanics_auto_modifiers.txt

输出：[tv_engineering_department_wonder_mechanics_auto_modifiers.txt](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/auto_modifiers/tv_engineering_department_wonder_mechanics_auto_modifiers.txt:1)；1294 行，105 个顶层定义。

生产者：[gen_tv_engineering_department_wonder_mechanics_auto_modifiers.py](C:/Users/Hades/Documents/code/eu5-great-projects/scripts_engineering_department/in_game/common/auto_modifiers/gen_tv_engineering_department_wonder_mechanics_auto_modifiers.py:1)。

| 定义家族或大入口 | 个数 | 主体行合计 | 首例 |
|---|---:|---:|---|
| `tv_wonder_auto_{wonder}` | 103 | 1167 | [定位](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/auto_modifiers/tv_engineering_department_wonder_mechanics_auto_modifiers.txt:6) |
| `tv_wonder_auto_{wonder}_unscaled` | 2 | 18 | [定位](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/auto_modifiers/tv_engineering_department_wonder_mechanics_auto_modifiers.txt:354) |

### tv_engineering_department_wonder_mechanics_buildings.txt

输出：[tv_engineering_department_wonder_mechanics_buildings.txt](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/building_types/tv_engineering_department_wonder_mechanics_buildings.txt:1)；14518 行，195 个顶层定义。

生产者：[gen_tv_engineering_department_wonder_mechanics_buildings.py](C:/Users/Hades/Documents/code/eu5-great-projects/scripts_engineering_department/in_game/common/building_types/gen_tv_engineering_department_wonder_mechanics_buildings.py:1)。

| 定义家族或大入口 | 个数 | 主体行合计 | 首例 |
|---|---:|---:|---|
| `{wonder}` | 195 | 14319 | [定位](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/building_types/tv_engineering_department_wonder_mechanics_buildings.txt:6) |

### tv_vw_vanilla_building_overrides.txt

输出：[tv_vw_vanilla_building_overrides.txt](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/building_types/tv_vw_vanilla_building_overrides.txt:1)；991 行，21 个顶层定义。

生产者：[gen_tv_vw_vanilla_building_overrides.py](C:/Users/Hades/Documents/code/eu5-great-projects/scripts_engineering_department/in_game/common/building_types/gen_tv_vw_vanilla_building_overrides.py:1)。

该文件按原版对象作小型适配；完整逐定义清单见 JSON。

### tv_wonder_module_buildings.txt

输出：[tv_wonder_module_buildings.txt](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/building_types/tv_wonder_module_buildings.txt:1)；34129 行，975 个顶层定义。

生产者：[gen_tv_wonder_module_buildings.py](C:/Users/Hades/Documents/code/eu5-great-projects/scripts_engineering_department/in_game/common/building_types/gen_tv_wonder_module_buildings.py:1)。

| 定义家族或大入口 | 个数 | 主体行合计 | 首例 |
|---|---:|---:|---|
| `tv_wonder_{wonder}_foundation` | 195 | 6630 | [定位](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/building_types/tv_wonder_module_buildings.txt:6) |
| `tv_wonder_{wonder}_body` | 195 | 6630 | [定位](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/building_types/tv_wonder_module_buildings.txt:41) |
| `tv_wonder_{wonder}_function` | 195 | 6630 | [定位](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/building_types/tv_wonder_module_buildings.txt:76) |
| `tv_wonder_{wonder}_decoration` | 195 | 6630 | [定位](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/building_types/tv_wonder_module_buildings.txt:111) |
| `tv_wonder_{wonder}` | 195 | 6630 | [定位](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/building_types/tv_wonder_module_buildings.txt:146) |

### tv_vw_vanilla_decision_overrides.txt

输出：[tv_vw_vanilla_decision_overrides.txt](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/decisions/tv_vw_vanilla_decision_overrides.txt:1)；396 行，4 个顶层定义。

生产者：[gen_tv_vw_vanilla_decision_overrides.py](C:/Users/Hades/Documents/code/eu5-great-projects/scripts_engineering_department/in_game/common/decisions/gen_tv_vw_vanilla_decision_overrides.py:1)。

| 定义家族或大入口 | 个数 | 主体行合计 | 首例 |
|---|---:|---:|---|
| `REPLACE:mos_build_kremlin_decision` | 1 | 186 | [定位](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/decisions/tv_vw_vanilla_decision_overrides.txt:159) |

### tv_vw_vanilla_damage_overrides.txt

输出：[tv_vw_vanilla_damage_overrides.txt](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/scripted_effects/tv_vw_vanilla_damage_overrides.txt:1)；2391 行，3 个顶层定义。

生产者：[gen_tv_vw_vanilla_damage_overrides.py](C:/Users/Hades/Documents/code/eu5-great-projects/scripts_engineering_department/in_game/common/scripted_effects/gen_tv_vw_vanilla_damage_overrides.py:1)。

| 定义家族或大入口 | 个数 | 主体行合计 | 首例 |
|---|---:|---:|---|
| `REPLACE:minor_destroy_building_levels_in_location` | 1 | 795 | [定位](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/scripted_effects/tv_vw_vanilla_damage_overrides.txt:5) |
| `REPLACE:major_destroy_building_levels_in_location` | 1 | 795 | [定位](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/scripted_effects/tv_vw_vanilla_damage_overrides.txt:801) |
| `REPLACE:catastrophic_destroy_building_levels_in_location` | 1 | 795 | [定位](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/scripted_effects/tv_vw_vanilla_damage_overrides.txt:1597) |

### tv_vw_vanilla_takeover_effects.txt

输出：[tv_vw_vanilla_takeover_effects.txt](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/scripted_effects/tv_vw_vanilla_takeover_effects.txt:1)；280 行，28 个顶层定义。

生产者：[gen_tv_vw_vanilla_takeover_effects.py](C:/Users/Hades/Documents/code/eu5-great-projects/scripts_engineering_department/in_game/common/scripted_effects/gen_tv_vw_vanilla_takeover_effects.py:1)。

| 定义家族或大入口 | 个数 | 主体行合计 | 首例 |
|---|---:|---:|---|
| `tv_vw_{wonder}_raise_effect` | 24 | 72 | [定位](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/scripted_effects/tv_vw_vanilla_takeover_effects.txt:9) |
| `tv_vw_startup_reconcile_effect` | 1 | 141 | [定位](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/scripted_effects/tv_vw_vanilla_takeover_effects.txt:140) |

### tv_wonder_finalization_effects.txt

输出：[tv_wonder_finalization_effects.txt](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/scripted_effects/tv_wonder_finalization_effects.txt:1)；40409 行，980 个顶层定义。

生产者：[gen_tv_wonder_finalization_effects.py](C:/Users/Hades/Documents/code/eu5-great-projects/scripts_engineering_department/in_game/common/scripted_effects/gen_tv_wonder_finalization_effects.py:1)。

| 定义家族或大入口 | 个数 | 主体行合计 | 首例 |
|---|---:|---:|---|
| `tv_wonder_execute_finalization_hidden_event_effect` | 1 | 197 | [定位](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/scripted_effects/tv_wonder_finalization_effects.txt:17) |
| `tv_wonder_mechanics_trigger_finalization_event_effect` | 1 | 782 | [定位](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/scripted_effects/tv_wonder_finalization_effects.txt:238) |
| `tv_wonder_{wonder}_construct_final_building_effect` | 195 | 23205 | [定位](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/scripted_effects/tv_wonder_finalization_effects.txt:1021) |
| `tv_wonder_{wonder}_destroy_finalization_intermediate_buildings_effect` | 195 | 3120 | [定位](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/scripted_effects/tv_wonder_finalization_effects.txt:1141) |
| `tv_wonder_{wonder}_broadcast_finalization_completion_event_effect` | 195 | 3120 | [定位](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/scripted_effects/tv_wonder_finalization_effects.txt:1158) |
| `tv_wonder_{wonder}_finalization_visible_effect` | 195 | 1170 | [定位](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/scripted_effects/tv_wonder_finalization_effects.txt:1175) |
| `tv_wonder_{wonder}_finalization_hidden_effect` | 195 | 7800 | [定位](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/scripted_effects/tv_wonder_finalization_effects.txt:1182) |

### tv_wonder_index_effects.txt

输出：[tv_wonder_index_effects.txt](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/scripted_effects/tv_wonder_index_effects.txt:1)；10062 行，4 个顶层定义。

生产者：[gen_tv_wonder_index_effects.py](C:/Users/Hades/Documents/code/eu5-great-projects/scripts_engineering_department/in_game/common/scripted_effects/gen_tv_wonder_index_effects.py:1)。

| 定义家族或大入口 | 个数 | 主体行合计 | 首例 |
|---|---:|---:|---|
| `tv_wonder_index_rebuild_global_maps_effect` | 1 | 10018 | [定位](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/scripted_effects/tv_wonder_index_effects.txt:6) |

### tv_wonder_level_change_effects.txt

输出：[tv_wonder_level_change_effects.txt](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/scripted_effects/tv_wonder_level_change_effects.txt:1)；9398 行，594 个顶层定义。

生产者：[gen_tv_wonder_level_change_effects.py](C:/Users/Hades/Documents/code/eu5-great-projects/scripts_engineering_department/in_game/common/scripted_effects/gen_tv_wonder_level_change_effects.py:1)。

| 定义家族或大入口 | 个数 | 主体行合计 | 首例 |
|---|---:|---:|---|
| `tv_wonder_{wonder}_raise_existing_final_building_level_effect` | 195 | 2730 | [定位](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/scripted_effects/tv_wonder_level_change_effects.txt:206) |
| `tv_wonder_{wonder}_raise_level_effect` | 56 | 952 | [定位](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/scripted_effects/tv_wonder_level_change_effects.txt:222) |
| `tv_wonder_{wonder}_lower_generic_level_effect` | 56 | 840 | [定位](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/scripted_effects/tv_wonder_level_change_effects.txt:240) |
| `tv_wonder_{wonder}_raise_unique_level_effect` | 139 | 2641 | [定位](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/scripted_effects/tv_wonder_level_change_effects.txt:3022) |
| `tv_wonder_{wonder}_lower_unique_level_effect` | 139 | 1251 | [定位](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/scripted_effects/tv_wonder_level_change_effects.txt:3042) |

### tv_wonder_location_display_effects.txt

输出：[tv_wonder_location_display_effects.txt](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/scripted_effects/tv_wonder_location_display_effects.txt:1)；9674 行，206 个顶层定义。

生产者：[gen_tv_wonder_location_display_effects.py](C:/Users/Hades/Documents/code/eu5-great-projects/scripts_engineering_department/in_game/common/scripted_effects/gen_tv_wonder_location_display_effects.py:1)。

公共实现：[gen_tv_engineering_department_wonder_mechanics_effects.py](C:/Users/Hades/Documents/code/eu5-great-projects/scripts_engineering_department/in_game/common/scripted_effects/gen_tv_engineering_department_wonder_mechanics_effects.py:1)。

| 定义家族或大入口 | 个数 | 主体行合计 | 首例 |
|---|---:|---:|---|
| `tv_wonder_mechanics_reference_display_modifiers_effect` | 1 | 2348 | [定位](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/scripted_effects/tv_wonder_location_display_effects.txt:6) |
| `tv_wonder_{wonder}_handle_final_building_level_changed_effect` | 195 | 3316 | [定位](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/scripted_effects/tv_wonder_location_display_effects.txt:2406) |
| `tv_wonder_seed_existing_unique_wonders_effect` | 1 | 3434 | [定位](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/scripted_effects/tv_wonder_location_display_effects.txt:5927) |
| `tv_wonder_mechanics_refresh_location_display_state_effect` | 1 | 145 | [定位](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/scripted_effects/tv_wonder_location_display_effects.txt:9524) |

### tv_wonder_module_effects.txt

输出：[tv_wonder_module_effects.txt](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/scripted_effects/tv_wonder_module_effects.txt:1)；31225 行，23 个顶层定义。

生产者：[gen_tv_wonder_module_effects.py](C:/Users/Hades/Documents/code/eu5-great-projects/scripts_engineering_department/in_game/common/scripted_effects/gen_tv_wonder_module_effects.py:1)。

| 定义家族或大入口 | 个数 | 主体行合计 | 首例 |
|---|---:|---:|---|
| `tv_wonder_validate_priority_candidate_for_saved_wonder_effect` | 1 | 4101 | [定位](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/scripted_effects/tv_wonder_module_effects.txt:63) |
| `tv_wonder_project_priority_candidate_display_effect` | 1 | 16967 | [定位](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/scripted_effects/tv_wonder_module_effects.txt:4165) |
| `tv_wonder_construct_module_for_last_completed_part_effect` | 1 | 126 | [定位](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/scripted_effects/tv_wonder_module_effects.txt:21441) |
| `tv_wonder_sync_units_from_buildings_effect` | 1 | 419 | [定位](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/scripted_effects/tv_wonder_module_effects.txt:21568) |
| `tv_wonder_sync_existing_final_building_level_effect` | 1 | 161 | [定位](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/scripted_effects/tv_wonder_module_effects.txt:22042) |
| `tv_wonder_restore_locked_wonder_final_building_state_effect` | 1 | 154 | [定位](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/scripted_effects/tv_wonder_module_effects.txt:22204) |
| `tv_wonder_apply_helper_building_to_final_site_effect` | 1 | 492 | [定位](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/scripted_effects/tv_wonder_module_effects.txt:22359) |
| `tv_wonder_materialize_module_buildings_from_unit_vars_effect` | 1 | 2760 | [定位](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/scripted_effects/tv_wonder_module_effects.txt:22852) |
| `tv_wonder_combine_completed_modules_at_location_effect` | 1 | 335 | [定位](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/scripted_effects/tv_wonder_module_effects.txt:25613) |
| `tv_wonder_destroy_discovered_generic_intermediate_buildings_at_location_effect` | 1 | 1515 | [定位](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/scripted_effects/tv_wonder_module_effects.txt:25949) |
| `tv_wonder_destroy_discovered_unique_intermediate_buildings_at_location_effect` | 1 | 3756 | [定位](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/scripted_effects/tv_wonder_module_effects.txt:27465) |

### tv_wonder_ownership_effects.txt

输出：[tv_wonder_ownership_effects.txt](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/scripted_effects/tv_wonder_ownership_effects.txt:1)；1668 行，4 个顶层定义。

生产者：[gen_tv_wonder_ownership_effects.py](C:/Users/Hades/Documents/code/eu5-great-projects/scripts_engineering_department/in_game/common/scripted_effects/gen_tv_wonder_ownership_effects.py:1)。

| 定义家族或大入口 | 个数 | 主体行合计 | 首例 |
|---|---:|---:|---|
| `tv_wonder_ownership_trigger_gain_event_effect` | 1 | 782 | [定位](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/scripted_effects/tv_wonder_ownership_effects.txt:103) |
| `tv_wonder_ownership_trigger_loss_event_effect` | 1 | 782 | [定位](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/scripted_effects/tv_wonder_ownership_effects.txt:887) |

### tv_wonder_proposal_effects.txt

输出：[tv_wonder_proposal_effects.txt](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/scripted_effects/tv_wonder_proposal_effects.txt:1)；839 行，7 个顶层定义。

生产者：[gen_tv_wonder_proposal_effects.py](C:/Users/Hades/Documents/code/eu5-great-projects/scripts_engineering_department/in_game/common/scripted_effects/gen_tv_wonder_proposal_effects.py:1)。

公共实现：[gen_tv_engineering_department_wonder_mechanics_effects.py](C:/Users/Hades/Documents/code/eu5-great-projects/scripts_engineering_department/in_game/common/scripted_effects/gen_tv_engineering_department_wonder_mechanics_effects.py:1)。

| 定义家族或大入口 | 个数 | 主体行合计 | 首例 |
|---|---:|---:|---|
| `tv_wonder_mechanics_rebuild_feasible_deck_effect` | 1 | 782 | [定位](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/scripted_effects/tv_wonder_proposal_effects.txt:11) |

### tv_wonder_ritual_phase_effects.txt

输出：[tv_wonder_ritual_phase_effects.txt](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/scripted_effects/tv_wonder_ritual_phase_effects.txt:1)；13981 行，19 个顶层定义。

生产者：[gen_tv_wonder_ritual_state_effects.py](C:/Users/Hades/Documents/code/eu5-great-projects/scripts_engineering_department/in_game/common/scripted_effects/gen_tv_wonder_ritual_state_effects.py:1)。

公共实现：[wonder_ritual_codegen.py](C:/Users/Hades/Documents/code/eu5-great-projects/scripts_engineering_department/wonder_ritual_codegen.py:1)。

| 定义家族或大入口 | 个数 | 主体行合计 | 首例 |
|---|---:|---:|---|
| `tv_wonder_ritual_apply_style_{n}_effect` | 3 | 2346 | [定位](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/scripted_effects/tv_wonder_ritual_phase_effects.txt:6) |
| `tv_wonder_ritual_refresh_display_effect` | 1 | 3959 | [定位](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/scripted_effects/tv_wonder_ritual_phase_effects.txt:2369) |
| `tv_wonder_ritual_roll_estates_effect` | 1 | 1764 | [定位](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/scripted_effects/tv_wonder_ritual_phase_effects.txt:6329) |
| `tv_wonder_ritual_enter_phase_effect` | 1 | 598 | [定位](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/scripted_effects/tv_wonder_ritual_phase_effects.txt:8149) |
| `tv_wonder_ritual_complete_effect` | 1 | 207 | [定位](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/scripted_effects/tv_wonder_ritual_phase_effects.txt:8800) |
| `tv_wonder_reritual_lock_effect` | 1 | 4916 | [定位](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/scripted_effects/tv_wonder_ritual_phase_effects.txt:9058) |

### tv_wonder_ritual_state_effects.txt

输出：[tv_wonder_ritual_state_effects.txt](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/scripted_effects/tv_wonder_ritual_state_effects.txt:1)；21548 行，2731 个顶层定义。

生产者：[gen_tv_wonder_ritual_state_effects.py](C:/Users/Hades/Documents/code/eu5-great-projects/scripts_engineering_department/in_game/common/scripted_effects/gen_tv_wonder_ritual_state_effects.py:1)。

公共实现：[wonder_ritual_codegen.py](C:/Users/Hades/Documents/code/eu5-great-projects/scripts_engineering_department/wonder_ritual_codegen.py:1)。

| 定义家族或大入口 | 个数 | 主体行合计 | 首例 |
|---|---:|---:|---|
| `tv_wonder_{wonder}_ritual_{n}_grant_effect` | 585 | 6045 | [定位](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/scripted_effects/tv_wonder_ritual_state_effects.txt:6) |
| `tv_wonder_{wonder}_ritual_{n}_settle_effect` | 585 | 1952 | [定位](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/scripted_effects/tv_wonder_ritual_state_effects.txt:17) |
| `tv_wonder_display_{n}_ritual_{n}_location_tooltip_effect` | 585 | 1950 | [定位](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/scripted_effects/tv_wonder_ritual_state_effects.txt:21) |
| `tv_wonder_display_{n}_ritual_{n}_catalogue_effect` | 585 | 4045 | [定位](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/scripted_effects/tv_wonder_ritual_state_effects.txt:25) |
| `tv_wonder_{wonder}_ritual_sync_country_effect` | 195 | 3454 | [定位](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/scripted_effects/tv_wonder_ritual_state_effects.txt:90) |
| `tv_wonder_{wonder}_ritual_revoke_effect` | 195 | 1170 | [定位](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/scripted_effects/tv_wonder_ritual_state_effects.txt:108) |
| `tv_wonder_ritual_revoke_location_effect` | 1 | 197 | [定位](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/scripted_effects/tv_wonder_ritual_state_effects.txt:21352) |

### tv_wonder_survey_effects.txt

输出：[tv_wonder_survey_effects.txt](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/scripted_effects/tv_wonder_survey_effects.txt:1)；12312 行，207 个顶层定义。

生产者：[gen_tv_wonder_survey_effects.py](C:/Users/Hades/Documents/code/eu5-great-projects/scripts_engineering_department/in_game/common/scripted_effects/gen_tv_wonder_survey_effects.py:1)。

公共实现：[gen_tv_engineering_department_wonder_mechanics_effects.py](C:/Users/Hades/Documents/code/eu5-great-projects/scripts_engineering_department/in_game/common/scripted_effects/gen_tv_engineering_department_wonder_mechanics_effects.py:1)。

| 定义家族或大入口 | 个数 | 主体行合计 | 首例 |
|---|---:|---:|---|
| `tv_wonder_calculate_{wonder}_suitability_actuals_effect` | 195 | 6703 | [定位](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/scripted_effects/tv_wonder_survey_effects.txt:96) |
| `tv_wonder_mechanics_calculate_suitability_actuals_effect` | 1 | 782 | [定位](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/scripted_effects/tv_wonder_survey_effects.txt:6994) |
| `tv_wonder_mechanics_copy_completed_survey_from_location_effect` | 1 | 154 | [定位](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/scripted_effects/tv_wonder_survey_effects.txt:7777) |
| `tv_wonder_mechanics_store_survey_on_location_effect` | 1 | 103 | [定位](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/scripted_effects/tv_wonder_survey_effects.txt:7985) |
| `tv_wonder_mechanics_apply_survey_site_preference_effect` | 1 | 4116 | [定位](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/scripted_effects/tv_wonder_survey_effects.txt:8089) |

### tv_engineering_department_wonder_mechanics_triggers.txt

输出：[tv_engineering_department_wonder_mechanics_triggers.txt](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/scripted_triggers/tv_engineering_department_wonder_mechanics_triggers.txt:1)；32694 行，2547 个顶层定义。

生产者：[gen_tv_engineering_department_wonder_mechanics_triggers.py](C:/Users/Hades/Documents/code/eu5-great-projects/scripts_engineering_department/in_game/common/scripted_triggers/gen_tv_engineering_department_wonder_mechanics_triggers.py:1)。

| 定义家族或大入口 | 个数 | 主体行合计 | 首例 |
|---|---:|---:|---|
| `tv_wonder_suitability_flag_static_reference_trigger` | 1 | 564 | [定位](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/scripted_triggers/tv_engineering_department_wonder_mechanics_triggers.txt:6) |
| `tv_wonder_location_meets_{wonder}_base_site_rules_trigger` | 195 | 1046 | [定位](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/scripted_triggers/tv_engineering_department_wonder_mechanics_triggers.txt:571) |
| `tv_wonder_location_has_{wonder}_intermediate_building_trigger` | 195 | 1755 | [定位](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/scripted_triggers/tv_engineering_department_wonder_mechanics_triggers.txt:580) |
| `tv_wonder_location_has_{wonder}_final_building_trigger` | 195 | 975 | [定位](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/scripted_triggers/tv_engineering_department_wonder_mechanics_triggers.txt:590) |
| `tv_wonder_location_has_{wonder}_expandable_final_building_trigger` | 195 | 9369 | [定位](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/scripted_triggers/tv_engineering_department_wonder_mechanics_triggers.txt:596) |
| `tv_wonder_location_has_{wonder}_capped_final_building_trigger` | 195 | 780 | [定位](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/scripted_triggers/tv_engineering_department_wonder_mechanics_triggers.txt:642) |
| `tv_wonder_location_is_valid_priority_module_project_for_{wonder}_trigger` | 195 | 780 | [定位](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/scripted_triggers/tv_engineering_department_wonder_mechanics_triggers.txt:647) |
| `tv_wonder_location_is_valid_priority_final_project_for_{wonder}_trigger` | 195 | 780 | [定位](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/scripted_triggers/tv_engineering_department_wonder_mechanics_triggers.txt:652) |
| `tv_wonder_location_is_valid_priority_project_for_{wonder}_trigger` | 195 | 1170 | [定位](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/scripted_triggers/tv_engineering_department_wonder_mechanics_triggers.txt:657) |
| `tv_wonder_country_has_{wonder}_project_or_final_trigger` | 195 | 1560 | [定位](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/scripted_triggers/tv_engineering_department_wonder_mechanics_triggers.txt:664) |
| `tv_wonder_location_has_any_wonder_final_building_trigger` | 1 | 199 | [定位](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/scripted_triggers/tv_engineering_department_wonder_mechanics_triggers.txt:20541) |
| `tv_wonder_location_has_locked_wonder_intermediate_building_trigger` | 1 | 783 | [定位](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/scripted_triggers/tv_engineering_department_wonder_mechanics_triggers.txt:20741) |
| `tv_wonder_location_has_locked_wonder_expandable_final_building_trigger` | 1 | 783 | [定位](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/scripted_triggers/tv_engineering_department_wonder_mechanics_triggers.txt:21525) |
| `tv_wonder_location_meets_locked_wonder_base_site_rules_trigger` | 1 | 783 | [定位](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/scripted_triggers/tv_engineering_department_wonder_mechanics_triggers.txt:22309) |
| `tv_wonder_location_is_valid_priority_project_for_locked_wonder_trigger` | 1 | 783 | [定位](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/scripted_triggers/tv_engineering_department_wonder_mechanics_triggers.txt:23093) |
| `tv_wonder_display_{n}_base_site_rules_trigger` | 195 | 907 | [定位](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/scripted_triggers/tv_engineering_department_wonder_mechanics_triggers.txt:23877) |
| `tv_wonder_location_can_host_{wonder}_trigger` | 195 | 2535 | [定位](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/scripted_triggers/tv_engineering_department_wonder_mechanics_triggers.txt:24979) |
| `tv_wonder_can_build_{wonder}_trigger` | 195 | 2200 | [定位](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/scripted_triggers/tv_engineering_department_wonder_mechanics_triggers.txt:24993) |
| `tv_wonder_player_visible_site_rules_{wonder}_trigger` | 195 | 795 | [定位](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/scripted_triggers/tv_engineering_department_wonder_mechanics_triggers.txt:25005) |
| `tv_wonder_site_rule_player_visible_locked_wonder_trigger` | 1 | 783 | [定位](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/scripted_triggers/tv_engineering_department_wonder_mechanics_triggers.txt:31117) |
| `tv_wonder_location_can_host_locked_wonder_trigger` | 1 | 783 | [定位](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/scripted_triggers/tv_engineering_department_wonder_mechanics_triggers.txt:31901) |

### tv_vw_vanilla_takeover_triggers.txt

输出：[tv_vw_vanilla_takeover_triggers.txt](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/scripted_triggers/tv_vw_vanilla_takeover_triggers.txt:1)；309 行，56 个顶层定义。

生产者：[gen_tv_vw_vanilla_takeover_triggers.py](C:/Users/Hades/Documents/code/eu5-great-projects/scripts_engineering_department/in_game/common/scripted_triggers/gen_tv_vw_vanilla_takeover_triggers.py:1)。

| 定义家族或大入口 | 个数 | 主体行合计 | 首例 |
|---|---:|---:|---|
| `tv_vw_{wonder}_gate_trigger` | 43 | 129 | [定位](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/scripted_triggers/tv_vw_vanilla_takeover_triggers.txt:5) |
| `tv_vw_{wonder}_present_here_trigger` | 10 | 93 | [定位](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/scripted_triggers/tv_vw_vanilla_takeover_triggers.txt:17) |
| `tv_vw_{wonder}_present_owned_trigger` | 2 | 22 | [定位](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/scripted_triggers/tv_vw_vanilla_takeover_triggers.txt:199) |

### tv_wonder_level_change_triggers.txt

输出：[tv_wonder_level_change_triggers.txt](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/scripted_triggers/tv_wonder_level_change_triggers.txt:1)；784 行，195 个顶层定义。

生产者：[gen_tv_wonder_level_change_effects.py](C:/Users/Hades/Documents/code/eu5-great-projects/scripts_engineering_department/in_game/common/scripted_effects/gen_tv_wonder_level_change_effects.py:1)。

| 定义家族或大入口 | 个数 | 主体行合计 | 首例 |
|---|---:|---:|---|
| `tv_wonder_location_survey_scale_allows_level_{n}_trigger` | 195 | 585 | [定位](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/scripted_triggers/tv_wonder_level_change_triggers.txt:6) |

### tv_wonder_ritual_triggers.txt

输出：[tv_wonder_ritual_triggers.txt](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/scripted_triggers/tv_wonder_ritual_triggers.txt:1)；227 行，4 个顶层定义。

生产者：[gen_tv_wonder_ritual_state_effects.py](C:/Users/Hades/Documents/code/eu5-great-projects/scripts_engineering_department/in_game/common/scripted_effects/gen_tv_wonder_ritual_state_effects.py:1)。

公共实现：[wonder_ritual_codegen.py](C:/Users/Hades/Documents/code/eu5-great-projects/scripts_engineering_department/wonder_ritual_codegen.py:1)。

| 定义家族或大入口 | 个数 | 主体行合计 | 首例 |
|---|---:|---:|---|
| `tv_wonder_current_site_is_shell_trigger` | 1 | 199 | [定位](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/scripted_triggers/tv_wonder_ritual_triggers.txt:29) |

### tv_engineering_department_wonder_mechanics_modifiers.txt

输出：[tv_engineering_department_wonder_mechanics_modifiers.txt](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/static_modifiers/tv_engineering_department_wonder_mechanics_modifiers.txt:1)；17255 行，3120 个顶层定义。

生产者：[gen_tv_engineering_department_wonder_mechanics_modifiers.py](C:/Users/Hades/Documents/code/eu5-great-projects/scripts_engineering_department/in_game/common/static_modifiers/gen_tv_engineering_department_wonder_mechanics_modifiers.py:1)。

| 定义家族或大入口 | 个数 | 主体行合计 | 首例 |
|---|---:|---:|---|
| `tv_wonder_display_{n}_level_{n}` | 1170 | 3174 | [定位](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/static_modifiers/tv_engineering_department_wonder_mechanics_modifiers.txt:6) |
| `tv_wonder_display_{n}_local_level_{n}` | 1170 | 7434 | [定位](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/static_modifiers/tv_engineering_department_wonder_mechanics_modifiers.txt:11) |
| `tv_wonder_{wonder}_ritual_{n}_modifier` | 585 | 2539 | [定位](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/static_modifiers/tv_engineering_department_wonder_mechanics_modifiers.txt:72) |
| `tv_wonder_{wonder}_ritual_{n}_location_modifier` | 195 | 984 | [定位](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/common/static_modifiers/tv_engineering_department_wonder_mechanics_modifiers.txt:83) |

### 0000_tv_vw_vanilla_event_overrides.txt

输出：[0000_tv_vw_vanilla_event_overrides.txt](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/events/0000_tv_vw_vanilla_event_overrides.txt:1)；4474 行，55 个顶层定义。

生产者：[gen_tv_vw_vanilla_event_overrides.py](C:/Users/Hades/Documents/code/eu5-great-projects/scripts_engineering_department/in_game/events/gen_tv_vw_vanilla_event_overrides.py:1)。

| 定义家族或大入口 | 个数 | 主体行合计 | 首例 |
|---|---:|---:|---|
| `flavor_chi.2` | 1 | 142 | [定位](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/events/0000_tv_vw_vanilla_event_overrides.txt:236) |
| `flavor_gra.14` | 1 | 113 | [定位](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/events/0000_tv_vw_vanilla_event_overrides.txt:1267) |
| `flavor_mos.6` | 1 | 137 | [定位](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/events/0000_tv_vw_vanilla_event_overrides.txt:1928) |
| `flavor_mos.11` | 1 | 190 | [定位](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/events/0000_tv_vw_vanilla_event_overrides.txt:2161) |
| `flavor_mos.12` | 1 | 109 | [定位](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/events/0000_tv_vw_vanilla_event_overrides.txt:2352) |
| `flavor_mos.28` | 1 | 109 | [定位](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/events/0000_tv_vw_vanilla_event_overrides.txt:2462) |
| `flavor_mos.34` | 1 | 118 | [定位](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/events/0000_tv_vw_vanilla_event_overrides.txt:2572) |
| `flavor_mos.35` | 1 | 165 | [定位](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/events/0000_tv_vw_vanilla_event_overrides.txt:2691) |
| `flavor_mos.37` | 1 | 161 | [定位](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/events/0000_tv_vw_vanilla_event_overrides.txt:2857) |
| `flavor_mos.57` | 1 | 124 | [定位](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/events/0000_tv_vw_vanilla_event_overrides.txt:3107) |
| `flavor_mos.62` | 1 | 137 | [定位](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/events/0000_tv_vw_vanilla_event_overrides.txt:3326) |
| `flavor_mos.92` | 1 | 151 | [定位](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/events/0000_tv_vw_vanilla_event_overrides.txt:3464) |
| `flavor_rus.70` | 1 | 138 | [定位](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/events/0000_tv_vw_vanilla_event_overrides.txt:4119) |
| `grand_tour_events.2` | 1 | 181 | [定位](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/events/0000_tv_vw_vanilla_event_overrides.txt:4294) |

### tv_wonder_finalization_events.txt

输出：[tv_wonder_finalization_events.txt](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/events/tv_wonder_finalization_events.txt:1)；9780 行，587 个顶层定义。

生产者：[gen_tv_wonder_finalization_events.py](C:/Users/Hades/Documents/code/eu5-great-projects/scripts_engineering_department/in_game/events/gen_tv_wonder_finalization_events.py:1)。

| 定义家族或大入口 | 个数 | 主体行合计 | 首例 |
|---|---:|---:|---|
| `event 5000..` | 195 | 4875 | [定位](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/events/tv_wonder_finalization_events.txt:8) |
| `event 6000..` | 197 | 2167 | [定位](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/events/tv_wonder_finalization_events.txt:5078) |
| `event 9000..` | 195 | 2145 | [定位](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/events/tv_wonder_finalization_events.txt:5102) |

### tv_wonder_ownership_events.txt

输出：[tv_wonder_ownership_events.txt](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/events/tv_wonder_ownership_events.txt:1)；19509 行，390 个顶层定义。

生产者：[gen_tv_wonder_ownership_events.py](C:/Users/Hades/Documents/code/eu5-great-projects/scripts_engineering_department/in_game/events/gen_tv_wonder_ownership_events.py:1)。

| 定义家族或大入口 | 个数 | 主体行合计 | 首例 |
|---|---:|---:|---|
| `event 8000..` | 195 | 13845 | [定位](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/events/tv_wonder_ownership_events.txt:11) |
| `event 9000..` | 195 | 5265 | [定位](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/events/tv_wonder_ownership_events.txt:14051) |

### tv_wonder_ritual_lifecycle_events.txt

输出：[tv_wonder_ritual_lifecycle_events.txt](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/events/tv_wonder_ritual_lifecycle_events.txt:1)；17791 行，395 个顶层定义。

生产者：[gen_tv_wonder_ritual_state_effects.py](C:/Users/Hades/Documents/code/eu5-great-projects/scripts_engineering_department/in_game/common/scripted_effects/gen_tv_wonder_ritual_state_effects.py:1)。

公共实现：[wonder_ritual_codegen.py](C:/Users/Hades/Documents/code/eu5-great-projects/scripts_engineering_department/wonder_ritual_codegen.py:1)。

| 定义家族或大入口 | 个数 | 主体行合计 | 首例 |
|---|---:|---:|---|
| `event 2000..` | 5 | 1985 | [定位](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/events/tv_wonder_ritual_lifecycle_events.txt:8) |
| `event 3000..` | 195 | 13065 | [定位](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/events/tv_wonder_ritual_lifecycle_events.txt:1998) |
| `event 4000..` | 195 | 2340 | [定位](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/events/tv_wonder_ritual_lifecycle_events.txt:2066) |

### tv_engineering_department_wonder_mechanics_concepts.txt

输出：[tv_engineering_department_wonder_mechanics_concepts.txt](C:/Users/Hades/Documents/code/eu5-great-projects/src/main_menu/common/game_concepts/tv_engineering_department_wonder_mechanics_concepts.txt:1)；5472 行，1367 个顶层定义。

生产者：[gen_tv_engineering_department_wonder_mechanics_concepts.py](C:/Users/Hades/Documents/code/eu5-great-projects/scripts_engineering_department/main_menu/common/game_concepts/gen_tv_engineering_department_wonder_mechanics_concepts.py:1)。

| 定义家族或大入口 | 个数 | 主体行合计 | 首例 |
|---|---:|---:|---|
| `tv_wonder_{wonder}` | 195 | 585 | [定位](C:/Users/Hades/Documents/code/eu5-great-projects/src/main_menu/common/game_concepts/tv_engineering_department_wonder_mechanics_concepts.txt:14) |
| `tv_wonder_display_{n}` | 195 | 585 | [定位](C:/Users/Hades/Documents/code/eu5-great-projects/src/main_menu/common/game_concepts/tv_engineering_department_wonder_mechanics_concepts.txt:794) |
| `tv_wonder_display_image_{n}` | 195 | 585 | [定位](C:/Users/Hades/Documents/code/eu5-great-projects/src/main_menu/common/game_concepts/tv_engineering_department_wonder_mechanics_concepts.txt:1574) |
| `tv_wonder_display_full_image_{n}` | 195 | 585 | [定位](C:/Users/Hades/Documents/code/eu5-great-projects/src/main_menu/common/game_concepts/tv_engineering_department_wonder_mechanics_concepts.txt:2354) |
| `tv_wonder_display_{n}_ritual_{n}` | 585 | 1755 | [定位](C:/Users/Hades/Documents/code/eu5-great-projects/src/main_menu/common/game_concepts/tv_engineering_department_wonder_mechanics_concepts.txt:3134) |

### GUI 与本地化生产者补充

- [tv_encyclopedia_wonders_cards.gui](C:/Users/Hades/Documents/code/eu5-great-projects/data/generated_fragments/tv_encyclopedia_wonders_cards.gui:1)：[gen_tv_encyclopedia_wonders_cards_gui.py](C:/Users/Hades/Documents/code/eu5-great-projects/scripts_engineering_department/in_game/gui/gen_tv_encyclopedia_wonders_cards_gui.py:1)。
- [tv_engineering_department_wonder_mechanics.gui](C:/Users/Hades/Documents/code/eu5-great-projects/data/generated_fragments/tv_engineering_department_wonder_mechanics.gui:1)：[gen_tv_engineering_department_wonder_mechanics_gui.py](C:/Users/Hades/Documents/code/eu5-great-projects/scripts_engineering_department/in_game/gui/panels/organization/gen_tv_engineering_department_wonder_mechanics_gui.py:1)。
- [location_window.gui](C:/Users/Hades/Documents/code/eu5-great-projects/src/in_game/gui/location_window.gui:1)：[gen_location_window.py](C:/Users/Hades/Documents/code/eu5-great-projects/scripts_engineering_department/in_game/gui/gen_location_window.py:1)。
- [tv_engineering_department_wonder_mechanics_l_english.yml](C:/Users/Hades/Documents/code/eu5-great-projects/src/main_menu/localization/english/tv_engineering_department_wonder_mechanics_l_english.yml:1)：[gen_tv_engineering_department_wonder_mechanics_l_english.py](C:/Users/Hades/Documents/code/eu5-great-projects/scripts_engineering_department/main_menu/localization/english/gen_tv_engineering_department_wonder_mechanics_l_english.py:1)。
- [tv_engineering_department_wonder_mechanics_l_simp_chinese.yml](C:/Users/Hades/Documents/code/eu5-great-projects/src/main_menu/localization/simp_chinese/tv_engineering_department_wonder_mechanics_l_simp_chinese.yml:1)：[gen_tv_engineering_department_wonder_mechanics_l_simp_chinese.py](C:/Users/Hades/Documents/code/eu5-great-projects/scripts_engineering_department/main_menu/localization/simp_chinese/gen_tv_engineering_department_wonder_mechanics_l_simp_chinese.py:1)。

面板/百科的合并入口为 [merge_tv_engineering_department_wonder_mechanics_gui.py](C:/Users/Hades/Documents/code/eu5-great-projects/scripts_engineering_department/in_game/gui/panels/organization/merge_tv_engineering_department_wonder_mechanics_gui.py:1) 和 [merge_tv_encyclopedia_wonders_cards_gui.py](C:/Users/Hades/Documents/code/eu5-great-projects/scripts_engineering_department/in_game/gui/merge_tv_encyclopedia_wonders_cards_gui.py:1)；语言派生入口为 [translate_engineering_department_localization_google.py](C:/Users/Hades/Documents/code/eu5-great-projects/scripts_engineering_department/main_menu/localization/translate_engineering_department_localization_google.py:1)，旧 ceremony 文件不是当前登记的生产输出。
