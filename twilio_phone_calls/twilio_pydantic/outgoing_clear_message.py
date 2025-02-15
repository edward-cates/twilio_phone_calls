from pydantic import BaseModel

from .stream_events_enum import StreamEventsEnum

class OutgoingClearMessage(BaseModel):
    """
    This message is used to interrupt the outgoing audio (clear the buffer).
    https://www.twilio.com/docs/voice/media-streams/websocket-messages

    { 
        "event": "clear",
        "streamSid": "MZ18ad3ab5a668481ce02b83e7395059f0",
    }
    """
    event: str = StreamEventsEnum.clear.value
    streamSid: str

    @classmethod
    def create_default(cls, stream_sid: str):
        return cls(
            streamSid=stream_sid,
        )
