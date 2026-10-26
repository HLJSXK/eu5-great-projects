from ._core import (
    indent_script_block,
    level_static_modifier_loc,
    loc_line,
    monthly_country_pulse_event,
    monthly_country_pulse_event_delay_days,
    q,
    render_header,
    upper_key,
)


def variable_map_key_trigger(name: str, key: str | int) -> str:
    """Check a possibly absent map without evaluating its key lookup first."""
    return (
        f"trigger_if = {{ limit = {{ has_variable_map = {name} }} "
        f"is_key_in_variable_map = {{ name = {name} target = {key} }} }} "
        "trigger_else = { always = no }"
    )
