from abc import ABC, abstractmethod, ABCMeta
from pydantic import BaseModel, ConfigDict, Field

from enum import StrEnum

from typing import (
    TypeVar,
    Any,
    Generic,
    ClassVar
)

from ..client.context import ClientContextController


BaseType = TypeVar("BaseType", bound=Any)


class RequestMethod(StrEnum):
    GET: str = "get"
    POST: str = "post"
    PUT: str = "put"
    PATCH: str = "patch"
    DELETE: str = "delete"


class Request(BaseModel, Generic[BaseType]):
    method: RequestMethod


class Response(BaseModel, Generic[BaseType]):
    result: BaseType | None = None
    err_code: str | None = Field(alias='errCode', default=None)
    err_text: str | None = Field(alias='errText', default=None)

    def __init__(
            self,
            **kwargs
    ):
        if 'errCode' in kwargs:
            super().__init__(**kwargs)
        else:
            super().__init__(
                result={**kwargs}
            )


class ClientMethod(ClientContextController, BaseModel, Generic[BaseType], ABC):

    __request_method__ = ClassVar[RequestMethod]
    __request_path__ = ClassVar[str]
    __returning__ = ABCMeta

    @property
    @abstractmethod
    def __request_method__(self):
        pass

    @property
    @abstractmethod
    def __request_path__(self):
        pass

    @property
    @abstractmethod
    def __returning__(self):
        pass

    @property
    def base_url(self, mode: str = 'production') -> str:
        return "https://api.monobank.ua"

    @property
    def request_url(self):
        return f'{self.base_url}{self.build_path()}'
