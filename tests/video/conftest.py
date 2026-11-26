def pytest_configure(config):
    config.addinivalue_line(
        "markers", "slow: end-to-end render (speech -> whisper -> Remotion -> ffmpeg), ~1-3 min"
    )
