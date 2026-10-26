> 2026-10-23 仪式重写：每种奇观只有一个 `final_building`，通用升级接口不再接受 `style`。外部新建为朴素；已有仪式在仍有成品等级时保留，最后一级拆除走统一 revoke。

# 伟大工程外部升降级接口（ED）

> 状态：接口、生命周期、本地化已实现（2026-10-21）；易主劫掠已接入（2026-10-22）。
> 以下两个功能必须通过本接口改等级，不得自行写 `change_building_level_in_location`
> / `construct_building` 到最终建筑：
>
> 1. 原生奇观建设事件（原本给艺术品或建一座建筑）改为“当地对应伟大工程 +1 级”。
> 2. 地点易主时的掠夺：逐座工程询问新主，选择劫掠的工程 -1 级。

## 1. 公开接口

| 接口 | 作用域 | 参数 | 说明 |
| --- | --- | --- | --- |
| `tv_wonder_raise_generic_level_effect` | 地点 | `wonder = <wonders.yaml key>` `-3` | 通用奇观 +1 级；0 级时按 `style` 新建 1 级 |
| `tv_wonder_lower_generic_level_effect` | 地点 | `wonder = <key>` | 通用奇观 -1 级；1 级时拆除 |
| `tv_wonder_raise_unique_level_effect` | 任意 | `wonder = <unique_wonders.yaml key>` | 独特奇观 +1 级；总在其固定地点生效；0 级时新建 1 级 |
| `tv_wonder_lower_unique_level_effect` | 任意 | `wonder = <unique key>` | 独特奇观 -1 级；1 级时拆除 |

```pdx
# 原生事件选项示例（独特接口无需先切换到地点）
tv_wonder_raise_unique_level_effect = { wonder = unique_hagia_sophia }

# 地点作用域示例
scope:plundered_location = {
	tv_wonder_lower_generic_level_effect = { wonder = great_port }
}
```

- 公开接口只做名字替换：`tv_wonder_$wonder$_raise_generic_level_style_$style$_effect` 等。
  所以每个分支都是字面量，可在事件选项悬停中正确预览；传错 key（例如把独特奇观 key
  传给通用接口）会在加载期报未知 effect，而不是静默失败。
- 每次调用只变动一级。等级变化是引擎排队任务，同一天内重复调用读到的是变化前等级；
  需要多级时请跨日调用。
- 生成器：`scripts_engineering_department/in_game/common/scripted_effects/gen_tv_wonder_level_change_effects.py`
  → `src/in_game/common/scripted_effects/tv_wonder_level_change_effects.txt`。
  名字模式统一在 `wonder_mechanics/_core.py` 的 `EXTERNAL_*` 常量中。

## 2. 边界规则（已与用户确认）

| 情形 | 升级 | 降级 |
| --- | --- | --- |
| 地点无主 | 无效果（`TV_WONDER_LEVEL_RAISE_UNOWNED_TT`） | 照常 |
| 该奇观不存在（0 级） | 通用：按 `style` 新建；独特：新建唯一样式 | 无效果（`TV_WONDER_LEVEL_LOWER_ABSENT_TT`） |
| 已存在 | 在已有样式上 +1；已落成奇观的仪式样式不会改变，`style` 被忽略 | -1 |
| 1 级降级 | — | 拆除，走完整“失去奇观”生命周期 |
| 6 级或达到适性上限 | 无效果（`TV_WONDER_LEVEL_RAISE_CAPPED_TT`） | — |
| 所有者工程部正在本地建造/扩建同一奇观（阶段 ≥3 且未落成） | 项目等级 +1（见第 3 节） | 照常降最终建筑；落成时按项目目标等级补齐 |

- 适性上限：若该地点已记录该奇观的勘测规模等级 `tv_wonder_survey_scale_tier`，不得超过它；
  未勘测时只受建筑 6 级上限约束；人类玩家开启“无限规模”时与工程部扩建一致地忽略规模等级。
  判定在 `tv_wonder_location_scale_allows_level_trigger`。
- 外部升级不发放任何“奇观落成”奖励（全国/本地欢庆、繁荣、威望、仪式效果），奖励由调用方
  自行决定。外部新建的独特奇观不视为已完成仪式。
- 外部改等级绕过最终建筑的 `can_destroy`（那只拦截玩家手动拆除）。

