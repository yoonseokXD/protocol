import asyncio

async def pingpong_client():
    try:
        reader, writer = await asyncio.open_connection(host='localhost',port=8000)
    except OSError:
        print('connection fail')
        return
    
    for _ in range(10):
        writer.write(b'ping')
        print('send: ping')
        
        data = await reader.read(8)
        print('recv:',data.decode())
        await asyncio.sleep(1)
    
    writer.write(b'done')
    print('send: ping')
    writer.close()
    await writer.wait_closed()
    print('connection was closed')
    


if __name__ == "__main__":
    
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None
    
    if loop and loop.is_running():
        print('Async event loop already running')
        tsk = loop.create_task(pingpong_client())
    else:
        print('Starting new event loop')
        asyncio.run(pingpong_client())