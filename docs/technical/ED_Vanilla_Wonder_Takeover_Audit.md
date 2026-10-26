# ED 原版奇观接管：审计报告

> 审计对象：worker 依据 [ED_Vanilla_Wonder_Takeover_Handoff.md](ED_Vanilla_Wonder_Takeover_Handoff.md)（下称“交接”）
> 交付的未提交改动集，工作区 `eu5-towards-victory`。
> 审计性质：只读审计。本文件之外无任何编辑。
> 审计日期：2026-10-22。
> 结论：**有条件通过**。核心机制（写入改写、读取转接、封存、灾害分流）与交接契约一致，可回归项全部复现；
> 但存在 2 处校验层做法与仓库知识归属规则冲突、1 处丢失的文件编码、1 处守卫表达力弱于设计描述的清理逻辑，
> 以及 1 处影响面超出交接描述的数据放宽（设计已接受，须转为实机检查项）。逐条见第 3 章。

## 1. 审计范围与方法

### 1.1 实际改动集并不等于 `git status`

工作区在 git 层面显示 1688 个条目（1652 修改 / 8 删除 / 28 未跟踪），但其中 **1578 个“修改”是纯换行符差异**：
仓库索引内是 LF，工作区是 CRLF，且仓库没有 `.gitattributes`、`core.autocrlf` 也未设置。这类差异遍布 1652 个文件
（包括 `CLAUDE.md`、`src/in_game/common/scripted_effects/tv_trade_league_effects.txt` 等与本次任务无关的文件），
不属于 worker 的改动。

按内容差异重新统计，本次交付的实际改动是：

| 类别 | 数量 |
| --- | --- |
| 内容有变化的已跟踪文件（1652 个修改中） | 74 |
| 新增未跟踪文件 | 28 |
| 已删除文件 | 8 |
| 仅换行符差异（非本次改动） | 1578 |

后文所有结论均基于这 74 + 28 + 8 个文件。涉及换行符的说明单列于 3.7。

### 1.2 验证环境

`.eu5-base` 在本沙箱中是不可读的链接（`Input/output error`），无法原地运行仓库脚本。审计采用镜像法：
把仓库复制到临时目录，将 `.eu5-base` 指向 `eu5-modding-base` 的真实挂载，在其中运行交接第 7.1 节的命令。
由于改动的都是源数据与生成器，镜像执行与原地执行等价；但第 3.7 节说明这会影响 `--changed` 的覆盖面。

### 1.3 独立复核方式

不复用 worker 的结论。重建了三类独立证据：

1. **生成物重放**：直接调用 `vanilla_takeover.render` / `rewrite` 重新生成全部 7 个产物，与仓库内文件逐字节比对。
2. **差异逐块阅读**：把 59 个被复制定义的“改写前 / 改写后”做 unified diff，逐块人工核对改写点是否落在 5.2/5.3 允许的形态内。
3. **第三方旁证**：在原版参考镜像里独立搜索载体 key 的全部出现位置，与扫描器的 99 个位点比对；语义断言以
   `reference_official_defines/docs/{triggers,effects,event_targets}.log` 为准，不以 worker 文档为准。

## 2. 复现结果

以下均在镜像中实际执行，不是引用 worker 记录。

| 项目 | 命令 | 结果 |
| --- | --- | --- |
| 覆盖报告 | `vanilla_takeover/report.py` | 47 个载体、99 个位点：改写 75 / 开局对齐 20 / 保持 4，无“未处理”，退出码 0 |
| 接管契约测试 | `pytest tests/test_vanilla_wonder_takeover.py` | 28 passed |
| 场地审计 | `audit_unique_wonder_site_requirements.py` | 退出 0；PASS 113 / FAIL 0 / INTENDED 22，无 `BASELINE DRIFT` |
| 机制规则 | `test_wonder_mechanics_rules.py` | `[OK] 191 wonders, 135 unique wonders` |
| 相关回归 | `pytest test_wonder_ownership / test_engineering_department_ai / test_wonder_priority_proposals` | 254 passed |
| 胜利任务 | `scripts/test_victory_path_tasks.py` | 静态检查通过 |
| 全量校验 | `validate.py --fix --ai-report` | 376 文件，0 errors / 0 warnings |

