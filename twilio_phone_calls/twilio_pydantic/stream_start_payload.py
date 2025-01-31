from pydantic import BaseModel, Field

from twilio_phone_calls.twilio_pydantic.stream_start_custom_params import StreamStartCustomParams

class StreamStartPayload(BaseModel):
    accountSid: str
    streamSid: str
    callSid: str
    tracks: list
    mediaFormat: dict
    customParameters: StreamStartCustomParams = Field(default_factory=StreamStartCustomParams)
