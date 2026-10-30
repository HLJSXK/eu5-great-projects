import pytest

from scripts_engineering_department.main_menu.localization import (
    translate_engineering_department_localization_google as translate,
)


def test_fill_preserves_translations_foreign_keys_tokens_and_nested_owners(tmp_path, monkeypatch):
    source = tmp_path / "english" / "example_l_english.yml"
    source.parent.mkdir()
    source.write_text(
        'l_english:\n live:0 "Live"\n nested:0 "Nested"\n'
        ' missing:0 "$live$ [ROOT.GetName] @gold! #Y 10#!\\nNext"\n',
        encoding="utf-8-sig",
    )
    target = tmp_path / "french" / "example_l_french.yml"
    target.parent.mkdir()
    original = 'l_french:\r\n live:0 "Traduit"\r\n foreign:0 "Conserver"\r\n'
    target.write_bytes(original.encode("utf-8-sig"))
    nested = target.parent / "events" / "other.yml"
    nested.parent.mkdir()
    nested.write_text('l_french:\n nested:0 "Ailleurs"\n', encoding="utf-8-sig")
    monkeypatch.setattr(translate, "SOURCE_DIR", source.parent)
    monkeypatch.setattr(translate, "OUTPUT_ROOT", tmp_path)

    assert translate.fill_missing_keys("french", [source]) == 1
    expected = original + ' missing:0 "$live$ [ROOT.GetName] @gold! #Y 10#!\\nNext"\r\n'
    assert target.read_bytes() == expected.encode("utf-8-sig")
    assert translate.fill_missing_keys("french", [source]) == 0
    assert target.read_bytes() == expected.encode("utf-8-sig")


def test_fill_creates_missing_language_file_with_bom_and_correct_header(tmp_path, monkeypatch):
    source = tmp_path / "english" / "example_l_english.yml"
    source.parent.mkdir()
    source.write_text('l_english:\n added:0 "Added"\n', encoding="utf-8-sig")
    monkeypatch.setattr(translate, "SOURCE_DIR", source.parent)
    monkeypatch.setattr(translate, "OUTPUT_ROOT", tmp_path)

    assert translate.fill_missing_keys("japanese", [source]) == 1
    output = tmp_path / "japanese" / "example_l_japanese.yml"
    assert output.read_bytes().startswith(b"\xef\xbb\xbfl_japanese:\n")
    assert ' added:0 "Added"\n' in output.read_text(encoding="utf-8-sig")


@pytest.mark.parametrize("arguments", [[], ["--fill-missing"]])
def test_fill_cli_defaults_to_all_nine_languages_without_a_translation_client(monkeypatch, arguments):
    calls = []
    monkeypatch.setattr(translate.sys, "argv", ["translate", *arguments])
    monkeypatch.setattr(translate, "collect_source_files", lambda filters: [])
    monkeypatch.setattr(translate, "fill_missing_keys", lambda language, sources: calls.append(language) or 0)
    monkeypatch.setattr(translate, "load_cache", lambda path: (_ for _ in ()).throw(AssertionError("offline")))
    assert translate.main() == 0
    assert set(calls) == set(translate.LANGUAGE_TO_GOOGLE)
    assert len(calls) == 9
