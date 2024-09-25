import asyncio
import requests_sse
import aiohttp

async def sse_listener(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers={'Accept': 'text/event-stream'}) as response:
            client = requests_sse.SSEClient(response)
            async for event in client.events():
                if event.event == 'message':
                    print(f"Received event: {event.data}")
                elif event.event == 'error':
                    print(f"Error: {event.data}")

async def main():
    sse_url = "http://localhost:3000/api/events"
    
    # Start the SSE listener as a background task
    sse_task = asyncio.create_task(sse_listener(sse_url))
    
    # Your main program logic goes here
    try:
        while True:
            await asyncio.sleep(5)
    except asyncio.CancelledError:
        print("Main program cancelled")
    finally:
        # Cancel the SSE listener task when the main program exits
        sse_task.cancel()
        try:
            await sse_task
        except asyncio.CancelledError:
            print("SSE listener cancelled")