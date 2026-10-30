#!/usr/bin/env python3
"""Edit every configured historical source image into a stylized PNG."""

import base64
import binascii
import argparse
import http.client
import json
import os
import re
import struct
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from pathlib import Path
from typing import Callable


REPO_ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = REPO_ROOT / "data/tool_config/dds_icons.json"
PROMPTS_PATH = REPO_ROOT / "assets/historical/review/historical_image_prompts.json"
OUTPUT_DIR = REPO_ROOT / "assets/historical/processed"
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
MAX_NETWORK_RETRIES = 10
NETWORK_RETRY_DELAY_SECONDS = 10
DEFAULT_PROMPT = (
    "Repaint the reference as a monumental historical strategy-game painting. "
    "Preserve the main subject's identity, defining silhouette, structural relationships "
    "and proportions. You may add, remove or rearrange secondary surroundings and "
    "make a modest change in camera height, distance or angle to emphasize its grandeur. "
    "Keep the complete subject dominant and recognizable; use plausible period details, "
    "small scale figures, atmospheric depth and substantial painterly materials. "
    "No invented extensions to the monument, text, logo, watermark or UI."
)


def parse_size(size: str) -> tuple[int, int]:
    if not isinstance(size, str) or not re.fullmatch(r"[1-9][0-9]*x[1-9][0-9]*", size):
        raise ValueError("Historical image size must be positive WIDTHxHEIGHT, such as 1536x1024")
    width, height = size.split("x")
    return int(width), int(height)


def load_tasks() -> tuple[dict, list[tuple[Path, Path]]]:
    root_config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    config = root_config["historical_images"]
    api_config = root_config.get("api", {})
    config.setdefault("api_key", api_config.get("api_key", ""))
    config.setdefault("api_key_env", api_config.get("api_key_env", "IMAGE_API_KEY"))
    endpoint = config["endpoint"]
    parsed = urllib.parse.urlparse(endpoint)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc or not parsed.path.rstrip("/").endswith("/images/edits"):
        raise ValueError("historical_images.endpoint must be an absolute Images edits URL")
    if not isinstance(config.get("overwrite"), bool):
        raise ValueError("historical_images.overwrite must be true or false")
    if not isinstance(config.get("model"), str) or not config["model"].strip():
        raise ValueError("historical_images.model must be set")
    images = config.get("images")
    if not isinstance(images, list) or not images:
        raise ValueError("historical_images.images must contain source/output mappings")

    prompts = json.loads(PROMPTS_PATH.read_text(encoding="utf-8")) if PROMPTS_PATH.exists() else {}
    if not isinstance(prompts, dict):
        raise ValueError(f"{PROMPTS_PATH.name} must contain an object keyed by source path")
    config["_prompts"] = prompts
    tasks = []
    seen_outputs = set()
    seen_sources = set()
    for image in images:
        if "size" in image:
            parse_size(image["size"])
        if "batch" in image and (not isinstance(image["batch"], str) or not image["batch"].strip()):
            raise ValueError("Historical image batch must be a non-empty string")
        source = (REPO_ROOT / image["source"]).resolve()
        output_name = image["output"]
        if Path(output_name).name != output_name or not output_name.endswith(".png"):
            raise ValueError(f"Output must be a PNG filename: {output_name}")
        if output_name in seen_outputs:
            raise ValueError(f"Duplicate historical output: {output_name}")
        if not source.is_file() or source.suffix.lower() not in {".jpg", ".jpeg", ".png", ".webp"}:
            raise FileNotFoundError(f"Missing or unsupported historical source: {source}")
        if source in seen_sources:
            raise ValueError(f"Duplicate historical source: {source}")
        prompt = prompts.get(image["source"])
        # Repository historical assets must have an explicit prompt. Small
        # isolated fixture configs may use the backward-compatible default.
        is_repo_historical = source.is_relative_to(REPO_ROOT / "assets" / "historical")
        if is_repo_historical and (not isinstance(prompt, str) or not prompt.strip()):
            raise ValueError(f"Missing historical prompt: {image['source']}")
        seen_sources.add(source)
        seen_outputs.add(output_name)
        tasks.append((source, OUTPUT_DIR / output_name))
    return config, tasks


def resolve_api_key(config: dict) -> str:
    configured = str(config.get("api_key") or "").strip()
    env_names = config.get("api_key_env", "IMAGE_API_KEY")
    if isinstance(env_names, str):
        env_names = [env_names]
    if not isinstance(env_names, list) or not all(isinstance(name, str) for name in env_names):
        raise ValueError("historical_images.api_key_env must be a string or list of strings")
    key = configured or next((os.environ[name].strip() for name in env_names if os.environ.get(name, "").strip()), "")
    if not key:
        raise RuntimeError(f"Set one of {', '.join(env_names)} or api.api_key in {CONFIG_PATH.name}")
    return key


