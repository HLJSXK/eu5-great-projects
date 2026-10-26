"""Find physical carrier declarations and operations, retaining source spans.

Setup includes are recorded as provenance, not expanded or resolved for overrides.
An include-only bookmark can reuse instances defined under another bookmark; a
zero local declaration count does not imply that the bookmark loads no carriers.
"""

from collections import Counter
from dataclasses import dataclass, field
from functools import lru_cache
import re

from wonder_mechanics._core import load_unique_wonders_source_data
from .parse import REFERENCE, Node, Source, walk


@dataclass
class Carrier:
    wonder: dict
    declaration: dict
    startup: list = field(default_factory=list)
    definition: tuple | None = None

    @property
    def key(self):
        return self.declaration["key"]

    @property
    def kind(self):
        return self.declaration["kind"]

    @property
    def level(self):
        return self.declaration.get("present_at_level", 1 if self.startup else self.wonder["initial_level"] + 1)


@dataclass
class Site:
    source: Source
    definition: Node
    node: Node
    carrier: Carrier
    form: str
    ancestors: tuple = ()
    op: str = ""
    location: str = ""
    status: str = "未处理"

    @property
    def path(self):
        return "/".join(n.key for n in (*self.ancestors, self.node))

    @property
    def line(self):
        return self.source.line(self.node)

    @property
    def site_id(self):
        return self.definition.key


@dataclass
class Scan:
    carriers: dict[str, Carrier]
    sources: list[Source]
    sites: list[Site]
    setup_includes: dict[str, list[str]]


def _art_in(node, declared):
    return [c for c in declared.values() if c.kind == "art" and any(
        n.value == f"work_of_art:{c.key}" for n, _ in walk(node)
    )]


def _building(value):
    return value.removeprefix("building_type:")


def _classify(node, ancestors, carriers):
    """Return (carrier, form, operation) for one whole rewritable statement."""
    key, value = node.key, node.value.strip('"')
    if node.children:
        art = carriers.get(node.scalar("key"))
        if art and art.kind == "art":
            return art, "write", "raise"
        if key in {"construct_building", "change_building_level_in_location"}:
            c = carriers.get(_building(node.scalar("building_type") or node.scalar("building")))
            if c and c.kind == "building":
                if key == "construct_building":
                    return c, "write", "raise"
                value_node = node.child("value")
                if not value_node or not re.fullmatch(r"-?\d+(?:\.\d+)?", value_node.value):
                    raise ValueError(f"Nonliteral building level change for {c.key}")
                return c, "write", "raise" if float(value_node.value) > 0 else "lower"
        if key in {"location_building_level", "any_buildings_in_location"}:
            c = carriers.get(_building(node.scalar("building_type")))
            if c and c.kind == "building":
                return c, "level" if key == "location_building_level" else "max", ""
        if key in {"any_work_of_art_in_location", "random_work_of_art_in_location"}:
            cs = _art_in(node, carriers)
            if cs:
                if len(cs) != 1:
                    raise ValueError("Multiple declared artworks in one iterator need an explicit rule")
                return cs[0], "keep" if key.startswith("random_") else "art_here", ""
        if key.startswith("work_of_art:"):
            c = carriers.get(key.split(":", 1)[1])
            if c:
                owned = len(node.children) == 1 and node.children[0].key == "owner" and node.children[0].value.lower() == "root"
                return c, "art_owned" if owned else "art_scope", ""
        if key.startswith("add_") and key.endswith("_modifier"):
            c = carriers.get(node.scalar("modifier"))
            if c and c.kind == "modifier":
                return c, "write", c.declaration["op"]
    elif key in {"destroy_building", "destroy_building_forcefully"}:
        for c in carriers.values():
            if c.kind == "building" and re.search(r"\bbuilding_type:" + re.escape(c.key) + r"\b", value):
                return c, "write", "lower"
    elif key in {"has_building", "has_building_with_at_least_one_level"}:
        c = carriers.get(_building(value))
        if c and c.kind == "building":
            return c, "has", ""
    elif key.startswith("total_effective_building_levels:"):
        c = carriers.get(key.split(":", 1)[1])
        if c:
            return c, "owned", ""
    elif key in {"exists", "destroy_art"} and value.startswith("work_of_art:"):
        c = carriers.get(value.split(":", 1)[1])
        if c:
            return c, "anywhere" if key == "exists" else "write", "" if key == "exists" else "lower"
    elif key in carriers and carriers[key].kind == "effect" and value == "yes":
        c = carriers[key]
        return c, "write", c.declaration["op"]
    if value.startswith(("work_of_art:", "building_type:")):
        c = carriers.get(value.split(":", 1)[1])
        # Advances only unlock a sealed building; section 6.2 explicitly keeps them.
        if c and key != "unlock_building":
            return c, "unsupported", ""
    return None


