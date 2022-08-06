from aitextgen import aitextgen
import asyncio
import json
import websockets

port = 5678

global ai
ai = aitextgen()

async def handle_textgen_requests(websocket, path):
  global ai
  async for data in websocket:
    request = json.loads(data)
    print("< {}".format(request))
    continuation = ai.generate_one(prompt=str(request["text"]))
    reply = {"text": continuation, "id": request["id"]}
    await websocket.send(json.dumps(reply))
    print("> {}".format(reply))

start_server = websockets.serve(handle_textgen_requests, 'localhost', port)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
