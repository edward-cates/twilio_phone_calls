"""
FastAPI server for the frontend
"""

from datetime import datetime
import sys
from typing import Optional

from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import Response
from twilio.twiml.voice_response import VoiceResponse, Connect, Stream

from src.twilio_phone_call import TwilioStream

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
    print("Websocket opened.")
    sys.stdout.flush()
    await websocket.accept()
    stream: Optional[TwilioStream] = None
    while True:
        try:
            text = await websocket.receive_text()
        except WebSocketDisconnect:
            print("Websocket closed.")
            break

        if stream is None:
            # TODO: Why would it still be none?
            stream: Optional[TwilioStream] = TwilioStream.parse_message_text(text)
            if stream is not None:
                print(f"TwilioStream created: {stream.caller=}")
                for response in stream.get_welcome_message_texts():
                    await websocket.send_text(response)
        else:
            for response in stream.receive_message_text(text):
                await websocket.send_text(response)