## 3. 活跃项目冲突：项目等级 +1

当 `tv_wonder_location_has_active_project_for_trigger = { wonder_id = N }` 成立：

1. 悬停/选项阶段：`tv_wonder_request_external_project_level_raise_effect` 只读持久的项目状态，
   显示“立即完成第 N 级全部部件，随后停在仪式阶段”，并记一个待处理标记，触发
   `tv_engineering_department.207`。同日重复请求合并为一次。
   若项目已达自身规模上限：无效果（`TV_WONDER_LEVEL_RAISE_PROJECT_CAPPED_TT`）。
2. 事件 207 的 `immediate` 执行 `tv_wonder_apply_external_project_level_raise_effect`
   （重型的模块/辅助建筑重建不进入任何悬停链）：
   - 重新确认项目仍有效且未达上限；
   - 四个部件都补到“当前等级 +1”，刷新等级、辅助建筑与剩余模块；
   - 建设阶段：结束建设，`tv_wonder_finish_construction_effect` 进入仪式阶段；
   - 已在仪式阶段：仪式改为落成新等级，并刷新已缓存的落成预览。
3. 事件 207 向玩家明确说明进度变化原因；仪式永远不会被自动完成，玩家只失去“继续自动建造
   更高等级”的流程，需手动完成仪式。若请求到达时项目已变化，事件说明“无变化”。

## 4. 生命周期

```text
外部改等级 (custom_description 可见)
  ├─ change_building_level_in_location / construct_building（排队任务）
  └─ hidden: 次日
       ├─ tv_engineering_department.<9400+id>   → tv_wonder_<key>_handle_final_building_level_changed_effect
       │     同步地点等级表、苏伊士运河关闭、扩建候选重登记、
       │     若该奇观已无最终建筑则移除仪式国家修正/独特仪式完成记录、
       │     刷新所有者国家自动修正表、刷新地点显示
       └─ （仅升级）tv_wonder_trigger_final_building_completion_sync_hidden_event_effect
             与真实建造完成相同的完成同步
```

- `..._handle_final_building_level_changed_effect`（原名 `..._handle_final_building_destroyed_effect`）
  现在是原生拆除、外部降级、外部升级共用的唯一次日重同步入口。
- 原生 `on_destroyed` 若同样触发，会重复调度同一个幂等事件，无害。

## 5. 本地化

- `custom_description` 文本在 `effect_localization/tv_engineering_department_effects.txt` 注册：
  `tv_wonder_level_founded_text`、`tv_wonder_level_raised_to_2..6_text`、
  `tv_wonder_level_lowered_to_1..5_text`、`tv_wonder_level_destroyed_text`、
  `tv_wonder_level_raised_project_text`。主体为地点（`[LOCATION.GetName]`），`value` 为最终建筑类型
  （`[BUILDING_TYPE.GetName]`，与原版 `unlock_building_effect` 同法）；项目文本 `value` 为目标等级。
- EN/简中显示文本与事件 207 在 `tv_engineering_department_l_{english,simp_chinese}.yml` 末尾。

## 6. 已知限制

- 请求路径先写一个待处理标记再排队事件；标记写入放在 `hidden_effect` 内，避免悬停预览就排队。
  若请求到达时项目已变化，事件 207 会显示“无变化”分支。
- 项目路径不发放国内支持度，也不改变最近一次“自动完成”相关记录；仪式必须手动完成。
- 事件 207 的 `immediate` 会重建辅助/模块建筑，因此它只在真实执行时运行，不要在可见选项里重复调用。

## 7. 后续接入提示

- 原生奇观事件接入已实施，见 [ED_Vanilla_Wonder_Takeover_Handoff.md](../technical/ED_Vanilla_Wonder_Takeover_Handoff.md)。

- 原生奇观事件：在事件选项里用本接口替换 `create_art` / `construct_building`；接口自带可见提示，
  不要再加手写说明。需要另行决定的只有“原生事件 → 奇观 key”的映射。
- 掠夺已通过 `tv_wonder_ownership_location_changed_owner` 接入 `on_location_changed_owner`：
  新主对每座实际等级 ≥1 的工程分别选择保留或劫掠，劫掠调用一次对应降级接口。
  原主的仪式收益清理在易主时执行，选择后另行发送结果通知。
  见 [ED 易主实现与验收](../technical/ED_Wonder_Ownership.md)。
