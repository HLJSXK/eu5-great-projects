# 工程部启动日志五类错误修复

日期：2026-10-23。范围由用户确认：本次启动日志的五类工程部错误。
诊断依据为 `tmp/error_log_audit_20261023_171330/summary.txt` 及各类原始报错快照。
第一轮修复已写入工作区源文件和生成器，并重建其输出；当时未部署到游戏或重启实测。
21:05 新日志中的生产方式重名问题及本轮部署记录见末节。

## 修复结果

| 原报错 | 修改与验证边界 |
| --- | --- |
| 1,528 条建筑引用重复前缀 | 等级变更生成器统一以带类型的建筑引用调用等级判断。实际展开共享升降级 helper，核对生成后的引用只有一个 `building_type:`。 |
| 2,865 条规模表解析及连锁错误 | 删除带引号表达式中的 `$wonder_id$`。新增登记在生成清单中的 191 个静态键查询触发器，原入口按 id 分派；先判表存在，再判键存在。覆盖全部奇观、1–7 级请求、缺表／空表／其他键／1–6 级勘测，以及人类无限规模和 AI 分支。 |
| 2,292 条本地显示修正及 PostValidate 错误 | 补齐 191 × 6 = 1,146 个地点显示 modifier，声明地点类别，读取现有建筑的基础本地效果。普通效果按等级缩放，`raw_modifier` 不缩放；显示沿用建筑已序列化数值的精度。引用闭包及各等级数值对账通过。这些定义用于既有只读预览，未新增实际奖励发放。 |
| 260 条仪式状态表不存在 | 新增共用的显式 `trigger_if` 判表查询，缺表返回否；用于仪式风格、记忆、朴素和全国等级缓存。覆盖地点显示、月度缓存、授予后去重、撤销、淡忘和重新仪式化候选；未增加读路径建表或地点遍历。 |
| 193 条隐藏事件缺标题 | `.2002`、`.2004` 和 191 个淡忘事件使用原版已有的 `empty_text` 标题，沿用原版隐藏事件写法。 |

本地显示定义现在依赖建筑设计数据，因此编辑器生成计划增加了
`mechanics.buildings` 对该生成器的触发关系，避免改建筑后显示定义过期。

## 验证

环境：Windows，直接使用 `C:\Users\Hades\anaconda3\envs\eu5\python.exe`，
共享参考来自当前 `.eu5-base`。

- 相关 pytest：**140 passed、1 deselected**。排除的完整生成链另行执行，结果见下节。
- 新增启动错误回归覆盖五类问题；原有仪式、优先候选、编辑器资源和生成计划回归通过。
- 本轮 22 个生成输出与其当前生成器内容一致，均保留 UTF-8 BOM。
- `scripts_engineering_department/test_wonder_mechanics_rules.py` 通过。
- `scripts/validate.py --changed --fix --ai-report`：18 个变化文件，**0 错误、0 警告**。
- `git -c core.whitespace=cr-at-eol diff --check` 通过；手写触发器在 HEAD 中已使用 CRLF。

可复现回归命令：

```powershell
& 'C:\Users\Hades\anaconda3\envs\eu5\python.exe' -m pytest tests/test_engineering_startup_errors.py tests/test_wonder_ritual_rework.py tests/test_wonder_priority_proposals.py tests/test_generation_plan.py tests/test_wonder_payload_loading.py tests/test_wonder_resource_contract.py -m 'not slow' -q --basetemp .tmp/pytest-ed-startup-regression
```

## 完整生成链的独立差异

完整隔离重建执行 36 个生成步骤、检查 54 个登记输出。生成步骤完成，
49 个输出逐字节一致，但全量新鲜度测试仍有以下五个文件与工作区不同；
已逐一确认它们在 Git 中相对 HEAD 无修改：

| 文件 | 差异 |
| --- | --- |
| `src/main_menu/localization/english/tv_engineering_department_wonder_mechanics_l_english.yml` | 文本相同，换行字节不同。 |
| `src/main_menu/localization/simp_chinese/tv_engineering_department_wonder_mechanics_l_simp_chinese.yml` | 文本相同，换行字节不同。 |
| `data/wonder_editor_catalog.yaml` | 当前共享参考新增的国家／地点 modifier 名称和扫描计数。 |
| `src/in_game/events/0000_tv_vw_vanilla_event_overrides.txt` | 原版接管输出中的黄金费用倍率 `-0.1` 与当前参考生成的 `-1` 不同。 |
| `src/in_game/common/building_types/tv_vw_vanilla_building_overrides.txt` | 三个大津巴布韦原版建筑的地点／国家限制与当前参考不同。 |

