# Great Projects / ED 仓库拆分交接（第一棒）

日期：2026-10-26。本文面向下一位审计者，说明边界、可复现证据、实际改动和未验证部分。
本文与新仓库 `docs/archive/repository_split/Repository_Split.md` 同步交付。

## 1. 起点与最终边界

拆分起点：`eu5-towards-victory` 提交
`2cf4171b4e273c87efb8257baef895c7a6017ad6`，开始时工作树干净。
共享 base 起点：`33e60f14164ad06fc227b2d9e7c365b6db67c561`。

新仓库路径：`C:/Users/Hades/Documents/code/eu5-great-projects`。
这是独立的本地 Git 仓库，主分支为 `main`。初始提交 `c90007e44bc3`；接受完整 clone 验证的快照为 `cdab9113f0f4`。未创建 GitHub 仓库，未推送，未发布网站，未部署到游戏。
初始提交是当前可构建快照；没有重写或导入整个 TV 提交历史。
原始历史继续保留在 TV，逐文件来源由新仓库的 `data/extraction_provenance.json` 记录。

| 仓库 | 当前所有权 |
| --- | --- |
| `eu5-towards-victory` | TV 的 `src/`、胜利/组织数据及生成器、TV 编辑器、TV 图标工具、TV 验证与部署 |
| `eu5-great-projects` | ED/奇观 `src/`、数据、领域生成器、独立编辑器、图像工具与资产、静态图鉴、三个 GUI 兼容补丁、相关文档和测试 |
| `eu5-modding-base` | 共享 EU5 参考文件、引擎规则、共享工具，以及跨仓库知识规则的迁移来源记录 |
| `eu5-court-positions` / `eu5-eureka` | 既有独立仓库；本轮未修改它们的代码、数据或工作树 |

开发依赖与游戏依赖是两个边界：

- GP 的开发只需要自己的文件和 `.eu5-base`。不读取 TV checkout，不通过相对路径调用 TV 工具。
- TV 的开发同样不读取 GP checkout，但游戏内继续依赖 `hades.towards_victory.great_project`。
- GP 游戏 ID、`tv_` 脚本符号、事件命名空间、部署目录 `tv_engineering_department` 保留。
- GP 的运行依赖仍是 CMF 2.x 和 Construction Manager；没有增加 TV 运行依赖。
- TV 对 GP 的版本约束改为 `*`。TV 的日期版本工具不再替另一个仓库决定版本。

## 2. 文件迁移与保留方式

| 原路径 | GP 路径 / 处理 |
| --- | --- |
| `src_engineering_department/**` | `src/**` |
| `scripts_engineering_department/**` | 原名保留，作为 GP 的领域生成器包 |
| `data/*wonder*`、奇观生成片段及图像清单 | 保留在 GP 的 `data/`，从 TV 移除 |
| `data/pulse_registry.yaml` | 按 hook 中的实际回调归属拆开，GP 仅有 ED/wonder 回调 |
| `data/cmf_warning_suppressions.yaml` | GP 仅保留 ED/wonder 的既有变量；没有添加屏蔽项绕过验证 |
| `data/io_leaders.yaml` | GP 只保留 engineering 条目；TV 的 engineering 条目是显式的游戏集成契约 |
| `data/cost_reward_units.yaml` | 两边各自维护的数值目录快照；不是共享 base 的引擎规则，没有跨仓库自动同步 |
| `data/task_pool.yaml` | TV 保留真实任务目录；GP 编辑器的本地任务目录为空，不复制 TV 任务 |
| `scripts/compat/**`、`data/compat/**`、`submods/**` | 全部归 GP；保留兼容补丁自身已有 ID 和部署名称 |
| `assets/generated_wonders/**`、`assets/historical/**` | 归 GP，保留来源图、加工结果、历史归档和相关元数据 |
| 奇观 building icons / metadata | 归 GP；通用样式参考按实际工具输入复制到 GP |
| `unique_wonders_site/**`、对应 `.github/workflows` | 归 GP；没有调用远端 Pages 发布 |
| `ai_gui_assessment/**` | ED 离线 GUI 预览、fixture、原型与历史渲染图归 GP；默认 mod-root 改为 `src`，继续使用 base renderer |
| GP 的宣传稿/配图与苏伊士接入文档 | 逐项核对后迁入 GP；两个混合 Steam 原件留在 TV 作历史证据 |
| Wonder/cropper 的前后端模块、测试 | 迁入 `great_projects_editor_web/` 及 GP `tests/` |
| 共同的编辑器事务/作业/验证基础设施 | 各仓库本地维护一份，从原版本派生；不建立依赖 TV 的包装器 |
| `docs/**/ED_*`、Great Project 设计/宣传稿、奇观设计/指南/风险卡 | 归 GP；保留原有归档状态 |
| 混合领域的旧编辑器方案和手册 | 明确标注为拆分前历史资料；当前命令以各自 README / CLAUDE 为准 |

