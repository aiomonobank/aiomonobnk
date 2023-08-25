from contextlib import asynccontextmanager
from typing import AsyncIterator

from .session.base import BaseSession
from .session.session import Session

from ..methods.base import ClientMethod


class Client:
    def __init__(
            self,
            token: str,
            session: BaseSession | None = None
    ):
        if session is None:
            session = Session(token=token)

        self.session = session
        self.__token = token

    @property
    def token(self) -> str:
        return self.__token

    @asynccontextmanager
    async def context(self, auto_close: bool = True) -> AsyncIterator['Client']:
        """
        Generate client context

        :param auto_close: close session on exit
        :return:
        """
        try:
            yield self
        finally:
            if auto_close:
                await self.session.close()

    async def __call__(
            self, method: ClientMethod, request_timeout: int | None = None
    ):
        """
        Call API method
        """
        return await self.session(self, method, timeout=request_timeout)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        return await self.session.close()
