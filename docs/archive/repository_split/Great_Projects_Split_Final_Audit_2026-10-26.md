# Great Projects 拆分最终审计（第三棒，2026-10-26）

审计基线：TV 起点 `2cf4171b4e273c87efb8257baef895c7a6017ad6`；GP 接棒提交
`165bf62`；共享 base 起点 `33e60f14164ad06fc227b2d9e7c365b6db67c561`。
本轮在 Windows、Python 3.11.15 的直接 EU5 解释器上执行，未使用 Linux 路径 shim。

**结论：第二棒的迁移完整性结论成立，三项 P2 已关闭；没有发现拆分新增的构建或运行代码阻断项。**
完整测试仍有下文列出的既有失败，不能称为全绿。本轮修复不改变游戏源文件或兼容补丁输出。

## 独立核验

- 修改前，GP `verify_extraction.py --source-repo ../eu5-towards-victory` 通过原始交付快照及源 Git blob 校验。
- TV 的 **5,527 个受控删除**与 provenance 的 **5,527 个 move**做集合比较，双向差集为空；所有 retained 目标存在。
- 从原 Git blob 重新读取迁出的 `src/`、`submods/` 中 **192 个游戏文本文件**，保留字符串、排除注释和空白后比较。
  只有 4 个文件存在差异，逐项核对后均为第一棒记录的失去工地通知 `.21` → `.22`：事件、调用 hook、EN/ZH 文本键。
  支持度挽救事件仍为 `.21`。本轮没有追加玩法变更。
- TV 327 个 / GP 35 个 action 无同名；消息类型、scripted effects、scripted triggers、game concepts 和 EN/ZH 本地化键均无交叉重复。
- GP 的 35 个实际 action 均由现有边界测试检查 AI `actions` 成员、同根消息类型及五字段本地化；验证器无错误或警告。
- 称号文件的唯一 `localization_key` 集合：TV 416、GP 412，TV 恰多 4 个领袖称号。
  第二棒的 420/416 是包含重复出现项的数量；两种计数都满足严格超集关系。
- 两个共享 loader 分别实跑 TV、GP 的 migration coverage：TV 本地 24 条，GP 本地 32 条，共享 369 条；
  GP 的 12 条迁入规则全部被要求存在，两个工作区均未遮蔽共享 ID。
- GP 开发代码的 TV 名称引用落在 `.eu5-base/reference_mods` 参考快照内。
  真实 freshness 构建在只复制 GP 的 scripts/data/src/submods/editor 并连接 base 的临时目录中通过，无 TV checkout 输入。

## 已补全

1. **本地产物归属**：把 TV 中 191 个离线预览文件（74,532,297 字节）及 2 个旧奇观图片 ZIP
   （1,199,913,008 字节）迁到 GP 的 `ai_gui_assessment/images/`、`assets/archives/`。
   逐文件 SHA-256 迁移前后相同，目的目录已由 GP 忽略；没有删除原图或覆盖目标文件。
   同时移除 TV `.gitignore` 的 atlas 白名单。残留空目录/已忽略 Python 缓存不进入 Git。
2. **PNG freshness**：`scripts/generate.py` 对静态 PNG 比较格式、帧数、尺寸和解码后的完整 RGBA 字节；
   不再把 zlib 压缩差异当成过期。其他文件继续逐字节比较。
   新增 7 项回归覆盖不同压缩级别、RGB/alpha/透明像素 RGB/尺寸变化、缺失或损坏图片及文本换行差异。
   此处没有锁死 Pillow，也没有重新提交缩略图来掩盖差异。
3. **失效知识指引**：删除 TV `object_on_built` 的 GP 测试命令和旧路由前缀；遗漏的 ritual similarity 规则迁到 GP，
   明确其工具已经退役、内容是历史证据，并补上 base 的 `destination_project`，保留原始来源条目。
   TV 和 base 的旧 ED 源路径标明 `eu5-great-projects:src/...`；base 的过时 lint 路径分支被移除，`src/in_game/` 检查仍在。
