import abc
import enum
import json
from enum import Enum

from typing import (
    Callable, Any, Final, Type, TYPE_CHECKING, cast
)
from types import TracebackType

from pydantic import ValidationError
from http import HTTPStatus

from .middlewares.manager import RequestMiddlewareManager
from ...methods.base import Response, ClientMethod, BaseType
from ...exceptions import *

import typing


_JsonLoads = Callable[..., Any]
_JsonDumps = Callable[..., str]

DEFAULT_TIMEOUT: Final[float] = 60.0

if TYPE_CHECKING:
    from ..client import Client


class BaseSession(abc.ABC):

    def __init__(
            self,
            json_loads: _JsonLoads = json.loads,
            json_dumps: _JsonDumps = json.dumps,
            timeout: float = DEFAULT_TIMEOUT
    ):
        self.json_loads: _JsonLoads = json_loads
        self.json_dumps: _JsonDumps = json_dumps
        self.timeout = timeout

        self.middleware = RequestMiddlewareManager()

    def check_response(self, method, status_code: int, content: str):
        """
        Check response
        """

        try:
            json_data = self.json_loads(content)
        except Exception as ex:

            raise ClientDecodeError("Failed to decode object", ex, content)

        try:
            response_type = Response[method.__returning__]

            if isinstance(json_data, list):
                response = [
                    typing.get_args(response_type)[0].model_validate(obj, from_attributes=True)
                    for obj in json_data
                ]
            else:
                response = response_type.model_validate(json_data, from_attributes=True)
        except ValidationError as e:
            raise e

        if status_code == HTTPStatus.BAD_REQUEST:
            raise ClientBadRequestError(
                err_code=response.err_code,
                err_text=response.err_text
            )
        if status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
            raise ClientBadRequestError(
                err_code=response.err_code,
                err_text=response.err_text
            )
        if status_code == HTTPStatus.NOT_FOUND:
            raise ClientNotFoundError(
                err_code=response.err_code,
                err_text=response.err_text
            )
        if status_code == HTTPStatus.UNAUTHORIZED:
            raise ClientUnauthorizedError(
                err_code=response.err_code,
                err_text=response.err_text
            )
        if status_code == HTTPStatus.FORBIDDEN:
            raise ClientForbiddenError(
                err_code=response.err_code,
                err_text=response.err_text
            )

        if status_code == HTTPStatus.OK:
            return response.result

    @abc.abstractmethod
    async def close(self) -> None:
        """
        Close client session
        """
        pass

    @abc.abstractmethod
    async def make_request(
            self,
            client: 'Client',
            method: ClientMethod,
            timeout: int | None = None) -> BaseType:
        """
        Make request to API

        :return:
        """
        pass

    def prepare_value(self, value: Any):
        """
        Prepare value before build
        """

        if value is None:
            return None
        if isinstance(value, str):
            return value

        if isinstance(value, dict):
            print(value)
            new = {}
            for k, v in value.items():
                v = self.prepare_value(v)
                if v is None:
                    continue

                new[k] = v
            value = new

        return value

    async def __call__(
            self,
            client: 'Client',
            method: ClientMethod,
            timeout: int | None = None,
    ):
        middleware = self.middleware.wrap_middlewares(self.make_request, timeout=timeout)
        return cast(BaseType, await middleware(client, method))

    async def __aenter__(self) -> 'BaseSession':
        return self

    async def __aexit__(
            self,
            exc_type: Type[BaseException] | None,
            exc_value: BaseException | None = None,
            traceback: TracebackType | None = None,
    ) -> None:
        await self.close()