补充的独立检查：

- 7 个生成器重放产出与仓库文件逐字节一致（含 `on_action`）。
- 7 个新产物括号配平、顶层定义无重复；`damage_overrides` 三个 `REPLACE:` 块的 `else` 分支包含原版函数体原文（逐字为真）。
- 开局清理的调用数与开局位点数一致：12 次 `destroy_art`（12 个艺术品开局实例）+ 8 次 `destroy_building_forcefully`
  （8 个建筑开局实例，全部在 1337 剧本）。
- 全仓搜索 `unique_bastille` / `tv_wonder_bastille`（排除交接第 2.1 节授权范围）零命中；135 座独特工程、id 198 空位不复用。
- 6 座迁移工程的新地点在索引 `tv_wonder_unique_id_to_location` 中全部就位（117→paris、126→shanyang_huaian、
  131→tehotihuacan、141→amesbury、145→pushkino、197→avranches），旧地点映射零残留。
- `src` 中残留的 9 处 `location:tenochtitlan` 经核对属于独立工程 `unique_tenochtitlan_causeways`（id 118），
  不是迁移遗漏。

## 3. 发现

按严重度排序。每条给出证据位置、影响与建议；本报告不实施修改。

### 3.1 中高：`sacred_mountain` 场地规则被整体放宽（D8 的副作用超出交接描述）

`data/wonder_site_rules.yaml:282` 的 `sacred_mountain.trigger_script` 现在包含 `topography = wetlands`。
这是 D8 明确授权的临时修正，本身不算越权。问题在于它改的是**通用工程的场地规则**，而交接把该改动描述为
“不改圣米歇尔山的基底”。

实际影响面（独立统计）：

- 通用工程：`data/wonders.yaml` 的 56 个通用 key 中，只有 `sacred_mountain` 一个使用该基底，因此通用侧影响仅限这一类，
  但它对全地图所有玩家/AI 的选址池生效。
- 独特工程：另有 4 座以 `sacred_mountain` 为 `base_key` 的独特工程一并受影响——`unique_potala_palace`、
  `unique_machu_picchu`、`unique_lalibela_churches`、`unique_changbai_mountain_altar`。这 4 座的地点都在山地/高原，
  放宽湿地不会让它们变更地点，但会让它们的“场地规则满足”判断在湿地点上也成立，属于多余的放宽。

交接第 10 章预先答复说“不要顺手修通用候选扩大”，意味着用户已知该副作用存在、但接受它作为临时折中。

判定：**设计已接受，实现无缺陷**。但审计建议把它列为实机验收的必查项——因为它改变的不只是一座工程，而是
一类工程在全地图的选址池。若验收发现 AI 大量把神圣山城建在沼泽，应回到“给圣米歇尔山换基底”的方案，
而不是继续放宽规则。

### 3.2 中高：`validate.py` 的共享规则被就地加白名单，违反仓库知识归属规则

`scripts/validate.py` 被改了两处，都属于“按规则 id 特判跳过”：

1. `yaml_localization_non_ascii_quotes` 在非 `.yml/.yaml` 文件上直接 `continue`（第 379 行）。
2. `eu4_province_modifier_scope` 在 `_modifier_scope_at(...) == "province"` 时跳过（第 391 行），并新增
   一个 20 行的 `_modifier_scope_at` 作用域推断函数（第 401–419 行）。

两处各有可辩护的事实依据：

- 弯引号：原版 `flavor_FRA.txt` 的事件注释里确有 `d’Opera`，交接要求“除改写点外逐字保留”，因此注释被原样带入。
- `add_province_modifier`：`reference_official_defines/docs/effects.log:367` 明确写 **Supported Scopes: province**，
  而 `docs/knowledge/anti_patterns_shared.yaml:209` 的这条规则仍声称“EU4 省份效果在 EU5 不存在”。规则的
  provenance 已经过时。

