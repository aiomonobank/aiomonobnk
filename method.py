import re
import json

from typing import Optional, Union

import requests

from requests import Response
from aiohttp import (
    ClientSession,
    ClientResponse
)

from mbnk.exceptions import (
    MonoPayAPIException,
    MonobankAPIException
)

import asyncio


class APIMethod:

    __api_token = None
    __headers = {}

    def __init__(
            self,
            base_url: str,
            _async: bool,
            api_token: str
    ):
        self.__is_async: bool = _async
        self.__api_token: str = api_token
        self.__base_url: str = base_url
        self.__headers["X-Token"] = self.__api_token

    @staticmethod
    def camel_to_underscore(text: str):
        camel_pat = re.compile(r'([A-Z])')
        return camel_pat.sub(lambda x: '_' + x.group(1).lower(), text)

    @staticmethod
    def underscore_to_camel(text: str):
        under_pat = re.compile(r'_([a-z])')
        return under_pat.sub(lambda x: x.group(1).upper(), text)

    def json_convert(self, data, convert):
        if isinstance(data, dict):
            new_data = {}
            for k, value in data.items():
                new_data[convert(k)] = self.json_convert(value, convert) if (
                    isinstance(value, dict)
                ) else self.json_convert(value, convert) if isinstance(value, list) else value
            return new_data
        elif isinstance(data, list):
            new_list = []
            for item in data:
                new_list.append(self.json_convert(item, convert))
            return new_list

    def load_response(self, response_data: Union[dict, list]):

        return self.json_convert(response_data, self.camel_to_underscore)

    def build_data(self, **kwargs):
        data = {}

        for kwarg in kwargs:
            key = kwarg.replace("timestamp", "")
            key = self.underscore_to_camel(key)
            value = kwargs.get(kwarg)
            data[key] = value

        return data

    @staticmethod
    def is_exception(response: Union[Response, ClientResponse]) -> bool:
        if isinstance(response, Response):
            if response.status_code != 200:
                return True

        if isinstance(response, ClientResponse):
            if response.status != 200:
                return True

        return False

    def sync_request(
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
        response_data = self.load_response(response_data)

        if self.is_exception(response):
            return MonoPayAPIException(**response_data)

        return response_data

    async def async_request(
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
                response_data = self.load_response(response_data)

                if self.is_exception(response):
                    return MonoPayAPIException(**response_data)

                return response_data

    @staticmethod
    def request(
            request_method: str,
            path: str
    ):
        def outer(func):
            def inner(*args, **kwargs):
                self = args[0]
                args = args[1:]
                func_args = {
                    "method": request_method,
                    "path": path,
                    ("params" if request_method == "get" else "data"): self.build_data(**kwargs)
                }

                async def async_wrapper():
                    response = await self.async_request(**func_args)

                    if isinstance(response, MonoPayAPIException) or isinstance(response, MonobankAPIException):
                        return response

                    return func(self, *args, **kwargs, response_data=response)

                def sync_wrapper():
                    response = self.sync_request(**func_args)

                    if isinstance(response, MonoPayAPIException) or isinstance(response, MonobankAPIException):
                        return response

                    return func(self, *args, **kwargs, response_data=response)

                if self.__is_async:
                    return async_wrapper()
                else:
                    return sync_wrapper()

            return inner

        return outer


class BaseMethod(APIMethod):

    @APIMethod.request("get", path="bank/currency")
    def get_data(self, **kwargs):
        return kwargs['response_data']


async def main():
    api_token = ""
    mthd = BaseMethod(
        api_token=api_token,
        base_url="https://api.monobank.ua",
        _async=True
    )

    result = await mthd.get_data()
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
