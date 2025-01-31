from pydantic import BaseModel

class TwilioStreamMessage(BaseModel):
    event: str
    sequenceNumber: str
    streamSid: str
