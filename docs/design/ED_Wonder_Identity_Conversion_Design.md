# 伟大工程身份转化（ED）——可行性与方案草案

> 状态：已实现（2026-10-24），采用第 6 节的建议；已完成离线测试与显示检查，尚未游戏内验收。
> 起因：圣索菲亚大教堂 1453 年后被改为清真寺。我们想让穆斯林玩家付出代价，通过决议完成转化，并保留当前等级。

## 1. 结论

现有架构**支持**这个功能，但应当做成“同一座工程，切换身份状态”，**不要**做成“拆掉一座工程，再建另一座”。

| 依据 | 现状 | 结论 |
| --- | --- | --- |
| 最终建筑效果与宗教无关 | `tv_wonder_unique_hagia_sophia_inaugurated` 只有 `local_cultural_tradition`、`local_cultural_influence`、`global_pop_conversion_speed`；`allow` 里的 `dominant_religion = owner.religion` 只用于直接建造 | 转化不需要改动建筑，等级自然保留 |
| 每座奇观只有一个最终建筑（仪式重写，2026-10-23） | 已废除风格变体建筑 | 不应因为宗教再引入变体建筑 |
| 每个地点最多 3 座独特工程（硬性规则） | `constantinople` 已有 `unique_hagia_sophia`、`unique_topkapi_palace`、`unique_enderun_palace_school` | 新增一个“阿亚索菲亚清真寺”条目会超出上限 |
| 外部升降级接口每次只变动一级，且是排队任务 | 见 [Wonder_Level_Change_Interface.md](Wonder_Level_Change_Interface.md) | “拆旧建新再补到 N 级”需要 N 天，还会触发完整的失去奇观生命周期，不可取 |
| 原版已有同一机制 | `mysticism_vs_jurisprudence.21` 设置全局变量 `hagia_sophia_now_mosque`，并执行 `force_city_gfx_rebuild = location:constantinople`；`on_religion_changed` 与 `on_location_changed_owner` 在基督徒重新取得时移除该变量 | 直接复用这个全局变量作为唯一状态来源，就能与原版事件、城市外观和自动复原保持一致 |

## 2. 方案：身份变体（identity variant）

### 2.1 数据

在 `unique_wonders.yaml` 的条目上增加可选字段 `identity_variants`。实际字段见该文件的圣索菲亚条目；下列为原始设计示意：

```yaml
identity_variants:
- key: mosque
  state: { global_variable: hagia_sophia_now_mosque }   # 复用原版变量，不新建状态
  potential: muslim_owner_and_muslim_dominant           # 见 D2
  cost: ...                                             # 见 D3
  name_en: Hagia Sophia Grand Mosque
  name_zh: 圣索菲亚大清真寺
  desc_en / desc_zh: ...
  image: tv_wonder_unique_hagia_sophia_mosque            # 新图，走现有 img2img 流程
  ritual_text: { 1: ..., 2: ..., 3: ... }                # 只换文本，三种风格的效果仍继承 sky_dome_grand_temple
```

加载器和 schema 已校验状态变量、条件脚本、正数金钱倍率、中英名称与描述、全部三组仪式文本，以及可选的原版事件接入信息。

### 2.2 转化决议

- 由 `gen_tv_wonder_identity_effects.py` 生成到 ED 的 `decisions/tv_wonder_identity_decisions.txt`，与重新仪式化决议使用相同分类。决议不是 generic action，因此没有新增 generic action 注册。
- `potential` / `allow`：拥有 `constantinople`，地点上存在最终建筑（等级 ≥1），尚未转化，没有正在进行中的同一工程项目（阶段 ≥3），并满足 D2 的宗教条件。
- `effect`：
  1. 支付代价（D3）；
  2. `set_global_variable = hagia_sophia_now_mosque` 以及 `force_city_gfx_rebuild = location:constantinople`（与原版写法相同）；
  3. 按 D4 处理当前仪式；
  4. 次日调度已有的 `tv_engineering_department.9502` 重同步，用来刷新地点显示和缓存。
- 等级：建筑本身不动，所以无需调用升降级接口。

### 2.3 显示

- ED 面板、百科卡片和地点显示根据变量选择名称、描述、图片和仪式文本。
- 原版建筑的静态名称（`building_type` 的本地化键）无法随状态改变。历史上它一直叫 Ayasofya，所以保留“圣索菲亚”作为建筑名是可以接受的，可以在描述里注明当前身份。
- 图片通过 `GetConceptTexture(Select_CString(...))` 选择注册过的图片概念；不把字符串 DDS 路径当作纹理句柄。面板、地点与百科均读取原版全局变量，教堂/清真寺离线严格渲染均无缺失绑定或资源。

### 2.4 与原版和现有生命周期的衔接

- 原版事件 `.21` 的触发条件包含 `NOT = { has_global_variable = hagia_sophia_now_mosque }`，所以决议与原版事件不会重复执行。是否保留原版事件见 D5。
- 自动复原：基督徒征服或所有者改宗基督教时，原版会删除该变量，身份随之复原，等级不受影响。
  - 易主时，ED 已经会把仪式清为朴素，这里不需要额外处理。
  - 所有者改宗的缺口已补齐：ED 的 `on_religion_changed` 回调撤销当前仪式，并在次日重同步。地点上的仪式身份标记只记录需要清理的旧奉献，显示与转化条件始终以原版全局变量为准。基督教征服还会清除该标记，避免后续教派变更错误撤销新仪式。
- `ED_Vanilla_Wonder_Takeover_Design.md` 原先记载“`hagia_sophia_now_mosque` 不接管”。本方案只读取这个变量，并在原版语义内写入，不重定向原版的写入，所以与该决定不冲突。

