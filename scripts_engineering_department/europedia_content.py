"""Hand-authored Europedia card content for Great Projects (English + Simplified Chinese).

One entry per card. Each card renders through in_game/gui/shared/tv_europedia_style.gui;
the layout (which widget a section becomes) is decided here, the prose lives in this file.

A card is a dict:
    id            stable slug, also the localization key prefix (TV_EU_<ID>_*)
    filter        catalog id; a card shows when the tab filter is 'all' or matches this
    icon          texture for the header tab
    title         (en, zh) header and card title
    lead          (en, zh) the one-paragraph summary under the header
    sections      list of section dicts, rendered in order:

        {"kind": "text",    "title": (en, zh), "icon": texture, "body": (en, zh)}
        {"kind": "flow",    "title": ..., "icon": ..., "steps": [step, ...], "sign": (en, zh) | None}
        {"kind": "cycle",   "title": ..., "icon": ..., "note": (en, zh) | None,
                            "steps": [{"icon": texture, "link": raw link, "title": (en, zh),
                                       "text": (en, zh)}, ...]}
        {"kind": "guide",   "title": ..., "icon": ..., "body": (en, zh),
                            "anatomy": one of europedia_render.ANATOMY_PANEL_TITLES,
                            "rows": [{"mock": mock | None, "title": (en, zh), "text": (en, zh)}]}
        {"kind": "scale",   "title": ..., "icon": ..., "steps": [{"medallion": widget_fn, "label": (en, zh)}],
                            "body": (en, zh) | None}
        {"kind": "panels",  "title": ..., "icon": ..., "panels": [panel, panel], "sign": (en, zh)}
        {"kind": "entries", "title": ..., "icon": ..., "body": (en, zh) | None, "entries": [entry, ...]}
        {"kind": "row",     "title": ..., "icon": ..., "label": (en, zh), "items": [item, ...], "body": ...}

    step   {"icon": texture, "link": raw link text, "title": (en, zh), "text": (en, zh)}

    A guide row's "mock" names the panel control it draws and freezes one example state. Every
    label inside a mock is an existing panel key, so no mock text is translated twice:
        None                                   nothing drawn, the note stands alone
        ("status", key)                        the header status strip
        ("portrait", key)                      the empty chief portrait with its prompt
        ("button", key, colour)                one button, colour in regular|green|yellow|red
        ("buttons", [(key, colour), ...])      a stack of buttons
        ("pills", [key, ...], active_key)      the three size labels, one picked
        ("bar", key, value, text[, captions])  a labelled bar frozen at value/100
        ("demands",)                           one demand row per estate and its three answers
        ("triplet",)                           the survey's three competence readings
        ("stats",) / ("stats_goods",)          stat tiles; the input goods table
        ("equation",)                          the monthly settlement sum
        ("parts",)                             the four construction parts with unit pips
        ("stat", label_a, value_a, label_b, value_b_key) two stat tiles, values can be keys
        ("styles", [key, ...])                 the ceremony style picker
    panel  {"title": (en, zh), "text": (en, zh), "items": [item, ...], "arrows": bool}
    entry  {"icons": [widget_fn, ...], "title": (en, zh), "text": (en, zh)}
    item   {"icon": texture, "link": raw link text, "alpha": float | None}

Token strings (the *_icon values and widget_fn callables) are GUI-writer functions defined in the
generator; this module only describes structure and prose, so it stays importable without GUI
helpers. The generator resolves them.

Every number below is taken from the shipped script or data, never invented: conception gain is
the Great Engineer's Administrative skill x 0.2 a month (tv_engineering_department_effects.txt),
survey gain is Military x 0.1, support runs 0-200 with 100 needed to close the debate, the survey
tiers break at 20/40/60/80/100, organization caps the worksite at competence/5 (max 20) and
logistics scales progress to 50-150%, ritual costs are 2/3/5 scaled gold with a 24 month
duration, 0.1 monthly societal pull, 0.1/0.05 estate satisfaction and a 100 year memory, and a repair
round offers one reprieve.
"""

from __future__ import annotations

# --- shared link tokens (raw GUI expressions, identical in both languages) -------------------
LINK_SMALL = "[tv_wonder_small|e]"
LINK_MEDIUM = "[tv_wonder_medium|e]"
LINK_LARGE = "[tv_wonder_large|e]"
LINK_ED = "[tv_engineering_department|e]"
LINK_ENGINEER = "[tv_great_engineer|e]"
LINK_CONCEPT = "[tv_wonder_concept|e]"
LINK_DEBATE = "[tv_wonder_debate|e]"
LINK_SURVEY = "[tv_wonder_survey|e]"
LINK_CONSTRUCTION = "[tv_wonder_construction|e]"
LINK_PART = "[tv_wonder_construction_part|e]"
LINK_CEREMONY = "[tv_wonder_ceremony|e]"
LINK_EXPANSION = "[tv_wonder_expansion|e]"
LINK_GENERIC = "[tv_wonder_generic|e]"
LINK_UNIQUE = "[tv_wonder_unique|e]"
LINK_SUPPORT = "[tv_wonder_domestic_support|e]"
LINK_SCALE = "[tv_wonder_scale_competence|e]"
LINK_ORG = "[tv_wonder_organization_competence|e]"
LINK_LOG = "[tv_wonder_logistics_competence|e]"
LINK_ESTATE = "[ShowEstateTypeName('nobles_estate')]"

# Every texture below is referenced by vanilla GUI, so it ships with the game. Keep it that way:
# an icon that no vanilla .gui mentions may not exist at all and would render blank.
ICON_BOOK = "gfx/interface/icons/flat_icons/tabicons/europedia_flat_icon.dds"
ICON_CROWN = "gfx/interface/icons/flat_icons/hre_parliament.dds"
ICON_BUILD = "gfx/interface/icons/flat_icons/building_panel/build.dds"
ICON_EFFECT = "gfx/interface/icons/flat_icons/action.dds"
ICON_IDEA = "gfx/interface/icons/flat_icons/tabicons/advances.dds"
ICON_GOLD = "gfx/interface/icons/flat_icons/gold.dds"
ICON_MAP = "gfx/interface/icons/flat_icons/tabicons/mapmodes.dds"
ICON_LAW = "gfx/interface/icons/flat_icons/laws.dds"
ICON_PRESTIGE = "gfx/interface/icons/flat_icons/prestige.dds"
ICON_POWER = "gfx/interface/icons/flat_icons/power_projection.dds"
ICON_ESTATE = "gfx/interface/icons/flat_icons/estates/estates.dds"
ICON_POP = "gfx/interface/icons/location_icons/new/population.dds"
ICON_GROWTH = "gfx/interface/icons/location_icons/new/population_growth.dds"
ICON_PROSPERITY = "gfx/interface/icons/location_icons/new/prosperity.dds"
ICON_TRADE = "gfx/interface/icons/flat_icons/trade.dds"
ICON_MILITARY = "gfx/interface/icons/flat_icons/military.dds"
ICON_MARITIME = "gfx/interface/icons/flat_icons/tabicons/production.dds"
ICON_WARNING = "gfx/interface/icons/alerts_icons/unhappy_estates.dds"
ICON_STARVE = "gfx/interface/icons/alerts_icons/starving_provinces.dds"
ICON_LABOR = "gfx/interface/icons/flat_icons/estates_enrichment.dds"
ICON_CULTURE = "gfx/interface/icons/flat_icons/cultural_tradition.dds"
ICON_RELIGION = "gfx/interface/icons/flat_icons/religious_unity.dds"
ICON_DIPLO = "gfx/interface/icons/flat_icons/diplomatic_range.dds"
ICON_ART = "gfx/interface/icons/flat_icons/art_works.dds"
ICON_FORT = "gfx/interface/icons/flat_icons/siege_occupation/siege.dds"
ICON_ED = "gfx/interface/icons/international_organizations/tv_engineering_department.dds"
ICON_CEREMONY = "gfx/interface/icons/flat_icons/hre_parliament.dds"
ICON_LOG = "gfx/interface/icons/flat_icons/tabicons/production.dds"
ICON_GOV = "gfx/interface/icons/flat_icons/tabicons/government.dds"
ICON_ENGINEER = "gfx/interface/icons/flat_icons/tabicons/government.dds"
ICON_SCALE = "gfx/interface/icons/flat_icons/mass_upgrade.dds"
ICON_EXPANSION = "gfx/interface/icons/flat_icons/mass_upgrade.dds"
ICON_KIND_SMALL = "gfx/interface/icons/flat_icons/menu_icon_square.dds"
ICON_KIND_MEDIUM = "gfx/interface/icons/flat_icons/hre_parliament.dds"
ICON_KIND_LARGE = "gfx/interface/icons/flat_icons/power_projection.dds"
ICON_CAPITAL = "gfx/interface/icons/flat_icons/menu_icon_square.dds"
ICON_FOOD = "gfx/interface/icons/flat_icons/trade_market/food_stockpile.dds"

ICON_PART_FOUNDATION = "gfx/interface/icons/towards_victory/wonders/tv_wonder_foundation.dds"
ICON_PART_BODY = "gfx/interface/icons/towards_victory/wonders/tv_wonder_body.dds"
ICON_PART_FUNCTION = "gfx/interface/icons/towards_victory/wonders/tv_wonder_function.dds"
ICON_PART_CROWNING = "gfx/interface/icons/towards_victory/wonders/tv_wonder_decoration.dds"
ICON_COMPLETE = "gfx/interface/icons/towards_victory/wonders/tv_wonder_complete.dds"
ICON_CONSTRUCTION = "gfx/interface/icons/towards_victory/wonders/tv_wonder_construction.dds"

# Social/estate links used inside prose; identical in both languages.
L = {
    "gold": "@gold!",
    "prestige": "@prestige!",
}


def _t(en: str, zh: str) -> tuple[str, str]:
    return (en, zh)


