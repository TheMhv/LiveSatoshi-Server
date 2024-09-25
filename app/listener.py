import aiohttp
import asyncio
import json
from app.audiogen import audiogen

async def start_sse_listener(app):
    while True:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get("http://localhost:3000/api/events") as response:
                    async for line in response.content:
                        if line:
                            decoded_line = line.decode('utf-8').strip()
                            if decoded_line.startswith('data: '):
                                data = decoded_line[6:]
                                try:
                                    event_data = json.loads(data)
                                    if 'message' in event_data and event_data['message'] == 'Heartbeat':
                                        # Heartbeat received, do nothing
                                        pass
                                    elif 'text' in event_data and 'model' in event_data:
                                        # Process the event
                                        print(f"Received event: {event_data}")
                                        audio_data = await audiogen(text=event_data['text'], model_name=event_data['model'])

                                        await app.queue.put(json.dumps({
                                            "text": event_data['text'],
                                            "audio": audio_data.decode("utf-8"),
                                        }))
                                except json.JSONDecodeError:
                                    print(f"Failed to parse JSON: {data}")
        except aiohttp.ClientError as e:
            print(f"Connection error: {e}")
        except asyncio.CancelledError:
            break
        except Exception as e:
            print(f"Unexpected error: {e}")
        
        # Wait before attempting to reconnect
        await asyncio.sleep(5)