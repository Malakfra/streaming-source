import asyncio
import json
import random
from datetime import datetime, timezone
from uuid import uuid4

from fastapi import FastAPI
from fastapi.responses import StreamingResponse


# Create the API application.
app = FastAPI(title="QuickCart Order Streaming API")


# A simple endpoint to check whether the API is running.
@app.get("/")
def home():
    return {
        "message": "The order streaming API is running",
        "stream_endpoint": "/orders/stream"
    }


# Generate simulated order events continuously.
async def generate_orders():
    while True:
        order = {
            "event_id": str(uuid4()),
            "order_id": str(uuid4()),
            "event_type": "order_created",
            "event_time": datetime.now(timezone.utc).isoformat(),
            "customer_id": random.randint(1, 100),
            "amount": round(random.uniform(5, 200), 2),
            "currency": "JOD"
        }

        # Convert the Python dictionary into JSON text.
        json_text = json.dumps(order)

        # Send one message using Server-Sent Events format.
        yield f"data: {json_text}\n\n"

        # Wait three seconds before generating another order.
        await asyncio.sleep(3)


# The endpoint that clients connect to for streaming orders.
@app.get("/orders/stream")
async def stream_orders():
    return StreamingResponse(
        generate_orders(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache"}
    )