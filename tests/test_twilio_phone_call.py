from pathlib import Path
import json

from tqdm import tqdm

from twilio_phone_calls import TwilioPhoneCall

class MockClient:
    def __init__(self):
        self.second_to_last_message_text = ""
        self.last_message_text = ""

    async def send_text(self, text: str) -> None:
        self.second_to_last_message_text = self.last_message_text
        self.last_message_text = text

    async def text_to_text(self, text: str) -> str:
        return text

    def get_acknowledge_mark_message_text(self) -> str:
        return """{ 
            "event": "mark",
            "sequenceNumber": "4",
            "streamSid": "test_stream",
            "mark": {
                "name": "ack"
            }
        }"""


async def test_twilio_stream():
    data_file = Path("tests/fixtures/stream1.txt")
    """
    Each line of text is a json message.
    """
    with data_file.open() as f:
        lines = f.readlines()
    start_message = lines[1]
    media_lines = lines[2:-1]

    client = MockClient()

    """
    Constructor will send "Hello from jarvis", or similar prompt.
    """
    stream = TwilioPhoneCall.from_start_message(
        json.loads(start_message),
        send_websocket_message_async_method=client.send_text,
        text_to_text_async_method=client.text_to_text,
    )
    assert stream is not None

    print("Caller:", stream.start_message.caller)

    await stream.send_text_as_audio("Welcome")

    last_media_message_text = client.second_to_last_message_text
    assert client.last_message_text == """{"event":"mark","streamSid":"test_stream","mark":{"name":"ack"}}""", \
        client.last_message_text

    """
    Agent should start listening once mark message is received.
    """
    await stream.receive_twilio_message(json.loads(client.get_acknowledge_mark_message_text()))

    def assert_section_complete(client, stream, last_media_message_text):
        assert client.second_to_last_message_text != last_media_message_text
        assert not stream.is_listening
        stream.receive_twilio_message(json.loads(client.get_acknowledge_mark_message_text()))
        assert stream.is_listening

    # send all the media
    for ix, line in tqdm(enumerate(media_lines), total=len(media_lines)):
        await stream.receive_twilio_message(json.loads(line))

        if ix == 323:
            assert_section_complete(client, stream, last_media_message_text)
            last_media_message_text = client.second_to_last_message_text

        elif ix == 550:
            assert_section_complete(client, stream, last_media_message_text)
            last_media_message_text = client.second_to_last_message_text

    # assert False

