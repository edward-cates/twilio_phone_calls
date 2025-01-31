
from .twilio_stream_message import TwilioStreamMessage
from .stream_mark_payload import StreamMarkPayload

class StreamMarkMessage(TwilioStreamMessage):
    """
    { 
        "event": "mark",
        "sequenceNumber": "4",
        "streamSid": "MZ18ad3ab5a668481ce02b83e7395059f0",
        "mark": {
            "name": "my label"
        }
    }
    """
    mark: StreamMarkPayload