TV 的 5,527 项受控删除全部映射到 GP，没有未登记的删除。35 个实际 generic actions 与 11 个语言目录一起移交。

来源清单包含原路径、新路径、迁移类别、原 Git blob、原 Windows 工作树 SHA-256；
最终交付文件另有 SHA-256 快照。两种哈希不混为一谈：原工作树可能有 CRLF，而 Git 保存 LF。
清单中 `excluded-after-split` 表示复制分析阶段进入暂存区、之后剔除的 TV 专属文件，不是漏迁。

私有 `generate_wonder_image.local.json` 只作为忽略的本机配置转移；不进入 Git、清单内容或日志。
没有调用付费图像 API，没有重新生成图像内容。
最终名称审计额外移交 ED 封面、其生成记录/样式参考、宣传稿和独特增益设计稿共 7 项，列于 results.json；它们不改变经过 clone 验证的玩法或生成输出。

## 3. 共同生成器如何拆开

1. **IO leader actions**：TV 只写 TV actions；GP 的生成器只读本地 engineering 数据，写 GP leader actions。
2. **character_title.txt**：每个游戏根仍生成自己的完整 vanilla 副本。GP 只有自己的称号；TV 保留包含 engineering 的运行时称号集合。
3. **pulse bridges**：每个仓库只写自己的桥接文件，数据源已经分开。GP 在游戏启动、加载、月度等钩子上的原顺序保留。
4. **CMF suppressions**：GP 生产者只读自己的显式变量表；TV 不再生成 GP 文件。
5. **message types**：GP 的通知显示策略成为 `data/message_types.txt`，生产者核对本地 actions 后写 additive 文件。缺策略直接报错。TV 保留自己的生成规则。
6. **索引、版本、验证、部署**：TV 只登记 `src/`；GP 也只登记自己的 `src/`，兼容补丁由其专用 freshness/build 检查负责。
7. **严格 YAML / cost catalog**：TV 使用新的 `scripts/yaml_catalog.py`，从原 Wonder 模块抽出实际使用的通用原语，保留重复键拒绝语义；不再导入 ED 包。

`data/generated_files.yaml` 两边均已按输出归属重建，GP 的 50 个生产者对应 81 项登记/合并输出。
所有 generic actions 随其 AI `actions` 列表、root-owned message type 和五字段通知本地化一起迁移。
实际 action 集合另有测试核对 AI membership；验证器检查消息类型、五字段及别名，未降低规则。

## 4. 编辑器与工具

TV：`python -m towards_victory_editor_web`，默认端口 8760。
工具页为花费/奖励、胜利树、媒体、生成器、本地化、胜利路径。

GP：`python -m great_projects_editor_web`，默认端口 8763。
工具页为花费/奖励、奇观、媒体、奇观裁剪、生成器、本地化。
GP operation store 环境变量改为 `GP_EDITOR_OPERATION_STORE`；默认仍在自己的 `.editor_state/`。

两边保留资源 preview/commit、事务回滚、作业取消和日志协议。外域 HTTP 路由已删除，返回 404。
GP DDS 工具去掉胜利树/胜利奖励批次；TV 去掉 Wonder 图片、历史图处理及奇观批次。
配置中的输出路径、默认批次和样式输入同步拆开，避免旧目标重新生成已迁出的目录。

原混合浏览器总场景作为 `docs/archive/pre_split_editor/Pre_Split_Browser_Acceptance.cjs.txt` 保留，未声称完整重放其所有旧步骤。
当前 `tests/resource_state_browser.cjs` 验证实际六页导航、所属资源、外域 404、只读预览、两种视口和 JS 异常。
各领域原有 Python/Node 合同测试随所有者保留。截图在 `docs/archive/repository_split/split_validation/`。