def task_for_source(config: dict, source: Path) -> dict:
    """Resolve from the captured config, including when outputs are staged."""
    matches = [image for image in config["images"]
               if (REPO_ROOT / image["source"]).resolve() == source.resolve()]
    if len(matches) != 1:
        raise ValueError(f"Expected exactly one historical task for {source}")
    return matches[0]


def prompt_for_source(config: dict, source: Path) -> str:
    task = task_for_source(config, source)
    prompt = config.get("_prompts", {}).get(task["source"])
    if not isinstance(prompt, str) or not prompt.strip():
        return DEFAULT_PROMPT
    return prompt.strip()


def multipart_body(source: Path, model: str, prompt: str, *, size: str | None = None) -> tuple[bytes, str]:
    boundary = f"----TowardsVictoryHistorical{uuid.uuid4().hex}"
    body = bytearray()
    fields = {
        "model": model,
        "prompt": prompt,
        "n": "1",
        "output_format": "png",
        "response_format": "url",
    }
    if size is not None:
        parse_size(size)
        fields["size"] = size
    for name, value in fields.items():
        body.extend(f'--{boundary}\r\nContent-Disposition: form-data; name="{name}"\r\n\r\n{value}\r\n'.encode("utf-8"))
    content_type = {".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png", ".webp": "image/webp"}[source.suffix.lower()]
    body.extend(f'--{boundary}\r\nContent-Disposition: form-data; name="image"; filename="{source.name}"\r\nContent-Type: {content_type}\r\n\r\n'.encode("utf-8"))
    body.extend(source.read_bytes())
    body.extend(f"\r\n--{boundary}--\r\n".encode("ascii"))
    return bytes(body), boundary


def request_bytes(
    request: urllib.request.Request | str,
    label: str,
    *,
    check_cancelled: Callable[[], None] = lambda: None,
    wait: Callable[[float], None] = time.sleep,
) -> bytes:
    """Retry transient network failures, separately for generation and download."""
    for retries_used in range(MAX_NETWORK_RETRIES + 1):
        check_cancelled()
        try:
            with urllib.request.urlopen(request, timeout=180) as response:
                data = response.read()
        except urllib.error.HTTPError as exc:
            try:
                details = exc.read(500).decode("utf-8", errors="replace")
            except (OSError, http.client.HTTPException):
                details = str(exc.reason)
            finally:
                exc.close()
            message = f"HTTP {exc.code}: {details}"
            if exc.code not in {408, 429} and not 500 <= exc.code < 600:
                raise RuntimeError(f"{label} failed: {message}") from exc
            cause = exc
        except (urllib.error.URLError, OSError, http.client.HTTPException) as exc:
            message = f"{type(exc).__name__}: {exc}"
            cause = exc
        else:
            check_cancelled()
            return data
        check_cancelled()
        if retries_used == MAX_NETWORK_RETRIES:
            raise RuntimeError(f"{label} failed after {MAX_NETWORK_RETRIES} retries: {message}") from cause
        print(
            f"[retry] {label}: {message}. Waiting {NETWORK_RETRY_DELAY_SECONDS}s "
            f"before retry {retries_used + 1}/{MAX_NETWORK_RETRIES}...",
            flush=True,
        )
        wait(NETWORK_RETRY_DELAY_SECONDS)
    raise RuntimeError(f"{label} failed without a response")


def edit_image(config: dict, source: Path, api_key: str, *, prompt: str | None = None, size: str | None = None, check_cancelled: Callable[[], None] = lambda: None, wait: Callable[[float], None] = time.sleep) -> bytes:
    check_cancelled()
    prompt = prompt or str(config.get("prompt") or DEFAULT_PROMPT)
    body, boundary = multipart_body(source, config["model"], prompt, size=size)
    request = urllib.request.Request(
        config["endpoint"],
        data=body,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": f"multipart/form-data; boundary={boundary}",
            "Accept": "application/json",
        },
        method="POST",
    )
    try:
        result = json.loads(request_bytes(request, "Image edit", check_cancelled=check_cancelled, wait=wait))
        check_cancelled()
        item = result["data"][0]
        if isinstance(item.get("b64_json"), str):
            encoded = item["b64_json"].split(",", 1)[-1]
            image = base64.b64decode(encoded, validate=True)
        elif isinstance(item.get("url"), str):
            image = request_bytes(item["url"], "Image download", check_cancelled=check_cancelled, wait=wait)
        else:
            raise RuntimeError("Edit response has neither data[0].url nor data[0].b64_json")
    except (KeyError, IndexError, TypeError, ValueError, binascii.Error) as exc:
        raise RuntimeError(f"Invalid image edit response: {exc}") from exc
    if not image.startswith(PNG_SIGNATURE):
        raise RuntimeError("Image edit response is not a PNG")
    if size is not None:
        if len(image) < 24 or image[12:16] != b"IHDR":
            raise RuntimeError("Image edit response has no valid PNG dimensions")
        width, height = struct.unpack_from(">II", image, 16)
        if (width, height) != parse_size(size):
            raise RuntimeError(f"Image edit returned {width}x{height}; requested {size}. Output was not saved.")
    return image


