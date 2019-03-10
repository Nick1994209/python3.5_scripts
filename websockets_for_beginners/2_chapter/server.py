import asyncio
import websockets


connections = []


async def send_message(message):
    for websocket in connections:
        await websocket.send(message)


async def handler(websocket, _):
    print('New connection')
    connections.append(websocket)

    while True:
        message = await websocket.recv()
        await send_message(message)


start_server = websockets.serve(handler, host='localhost', port=8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