## 5. 共享知识库的配套修改

`eu5-modding-base` 本轮修改四个文件：

- `docs/knowledge/MIGRATION_COVERAGE.yaml`
- `docs/knowledge/knowledge_loader.py`
- `scripts/knowledge_loader.py`
- 重新生成的 `docs/knowledge/BRIEF.md`

迁移清单 schema 从 1 升为 2，local 条目可写 `destination_project`。
`source_project` 和原始 `entry` 保留，coverage 根据当前归属检查本地规则。
11 条明确属于奇观/仪式的规则转归 GP。
同时纠正既有 Court Positions 规则 `court_character_variable_scope_link_missing_var_prefix` 的归属；
它在本轮开始时已从 TV 移出，但 base 清单仍要求它留在 TV，导致旧校验失败。

两个加载器都做了测试：转移后 TV 不再要求该规则，GP 必须有该规则，删除 GP 规则会失败。
补丁副本为 `Great_Projects_Base_Changes.patch`，便于审计和在其他机器上配套应用。
没有把工程部的机制、数值或特有设计搬进共享引擎规则。

## 6. 本轮额外的两项有限修正

### 重复事件 ID

原 `tv_engineering_department_events.txt` 有两个 `.21`：支持耗尽挽救事件，以及失去工地的纯通知。
EN/ZH AI 本地化也与主文件重复，阻止本地化编辑器启动。
保留挽救事件 `.21`，将纯通知改为 `.22`，同步 ownership hook、AI 本地化及相关测试。
没有改变失败惩罚、挽救选项或项目状态算法。新测试核对两个 ID 唯一及通知调用正确。

### 跨平台生成换行

GP 的文本生产者显式写 LF，保留游戏文本的 UTF-8 BOM；七个 vanilla takeover 输出原来的显式 CRLF 也改为 LF。
这是为了让 `.gitattributes`、新 clone 和生成器得到一致字节，防止新仓库永远显示过期。
对应换行测试仍检查 BOM，并改为严格验证 LF。批处理文件继续使用 CRLF。

另外，新仓库初次 `--changed` 会列出所有未跟踪文件，包括故意写错的 lint fixtures。
自动选择现在排除 `tests/fixtures/`，这些样例仍由 `test_lint_rules.py` 执行。
新增负向测试证明相同错误放在 `src/` 仍被拒绝；游戏规则及 action 注册诊断没有屏蔽。

## 7. 验证记录与边界

所有 Python 命令使用 `C:/Users/Hades/anaconda3/envs/eu5/python.exe`，未使用 `conda run`。
测试临时目录明确设在可写位置。GP 暂存路径较长时曾触发 Windows 路径长度限制，
已使用较短的 basetemp 重跑；该环境失败不计作产品回归。

当前逐项命令、通过数和日志位置见 `split_validation/results.json`；最终 clone 的验证也记录在那里。
已确认的核心结果：

- TV 快速 Python 回归：315 通过；Node：105 通过。
- GP 正式 clone 全量 Python 回归（含真实生成链）：883 通过、1 项既有仪式 GUI 断言失败，耗时 136.55 秒。
- GP Node：127 通过，1 个既有缺失模块测试失败。
- GP 离线 GUI 工具：16 项测试、43 项子检查通过；未启动游戏。
- 两边独立浏览器验收通过；GP 实际加载 56 个通用奇观和 139 个独特奇观。
- GP `scripts/build.py --check --date 2026-10-26` 通过：50 个生产者、81 项输出一致性、189 个游戏文本文件静态检查。
- TV 全量静态验证：181 个游戏文本文件，无错误或警告。
- 两边 `scripts/validate.py --changed --fix --ai-report`、routing 检查和 lint fixtures 的最终结果见机器记录。
- 实际所有 action 的注册检查通过，没有新增 suppressions 或移除五字段检查。

正式 clone 已独立 bootstrap、构建校验、来源校验、Web/Node/浏览器回归，并成功打包四个目录到自己的 `build/`；无 staging origin 或 Git alternates。