问题在于修法。仓库 `CLAUDE.md` 规定：共享规则变更要改规则卡并更新其 provenance，且基础仓库与本地知识要分开维护；
`anti_patterns_shared.yaml` 是共享知识。现在的做法是在校验器里按 id 写例外，造成三处不一致：

- 规则卡仍说“用 location 效果替代”，而校验器对 province 放行——同一个仓库里同时存在互相矛盾的两种指引。
- 例外只写在 `scripts/validate.py` 里。基础仓库的 `scripts/ai_context.py` 会把 `anti_patterns_shared.yaml` 原样
  分发给 agent 作为规则文本，那里仍然是旧结论；也就是说人会看到“不能用”，校验器却放行。
- `_modifier_scope_at` 是启发式：`province = { every_location_in_province = { add_province_modifier } }`
  会推断为 `location` 而报错（实测正确），`scope:target_province` 平铺会推断为 `province` 而放行（实测正确），
  未识别的作用域（如 `capital.market`）返回 `None` 从而维持报错（实测正确）。风险在于它的识别集是白名单：
  只认 `province*` / `location*` / `owner` / `controller` / `c:*`，将来若新增别的省份同义作用域，
  会被当作“未进入省份”而误报（而非漏报），因此是偏保守的失败方向。

判定：**事实正确、层次错误**。建议把 `eu4_province_modifier_scope` 的规则卡改写为“province 作用域合法，
location/country 非法”，删除 `validate.py` 的 id 特判；弯引号同理应在规则卡里声明“仅适用于本地化文件”，
而不是在 Python 里按后缀分流。

### 3.3 中：开局对齐的两个守卫退化成了“该地点有主”，与交接 4.5 的描述不等价

`tv_vw_startup_reconcile_effect` 的开局清理逻辑，两个分支的守卫都是把同一个地点与它自己比较：

```pdx
# 建筑分支（render.py:104）
location:lubeck = {
	if = {
		limit = { owner ?= location:lubeck.owner }      # 地点的所有者 与 同一地点的所有者 比较
		destroy_building_forcefully = "building(building_type:hanseatic_town_hall|owner)"
	}
}
# 艺术品分支（render.py:99）
work_of_art:stonehenge ?= { location.owner ?= location:amesbury.owner }
```

交接 4.5 的措辞是“若其所在地点的所有者 = `location:<S>.owner`”，隐含两处不同地点之间的比较。但生成器把
“载体所在地点”和“ED 工程地点”当成了同一个：建筑分支直接在 `location:<S>` 内执行，艺术品分支先在
`work_of_art:<A>` 上比较。结果条件是：

- 建筑分支：`location:<S>.owner ?= location:<S>.owner` —— 只等价于“该地点有主”。
- 艺术品分支：`作品所在地点.owner ?= location:<S>.owner` —— 因为全部 12 个艺术品载体与 3 个津巴布韦建筑载体的
  剧本地点都与工程 `location` 逐一相同（独立核对），它同样只等价于“该地点有主”。

所以守卫不会筛掉任何“所有者不符”的实例，只筛掉无主地点。对 1337 剧本而言结果正确（这些地点开局都有主），
但存在两个后果：

- 若将来某个载体的剧本地点与工程地点不同（新增一个在别处生成、或工程改址），守卫不会发现差异，
  会按“有主”就删，误删别处的实例。
- `tests/test_vanilla_wonder_takeover.py:218` 把这条字面表达式当作契约断言，等于把这种退化锁进测试。

判定：**当前无行为错误，但守卫的表达力弱于设计描述，且测试在保护这个弱化版本**。建议分别处理两种载体：
建筑分支改为比较“剧本实例地点”与工程地点（不一致则报错而非静默删），艺术品分支保留现有比较并补一条
“载体地点必须等于工程地点”的断言；否则至少要在注释与交接 4.5 里写明该条件对当前剧本只起“有主”判断作用。

### 3.4 中：`data/unique_wonders.yaml` 丢失 UTF-8 BOM

