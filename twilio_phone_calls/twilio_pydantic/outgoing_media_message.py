from pathlib import Path

from pydantic import BaseModel

from twilio_phone_calls.twilio_pydantic.stream_events_enum import StreamEventsEnum
from twilio_phone_calls.twilio_pydantic.outgoing_media_payload import OutgoingMediaPayload

class OutgoingMediaMessage(BaseModel):
    """
    {
        "event": "media",
        "streamSid": get_stream_sid(),
        "media": {
            "payload": encoded_str,
        }
    }
    """
    event: str = StreamEventsEnum.media.value
    streamSid: str
    media: OutgoingMediaPayload

    @classmethod
    def from_sid_and_mulaw_str(cls, stream_sid: str, twilio_mulaw_str: str):
        return cls(
            streamSid=stream_sid,
            media=OutgoingMediaPayload(payload=twilio_mulaw_str),
        )
