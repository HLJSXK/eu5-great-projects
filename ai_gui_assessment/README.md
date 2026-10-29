# ED 模块离线 GUI 预览

## 组织与物流设计预览

运行 `C:\Users\Hades\anaconda3\envs\eu5\python.exe ai_gui_assessment/org_logistics_mockups.py --strict`，
生成 `ai_gui_assessment/images/org_logistics/` 下的 `active.png`、`locked.png`、`full.png`，
以及原生 GUI 源、元素树、诊断和 `index.json`。`--state active|locked|full` 选择单个状态，
`--scale 1.5` 导出更大图片；也支持 `--fixture`、`--output-root`、`--game-root` 和
`--renderer-root`。严格模式遇到任意共享渲染诊断返回非零退出码。

构图对照 `docs/design/Org_Logistics_Panel_Design.html`：组织读数与带上限标记的营地条、
三格就业/有效等级/月进度、两张维护价格卡、后勤乘数条、八行原料→工艺节点、
建材市场/进口建议/工具→劳工营、四格月进度结算。满配和未勘测状态独立输出。
标题、面板、按钮、进度条、字体和物资图标使用游戏/模组资源；原料状态按供给/需求
分为充足（≥1）、紧张（≥0.7）和短缺，工艺取最缺原料的状态。原料节点的 GUI tooltip
保留每单位工艺投入量。只有连接线用 Python 预烘焙为透明纹理，再由共享渲染器合成。
组织、物流、结算的详情裁图由 `render_tree(detail_elements=...)` 根据真实布局输出。

八种工艺及营地维护用量读取当前生产方式，物资/工艺名称与基准价读取游戏/模组数据库。
`fixtures/org_logistics.json` 显式保存虚构市场、价格、就业率和设计稿的 20 级上限/每级
1,000 进度假设。这些是设计预览规则，不替代生产脚本。数值统一计算：7×86%=6.02，
本月 6,020×98%×84%≈4,956；建材需求 140、供应 117.6、缺口 22.4；月维护 1,172.5。
修正了 HTML 样例中 6.0/6,000、140/96 与 84% 不相符的问题，但不改动设计稿。
不声称补一座工坊就能填平缺口，诊断只给出补齐供应后的进度增量。

预览保留中文草稿标签，未改写生产 GUI。建设按钮有原生外观和锁定/上限禁用状态，
尚未绑定游戏动作；不执行点击、悬停命中、脚本或市场结算。素材及无缺失诊断不等于
实机像素一致。生成结果和连接线均位于忽略的 images 目录，不提交游戏二进制资源。

## 地点窗口与伟大工程弹出面板

`location.py` 读取当前 `src/in_game/gui/location_window.gui` 的实际窗口，以及伟大工程按钮
挂载的 `contextmenu_widget`，输出地点窗口、点击弹出面板的合成图、独立图片、元素树和诊断。

```powershell
C:\Users\Hades\anaconda3\envs\eu5\python.exe ai_gui_assessment\location.py --state multiple --strict
C:\Users\Hades\anaconda3\envs\eu5\python.exe ai_gui_assessment\location.py --all --strict
```

状态包括 `single`（单奇观）、`multiple`（三奇观）、`empty`（无奇观）、
`overflow`（六奇观，面板显示五项并提示剩余一项）、`unbuilt`（等级零）。
默认输出目录为 `ai_gui_assessment/images/location/`；合成图为 `location_<state>.png`，
独立图为 `*_panel.png` 和 `*_menu.png`，总索引为 `location_index.json`。
`--closed` 预览收起状态，`--selected-slot 3` 预览第三项详情（所选状态须包含该项）。
支持 `--mocks`、`--scale`、`--width`、`--height`、`--language` 和显式路径参数。

地点、经济和队列数据来自 `fixtures/location.json` 中逐条列出的虚构样例；默认选择基础设施页，
次级列表为空，奇观采用朴素落成状态。国家／地点修正读取所选 Mod 当前生成的 static modifiers，
格式来自 modifier 索引；地点条件明确显示为示例，未执行游戏条件或脚本。
3D 地景使用占位区域，旗帜和实机悬停时序不在预览范围内。