CARDS: list[dict] = [
    # ------------------------------------------------------------------ overview ----
    {
        "id": "overview",
        "filter": "overview",
        "icon": ICON_BOOK,
        "title": _t("Great Projects", "伟大工程"),
        "lead": _t(
            "#F Leave a monument of your own on your city's skyline. Appoint a Great Engineer, "
            "persuade nobles, burghers and clergy, survey your site, and raise your wonder toward "
            "the clouds, brick by brick and stone by stone.#!",
            "#F 在城市的天际线上留下属于你的丰碑吧。任命一位总工程师，说服贵族、市民与教士，勘测选址，"
            "一砖一石把奇观垒向云端。#!",
        ),
        "sections": [
            {
                "kind": "cycle",
                "title": _t("The Whole Project at a Glance", "全流程一览"),
                "icon": ICON_IDEA,
                "note": _t(
                    "Seven steps in order, linked clockwise. The lessons below follow the same order.",
                    "七步依次推进，沿圆环顺时针排列。下面的教程也按这个顺序展开。",
                ),
                "steps": [
                    {
                        "icon": ICON_ENGINEER,
                        "link": LINK_ENGINEER,
                        "title": _t("Appoint", "任命"),
                        "text": _t(
                            "An empty office blocks everything.",
                            "职位空着，什么都别想开始。",
                        ),
                    },
                    {
                        "icon": ICON_IDEA,
                        "link": LINK_CONCEPT,
                        "title": _t("Conceive", "构想"),
                        "text": _t(
                            "The engineer proposes; you accept one of three.",
                            "工程师提案，你从三选一。",
                        ),
                    },
                    {
                        "icon": ICON_ESTATE,
                        "link": LINK_DEBATE,
                        "title": _t("Debate", "辩论"),
                        "text": _t(
                            "The estates name their price. Support must reach 100.",
                            "各阶层开价，支持度要够 100。",
                        ),
                    },
                    {
                        "icon": ICON_MAP,
                        "link": LINK_SURVEY,
                        "title": _t("Survey", "勘测"),
                        "text": _t(
                            "The ground is read: the ceiling on all that follows.",
                            "丈量地基：此后一切的上限。",
                        ),
                    },
                    {
                        "icon": ICON_LABOR,
                        "link": LINK_ORG + " / " + LINK_LOG,
                        "title": _t("Organize", "组织"),
                        "text": _t(
                            "Worksites supply the labour, logistics its pace.",
                            "工地出劳力，物流定快慢。",
                        ),
                    },
                    {
                        "icon": ICON_BUILD,
                        "link": LINK_CONSTRUCTION,
                        "title": _t("Build", "施工"),
                        "text": _t(
                            "One part at a time; the weakest sets the level.",
                            "一次推一个部件，最弱那个定等级。",
                        ),
                    },
                    {
                        "icon": ICON_CROWN,
                        "link": LINK_CEREMONY,
                        "title": _t("Dedicate", "落成"),
                        "text": _t(
                            "A ceremony, or a plain opening. This is its permanent character.",
                            "郑重仪式或朴素启用，此后永久生效。",
                        ),
                    },
                ],
            },
            {
                "kind": "guide",
                "title": _t("Step 1  Appoint a Great Engineer", "第一步 任命大工程师"),
                "anatomy": "appointment",
                "icon": ICON_ENGINEER,
                "body": _t(
                    "Open the [tv_engineering_department|e] panel, click 'Appoint Great Engineer' in the "
                    "header, and choose a [character|e] to serve as [tv_great_engineer|e]. While this office "
                    "is vacant, both [tv_wonder_concept|e] and [tv_wonder_survey|e] stop.",
                    "打开[tv_engineering_department|e]面板，在页眉点击「任命大工程师」，选一位[character|e]"
                    "担任[tv_great_engineer|e]。这个职位空着的时候，[tv_wonder_concept|e]和[tv_wonder_survey|e]都会停下。",
                ),
                # The player's first sight of the panel: an empty portrait slot with a +
                # over it, and the header saying why nothing can start.
                "rows": [
                    {
                        "mock": ("status", "TV_ENGINEERING_HEADER_STATUS_NO_ENGINEER", None),
                        "title": _t("The header says why", "页眉先告诉你卡在哪"),
                        "text": _t(
                            "Until an engineer is appointed, the panel shows this status and the next "
                            "step reads 'Appoint engineer.' Everything else stays locked.",
                            "在任命之前，面板就显示这一状态，下一步提示写着「任命工程师」。其余功能全部锁住。",
                        ),
                    },
                    {
                        "mock": ("portrait", "TV_IO_HEADER_APPOINT_CHIEF_PROMPT", None),
                        "title": _t("The empty portrait is the button", "空头像就是按钮"),
                        "text": _t(
                            "Click the empty portrait in the header. The game offers characters; "
                            "whoever you pick holds the post until you replace or dismiss them.",
                            "点页眉里那个空头像，游戏会让你挑人。选中的角色一直担任此职，直到你换人或免职。",
                        ),
                    },
                    {
                        "mock": ("buttons", [("TV_ENGINEERING_CHANGE_LEADER_SHORT", "yellow"),
                                             ("TV_ENGINEERING_REMOVE_LEADER_SHORT", "red")], None),
                        "title": _t("Changing your mind costs nothing here", "换人和免职都不花钱"),
                        "text": _t(
                            "Once appointed, the same header offers change and remove. Both are free, "
                            "but a project already under way keeps its progress.",
                            "任命之后，页眉会出现「更换」和「免职」两个按钮，都不花钱，但已经开工的工程进度会保留。",
                        ),
                    },
                ],
            },
            {
                "kind": "guide",
                "title": _t("Step 2  Conceive and Accept a Proposal", "第二步 构想并接受提案"),
                "anatomy": "conception",
                "icon": ICON_IDEA,
                "body": _t(
                    "Each month, conception progress increases by 0.2 times the Great Engineer's [adm|e]. "
                    "At 100, three proposals appear. Use 'View First Proposal' and the other proposal buttons "
                    "to read their briefs, then click 'Accept Proposal' to lock in the wonder and its size "
                    "([tv_wonder_small|e], [tv_wonder_medium|e] or [tv_wonder_large|e]). "
                    "If none of the three suits you, either option below gives you a new set.",
                    "每个月构想进度增加大工程师[adm|e]的 0.2 倍，满 100 后会出现三项提案。"
                    "点「查看第一提案」等按钮可以阅读简报，选好后点「接受提案」，就锁定了奇观和它的规模"
                    "（[tv_wonder_small|e]、[tv_wonder_medium|e]或[tv_wonder_large|e]）。三项都不满意的话，可以用以下方式换一组新提案。",
                ),
                "rows": [
                    {
                        "mock": ("bar", "TV_ENGINEERING_CONCEPT_CARD_TITLE", 100, "100 / 100"),
                        "title": _t("The bar is the appointment's pay-off", "这条进度是任命的回报"),
                        "text": _t(
                            "The bar fills only while a [tv_great_engineer|e] holds office, at 0.2 times "
                            "their [adm|e] a month. A better administrator conceives faster; nothing else "
                            "in the game moves it.",
                            "只有[tv_great_engineer|e]在任时这条进度才会走，每月涨其[adm|e]的 0.2 倍。"
                            "行政能力越高构想越快，除此之外没有任何东西能推动它。",
                        ),
                    },
                    {
                        "mock": ("buttons", [("TV_ENGINEERING_PROPOSAL_BUTTON_SKY_DOME", "yellow"),
                                             ("TV_ENGINEERING_PROPOSAL_BUTTON_TOWER_TEMPLE", "yellow"),
                                             ("TV_ENGINEERING_PROPOSAL_BUTTON_STAR_FORTRESS", "yellow")], None),
                        "title": _t("Three proposals, one choice", "三项提案，只能选一项"),
                        "text": _t(
                            "At 100 the bar is replaced by three proposal buttons. Hover one to read its "
                            "levels, effects and size before committing.",
                            "满 100 后进度条会换成三个提案按钮。提交之前先悬停读一读它的等级、效果和规模。",
                        ),
                    },
                    {
                        "mock": ("buttons", [("TV_ENGINEERING_ACCEPT_BUTTON", "green"),
                                             ("TV_ENGINEERING_REFUTE_BUTTON", "red"),
                                             ("TV_ENGINEERING_BRIBE_BUTTON", "yellow")], None),
                        "title": _t("Accept locks it in; the other two only reroll", "接受才锁定，另外两个只是重抽"),
                        "text": _t(
                            "Accept fixes the wonder and its size for the whole project. Refute spends "
                            "10 [prestige|e] and Fund spends a scaled [gold|e] for a fresh set of three.",
                            "「接受」把奇观和规模定死，整局工程都按它来。「驳倒」花 10 [prestige|e]、"
                            "「拨款」花一笔缩放[gold|e]，都是换一组新的三个提案。",
                        ),
                    },
                    {
                        "mock": ("pills", ["TV_ENGINEERING_WONDER_SIZE_SMALL_LABEL",
                                           "TV_ENGINEERING_WONDER_SIZE_MEDIUM_LABEL",
                                           "TV_ENGINEERING_WONDER_SIZE_LARGE_LABEL"], "TV_ENGINEERING_WONDER_SIZE_SMALL_LABEL"),
                        "title": _t("Size is part of the proposal", "规模写在提案里"),
                        "text": _t(
                            "Each proposal carries its own size. It sets the [tv_wonder_construction|e] "
                            "cost, the number of units per part, and the ritual price later.",
                            "每项提案自带规模。规模决定[tv_wonder_construction|e]造价、每个部件的单元数，"
                            "以及之后仪式的价钱。",
                        ),
                    },
                ],
            },
            {
                "kind": "guide",
                "title": _t("Step 3  Win the Debate", "第三步 赢得辩论"),
                "anatomy": "debate",
                "icon": ICON_ESTATE,
                "body": _t(
                    "During [tv_wonder_debate|e], [ShowEstateTypeName('nobles_estate')], "
                    "[ShowEstateTypeName('burghers_estate')] and [ShowEstateTypeName('clergy_estate')] each "
                    "present one demand. Each demand has three responses.",
                    "[tv_wonder_debate|e]阶段，[ShowEstateTypeName('nobles_estate')]、"
                    "[ShowEstateTypeName('burghers_estate')]和[ShowEstateTypeName('clergy_estate')]"
                    "会各提一项诉求。每项诉求有三种处理方式。",
                ),
                "rows": [
                    {
                        "mock": ("bar", "TV_ENGINEERING_DOMESTIC_SUPPORT_LABEL", 135, "135 / 100",
                                 ("TV_ENGINEERING_SUPPORT_BASE_LABEL", "TV_ENGINEERING_SUPPORT_RESERVE_LABEL")),
                        "title": _t("One number to reach, one you may bank", "一个要够，一个可以存"),
                        "text": _t(
                            "The upper bar is [tv_wonder_domestic_support|e] against its target of 100. "
                            "The lower caption is the reserve the debate allows you to carry to 200, so a "
                            "surplus of 100 is worth keeping.",
                            "上面那条是[tv_wonder_domestic_support|e]，目标 100。下面的小字写的是辩论允许你囤到的上限 200，"
                            "所以超出 100 的部分不要白扔。",
                        ),
                    },
                    {
                        "mock": ("demands", None, None),
                        "title": _t("Three estates, three demands", "三个阶层，三项诉求"),
                        "text": _t(
                            "Each estate posts one demand with its own price. Reading all three before "
                            "acting is free and tells you which responses are cheapest this round.",
                            "每个阶层提一项诉求，各带各的价码。先读三项再动手不花钱，也能看出这轮哪种回应最便宜。",
                        ),
                    },
                    {
                        "mock": ("buttons", [("TV_ENGINEERING_ACCEPT_SHORT_BUTTON", "green"),
                                             ("TV_ENGINEERING_REFUTE_SHORT_BUTTON", "red"),
                                             ("TV_ENGINEERING_BRIBE_SHORT_BUTTON", "yellow")], None),
                        "title": _t("Accept, refute or bribe", "接受、驳倒或贿赂"),
                        "text": _t(
                            "Accept gains 20 [tv_wonder_domestic_support|e] and pays the demand's price. "
                            "Refute spends 10 [prestige|e] and Bribe spends scaled [gold|e] to replace the "
                            "demand with another, so they only reroll the price.",
                            "「接受」拿 20 点[tv_wonder_domestic_support|e]，同时付清诉求的代价。"
                            "「驳倒」花 10 [prestige|e]、「贿赂」花缩放[gold|e]，都只是把这一项换成别的，也就是重摇价码。",
                        ),
                    },
                    {
                        "mock": ("button", "TV_ENGINEERING_END_DEBATE_BUTTON", "green", None),
                        "title": _t("Closing the debate is a button, not automatic", "结束辩论要手动点"),
                        "text": _t(
                            "Support does not close the debate on its own. At 100 and above, click this bar.",
                            "支持度够了不会自动结束辩论。到 100 以上之后，点这条按钮。",
                        ),
                    },
                ],
            },
            {
                "kind": "guide",
                "title": _t("Step 4  Survey and Lock In the Site", "第四步 测绘并锁定工地"),
                "anatomy": "survey",
                "icon": ICON_MAP,
                "body": _t(
                    "Click 'Assign Survey Site' and choose one of your country's [location|e]s. Each month, "
                    "survey progress increases by 0.1 times the Great Engineer's [mil|e]. At 100, the survey "
                    "produces three readings.",
                    "点「指派测绘地点」，选一处本国[location|e]。每个月测绘进度增加大工程师[mil|e]的 0.1 倍，"
                    "满 100 后会得出三项读数。",
                ),
                "rows": [
                    {
                        "mock": ("bar", "TV_ENGINEERING_SURVEY_PROGRESS_LABEL", 100, "100 / 100"),
                        "title": _t("Survey progress is the second meter", "测绘进度是第二条进度"),
                        "text": _t(
                            "It fills from the engineer's [mil|e], not their [adm|e], at 0.1 a month per point. "
                            "The site you name does not change the pace, only the readings.",
                            "它由大工程师的[mil|e]推动，与[adm|e]无关，每点每月 0.1。你选的工地不改变速度，只改变读数。",
                        ),
                    },
                    {
                        "mock": ("buttons", [("TV_ENGINEERING_SELECT_SURVEY_SITE_BUTTON", "yellow"),
                                             ("TV_ENGINEERING_RERUN_SURVEY_BUTTON", "yellow")], None),
                        "title": _t("Name a site, then ask again", "先指地方，不满意再测一次"),
                        "text": _t(
                            "Set Survey Site opens the location picker. Rerun Survey discards the readings "
                            "and starts a fresh survey, which costs the same time again.",
                            "「指派测绘地点」打开地图选点。「重新执行测绘」会丢掉这次读数重来一遍，时间照样要再花一次。",
                        ),
                    },
                    {
                        "mock": ("triplet", None, None),
                        "title": _t("The three readings", "三项读数"),
                        "text": _t(
                            "[tv_wonder_scale_competence|e] sets the wonder's maximum level, with bands at "
                            "20, 40, 60, 80 and 100; level 6 needs a full 100. "
                            "[tv_wonder_organization_competence|e] sets the worksite level cap. "
                            "[tv_wonder_logistics_competence|e] sets the construction speed multiplier.",
                            "[tv_wonder_scale_competence|e]决定奇观最高能建到几级，以 20、40、60、80、100 分档，6 级需要满 100；"
                            "[tv_wonder_organization_competence|e]决定工地等级上限；"
                            "[tv_wonder_logistics_competence|e]决定施工速度乘数。",
                        ),
                    },
                    {
                        "mock": ("button", "TV_ENGINEERING_CONFIRM_SURVEY_SITE_BUTTON", "green", None),
                        "title": _t("Confirming is irreversible", "确认之后不可更改"),
                        "text": _t(
                            "Until you click it the readings are a preview. After it, they are the "
                            "project's permanent ceiling, so compare all three before committing.",
                            "在点之前，读数只是预览；点了之后，它们就是这项工程永久的上限。所以提交前把三项都看一遍。",
                        ),
                    },
                ],
            },
            {
                "kind": "guide",
                "title": _t("Step 5  Organization and Logistics", "第五步 组织和物流"),
                "anatomy": "organization_logistics",
                "icon": ICON_LABOR,
                "body": _t(
                    "Confirming the site unlocks the 'Organization and Logistics' card in the panel.",
                    "选址确认后，面板上的「组织和物流」卡解锁。",
                ),
                "rows": [
                    {
                        "mock": ("bar", "TV_ENGINEERING_ORGANIZATION_COMPETENCE_LABEL", 62, "7 / 12"),
                        "title": _t("Organization decides how many worksites", "组织决定能建几座工地"),
                        "text": _t(
                            "[tv_wonder_organization_competence|e] is the level cap. Level that many "
                            "[ShowBuildingTypeName('tv_wonder_labor_camp')]s in the site's [market|e] and no "
                            "more; each operating level supplies 1000 progress a month.",
                            "[tv_wonder_organization_competence|e]就是等级上限。在工地所在[market|e]里最多修这么多级"
                            "[ShowBuildingTypeName('tv_wonder_labor_camp')]，每级正常运转每月提供 1000 点进度。",
                        ),
                    },
                    {
                        "mock": ("stats", None, None),
                        "title": _t("Four numbers on the worksite card", "工地卡上的四个数"),
                        "text": _t(
                            "Base progress is what the worksites produce. Employment is how much of their "
                            "workforce is filled, from local [ShowPopTypeName('laborers')]; vacancies cut "
                            "progress in proportion. Maintenance is the monthly cost.",
                            "「基础进度」是工地能产出的量；「雇佣」是岗位填满的比例，靠当地[ShowPopTypeName('laborers')]，"
                            "空缺按比例削减进度；「总维护费」是每月开支。",
                        ),
                    },
                    {
                        "mock": ("stats_goods", None, None),
                        "title": _t("Two goods, two numbers each", "两种物资，各看两个数"),
                        "text": _t(
                            "The worksite consumes [ShowGoodsName('tools')] and "
                            "[ShowGoodsName('tv_wonder_materials')] every month. Demand over supply is the "
                            "figure to watch; when supply falls short, imports or a "
                            "[ShowBuildingTypeName('tv_wonder_material_dispatch_point')] close the gap.",
                            "工地每月消耗[ShowGoodsName('tools')]和[ShowGoodsName('tv_wonder_materials')]。"
                            "要盯的是「需求 / 供给」这一栏，供给不够时靠进口或"
                            "[ShowBuildingTypeName('tv_wonder_material_dispatch_point')]补上。",
                        ),
                    },
                    {
                        "mock": ("equation", None, None),
                        "title": _t("The multiplication at the bottom", "底部的连乘式"),
                        "text": _t(
                            "Monthly progress = Worksite progress × Material efficiency × "
                            "[tv_wonder_logistics_competence|e] multiplier (50% to 150%). The bottom of the "
                            "card spells the same sum out with your own figures.",
                            "每月进度 = 工地进度 × 物资效率 × [tv_wonder_logistics_competence|e]乘数（50% 到 150%）。"
                            "卡片底部会用你自己的数字把同一道算式列出来。",
                        ),
                    },
                    {
                        "mock": ("button", "TV_ENGINEERING_BUILD_WORKSITE_BUTTON", "yellow", None),
                        "title": _t("Building is a separate step", "建工地是另一步"),
                        "text": _t(
                            "The card only reports. Click this button to actually construct the worksites; "
                            "until you do, every progress figure stays at zero.",
                            "卡片只负责汇报。要真的把工地建起来得点这条按钮，在此之前所有进度数字都是零。",
                        ),
                    },
                ],
            },
            {
                "kind": "guide",
                "title": _t("Step 6  Construction", "第六步 建设"),
                "anatomy": "construction",
                "icon": ICON_BUILD,
                "body": _t(
                    "Only one [tv_wonder_construction_part|e] advances at a time. By default, the part with "
                    "the least progress is selected automatically. You can also switch manually with the "
                    "four buttons below, but switching resets progress on the current unit to zero.",
                    "同一时间只推进一个[tv_wonder_construction_part|e]，默认自动选进度最落后的那个。"
                    "你也可以点「建设基础」「建设主体」「建设功能」「建设封顶装饰」手动切换，但切换会清零当前这一单元的进度。",
                ),
                "rows": [
                    {
                        "mock": ("parts", None, None),
                        "title": _t("Four rows, each with its units", "四行部件，各有各的单元"),
                        "text": _t(
                            "Every part is a row of unit buttons. Green is finished, yellow is the unit "
                            "being built now, red is still waiting. Only the yellow row is moving.",
                            "每个部件都是一排单元按钮：绿色是已完成，黄色是正在建的那个，红色是还排着的。只有黄色那一行在动。",
                        ),
                    },
                    {
                        "mock": ("buttons", [("TV_ENGINEERING_CONSTRUCTION_PART_FOUNDATION", "yellow"),
                                             ("TV_ENGINEERING_CONSTRUCTION_PART_BODY", "yellow"),
                                             ("TV_ENGINEERING_CONSTRUCTION_PART_FUNCTION", "yellow"),
                                             ("TV_ENGINEERING_CONSTRUCTION_PART_DECORATION", "yellow")], None),
                        "title": _t("Switch parts by hand, at a price", "手动切换要付代价"),
                        "text": _t(
                            "The four switches override the automatic choice. The current unit's progress "
                            "resets to zero, so switch only when the order actually matters.",
                            "这四个切换按钮会覆盖自动选择，代价是当前单元的进度清零。所以只有顺序真的重要时才手动切。",
                        ),
                    },
                    {
                        "mock": ("stat", "TV_ENGINEERING_WONDER_LEVEL_LABEL", "2",
                                 "TV_ENGINEERING_ACTIVE_PART_LABEL", "TV_ENGINEERING_ACTIVE_PART_BODY"),
                        "title": _t("The level is the weakest part", "等级取最弱的那个部件"),
                        "text": _t(
                            "The wonder's level equals its least advanced part, which is why the switches "
                            "matter at all. Building only one part perfectly raises nothing.",
                            "奇观等级等于最落后的那个部件，这正是切换按钮存在的理由。只把一个部件做到极致，等级不会升。",
                        ),
                    },
                    {
                        "mock": ("button", "TV_ENGINEERING_FINISH_CONSTRUCTION_BUTTON", "green", None),
                        "title": _t("Finished means one level higher", "完工的定义是涨了一级"),
                        "text": _t(
                            "The button unlocks once the level is at least one above where it stood when "
                            "construction began. Clicking it ends the construction stage for good.",
                            "只有等级比开工时至少高一级，这条按钮才会亮。点下去，建设阶段就永久结束。",
                        ),
                    },
                ],
            },
            {
                "kind": "guide",
                "title": _t("Step 7  Ceremony", "第七步 仪式"),
                "anatomy": "ceremony",
                "icon": ICON_CEREMONY,
                "body": _t(
                    "After construction, the project enters [tv_wonder_ceremony|e]. You have two choices.",
                    "建成后进入[tv_wonder_ceremony|e]阶段，有两种选择。",
                ),
                "rows": [
                    {
                        "mock": ("styles", ["TV_WONDER_RITUAL_NAME_1_1", "TV_WONDER_RITUAL_NAME_2_1",
                                            "TV_WONDER_RITUAL_NAME_3_1"], None),
                        "title": _t("Three styles, free to compare", "三种风格，免费比较"),
                        "text": _t(
                            "The style buttons above the detail panel are previews. Clicking one costs "
                            "nothing and changes no state, so try them all and read the expected effects "
                            "before you commit. Styles are specific to the wonder: Royal Sacrifice, "
                            "Meditation Ceremony and Divine Investiture are only the first project's.",
                            "详情面板上方的风格按钮只是预览。点它们不花钱、也不改变任何状态，"
                            "所以尽管挨个点开，把预期效果念完再决定。风格是按奇观定的："
                            "「王室献祭」「冥想典礼」「神圣授职」只是第一座工程的选项。",
                        ),
                    },
                    {
                        "mock": ("stats", None, None),
                        "title": _t("What the preview tells you", "预览里能看到什么"),
                        "text": _t(
                            "Each style lists its rewards and which estates support or oppose it. Supporting "
                            "estates receive +0.10 [estate_satisfaction|e]; the others receive −0.05. The "
                            "settlement happens when you confirm, not month by month.",
                            "每种风格列出它的奖励，以及哪些阶层支持、哪些反对。支持的阶层[estate_satisfaction|e] +0.10，其余 −0.05。"
                            "这些在确认时一次性结算，不是逐月变化。",
                        ),
                    },
                    {
                        "mock": ("buttons", [("TV_WONDER_RITUAL_CONFIRM", "green"),
                                             ("TV_WONDER_RITUAL_PLAIN", "yellow")], None),
                        "title": _t("Two ways to finish, one is free", "两种收尾，一种免费"),
                        "text": _t(
                            "Hold Ceremony costs 2, 3 or 5 times scaled [gold|e] for a small, medium or "
                            "large project and dedicates after 24 months. Inaugurate plainly completes at "
                            "once for nothing, at −0.05 satisfaction and into the [tv_wonder_plain|e] state.",
                            "「举行仪式」按小、中、大规模支付 2、3、5 倍缩放[gold|e]，24 个月后落成。"
                            "「以朴素方式落成」立刻完成且不花钱，代价是 −0.05 满意度，并进入[tv_wonder_plain|e]状态。",
                        ),
                    },
                    {
                        "mock": None,
                        "title": _t("A plain wonder is not a dead end", "朴素落成不是死路"),
                        "text": _t(
                            "A plain wonder can receive a ceremony later. During conception, use the "
                            "'Rededicate a Wonder' [decision|e], or click 'Hold a New Ceremony for This "
                            "Project' in the location panel.",
                            "朴素奇观以后还能补办仪式：在构想阶段使用[decision|e]「重新奉献奇观」，"
                            "或者在地点面板点「为此工程重新举行仪式」。",
                        ),
                    },
                ],
            },
        ],
    },
    # --------------------------------------------------------- engineering dept ----
    {
        "id": "department",
        "filter": "mechanics",
        "icon": ICON_ED,
        "title": _t("The Engineering Department", "工程部"),
        "lead": _t(
            "A standing office, one officer, one project at a time. It costs nothing to keep open and "
            "it is the only place a wonder can begin.",
            "一个常设机构，一名官员，同一时间只推进一个工程。维持它不需要花费，而一切奇观只能从这里开始。",
        ),
        "sections": [
            {
                "kind": "text",
                "title": _t("What the Office Is", "这个机构是什么"),
                "icon": ICON_GOV,
                "body": _t(
                    "Every country holds a seat in the Engineering Department from the first day of the "
                    "campaign, whether or not it ever builds anything. The department does not build: it "
                    "holds the project. It remembers which wonder is underway, how far each part has "
                    "risen, what the surveyors measured, whether support has collapsed, and who is "
                    "entitled to be remembered at the dedication.\n\n"
                    "Because the project lives in the department and not in the buildings, a wonder "
                    "survives losing its engineer, losing its site, or being paused for decades. Only "
                    "abandoning the project or failing it outright ends the round.",
                    "从战役第一天起，每个国家都在工程部中拥有席位，无论它是否真的打算建造什么。工程部并不"
                    "施工，它持有工程：记住哪座奇观正在推进、每个部件建到多高、勘测师量到了什么、支持度是否"
                    "崩塌过，以及落成时谁有权被记住。\n\n"
                    "正因为工程存在于部门而不存在于建筑里，奇观不会因为失去总工程师、失去工地、或停摆数十年而"
                    "消失。只有放弃工程或彻底失败，才会结束这一轮。",
                ),
            },
            {
                "kind": "entries",
                "title": _t("What It Tracks", "它记住什么"),
                "icon": ICON_BOOK,
                "entries": [
                    {
                        "icons": [("icon", ICON_IDEA)],
                        "title": _t("The Current Wonder", "当前奇观"),
                        "text": _t(
                            "Which wonder, at which size, at which site, in which stage. One at a time: "
                            "a second project waits until the first is finished, abandoned or failed.",
                            "哪一座奇观、什么规模、选在何处、处于哪一阶段。同一时间只推进一个：第二个工程要等"
                            "第一个建成、放弃或失败。",
                        ),
                    },
                    {
                        "icons": [("icon", ICON_GROWTH)],
                        "title": _t("Progress and Competence", "进度与能力"),
                        "text": _t(
                            "Conception and survey progress, the four construction part counts, and the "
                            "three survey readings that cap everything downstream.",
                            "构想与勘测进度、四个部件的计数，以及限制下游一切的三项勘测读数。",
                        ),
                    },
                    {
                        "icons": [("icon", ICON_ESTATE)],
                        "title": _t("Support and Estate Mood", "支持度与阶层情绪"),
                        "text": _t(
                            "Current Domestic Support, whether this round's one reprieve has been spent, "
                            "and which estate asked for what during the debate.",
                            "当前国内支持度、本轮唯一一次挽救是否已用掉，以及辩论中哪个阶层提了什么要求。",
                        ),
                    },
                ],
            },
        ],
    },
    {
        "id": "engineer",
        "filter": "mechanics",
        "icon": ICON_ENGINEER,
        "title": _t("The Great Engineer", "总工程师"),
        "lead": _t(
            "One character does the thinking and the walking. Their Administrative skill decides how "
            "fast a project is conceived, their Military skill how fast it is surveyed, and their name "
            "is on the monument afterwards.",
            "智与行皆系于一人。行政能力决定构想多快，军事能力决定勘测多快，而落成之后，碑上刻的是他的名字。",
        ),
        "sections": [
            {
                "kind": "entries",
                "title": _t("What Each Skill Does", "各项能力的作用"),
                "icon": ICON_ENGINEER,
                "entries": [
                    {
                        "icons": [("icon", ICON_IDEA)],
                        "title": _t("Administrative Skill, in Conception", "行政能力 · 构想"),
                        "text": _t(
                            "Conception progress rises #high 1/5#! of the engineer's Administrative skill "
                            "each month. A skill of 10 is two points a month; the meter runs to 100.",
                            "每月构想进度增加 #high 1/5#! 的行政能力。行政能力 10 即每月 2 点；进度条满值为 100。",
                        ),
                    },
                    {
                        "icons": [("icon", ICON_MAP)],
                        "title": _t("Military Skill, in Survey", "军事能力 · 勘测"),
                        "text": _t(
                            "Survey progress rises #high 1/10#! of Military skill each month, and the "
                            "survey is what confirms the ground. A strong engineer on a good site is "
                            "the whole difference between a level 3 monument and a level 6 one.",
                            "每月勘测进度增加 #high 1/10#! 的军事能力，而只有勘测才能确认地基。一位能干的总工程师"
                            "加上一块好地基，正是三级纪念碑与六级纪念碑的全部差别。",
                        ),
                    },
                    {
                        "icons": [("icon", ICON_CROWN)],
                        "title": _t("Tenure", "任期"),
                        "text": _t(
                            "The office is a role on the character, not a permanent appointment. Dismiss "
                            "them and their replacement picks the project up where it stands, but a "
                            "vacant seat freezes conception and survey until someone is appointed, while "
                            "construction and ritual continue.",
                            "这是一项挂在人物身上的职务，而非终身任命。撤换之后，继任者从工程当前进度接手；但职位"
                            "空缺期间构想与勘测会冻结，施工与仪式则照常进行。",
                        ),
                    },
                ],
            },
            {
                "kind": "text",
                "title": _t("Choosing One", "如何挑选"),
                "icon": ICON_PRESTIGE,
                "body": _t(
                    "Look at the two skills the project actually consumes: Administrative for what comes "
                    "next, Military for the site. An old, highly skilled engineer is often better than a "
                    "young brilliant one, because a project takes years and a dead engineer stops both "
                    "of the meters that matter.\n\n"
                    "There is no experience, no training and no promotion attached to the post. The "
                    "engineer is a filter on your project's speed, nothing more.",
                    "只需看工程真正消耗的那两项能力：行政用于下一步，军事用于选址。一位年迈而能力极高者，往往"
                    "胜过一位年轻天才，因为工程以年计，而总工程师一死，两个最要紧的进度条都会停下。\n\n"
                    "这个职位没有经验、没有培训、没有晋升。总工程师只是筛子，决定你的工程有多快，如此而已。",
                ),
            },
        ],
    },
    # ------------------------------------------------------------------ conception ----
    {
        "id": "conception",
        "filter": "mechanics",
        "icon": ICON_IDEA,
        "title": _t("Conception", "构想"),
        "lead": _t(
            "The engineer decides what the country is capable of building, and puts three proposals "
            "in front of you. You may accept one, reject them for a small price, or buy a new set.",
            "总工程师判断这个国家能建什么，并把三份方案摆在你面前。你可以接受其一、花小代价驳回，或出钱换一批。",
        ),
        "sections": [
            {
                "kind": "flow",
                "title": _t("How a Proposal Becomes a Project", "提案如何成为工程"),
                "icon": ICON_IDEA,
                "steps": [
                    {
                        "icon": ICON_ENGINEER,
                        "link": LINK_ENGINEER,
                        "title": _t("The Meter Fills", "进度积累"),
                        "text": _t(
                            "Conception progress rises every month from Administrative skill until it "
                            "reaches 100.",
                            "构想进度每月按行政能力增长，直至 100。",
                        ),
                    },
                    {
                        "icon": ICON_IDEA,
                        "link": LINK_CONCEPT,
                        "title": _t("Three Proposals", "三份方案"),
                        "text": _t(
                            "The engineer offers up to three undertakings the country can actually "
                            "support, at a size it can actually carry.",
                            "总工程师提出至多三份工程，其规模都在国家当下能真正承受的范围内。",
                        ),
                    },
                    {
                        "icon": ICON_CROWN,
                        "link": LINK_SMALL,
                        "title": _t("Choose a Size", "选定规模"),
                        "text": _t(
                            "Small, medium or large. Size sets the ritual price, the per-unit "
                            "construction demand and the ceiling on how often it can be repeated.",
                            "小、中、大。规模决定仪式价格、每单元施工需求，以及可重复建造的次数上限。",
                        ),
                    },
                    {
                        "icon": ICON_ESTATE,
                        "link": LINK_DEBATE,
                        "title": _t("Accept", "接受"),
                        "text": _t(
                            "Accepting locks the wonder and opens the domestic debate. Nothing is "
                            "spent yet.",
                            "接受即锁定奇观并开启国内辩论。此时尚未支出分文。",
                        ),
                    },
                ],
            },
            {
                "kind": "entries",
                "title": _t("Your Three Answers", "三种回应"),
                "icon": ICON_GOLD,
                "entries": [
                    {
                        "icons": [("icon", ICON_GOLD)],
                        "title": _t("Accept", "接受"),
                        "text": _t(
                            "Take the proposal as it stands and move to the [tv_wonder_debate|e]. "
                            "Free.",
                            "按原样接受提案，进入[tv_wonder_debate|e]。免费。",
                        ),
                    },
                    {
                        "icons": [("icon", ICON_PRESTIGE)],
                        "title": _t("Reject", "驳回"),
                        "text": _t(
                            "Pay a little #high prestige#! and go back to conceiving. Use it when the "
                            "three proposals are all wrong for your country's geography.",
                            "付出少量 #high 威望#! 后退回构想。当三份方案都与本国的地理条件不合时使用。",
                        ),
                    },
                    {
                        "icons": [("icon", ICON_GOLD)],
                        "title": _t("Bribe", "贿赂"),
                        "text": _t(
                            "Pay one size-scaled sum of #high gold#! and draw a fresh set immediately. "
                            "The expensive way to keep looking.",
                            "付出一笔随规模缩放 #high 金币#!，立即重抽一批。是用钱继续挑选的方式。",
                        ),
                    },
                ],
            },
        ],
    },
    # ---------------------------------------------------------------------- debate ----
    {
        "id": "debate",
        "filter": "mechanics",
        "icon": ICON_ESTATE,
        "title": _t("The Domestic Debate", "国内辩论"),
        "lead": _t(
            "Before a single stone is cut, the nobility, the burghers and the clergy each want "
            "something. Satisfy enough of them and Domestic Support reaches 100 and the debate "
            "closes.",
            "在动第一块石头之前，贵族、市民与教士各有所求。满足足够多的诉求，国内支持度达到 100，辩论即告结束。",
        ),
        "sections": [
            {
                "kind": "text",
                "title": _t("What Support Is", "支持度是什么"),
                "icon": ICON_ESTATE,
                "body": _t(
                    "[tv_wonder_domestic_support|e] is the country's willingness to keep paying for "
                    "somebody else's monument. It runs from #high 0 to 200#! and it is the only figure "
                    "that can end your project outright.\n\n"
                    "Once the debate closes, support stops being a goal and becomes a clock. It decays "
                    "every month for the whole of survey and construction, and reclaiming it is far "
                    "harder than earning it was.",
                    "[tv_wonder_domestic_support|e] 是这个国家愿意继续为他人纪念碑掏钱的程度。取值"
                    "#high 0 到 200#!，也是唯一能让工程当场终止的数值。\n\n"
                    "辩论结束之后，支持度不再是目标，而成了倒计时。整个勘测与施工期间它每月衰减，而重新把它"
                    "补回来，远比当初挣到它更难。",
                ),
            },
            {
                "kind": "scale",
                "title": _t("The Shape of the Debate", "辩论的区间"),
                "icon": ICON_CROWN,
                "steps": [
                    {"medallion": ("bar", 0.0), "label": _t("0\nDebate ends in failure", "0\n辩论以失败告终")},
                    {"medallion": ("bar", 0.5), "label": _t("100\nDebate may close", "100\n可结束辩论")},
                    {"medallion": ("bar", 1.0), "label": _t("200\nCloses by itself", "200\n自动结束")},
                ],
                "body": _t(
                    "Support is spent as well as earned: every accepted demand adds a flat #high 20#!, "
                    "and a debate event can swing it either way by the same amount. At 200 the debate "
                    "closes whether or not you are ready, so the only reason to hold a full meter is to "
                    "carry the surplus into the decay that follows.",
                    "支持度既会积攒也会流失：每接受一项诉求固定 +20，辩论事件也可能以同样的幅度加减。达到 200 "
                    "时辩论会自动结束，不论你是否准备好；因此把进度条压满的唯一理由，就是把这部分盈余带进随后的"
                    "衰减期。",
                ),
            },
            {
                "kind": "entries",
                "title": _t("Reading the Room", "读懂局势"),
                "icon": ICON_LAW,
                "entries": [
                    {
                        "icons": [("icon", ICON_ESTATE)],
                        "title": _t("Only Living Estates Play", "只有在场的阶层参与"),
                        "text": _t(
                            "A country without burghers simply has one fewer demand to satisfy. The "
                            "debate never asks for what the realm does not have.",
                            "没有市民阶层的国家，就少一项诉求要满足。辩论从不会索要国家本就没有的东西。",
                        ),
                    },
                    {
                        "icons": [("icon", ICON_GOLD)],
                        "title": _t("Paying Your Way Out", "花钱脱身"),
                        "text": _t(
                            "Every demand can be bribed away for one size-scaled sum of gold, at the "
                            "cost of drawing a new demand from the same estate. Gold is the only "
                            "resource that can make this stage harmless.",
                            "任何诉求都可以用一笔随规模缩放的金币打发了事，代价是该阶层会重新抽取一项诉求。金币是"
                            "唯一能让这个阶段变得无害的资源。",
                        ),
                    },
                    {
                        "icons": [("icon", ICON_WARNING)],
                        "title": _t("When It Runs Out", "耗尽之后"),
                        "text": _t(
                            "The first time support hits zero after the debate, the court offers one "
                            "reprieve: bribe the estates or make a public statement. The second time, "
                            "the project ends.",
                            "辩论结束后第一次归零，朝廷会给出一次挽救机会：收买各阶层，或由君主公开表态。第二次"
                            "归零，工程即告终止。",
                        ),
                    },
                ],
            },
        ],
    },
    # ------------------------------------------------------------------- demands ----
    {
        "id": "demands",
        "filter": "mechanics",
        "icon": ICON_LAW,
        "title": _t("Estate Demands", "阶层诉求"),
        "lead": _t(
            "Every demand is a real concession out of your own treasury or your own privileges. "
            "There are only a handful of kinds, and each one maps to a tooltip you can read before "
            "you accept it.",
            "每一项诉求都是从你自己的国库或特权里真实割出去的东西。种类并不多，每一种在你接受之前都能读到"
            "对应的提示。",
        ),
        "sections": [
            {
                "kind": "entries",
                "title": _t("The Kinds of Demand", "诉求的种类"),
                "icon": ICON_LAW,
                "entries": [
                    {
                        "icons": [("icon", ICON_CROWN)],
                        "title": _t("A Privilege", "授予特权"),
                        "text": _t(
                            "One of that estate's unpicked privileges is granted, permanently and for "
                            "free. The cheapest-looking demand and often the most lasting cost.",
                            "该阶层一项尚未授予的特权被永久授予，且不收费。看起来最便宜的诉求，往往代价最长久。",
                        ),
                    },
                    {
                        "icons": [("icon", ICON_GOLD)],
                        "title": _t("Lighter Burdens", "减轻负担"),
                        "text": _t(
                            "Five years of lower taxation or lower conscription for that estate. It "
                            "expires, which makes it the easiest demand to accept.",
                            "为该阶层减免税负或征召义务五年。它会自行失效，因此是最容易接受的诉求。",
                        ),
                    },
                    {
                        "icons": [("icon", ICON_GOV)],
                        "title": _t("A Policy Change", "更改政策"),
                        "text": _t(
                            "A policy that estate favours is enacted, with its usual stability price. "
                            "You may not always be able to pay it.",
                            "颁布该阶层偏好的政策，并照旧支付其稳定度代价。你未必总能付得起。",
                        ),
                    },
                    {
                        "icons": [("icon", ICON_STARVE)],
                        "title": _t("Punishment", "惩罚"),
                        "text": _t(
                            "Lost prestige, lost stability, lost legitimacy, a rival estate offended, "
                            "mild inflation. Straightforward to read, straightforward to pay.",
                            "损失威望、稳定度或正统性，得罪另一个阶层，或来一次轻度通胀。看得明白，也付得明白。",
                        ),
                    },
                    {
                        "icons": [("icon", ICON_ART)],
                        "title": _t("A Sacrifice", "牺牲"),
                        "text": _t(
                            "A cabinet member dismissed, an artist killed, a work of art destroyed. "
                            "The demands that hurt beyond the ledger.",
                            "阁员被逐出内阁、艺术家被处死、艺术品被销毁。这是超出账面的伤害。",
                        ),
                    },
                ],
            },
            {
                "kind": "text",
                "title": _t("What Choice You Actually Have", "你真正的选择"),
                "icon": ICON_GOLD,
                "body": _t(
                    "Accepting is usually the right answer, because #high 20 support#! is worth more "
                    "than most single costs, and because gold can buy you past anything you refuse.\n\n"
                    "The one demand to think twice about is a privilege: it is the only one that never "
                    "comes back to you. If the estates are already powerful, refusing it for prestige "
                    "or gold is usually the better trade.",
                    "接受通常是对的，因为 #high 20 点支持度#! 比多数单项代价更值钱，而且金币能让你绕过任何"
                    "你不愿接受的东西。\n\n"
                    "唯一值得犹豫的是授予特权：它是唯一不会回到你手上的代价。若各阶层本已势大，用威望或金币"
                    "驳回它，通常是更划算的交易。",
                ),
            },
        ],
    },
    # -------------------------------------------------------------------- survey ----
    {
        "id": "survey",
        "filter": "mechanics",
        "icon": ICON_MAP,
        "title": _t("Survey", "勘测"),
        "lead": _t(
            "The survey is where the ground argues back. You pick a location; the surveyors read what "
            "it can actually carry, and those readings cap the project for the rest of its life.",
            "勘测是地基反过来向你提出异议的环节。你选定地点，勘测师读出它真正能承载什么，而这些读数将在"
            "此后整段工程中封顶。",
        ),
        "sections": [
            {
                "kind": "flow",
                "title": _t("Choosing the Ground", "选定地基"),
                "icon": ICON_MAP,
                "steps": [
                    {
                        "icon": ICON_MAP,
                        "link": LINK_SURVEY,
                        "title": _t("Pick a Location", "选择地点"),
                        "text": _t(
                            "Any location you own that meets the wonder's own siting rule. The "
                            "department lists which do.",
                            "任何满足该奇观选址规则的自有地点。部门面板会列出符合条件的那些。",
                        ),
                    },
                    {
                        "icon": ICON_ENGINEER,
                        "link": LINK_ENGINEER,
                        "title": _t("The Meter Fills", "进度积累"),
                        "text": _t(
                            "Survey progress rises at #high 1/10#! of Military skill a month until it "
                            "reaches 100.",
                            "勘测进度以每月 #high 1/10#! 军事能力增长，直至 100。",
                        ),
                    },
                    {
                        "icon": ICON_SCALE,
                        "link": LINK_SCALE,
                        "title": _t("Read the Ground", "读数"),
                        "text": _t(
                            "Scale, organization and logistics are each measured: natural suitability "
                            "plus the engineer's Administrative skill.",
                            "规模、组织与后勤各自计量：天然适宜度加上总工程师的行政能力。",
                        ),
                    },
                    {
                        "icon": ICON_BUILD,
                        "link": LINK_CONSTRUCTION,
                        "title": _t("Lock the Site", "锁定工地"),
                        "text": _t(
                            "Confirming fixes the site and the readings. They cannot be improved once "
                            "construction begins.",
                            "确认之后，工地与读数即固定。一旦动工便无法再提升。",
                        ),
                    },
                ],
            },
            {
                "kind": "text",
                "title": _t("Re-surveying", "重新勘测"),
                "icon": ICON_WARNING,
                "body": _t(
                    "Choosing a new site is free and often worth doing: a coastal city with a good "
                    "harbour will out-read an inland village by a wide margin, and the survey meter is "
                    "the cheapest thing in the whole project to refill.\n\n"
                    "Confirming a site is what costs you. A site abandoned before confirmation was never "
                    "spent.",
                    "换一处地点不花钱，而且往往值得一做：一个有良港的沿海城市，读数会远远好过内陆村庄，而勘测"
                    "进度是整个工程里最便宜的可重复项。\n\n"
                    "真正让你付出的是确认工地。确认之前放弃的地基，从未算作花费。",
                ),
            },
        ],
    },
    # ---------------------------------------------------------------- competences ----
    {
        "id": "competences",
        "filter": "mechanics",
        "icon": ICON_SCALE,
        "title": _t("Survey Competences", "勘测能力"),
        "lead": _t(
            "Three readings come out of a survey. Scale caps the wonder's level, organization caps the "
            "size of the workforce you can put on it, and logistics sets how fast the work actually "
            "moves.",
            "勘测会得出三项读数。规模封顶奇观等级，组织封顶你能投入的劳动力规模，后勤决定施工实际推进的速度。",
        ),
        "sections": [
            {
                "kind": "scale",
                "title": _t("Scale: the Level Ceiling", "规模：等级上限"),
                "icon": ICON_SCALE,
                "steps": [
                    {"medallion": ("roman", 1), "label": _t("20\nLevel I", "20\n一级")},
                    {"medallion": ("roman", 2), "label": _t("40\nLevel II", "40\n二级")},
                    {"medallion": ("roman", 3), "label": _t("60\nLevel III", "60\n三级")},
                    {"medallion": ("roman", 4), "label": _t("80\nLevel IV", "80\n四级")},
                    {"medallion": ("roman", 5), "label": _t("100\nLevel V", "100\n五级")},
                    {"medallion": ("roman", 6), "label": _t("+ Settings\nLevel VI", "+ 设置\n六级")},
                ],
                "body": _t(
                    "Each band unlocks one more level. #high Level VI#! needs a full 100, which is why "
                    "a poor site can never be pushed to the top no matter how much gold you spend on "
                    "it. The Construction Flow Tuning setting can lift the ceiling entirely, for "
                    "players who would rather build than negotiate with geography.",
                    "每跨越一档即可多建一级。#high 六级#! 需要满 100，所以贫瘠的地基无论砸多少钱都推不到顶。"
                    "「施工流程调整」设置可以彻底解除上限，留给更想建造、而不是与地理讨价还价的玩家。",
                ),
            },
            {
                "kind": "panels",
                "title": _t("Organization and Logistics", "组织与后勤"),
                "icon": ICON_LABOR,
                "panels": [
                    {
                        "title": _t("Organization", "组织"),
                        "text": _t(
                            "Divided by five, this is the maximum level of the labor camp you may "
                            "raise on the site, capped at #high 20#!. The camp is the workforce: no "
                            "camp, no progress.",
                            "除以五，即为工地可建劳工营的最高等级，上限 #high 20#!。劳工营就是劳动力："
                            "没有营，就没有进度。",
                        ),
                        "items": [
                            {"icon": ICON_LABOR, "link": LINK_ORG},
                            {"icon": ICON_CONSTRUCTION, "link": "[ShowBuildingTypeName('tv_wonder_labor_camp')]"},
                        ],
                        "arrows": True,
                    },
                    {
                        "title": _t("Logistics", "后勤"),
                        "text": _t(
                            "Added to fifty, this is the percentage multiplier on progress: a reading "
                            "of 0 still moves at half speed, a reading of 100 at #high 150%#!.",
                            "加上五十，即为进度的百分比乘数：读数 0 也仍有半速，读数 100 则达 #high 150%#!。",
                        ),
                        "items": [
                            {"icon": ICON_LOG, "link": LINK_LOG},
                            {"icon": ICON_GROWTH, "link": "[tv_wonder_construction|e]"},
                        ],
                        "arrows": True,
                    },
                ],
            },
            {
                "kind": "text",
                "title": _t("Why the Ground Matters More Than the Engine", "为什么地基比人更关键"),
                "icon": ICON_PROSPERITY,
                "body": _t(
                    "Competence is a mix of the site's own suitability and the engineer's "
                    "Administrative skill, and the site half is usually the larger half. Two locations "
                    "in the same country can differ by tens of points because one is a capital city on "
                    "a river and the other is a hill village.\n\n"
                    "$BULLET$ A capital, a city, a port, a river and a road all raise the reading.\n"
                    "$BULLET$ Mountains, wetlands, jungle and harsh climate lower it.\n"
                    "$BULLET$ Development and existing buildings raise it, which is why a rich, busy "
                    "location is the best place for a wonder and the worst place to find free ground.",
                    "能力是地基天然适宜度与总工程师行政能力的混合，而地基那一半通常更大。同一个国家的两处"
                    "地点可以相差几十点，只因为一处是河畔都城，另一处是山间村落。\n\n"
                    "$BULLET$ 首都、城市、港口、河流与道路都会提高读数。\n"
                    "$BULLET$ 山地、湿地、丛林与恶劣气候会降低读数。\n"
                    "$BULLET$ 发展度与既有建筑会提高读数：所以富庶繁忙之地最适合建奇观，也最难找到空地。",
                ),
            },
        ],
    },
    # ---------------------------------------------------------------- construction ----
    {
        "id": "construction",
        "filter": "mechanics",
        "icon": ICON_BUILD,
        "title": _t("Construction", "施工"),
        "lead": _t(
            "Four parts rise at once from one labor camp. The wonder's level is the level of its "
            "slowest part, so feeding one part and starving the others is the most common way to "
            "waste a decade.",
            "四个部件从同一座劳工营同时升起。奇观等级等于最慢那个部件的等级，所以只喂一个部件、饿着其余，"
            "是最常见的虚耗十年之法。",
        ),
        "sections": [
            {
                "kind": "flow",
                "title": _t("The Four Parts", "四个部件"),
                "icon": ICON_BUILD,
                "steps": [
                    {
                        "icon": ICON_PART_FOUNDATION,
                        "link": LINK_PART,
                        "title": _t("Foundation", "地基"),
                        "text": _t(
                            "Clearing, levelling, drainage and the first courses of stone.",
                            "清场、平整、排水与最初的几层砌石。",
                        ),
                    },
                    {
                        "icon": ICON_PART_BODY,
                        "link": LINK_PART,
                        "title": _t("Main Structure", "主体"),
                        "text": _t(
                            "The mass of the building: walls, piers, vaults, the thing that is seen "
                            "from a distance.",
                            "建筑的本体：墙、墩、拱，从远处看得见的那一部分。",
                        ),
                    },
                    {
                        "icon": ICON_PART_FUNCTION,
                        "link": LINK_PART,
                        "title": _t("Function", "功能"),
                        "text": _t(
                            "What the wonder actually does: docks, granaries, halls, water, watch.",
                            "奇观真正起作用的部分：码头、粮仓、厅堂、水系、哨望。",
                        ),
                    },
                    {
                        "icon": ICON_PART_CROWNING,
                        "link": LINK_PART,
                        "title": _t("Crowning", "冠饰"),
                        "text": _t(
                            "Domes, spires, gilding and inscription: the part that makes it a wonder "
                            "and not a large building.",
                            "穹顶、尖塔、贴金与铭文：让它成为奇观而非一座大楼的部分。",
                        ),
                    },
                ],
            },
            {
                "kind": "text",
                "title": _t("What Actually Moves the Work", "真正推动工程的东西"),
                "icon": ICON_LABOR,
                "body": _t(
                    "Progress each month comes from four things at once, and any one of them can be "
                    "the bottleneck:\n\n"
                    "$BULLET$ #T The labor camp:#! each effective level adds a fixed amount of monthly "
                    "progress. Its level cap comes from Organization, and it consumes #high tools and "
                    "wonder materials#! every month.\n"
                    "$BULLET$ #T Employment:#! a camp with unfilled jobs produces nothing. You need "
                    "laborers in that location, not just the building.\n"
                    "$BULLET$ #T Inputs:#! the camp buys its materials on the local market. A poor "
                    "market means an empty-handed camp. Material workshops turn ordinary construction "
                    "goods into wonder materials through eight methods, each yielding 1.00 materials. "
                    "Earth, timber and kiln methods need no purchased tools; stone finishing and standardized "
                    "components reward developed industries. Choose by market prices and supply, or import materials.\n"
                    "$BULLET$ #T Logistics:#! the survey reading, applied as a 50% to 150% multiplier "
                    "on whatever the above produces.",
                    "每月进度同时来自四样东西，任何一样都可能成为瓶颈：\n\n"
                    "$BULLET$ #T 劳工营：#! 每个有效等级每月提供固定进度。等级上限来自组织能力，而它每月光是"
                    "维持就要消耗 #high 工具与奇观建材#!。\n"
                    "$BULLET$ #T 就业：#! 岗位空缺的营地什么也产出不了。那个地点要有劳工，而不只是有一栋建筑。\n"
                    "$BULLET$ #T 投入品：#! 营地在本地市场采购材料。建材工坊提供八种工艺，每种产出1.00份建材。"
                    "夯土、木构和烧砖无需外购工具，石材精加工与标准化构件则发挥成熟产业的优势。"
                    "应按市场价格与供应选择工艺，也可以通过贸易进口。市场贫弱，营地就空着手。\n"
                    "$BULLET$ #T 后勤：#! 勘测读数，以 50% 到 150% 的乘数作用在以上所有产出上。",
                ),
            },
            {
                "kind": "panels",
                "title": _t("Balanced or Rushed", "均衡还是催工"),
                "icon": ICON_CROWN,
                "panels": [
                    {
                        "title": _t("Four Even Parts", "四部齐进"),
                        "text": _t(
                            "Slow and sure. Every part reaches the new level together, the wonder "
                            "climbs one level at a time, and nothing is wasted holding a part above "
                            "the rest.",
                            "慢而稳。所有部件同时到达新等级，奇观逐级抬升，不会有任何部件被白白建到高于其余部件的位置。",
                        ),
                        "items": [
                            {"icon": ICON_PART_FOUNDATION, "link": ""},
                            {"icon": ICON_PART_BODY, "link": ""},
                            {"icon": ICON_PART_FUNCTION, "link": ""},
                            {"icon": ICON_PART_CROWNING, "link": ""},
                        ],
                        "arrows": False,
                    },
                    {
                        "title": _t("One Showpiece Part", "单推一部"),
                        "text": _t(
                            "Impressive in the panel, useless in the wonder. The other three parts "
                            "hold the level exactly where it was until they catch up.",
                            "在面板里好看，在奇观上无用。其余三个部件会把等级死死按在原处，直到它们追上来。",
                        ),
                        "items": [
                            {"icon": ICON_PART_CROWNING, "link": ""},
                            {"icon": ICON_PART_FOUNDATION, "link": "", "alpha": 0.4},
                            {"icon": ICON_PART_BODY, "link": "", "alpha": 0.4},
                            {"icon": ICON_PART_FUNCTION, "link": "", "alpha": 0.4},
                        ],
                        "arrows": False,
                    },
                ],
            },
            {
                "kind": "entries",
                "title": _t("Finishing, or Stopping Short", "完工，或不完工"),
                "icon": ICON_COMPLETE,
                "entries": [
                    {
                        "icons": [("icon", ICON_COMPLETE)],
                        "title": _t("Declaring It Built", "宣布建成"),
                        "text": _t(
                            "You must reach at least one level above where you started this round, "
                            "then declare the wonder built. Declaring early is allowed and sometimes "
                            "wise: a level 3 wonder you can dedicate now beats a level 6 one you "
                            "cannot afford to keep.",
                            "本轮至少要比起始等级高出一级，然后宣布建成。提前宣布是允许的，有时也明智：一座"
                            "现在就能落成的三级奇观，胜过一个你养不起的六级奇观。",
                        ),
                    },
                    {
                        "icons": [("icon", ICON_CONSTRUCTION)],
                        "title": _t("Continuing a Shell", "续建空壳"),
                        "text": _t(
                            "A wonder whose parts were built but which was never dedicated exists as a "
                            "shell. Building the main structure to level 1 is enough to declare it, "
                            "which lets a later ruler finish what an earlier one started.",
                            "部件已建、却从未落成的奇观会以空壳形式存在。主体建到一级即可宣布建成，于是后来的"
                            "统治者能接手前人未竟之事。",
                        ),
                    },
                    {
                        "icons": [("icon", ICON_WARNING)],
                        "title": _t("Losing the Site", "失去工地"),
                        "text": _t(
                            "If the location changes hands, the project aborts at once and its failure "
                            "cost is paid. The worked stone stays where it is, and a conqueror who "
                            "takes the site can continue it.",
                            "若该地点易主，工程立即中止，并支付失败代价。已砌好的石料留在原处，夺取此地的征服者"
                            "可以续建。",
                        ),
                    },
                ],
            },
        ],
    },
    # ------------------------------------------------------------------- ceremony ----
    {
        "id": "ceremony",
        "filter": "mechanics",
        "icon": ICON_CROWN,
        "title": _t("Dedication", "落成"),
        "lead": _t(
            "A finished wonder is a shell until it is dedicated. Three ritual styles are offered; "
            "each one gives the wonder a different permanent character and a different set of "
            "rewards, and each one costs gold and takes two years.",
            "已建成的奇观在落成之前只是空壳。可供选择三种仪式风格；每一种赋予奇观不同的永久性格与不同的"
            "奖励组合，也各自要花金币、耗时两年。",
        ),
        "sections": [
            {
                "kind": "flow",
                "title": _t("How a Dedication Happens", "落成如何发生"),
                "icon": ICON_CEREMONY,
                "steps": [
                    {
                        "icon": ICON_COMPLETE,
                        "link": LINK_CONSTRUCTION,
                        "title": _t("The Shell", "空壳"),
                        "text": _t(
                            "Built, standing, doing almost nothing. It carries only its cultural "
                            "tradition until it is dedicated.",
                            "已建成、矗立着，却几乎不起作用。落成之前，它只带来文化传统。",
                        ),
                    },
                    {
                        "icon": ICON_IDEA,
                        "link": LINK_CEREMONY,
                        "title": _t("Pick a Style", "选择风格"),
                        "text": _t(
                            "Preview all three for free. Each shows its real completion effect on the "
                            "game's own terms, not a summary.",
                            "三种风格都可免费预览，每一个都以游戏自身的渲染方式显示其真实的完成效果，而非概述。",
                        ),
                    },
                    {
                        "icon": ICON_GOLD,
                        "link": LINK_CEREMONY,
                        "title": _t("Pay and Settle", "付费与结算"),
                        "text": _t(
                            "Confirming charges a size-scaled sum and settles every existing estate's "
                            "satisfaction at once, for or against.",
                            "确认时收取一笔随规模缩放的费用，并当场结算每一个在场阶层的好感，或升或降。",
                        ),
                    },
                    {
                        "icon": ICON_POWER,
                        "link": LINK_CEREMONY,
                        "title": _t("Two Years", "两年"),
                        "text": _t(
                            "The ritual runs 24 months. Support does not decay during it, and the "
                            "style can no longer be changed.",
                            "仪式持续 24 个月。期间支持度不衰减，风格也不能再改。",
                        ),
                    },
                ],
            },
            {
                "kind": "entries",
                "title": _t("What the Styles Have in Common", "三种风格共通之处"),
                "icon": ICON_EFFECT,
                "entries": [
                    {
                        "icons": [("icon", ICON_GOLD)],
                        "title": _t("A Price by Size", "按规模定价"),
                        "text": _t(
                            "#high 2#, #high 3#! or #high 5#! size-scaled sums of gold for a small, "
                            "medium or large wonder. Confirming is the moment it is charged.",
                            "小、中、大奇观分别为 #high 2#!、#high 3#!、#high 5#! 倍缩放金。确认之时即扣款之时。",
                        ),
                    },
                    {
                        "icons": [("icon", ICON_ESTATE)],
                        "title": _t("Estate Satisfaction, Settled Once", "阶层好感，一次结算"),
                        "text": _t(
                            "Every estate that favours your style gains #high 0.10#! satisfaction; "
                            "every estate against it loses #high 0.05#!. Since the three styles "
                            "disagree, some estate always pays.",
                            "支持你选定风格的阶层好感 #high +0.10#!，反对者 #high −0.05#!。既然三种风格彼此对立，"
                            "总会有阶层为此付出。",
                        ),
                    },
                    {
                        "icons": [("icon", ICON_POWER)],
                        "title": _t("A Monthly Societal Pull", "月度价值观倾向"),
                        "text": _t(
                            "After completion, the dedication adds #high 0.1#! monthly pull "
                            "towards the chosen societal direction.",
                            "完成仪式后，沿所选社会价值观方向提供 #high 0.1#! 月度推力。",
                        ),
                    },
                    {
                        "icons": [("icon", ICON_PRESTIGE)],
                        "title": _t("A Memory of a Century", "百年记忆"),
                        "text": _t(
                            "A dedication lasts 100 years, or until the location is lost or the "
                            "building is demolished. A wonder that outlives its dedication falls "
                            "back to plain.",
                            "一次落成持续 100 年，或直到该地易主、建筑被拆。落成过期之后，奇观退回朴素状态。",
                        ),
                    },
                ],
            },
            {
                "kind": "panels",
                "title": _t("Plain, or Dedicated", "朴素，或落成"),
                "icon": ICON_CROWN,
                "panels": [
                    {
                        "title": _t("Plain Inauguration", "朴素启用"),
                        "text": _t(
                            "Immediate, free, and it still pays the completion rewards. Every "
                            "participating estate resents it, and the wonder carries no ritual "
                            "character at all.",
                            "即时、免费，仍照发落成奖励。但每个参与的阶层都对此不满，奇观也完全没有仪式性格。",
                        ),
                        "items": [
                            {"icon": ICON_COMPLETE, "link": "[tv_wonder_ceremony|e]"},
                            {"icon": ICON_ESTATE, "link": ""},
                        ],
                        "arrows": True,
                    },
                    {
                        "title": _t("Dedicated", "仪式落成"),
                        "text": _t(
                            "Two years and a price, and in return the wonder keeps a style, its "
                            "rewards, its societal pull and the estates that backed it.",
                            "两年与一笔费用，换来奇观保有风格、其奖励、其价值牵引，以及支持它的那些阶层。",
                        ),
                        "items": [
                            {"icon": ICON_CEREMONY, "link": "[tv_wonder_ceremony|e]"},
                            {"icon": ICON_EFFECT, "link": ""},
                        ],
                        "arrows": True,
                    },
                ],
            },
            {
                "kind": "text",
                "title": _t("Expanding a Dedicated Wonder", "扩建已落成的奇观"),
                "icon": ICON_EXPANSION,
                "body": _t(
                    "Every expansion offers a fresh choice of all three ritual styles or a plain "
                    "inauguration. The old dedication lasts until completion, when the new choice "
                    "replaces it. A ritual follows the normal cost, duration, estate settlement and rewards.",
                    "每次扩建结束都能重新自由选择三种仪式风格，或选择朴素落成。旧仪式持续到本次落成，"
                    "届时由新选择替代。举行仪式仍按正常规则支付费用、等待完成、结算阶层态度并领取仪式奖励。",
                ),
            },
        ],
    },
    # ------------------------------------------------------------------ expansion ----
    {
        "id": "expansion",
        "filter": "mechanics",
        "icon": ICON_EXPANSION,
        "title": _t("Expansion and Rededication", "扩建与重新仪式"),
        "lead": _t(
            "A finished wonder is not the end of it. It can be raised higher, and a plain one can be "
            "given a dedication it never had.",
            "建成并不是终点。奇观可以继续建高，而朴素状态的奇观也能补上当初没有举行的落成。",
        ),
        "sections": [
            {
                "kind": "entries",
                "title": _t("Two Ways Back In", "两条回头的路"),
                "icon": ICON_EXPANSION,
                "entries": [
                    {
                        "icons": [("icon", ICON_BUILD)],
                        "title": _t("Expansion", "扩建"),
                        "text": _t(
                            "A new construction round on the same site, with its own survey readings "
                            "and its own rewards. Every wonder freely chooses its ritual again at the end.",
                            "在同一工地开启新一轮施工，自带勘测读数与自有奖励。无论原有仪式如何，"
                            "都在结束时重新自由选择仪式。",
                        ),
                    },
                    {
                        "icons": [("icon", ICON_CROWN)],
                        "title": _t("Rededication", "重新仪式"),
                        "text": _t(
                            "A decision available while a project is being conceived. It takes a plain "
                            "wonder straight to the ritual, skipping debate, survey and construction.",
                            "在构思期间可用的一项决议。它把朴素奇观直接送进仪式，跳过辩论、勘测与施工。",
                        ),
                    },
                ],
            },
            {
                "kind": "panels",
                "title": _t("What Each One Pays", "两者各得什么"),
                "icon": ICON_GOLD,
                "panels": [
                    {
                        "title": _t("Expansion", "扩建"),
                        "text": _t(
                            "Full completion rewards every time, and the wonder rises a level. Holding "
                            "a ritual grants its rewards again and replaces the site's previous style; "
                            "a plain inauguration removes the old dedication.",
                            "每次都有完整的落成奖励，奇观等级提升。举行仪式会再次结算其奖励，并替换该地点的旧风格；"
                            "选择朴素落成则移除原有仪式。",
                        ),
                        "items": [
                            {"icon": ICON_BUILD, "link": "[tv_wonder_expansion|e]"},
                            {"icon": ICON_EFFECT, "link": ""},
                        ],
                        "arrows": True,
                    },
                    {
                        "title": _t("Rededication", "重新仪式"),
                        "text": _t(
                            "Only the chosen ritual's rewards. Choosing plain grants no additional rewards.",
                            "仅获得所选仪式的奖励。选择朴素不获得额外奖励。",
                        ),
                        "items": [
                            {"icon": ICON_CEREMONY, "link": "[tv_wonder_ceremony|e]"},
                            {"icon": ICON_EFFECT, "link": ""},
                        ],
                        "arrows": True,
                    },
                ],
            },
        ],
    },
    # --------------------------------------------------------------------- support ----
    {
        "id": "support",
        "filter": "mechanics",
        "icon": ICON_WARNING,
        "title": _t("When a Project Fails", "工程失败时"),
        "lead": _t(
            "Support decays through survey and construction. When it runs dry the court offers one "
            "chance to buy the project back; after that the project is over.",
            "支持度在勘测与施工期间持续衰减。耗尽时朝廷会给一次挽回的机会；再之后，工程即告结束。",
        ),
        "sections": [
            {
                "kind": "flow",
                "title": _t("The Road to Failure", "失败之路"),
                "icon": ICON_WARNING,
                "steps": [
                    {
                        "icon": ICON_ESTATE,
                        "link": LINK_SUPPORT,
                        "title": _t("Support Decays", "支持度衰减"),
                        "text": _t(
                            "Shortly after the debate closes, support starts falling every month. "
                            "Nothing else in the project drains it.",
                            "辩论结束不久，支持度便每月下滑。工程中没有别的东西会消耗它。",
                        ),
                    },
                    {
                        "icon": ICON_WARNING,
                        "link": LINK_SUPPORT,
                        "title": _t("It Reaches Zero", "归零"),
                        "text": _t(
                            "If the project can already be declared built, it is finished instead. "
                            "Otherwise this is where it starts to hurt.",
                            "若工程此时已可宣布建成，就直接收工。否则，这才是开始疼的地方。",
                        ),
                    },
                    {
                        "icon": ICON_GOLD,
                        "link": LINK_ESTATE,
                        "title": _t("One Reprieve", "一次挽救"),
                        "text": _t(
                            "Bribe every estate, or make a public statement. Either way, +50 support "
                            "and the project continues.",
                            "收买所有阶层，或由君主公开表态。两者都给 +50 支持度，工程继续。",
                        ),
                    },
                    {
                        "icon": ICON_STARVE,
                        "link": LINK_SUPPORT,
                        "title": _t("The Second Time", "第二次"),
                        "text": _t(
                            "There is no third. The project ends: the engineer is killed, prestige "
                            "and estate satisfaction are lost with it.",
                            "没有第三次。工程终止：总工程师被处死，威望与阶层好感随之失去。",
                        ),
                    },
                ],
            },
            {
                "kind": "entries",
                "title": _t("The Two Reprieves", "两种挽救"),
                "icon": ICON_GOLD,
                "entries": [
                    {
                        "icons": [("icon", ICON_GOLD)],
                        "title": _t("Bribe the Estates", "收买阶层"),
                        "text": _t(
                            "Twelve months of trade and tax income, split evenly among every estate "
                            "the country has, with a floor of 100 gold. Expensive but immediate.",
                            "相当于十二个月的贸易与税收收入，在本国所有阶层间均分，下限 100 金币。昂贵但立竿见影。",
                        ),
                    },
                    {
                        "icons": [("icon", ICON_POWER)],
                        "title": _t("A Public Statement", "公开表态"),
                        "text": _t(
                            "#high 50 political influence#! and #high 25 prestige#!. Cheaper in gold, "
                            "dearer in the things a ruler cannot simply mint.",
                            "#high 50 政治影响力#! 与 #high 25 威望#!。金币上更便宜，但付出的是君主无法凭空"
                            "铸造的东西。",
                        ),
                    },
                    {
                        "icons": [("icon", ICON_WARNING)],
                        "title": _t("Giving Up", "放弃"),
                        "text": _t(
                            "Abandoning voluntarily costs the same as failing. If the site is already "
                            "lost or the country already bankrupt, sometimes the honest answer is to "
                            "let it go.",
                            "主动放弃的代价与失败相同。若工地已失、国家已破产，有时诚实的答案就是放手。",
                        ),
                    },
                ],
            },
        ],
    },
    # ----------------------------------------------------------------------- sizes ----
    {
        "id": "sizes",
        "filter": "mechanics",
        "icon": ICON_GOLD,
        "title": _t("Project Sizes", "工程规模"),
        "lead": _t(
            "Three sizes, with three different prices, three different rhythms and one important "
            "difference in what you are allowed to do with them afterwards.",
            "三种规模，三种价格、三种节奏，以及一条关于「此后能拿它怎么办」的重要区别。",
        ),
        "sections": [
            {
                "kind": "panels",
                "title": _t("How They Compare", "三者之比"),
                "icon": ICON_GOLD,
                "panels": [
                    {
                        "title": _t("Small", "小型"),
                        "text": _t(
                            "Cheapest per unit and the only size that may be raised more than once. "
                            "Its national effect is limited to moving a value, which keeps it from "
                            "being an infinite economy on its own.",
                            "每单元最便宜，也是唯一可以重复建造的规模。其全国效果仅限于推动某项数值，以免它单独"
                            "成为无限经济。",
                        ),
                        "items": [
                            {"icon": ICON_KIND_SMALL, "link": LINK_SMALL},
                            {"icon": ICON_BUILD, "link": ""},
                        ],
                        "arrows": True,
                    },
                    {
                        "title": _t("Medium and Large", "中型与大型"),
                        "text": _t(
                            "One of each kind per country, no exceptions, with unrestricted national "
                            "and local effects. The budget of a generation for one monument.",
                            "每种每国仅限一座，没有例外，但全国与地方效果不受限制。举一代之力成一座纪念碑。",
                        ),
                        "items": [
                            {"icon": ICON_KIND_MEDIUM, "link": LINK_MEDIUM},
                            {"icon": ICON_KIND_LARGE, "link": LINK_LARGE},
                        ],
                        "arrows": True,
                    },
                ],
            },
            {
                "kind": "text",
                "title": _t("What Size Changes", "规模改变了什么"),
                "icon": ICON_BUILD,
                "body": _t(
                    "$BULLET$ #T Ritual price:#! 2, 3 and 5 scaled gold.\n"
                    "$BULLET$ #T Per-unit cost:#! roughly ten, twenty and thirty thousand gold per "
                    "level in the game's own reference prices.\n"
                    "$BULLET$ #T Progress demand:#! each construction unit asks more of the camp.\n"
                    "$BULLET$ #T Repetition:#! small can be rebuilt elsewhere, medium and large cannot "
                    "be duplicated at all.",
                    "$BULLET$ #T 仪式价格：#!分别为 2、3、5 倍缩放金。\n"
                    "$BULLET$ #T 每单元成本：#!按游戏自带参考价格，每级约为一万、两万、三万金币。\n"
                    "$BULLET$ #T 进度需求：#!每个施工单元对营地的要求更高。\n"
                    "$BULLET$ #T 重复：#!小型可在别处重建，中型与大型完全不可复制。",
                ),
            },
            {
                "kind": "text",
                "title": _t("Choosing a Size", "如何选择规模"),
                "icon": ICON_IDEA,
                "body": _t(
                    "The engineer proposes what the country can support, so the choice is usually "
                    "between a size you can finish and a size you can only start. A large wonder "
                    "abandoned at level 2 is worse than a small one dedicated at level 4: the shell "
                    "does nothing, and the estates remember the failure.\n\n"
                    "Take the large one when you know you are not going to be interrupted: a secure "
                    "capital, a strong treasury, and an engineer who will live through it.",
                    "总工程师只会提出国家承受得起的方案，所以选择通常是「建得完的规模」与「只能开工的规模」之间。"
                    "一座停在二级就放弃的大型奇观，比一座四级落成的小型奇观更糟：空壳不产生任何效果，而阶层"
                    "会记住这次失败。\n\n"
                    "只有在你确定不会被打断时才选大型：稳固的首都、充裕的国库，以及一位能活着看到它完工的"
                    "总工程师。",
                ),
            },
        ],
    },
    # -------------------------------------------------------------------- settings ----
    {
        "id": "settings",
        "filter": "mechanics",
        "icon": ICON_LAW,
        "title": _t("Settings and Tuning", "设置与调整"),
        "lead": _t(
            "The mod ships with a full tuning menu for players who want the monument without the "
            "negotiation. Everything on it is optional and none of it is enabled by default.",
            "本模组带有一整套调整菜单，供想直接要纪念碑、不愿谈判的玩家使用。其中每一项都是可选的，默认全部关闭。",
        ),
        "sections": [
            {
                "kind": "entries",
                "title": _t("What You Can Change", "可以改变什么"),
                "icon": ICON_LAW,
                "entries": [
                    {
                        "icons": [("icon", ICON_IDEA)],
                        "title": _t("Skip the Stages", "跳过阶段"),
                        "text": _t(
                            "Conception, debate and survey can each be completed automatically, and "
                            "construction can be raised straight to level 6. Useful for measuring "
                            "effects, ruinous for the game's tension.",
                            "构想、辩论与勘测均可自动完成，施工也可直接抬到六级。用来测试效果很方便，用来玩则"
                            "毁掉全部张力。",
                        ),
                    },
                    {
                        "icons": [("icon", ICON_SCALE)],
                        "title": _t("Lift the Ceilings", "解除上限"),
                        "text": _t(
                            "Unlimited scale lets any site reach level 6; unlimited organization lets "
                            "any camp reach 20. Together they remove geography as a constraint.",
                            "无限规模让任何地基都能建到六级；无限组织让任何营地都能建到 20 级。两者合用，等于"
                            "把地理从限制条件里删掉。",
                        ),
                    },
                    {
                        "icons": [("icon", ICON_BUILD)],
                        "title": _t("Price and Pace", "价格与节奏"),
                        "text": _t(
                            "Direct construction prices, per-unit progress requirements, and the "
                            "random construction and survey events can all be adjusted or turned off.",
                            "直接建造的价格、每单元进度需求，以及随机的施工与勘测事件，都可调整或关闭。",
                        ),
                    },
                    {
                        "icons": [("icon", ICON_CROWN)],
                        "title": _t("Skip the Ritual", "跳过仪式"),
                        "text": _t(
                            "A style can be chosen and confirmed instantly and for free, for generic "
                            "and unique wonders alike.",
                            "选定风格后可即时免费确认，通用奇观与独特奇观皆然。",
                        ),
                    },
                ],
            },
        ],
    },
    # ------------------------------------------------------------ generic vs unique ----
    {
        "id": "kinds",
        "filter": "mechanics",
        "icon": ICON_CULTURE,
        "title": _t("Generic and Unique Wonders", "通用与独特奇观"),
        "lead": _t(
            "Every wonder in this catalogue is one of two things: an archetype you may site wherever "
            "the ground allows, or a monument that belongs to one place in the world.",
            "本目录中的每一座奇观都属于两类之一：一种是你可在许可地基上自行选址的原型，一种是属于世上唯一"
            "某地的纪念碑。",
        ),
        "sections": [
            {
                "kind": "panels",
                "title": _t("The Trade", "取舍"),
                "icon": ICON_CULTURE,
                "panels": [
                    {
                        "title": _t("Generic", "通用"),
                        "text": _t(
                            "You choose the site, so you can put it where the survey reads highest. "
                            "Small ones repeat, which makes them the reliable way to farm a "
                            "particular reward. The wonder is whatever your country makes of it.",
                            "由你选址，因此可以把它放在勘测读数最高之处。小型可重复建造，是稳定刷取某种奖励的"
                            "可靠方式。奇观是什么，取决于你的国家把它造成什么。",
                        ),
                        "items": [
                            {"icon": ICON_MAP, "link": LINK_GENERIC},
                            {"icon": ICON_SCALE, "link": LINK_SCALE},
                        ],
                        "arrows": True,
                    },
                    {
                        "title": _t("Unique", "独特"),
                        "text": _t(
                            "One place, one owner, one monument. You cannot choose the ground, and "
                            "someone else may hold it before you. In exchange, the base effect is "
                            "multiplied and the reward is worth the wait.",
                            "一地、一主、一座。你无法选择地基，也可能有人先你一步占据它。作为回报，其基础效果"
                            "翻倍，奖励值得等待。",
                        ),
                        "items": [
                            {"icon": ICON_CROWN, "link": LINK_UNIQUE},
                            {"icon": ICON_PRESTIGE, "link": ""},
                        ],
                        "arrows": True,
                    },
                ],
            },
            {
                "kind": "text",
                "title": _t("Historic Wonders at the Start", "开局的历史奇观"),
                "icon": ICON_CROWN,
                "body": _t(
                    "The world begins with many of these monuments already standing, owned by "
                    "whoever holds their location, in the plain state. They give their base effects "
                    "and nothing else until someone dedicates them, which makes a campaign's first "
                    "prize the wonder a neighbour is sitting on.\n\n"
                    "Taking one has its own consequence: the new owner is asked whether to spare it "
                    "as its custodian for prestige, or to strip it for gold at the cost of one level.",
                    "开局时世上已有许多这样的纪念碑矗立着，归其所在地的持有者所有，处于朴素状态。它们只提供"
                    "基础效果，直到有人为它举行落成仪式；于是战役里最早的一块肥肉，往往就是邻国正坐着的那座。\n\n"
                    "夺取它自有代价：新主人要决定是保留它、以守护者之名换取威望，还是拆走珍宝换取金币，代价是降低一级。",
                ),
            },
        ],
    },
]
