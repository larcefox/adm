import asyncio
import websockets
import json


async def send_data(websocket, data):
    """Send data to the WebSocket server."""
    await websocket.send(json.dumps(data))
    print('Send:', data)

    # Optionally, wait for and print a response from the server
    response = await websocket.recv()
    print(f"Received: {response}")

async def websocket_client(data):
    uri = "ws://localhost:8765"  # Replace with your WebSocket server URI
    async with websockets.connect(uri) as websocket:

        # Use the send_data function to send the message
        await send_data(websocket, data)
        

# Run the WebSocket client
# asyncio.get_event_loop().run_until_complete(websocket_client())