`data/unique_wonders.yaml` 在已提交版本里以 UTF-8 BOM 开头，工作区版本已无 BOM。本次改动中这是唯一一处 BOM 变化：
其余 43 个 `data/*.yaml` 原本就无 BOM，`data/unique_wonder_ritual_designs.yaml` 与 `..._zh.yaml` 两个原本有 BOM 的文件保持不变。

影响：所有读写方都用 `utf-8-sig`（`_core.py:1234` 经 `load_yaml`、`merge_ceremony_cost_options.py:149/164`），
所以当前不会出错。但 `merge_ceremony_cost_options.py:164` 会以 `utf-8-sig` 写回，下次该脚本运行时 BOM 会被
重新加回，产生无意义的 diff；同时该文件是本项目的核心数据文件，编码状态应保持稳定。

判定：**低风险但应修复**。不属于任何 WP 的授权改动，属于手工编辑的附带损伤。

### 3.5 中：两处接管门的判据地点与写入地点分离，其中一处依赖上游事件

`flavor_mug.8` 的写入发生在 `capital ?= { … }` 内，而门的判据是 `location:delhi.owner ?= root`。
当莫卧儿的首都不是德里时：门不通过 → 走原版 `create_art`（在首都创建）；门通过（首都是德里）→ 改为 ED +1。
两种结果都自洽，且与交接 5.2“replace 模式回落原版写入”一致。

`flavor_chi.52` 的情况不同：该事件的写入作用域是 `scope:target_location`，而该 scope 是在**上游事件
`flavor_chi.51` 的 `immediate`** 里由 `location:shangyuan` 保存的。琉璃塔的 ED 地点同样是 `shangyuan`，
因此门与作用域一致，无问题；但这一致性依赖上游事件，若上游地点变化而工程地点不改，门会静默失配。

判定：**当前正确，属脆弱耦合**。交接第 6 章未记录“载体写入依赖上游事件的 save_scope”这一点，建议补记，
因为它是唯一一个门地点由另一个事件提供的情形。

### 3.6 中：1658 剧本通过 `include` 复用 1337，交接“1658 不含载体”的前提不成立

交接第 2.3 节与第 10 章都写“1658 剧本当前不含任何载体，扫描结果为空是正常的”，并据此把“只扫描 1337”当作充分条件。
实际检查发现 1658 的四个相关文件都是 stub，靠 `include` 复用了 1337：

```
main_menu/setup/1658/02_core.txt                  → include = "setup/1337/02_core"
main_menu/setup/1658/06_pops.txt                  → include = "setup/1337/06_pops"
main_menu/setup/1658/07_cities_and_buildings.txt  → include = "setup/1337/07_cities_and_buildings"
main_menu/setup/1658/11_art.txt                   → include = "setup/1337/11_art"
```

也就是说 1658 开局同样会载入这 20 个载体实例（12 艺术品 + 8 建筑），只是实例定义写在 1337 的文件里。
这带来两个后果：

- 交接里“扫描 1658 结果为空”的观察是**扫描器行为**（它只按文件路径识别 `main_menu/setup/*/`，不解析 `include`），
  不是游戏行为。若将来某次版本更新给 1658 加了本地覆盖（在 `include` 之后写自己的实例），扫描器仍会看到 1337 的那份，
  而游戏里会同时存在两份实例。
- 好消息是 `tv_wonder_vw_startup_reconcile_on_game_start` 是 `on_game_start` 钩子而非剧本初始化脚本，因此
  无论哪个剧本开局都会执行同一份清理逻辑，**当前行为正确**。

判定：**当前无行为错误，但交接的事实陈述有误，且扫描器对 `include` 无感知**。建议把交接第 2.3/第 10 章关于
“1658 为空”的表述改为“1658 通过 include 复用 1337，因此与 1337 同一组实例”；并在扫描器的已知限制里写明
不解析 `include`，避免下次版本升级时误信“扫描为空”。

### 3.7 低：`validate.py --changed` 在当前工作树下不可复用，交接中的“99 文件”无法复现

