# 工程条目设计样稿

2026-10-30，用户已批准并接入正式界面。此目录保留独立离线原型，不作为正式生成入口。
正式实现见 `scripts_engineering_department/europedia_catalogue.py`，实际界面预览入口为
`ai_gui_assessment/europedia.py`。主模组与 Prosper or Perish 兼容版已同步。
初稿生成托普卡帕宫和凯旋轴线两个完整条目样例，代表独特工程与通用工程的共用版式；
页签旁的 139 / 56 是当前数据的总数，不表示已实现全部条目。

初稿结构（已由下方最新紧凑版替代）：

- 上部为工程名称、完整原画、规模/分类/阶层与建造条件。
- 中部逐列展示 I—VI 级总效果，区分全国和所在地。
- 下部同时展示三种仪式名称、国家/所在地的持续效果和一次性奖励。
- 不重复长篇通用机制说明；原画保留完整比例。

## 紧凑版（2026-10-30 审版调整）

最新预览为 `compact_unique.png` 和 `compact_generic.png`。每条 300 像素高，
1530×1080 画布完整显示三个条目；保留名称、原画、六级效果和三种仪式的全部效果。
最新审版已移除全部建造条件。独特奇观在原画下方显示原版“地点”图标和原生链接色的地点引用；
通用奇观不生成这一行。最左原画仍按原比例放进 240×160 范围。
等级表恢复为原画右侧的全宽 1152 像素，与下方三种仪式的整体边界对齐，单条仍为 300 像素高。

地点名称在离线生成时固定，引用目标使用数据中的固定地点 ID。
原型仅在点击时执行 `SelectLocation(GetLocationByKey('<id>'))`，不在加载或显示时读取地点对象，
不调用 `ShowLocationName`。图标来自原版 `font_icons.gui` 的 `location` 注册。
离线预览验证图标、引用样式和静态布局，不执行或验证游戏内点击跳转。
删去重复的流程说明与大段留白，正文主要为 14—15 号，范围标签更小。

独特样例为托普卡帕宫、法罗斯灯塔、圣索菲亚大教堂；通用样例为凯旋轴线、大灯塔、万国宫城。
原画有不同比例时等比放进固定范围。圣索菲亚采用原始身份的静态名称与仪式名，
不引用会判断游戏变量的动态本地化。

```powershell
& 'C:/Users/Hades/anaconda3/envs/eu5/python.exe' ai_gui_assessment/mockups/europedia_entries/compact.py
```

本轮仍是六个条目的布局样例，不是全量实现。正式推广时，少数有四条基础效果的
条目应按内容适当增高，不通过缩小正文或省略效果硬塞入 300 像素。全量数据中当前最多
四条基础效果、每个仪式最多三条效果；这项计数仅用于审版，不创建正式卡片。

## 静态内容约束（2026-10-30 用户确认）

正式条目必须硬编码全部展示内容。名称、固定地点名、I—VI 级效果、三种仪式名称与效果
在离线生成时写成静态本地化和 GUI，原画写入固定纹理路径。可以由生成脚本读取数据后
固化结果；游戏加载和显示时不得再查询或计算这些内容。数据变更后需重新生成。

禁止用 `ShowModifierEffect`、`ShowScriptedEffectForScope`、
`ShowTriggerConditionsForScope`、动态 `textcontext`，或同类实时游戏数据接口来拼装条目。
不展示建造条件，也不根据当前国家或地点实时求值、标记通过/失败。
页签切换和固定地点引用的点击操作不承担内容计算。

用户报告实时接口会使加载期负载过重并卡死，因此不将其作为正式实现的备选方案。
本样稿已采用静态文字与纹理；这项约束不改变当前视觉稿。

运行：

```powershell
& 'C:/Users/Hades/anaconda3/envs/eu5/python.exe' ai_gui_assessment/mockups/europedia_entries/render.py
```

`unique.png` 和 `generic.png` 是整页；细节图从同一次渲染的实际元素边界裁出。
GUI、独立本地化、数据快照、元素树和诊断均留在本目录。

名称与仪式名来自当前本地化；原画使用 `src/main_menu/gfx/interface/icons/towards_victory/wonders/`
中的完整 DDS；基础效果与仪式奖励读取 `load_all_wonder_mechanics_data()`、
`wonder_base_country_modifiers()`、`authored_final_building_local_modifiers()` 和 `ritual_styles()`。
数值格式来自当前 modifier 索引。建造条件是这两个样例当前选址脚本的审阅文本，
其中托普卡帕宫要求君士坦丁堡为本国首都。

这是当前数据的静态示例，不执行触发器、原生效果或存档判定；所有条件均中性显示。
正式目录现已接入全部 195 种工程；仍不使用引擎效果预览。此处的 PNG 保留审版过程，
当前正式结果以 `ai_gui_assessment/images/europedia/` 为准。
