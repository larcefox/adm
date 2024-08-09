import asyncio
import websockets


async def send_data(websocket, user, data):
    """Send data to the WebSocket server."""
    await websocket.send(str({user: data}))
    print('Send:', str({user: data}))

    # Optionally, wait for and print a response from the server
    response = await websocket.recv()
    print(f"Received: {response}")

async def websocket_client(user, data):
    uri = "ws://localhost:8765"  # Replace with your WebSocket server URI
    async with websockets.connect(uri) as websocket:

        # Use the send_data function to send the message
        await send_data(websocket, user, data)
        

# Run the WebSocket client
# asyncio.get_event_loop().run_until_complete(websocket_client())