弹出内容按实际按钮的挂载定义展开，地点上下文由该类型自身绑定。离线样例提供原生弹出
容器的 `ExtraTooltipInfo` 和选中项目状态，在地点窗右侧放置预览；不执行实际点击、自动定位、
滚动或关闭行为。原生容器将高度限制为 650，详情图片和效果表只展开所选项目。
布局及裁图仍由共享 `preview.render_tree` 处理，不改写生产 GUI 的布局或效果内容。

## 工程部面板

`engineering.py` 使用共享渲染器，直接展开 `src` 中实际的 `organization_panel` 实例及其覆盖块，读取所选游戏安装的字体、纹理和本地化。覆盖工程部的总览、勘测和物流、建造与仪式三个页签，无需启动游戏。

```powershell
C:\Users\Hades\anaconda3\envs\eu5\python.exe ai_gui_assessment\engineering.py --list-states
C:\Users\Hades\anaconda3\envs\eu5\python.exe ai_gui_assessment\engineering.py --state survey
C:\Users\Hades\anaconda3\envs\eu5\python.exe ai_gui_assessment\engineering.py --state ceremony-ready
C:\Users\Hades\anaconda3\envs\eu5\python.exe ai_gui_assessment\engineering.py --state unique-ready
C:\Users\Hades\anaconda3\envs\eu5\python.exe ai_gui_assessment\engineering.py --all --strict
```

圣索菲亚身份转化可用 `--state hagia-church` 和 `--state hagia-mosque` 对照。
加上 `--fixture ai_gui_assessment/fixtures/hagia_overview.json` 可在总览对照名称与图片；
使用默认建设与仪式页签可对照三组仪式文本。两个样例都读取同一座等级 1 的工程，仅切换原版全局变量
`hagia_sophia_now_mosque`；这验证显示路由，不执行转化决议或游戏生命周期。

## 场景

| 页签 | 状态 | 内容 |
| --- | --- | --- |
| `overview` | `no-engineer`、`conception`、`proposal`、`debate`、`support-reserve` | 未任命、构思中、备选方案、辩论、支持度超过 100 |
| `resolutions` | `survey`、`survey-complete` | 勘测进度、地点适宜性、规模/组织/物流能力 |
| `custom` | `construction`、`construction-complete` | 四部分建设单元、当前单元进度、仪式风格选择 |
| `custom` | `ceremony-ready`、`ritual-progress`、`finalized` | 三风格选择、当前数据的效果示例、价值观轴、阶层偏好、24 月进度、奖励已发放状态 |
| `custom` | `unique-ready`、`unique-progress` | 独特奇观的统一仪式选择与进度 |
| `custom` | `reritual-ready`、`reritual-progress` | 重新仪式化，与建设共用三风格及朴素选项 |

每个状态选中对应页签；`--tab` 可覆盖。仪式效果区保留实际完成效果的原生接收方式；离线返回值根据 `ritual_styles()` 的当前数据生成，并明确标注为示例，涵盖国家/地点奖励、即时奖励、价值观移动及重新仪式化的额外威望。数值格式取自 modifier 索引，名称读取所选游戏与 Mod 的本地化，不执行效果脚本。仪式时长、独特奇观身份与地点、阶层固定/随机/地点奖励偏好来源也取自当前数据；不存在的阶层变量为 null，自动隐藏。

## 输出与路径

默认输出至 `ai_gui_assessment/images/engineering/`。每个状态生成 PNG、元素树 `*_tree.txt` 和诊断 `*_report.json`；仪式卡可见时，共享渲染器额外按实际布局边界裁出 `*_ritual.png`，路径记录在报告的 `details.ritual` 字段。`--all` 复用 GUI 数据库及字体/本地化资源，同时生成 `engineering_index.json`。生成结果不纳入版本控制。

