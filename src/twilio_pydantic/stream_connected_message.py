from pydantic import BaseModel

class StreamConnectedPayload(BaseModel):
    """
    {"event":"connected","protocol":"Call","version":"1.0.0"}
    """
    event: str = "connected"
    protocol: str
    version: str
