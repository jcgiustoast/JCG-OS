def pytest_configure(config):
    config.addinivalue_line(
        "markers", "slow: end-to-end render (speech -> whisper -> Remotion -> ffmpeg), ~1-3 min"
    )
    config.addinivalue_line(
        "markers", "gpu: needs the cut-out venv (.venv-matte) and the RTX GPU"
    )
