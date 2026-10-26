"""Lossless rewrites of declared operations, and closure copying of event helpers."""

from collections import Counter
from dataclasses import dataclass
from functools import lru_cache
import re

from .parse import Node, Source, splice, walk
from .render import name
from .scan import scan_reference


def present(site, scope, n=1):
    has_building = any(carrier.kind == "building" and carrier.wonder["key"] == site.carrier.wonder["key"]
                       for carrier in scan_reference().carriers.values())
    return f"{name(site.carrier.wonder, f'present_{scope}_trigger')} = {{ ed_level = {site.carrier.level + n - 1}" + (f" vanilla_level = {n}" if has_building else "") + " }"


def indentation(source, node):
    prefix = source.text[source.text.rfind("\n", 0, node.start) + 1:node.start]
    return re.match(r"[ \t]*", prefix)[0]


def _location_scope(site):
    scopes = {"capital", "any_owned_location", "every_owned_location", "random_owned_location", "scope:target_location"}
    return any(a.key.startswith("location:") or a.key in scopes for a in site.ancestors)


def replacement(site, helpers=None):
    source, node, c = site.source, site.node, site.carrier
    raw = source.raw(node)
    indent = indentation(source, node)
    if site.form == "keep":
        return None
    if site.form == "startup":
        return None
    if site.form == "write":
        gate = name(c.wonder, "gate_trigger")
        call = name(c.wonder, f"{site.op}_effect")
        guard = f"if = {{\n{indent}\tlimit = {{ {gate} = yes }}\n{indent}\t{call} = yes\n{indent}}}"
        if c.declaration["mode"] == "replace":
            return f"{guard}\n{indent}else = {{\n{indent}{raw}\n{indent}}}"
        if helpers and node.key in helpers:
            raw = helpers[node.key] + raw[len(node.key):]
        return raw + f"\n{indent}" + guard
    if site.form == "art_scope":
        return raw.replace("=", "?=", 1) if node.op == "=" else None
    if site.form == "anywhere":
        return present(site, "anywhere")
    if site.form == "art_owned":
        if node.op != "?=" or not any(a.key == "trigger" for a in site.ancestors):
            raise ValueError(f"Unsupported art owner scope: {site.site_id}:{site.line}")
        return present(site, "owned")
    if site.form == "owned":
        if (node.op, node.value) in {(">", "0"), (">=", "1")}:
            return present(site, "owned")
        if (node.op, node.value) == ("<", "1"):
            return "NOT = { " + present(site, "owned") + " }"
        raise ValueError(f"Unsupported owned building read: {raw}")
    if not _location_scope(site):
        raise ValueError(f"Cannot establish location read scope: {site.site_id}:{site.line} {site.path}")
    if site.form == "has":
        return present(site, "here")
    if site.form == "level":
        threshold = node.child("value")
        if not threshold or threshold.op not in {">", ">="} or not re.fullmatch(r"\d+", threshold.value):
            raise ValueError(f"Unsupported building threshold: {raw}")
        return present(site, "here", int(threshold.value) + (threshold.op == ">"))
    if site.form == "max":
        if {n.key for n in node.children} != {"building_type", "is_at_max_level"} or node.scalar("is_at_max_level") != "yes":
            raise ValueError(f"Unsupported max-level iterator: {raw}")
        maximum = c.definition[1].scalar("max_levels")
        if not maximum.isdigit():
            raise ValueError(f"Nonliteral max_levels for {c.key}")
        return present(site, "here", int(maximum))
    if site.form == "art_here":
        children = node.children
        if len(children) == 1 and children[0].key == "OR":
            children = children[0].children
        if not children or any(n.key != "this" or n.op not in {"=", "?="} or not n.value.startswith("work_of_art:") for n in children):
            raise ValueError(f"Unsupported art iterator: {raw}")
        others = [source.raw(n) for n in children if n.value != f"work_of_art:{c.key}"]
        if not others:
            return present(site, "here")
        inner = others[0] if len(others) == 1 else "OR = { " + " ".join(others) + " }"
        return f"OR = {{ {present(site, 'here')} any_work_of_art_in_location = {{ {inner} }} }}"
    raise ValueError(f"Unknown read form: {site.form}")


@dataclass
class Copy:
    source: Source
    definition: Node
    text: str
    edits: list


@dataclass
class Copies:
    events: str
    decisions: str
    records: list[Copy]


def _copy_definition(source, definition, sites, helpers):
    raw = source.raw(definition)
    edits, occupied = [], []
    for site in sites:
        replacement_text = replacement(site, helpers)
        site.status = "保持" if site.form == "keep" else "改写"
        if replacement_text is not None:
            edits.append((site.node.start - definition.start, site.node.end - definition.start, replacement_text))
            occupied.append((site.node.start, site.node.end))
    for node, _ in walk(definition):
        if node.key not in helpers or any(a <= node.start < b for a,b in occupied):
            continue
        if node is definition and node.declaration:
            begin = re.search(r"\b" + re.escape(node.key) + r"\s*=", source.text[node.start:node.opening]).start() + node.start
        else:
            begin = node.start
        edits.append((begin - definition.start, begin - definition.start + len(node.key), helpers[node.key]))
    modified = splice(raw, edits)
    if "/decisions/" in source.path:
        modified = "REPLACE:" + modified
    return Copy(source, definition, modified, sorted(edits))


@lru_cache(maxsize=1)
def copies():
    scan = scan_reference()
    groups = {}
    for site in scan.sites:
        if site.form == "startup":
            continue
        key = (site.source.path, site.definition.start)
        groups.setdefault(key, (site.source, site.definition, []))[2].append(site)
    records = []
    for source in scan.sources:
        selected = {start: entry for (path, start), entry in groups.items() if path == source.path}
        if not selected:
            continue
        local = {n.key: n for n in source.definitions if n.declaration}
        required = set()
        pending = [entry[1] for entry in selected.values()]
        while pending:
            definition = pending.pop()
            for node, _ in walk(definition):
                if node is definition:
                    continue
                if node.key in local and node.key not in required:
                    required.add(node.key)
                    pending.append(local[node.key])
        helpers = {key: "tv_vw_" + key for key in required}
        for key in required:
            node = local[key]
            selected.setdefault(node.start, (source, node, []))
        for _, (src, definition, sites) in sorted(selected.items()):
            if not definition.declaration:
                if "/events/" in src.path:
                    if definition.scalar("type") != "country_event":
                        raise ValueError(f"Non-country event root: {definition.key}")
                elif "/decisions/" not in src.path:
                    raise ValueError(f"Unsupported carrier entry: {src.path}:{definition.key}")
            counts = Counter()
            for site in sites:
                if site.form != "write":
                    continue
                effect = next((a for a in reversed(site.ancestors) if a.key in {"effect", "option", "immediate", "after"}), definition)
                counts[(effect.start, site.carrier.wonder["key"])] += 1
            if any(n > 1 for n in counts.values()):
                raise ValueError(f"Multiple writes to one wonder in one effect: {definition.key}")
            records.append(_copy_definition(src, definition, sites, helpers))
    event_groups = {}
    decisions = []
    for record in records:
        if "/decisions/" in record.source.path:
            decisions.append(record.text)
        else:
            event_groups.setdefault(record.definition.namespace, []).append(record.text)
    events = "\n\n".join(f"namespace = {ns}\n\n" + "\n\n".join(blocks) for ns, blocks in sorted(event_groups.items()))
    return Copies(events, "\n\n".join(decisions), records)
