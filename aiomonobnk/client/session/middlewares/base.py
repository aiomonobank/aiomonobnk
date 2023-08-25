from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Protocol

from ....methods.base import Response, ClientMethod
from ....methods.base import BaseType

if TYPE_CHECKING:
    from ...client import Client


class NextRequestMiddlewareType(Protocol[BaseType]):  # pragma: no cover
    async def __call__(
            self,
            client: 'Client',
            method: ClientMethod[BaseType],
    ) -> Response[BaseType]:
        pass


class RequestMiddlewareType(Protocol):  # pragma: no cover
    async def __call__(
            self,
            make_request: NextRequestMiddlewareType[BaseType],
            client: 'Client',
            method: ClientMethod[BaseType],
    ) -> Response[BaseType]:
        pass


class BaseRequestMiddleware(ABC):
    """
    Generic middleware class
    """

    @abstractmethod
    async def __call__(
            self,
            make_request: NextRequestMiddlewareType[BaseType],
            client: 'Client',
            method: ClientMethod[BaseType],
    ) -> Response[BaseType]:
        """
        Execute middleware

        :param make_request: Wrapped make_request in middlewares chain
        :param method: Request method (Subclass of :class:`aiogram.methods.base.TelegramMethod`)

        :return: :class:`aiogram.methods.Response`
        """
        pass
