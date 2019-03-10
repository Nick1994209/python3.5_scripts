import asyncio
import websockets


# функция будет вызываться при каждом новом подключении по вебсокету
async def handler(websocket, _):
    print('New connection')

    count = 0
    # в бесконечном цикле (пока websocket не покинет нас) будем каждые 2 секунды отправдять сообщение
    while True:
        await websocket.send('hello! %d' % count)
        await asyncio.sleep(2)
        count += 1


start_server = websockets.serve(handler, host='localhost', port=8765)
loop = asyncio.get_event_loop()
loop.run_until_complete(start_server)
loop.run_forever()
