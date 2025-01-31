"""
FastAPI server for the frontend
"""

import json
import sys
from datetime import datetime

from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import Response
from twilio.twiml.voice_response import VoiceResponse, Connect, Stream

from src.twilio_phone_call import TwilioPhoneCall
from src.twilio_pydantic.stream_events_enum import StreamEventsEnum

URL = "4a95-2605-a601-a314-f100-b967-1001-fbf6-7ef2.ngrok-free.app"

app = FastAPI()

start_time = datetime.now()

# hello world
@app.get("/")
async def root():
    print("Received hello world request")
    return {"message": f"Hello World {start_time}"}

@app.post("/")
async def phone_call(request: Request):
    print("Received phone call")
    form_data = await request.form()
    """
    EXAMPLE
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
        ('ToZip', '...')])
    """
    caller_number = form_data.get("Caller")
    print(f"Caller number: {caller_number}")
    response = VoiceResponse()
    connect = Connect()
    stream = Stream(
        name="stream",
        url=f"wss://{URL}/stream",
    )
    stream.parameter('caller', caller_number)
    connect.append(stream)
    response.append(connect)
    xml_content = response.to_xml()
    response = Response(content=xml_content, media_type="application/xml")
    return response

@app.websocket("/stream")
async def stream(websocket: WebSocket):
    try:
        await websocket.accept()
        print("Websocket opened.")
        sys.stdout.flush() # TODO: Is this needed?

        stream: TwilioPhoneCall | None = None

        async def _send_text_to_caller(text: str) -> None:
            assert stream is not None, "Stream not created."
            for response in stream.text__to__twilio_messages(text):
                await websocket.send_text(response)

        while True:
            twilio_json = await websocket.receive_text()
            twilio_message: dict = json.loads(twilio_json)

            if twilio_message["event"] == StreamEventsEnum.connected.value:
                print("Connected to Twilio.")
                continue

            if stream is None:
                stream = TwilioPhoneCall.from_start_message(twilio_message)
                print(f"TwilioPhoneCall created: {stream.caller=}")
                await _send_text_to_caller("Hey! How can I help you?")
            else:
                """
                Voice samples are split across (very) many twilio messages.
                Once a full sample has been pieced together
                and a long pause detected, the voice message will be processed
                and a response (i.e. `mail`) provided.
                """
                stream.receive_twilio_message(twilio_message)
                mail: str | None = stream.check_mailbox()
                if mail is not None:
                    await _send_text_to_caller(mail)
    except WebSocketDisconnect:
        print("Websocket closed.")

