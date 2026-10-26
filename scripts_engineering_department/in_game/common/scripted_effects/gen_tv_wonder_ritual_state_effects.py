"""Generate the unified ritual runtime from canonical wonder data."""
import sys
from pathlib import Path
REPO_ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(REPO_ROOT / "scripts_engineering_department"))
from wonder_mechanics.io import load_all_wonder_mechanics
from wonder_mechanics.render import render_header
from wonder_localization_lib import load_yaml, WONDER_LOCALIZATION_FILE
from wonder_ritual_codegen import state_effects, phase_effects, reritual_effects, triggers, actions, prices, lifecycle_events, message_localization
from in_game.common.scripted_effects.gen_tv_engineering_department_wonder_mechanics_effects import reward_effect_lines, location_tooltip_reward_effect_lines
SCRIPT_REL = "scripts_engineering_department/in_game/common/scripted_effects/gen_tv_wonder_ritual_state_effects.py"
DATA_REL = "data/wonders.yaml + data/unique_wonders.yaml + data/wonder_generic_rituals.yaml + data/wonder_ritual_rules.yaml + data/wonder_societal_axes.yaml"

def outputs():
    wonders, mechanics = load_all_wonder_mechanics()
    header = "\n".join(render_header(SCRIPT_REL, DATA_REL)) + "\n"
    result = {
        "in_game/common/scripted_effects/tv_wonder_ritual_state_effects.txt": header + state_effects(wonders, mechanics, reward_effect_lines, location_tooltip_reward_effect_lines),
        "in_game/common/scripted_effects/tv_wonder_ritual_phase_effects.txt": header + phase_effects(wonders, mechanics) + reritual_effects(wonders, mechanics),
        "in_game/common/scripted_triggers/tv_wonder_ritual_triggers.txt": header + triggers(mechanics, wonders),
        "in_game/common/generic_actions/tv_wonder_ritual_actions.txt": header + actions(),
        "in_game/common/prices/tv_wonder_ritual_prices.txt": header + prices(mechanics),
        "in_game/events/tv_wonder_ritual_lifecycle_events.txt": header + lifecycle_events(wonders, mechanics),
    }
    localization = load_yaml(WONDER_LOCALIZATION_FILE)['wonder_localization']
    for language in ("english", "simp_chinese", "french", "german", "spanish", "russian", "polish", "japanese", "korean", "braz_por", "turkish"):
        result[f"main_menu/localization/{language}/tv_wonder_ritual_messages_l_{language}.yml"] = message_localization(language, localization)
    return {
        relative: '\n'.join(line.rstrip() for line in content.splitlines()).rstrip() + '\n'
        for relative, content in result.items()
    }


def main():
    for relative, content in outputs().items():
        path = REPO_ROOT / "src" / relative
        path.write_text(content, encoding="utf-8-sig", newline="\n")
        print(f"Wrote {path.relative_to(REPO_ROOT)}")

if __name__ == "__main__": main()
