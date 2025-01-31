from pathlib import Path

import numpy as np

from twilio_phone_calls.audio.tmp_file_path import TmpFilePath
from twilio_phone_calls.audio.audio_conversions import (
    mulaw_filepath__to__np_pcm_wav,
    np_pcm_wav__to__wav_filepath,
)
from twilio_phone_calls.audio.voice_to_text import voice_to_text

def test_voice_to_text():
    sample_path = Path("tests/fixtures/1684778198.0636666.sample.wav") # Mulaw file.
    with TmpFilePath("wav") as tmp_path:
        pcm_wav_audio: np.ndarray = mulaw_filepath__to__np_pcm_wav(sample_path)
        np_pcm_wav__to__wav_filepath(pcm_wav_audio, tmp_path)
        text = voice_to_text(tmp_path)
    assert "how are you" in text.lower(), text

if __name__ == "__main__":
    test_voice_to_text()
    print("Tests pass.")
