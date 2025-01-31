import pytest

from twilio.twiml.voice_response import VoiceResponse, Connect, Stream

@pytest.mark.skip(reason="Need a server running.")
def test_server_call_response_xml():
    response = VoiceResponse()
    connect = Connect()
    stream = Stream(
        name="stream",
        url="ws://localhost:8000/stream",
    )
    stream.parameter('caller', '+1...')
    connect.append(stream)
    response.append(connect)
    xml_content = response.to_xml()
    expected_xml = """<?xml version="1.0" encoding="UTF-8"?><Response><Connect><Stream name="stream" url="ws://localhost:8000/stream"><Parameter name="caller" value="+1..." /></Stream></Connect></Response>"""
    assert xml_content == expected_xml

if __name__ == "__main__":
    test_server_call_response_xml()
    print("Tests pass.")
