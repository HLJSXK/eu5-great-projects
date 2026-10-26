# 仪式区新界面：三套设计稿

对应 [实施方案](../../../docs/design/Wonder_Ritual_Rework_Implementation_Plan.md) §13 和 [决策清单](../../../docs/design/Wonder_Ritual_Rework_Decisions.md) F 节。每套方案都渲染了两个状态：**选择阶段**（建成后进入仪式阶段、尚未确认）和**仪式进行中**（A 的进行中状态同时演示了重新仪式化模式）。

| 对比图 | 文件 |
|---|---|
| 选择阶段，三套并排 | [renders/compare_select.png](renders/compare_select.png) |
| 仪式进行中，三套并排 | [renders/compare_progress.png](renders/compare_progress.png) |
| 单张 | `renders/ritual_{a,b,c}_{select,progress}.png` |

示例数据：里耶卡的大港口（great_port，small，市民），风格 1 被选中。价值观方向、阶层偏好、费用，以及“当前 −12”这类数值都是虚构的，只用来展示布局，不代表内容评审结论。渲染时使用真实的工程部面板，只替换了“仪式”卡的内部；顶部的工程师区与页签也是真实面板。

## 效果区的统一规则（三套方案共用）

效果区一律调用原生效果渲染：`text_multi` 的 `raw_text = "[ShowScriptedEffectForScope('<效果>',InternationalOrganizationsView.GetPlayer.MakeScope.Self)]"`。这与辩论面板现有的接收方式相同。不手写效果文本，也不另写只用于 tooltip 的包装效果（共享知识库规则 `gui_effect_preview_replaced_with_manual_text`）。被渲染的就是仪式完成时实际执行的效果，所以预览和结算一定一致：

| 效果 | 作用域 | 内容 | 使用者 |
|---|---|---|---|
| `tv_wonder_ritual_apply_style_<n>_effect`（n = 1/2/3） | 国家 | 按 `tv_wonder_locked` 分支，执行该奇观风格 n 的 grant（经由 `var:tv_wonder_site`）与 settle | 仪式完成时按所选风格调用；A 的卡片按钮 tooltip |
| `tv_wonder_ritual_apply_choice_effect` | 国家 | 按 `tv_wonder_ritual_choice` 分支，调用上一行的对应效果；模式 3 时再加 `add_prestige = 10` | `tv_wonder_ritual_complete_effect`；A/B/C 的效果区 |

引擎会自动写出：合并国家 modifier（显示“持续至游戏结束”，并展开海上贸易效率、每月价值观倾向 +0.1 等内容）、地点 modifier、`change_societal_value` +20（自带“当前偏移”），以及即时奖励。

阶层满意度在“举行仪式”时结算（D17），不属于完成效果，所以不出现在效果区。它由“举行仪式”按钮（generic action `tv_wonder_ritual_confirm`）的原生动作 tooltip 显示，与费用并列。离线渲染不包括悬停，图中看不到这个 tooltip。阶层区标题注明“举行仪式时结算”，进行中状态的说明文字改为“阶层满意度已在举行时结算”。

grant 中写 map 和排队 100 年计时器的部分必须放进 `hidden_effect`，否则会出现在预览里。

因此，效果区以外不再重复写效果数值：价值观轴只画位置和方向，不再手写推力数值；阶层格子只标“支持 / 反对”和原因，不写百分比；C 的三个载体徽章只表示亮或灭。

离线渲染器不执行脚本。`ShowScriptedEffectForScope` 的返回值由 `draft_loc_simp_chinese.yml` 中的 `RR_SAMPLE_ENGINE_FX_<n>` 代替，措辞仿照原版 `effects_l_simp_chinese.yml` 的模板。渲染器会去掉行首缩进，所以 modifier 展开行没有缩进；游戏内会缩进。这个接收方式仍需在游戏内截图确认。

## A · 三联卡

三种风格做成三张等宽卡片并排，每张自上而下是：名称、价值观图标与方向、奖励类型、4 个阶层的支持/反对标记、选择按钮。选中的卡顶部有金边并加上暖色底。卡片下方是整宽的“所选风格的效果”区（原生渲染），再往下是朴素横幅和确认行（费用、时长、“举行仪式”）。每张卡的按钮 tooltip 是该风格的原生效果。进行中时，另外两张卡变暗，按钮换成“已锁定”，确认行换成进度条。

- 优点：价值观方向和阶层立场一眼就能横向比较，最接近 `Original_Design.md` 中“三个互斥风格按钮”的设想；操作只有“点卡片 → 举行”两步。
- 缺点：150 像素的卡片放不下原生效果文本，所以卡片里只剩类型标签；要比较具体奖励，只能悬停按钮或逐个点选。阶层只能用图标加勾叉表示，看不出“为什么”（随机 / 地点建筑）。
- 实现：整宽效果区读 `apply_choice`，按钮 tooltip 读 `apply_style_<n>`；不需要摘要文本。

