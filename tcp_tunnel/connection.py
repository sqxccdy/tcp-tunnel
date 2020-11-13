import asyncio


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
