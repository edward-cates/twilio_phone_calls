import numpy as np

from twilio_phone_calls.twilio_pydantic.stream_events_enum import StreamEventsEnum
from twilio_phone_calls.twilio_pydantic.stream_start_message import StreamStartMessage
from twilio_phone_calls.twilio_pydantic.stream_media_message import StreamMediaMessage
from twilio_phone_calls.twilio_pydantic.stream_mark_message import StreamMarkMessage
from twilio_phone_calls.twilio_pydantic.outgoing_media_message import OutgoingMediaMessage
from twilio_phone_calls.twilio_pydantic.outgoing_mark_message import OutgoingMarkMessage
from twilio_phone_calls.audio.audio_stream_listener import AudioStreamListener
from twilio_phone_calls.audio.voice_to_text import voice_to_text_safe
from twilio_phone_calls.audio.tmp_file_path import TmpFilePath
from twilio_phone_calls.audio.audio_conversions import (
    text__to__mp3,
    mp3_filepath__to__twilio_mulaw_str,
    twilio_mulaw_str__to__np_pcm_wav,
    np_pcm_wav__to__wav_filepath,
)

class TwilioPhoneCall:
    def __init__(self, start_message: StreamStartMessage):
        assert start_message.event == StreamEventsEnum.start.value
        self.start_message = start_message

        """
        Start off talking and not listening (Welcome! message).
        Once that's send, we'll stop talking and listen.
        """
        self._stream_listener = None

        """
        A string in `_mailbox` represents a message from the caller that hasn't been answered yet.
        """
        self._mailbox: str | None = None

    @classmethod
    def from_start_message(cls, twilio_message: dict):
        assert twilio_message["event"] == StreamEventsEnum.start.value, \
            f"Expected start message, got {twilio_message['event']=}"
        return cls(
            start_message=StreamStartMessage.model_validate(twilio_message),
        )

    @property
    def caller(self) -> str:
        return self.start_message.caller

    @property
    def stream_sid(self) -> str:
        return self.start_message.streamSid
    
    def stop_listening_and_talk(self) -> None:
        assert self.is_listening, "Confused: Not listening."
        self._stream_listener = None

    def stop_talking_and_listen(self) -> None:
        assert not self.is_listening, "Confused: Already listening."
        self._stream_listener = AudioStreamListener()

    @property
    def is_listening(self) -> bool:
        return self._stream_listener is not None

    def receive_twilio_message(self, twilio_message: dict) -> None:
        """
        This message determines whether this is a media or mark message
        and calls the appropriate method, which returns messages to send back
        in JSON-string format.
        """
        if twilio_message["event"] == StreamEventsEnum.media.value:
            self._receive_media_message(StreamMediaMessage.model_validate(twilio_message))
        elif twilio_message["event"] == StreamEventsEnum.mark.value:
            """
            A mark message is received in confirmation of our outgoing messages.
            We shouldn't get one unless we just sent something.
            """
            self.stop_talking_and_listen()
        else:
            print(f"[warning:phone_call.py] Received other message type: {twilio_message['event']=}")

    def text__to__twilio_messages(self, text: str) -> list[str]:
        """
        Convert a text message to the twilio message that need to be sent
        to send it as voice-audio to the caller.
        """
        with TmpFilePath("mp3") as tmp_file_path:
            text__to__mp3(text, tmp_file_path)
            twilio_mulaw_str: str = mp3_filepath__to__twilio_mulaw_str(tmp_file_path)
        outgoing_media_message = OutgoingMediaMessage.from_sid_and_mulaw_str(
            stream_sid=self.stream_sid,
            twilio_mulaw_str=twilio_mulaw_str,
        )
        outgoing_mark_message = OutgoingMarkMessage.create_default(
            stream_sid=self.stream_sid,
        )
        return [
            outgoing_media_message.model_dump_json(),
            outgoing_mark_message.model_dump_json(),
        ]

    def check_mailbox(self) -> str | None:
        """
        Check the mailbox for a message from the caller.
        """
        mail = self._mailbox
        self._mailbox = None
        return mail

    # Private.

    def _receive_media_message(self, stream_media_message: StreamMediaMessage) -> None:
        # Ignore incoming audio while we're talking and not listening.
        if self._stream_listener is not None:
            """
            Will return parsed_audio if a pause from the caller is detected, otherwise None.
            """
            audio_chunk: np.ndarray = twilio_mulaw_str__to__np_pcm_wav(stream_media_message.media.payload)
            parsed_audio: np.ndarray | None = self._stream_listener.read_next_chunk(audio_chunk)
            if parsed_audio is not None:
                with TmpFilePath("wav") as tmp_file_path:
                    np_pcm_wav__to__wav_filepath(np_pcm_wav=parsed_audio, wav_path=tmp_file_path)
                    self._mailbox = voice_to_text_safe(wav_path=tmp_file_path)
                    print(f"[debug:twilio_phone_call.py] Caller text deciphered: {self._mailbox=}")
                self.stop_listening_and_talk()