## B · 卷宗

上方是四行可选列表：三种风格各一行（价值观图标、名称、“→方向 · 奖励类型”、支持/反对计数），朴素是第四行，颜色较暗。选中某一行后，下方展开详情页，依次为：名称与风味文字、效果清单（原生渲染 `apply_choice`）、价值观轴（两端图标、当前位置、推力方向）、四个阶层格子（支持/反对，以及“随机”“想要：舰队检阅”这类原因）。底部是确认行。进行中时，列表锁定在已选的那一行，其余变暗，朴素行隐藏，底部换成进度条。

- 优点：信息最完整，阶层的原因、价值观的当前位置都能看到；详情区高度随内容变化，以后无论奖励怎么组合都放得下；朴素与三种风格处在同一层级，选择关系最清楚。
- 缺点：比较不同风格需要逐行点开；整张卡最长（选择阶段约 1000 像素），在小分辨率下需要滚动。
- 实现：只需要一个详情区，按 `tv_wonder_ritual_choice` 显示；效果清单只有一处原生调用；列表行只用到显示变量。三套方案里它的生成器工作量最小。

## C · 罗盘

顶部是奇观主图条，包括主图、名称、地点与等级，以及状态徽记（空壳 · 仪式阶段 / 仪式进行中 · 10/24），并说明“反对者已经闭嘴”。下面是四个页签（三种风格 + 朴素）。每个页签的主体以**价值观轴**开头，用大图标和刻度显示当前位置与推力方向，接着是“仪式加成”的三个载体徽章（国家 / 地点 / 即时，有内容的点亮，没有的变暗，不写数值），然后是效果清单（原生渲染 `apply_choice`），最后是阶层反应（大图标，配合升降箭头和支持/反对）。底部是确认行或进度条。

- 优点：视觉层次最强，把价值观这一新机制放在首位；三个载体徽章与 R2 的三类奖励直接对应，以后同一风格带多类奖励时，只需点亮多个徽章；奇观主图让仪式阶段更有分量。
- 缺点：比较风格需要切换页签；主图条与面板顶部的工程师区域在视觉上有些重复；徽章与效果清单表达的是同一件事，略显重复。
- 实现：页签按钮沿用现有的 `button_regular_diamond` 与绿色选中态；主图使用现有概念 `tv_wonder_display_full_image_<id>`；徽章需要按“该风格是否带某类奖励”显示的生成变量。

## 推荐

**推荐 B**。理由是 R2 明确要求生成器以后允许任意的奖励组合，而原生效果文本长度不定，B 的详情区宽度足够、高度可变，放原生效果不用截断；同时它能把 R9 的阶层原因和 R3 的价值观当前位置都完整展示出来。如果想要更强的视觉表现，可以把 C 的价值观轴和载体徽章移植进 B 的详情页（这些都是独立的部件）。

## 重新渲染

Windows（需要已安装游戏，默认使用 Steam 路径）：

```powershell
C:\Users\Hades\anaconda3\envs\eu5\python.exe ai_gui_assessment\ritual_rework_mockups.py
C:\Users\Hades\anaconda3\envs\eu5\python.exe ai_gui_assessment\mockups\ritual_rework\stitch.py ai_gui_assessment\mockups\ritual_rework\renders ai_gui_assessment\images\engineering\ritual_rework\ritual_a_select.png
```

`ritual_rework_mockups.py` 的参数与 `priority_proposal_mockups.py` 相同，另外支持 `--renderer-root`、`--game-root`、`--output-root`，可以只渲染部分方案（例如 `a_select b_select`）。`stitch.py` 把面板顶部和仪式卡拼接成单张图；`compare.py <字体路径>` 生成并排对比图。

渲染结果：6 个状态均为 unknown = 0、unresolved = 0、缺失纹理 = 0、缺失本地化 = 0。离线渲染不包括悬停、动画和真实滚动，不能据此断言与游戏内逐像素一致。

## 文件

| 文件 | 内容 |
|---|---|
| `scheme_a_triptych.gui` / `_progress.gui` | 方案 A |
| `scheme_b_ledger.gui` / `_progress.gui` | 方案 B |
| `scheme_c_compass.gui` / `_progress.gui` | 方案 C |
| `draft_loc_simp_chinese.yml` | 草稿文本（`RR_*`）；`RR_SAMPLE_ENGINE_FX_<n>` 是原生效果输出的替身；并覆写了面板顶部的 `TV_ENGINEERING_HEADER_GUIDANCE_CEREMONY` |
| `stitch.py`、`compare.py` | 后处理 |
| `renders/` | 渲染结果 |
