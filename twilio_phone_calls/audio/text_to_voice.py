from pathlib import Path
import time

from TTS.api import TTS

tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to("cuda")

def text__to__wav_filepath(text: str, wav_path: str | Path) -> None:
    wav_path = Path(wav_path)
    assert wav_path.parent.exists(), f"Expected {wav_path.parent} to exist"
    assert not wav_path.exists(), f"Expected {wav_path} to not exist"
    assert wav_path.suffix == ".wav", f"Expected .wav file, got {wav_path}"
    start_time = time.time()
    tts.tts_to_file(
        text=text,
        speaker='Tammy Grit',
        language="en",
        file_path=str(wav_path),
    )
    end_time = time.time()
    print(f"Time taken to generate audio: {end_time - start_time} seconds")
