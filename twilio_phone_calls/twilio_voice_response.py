from twilio.twiml.voice_response import VoiceResponse, Connect, Stream

"""
In FastAPI, the form data for the call POST route is like this:

form FormData([
    ('AccountSid', '...'), 
    ('ApiVersion', '2010-04-01'), 
    ('CallSid', '...'), 
    ('CallStatus', 'ringing'), 
    ('CallToken', '...'), 
    ('Called', '+1...'),
    ('CalledCity', '...'), 
    ('CalledCountry', '...'), 
    ('CalledState', '...'), 
    ('CalledZip', '...'), 
    ('Caller', '+1...'), 
    ('CallerCity', '...'), 
    ('CallerCountry', 'US'), 
    ('CallerState', 'CA'), 
    ('CallerZip', '...'), 
    ('Direction', 'inbound'), 
    ('From', '+1...'), 
    ('FromCity', '...'), 
    ('FromCountry', 'US'), 
    ('FromState', 'CA'), 
    ('FromZip', '...'), 
    ('To', '+1...'), 
    ('ToCity', '...'), 
    ('ToCountry', 'US'), 
    ('ToState', 'CA'), 
    ('ToZip', '...')
])
"""

def create_twilio_voice_response(
    caller_number: str,
    websocket_url: str,
) -> VoiceResponse:
    response = VoiceResponse()
    connect = Connect()
    stream = Stream(name="stream", url=websocket_url)
    stream.parameter('caller', caller_number)
    connect.append(stream)
    response.append(connect)
    return response

