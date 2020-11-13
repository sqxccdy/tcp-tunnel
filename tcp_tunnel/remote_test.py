import asyncio
from tcp_tunnel import logger
from tcp_tunnel.connection import Connection

data2 = {}


class DuplexConnection(object):
    server2 = server = None

    def __init__(self, loop):
        self.queue = asyncio.Queue(maxsize=100)
        self.loop = loop

    async def serve(self):
        self.server2 = await asyncio.start_server(self.receive_conn, '127.0.0.1', 8889)
        self.server = await asyncio.start_server(self.handle_echo, '127.0.0.1', 8888)
        addr = self.server.sockets[0].getsockname()
        addr2 = self.server2.sockets[0].getsockname()
        logger.info(f'Serving on {addr} {addr2}')
        while True:
            await asyncio.sleep(1)

    async def receive_conn(self, reader, writer):
        logger.debug('received conn')
        await self.queue.put((reader, writer))

    async def handle_echo(self, reader, writer):
        gold_reader, gold_writer = await self.queue.get()
        conn = Connection(reader, writer, gold_reader, gold_writer)
        self.loop.create_task(conn.run_writer())
        self.loop.create_task(conn.run_reader())
        logger.debug('create conn')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    duplex_app = DuplexConnection(loop)
    future = asyncio.ensure_future(duplex_app.serve())
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        future.cancel()
        loop.run_until_complete(future)
    finally:
        # 不管是什么异常，最终都要close掉loop循环
        loop.close()
