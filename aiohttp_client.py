import logging

from aiohttp import ClientSession, ClientTimeout, TCPConnector

SIZE_POOL_AIOHTTP = 100
MAX_RETRIES = 3
TIMEOUT = 15

logger = logging.getLogger(__name__)


class AiohttpSession:
    def __init__(self):
        self.session: ClientSession = None

    async def get(self) -> ClientSession:
        if self.session is None:
            timeout = ClientTimeout(total=TIMEOUT)
            connector = TCPConnector(limit_per_host=SIZE_POOL_AIOHTTP)
            self.session = ClientSession(timeout=timeout, connector=connector)

        return self.session

    async def close(self) -> None:
        if self.session:
            await self.session.close()
            self.session = None


class AiohttpClient:
    def __init__(self, session: AiohttpSession):
        self.session = session

    async def make_request(self, method: str, url: str, **kwargs):
        client = await self.session.get()
        async with client.request(method=method, url=url, **kwargs) as response:
            if response.status == 200:
                data = await response.text()
            else:
                data = None
                logger.error(f"Error on {url}")
        return data

    async def get(
        self, url: str, headers: dict | None = None
    ) -> dict | list[dict] | None:
        return await self.make_request(method="GET", url=url, headers=headers)

    async def post(
        self, url: str, json: dict, headers: dict | None = None
    ) -> dict | list[dict] | None:
        return await self.make_request(
            method="POST", url=url, json=json, headers=headers
        )


session = AiohttpSession()
client = AiohttpClient(session=session)