上述原版接管差异涉及其他玩法条件，未作为启动错误修复一并重生成。
不能把本轮回归通过写成“全仓所有测试通过”，也不能用静态结果声称游戏日志中的报错已消失。
五类修复的引擎验收仍需部署后重新启动，使用新会话日志检查；旧会话日志保留作为诊断证据。

## 21:05 生产方式重名：补充修复与部署

新日志中的五条 `duplicated production method name` 属于另一处遗漏。
已确认游戏部署目录的等级变更文件与上一轮修复后的源码哈希一致；
生产方式警告来自 `tv_vw_vanilla_building_overrides.txt` 复制的原版内嵌生产方式 ID。
`REPLACE:<building>` 不会替换这些生产方式的全局注册，因此必须使用独立 ID。
共享知识库已有 `replaced_building_reuses_vanilla_unique_production_method_id` 规则说明这一行为。

- `vanilla_takeover/render.py` 现在为复制的五个生产方式统一添加 `tv_vw_` 前缀；逐项保留原有图标、商品需求和类别。
- 11 种语言各补充五个名称别名，引用原版名称，保留 UTF-8 BOM。
- 重建此文件同时消除了上一节登记的大津巴布韦三个建筑的生成差异：地点限制采用当前原版的 `this = location:great_zimbabwe`，国家限制采用 `has_or_had_tag = ZMW`。
- 接管与启动错误回归：**38 passed、2 failed**。两项失败均来自上一节已登记、未修改的事件输出中 `flavor_gra.14` 黄金费用倍率与当前参考不同；生产方式唯一性、本地化和建筑字段保留检查均通过。
- 静态验证：19 个变化文件，**0 错误、0 警告**；本轮文件的空白检查通过。

已将本轮建筑输出和 11 个名称文件同步到：

```text
C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/game/mod/tv_engineering_department
```

部署前逐一确认原文件与 HEAD 内容一致，备份后写入并验证全部 12 个文件的 SHA-256。
备份、清单及部署结果在 `tmp/ed_production_method_fix_20261023/`。
未关闭或重启游戏；当前进程不会因此重新加载定义，是否消除警告须以重新启动后的新日志确认。

## 21:05 AI 动作列表 Unexpected token：补充修复

`tv_engineering_department_list.txt` 中六个新仪式动作被写在 `actions = { ... }`
闭合括号之外，成为列表对象下的裸 token。日志报告了其中三项，实际修复六项：
三种风格预览、确认、朴素落成和取消重新仪式化。六项均已移回 `actions` 内，
保留现有动作和参与条件。该文件未登记为生成物，也没有活动生成器重写它。

新增回归检查列表层级、重复动作及动作定义闭包；修复前复现失败，修复后通过。
启动错误和仪式回归合计 **32 passed**；changed 静态验证检查 22 个变化文件，
**0 错误、0 警告**。本轮文件空白检查通过。

已同步这一个文件到游戏工程部目录，部署文件与测试源码 SHA-256 一致：
`74D14044505D6AF1D5548857A74ADD3F7AA28FA494FE1CF4F567CB9961F6C85D`。
原部署文件保存在 `tmp/ed_ai_list_fix_20261023/tv_engineering_department_list.before.txt`。
仍需完全重启游戏，以新启动日志完成引擎验收。

## 正式修复计划对账完成

收到 `Error_Log_Fix_Plan_2026-10-23.md` 后，已按其完整范围补齐此前未处理的
#4、#7、#8 描述、#9、#11 及精确过滤规则、共享知识和交接例外。
详细条目、#11 的事实纠正和部署清单见该计划末节“执行复核记录”。

最新结果为 **186 项 pytest 通过**（包含完整隔离重建），静态验证 49 个变化文件
0 错误、0 警告；本页先前记录的两项事件复制测试失败和五处生成差异现已关闭。
新增修复已部署：10 个文件更新、4 个旧消息文件移除，全部核验 SHA-256。
尚未完成 ED 加入 Construction Manager 后的游戏内重启验收；当前活动 SOL 播放集未被切换。
