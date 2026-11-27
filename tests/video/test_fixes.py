import json

from content.scripts.video.prep.fixes import apply_fixes, load_fixes


def test_apply_fixes_whole_word_case_insensitive():
    assert apply_fixes("I am 8 is great", {"i am 8": "im8"}) == "im8 is great"
    assert apply_fixes("diam 8 is", {"i am 8": "im8"}) == "diam 8 is"


def test_longest_key_first():
    assert apply_fixes("foo bar", {"foo": "X", "foo bar": "Y"}) == "Y"


def test_load_fixes_missing_is_empty(tmp_path):
    assert load_fixes(tmp_path) == {}


def test_load_fixes_reads_file(tmp_path):
    (tmp_path / "fixes.json").write_text(json.dumps({"a b": "ab"}), encoding="utf-8")
    assert load_fixes(tmp_path) == {"a b": "ab"}
