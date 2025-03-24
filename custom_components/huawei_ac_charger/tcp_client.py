import asyncio
import logging

_LOGGER = logging.getLogger(__name__)

class HuaweiTCPClient:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.reader = None
        self.writer = None
        self._lock = asyncio.Lock()
        self.connected = False

    async def connect(self):
        try:
            self.reader, self.writer = await asyncio.open_connection(self.ip, self.port)
            self.connected = True
            _LOGGER.debug("Connected successfully to Huawei Charger")
        except Exception as e:
            self.connected = False
            _LOGGER.error(f"Connection error: {e}")

    async def ensure_connected(self):
        if not self.connected or self.writer is None or self.writer.is_closing():
            await self.connect()

    async def send_request(self, request):
        async with self._lock:
            await self.ensure_connected()

            if not self.connected:
                _LOGGER.error("Cannot send request, connection not established.")
                return None

            try:
                self.writer.write(request)
                await self.writer.drain()

                # Read MBAP header (7 bytes)
                header = await self.reader.readexactly(7)
                length = int.from_bytes(header[4:6], 'big')

                # Read the specified number of remaining bytes
                body = await self.reader.readexactly(length)

                response = header + body
                return response

            except (asyncio.IncompleteReadError, BrokenPipeError) as e:
                _LOGGER.error(f"Connection lost, attempting to reconnect: {e}")
                self.connected = False
                await self.connect()
                return None
            except Exception as e:
                _LOGGER.error(f"Unexpected error during communication: {e}")
                self.connected = False
                return None

    async def close(self):
        self.connected = False
        if self.writer:
            self.writer.close()
            await self.writer.wait_closed()