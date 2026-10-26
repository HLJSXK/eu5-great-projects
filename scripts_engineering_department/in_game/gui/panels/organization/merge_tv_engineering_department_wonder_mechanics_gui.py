import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

REPO_ROOT = Path(__file__).resolve().parents[5]
MAIN_FILE = REPO_ROOT / "src" / "in_game" / "gui" / "panels" / "organization" / "tv_engineering_department.gui"
FRAGMENT_FILE = REPO_ROOT / "data" / "generated_fragments" / "tv_engineering_department_wonder_mechanics.gui"

MARKERS = [
    "TV_WONDER_RITUAL_TYPES",
    "TV_WONDER_MECHANICS_PREVIEW_WIDGETS",
    "TV_WONDER_MECHANICS_PROPOSAL_TEXTS",
    "TV_WONDER_MECHANICS_PROPOSAL_RESUME_TEXTS",
    "TV_WONDER_MECHANICS_PROPOSAL_EXPAND_TEXTS",
    "TV_WONDER_MECHANICS_LOCKED_TEXTS",
    "TV_WONDER_MECHANICS_SUITABILITY_LOCATION_CONDITIONS_TYPE",
    "TV_WONDER_MECHANICS_SUITABILITY_KNOWLEDGE",
    "TV_WONDER_MECHANICS_PROPOSAL_BUTTONS",
    "TV_WONDER_MECHANICS_PRIORITY_CANDIDATES",
    "TV_WONDER_RITUAL_CARD",
]




def extract_fragment(marker: str, fragment: str) -> str:
    pattern = re.compile(
        rf"### BEGIN {re.escape(marker)}\n(.*?)\n### END {re.escape(marker)}",
        re.DOTALL,
    )
    match = pattern.search(fragment)
    if not match:
        raise ValueError(f"Missing fragment marker {marker}")
    return match.group(1).rstrip()


def indent_block(block: str, indent: str) -> str:
    return "\n".join(f"{indent}{line}" if line.strip() else "" for line in block.splitlines())


def replace_generated_segment(text: str, marker: str, block: str) -> str:
    begin = f"# BEGIN GENERATED {marker}"
    end = f"# END GENERATED {marker}"
    pattern = re.compile(
        rf"(?P<prefix>^|\n)(?P<indent>[ \t]*){re.escape(begin)}[ \t]*\n.*?[ \t]*{re.escape(end)}(?=\n|$)",
        re.DOTALL,
    )
    matches = list(pattern.finditer(text))
    if not matches:
        raise ValueError(f"Generated marker {marker} not found in {MAIN_FILE.relative_to(REPO_ROOT)}")

    def replacement(match: re.Match[str]) -> str:
        prefix = match.group("prefix")
        indent = match.group("indent")
        if not indent:
            previous_line_start = text.rfind("\n", 0, match.start())
            previous_line = text[previous_line_start + 1:match.start()] if previous_line_start != -1 else ""
            previous_indent = re.match(r"[ \t]*", previous_line).group(0)
            if previous_line.strip():
                indent = previous_indent
        return f"{prefix}{indent}{begin}\n{indent_block(block, indent)}\n{indent}{end}"

    return pattern.sub(replacement, text)














def normalize_marker_newlines(text: str) -> str:
    text = re.sub(r"(?m)^[ \t]+$", "", text)
    text = re.sub(r"([^\s])([ \t]*# BEGIN GENERATED)", r"\1\n\2", text)
    text = re.sub(r"(# END GENERATED [A-Z0-9_]+)(?=[ \t]*# BEGIN GENERATED)", r"\1\n", text)
    return text


def main() -> None:
    text = MAIN_FILE.read_text(encoding="utf-8")
    fragment = FRAGMENT_FILE.read_text(encoding="utf-8")
    text = normalize_marker_newlines(text)
    for marker in MARKERS:
        text = replace_generated_segment(text, marker, extract_fragment(marker, fragment))
    text = normalize_marker_newlines(text)
    MAIN_FILE.write_text(text, encoding="utf-8", newline="\n")
    print(f"Merged {FRAGMENT_FILE.relative_to(REPO_ROOT)} into {MAIN_FILE.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
