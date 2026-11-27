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


def _matte_setup(tmp_path, monkeypatch, clips):
    """Job with a planned edl of full pictures; the cut-out tool is faked (never the GPU)."""
    job = _tjob(tmp_path)
    (job / "face.mp4").write_bytes(b"face")
    pics = [{"picture": f"{i}.png", "show": "full",
             "matte": {"file": f"job/matte/{i}.webm", "srcStart": s, "srcEnd": e}}
            for i, (s, e) in enumerate(clips, start=1)]
    (job / "edl.json").write_text(json.dumps({"format": "transparent", "pictures": pics}))
    py, model = tmp_path / "py.exe", tmp_path / "m.onnx"
    py.write_bytes(b"")
    model.write_bytes(b"")
    monkeypatch.setattr(make_short, "MATTE_PY", py)
    monkeypatch.setattr(make_short, "MATTE_MODEL", model)
    calls = []

    def fake_run(cmd, **kw):
        out = Path(cmd[cmd.index("--start") - 1])
        calls.append(out.name)
        if out.name in fail_on:
            return subprocess.CompletedProcess(cmd, 1)
        out.write_bytes(b"webm")
        return subprocess.CompletedProcess(cmd, 0)

    fail_on = set()
    monkeypatch.setattr(make_short.subprocess, "run", fake_run)
    return job, calls, fail_on


def test_matte_skips_when_nothing_changed(tmp_path, monkeypatch):
    job, calls, _ = _matte_setup(tmp_path, monkeypatch, [(1.0, 4.0)])
    make_short.matte_transparent(job)
    make_short.matte_transparent(job)
    assert calls == ["1.webm"]


def test_matte_redoes_when_times_change(tmp_path, monkeypatch):
    job, calls, _ = _matte_setup(tmp_path, monkeypatch, [(1.0, 4.0)])
    make_short.matte_transparent(job)
    edl = json.loads((job / "edl.json").read_text())
    edl["pictures"][0]["matte"]["srcEnd"] = 5.0
    (job / "edl.json").write_text(json.dumps(edl))
    make_short.matte_transparent(job)
    assert calls == ["1.webm", "1.webm"]


def test_matte_redoes_when_face_changes(tmp_path, monkeypatch):
    job, calls, _ = _matte_setup(tmp_path, monkeypatch, [(1.0, 4.0)])
    make_short.matte_transparent(job)
    (job / "face.mp4").write_bytes(b"a different take")
    make_short.matte_transparent(job)
    assert calls == ["1.webm", "1.webm"]


def test_matte_deletes_unlisted_files(tmp_path, monkeypatch):
    job, calls, _ = _matte_setup(tmp_path, monkeypatch, [(1.0, 4.0)])
    (job / "matte").mkdir()
    (job / "matte" / "old.webm").write_bytes(b"x")
    make_short.matte_transparent(job)
    assert not (job / "matte" / "old.webm").exists()
    assert (job / "matte" / "1.webm").exists()


def test_matte_failing_second_clip_keeps_first_recorded(tmp_path, monkeypatch, capsys):
    job, calls, fail_on = _matte_setup(tmp_path, monkeypatch, [(1.0, 4.0), (6.0, 9.0)])
    fail_on.add("2.webm")
    assert make_short.main(["transparent", str(job), "--step", "matte"]) == 2
    index = json.loads((job / "matte" / "index.json").read_text())
    assert list(index) == ["1.webm"]
    fail_on.clear()
    make_short.matte_transparent(job)
    assert calls == ["1.webm", "2.webm", "2.webm"]


def test_render_rejects_stale_matte(tmp_path, monkeypatch, capsys):
    job, calls, _ = _matte_setup(tmp_path, monkeypatch, [(1.0, 4.0)])
    make_short.matte_transparent(job)
    edl = json.loads((job / "edl.json").read_text())
    edl["pictures"][0]["matte"]["srcEnd"] = 5.0
    (job / "edl.json").write_text(json.dumps(edl))
    monkeypatch.setattr(make_short, "PUBLIC_JOB", tmp_path / "public_job")
    assert make_short.main(["transparent", str(job), "--step", "render"]) == 2
    assert "--step matte" in capsys.readouterr().err


def test_render_rejects_matte_from_another_take(tmp_path, monkeypatch, capsys):
    job, calls, _ = _matte_setup(tmp_path, monkeypatch, [(1.0, 4.0)])
    make_short.matte_transparent(job)
    (job / "face.mp4").write_bytes(b"a re-recorded take")
    monkeypatch.setattr(make_short, "PUBLIC_JOB", tmp_path / "public_job")
    assert make_short.main(["transparent", str(job), "--step", "render"]) == 2
    assert "--step matte" in capsys.readouterr().err


