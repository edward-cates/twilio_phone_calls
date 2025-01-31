from twilio_phone_calls.twilio_pydantic.twilio_stream_message import TwilioStreamMessage

class StreamStopMessage(TwilioStreamMessage):
    """
    {
        "event": "stop",
        "sequenceNumber": "618",
        "streamSid": "MZ7c8817f8a231170163c51f360708d9a2",
        "stop": {
            "accountSid": "AC64f4d8c1481c0a5ac9cdbe997bfbcf58",
            "callSid": "CA3ae75ffe1c5d8847e478556c07d07103"
        }
    }
    """
    stop: dict
