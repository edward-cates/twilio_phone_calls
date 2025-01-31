from pathlib import Path
import traceback

import speech_recognition as sr

def voice_to_text(wav_path: str | Path) -> str:
    """
    Converts Linear PCM WAV (as opposed to mulaw) audio to text using SpeechRecognition (OpenAI Whisper).
    """
    assert Path(wav_path).exists(), f"Expected {wav_path} to exist"
    r = sr.Recognizer()
    with sr.AudioFile(str(wav_path)) as source:
        audio = r.record(source)
    try:
        # return r.recognize_google(audio)  # Use Google Speech Recognition engine
        return r.recognize_whisper(audio)
    except sr.UnknownValueError:
        raise Exception("Speech recognition could not understand audio.")
    except sr.RequestError as e:
        raise Exception(f"Could not request results from SpeechRecognition service; {e}")

def voice_to_text_safe(wav_path: str | Path) -> str:
    try:
        return voice_to_text(wav_path)
    except Exception as e:
        print(traceback.format_exc())
        return "I'm sorry, I didn't get that. Will you try again?"
