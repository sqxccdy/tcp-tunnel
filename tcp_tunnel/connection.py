import asyncio
import sys

from tcp_tunnel import logger


class Connection(object):
    def __init__(self, reader, writer, gold_reader, gold_writer, loop):
        self.reader = reader
        self.writer = writer
        self.gold_writer = gold_writer
        self.gold_reader = gold_reader
        self.loop = loop
        self.stop_sign = loop.create_future()
        self.closed = False

    async def run_writer(self):
        try:
            while not self.closed:
                # incoming = asyncio.ensure_future(self.reader.read(sys.maxsize - 1))
                # done, pending = await asyncio.wait([incoming, self.stop_sign],
                #                                    return_when=asyncio.FIRST_COMPLETED)
                # if incoming in pending:
                #     incoming.cancel()
                # if incoming in done:
                #     data = incoming.result()
                #     self.gold_writer.write(data)
                # if self.stop_sign in done:
                #     break
                try:
                    data = (await asyncio.wait_for(self.reader.read(4096), timeout=1))
                    self.gold_writer.write(data)
                except (ConnectionResetError, ConnectionAbortedError) as e:
                    break  # Client disconnected
                except asyncio.exceptions.TimeoutError:
                    pass
        finally:
            self.closed = True
            self.gold_writer.close()
            logger.debug('closed')

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
                # incoming = asyncio.ensure_future(self.gold_reader.read(sys.maxsize - 1))
                # done, pending = await asyncio.wait([incoming, self.stop_sign],
                #                                    return_when=asyncio.FIRST_COMPLETED)
                # if incoming in pending:
                #     incoming.cancel()
                # if incoming in done:
                #     data = incoming.result()
                #     self.writer.write(data)
                # if self.stop_sign in done:
                #     break
        finally:
            self.closed = True
            self.writer.close()
            logger.debug('closed')
