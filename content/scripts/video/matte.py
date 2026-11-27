"""Cut-out tool: remove the background behind a person (Robust Video Matting) -> alpha WebM.

Runs inside .venv-matte (numpy + onnxruntime only, no repo imports):

  .venv-matte/Scripts/python.exe -I matte.py SRC.mp4 OUT.webm --start S --end E
        [--warmup 0.5] [--model models/rvm_resnet50_fp32.onnx] [--dr 0.25] [--cpu]

Writes source seconds [S, E] as a 30 fps VP9 WebM with alpha. The model carries state from
frame to frame, so it first runs over `warmup` seconds before S (not written) to settle.
Prints: frames=N seconds=T provider=CUDAExecutionProvider
"""
import argparse
import subprocess
import sys
import time
from pathlib import Path

import numpy as np

FPS = 30
DEFAULT_MODEL = Path(__file__).resolve().parent / "models" / "rvm_resnet50_fp32.onnx"


def probe_size(path):
    out = subprocess.check_output([
        "ffprobe", "-v", "error", "-select_streams", "v:0",
        "-show_entries", "stream=width,height", "-of", "csv=p=0", str(path)]).decode().strip()
    w, h = out.split(",")[:2]
    return int(w), int(h)


def read_frames(path, w, h, ss, duration):
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-ss", f"{ss:.3f}", "-i", str(path),
                          "-t", f"{duration:.3f}", "-vf", f"fps={FPS}",
                          "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    n = w * h * 3
    while True:
        buf = p.stdout.read(n)
        if len(buf) < n:
            break
        yield np.frombuffer(buf, np.uint8).reshape(h, w, 3)
    p.stdout.close()
    p.wait()


def open_writer(path, w, h):
    return subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgba",
                             "-s", f"{w}x{h}", "-r", str(FPS), "-i", "-",
                             "-c:v", "libvpx-vp9", "-pix_fmt", "yuva420p", "-b:v", "0", "-crf", "30",
                             "-row-mt", "1", "-an", str(path)], stdin=subprocess.PIPE)


class RVM:
    def __init__(self, model, cpu, dr):
        import onnxruntime as ort
        if not cpu:
            ort.preload_dlls()
        prov = ["CPUExecutionProvider"] if cpu else ["CUDAExecutionProvider", "CPUExecutionProvider"]
        so = ort.SessionOptions()
        so.log_severity_level = 3
        self.s = ort.InferenceSession(str(model), so, providers=prov)
        self.provider = self.s.get_providers()[0]
        self.dt = np.float16 if "fp16" in str(model) else np.float32
        self.rec = [np.zeros([1, 1, 1, 1], self.dt)] * 4
        self.dr = np.array([dr], np.float32)

    def __call__(self, rgb):
        src = (rgb.astype(np.float32) / 255.0).transpose(2, 0, 1)[None].astype(self.dt)
        fgr, pha, *self.rec = self.s.run(None, {"src": src, "r1i": self.rec[0], "r2i": self.rec[1],
                                                "r3i": self.rec[2], "r4i": self.rec[3],
                                                "downsample_ratio": self.dr})
        fg = fgr[0].transpose(1, 2, 0).astype(np.float32)
        return pha[0, 0].astype(np.float32), fg


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("out")
    ap.add_argument("--start", type=float, required=True)
    ap.add_argument("--end", type=float, required=True)
    ap.add_argument("--warmup", type=float, default=0.5)
    ap.add_argument("--model", default=str(DEFAULT_MODEL))
    ap.add_argument("--dr", type=float, default=0.25)
    ap.add_argument("--cpu", action="store_true")
    a = ap.parse_args()

    if a.end <= a.start:
        sys.exit("matte: --end must be after --start")
    if not Path(a.model).exists():
        sys.exit(f"matte: model not found at {a.model} (run setup_matte.ps1)")

    m = RVM(a.model, a.cpu, a.dr)
    if not a.cpu and m.provider != "CUDAExecutionProvider":
        sys.exit("matte: the GPU (CUDA) is not available, so the cut-out would be very slow. "
                 "Check the NVIDIA driver / re-run setup_matte.ps1, or pass --cpu to run slowly anyway.")

    w, h = probe_size(a.src)
    ss = max(0.0, a.start - a.warmup)
    n_warm = round((a.start - ss) * FPS)
    n_out = round((a.end - a.start) * FPS)
    w_proc = open_writer(a.out, w, h)

    t0 = time.perf_counter()
    written = 0
    for i, rgb in enumerate(read_frames(a.src, w, h, ss, a.end - ss)):
        alpha, fg = m(rgb)
        if i < n_warm:
            continue
        rgba = np.empty((h, w, 4), np.uint8)
        rgba[..., :3] = (fg * 255.0).clip(0, 255).astype(np.uint8)
        rgba[..., 3] = (alpha * 255.0).clip(0, 255).astype(np.uint8)
        w_proc.stdin.write(rgba.tobytes())
        written += 1
        if written >= n_out:
            break
    w_proc.stdin.close()
    if w_proc.wait() != 0:
        sys.exit("matte: ffmpeg failed while writing the WebM")
    if written == 0:
        sys.exit("matte: no frames were read (is --start inside the video?)")
    print(f"frames={written} seconds={time.perf_counter() - t0:.1f} provider={m.provider}")


if __name__ == "__main__":
    main()