`--strict` 在存在未知表达式、未解析上下文、缺失纹理、未转换的 `textcontext`、缺失文本绑定或本地化时返回 1，仍保留 PNG 和完整报告。每次渲染独立记录纹理缺失，避免缓存让后续场景漏报。

`--workspace` 指定工作区，`--mod-root` 指定包含工程部 GUI 的部署根，`--renderer-root` 指定包含 `eu5_gui_renderer` 的共享渲染器目录，`--game-root` 指定游戏安装目录或 `game` 子目录；`--output-root` 指定输出目录，`--output` 指定单图文件名。相对 Mod、输出、fixture 和 mocks 路径以工作区为基准。

可调 `--width`、`--height`、`--scale` 和 `--language`。默认 570×1800，保留真实滚动区域的裁切；较长的效果列表可提高高度以检查底部卡片：

```powershell
C:\Users\Hades\anaconda3\envs\eu5\python.exe ai_gui_assessment\engineering.py --state reritual-progress --height 2600
C:\Users\Hades\anaconda3\envs\eu5\python.exe ai_gui_assessment\engineering.py --state ritual-progress --height 1080 --scale 1.5 --output ritual_1080.png
```

## 自定义场景

`--fixture` 用 JSON 覆盖所选预设，支持 `tab`、`engineer_name`、`player_variables`、`organization_variables`、`objects`、`lists`、`action_availability`。两个变量存储保持独立；数值 0 表示已设置，`null` 表示未设置。对象键为 `变量名.访问器`，对象内容使用原生类型名 `__type__` 及访问器键。

`fixtures/ceremony_style_2.json` 切换到第二种风格，展示地点奖励与阶层支持；`fixtures/ceremony_style_3.json` 切换到第三种风格并禁用“举行仪式”，展示当前统一费用下按钮不可用的状态：

```powershell
C:\Users\Hades\anaconda3\envs\eu5\python.exe ai_gui_assessment\engineering.py --state ceremony-ready --fixture ai_gui_assessment/fixtures/ceremony_style_2.json --strict --output ceremony_style_2.png
C:\Users\Hades\anaconda3\envs\eu5\python.exe ai_gui_assessment\engineering.py --state ceremony-ready --fixture ai_gui_assessment/fixtures/ceremony_style_3.json --strict --output ceremony_style_3.png
```

仪式确认前依次显示三个小节：仪式选项、仪式需求、预期效果；确认按钮单独放在三个小节下方。所选仪式的风味文本放在第一节的朴素选项下方，四个选项共用单行图标与名称布局。需求包含费用和时长，预期效果中的价值观变化仅由原生 effect 渲染，不再绘制额外的价值观轴、进度条或方向箭头。三个仪式选项采用单行卡片，只显示图标与仪式名；每张卡片下方按偏好排列带绿色勾标的支持阶层图标，最多七个，不再显示底部阶层卡片。普通建设和重新仪式化共用朴素选项；仪式区直接从选项小节开始，不再显示顶部说明与取消按钮。进行中只保留已锁定风格，建设与仪式详情分别可展开。阶层悬停采用原生提示框，标题说明该阶层当前支持此风格，下一行按缓存显示原因。可加 `--hover clergy_estate` 预览指定阶层的实际 tooltip 定义；离线不执行鼠标命中检测。费用区在游戏中直接渲染实际 `tv_wonder_ritual_pay_effect`，离线只注明原生费用样例，不模拟国库与价格修正。朴素选项与进行中展开详情可复现为：

```powershell
C:\Users\Hades\anaconda3\envs\eu5\python.exe ai_gui_assessment\engineering.py --state ceremony-ready --fixture ai_gui_assessment/fixtures/ceremony_plain.json --strict --output ceremony_plain.png
C:\Users\Hades\anaconda3\envs\eu5\python.exe ai_gui_assessment\engineering.py --state ritual-progress --mocks ai_gui_assessment/fixtures/ritual_details_open.json --strict --output ritual_details.png
```

