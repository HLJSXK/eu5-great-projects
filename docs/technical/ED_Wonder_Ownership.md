# ED 伟大工程易主

实现日期：2026-10-22。

- 沿用 `on_location_changed_owner` 桥接与逐工程的 8000+id / 9000+id 事件。
  回调要求实际最终建筑等级 ≥1；逐条分派前再次检查实体等级，缓存或未完工部件不会单独触发事件。
- 同一地点的多座工程各自选择：原封不动获得 5 威望；劫掠按工程数据中的 small / medium / large
  获得 2000 / 4000 / 6000 杜卡特，并调用统一外部降级接口降低该工程一级。
  一级工程降至零会拆除；后续缓存、仪式和候选同步由接口负责。
- AI 选项权重为 80 / 20，不依赖 AI 主动代操作开关。
- 原主失去工程对应的仪式收益在易主当时清理，仍拥有同类工程时沿用原有保留规则。
  新主确认后向原主发送保留或劫掠通知；通知本身不修改收益，避免延迟通知误清理收复后的状态。
- 每次符合条件的易主递增地点的 `tv_wonder_ownership_revision`，并保存至事件链。
  选项执行时检查当前所有者、易主序号与该座工程的实际等级。旧事件失效时不发奖励、不降级，
  原主收到状态已变化的通知。无原主时跳过通知；无新主时直接通知原主。
- 施工失地的强制放弃回调与原有执行顺序保留。

生成源：

- `scripts_engineering_department/in_game/events/gen_tv_wonder_ownership_events.py`
- `scripts_engineering_department/in_game/common/scripted_effects/gen_tv_wonder_ownership_effects.py`
- `data/wonder_localization.yaml` 与英／简中 ownership 本地化生成器。

验证：`tests/test_wonder_ownership.py`、`tests/test_engineering_department_ai.py`、
`tests/test_wonder_priority_proposals.py` 共 255 项通过。覆盖全部 192 座工程的奖励、接口、AI 权重与通知，
以及零级、失地、反复易主、无原主等选项执行场景。测试读取生成后的脚本；不模拟引擎的排队降级。
工程规则检查通过（192 座工程、136 座独特工程）；仓库校验通过，无错误及警告。

实机待验收：保留与劫掠各触发一次，检查原主结果通知；分别掠夺一／二级工程并跨日核对状态；
在事件打开期间连续转移地点、再转回同一新主，确认旧事件无法发奖；同地多工程分别选择并核对独立结果。
