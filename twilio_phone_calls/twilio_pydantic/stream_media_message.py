from pydantic import BaseModel

from .twilio_stream_message import TwilioStreamMessage
from .stream_media_payload import StreamMediaPayload

class StreamMediaMessage(TwilioStreamMessage):
    """
    {
    "event": "media",
    "sequenceNumber": "2",
    "media": {
        "track": "inbound",
        "chunk": "1",
        "timestamp": "135",
        "payload": "/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////w=="
    },
    "streamSid": "MZ7c8817f8a231170163c51f360708d9a2"
    }
    """
    media: StreamMediaPayload