def run(options: dict[str, object] | argparse.Namespace) -> int:
    """Run the configured batch from normalized application options."""
    values = vars(options) if isinstance(options, argparse.Namespace) else options
    dry_run = bool(values.get("dry_run", False))
    overwrite = bool(values.get("overwrite", False))
    config, tasks = load_tasks()
    batch = values.get("batch")
    if batch:
        tasks = [(source, output) for source, output in tasks
                 if task_for_source(config, source).get("batch") == batch]
        if not tasks:
            raise ValueError(f"Unknown historical batch: {batch}")
    selected = set(values.get("sources") or [])
    if selected:
        matched = {name for name in selected for source, _ in tasks
                   if name in {source.stem, source.relative_to(REPO_ROOT).as_posix()}}
        if selected - matched:
            raise ValueError(f"Unknown historical sources: {', '.join(sorted(selected - matched))}")
        tasks = [(source, output) for source, output in tasks
                 if selected.intersection({source.stem, source.relative_to(REPO_ROOT).as_posix()})]
    if values.get("output_dir"):
        output_dir = (REPO_ROOT / Path(values["output_dir"])).resolve()
        if not output_dir.is_relative_to(REPO_ROOT / "assets" / "historical" / "processed"):
            raise ValueError("output_dir must be inside assets/historical/processed")
        tasks = [(source, output_dir / output.name) for source, output in tasks]
    return run_tasks(config, tasks, dry_run=dry_run, overwrite=overwrite)


def run_tasks(config: dict, tasks: list[tuple[Path, Path]], *, dry_run: bool = False, overwrite: bool = False, check_cancelled: Callable[[], None] = lambda: None, wait: Callable[[float], None] = time.sleep) -> int:
    """Execute the task set already resolved by the CLI or Web plan."""
    print(f"[config] {CONFIG_PATH.relative_to(REPO_ROOT)}")
    pending = [(source, output) for source, output in tasks if overwrite or config["overwrite"] or not output.exists()]
    print(f"[tasks] selected={len(tasks)}, pending={len(pending)}, skipped={len(tasks) - len(pending)}")
    for source, output in tasks:
        if (source, output) not in pending:
            print(f"[skip] {output.relative_to(REPO_ROOT)} exists; overwrite=false")
    if not pending:
        return 0
    if dry_run:
        print(f"[dry-run] POST {config['endpoint']}")
        for source, output in pending:
            print(f"[dry-run] {source.relative_to(REPO_ROOT)} -> {output.relative_to(REPO_ROOT)}")
            size = task_for_source(config, source).get("size")
            if size is not None:
                print(f"[size] {size}")
            prompt = prompt_for_source(config, source)
            print(f"[prompt] {len(prompt)} characters: {prompt.splitlines()[0]}")
        return 0
    api_key = resolve_api_key(config)
    for source, output in pending:
        check_cancelled()
        output.parent.mkdir(parents=True, exist_ok=True)
        print(f"[edit] {source.relative_to(REPO_ROOT)} -> {output.relative_to(REPO_ROOT)}")
        prompt = prompt_for_source(config, source)
        size = task_for_source(config, source).get("size")
        image = edit_image(config, source, api_key, prompt=prompt, size=size, check_cancelled=check_cancelled, wait=wait)
        check_cancelled()
        temporary = output.with_suffix(output.suffix + ".tmp")
        try:
            temporary.write_bytes(image)
            temporary.replace(output)
        finally:
            temporary.unlink(missing_ok=True)
        print(f"[write] {output.relative_to(REPO_ROOT)}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Edit the configured historical images into styled PNGs.")
    parser.add_argument("--dry-run", action="store_true", help="List pending edits without calling the API")
    parser.add_argument("--overwrite", action="store_true", help="Regenerate outputs that already exist")
    parser.add_argument("--batch", help="Select a registered batch, such as landscape_3x2")
    parser.add_argument("--source", dest="sources", action="append", help="Select a source by name or repository path; repeat for multiple images")
    parser.add_argument("--output-dir", type=Path, help="Save a variant batch under assets/historical/processed")
    return run(parser.parse_args(argv))


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, RuntimeError, KeyError) as error:
        raise SystemExit(f"[error] {error}") from error
