import asyncio
import logging

import websockets

log = logging.getLogger('chat')

connections = set()


async def handler(websocket, _):
    websocket_id = id(websocket)
    log.info('New connection %d', websocket_id)

    connections.add(websocket)
    try:
        while True:
            message = await websocket.recv()
            log.info('From websocket=%d get new message=%s', websocket_id, message)
            await send_message(message)
    except websockets.exceptions.ConnectionClosed:
        log.info('websocket=%d left us', websocket_id)
    finally:
        connections.remove(websocket)


async def send_message(message):
    log.info('Send message="%s" to connections=%d', message, len(connections))
    # тут мы еще не отправляем сообщение
    tasks = [ws.send(message) for ws in connections]
    if tasks:
        await asyncio.wait(tasks)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    start_server = websockets.serve(handler, host='localhost', port=8765)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_server)
    try:
        loop.run_forever()
    finally:
        # нужно явно закрывать обработчика событий
        loop.close()
