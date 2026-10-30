"""Explicit, content-bound localization provenance; game YAML stays untouched.

Use register after editing the owning source and regenerating its outputs.
Unchanged records survive bulk registration, including stronger human grades.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
from scripts.localization_policy import LOCALIZATION_GRADES, LOCALIZATION_GRADE_RANK

REGISTRY = "data/localization_grades.json"
ENTRY = re.compile(r'^\s*([A-Za-z0-9_.-]+):\d*\s*"(.*)"\s*(?:#.*)?$')
ORIGINAL_BASES = ("user_manual", "user_requested")


def fingerprint(value: str | None) -> str | None:
    return None if value is None else hashlib.sha256(value.encode("utf-8")).hexdigest()


def make_record(value: str | None, grade: str, *, original_basis: str = "", note: str = "") -> dict:
    if grade not in LOCALIZATION_GRADES:
        raise ValueError(f"Unknown localization grade: {grade}")
    if value is None and grade != "缺失":
        raise ValueError("Absent text must be registered as 缺失")
    if grade == "缺失" and value not in (None, ""):
        raise ValueError("Non-empty text cannot be registered as 缺失")
    record = {"grade": grade, "sha256": fingerprint(value)}
    if grade == "原创":
        if original_basis not in ORIGINAL_BASES or not note.strip():
            raise ValueError("原创 requires user_manual or user_requested and a factual note")
        record.update(original_basis=original_basis, note=note.strip())
    elif original_basis or note:
        raise ValueError("Original provenance evidence is only valid for 原创")
    return record


def load_registry(repo_root: Path, *, raw: bytes | None = None) -> dict:
    path = repo_root / REGISTRY
    data = json.loads((path.read_bytes() if raw is None else raw).decode("utf-8"))
    if not isinstance(data, dict) or data.get("version") != 1 or not isinstance(data.get("files"), dict):
        raise ValueError(f"Invalid localization grade registry: {REGISTRY}")
    for relative, entries in data["files"].items():
        candidate = Path(relative)
        if candidate.is_absolute() or ".." in candidate.parts or "\\" in relative:
            raise ValueError(f"Invalid registry path: {relative}")
        if not isinstance(entries, dict):
            raise ValueError(f"Invalid registry entries: {relative}")
        for key, record in entries.items():
            if not isinstance(record, dict) or record.get("grade") not in LOCALIZATION_GRADES:
                raise ValueError(f"Invalid grade: {relative}:{key}")
            digest = record.get("sha256")
            if "sha256" not in record or (digest is not None and
                    (not isinstance(digest, str) or re.fullmatch(r"[0-9a-f]{64}", digest) is None)):
                raise ValueError(f"Invalid text fingerprint: {relative}:{key}")
            if record["grade"] == "原创" and (
                record.get("original_basis") not in ORIGINAL_BASES or
                not isinstance(record.get("note"), str) or not record["note"].strip()
            ):
                raise ValueError(f"原创 lacks user provenance: {relative}:{key}")
    return data


def registry_bytes(data: dict) -> bytes:
    # One record per line gives small, reviewable diffs even for a large corpus.
    lines = ['{', '  "version": 1,', '  "files": {']
    files = sorted(data["files"].items())
    for index, (path, entries) in enumerate(files):
        lines.append(f'    {json.dumps(path, ensure_ascii=False)}: {{')
        items = sorted(entries.items())
        for i, (key, record) in enumerate(items):
            lines.append(f'      {json.dumps(key, ensure_ascii=False)}: '
                         + json.dumps(record, ensure_ascii=False)
                         + ("," if i + 1 < len(items) else ""))
        lines.append('    }' + ("," if index + 1 < len(files) else ""))
    return ("\n".join([*lines, '  }', '}']) + "\n").encode("utf-8")


def discover_files(repo_root: Path) -> list[Path]:
    roots = [repo_root / "src", *sorted((repo_root / "submods").glob("*"))]
    return sorted(path for root in roots for path in
                  (root / "main_menu/localization").rglob("*.yml") if path.is_file())


def read_entries(path: Path) -> dict[str, str]:
    entries = {}
    header = False
    for number, line in enumerate(path.read_text(encoding="utf-8-sig").splitlines(), 1):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if re.fullmatch(r"l_[a-z_]+:\s*", line.strip()):
            header = True
            continue
        match = ENTRY.fullmatch(line)
        if not match or not header:
            raise ValueError(f"Malformed localization: {path}:{number}")
        key, value = match.groups()
        if key in entries:
            raise ValueError(f"Duplicate localization key: {path}:{key}")
        entries[key] = value
    if not header:
        raise ValueError(f"Missing language header: {path}")
    return entries


def entry_status(data: dict, path: str, key: str, value: str | None) -> dict:
    record = data["files"].get(path, {}).get(key)
    if value is None:
        return {"grade": "缺失", "grade_rank": 1, "grade_status": "missing"}
    if record is None:
        return {"grade": None, "grade_rank": None, "grade_status": "unregistered"}
    if record["sha256"] != fingerprint(value):
        return {"grade": None, "grade_rank": None, "grade_status": "stale"}
    return {"grade": record["grade"], "grade_rank": LOCALIZATION_GRADE_RANK[record["grade"]],
            "grade_status": "registered"}


def check_registry(repo_root: Path) -> list[str]:
    try:
        data = load_registry(repo_root)
        current = {p.relative_to(repo_root).as_posix(): read_entries(p) for p in discover_files(repo_root)}
    except (OSError, ValueError) as exc:
        return [str(exc)]
    errors = []
    for path, entries in current.items():
        for key, value in entries.items():
            status = entry_status(data, path, key, value)["grade_status"]
            if status != "registered":
                errors.append(f"{path}: {key}: {status}; register the actual grade for the current text")
            elif data["files"][path][key]["grade"] == "缺失" and value:
                errors.append(f"{path}: {key}: non-empty text marked 缺失")
    for path, entries in data["files"].items():
        for key, record in entries.items():
            if key not in current.get(path, {}) and (record["grade"] != "缺失" or record["sha256"] is not None):
                errors.append(f"{path}: {key}: deleted text still has a grade; use prune")
    return errors


def register_entries(data: dict, path: str, entries: dict[str, str], grade: str, *,
                     keys: list[str] | None = None, replace: bool = False,
                     original_basis: str = "", note: str = "") -> int:
    records = data["files"].setdefault(path, {})
    count = 0
    for key in keys if keys is not None else entries:
        value = entries.get(key)
        record = make_record(value, grade, original_basis=original_basis, note=note)
        # Bulk updates must never turn unchanged original text into AI/translation.
        if not replace and key in records and records[key]["sha256"] == fingerprint(value):
            continue
        if records.get(key) != record:
            records[key] = record
            count += 1
    return count


def main(argv: list[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("initialize", help="One-time user-approved EN/ZH AI生成, other languages 翻译 inventory")
    commands.add_parser("check")
    commands.add_parser("summary")
    commands.add_parser("prune", help="Remove records for deleted keys/files after regeneration")
    register = commands.add_parser("register")
    register.add_argument("--files", nargs="+", required=True)
    register.add_argument("--keys", nargs="+")
    register.add_argument("--grade", choices=LOCALIZATION_GRADES, required=True)
    register.add_argument("--replace", action="store_true", help="Explicitly regrade unchanged text")
    register.add_argument("--original-basis", choices=ORIGINAL_BASES, default="")
    register.add_argument("--note", default="")
    args = parser.parse_args(argv)
    destination = REPO_ROOT / REGISTRY
    try:
        if args.command == "check":
            errors = check_registry(REPO_ROOT)
            print("\n".join(errors) if errors else "All localization grades are registered and current.")
            return int(bool(errors))
        if args.command == "initialize":
            if destination.exists():
                raise ValueError("Registry already exists; initialization cannot overwrite existing grades")
            data = {"version": 1, "files": {}}
            for path in discover_files(REPO_ROOT):
                language = path.relative_to(REPO_ROOT).parts[path.relative_to(REPO_ROOT).parts.index("localization") + 1]
                register_entries(data, path.relative_to(REPO_ROOT).as_posix(), read_entries(path),
                                 "AI生成" if language in ("english", "simp_chinese") else "翻译")
        else:
            data = load_registry(REPO_ROOT)
            if args.command == "summary":
                counts = Counter()
                for path in discover_files(REPO_ROOT):
                    for key, value in read_entries(path).items():
                        status = entry_status(data, path.relative_to(REPO_ROOT).as_posix(), key, value)
                        counts[status["grade"] or status["grade_status"]] += 1
                print(json.dumps({g: counts[g] for g in (*LOCALIZATION_GRADES, "unregistered", "stale")}, ensure_ascii=False))
                return 0
            if args.command == "prune":
                current = {p.relative_to(REPO_ROOT).as_posix(): read_entries(p) for p in discover_files(REPO_ROOT)}
                data["files"] = {p: {k: r for k, r in rows.items() if k in current[p]}
                                 for p, rows in data["files"].items() if p in current}
            elif args.command == "register":
                allowed = set(discover_files(REPO_ROOT))
                for name in args.files:
                    path = (REPO_ROOT / name).resolve()
                    if path not in allowed:
                        raise ValueError(f"Not a workspace localization file: {name}")
                    register_entries(data, path.relative_to(REPO_ROOT).as_posix(), read_entries(path), args.grade,
                                     keys=args.keys, replace=args.replace, original_basis=args.original_basis, note=args.note)
        destination.parent.mkdir(parents=True, exist_ok=True)
        temporary = destination.with_suffix(".json.tmp")
        temporary.write_bytes(registry_bytes(data))
        temporary.replace(destination)
        print(f"Updated {REGISTRY}")
        return 0
    except (OSError, ValueError) as exc:
        parser.error(str(exc))


if __name__ == "__main__":
    raise SystemExit(main())
