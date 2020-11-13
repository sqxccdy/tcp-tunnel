import asyncio
from socket_ddns.remote_test import Connection


async def tcp_echo_client(message):
    for i in range(100):
        reader, writer = await asyncio.open_connection('127.0.0.1', 8889)
        gold_reader, gold_writer = await asyncio.open_connection('127.0.0.1', 8000)
        conn = Connection(reader, writer, gold_reader, gold_writer)
        loop.create_task(conn.run_writer())
        loop.create_task(conn.run_reader())
        print('create conn')

loop = asyncio.get_event_loop()
future = asyncio.ensure_future(tcp_echo_client('Hello World!'))
try:
    loop.run_forever()
except KeyboardInterrupt:
    future.cancel()
    loop.run_until_complete(future)
finally:
    # 不管是什么异常，最终都要close掉loop循环
    loop.close()
