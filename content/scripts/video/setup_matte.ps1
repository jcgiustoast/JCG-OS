# One-time setup for the cut-out tool (Robust Video Matting on the GPU).
# Creates .venv-matte next to this script, installs ~2 GB of wheels, fetches the 107 MB model.
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

if (-not (Test-Path ".venv-matte\Scripts\python.exe")) {
    py -3.13 -m venv .venv-matte
}
& .venv-matte\Scripts\python.exe -m pip install --upgrade pip
& .venv-matte\Scripts\python.exe -m pip install -r requirements-matte.txt

New-Item -ItemType Directory -Force models | Out-Null
$model = "models\rvm_resnet50_fp32.onnx"
if (-not (Test-Path $model)) {
    $cached = Join-Path $env:LOCALAPPDATA "Temp\claude\6d266a6eef6d0ce4\c1a0c63e-a9a3-4537-9022-72ed6f716258\scratchpad\bgtest\models\rvm_resnet50_fp32.onnx"
    if (Test-Path $cached) {
        Copy-Item $cached $model
    } else {
        Invoke-WebRequest "https://github.com/PeterL1n/RobustVideoMatting/releases/download/v1.0.0/rvm_resnet50_fp32.onnx" -OutFile $model
    }
}

& .venv-matte\Scripts\python.exe -I -c "import onnxruntime as o; o.preload_dlls(); print(o.get_available_providers())"
