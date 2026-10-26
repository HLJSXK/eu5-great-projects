"""Small, source-preserving Jomini parser; offsets always refer to the original text."""

from dataclasses import dataclass, field
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
REFERENCE = ROOT / ".eu5-base/reference_game_files/game"
TOKEN = re.compile(r'"(?:\\.|[^"\\])*"|\#[^\n]*|[{}]|\?=|>=|<=|!=|=|>|<|[^\s{}=<>!?#"]+')
OPS = {"=", "?=", ">=", "<=", "!=", ">", "<"}


@dataclass
class Node:
    key: str
    op: str
    value: str
    start: int
    end: int
    children: list = field(default_factory=list)
    opening: int | None = None
    closing: int | None = None
    declaration: str = ""
    namespace: str = ""

    def child(self, key):
        return next((n for n in self.children if n.key == key), None)

    def scalar(self, key, default=""):
        child = self.child(key)
        return child.value.strip('"') if child else default


def parse(text: str) -> list[Node]:
    tokens = [m for m in TOKEN.finditer(text) if not m[0].startswith("#")]
    pos = 0

    def level(nested=False):
        nonlocal pos
        nodes = []
        while pos < len(tokens):
            token = tokens[pos]
            if token[0] == "}":
                if not nested:
                    raise ValueError(f"Unexpected closing brace at {token.start()}")
                break
            start = token.start()
            declaration = ""
            key = token[0]
            pos += 1
            if key in {"scripted_effect", "scripted_trigger"} and pos < len(tokens) and tokens[pos][0] not in OPS:
                declaration, key = key, tokens[pos][0]
                pos += 1
            if pos >= len(tokens) or tokens[pos][0] not in OPS:
                if key == "{":
                    children = level(True)
                    if pos >= len(tokens):
                        raise ValueError("Unclosed anonymous block")
                    end = tokens[pos].end()
                    pos += 1
                    nodes.append(Node("", "", "", start, end, children, start, end - 1))
                else:
                    nodes.append(Node(key, "", "", start, token.end()))
                continue
            op = tokens[pos][0]
            pos += 1
            if pos >= len(tokens):
                raise ValueError(f"Missing value for {key}")
            value = tokens[pos]
            pos += 1
            if value[0] == "{":
                children = level(True)
                if pos >= len(tokens):
                    raise ValueError(f"Unclosed block {key}")
                close = tokens[pos]
                pos += 1
                nodes.append(Node(key, op, "", start, close.end(), children, value.start(), close.start(), declaration))
            else:
                nodes.append(Node(key, op, value[0], start, value.end(), declaration=declaration))
        return nodes

    nodes = level()
    namespace = ""
    for node in nodes:
        if node.key == "namespace":
            namespace = node.value
        node.namespace = namespace
    return nodes


def walk(node, ancestors=()):
    yield node, ancestors
    for child in node.children:
        yield from walk(child, (*ancestors, node))


@dataclass
class Source:
    path: str
    text: str
    nodes: list[Node]

    @classmethod
    def read(cls, path, root=REFERENCE):
        text = path.read_text(encoding="utf-8-sig")
        return cls(path.relative_to(root).as_posix(), text, parse(text))

    @property
    def definitions(self):
        return [n for n in self.nodes if n.opening is not None]

    def raw(self, node):
        return self.text[node.start:node.end]

    def line(self, node):
        return self.text.count("\n", 0, node.start) + 1


def splice(text, edits):
    """Apply disjoint replacements without formatting untouched source text."""
    previous = len(text)
    for start, end, replacement in sorted(edits, reverse=True):
        if end > previous:
            raise ValueError(f"Overlapping rewrite at {start}:{end}")
        text = text[:start] + replacement + text[end:]
        previous = start
    return text
