import asyncio
from tcp_tunnel.connection import Connection
from tcp_tunnel import logger


class LocationProxy(object):
    server2 = server = None

    def __init__(self, loop):
        self.queue = asyncio.Queue(maxsize=100)
        self.loop = loop

    async def serve(self):
        await self.create_conn()
        listen_reader, _ = await asyncio.open_connection('127.0.0.1', 8890)
        while True:
            if await listen_reader.read(1) == b'1':
                await self.create_conn()

    async def create_conn(self):
        reader, writer = await asyncio.open_connection('127.0.0.1', 8889)
        gold_reader, gold_writer = await asyncio.open_connection('127.0.0.1', 8000)
        conn = Connection(reader, writer, gold_reader, gold_writer, loop)
        loop.create_task(conn.run_writer())
        loop.create_task(conn.run_reader())
        logger.debug('create conn')


loop = asyncio.get_event_loop()
local_client = LocationProxy(loop)
future = asyncio.ensure_future(local_client.serve())
try:
    loop.run_forever()
except KeyboardInterrupt:
    future.cancel()
    loop.run_until_complete(future)
finally:
    # 不管是什么异常，最终都要close掉loop循环
    loop.close()
