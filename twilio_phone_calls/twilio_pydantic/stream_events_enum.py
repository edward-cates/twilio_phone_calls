import enum

class StreamEventsEnum(enum.Enum):
    connected = "connected"
    start = "start"
    media = "media"
    mark = "mark"
    stop = "stop"
    clear = "clear"