## 3. 其他类似工程（ED 独特工程清单内）

筛选标准：转化发生在 1337–1836 年间（或有明确的历史先例可以反向发生），建筑本身被保留，功能类别不变。

| 优先级 | 工程 | 历史 | 适用性 |
| --- | --- | --- | --- |
| 强 | `unique_hagia_sophia` | 1453 年由教堂改为清真寺；1204–1261 年间还曾是拉丁礼主教座堂 | 本提案 |
| 中 | `unique_alhambra`（granada） | 1492 年后，纳斯尔王宫成为天主教双王的王室居所，宫内清真寺改为圣玛利亚教堂 | 方向相反：穆斯林→基督教，属于宫殿身份转化，机制同 palace_of_nations |
| 中 | `unique_dome_of_the_rock`（jerusalem） | 1099–1187 年十字军时期改为 Templum Domini，1187 年复原 | 开局前的先例；游戏中基督教国家夺取耶路撒冷时可以双向转化 |
| 中 | `unique_malbork_castle` | 1457 年由条顿骑士团总部变为波兰王室城堡 | 非宗教转化（骑士团→王室），触发条件改为国家或政体 |
| 弱 | `unique_notre_dame_de_paris` | 1793 年改为“理性神殿” | 需要革命政体等条件，EU5 中没有对应宗教，暂不建议 |

不适用的情况（应走降级、劫掠或拆除，而不是身份转化）：

- 瓦拉纳西（1669 年 Kashi Vishwanath 被拆毁后改建清真寺）、特诺奇蒂特兰大神庙：都是拆毁后新建。
- 法罗斯灯塔：1477 年用它的石料修建了盖特贝城堡，功能类别改变了。
- 吴哥窟：由印度教转为佛教是开局前渐进完成的，没有一个明确的“决议时刻”。

建议 v1 只做圣索菲亚，同时把数据字段做成通用的；阿尔罕布拉、圆顶清真寺、马尔堡等之后作为数据补充。

## 4. 不采用的方案

- **新增独立的“清真寺”工程条目，转化时拆旧建新**：会超出每地点 3 座的上限，与“一个奇观一个最终建筑”冲突，需要多天补级，并触发失去奇观的生命周期。另外，计数、胜利统计和百科都会把它当成两座工程。
- **为宗教变体建立第二个最终建筑类型**：与仪式重写的决定冲突，会让所有按最终建筑名查找的触发器和效果翻倍。

## 5. 工作量估计

loader/schema 字段；生成器输出决议、变量读取和显示切换；一张新图片；转化后的 3 组仪式文本（中英）；`on_religion_changed` 的撤销钩子；验证。工作量约为一个中等 WP。

## 6. 本次采用的决策

| ID | 问题 | 建议 |
| --- | --- | --- |
| D1 | 只做圣索菲亚，还是 v1 就做通用字段并加入阿尔罕布拉等 | 做通用字段，v1 只填圣索菲亚 |
| D2 | 宗教条件：仅逊尼派，还是整个穆斯林宗教组 | 与原版一致：所有者属于穆斯林宗教组，且君士坦丁堡的主体宗教属于穆斯林宗教组 |
| D3 | 代价 | 使用原版 `change_gold_effect = { scale = -1.2 }`，决议额外校验足够国库；不增加草案中尚未定值的人口满意度或稳定度惩罚 |
| D4 | 已完成的仪式在转化时如何处理 | 撤销为朴素，转化后通过现有决议以新文本重新仪式化；效果仍继承同一通用工程 |
| D5 | 原版事件 `mysticism_vs_jurisprudence.21` 是否保留 | 保留，作为 AI 和随机路径，它与决议共用变量，互相排斥 |
| D6 | 转化是否附带一次性奖励（原版有威望和教士满意度） | 发放与原版相同的威望、教士满意度和律法方向社会价值移动；决议与原版事件的选项均重查状态，防止旧窗口重复付费和领奖 |
| D7 | 是否允许主动逆转（基督徒决议改回教堂） | 不提供决议，只依赖原版的自动复原 |

## 7. 实现与验收记录

- 数据唯一来源为 `data/unique_wonders.yaml.identity_variants`。仍只有 191 个工程与每工程一个最终建筑，君士坦丁堡仍为三座独特工程。
- 新增的生成器、四个输出和图片均已登记；编辑器的 unique 数据保存会重建身份脚本、地点面板及 M&T/SoL 兼容输出。本地化折叠会恢复原始教堂文本，不把动态显示表达式写回作者数据。
- 清真寺插画使用内置 `image_gen.imagegen`，参考原有插画编辑；PNG、完整/裁剪 DDS 和提示词/来源记录均保存在工作区。
- 专项 13 项测试通过，覆盖 schema 拒绝不完整数据、等级保留、条件和旧确认重查、原版事件效果保留、恢复清理、双语文本往返及图片资源。相关回归共 352 项测试与 43 项子测试通过（含独立重生成的逐字节比对）；仅有现有 Starlette/httpx 弃用警告。教堂与清真寺样例均可离线严格渲染。
- `scripts/validate.py --changed --fix --ai-report` 已通过。完整重建后的 `audit_wonder_rituals.py` 与 `test_wonder_mechanics_rules.py` 被已有的重复 `tv_engineering_department.21` 阻挡（同一个 `tv_engineering_department_events.txt` 中两份定义，HEAD 中亦存在）；未绕过或抑制该诊断。
- 尚未验收：游戏内实际扣款、原版随机事件与决议竞态、基督教易主/改宗复原、城市外观、保存载入和多人游戏。
