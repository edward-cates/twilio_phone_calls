from pathlib import Path
from datetime import datetime

class TmpFilePath:
    def __init__(self, extension: str):
        assert extension in {"mp3", "wav"}, extension
        assert Path("/tmp").exists(), "Expected `/tmp` directory to exist."
        self._tmp_dir = Path("/tmp/twilio_phone_calls")
        self._tmp_dir.mkdir(parents=True, exist_ok=True)
        now_ms_filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f")
        self._path = self._tmp_dir / f"{now_ms_filename}.{extension}"

    def __enter__(self) -> Path:
        return self._path

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._path.exists():
            self._path.unlink()
