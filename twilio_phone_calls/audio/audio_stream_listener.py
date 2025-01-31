from typing import Optional

import numpy as np

from twilio_phone_calls.audio.audio_sample_buffer import AudioSampleBuffer

class AudioStreamListener:
    """
    Listens to the audio stream, detects a pause,
    and returns the full audio sample.
    Like a person listening to morse code, deciphering the message.
    """
    def __init__(self):
        self._audio_sample_buffer = AudioSampleBuffer()
        self._is_listening = True
        """
        Chunk buffer is purely for drawing artifacts.
        Chunks are too small to draw individually and be useful to see.
        """
        self._chunk_buffer = np.empty(0, dtype=np.int8)
        self._chunk_buffer_max_size = 40000

    def read_next_chunk(self, audio_data: np.ndarray) -> Optional[np.ndarray]:
        """
        Take the next chunk of audio and add it to the buffer.
        If the whole sample is complete (i.e. the buffer detects a pause),
        return the (cleaned up) full audio sample.
        """
        if not self._is_listening:
            return None

        self._chunk_buffer = np.concatenate([self._chunk_buffer, audio_data])

        if len(self._chunk_buffer) > self._chunk_buffer_max_size:
            self._chunk_buffer = np.empty(0, dtype=np.int8)

        self._audio_sample_buffer.append(audio_data)
        if self._audio_sample_buffer.has_paused():
            print("[debug:audio_stream_listener.py] Pause in caller audio detected.")
            self._is_listening = False
            return self._audio_sample_buffer.crop_audio()

        return None

