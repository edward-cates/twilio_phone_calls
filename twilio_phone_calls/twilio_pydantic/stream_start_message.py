from twilio_phone_calls.twilio_pydantic.twilio_stream_message import TwilioStreamMessage
from twilio_phone_calls.twilio_pydantic.stream_start_payload import StreamStartPayload

class StreamStartMessage(TwilioStreamMessage):
    """
    {
    "event": "start",
    "sequenceNumber": "1",
    "start": {
        "accountSid": "AC64f4d8c1481c0a5ac9cdbe997bfbcf58",
        "streamSid": "MZ7c8817f8a231170163c51f360708d9a2",
        "callSid": "CA3ae75ffe1c5d8847e478556c07d07103",
        "tracks": ["inbound"],
        "mediaFormat": {
            "encoding": "audio/x-mulaw",
            "sampleRate": 8000,
            "channels": 1
        }
    },
    "streamSid": "MZ7c8817f8a231170163c51f360708d9a2"
    }
    """
    start: StreamStartPayload

    @property
    def caller(self) -> str:
        return self.start.customParameters.caller
