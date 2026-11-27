"""Cut-out tool (matte.py): mechanics only, on a synthetic clip. Needs the GPU venv + model."""
import subprocess
from pathlib import Path

import pytest

VIDEO_DIR = Path(__file__).resolve().parents[2] / "content" / "scripts" / "video"
PY = VIDEO_DIR / ".venv-matte" / "Scripts" / "python.exe"
MODEL = VIDEO_DIR / "models" / "rvm_resnet50_fp32.onnx"

pytestmark = [
    pytest.mark.gpu,
    pytest.mark.skipif(not (PY.exists() and MODEL.exists()),
                       reason="cut-out venv/model not set up (run content/scripts/video/setup_matte.ps1)"),
]


@pytest.fixture(scope="module")
def src(tmp_path_factory):
    p = tmp_path_factory.mktemp("matte") / "src.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi",
                    "-i", "testsrc2=size=1080x1920:rate=30:duration=3",
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", str(p)], check=True)
    return p


def run_matte(src, out, start, end):
    return subprocess.run([str(PY), "-I", str(VIDEO_DIR / "matte.py"), str(src), str(out),
                           "--start", str(start), "--end", str(end), "--model", str(MODEL)],
                          capture_output=True, text=True)


def probe(path, entries):
    return subprocess.check_output(["ffprobe", "-v", "error", "-select_streams", "v:0",
                                    "-show_entries", entries, "-of", "default=nw=1", str(path)],
                                   text=True)


def decoded_frames(path):
    out = subprocess.check_output(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0",
                                   "-show_entries", "stream=nb_read_frames", "-of", "csv=p=0",
                                   str(path)], text=True)
    return int(out.strip())


def test_matte_writes_alpha_webm(src, tmp_path):
    out = tmp_path / "o.webm"
    r = run_matte(src, out, 1.0, 2.0)
    assert r.returncode == 0, r.stderr
    assert out.exists()
    info = probe(out, "stream=codec_name,width,height,r_frame_rate:stream_tags=alpha_mode")
    assert "codec_name=vp9" in info
    assert "TAG:alpha_mode=1" in info
    assert "width=1080" in info and "height=1920" in info
    assert "r_frame_rate=30/1" in info
    assert abs(decoded_frames(out) - 30) <= 1


def test_matte_start_zero_has_no_warmup_before_file_start(src, tmp_path):
    out = tmp_path / "z.webm"
    r = run_matte(src, out, 0, 1)
    assert r.returncode == 0, r.stderr
    assert abs(decoded_frames(out) - 30) <= 1