4. **额外发现的文档混用**：TV 的 Europedia 卡仍包含已迁走的生成/兼容命令，现改为运行依赖的集成边界说明。
   GP 卡中的 TV 胜利树例子标明来源仓库；GP IO 卡移除仅适用于 TV Trade League 和初始法律的设计要求。
5. **其他说明**：两个 README 明确 Python 3.11+；称号生成器说明各自实际职责和所需加载顺序；
   atlas README 明确当前 base 不含参考地图目录，正常使用仓库已提交的 tiles 和 locations index。
   三份知识 BRIEF 均由生成器更新。

## 实跑结果

完整命令、退出码及日志见 [final_audit_2026-10-26/](split_validation/final_audit_2026-10-26/results.json)。

| 检查 | TV | Great Projects |
| --- | --- | --- |
| 全量 pytest，含 slow，4 workers | 316 通过，2 个既有失败 | 890 通过，1 个既有失败 |
| Editor Node 合同测试 | 105 通过 | 127 通过，1 个既有失败 |
| Web `--check` | 通过 | 通过 |
| Headless Chrome 实际编辑器 | 6 页、资源/预览/外域404、两种视口、无 JS 异常 | 同左 |
| 全量静态验证 | 181 文件，无问题 | 189 文件，无问题 |
| `build.py --check --date 2026-10-26` | 不适用 | 50 生产者、81 输出，通过 |
| 最终 `validate.py --changed --fix --ai-report` | 通过，无错误/警告 | 通过，无错误/警告 |
| routing / lint fixtures | 通过 / 60 fixtures | 通过 / 60 fixtures |
| 最后文档修正后的聚焦回归 | 9 通过 | 18 通过，含 PNG 与 action 注册检查 |

PNG 跨编码器风险用不同压缩参数的真实 PNG 在本机回归；本轮没有另开 Linux 环境。

既有失败独立复核如下，未新增 skip、baseline 或 suppression：

- GP Python：`test_gui_only_ritual_variables_are_suppressed_in_standalone_ed` 期待旧 GUI 的
  `tv_wonder_ritual_position_1`；直接查询 TV 起点提交的 ED GUI，同样没有该变量。
- GP Node：`wonder_rituals.cjs` 导入不存在的旧 `wonder_rituals.js`；起点提交包含测试而没有该模块。
- TV 两个 slow victory generator 测试：`prices.30 religion condition shape changed`。
  `scripts/victory_task_codegen.py` 与起点相同，失败仍是既有模板与当前 base reference 的不匹配。

这些属于已记录的归档/既有事项，本轮没有恢复退役仪式模块或修改胜利玩法。

## P3 处置和证据边界

- 修复了 Python 版本说明、称号 docstring、atlas 输入说明、base 旧路径、TV atlas 白名单和本地归档归属。
- 继承的本地规则仍可能在 TV/GP 各有一份。没有机械提升到共享 base：其中包含具体项目 IO/GUI 约定；
  是否成为通用引擎规则须另行逐条确定。它们不构成跨 checkout 依赖，也不遮蔽 base ID。
- 兼容补丁对 GP 的精确日期版本仍由 GP 版本工具同步；TV 对 GP 保持 `*`。这两种关系的用途不同，本轮保留。
- 部分合成测试夹具保留旧根名，用于虚拟多根数据或拒绝旧路径的断言，不是开发输入路径。
- 没有启动 EU5 或核验实际启动器的 TV/GP 加载顺序；没有部署到游戏、发布 Pages、创建远端仓库或推送。
  原先归档的玩法调查仍保持归档。离线结果不代表游戏内加载验收。

## 提交与快照

本轮修改留在 **TV、GP、base 三个工作树**，未代替用户提交。
GP 原始 `data/extraction_provenance.json` 保持不变；修复后的正常差异会使旧快照校验报告不同，
不应重写旧哈希把历史证据变成当前状态。新增审计证据记录修复文件及 SHA-256，freshness 则验证当前生成结果。

第一棒补丁副本作为历史证据保留；当前 base 的完整配套补丁另存为
[Great_Projects_Base_Final_Changes.patch](Great_Projects_Base_Final_Changes.patch)。
同步仓库时须包含 base 的 ownership/loader 配套变化以及 GP 的源文件和本轮修复，不能只提交 TV 的删除。
