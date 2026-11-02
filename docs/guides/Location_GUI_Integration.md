# 地点窗口控件接入

Great Projects 的控件由 `scripts_engineering_department/in_game/gui/gen_location_window.py`
生成到 `src/in_game/gui/tv_location_wonder_widgets.gui`。其他 Mod 只引用下面的接口，
不复制类型定义、tooltip、本地化或素材，也不需要读取 GP 开发仓库来构建。
GP 启用时，由其独立 GUI 文件提供定义，与最终生效的 `location_window.gui` 属于哪个 Mod 无关。

## 接入奇观按钮和侧栏

在地点窗口的城市场景 `widget` 内、布局 `vbox` 外加入：

```text
tv_location_wonders_button = {}
```

按钮已有右上角定位、尺寸、可见条件、地点上下文与点击行为。
不要把它放入 `hbox` / `vbox`，否则其锚点不再适用。

在 `lateralview` 根节点内，与 `widgetid = "location_window"` 同级加入：

```text
tv_location_wonders_panel = {}
```

侧栏必须是根窗口的直接子控件；放进城市场景会破坏悬浮命中。
默认向窗口右侧展开，顶部偏移为 163 原生 GUI 单位，与原版城市场景对齐。
不同布局可以在实例中覆盖 `position`；不要额外包一层容器。
两个控件需要活动的 `LocationView`，不能直接用于其他类型的窗口。

每个打开建造队列的 `action_tooltip` 中，在原有 `on_action` 前加入公共模板：

```text
action_tooltip = {
    # 原有 click_type / click_mode / title 等属性保持不变。
    using = tv_location_wonders_close_on_queue
    on_action = "[LocationView.OpenConstructionQueue('(int32)3', PdxGuiWidget.Self)]"
}
```

保留该按钮原有的队列编号和参数；上面的 `3` 仅示意。
模板关闭奇观侧栏，随后原动作打开队列。奇观按钮自身负责在打开时关闭建造队列。
单纯加入两个控件可以显示界面，但要保留双向互斥行为还需要这个模板。
不要把模板挂在窗口根部或普通控件上；它只为原有动作块提供 `on_action`。

## 引用 SOL

GP 主窗口及 M&T、SOL 兼容窗口均引用 SOL 提供的公开类型：

```text
sol_location_living_standard_button = {}
```

它位于人口统计行、满意度按钮之后的 `expand = {}` 前，继承该处的 `Location`。
SOL 自己维护按钮与 `StandardofLiving_tooltip`，GP 不提供同名空类型或复制它的实现。
SOL 的类型来源为 `SOL_location_widgets.gui`，经用户授权核对本地 SOL 源码（2026-10-30）。
生成器只保存约定的类型名和插入点，不增加跨仓库文件依赖或 SOL 元数据强制依赖。

## 加载与验证边界

GUI 仍按整个相对路径覆盖。最终生效的窗口必须包含双方引用；
若 SOL 窗口尚未接入 GP 控件，联用时需让 GP 窗口生效。
主窗口和 SOL 兼容窗口共用 `.eu5-base/reference_mods/3601047146` 中的 Glorp 1.4
底板（`30.10.26`），通过同一生成函数加入双方控件和六个队列关闭钩子。
Glorp 拆出的 `gui/vanilla/cmfg_location_window_vanilla_types.gui` 配套类型也合入
最终窗口文件；因此无需额外启用 Glorp，M&T 覆盖窗口时也不会留下竞争的类型文件。
不再套用旧版 Glorp 的 1.3→1.4 补丁；Glorp 的收入显示、地图模式悬浮和 CM
接入随当前底板保留。M&T 兼容窗口直接使用 `.eu5-base/reference_mods/3735059838`
中的 0.2.12/1.4 位置窗口，保留其 owner-flag 中心槽及新版布局后再注入共享控件；
奇观内容仍统一来自 GP 独立文件。

未启用控件提供方时，采用原版 GUI 的同一种缺失类型机制，预计记录缺失定义错误并省略控件。
本次静态解析与离线渲染不能确认原生加载器的报错次数、缺失控件间距或鼠标命中行为。
实机应检查 GP 单独启用、GP + SOL，以及由对方窗口承载 GP 的组合；
检查按钮、各类 hover、队列互斥、无奇观地点及窗口开关。

修改控件生成器后，重新生成主窗口和两个兼容窗口，并运行
`scripts/validate.py --changed --fix --ai-report`、`tests/test_location_widgets.py`、
`tests/test_location_site_conditions.py` 和 `ai_gui_assessment/tests/test_location.py`。
