import base64
import http.client
import io
import json
import urllib.error

import pytest
from PIL import Image

from scripts import generate_historical_images as historical


def png_bytes(size):
    buffer = io.BytesIO()
    Image.new("RGB", size, "skyblue").save(buffer, format="PNG")
    return buffer.getvalue()


@pytest.fixture
def configured_task(tmp_path, monkeypatch):
    source = tmp_path / "reference.png"
    source.write_bytes(png_bytes((64, 96)))
    output_dir = tmp_path / "assets/historical/processed"
    config_path = tmp_path / "config.json"
    prompts_path = tmp_path / "prompts.json"
    config = {"historical_images": {
        "endpoint": "https://example.invalid/images/edits",
        "model": "fixture", "overwrite": False, "api_key": "fixture",
        "images": [{"source": "reference.png", "output": "landscape.png", "size": "96x64"}],
    }}
    config_path.write_text(json.dumps(config), encoding="utf-8")
    prompts_path.write_text(json.dumps({"reference.png": "Keep the tower complete in a 3:2 landscape."}), encoding="utf-8")
    monkeypatch.setattr(historical, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(historical, "CONFIG_PATH", config_path)
    monkeypatch.setattr(historical, "PROMPTS_PATH", prompts_path)
    monkeypatch.setattr(historical, "OUTPUT_DIR", output_dir)
    return config, source, output_dir / "landscape.png"


def test_selected_task_sends_size_prompt_and_current_reference(configured_task, monkeypatch):
    _, source, output = configured_task
    result_png = png_bytes((96, 64))
    requests = []

    def respond(request, **_kwargs):
        requests.append(request)
        return io.BytesIO(json.dumps({"data": [{"b64_json": base64.b64encode(result_png).decode()}]}).encode())

    monkeypatch.setattr(historical.urllib.request, "urlopen", respond)
    assert historical.run({"sources": ["reference"]}) == 0
    assert len(requests) == 1
    body = requests[0].data
    assert b'name="size"\r\n\r\n96x64\r\n' in body
    assert b"Keep the tower complete in a 3:2 landscape." in body
    assert source.read_bytes() in body
    assert output.read_bytes() == result_png


def test_wrong_size_response_does_not_replace_existing_output(configured_task, monkeypatch):
    _, _, output = configured_task
    output.parent.mkdir(parents=True)
    output.write_bytes(b"existing accepted version")
    portrait = png_bytes((64, 96))
    monkeypatch.setattr(historical.urllib.request, "urlopen", lambda *_args, **_kwargs: io.BytesIO(
        json.dumps({"data": [{"b64_json": base64.b64encode(portrait).decode()}]}).encode()
    ))
    with pytest.raises(RuntimeError, match="returned 64x96; requested 96x64"):
        historical.run({"sources": ["reference"], "overwrite": True})
    assert output.read_bytes() == b"existing accepted version"
    assert not output.with_suffix(".png.tmp").exists()


def test_ordinary_task_omits_size_and_keeps_existing_dimensions(configured_task, monkeypatch):
    config, source, output = configured_task
    del config["historical_images"]["images"][0]["size"]
    historical.CONFIG_PATH.write_text(json.dumps(config), encoding="utf-8")

    def respond(request, **_kwargs):
        assert b'name="size"' not in request.data
        return io.BytesIO(json.dumps({"data": [{"b64_json": base64.b64encode(source.read_bytes()).decode()}]}).encode())

    monkeypatch.setattr(historical.urllib.request, "urlopen", respond)
    assert historical.run({"sources": ["reference"]}) == 0
    assert output.read_bytes() == source.read_bytes()


def test_size_dry_run_does_not_call_api_or_write_output(configured_task, monkeypatch, capsys):
    _, _, output = configured_task
    monkeypatch.setattr(historical, "resolve_api_key", lambda *_: pytest.fail("dry run requested an API key"))
    assert historical.run({"dry_run": True, "sources": ["reference"]}) == 0
    assert "[size] 96x64" in capsys.readouterr().out
    assert not output.exists()


@pytest.mark.parametrize("size", ["3:2", "0x1024", "1536x-1024", 1536, None])
def test_invalid_task_size_is_rejected_before_api(configured_task, size):
    config, _, _ = configured_task
    config["historical_images"]["images"][0]["size"] = size
    historical.CONFIG_PATH.write_text(json.dumps(config), encoding="utf-8")
    with pytest.raises(ValueError, match="positive WIDTHxHEIGHT"):
        historical.load_tasks()


def test_batch_resumes_pending_images_without_running_ordinary_tasks(configured_task, monkeypatch):
    config, source, accepted_output = configured_task
    images = config["historical_images"]["images"]
    images[0]["batch"] = "landscape_3x2"
    for name, batch in (("remaining", "landscape_3x2"), ("ordinary", None)):
        source.with_name(name + ".png").write_bytes(source.read_bytes())
        task = {"source": name + ".png", "output": name + "_result.png", "size": "96x64"}
        if batch:
            task["batch"] = batch
        images.append(task)
    historical.CONFIG_PATH.write_text(json.dumps(config), encoding="utf-8")
    accepted_output.parent.mkdir(parents=True)
    accepted_output.write_bytes(png_bytes((96, 64)))
    accepted_bytes = accepted_output.read_bytes()
    called = []

    def edit(_config, selected_source, _key, **kwargs):
        called.append(selected_source.name)
        assert kwargs["size"] == "96x64"
        return png_bytes((96, 64))

    monkeypatch.setattr(historical, "edit_image", edit)
    assert historical.run({"batch": "landscape_3x2"}) == 0
    assert called == ["remaining.png"]
    assert accepted_output.read_bytes() == accepted_bytes
    assert accepted_output.with_name("remaining_result.png").exists()
    assert not accepted_output.with_name("ordinary_result.png").exists()


def test_unknown_batch_is_rejected_before_api(configured_task, monkeypatch):
    monkeypatch.setattr(historical, "resolve_api_key", lambda *_: pytest.fail("unknown batch requested an API key"))
    with pytest.raises(ValueError, match="Unknown historical batch"):
        historical.run({"batch": "misspelled"})


def test_source_selector_cannot_escape_selected_batch(configured_task, monkeypatch):
    config, source, _ = configured_task
    config["historical_images"]["images"][0]["batch"] = "landscape_3x2"
    source.with_name("ordinary.png").write_bytes(source.read_bytes())
    config["historical_images"]["images"].append({"source": "ordinary.png", "output": "ordinary_result.png"})
    historical.CONFIG_PATH.write_text(json.dumps(config), encoding="utf-8")
    monkeypatch.setattr(historical, "resolve_api_key", lambda *_: pytest.fail("out-of-batch source requested an API key"))
    with pytest.raises(ValueError, match="Unknown historical sources: ordinary"):
        historical.run({"batch": "landscape_3x2", "sources": ["ordinary"]})


@pytest.mark.parametrize("error", [
    lambda: urllib.error.HTTPError("https://example.invalid/images/edits", 524, "timeout", {}, io.BytesIO(b"origin timed out")),
    lambda: urllib.error.HTTPError("https://example.invalid/images/edits", 429, "busy", {}, io.BytesIO(b"try later")),
    lambda: urllib.error.URLError("connection lost"),
    lambda: TimeoutError("read timed out"),
    lambda: ConnectionResetError("connection reset"),
    lambda: http.client.IncompleteRead(b"partial", 100),
])
def test_transient_edit_failure_retries_after_ten_seconds(configured_task, monkeypatch, error):
    _, source, _ = configured_task
    result_png = png_bytes((96, 64))
    requests, waits = [], []

    def respond(request, **_kwargs):
        requests.append(request)
        if len(requests) == 1:
            raise error()
        return io.BytesIO(json.dumps({"data": [{"b64_json": base64.b64encode(result_png).decode()}]}).encode())

    monkeypatch.setattr(historical.urllib.request, "urlopen", respond)
    config, _ = historical.load_tasks()
    assert historical.edit_image(config, source, "fixture", size="96x64", wait=waits.append) == result_png
    assert waits == [10]
    assert len(requests) == 2
    assert requests[0].data == requests[1].data


def test_network_retry_limit_preserves_existing_output(configured_task, monkeypatch):
    _, _, output = configured_task
    output.parent.mkdir(parents=True)
    output.write_bytes(b"accepted version")
    requests, waits = [], []

    def fail(request, **_kwargs):
        requests.append(request)
        raise urllib.error.HTTPError(request.full_url, 524, "timeout", {}, io.BytesIO(b"origin timed out"))

    monkeypatch.setattr(historical.urllib.request, "urlopen", fail)
    config, tasks = historical.load_tasks()
    with pytest.raises(RuntimeError, match="failed after 10 retries: HTTP 524"):
        historical.run_tasks(config, tasks, overwrite=True, wait=waits.append)
    assert len(requests) == 11  # The initial request plus at most ten retries.
    assert waits == [10] * 10
    assert output.read_bytes() == b"accepted version"
    assert not output.with_suffix(".png.tmp").exists()


@pytest.mark.parametrize("status", [400, 401, 403, 422])
def test_permanent_http_error_is_not_retried(configured_task, monkeypatch, status):
    _, source, _ = configured_task
    requests = []

    def fail(request, **_kwargs):
        requests.append(request)
        raise urllib.error.HTTPError(request.full_url, status, "rejected", {}, io.BytesIO(b"invalid request"))

    monkeypatch.setattr(historical.urllib.request, "urlopen", fail)
    config, _ = historical.load_tasks()
    with pytest.raises(RuntimeError, match=f"HTTP {status}"):
        historical.edit_image(config, source, "fixture", wait=lambda _: pytest.fail("permanent failure was retried"))
    assert len(requests) == 1


def test_download_retry_does_not_repeat_generation(configured_task, monkeypatch):
    _, source, _ = configured_task
    result_png = png_bytes((96, 64))
    edits, downloads, waits = [], [], []
    url = "https://example.invalid/result.png"

    def respond(request, **_kwargs):
        if isinstance(request, str):
            downloads.append(request)
            if len(downloads) == 1:
                raise urllib.error.HTTPError(url, 524, "timeout", {}, io.BytesIO(b"download timed out"))
            return io.BytesIO(result_png)
        edits.append(request)
        return io.BytesIO(json.dumps({"data": [{"url": url}]}).encode())

    monkeypatch.setattr(historical.urllib.request, "urlopen", respond)
    config, _ = historical.load_tasks()
    assert historical.edit_image(config, source, "fixture", size="96x64", wait=waits.append) == result_png
    assert len(edits) == 1
    assert downloads == [url, url]
    assert waits == [10]


def test_cancellation_during_retry_wait_prevents_next_request(configured_task, monkeypatch):
    _, source, _ = configured_task
    requests = []

    class Cancelled(Exception):
        pass

    def fail(request, **_kwargs):
        requests.append(request)
        raise TimeoutError("read timed out")

    def cancel(_seconds):
        raise Cancelled()

    monkeypatch.setattr(historical.urllib.request, "urlopen", fail)
    config, _ = historical.load_tasks()
    with pytest.raises(Cancelled):
        historical.edit_image(config, source, "fixture", wait=cancel)
    assert len(requests) == 1


def test_invalid_response_is_not_retried(configured_task, monkeypatch):
    _, source, _ = configured_task
    requests = []

    def respond(request, **_kwargs):
        requests.append(request)
        return io.BytesIO(b"not valid JSON")

    monkeypatch.setattr(historical.urllib.request, "urlopen", respond)
    config, _ = historical.load_tasks()
    with pytest.raises(RuntimeError, match="Invalid image edit response"):
        historical.edit_image(config, source, "fixture", wait=lambda _: pytest.fail("invalid response was retried"))
    assert len(requests) == 1