`validate.py` 的 `--changed` 走 `git diff --name-only HEAD`。当前工作树有 1652 个文件因换行符被标记为修改，
按该口径会选中 363 个 mod 内文件（`.txt/.yml/.yaml/.gui/.md/.py`，位于 4 个 mod 根），而不是交接 WP-8 记录的 99 个。
审计在镜像中实测到 `--changed` 选中 0 个文件（镜像不是 git 仓库），全量运行才是有效的复核方式（376 文件，0 error）。

这不是 worker 的过错（换行符问题早于本次任务），但意味着：

- 交接进度表里的“检查 99 文件”**无法在当前位置复现**，只能靠全量运行等效验证。
- 建议在验收脚本里改用显式文件列表（交接的 `--files` 习惯），或在仓库加入 `.gitattributes` 固定 `*.txt`/`*.yml` 的换行，
  否则每次全仓 `git diff` 都会淹没真实改动。

### 3.8 低：新增的 7 个产物用 LF，同目录既有产物用 CRLF

新产物（`tv_vw_vanilla_*.txt`、`0000_tv_vw_vanilla_event_overrides.txt`）全部是纯 LF 且带 BOM；
同一目录下既有的 `tv_engineering_department_*_triggers.txt`、`tv_engineering_department_pulse_bridges.txt`
是纯 CRLF。`render.py:25` 以 `newline="\n"` 写出，是刻意的。

对引擎无影响（Jomini 两种都接受），但与仓库既有生成器的输出习惯不一致；由于没有 `.gitattributes`，
在 Windows 上经 git 检出后这些文件会变成 CRLF，再生成又会变回 LF，形成长期抖动。

判定：**建议统一，不阻塞**。

### 3.9 低：`tv_wonder_vw_startup_reconcile_on_game_start` 未包 `hidden_effect`

同目录既有的 ED on_game_start 钩子（`tv_wonder_initialize_index_on_game_start`、
`tv_wonder_initialize_existing_unique_wonders_on_game_start`）都把主体包在 `hidden_effect` 里；
新钩子直接内联调用 `tv_vw_startup_reconcile_effect`（`render.py` 生成的 on_action 文件仅 9 行）。

`destroy_art` 与 `destroy_building_forcefully` 都带 effect localization，若在 `on_game_start` 中不隐藏，
可能在开局瞬间产生与玩家无关的提示。交接 7.3 已把“开局移除的时序”列为实机项，因此这条属于**待实机确认**的低风险项，
但如果确认有提示刷屏，修法就是加一层 `hidden_effect`（与既有钩子一致）。

### 3.10 信息：封存对 12 个“`always = no`”建筑无额外约束力

21 个被封存的建筑按原版 `allow` 的实际内容可分为三组（独立核对原版定义）：

| 组 | 数量 | 成员 | 封存前可否手动建造 |
| --- | --- | --- | --- |
| `allow` 内含 `always = no` | 12 | `lighthouse_of_alexandria`、`forbidden_city`、`red_fort`、`versailles`、`woodhenge_of_cahokia`（在 `custom_tooltip` 内）、`tower_of_belem`、`el_escorial_palace`、`fra_louvre_museum`、`schonbrunn_palace`、`zwinger`、`monument_kairouan_mosque`、`enderun_academy` | 否 |
| `allow` 有条件但可满足 | 5 | `alhambra`、`venetian_arsenal`、`great_enclosure`、`great_hill_complex`、`great_valley_complex`（均为 `is_capital = yes` + `country_has_no_other_copy_of_building`） | 是 |
| 原版无 `allow` 块 | 4 | `kremlin`、`khmer_baray`、`hanseatic_town_hall`、`ibadat_khana` | 是 |

因此封存真正改变行为的是后两组 9 个建筑；第一组 12 个本来就不可建，追加的 `custom_tooltip` 只影响提示文案。
判定：**实现正确**。此处记录是为了回答“封存到底拦住了什么”，避免验收时把 12 个本就不可建的当作成果。

### 3.11 信息：灾害分流的三臂在 191 座工程上按建筑类型分派，语义自洽