@lru_cache(maxsize=1)
def scan_reference():
    wonders = load_unique_wonders_source_data()["unique_wonders"]
    carriers = {d["key"]: Carrier(w, d) for w in wonders for d in w.get("vanilla_carriers", [])}
    pattern = re.compile(r"\b(?:" + "|".join(re.escape(k) for k in carriers) + r")\b")
    paths = sorted({*REFERENCE.glob("in_game/events/**/*.txt"), *REFERENCE.glob("in_game/common/**/*.txt"), *REFERENCE.glob("main_menu/setup/*/**/*.txt"), *REFERENCE.glob("main_menu/common/static_modifiers/**/*.txt")})
    sources, sites = [], []
    setup_includes = {}
    art_defined = set()
    for path in paths:
        text = path.read_text(encoding="utf-8-sig")
        relative = path.relative_to(REFERENCE).as_posix()
        if relative.startswith("main_menu/setup/") and "include" in text:
            from .parse import parse
            includes = [n.value.strip('"') for n in parse(text) if n.key == "include"]
            if includes:
                setup_includes[relative] = includes
        if not pattern.search(text):
            continue
        source = Source(path.relative_to(REFERENCE).as_posix(), text, [])
        from .parse import parse
        source.nodes = parse(text)
        sources.append(source)
        for definition in source.definitions:
            c = carriers.get(definition.key)
            if c and ((c.kind == "building" and "/building_types/" in source.path)
                      or (c.kind == "effect" and (definition.declaration == "scripted_effect" or "/scripted_effects/" in source.path))
                      or (c.kind == "modifier" and "/static_modifiers/" in source.path)):
                if c.definition:
                    raise ValueError(f"Duplicate reference carrier definition: {c.key}")
                c.definition = (source, definition)
            if "/building_types/" in source.path:
                continue
            covered = -1
            for node, ancestors in walk(definition):
                if node.start < covered:
                    continue
                if source.path.startswith("main_menu/setup/"):
                    if source.path.endswith("/11_art.txt"):
                        c = carriers.get(node.scalar("key"))
                        if not c or c.kind != "art":
                            continue
                        art_defined.add(c.key)
                    elif source.path.endswith("/07_cities_and_buildings.txt"):
                        c = carriers.get(node.key)
                        if not c or c.kind != "building" or not node.child("location"):
                            continue
                    else:
                        continue
                    site = Site(source, definition, node, c, "startup", ancestors, location=node.scalar("location"))
                    sites.append(site)
                    c.startup.append(site)
                    covered = node.end
                    continue
                result = _classify(node, ancestors, carriers)
                if result:
                    c, form, op = result
                    if form == "write" and c.kind == "art":
                        art_defined.add(c.key)
                    site = Site(source, definition, node, c, form, ancestors, op)
                    sites.append(site)
                    covered = node.end
    for c in carriers.values():
        if c.kind == "art":
            if c.key not in art_defined:
                raise ValueError(f"Artwork carrier absent from reference: {c.key}")
        elif not c.definition:
            raise ValueError(f"{c.kind} carrier absent from reference: {c.key}")
        if c.startup and c.wonder["initial_level"] == 0:
            raise ValueError(f"Startup carrier has zero ED initial level: {c.key}")
    return Scan(carriers, sources, sites, setup_includes)


def site_counts(scan):
    return Counter((s.carrier.key, s.site_id, s.form) for s in scan.sites)
