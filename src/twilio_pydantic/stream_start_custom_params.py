from pydantic import BaseModel

class StreamStartCustomParams(BaseModel):
    caller: str = "(empty)"