`tv_vw_vanilla_damage_overrides.txt` 的三个 `REPLACE:` 块各有 303 个 `if/else_if` 分支，覆盖 135 座独特 +
56 座通用工程（191 个 key）。逐项核对：

- 每支的 limit 都是 `prev = { building_type = … building_level >= 2 }`，1 级工程不匹配任何分支，
  因此 `else` 不会执行到原版的 `change_building_level_in_location`（该调用在 `prev.building_level = 1` 时
  `floor(-0.1 × 1) = -1`，会直接拆掉建筑）。
- 通用工程在地点作用域调用 `tv_wonder_lower_generic_level_effect`，与 `tv_wonder_level_change_effects.txt:19`
  声明的“Location scope”一致。
- 原版 `else` 分支为逐字原文（三个函数体均验证为真）。

判定：**与 D4 完全一致**。唯一可用性提示：单个函数内有 303 个 `else_if`，原版单次灾害最多命中数个建筑，
性能无虞，但文件体积（3687 行 × 3 份几乎相同的分派链）值得在后续把分派链抽成共享 scripted_effect 以减少重复。

### 3.12 信息：`present_at_level` 的推导与覆盖值全部一致，但推导本身在“开局载体”分支下恒为 1

`scan.py:29` 的推导是：有开局实例 → 1，否则 `initial_level + 1`。
核对 47 个载体的实际取值：除 `kremlin` 与 `woodhenge_of_cahokia`（显式写 2）外全部为 1，与交接第 6 章一致。

值得注意的是：对有开局实例的载体，推导**无条件**返回 1，忽略 `initial_level`。`notre_dame` 与 `pisa` 的
`initial_level` 被 D6 从 0 改为 1，正好使“开局 1 级”与“原版载体存在”两种表述对齐；但若将来某座工程的
`initial_level` 与剧本不一致，这个分支不会报警，只会静默取 1。`scan.py:197` 只检查了 `initial_level == 0`，
没有检查 `initial_level` 与剧本等级的匹配。

判定：**当前正确**，属可加固点。

### 3.13 信息：`baseline` 与审计脚本一致，但 `INTENDED` 与 `UNKNOWN` 的归类口径要留意

场地审计输出 `INTENDED 22`，其中 `unique_teotihuacan` 与 `unique_grand_canal` 记录为 UNKNOWN 并写明用户确认依据
（`tehotihuacan` 与 `tetzcoco` 相邻；山阳毗邻洪泽湖）。交接要求“脚本因无法解析 `any_neighbor_location` 报错则停下”，
实际脚本没有报错，而是走了“无静态数据 → UNKNOWN”的既有路径，因此未触发停止条件。

判定：**符合交接意图**。此处只是提醒：这两条 UNKNOWN 的成立依赖用户的人工确认，不是脚本证据，
实机验收时应优先查看特奥蒂瓦坎能否在开局正常显示为可建。

### 3.14 信息：多语言本地化删除范围经用户授权，已执行且零命中

除英文/简中外的 9 种语言里，`tv_engineering_department_wonder_mechanics_l_<lang>.yml` 各删 41 行、
`tv_wonder_ceremony_l_<lang>.yml` 各删 6 行，全部为键名或值中含 `bastille` 的条目；未新增任何翻译。
交接第 10 章所述“空段落注释保留不整理”也做到了。全仓（授权范围外）零命中。

## 4. 未发现问题的地方（已核对，供交接归档）

以下项目经独立复核确认为正确，不再需要在验收中重查：

