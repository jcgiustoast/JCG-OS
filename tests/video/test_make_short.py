"""Fast checks on the runner (the full pipeline is in test_e2e.py)."""
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
MAKE_SHORT = REPO / "content" / "scripts" / "video" / "make_short.py"


def _run(*args):
    return subprocess.run(
        [sys.executable, str(MAKE_SHORT), *args], cwd=REPO, capture_output=True, text=True
    )


def test_prep_without_recording_exits_2(tmp_path):
    job = tmp_path / "job"
    (job / "raw").mkdir(parents=True)
    (job / "shots").mkdir()
    result = _run("ranking", str(job), "--step", "prep")
    assert result.returncode == 2
    assert "raw" in (result.stdout + result.stderr)


def test_prep_with_two_recordings_exits_2(tmp_path):
    job = tmp_path / "job"
    (job / "raw").mkdir(parents=True)
    (job / "raw" / "a.mp4").write_bytes(b"")
    (job / "raw" / "b.MOV").write_bytes(b"")
    result = _run("ranking", str(job), "--step", "prep")
    assert result.returncode == 2
    assert "a.mp4" in result.stdout + result.stderr


def test_check_output_reads_size_fps_loudness(tmp_path):
    from content.scripts.video.make_short import check_output

    clip = tmp_path / "c.mp4"
    subprocess.run(
        [
            "ffmpeg", "-y", "-loglevel", "error",
            "-f", "lavfi", "-i", "color=c=gray:s=1080x1920:r=30:d=3",
            "-f", "lavfi", "-i", "sine=frequency=440:duration=3",
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", str(clip),
        ],
        check=True,
    )
    info = check_output(clip)
    assert (info["width"], info["height"]) == (1080, 1920)
    assert info["fps"] == pytest.approx(30, abs=0.01)
    assert -40 < info["lufs"] < 0  # ffmpeg's sine is ~-21 LUFS


# ---- Transparent Background steps -------------------------------------------

import json  # noqa: E402

from PIL import Image  # noqa: E402

from content.scripts.video import make_short  # noqa: E402
from tests.video.helpers import words_from  # noqa: E402


def _tjob(tmp_path):
    job = tmp_path / "job"
    (job / "raw").mkdir(parents=True)
    (job / "raw" / "rec.mp4").write_bytes(b"x")
    (job / "shots").mkdir()
    Image.new("RGB", (1080, 3000), "white").save(job / "shots" / "1.png")
    Image.new("RGB", (800, 600), "white").save(job / "shots" / "2.png")
    (job / "headline.txt").write_text("Seven emails that sell")
    return job


def _fake_prep(monkeypatch, words_text="so here is the first page and then the long page"):
    import content.scripts.video.prep.transcribe as tr

    monkeypatch.setattr(make_short, "normalize", lambda src, dst: Path(dst).write_bytes(b"face"))
    monkeypatch.setattr(tr, "transcribe", lambda face, model="small": words_from(words_text, step=0.5))


def test_transparent_prep_writes_stub_once(tmp_path, monkeypatch):
    job = _tjob(tmp_path)
    _fake_prep(monkeypatch)
    make_short.prep_transparent(job)
    (job / "fixes.json").write_text('{"a": "b"}')
    pics = job / "pictures.json"
    pics.write_text('[{"picture": "1.png", "words": "first page", "show": "card"}]')
    before = {n: (job / n).read_bytes() for n in ("pictures.json", "fixes.json", "headline.txt")}
    make_short.prep_transparent(job)
    after = {n: (job / n).read_bytes() for n in before}
    assert before == after


def test_transparent_prep_does_not_write_edl(tmp_path, monkeypatch):
    job = _tjob(tmp_path)
    _fake_prep(monkeypatch)
    make_short.prep_transparent(job)
    assert (job / "pictures.json").exists()
    assert (job / "words.json").exists()
    assert not (job / "edl.json").exists()


def test_transparent_plan_with_empty_words_exits_2(tmp_path, monkeypatch, capsys):
    job = _tjob(tmp_path)
    _fake_prep(monkeypatch)
    make_short.prep_transparent(job)  # stub has empty words
    assert make_short.main(["transparent", str(job), "--step", "plan"]) == 2
    assert "1.png" in capsys.readouterr().err


def test_transparent_render_without_matte_exits_2(tmp_path, monkeypatch, capsys):
    job = _tjob(tmp_path)
    (job / "face.mp4").write_bytes(b"face")
    edl = {"format": "transparent", "pictures": [
        {"picture": "1.png", "show": "full", "matte": {"file": "job/matte/1.webm"}},
        {"picture": "2.png", "show": "card", "matte": None},
    ]}
    (job / "edl.json").write_text(json.dumps(edl))
    monkeypatch.setattr(make_short, "PUBLIC_JOB", tmp_path / "public_job")
    assert make_short.main(["transparent", str(job), "--step", "render"]) == 2
    assert "matte" in capsys.readouterr().err


def test_matte_without_venv_exits_2(tmp_path, monkeypatch, capsys):
    job = _tjob(tmp_path)
    edl = {"format": "transparent", "pictures": [
        {"picture": "1.png", "show": "full",
         "matte": {"file": "job/matte/1.webm", "srcStart": 1.0, "srcEnd": 4.0}},
    ]}
    (job / "edl.json").write_text(json.dumps(edl))
    monkeypatch.setattr(make_short, "MATTE_PY", tmp_path / "nope" / "python.exe")
    monkeypatch.setattr(make_short, "MATTE_MODEL", tmp_path / "nope" / "m.onnx")
    assert make_short.main(["transparent", str(job), "--step", "matte"]) == 2
    assert "setup_matte" in capsys.readouterr().err


def test_ranking_rejects_plan_step(tmp_path, capsys):
    assert make_short.main(["ranking", str(tmp_path), "--step", "plan"]) == 2
    assert make_short.main(["ranking", str(tmp_path), "--step", "matte"]) == 2
