
import asyncio

class HuaweiTCPClient:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.reader = None
        self.writer = None

    async def connect(self):
        self.reader, self.writer = await asyncio.open_connection(self.ip, self.port)

    async def send_request(self, request):
        self.writer.write(request)
        await self.writer.drain()
        response = await self.reader.read(1024)
        return response

    async def close(self):
        if self.writer:
            self.writer.close()
            await self.writer.wait_closed()
