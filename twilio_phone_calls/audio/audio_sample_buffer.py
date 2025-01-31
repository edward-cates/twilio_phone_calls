import numpy as np

class AudioSampleBuffer:
    """
    Concat audio until a pause that denotes the sample is complete.
    """
    def __init__(self):
        self._audio_buffer = np.empty(0, dtype=np.int8)
        self._nonempty_threshold = 8
        self._pause_size = 10000
        self._min_total = 1000
        self._padding = 1000

    def append(self, data: np.ndarray) -> None:
        self._audio_buffer = np.concatenate([self._audio_buffer, data])

    def count_trailing_empty_audio(self) -> int:
        not_empty = np.abs(self._audio_buffer) >= self._nonempty_threshold
        return int(np.argmax(not_empty[::-1]))

    def nonempty_total(self) -> int:
        return int(np.sum(np.abs(self._audio_buffer) >= self._nonempty_threshold))

    def has_paused(self) -> bool:
        has_had_significant_audio = self.nonempty_total() >= self._min_total
        if not has_had_significant_audio:
            return False
        return self.count_trailing_empty_audio() >= self._pause_size

    def crop_audio(self) -> np.ndarray:
        starting_index = max(0, self.first_nonempty_index - self._padding)
        ending_index = min(len(self._audio_buffer), self.last_nonempty_index + self._padding)
        return self._audio_buffer[starting_index:ending_index]

    @property
    def first_nonempty_index(self) -> int:
        is_nonempty = np.abs(self._audio_buffer) > self._nonempty_threshold
        return int(np.argmax(is_nonempty))

    @property
    def last_nonempty_index(self) -> int:
        is_nonempty = np.abs(self._audio_buffer) > self._nonempty_threshold
        return int(len(self._audio_buffer) - np.argmax(is_nonempty[::-1]))
