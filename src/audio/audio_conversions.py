import audioop # FIXME: This is apparently deprecated and getting removed!!!
import base64
from pathlib import Path

import librosa
import numpy as np
import soundfile as sf
from pywav import WavRead, WavWrite
from pydub import AudioSegment
from gtts import gTTS

def twilio_mulaw_str__to__np_pcm_wav(twilio_audio_payload: str) -> np.ndarray:
    """
    Twilio audio payloads are mulaw audio encoded as utf-8 strings.
    Convert one of these to a numpy array of linear PCM WAV.
    """
    audio_bytes_mulaw: bytes = base64.b64decode(twilio_audio_payload)
    audio_bytes_linear_pcm_wav: bytes = audioop.ulaw2lin(audio_bytes_mulaw, 1)
    return np.frombuffer(audio_bytes_linear_pcm_wav, dtype=np.int8)

def np_pcm_wav__to__wav_filepath(np_pcm_wav: np.ndarray, wav_path: str | Path) -> None:
    """
    Write a numpy array of linear PCM WAV to a file.
    """
    assert Path(wav_path).parent.exists(), f"Expected {wav_path.parent} to exist"
    assert Path(wav_path).suffix == ".wav", f"Expected .wav file, got {wav_path}"
    normalized_audio: np.ndarray = librosa.util.normalize(np_pcm_wav.astype(np.float32))
    sf.write(str(wav_path), normalized_audio, 8000)

def mulaw_filepath__to__np_pcm_wav(mulaw_path: str | Path) -> np.ndarray:
    """
    Mulaw file is expected to be 8-bit mulaw format,
    which is how Twilio encodes audio.
    """
    assert Path(mulaw_path).exists(), f"Expected {mulaw_path} to exist"
    wav_read = WavRead(str(mulaw_path))
    audio_bytes = wav_read.getdata()
    audio_bytes = audioop.ulaw2lin(audio_bytes, 1)
    return np.frombuffer(audio_bytes, dtype=np.int8)

def mp3_filepath__to__twilio_mulaw_str(mp3_path: str | Path) -> str:
    assert Path(mp3_path).exists(), f"Expected {mp3_path} to exist"
    audio = AudioSegment.from_mp3(str(mp3_path))
    audio: bytes = audio.set_frame_rate(8000).set_channels(1).set_sample_width(1)
    mulaw_bytes: bytes = audioop.lin2ulaw(audio.raw_data, 1)
    return base64.b64encode(mulaw_bytes).decode("utf-8")

def text__to__mp3(text: str, mp3_path: str | Path) -> None:
    mp3_path = Path(mp3_path)
    assert mp3_path.suffix == ".mp3", f"Expected .mp3 file, got {mp3_path}"
    assert mp3_path.parent.exists(), f"Expected {mp3_path.parent} to exist"
    tts = gTTS(text=text, lang="en")
    tts.save(str(mp3_path))

def twilio_mulaw_str__to__pcm_wav_filepath__duplicate(twilio_mulaw_str: str, pcm_wav_path: str | Path) -> None:
    """
    Is this deprecated? Keep it in case cause it took me a while to find stuff that worked at all.
    """
    assert Path(pcm_wav_path).parent.exists(), f"Expected {pcm_wav_path.parent} to exist"
    assert Path(pcm_wav_path).suffix == ".wav", f"Expected .wav file, got {pcm_wav_path}"
    audio_bytes_mulaw: bytes = base64.b64decode(twilio_mulaw_str)
    wave_write = WavWrite(str(pcm_wav_path), 1, 8000, 8, 7)
    wave_write.write(audio_bytes_mulaw)
    wave_write.close()

