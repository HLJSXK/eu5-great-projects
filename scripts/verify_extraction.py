"""Verify the extraction snapshot, optionally against its original TV Git commit."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def verify(source_repo: Path | None = None) -> list[str]:
    manifest = json.loads((ROOT / 'data/extraction_provenance.json').read_text(encoding='utf-8'))
    problems = []
    for row in manifest['final_files']:
        path = ROOT / row['path']
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != row['sha256']:
            problems.append(f"Final snapshot differs: {row['path']}")
    if source_repo:
        commit = manifest['source_commit']
        raw = subprocess.check_output(['git', '-C', str(source_repo.resolve()), 'ls-tree', '-rz', commit])
        blobs = {line.split(b'\t', 1)[1].decode(): line.split()[2].decode() for line in raw.split(b'\0') if line}
        for row in manifest['files']:
            if row.get('source_blob') and blobs.get(row['source']) != row['source_blob']:
                problems.append(f"Source Git blob differs: {row['source']}")
    return problems


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-repo', type=Path)
    args = parser.parse_args()
    problems = verify(args.source_repo)
    for problem in problems:
        print(f'[FAIL] {problem}')
    if not problems:
        print('[OK] Extraction snapshot and requested source-commit mappings match.')
    raise SystemExit(int(bool(problems)))