| 项目 | 核对方式 | 结论 |
| --- | --- | --- |
| 复制事件用裸 id、决议用 `REPLACE:` | 解析 59 个复制定义 | 55 事件裸 id、4 决议带前缀，无混用 |
| 事件副本不含 `REPLACE:` | 全文搜索 | 0 命中 |
| 辅助定义改名闭包 | 解析 5 个辅助定义 | `is_yuan_china`、`upgrade_great_wall`、`is_part_of_yellow_river_near_canal`、`destroy_/repair_grand_canal_china` 全部改为 `tv_vw_` 前缀，事件内引用同步 |
| 单一归属 | 全仓 4 个 mod 根 | 同一原版事件 id / `REPLACE:` key 无重复定义 |
| 封存建筑恰一个 `allow`、其余字段逐字 | 21 个定义做 diff | 只有目标行变化，`allow` 唯一 |
| 写入改写的位置与形态 | 59 段 diff 逐块阅读 | replace 为 `if/else` 包裹、augment 为原句后追加，未出现同块多写 |
| 读取改写的作用域 | 逐位点核对祖先链 | `has`/`level`/`max`/`art_here` 均在地点作用域，`owned`/`anywhere` 按 5.3 替换 |
| 4 处“保持”位点 | 与交接 6.1/6.2 对照 | `random_work_of_art_in_location` 4 处原样保留 |
| `tv_vw_vanilla_*` 全部登记 | `data/generated_files.yaml` | 7 个条目，脚本/输出/数据依赖均存在 |
| pulse 注册 | 两个 bridges 文件 | 只在 ED 侧、紧跟既有初始化，主 mod 无该钩子 |
| 本地化键 | 英文/简中 | 各 1 键，BOM + CRLF，ASCII 直双引号 |
| `_core.py` 字段校验 | 负例测试 | kind/mode/op/replace+op/重复 key/waiver 均报错 |
| 135 座 / id 198 | 数据统计 | 计数正确，198 留空未复用，其他 id 未重排 |
| 地点上限 ≤3 | 数据统计 | 通过；巴黎恰为圣母院、卢浮宫、凡尔赛 |
| 7 个产物语法面 | 括号配平 + 顶层重名 | 全部平衡、无重名（55/3/28/55/21/4/1 个顶层定义） |
| 生成器可重放 | 逐字节比对 | 7 个产物与重放结果完全一致 |
| 落点在允许形态内 | 59 段 diff 全读 | 未发现 5.3 表外的读取形态，亦未触发第 9 章任一停止条件 |

## 5. 建议的处置顺序

1. **3.2**（校验层归属）优先处理：改规则卡而不是校验器。这是唯一会随基础仓库同步扩散的问题。
2. **3.4**（BOM）与 **3.3**（开局清理守卫 + 锁定它的测试）作为同一批小修：都属“当前不报错、但会误导后人”。
3. **3.7 / 3.8** 建议一并解决：加 `.gitattributes` 或统一生成器输出换行，否则交接里的 `--changed` 验收永远无法复现。
4. **3.1** 与 **3.9** 留给实机验收：前者看 AI 是否把神圣山城建到沼泽，后者看开局是否有拆除提示。
5. **3.5 / 3.6 / 3.12 / 3.13** 只需在交接与扫描器注释里补说明，不需要改代码。

## 6. 审计结论

worker 的交付在执行层面是扎实的：99 个位点全覆盖、生成物可重放、改写点全部落在允许形态内、原版回落保留、
回归全绿。7 个生成器、5 个库文件、7 个产物、42 份载体声明与交接第 6 章逐项吻合，没有发现“多改”或“漏改”。

需要退回处理的是三类问题：校验层次错误（3.2）、编码损伤（3.4），以及“守卫表达力弱于设计描述、测试锁定弱化版本”
（3.3）。三者都不影响当前游戏行为，但都会在后续维护中误导读者。3.5 与 3.6 不改代码，只需在交接受理文档里
补记两处事实（隐式 save_scope 依赖、1658 通过 include 复用 1337）。

D8 的副作用（3.1）是设计已接受项，不是实现缺陷；审计只要求把它从“临时修正”提升为实机验收的显式检查项，
并明确记录到 4 座共用该基底的独特工程。

## 7. 本报告不涉及的事项

- 未做任何实机测试（交接 7.3 所列项仍归用户）。
- 未修改任何源文件、生成物、测试或交接文档。
- 未评估 42 座之外的约 190 个原版奇观身份（交接 2.3 已明确不接管）。
- 未评估外观、图标、图片资源（本次任务未触及）。
