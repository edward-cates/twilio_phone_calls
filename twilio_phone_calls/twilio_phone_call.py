import traceback
from typing import Callable, Awaitable

import numpy as np
import torch

from .twilio_pydantic.stream_events_enum import StreamEventsEnum
from .twilio_pydantic.stream_start_message import StreamStartMessage
from .twilio_pydantic.stream_media_message import StreamMediaMessage
from .twilio_pydantic.outgoing_media_message import OutgoingMediaMessage
from .twilio_pydantic.outgoing_mark_message import OutgoingMarkMessage
from .twilio_pydantic.outgoing_clear_message import OutgoingClearMessage
from .audio.audio_sample_buffer import AudioSampleBuffer
from .audio.voice_to_text import voice_to_text_safe
from .audio.text_to_voice import text__to__wav_filepath
from .audio.tmp_file_path import TmpFilePath
from .audio.audio_conversions import (
    text__to__mp3,
    mp3_filepath__to__twilio_mulaw_str,
    twilio_mulaw_str__to__np_pcm_wav,
    np_pcm_wav__to__wav_filepath,
    wav_filepath__to__np_pcm_wav,
    np_pcm_wav__to__twilio_mulaw_str,
)

class TwilioPhoneCall:
    def __init__(
        self,
        start_message: StreamStartMessage,
        send_websocket_message_async_method: Callable[[str], Awaitable[None]],
        text_to_text_async_method: Callable[[str], Awaitable[str]],
    ):
        assert start_message.event == StreamEventsEnum.start.value
        self.start_message = start_message
        self._send_websocket_message_async_method = send_websocket_message_async_method
        self._text_to_text_async_method = text_to_text_async_method
        self._audio_buffer = AudioSampleBuffer()

    @classmethod
    def from_start_message(
        cls,
        twilio_message: dict,
        send_websocket_message_async_method: Callable[[str], Awaitable[None]],
        text_to_text_async_method: Callable[[str], Awaitable[str]],
    ):
        assert twilio_message["event"] == StreamEventsEnum.start.value, \
            f"Expected start message, got {twilio_message['event']=}"
        return cls(
            start_message=StreamStartMessage.model_validate(twilio_message),
            send_websocket_message_async_method=send_websocket_message_async_method,
            text_to_text_async_method=text_to_text_async_method,
        )

    @property
    def caller(self) -> str:
        return self.start_message.caller

    @property
    def stream_sid(self) -> str:
        return self.start_message.streamSid

    async def receive_twilio_message(self, twilio_message: dict) -> None:
        """
        This message determines whether this is a media or mark message
        and calls the appropriate method, which returns messages to send back
        in JSON-string format.
        """
        if twilio_message["event"] == StreamEventsEnum.media.value:
            await self._receive_media_message(StreamMediaMessage.model_validate(twilio_message))
        elif twilio_message["event"] == StreamEventsEnum.mark.value:
            """
            A mark message is received in confirmation of our outgoing messages.
            We shouldn't get one unless we just sent something.
            """
            pass
        else:
            print(f"[warning:phone_call.py] Received other message type: {twilio_message['event']=}")

    async def send_text_as_audio(self, text: str) -> None:
        """
        Convert a text message to the twilio message that need to be sent
        to send it as voice-audio to the caller.
        """
        if not torch.cuda.is_available():
            with TmpFilePath("mp3") as tmp_file_path:
                text__to__mp3(text, tmp_file_path)
                twilio_mulaw_str: str = mp3_filepath__to__twilio_mulaw_str(tmp_file_path)
            outgoing_media_message = OutgoingMediaMessage.from_sid_and_mulaw_str(
                stream_sid=self.stream_sid,
                twilio_mulaw_str=twilio_mulaw_str,
            )
        else:
            with TmpFilePath("wav") as tmp_file_path:
                try:
                    text__to__wav_filepath(text, tmp_file_path)
                    np_pcm_wav: np.ndarray = wav_filepath__to__np_pcm_wav(tmp_file_path)
                    twilio_mulaw_str: str = np_pcm_wav__to__twilio_mulaw_str(np_pcm_wav)
                except Exception as e:
                    traceback.print_exc()
                    raise e
            outgoing_media_message = OutgoingMediaMessage.from_sid_and_mulaw_str(
                stream_sid=self.stream_sid,
                twilio_mulaw_str=twilio_mulaw_str,
            )
        outgoing_mark_message = OutgoingMarkMessage.create_default(
            stream_sid=self.stream_sid,
        )
        await self._send_websocket_message_async_method(
            outgoing_media_message.model_dump_json()
        )
        await self._send_websocket_message_async_method(
            outgoing_mark_message.model_dump_json()
        )

    # Private.

    async def _receive_media_message(self, stream_media_message: StreamMediaMessage) -> None:
        """
        Will return parsed_audio if a pause from the caller is detected, otherwise None.
        """
        audio_chunk: np.ndarray = twilio_mulaw_str__to__np_pcm_wav(stream_media_message.media.payload)

        had_started = self._audio_buffer.check_has_started()
        self._audio_buffer.append(audio_chunk)
        just_started = (not had_started) and self._audio_buffer.check_has_started()

        if just_started:
            print(f"[debug:twilio_phone_call.py] Just started - interrupting.")
            await self._send_websocket_message_async_method(
                OutgoingClearMessage.create_default(stream_sid=self.stream_sid).model_dump_json()
            )

        if self._audio_buffer.check_has_finished():
            print(f"[debug:twilio_phone_call.py] Pause detected - processing.")
            parsed_audio: np.ndarray = self._audio_buffer.crop_audio()
            self._audio_buffer = AudioSampleBuffer() # New clean buffer.
            with TmpFilePath("wav") as tmp_file_path:
                np_pcm_wav__to__wav_filepath(np_pcm_wav=parsed_audio, wav_path=tmp_file_path)
                caller_text: str = voice_to_text_safe(wav_path=tmp_file_path)
                print(f"[debug:twilio_phone_call.py] Caller text deciphered: {caller_text=}")
                response_text: str = await self._text_to_text_async_method(caller_text)
                await self.send_text_as_audio(response_text)
