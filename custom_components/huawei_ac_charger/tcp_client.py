import asyncio

class HuaweiTCPClient:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.reader = None
        self.writer = None
        self._lock = asyncio.Lock()
        self.connected = False

    async def connect(self):
        self.reader, self.writer = await asyncio.open_connection(self.ip, self.port)
        self.connected = True

    async def send_request(self, request):
        async with self._lock:
            self.writer.write(request)
            await self.writer.drain()

            # First, read exactly 7 bytes for MBAP header
            header = await self.reader.readexactly(7)

            # Extract the length from header bytes 4-5
            length = int.from_bytes(header[4:6], 'big')

            # Read exactly the 'length' bytes specified
            body = await self.reader.readexactly(length)

            response = header + body
            return response

    async def close(self):
        self.connected = False
        if self.writer:
            self.writer.close()
            await self.writer.wait_closed()