def test_render_passes_matte_check_after_fresh_matte(tmp_path, monkeypatch):
    job, calls, _ = _matte_setup(tmp_path, monkeypatch, [(1.0, 4.0)])
    make_short.matte_transparent(job)
    monkeypatch.setattr(make_short, "PUBLIC_JOB", tmp_path / "public_job")

    class Reached(Exception):
        pass

    def stop(cmd, **kw):
        raise Reached

    monkeypatch.setattr(make_short.subprocess, "run", stop)
    with pytest.raises(Reached):  # got past the matte check, up to the Remotion call
        make_short.render(job)


# ---- out-of-date edit list ---------------------------------------------------

import os  # noqa: E402


class _Reached(Exception):
    pass


def _stop(cmd, **kw):
    raise _Reached


def _planned_job(tmp_path, monkeypatch):
    """Job that went through prep, got a filled-in pictures.json, and was planned (edl written)."""
    job = _tjob(tmp_path)
    _fake_prep(monkeypatch)
    make_short.prep_transparent(job)
    (job / "pictures.json").write_text(json.dumps([
        {"picture": "1.png", "words": "first page", "show": "card"},
        {"picture": "2.png", "words": "long page", "show": "card"}]))
    monkeypatch.setattr(make_short, "build_transparent_edl",
                        lambda j, w, s=None: {"format": "transparent", "pictures": []})
    monkeypatch.setattr(make_short, "write_transparent_review", lambda e, p: Path(p).write_text("r"))
    make_short.plan_transparent(job)
    monkeypatch.setattr(make_short, "PUBLIC_JOB", tmp_path / "public_job")
    monkeypatch.setattr(make_short.subprocess, "run", _stop)  # never a real render
    return job


def _newer(path, seconds=10):
    st = path.stat()
    os.utime(path, (st.st_atime, st.st_mtime + seconds))


def test_prep_removes_old_edl_and_review(tmp_path, monkeypatch):
    job = _planned_job(tmp_path, monkeypatch)
    assert (job / "edl.json").exists() and (job / "review.md").exists()
    make_short.prep_transparent(job)
    assert not (job / "edl.json").exists()
    assert not (job / "review.md").exists()


def test_render_after_new_prep_says_run_plan(tmp_path, monkeypatch, capsys):
    job = _planned_job(tmp_path, monkeypatch)
    make_short.prep_transparent(job)
    assert make_short.main(["transparent", str(job), "--step", "render"]) == 2
    assert "--step plan" in capsys.readouterr().err


def test_render_after_editing_pictures_says_run_plan(tmp_path, monkeypatch, capsys):
    job = _planned_job(tmp_path, monkeypatch)
    _newer(job / "pictures.json")
    assert make_short.main(["transparent", str(job), "--step", "render"]) == 2
    err = capsys.readouterr().err
    assert "--step plan" in err and "pictures.json" in err


@pytest.mark.parametrize("name", ["words.json", "fixes.json", "headline.txt"])
def test_render_after_editing_other_inputs_says_run_plan(tmp_path, monkeypatch, capsys, name):
    job = _planned_job(tmp_path, monkeypatch)
    if not (job / name).exists():
        (job / name).write_text("{}")
    _newer(job / name)
    assert make_short.main(["transparent", str(job), "--step", "render"]) == 2
    assert "--step plan" in capsys.readouterr().err


def test_render_after_editing_redact_says_run_plan(tmp_path, monkeypatch, capsys):
    job = _planned_job(tmp_path, monkeypatch)
    (job / "shots" / "redact.json").write_text("{}")
    _newer(job / "shots" / "redact.json")
    assert make_short.main(["transparent", str(job), "--step", "render"]) == 2
    assert "--step plan" in capsys.readouterr().err


def test_matte_after_editing_pictures_says_run_plan(tmp_path, monkeypatch, capsys):
    job = _planned_job(tmp_path, monkeypatch)
    _newer(job / "pictures.json")
    assert make_short.main(["transparent", str(job), "--step", "matte"]) == 2
    assert "--step plan" in capsys.readouterr().err


def test_render_after_plan_passes_the_check(tmp_path, monkeypatch):
    job = _planned_job(tmp_path, monkeypatch)
    (job / "face.mp4").write_bytes(b"face")
    with pytest.raises(_Reached):
        make_short.render(job)


def test_ranking_missing_edl_still_says_prep(tmp_path, capsys):
    assert make_short.main(["ranking", str(tmp_path), "--step", "render"]) == 2
    assert "--step prep" in capsys.readouterr().err


def test_transparent_render_with_no_edl_says_plan(tmp_path, capsys):
    assert make_short.main(["transparent", str(tmp_path), "--step", "render"]) == 2
    assert "--step plan" in capsys.readouterr().err


def test_step_all_passes_the_freshness_checks(tmp_path, monkeypatch):
    job = _planned_job(tmp_path, monkeypatch)
    (job / "face.mp4").write_bytes(b"face")
    old = job / "edl.json"
    st = old.stat()
    os.utime(old, (st.st_atime, st.st_mtime - 60))  # an out-of-date edit list; "all" plans again first
    with pytest.raises(_Reached):  # got through plan and matte up to the Remotion call
        make_short.main(["transparent", str(job), "--step", "all"])
