import asyncio

from aiohttp import ClientSession, FormData

from typing import Any, TYPE_CHECKING

from .base import BaseSession
from ...methods.base import ClientMethod, BaseType, RequestMethod

if TYPE_CHECKING:
    from ..client import Client


class Session(BaseSession):
    __token: str

    def __init__(self, token: str, **kwargs: Any) -> None:
        super().__init__(**kwargs)

        self.__token = token

        self._session: ClientSession | None = None
        self._should_reset_connector = True  # flag determines connector state

    async def create_session(self) -> ClientSession:
        if self._should_reset_connector:
            await self.close()

        if self._session is None or self._session.closed:
            self._session = ClientSession(
                headers={
                    'X-Token': self.__token
                }
            )
            self._should_reset_connector = False

        return self._session

    async def close(self) -> None:
        if self._session is not None and not self._session.closed:
            await self._session.close()

    def build_query(self, method: ClientMethod) -> dict[str, Any]:
        query = {}
        for key, value in method.model_dump(warnings=False, by_alias=True).items():
            value = self.prepare_value(value)

            if not value:
                continue

            if key[-1] == '_':
                key = key[:-1]

            query[key] = value

        return query

    @staticmethod
    def build_request_url(method: ClientMethod) -> str:
        url = f'{method.base_url}{method.__request_path__}'

        for key, value in method.model_dump(warnings=False).items():
            if not value:
                continue

            if key[len(key) - 2:] == '__':
                key = key[len(key) - 2:]
                url = url.replace('{' + key + '}', str(value))

        return url

    async def make_request(
            self,
            client: 'Client',
            method: ClientMethod,
            timeout: int | None = None
    ) -> BaseType:
        session = await self.create_session()

        url = self.build_request_url(method)
        request_method = method.__request_method__

        if (
            request_method == RequestMethod.POST or
            request_method == RequestMethod.PUT or
            request_method == RequestMethod.PATCH
        ):
            data = self.build_query(method)
        else:
            data = None

        print(data)

        if (
            request_method == RequestMethod.GET or
            request_method == RequestMethod.DELETE
        ):
            query = self.build_query(method)
        else:
            query = None

        print(url)

        try:
            async with session.request(
                request_method,
                url,
                json=data,
                params=query,
                timeout=self.timeout if timeout is None else timeout
            ) as resp:
                raw_result = await resp.text()
        except asyncio.TimeoutError:
            raise TimeoutError

        response = self.check_response(
            method=method,
            status_code=resp.status,
            content=raw_result
        )

        setattr(response, '_client', client)

        return response

    async def __aenter__(self):
        await self.create_session()
        return self
