from pydantic import BaseModel

class OutgoingMediaPayload(BaseModel):
    """
    "media": {
        "payload": encoded_str,
    }
    """
    payload: str
