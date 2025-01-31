from pydantic import BaseModel

class StreamMarkPayload(BaseModel):
    """
    "mark": {
        "name": "my label"
    }
    """
    name: str = "ack"
