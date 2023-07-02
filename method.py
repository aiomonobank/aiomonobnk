import json
from typing import Optional, Union

import requests
from aiohttp import ClientSession

from mbnk import MonoPayAPIException, MonobankAPIException


class APIRequest:

    __api_token = None
    __headers = {}

    def __init__(
            self,
            base_url: str,
            _async: bool,
            api_token: Union[Optional[str], None] = None
    ):
        self.__is_async: bool = _async
        self.__api_token: str = api_token
        self.__base_url: str = base_url
        self.__headers["X-Token"] = self.__api_token

    def sync_request(self):
        pass

    async def async_request(self):
        pass


class APIMethod:

    __api_token = None
    __headers = {}

    def __init__(
            self,
            base_url: str,
            _async: bool,
            api_token: Union[Optional[str], None] = None
    ):
        self.__is_async: bool = _async
        self.__api_token: str = api_token
        self.__base_url: str = base_url
        self.__headers["X-Token"] = self.__api_token

    def load_response(self, response_data: dict):
        return response_data

    def build_data(self, **kwargs):
        return kwargs

    def api_request(
            self,
            method: str,
            path: str,
            data: str = None,
            params: str = None
    ):
        request = getattr(requests, method)
        response = request(
            url=f"{self.__base_url}/{path}",
            headers=self.__headers,
            params=params,
            data=json.dumps(data) if data is not None else None
        )
        response_data = response.json()
        return self.load_response(response_data)

    async def async_api_request(
            self,
            method: str,
            path: str,
            data: str = None,
            params: str = None
    ):
        async with ClientSession() as session:
            request = getattr(session, method)
            async with request(
                    url=f"{self.__base_url}/{path}",
                    headers=self.__headers,
                    data=json.dumps(data) if data is not None else None,
                    params=params
            ) as response:
                response_data = await response.json()
                return self.load_response(response_data)

    def request(
            request_method: str,
            path: str
    ):
        def outer(func):
            def inner(self, *args, **kwargs):
                func_args = {
                    "method": request_method,
                    "path": path,
                    ("params" if request_method == "get" else "data"): self.build_data(**kwargs)
                }

                async def async_wrapper():
                    response = await self.async_api_request(**func_args)

                    if isinstance(response, MonoPayAPIException) or isinstance(response, MonobankAPIException):
                        return response

                    return func(self, *args, **kwargs, response_data=response)

                def sync_wrapper():
                    response = self.api_request(**func_args)

                    if isinstance(response, MonoPayAPIException) or isinstance(response, MonobankAPIException):
                        return response

                    return func(self, *args, **kwargs, response_data=response)

                if self.__is_async:
                    return async_wrapper()
                else:
                    return sync_wrapper()

            return inner

        return outer

    request = staticmethod(request)


class BaseMethod(APIMethod):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @APIMethod.request("get", path="bank/currency")
    def get_data(self, **kwargs):
        return kwargs['response_data']


method = BaseMethod(
    base_url="https://api.monobank.ua",
    _async=False
)

result = method.get_data()

print(result)
