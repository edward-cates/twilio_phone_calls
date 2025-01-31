# Twilio 

This is the gist (see [`src/fastapi.py`](src/fastapi.py) for the full example).

```python
...

def parrot(text: str) -> str:
    return text

@app.post("/")
async def phone_call(request: Request):
    form_data = await request.form()
    voice_response = create_twilio_voice_response(
        caller_number=form_data.get("Caller"),
        websocket_url="wss://4a95-2605-a601-a314-f100-b967-1001-fbf6-7ef2.ngrok-free.app/stream",
    )
    response = Response(
        content=voice_response.to_xml(),
        media_type="application/xml",
    )
    return response

@app.websocket("/stream")
async def stream(websocket: WebSocket):
    ...

    stream: TwilioPhoneCall | None = None

    ...

    while True:
        twilio_json = await websocket.receive_text()
        twilio_message: dict = json.loads(twilio_json)

        ...

        if stream is None:
            # Call created.
            stream = TwilioPhoneCall.from_start_message(twilio_message)
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
                response: str = parrot(mail)
                await _send_text_to_caller(response)

...
```
