import aiohttp
import asyncio
import json
from app.audiogen import audiogen
from app.config import load_config

config = load_config()

async def start_sse_listener(app):
    while True:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{config.API_URL}/events/{config.EVENT_ENDPOINT}") as response:
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
            break
        except Exception as e:
            break
        
        # Wait before attempting to reconnect
        await asyncio.sleep(5)