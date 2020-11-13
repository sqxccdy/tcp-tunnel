import asyncio

data2 = {}


class Connection(object):
    def __init__(self, reader, writer, gold_reader, gold_writer):
        self.reader = reader
        self.writer = writer
        self.gold_writer = gold_writer
        self.gold_reader = gold_reader
        self.closed = False

    async def run_writer(self):
        try:
            while not self.closed:
                try:
                    data = (await asyncio.wait_for(self.reader.read(4096), timeout=1))
                    self.gold_writer.write(data)
                except (ConnectionResetError, ConnectionAbortedError) as e:
                    break  # Client disconnected
                except asyncio.exceptions.TimeoutError:
                    pass
        finally:
            self.closed = True
            print('closed')

    async def run_reader(self):
        try:
            while not self.closed:
                try:
                    data = (await asyncio.wait_for(self.gold_reader.read(4096), timeout=1))
                    self.writer.write(data)
                except (ConnectionResetError, ConnectionAbortedError) as e:
                    break  # Client disconnected
                except asyncio.exceptions.TimeoutError:
                    pass
        finally:
            self.closed = True
            print('closed')


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
        print(f'Serving on {addr} {addr2}')
        while True:
            await asyncio.sleep(1)

    async def receive_conn(self, reader, writer):
        print('received conn')
        await self.queue.put((reader, writer))

    async def handle_echo(self, reader, writer):
        gold_reader, gold_writer = await self.queue.get()
        conn = Connection(reader, writer, gold_reader, gold_writer)
        self.loop.create_task(conn.run_writer())
        self.loop.create_task(conn.run_reader())
        print('create conn')


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