没有启动 EU5、加载存档、测试多人游戏或调用第三方 mod 运行时。
网站只做本地构建，保留 GitHub workflow；远端仓库/Pages 的后续设置尚未执行。
这些不应被理解成已完成游戏内验收。

## 8. 已知旧失败，不掩盖、不计为拆分新回归

1. GP `test_gui_only_ritual_variables_are_suppressed_in_standalone_ed`：期待已不在 GUI 中的 `tv_wonder_ritual_position_1`。
   用原提交文件独立复现，同样失败。没有添加不存在的变量、修改诊断或加 skip。
2. GP `tests/wonder_rituals.cjs`：导入原提交中已经不存在的 `static/wonder_rituals.js`。
   旧八阶段仪式/编辑器后续工作已经归档；本轮没有重建退役模块来获得绿灯。
3. TV 两个 slow victory generator 测试：`generate_price_events()` 因当前共享 vanilla `prices.30` 宗教条件形状与旧模板不同而拒绝生成。
   `scripts/victory_task_codegen.py` 与起点提交一致；直接调用亦复现 `prices.30 religion condition shape changed`。
   因此 TV 全量 pytest/编辑器 full runner 不能宣称全部绿色。快速回归与本轮改动的生成器通过。

4. 本地图鉴构建输出了 195 条奇观记录、复制 191 张图片，报告四张既有缺图：Amber Room、Parthenon、Bangkok Grand Palace、Wat Arun。源码迁移保留现状；本轮没有调用图像 API 补图。

整目录补充迁移曾被自动审批以混合资料误归属风险拒绝。随后核对标题、mod ID、工具 README 和实际配图，形成 `verified_supplement.json`；先复制 65 项并提交恢复点 `a5fc3fcbb8cb`，验证离线工具后仅移除 63 个明确归 GP 的旧副本。两个 Steam 稿的 SoL 提示与 GP 正文混合，TV 原件保留，GP 有审校副本。旧链接和宣传文字没有对外更新。

上述原始复现日志随交接保存。原先归档的 AI observer、vanilla takeover 游戏内调查、编辑器改进计划继续归档；
本轮只为仓库拆分执行其现有静态回归，不重新开立玩法调查。

## 9. 接棒建议顺序

1. 先读本文件，再看 GP `data/extraction_provenance.json` 与 TV 工作树 diff。
2. 核对共享 base 四文件补丁与两个 loader 的 destination coverage 测试。
3. 在没有 TV checkout 的新目录 clone GP，连接 base；确认所有命令只使用 GP/base。
4. 运行下列命令。若出现本节以外的失败，先保留完整日志，不要加 baseline/skip 来消除它。
5. 检查三个兼容补丁、字体/称号 singleton 与 TV runtime dependency 的打包/加载顺序。
6. 游戏内启动、双 mod 联用和 Pages 迁移需要后续明确执行；不得从静态结果推断已验收。

```powershell
$py = 'C:\Users\Hades\anaconda3\envs\eu5\python.exe'
& $py scripts/bootstrap_base.py
& $py scripts/ai_context.py --files src/in_game/common/generic_actions
& $py scripts/build.py --check --date 2026-10-26
& $py scripts/validate.py --changed --fix --ai-report
& $py -m great_projects_editor_web --check
& $py -m pytest -q -n 4 --dist worksteal tests --basetemp=.pytest-audit
& $py scripts/run_editor_tests.py --full
& $py scripts/verify_extraction.py --source-repo ../eu5-towards-victory
```

`verify_extraction.py` 比较交付快照，正常后续修改也会使它报告差异；这不是“生成器过期”的替代检查。
`--source-repo` 是可选的审计输入，构建和编辑器不需要原仓库。
常规 `build.bat` 只打包到 GP `build/`；只有显式 `--deploy <MOD_DIRECTORY>` 才镜像到游戏目录。

## 10. 提交与恢复

GP 的初始本地提交、最终 clone 检查以及文件计数写在 `split_validation/results.json`。
TV 与 base 的修改保留为可审查的工作树变更，没有代替用户提交或推送。
不要只提交 TV 的删除而遗失 GP 仓库；也不要只同步 GP 而漏掉 base 的 coverage 配套修改。
恢复旧布局可从上述 TV 起点提交提取原文件；精确来源与新路径映射均在 provenance 清单中。