```json
{
  "player_variables": {"tv_wonder_site": 1},
  "objects": {
    "tv_wonder_site.GetLocation": {
      "__type__": "Location",
      "Self": "rijeka",
      "GetName": "里耶卡"
    }
  },
  "action_availability": {"tv_wonder_finish_construction": false}
}
```

优先提案列表可通过 `lists.tv_wonder_priority_unfinished_list` 和 `lists.tv_wonder_priority_expansion_list` 提供，列表项使用实际 GUI 所需的 `Scope` 上下文。更底层的绑定可由 `--mocks` 提供 JSON `[["表达式正则", 值], ...]`，优先于场景默认值；可传入 `RequirementsList`、`StringPairList` 等类型的完整表格数据。

`scenario_state()`、`mocks()`、`build()`、`configure()`、`render()` 是项目内的工程部适配入口。先调用 `configure()`，再从共享包导入 `eu5_gui_renderer.preview.load_resources`；批量渲染时先 `resources = load_resources()`，再传给各次 `render(..., resources=resources)`。每个进程只使用一个游戏/Mod/语言配置。

## 模块边界

| 所在仓库 | 职责 |
| --- | --- |
| `eu5-modding-base` | `config.configure_paths` 配置路径；`preview` 加载资源、渲染 PNG、按 `detail_elements` 的实际布局导出详情图、输出统一元素树/诊断及详情路径、判定严格模式；`fixtures` 校验 mocks JSON、构造变量/对象绑定和原生表格、用调用方索引元数据格式化 modifier 示例、注入指定按钮状态；`gui.build_target` 选择实际根实例 |
| 当前项目 | 选择 ED GUI、三个页签、各生命周期状态、国家/组织变量、仪式及人物/航线样例、动作可用性规则、工程部 fixture 格式、加载当前仪式数据与 modifier 索引、效果示例分支和说明、选择仪式详情元素、批量场景编排 |

通用 `run.py`、本项目 `engineering.py` 和 `priority_proposal_mockups.py` 共用 `preview.render_tree`，项目内不保留第二套资源加载或 PNG/诊断输出实现。缺失本地化在共享求值器/文本处理时记录，支持任意模组的键名，不依赖 `TV_` 前缀。通用回归测试放在共享仓库，用无游戏资源依赖的合成 GUI 验证；工程部实际分支测试留在本项目。

共享实现和规则见 `.eu5-base/docs/guides/EU5_GUI_Modding_Guide.md` 的“Offline scenario samples and detail images”。自选 `--renderer-root` 需提供 `preview.render_tree(detail_elements=...)` 与 `fixtures.modifier_sample_lines()`。

## 模拟边界与验证

状态均为示例数据，不读取存档、不执行脚本、月结或点击动作。勘测要求与仪式奖励显式标注“示例”；勘测条件类型和权重取自机制 1 的初始化定义，仪式奖励取自当前数据，价值观当前位置、当前月份及原生要求表的连线尺寸为样例。结束辩论按钮按支持度 100 模拟，仪式风格按钮按阶段及进行/完成状态模拟；fixture 可指定其他动作是否可用，未指定的动作统一显示可用。预览不包含 3D 人物肖像、程序化旗帜、动画、悬停及原生滚动，不能据此声称与实机像素一致。

```powershell
C:\Users\Hades\anaconda3\envs\eu5\python.exe -m unittest discover -s .eu5-base/ai_gui_assessment/renderer/tests -v
C:\Users\Hades\anaconda3\envs\eu5\python.exe -m unittest discover -s ai_gui_assessment/tests -v
```

工程部 GUI 回归检查需要安装游戏资源；工程部 fixture 格式可独立测试。严格模式、输出文件、重复纹理缺失、原生表格和通用绑定的回归检查由共享仓库负责，可不依赖安装游戏运行。

共享包 `eu5_gui_renderer/textures.py` 需要支持 `modify_texture.visible`：隐藏的纹理修改层不应参与合成或加载纹理。使用其他 `--renderer-root` 时需包含此行为。
