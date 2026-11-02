# 建设完成后的摘要区

建设阶段结束后，建设卡不再折叠成一条可展开 / 收起的文字按钮。卡内原位置改为两行核心信息，
没有展开入口：建设详情只在建设阶段存在。

## 结构

`src/in_game/gui/panels/organization/tv_engineering_department.gui` 建设卡的
`common_bottom_content` 现在只有两个互斥分支：

```gui
widget = { visible = "[Not(<construction_complete>)]" … }   # 建设阶段的四部件 / 进度 / 宣布完工
widget = { name = "tv_wonder_construction_summary"          # 完成后的两行摘要
           visible = "[<construction_complete>]" … }
```

重建前这两个状态和折叠按钮挤在同一个 `hbox` 里：按钮 462 + 详情 470，展开时整卡内容宽 966，
而卡框声明 500，必然溢出。现在两个分支各自占一整行，摘要 470×60，整卡 500×130。

## 内容

底板 `bg_text_mask_container_dark_blue`，两行：

| 位置 | 内容 |
| --- | --- |
| 左 44×44 | `tv_wonder_level_1..6.dds` 等级徽章，白字罗马数字 |
| 上排 | 工程名，`SelectGameConcept('tv_wonder_display_<id>')`，与原提案预览同一路由 |
| 下排 | 六格等级刻条（`color_gold_texture` 已达 / `color_black_texture` 未达），规模徽章 `tv_project_size_*`，地点名 `tv_wonder_site.GetLocation.GetName` |

刻条把「等级 N / 6」变成可读进度，取代了原来用 462 像素只说「等级 1」的文字按钮。
徽章悬停沿用 `TV_ENGINEERING_WONDER_LEVEL_LABEL`。

## 退役

`TV_ENGINEERING_CONSTRUCTION_FOLD` 与视图变量 `tv_wonder_construction_details_open` 一并移除：
`data/wonder_localization.yaml` 删除该键，11 种语言随之重新生成；
`data/localization_grades.json` 用 `scripts/localization_grades.py prune` 清理；
`scripts/gen_index.py` 重建 `data/index/loc_keys_en.txt`。
`ai_gui_assessment/engineering.py` 不再为这个视图变量提供模拟值，
`ai_gui_assessment/tests/test_engineering.py` 改为断言摘要存在且折叠键消失。

## 验证边界

离线渲染（`ai_gui_assessment/engineering.py --state construction-complete / ceremony-ready /
ritual-progress`）确认：建设阶段图像与改动前逐像素一致，完成后各状态 unknown = 0、
缺失纹理 = 0、缺失本地化 = 0。刻条与底板在实机中的合成顺序、工具提示仍需进游戏确认。
