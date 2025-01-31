from pydantic import BaseModel

from twilio_phone_calls.twilio_pydantic.stream_events_enum import StreamEventsEnum
from twilio_phone_calls.twilio_pydantic.stream_mark_payload import StreamMarkPayload

class OutgoingMarkMessage(BaseModel):
    """
    { 
        "event": "mark",
        "streamSid": "MZ18ad3ab5a668481ce02b83e7395059f0",
        "mark": {
            "name": "my label"
        }
    }
    """
    event: str = StreamEventsEnum.mark.value
    streamSid: str
    mark: StreamMarkPayload = StreamMarkPayload()

    @classmethod
    def create_default(cls, stream_sid: str):
        return cls(
            streamSid=stream_sid,
        )
