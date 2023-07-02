import json
import requests

from aiohttp import ClientSession

from mbnk.utils import data_builder, is_exception
from mbnk.utils.format import convert_json, camel_to_underscore
from mbnk.exceptions import MonoPayAPIException, MonobankAPIException


def api_request(
        method: str,
        url: str,
        headers: dict,
        data: str = None,
        params: str = None
):
    request = getattr(requests, method)
    response = request(
        url=url,
        headers=headers,
        data=json.dumps(data) if data is not None else None,
        params=params
    )

    response_data = response.json()
    response_data = convert_json(response_data, camel_to_underscore)

    if is_exception(response):
        return MonoPayAPIException(**response_data)

    return response_data


async def async_api_request(
        method: str,
        url: str,
        headers: dict,
        data: str = None,
        params: str = None
):
    async with ClientSession() as session:
        request = getattr(session, method)
        async with request(
                url=url,
                headers=headers,
                data=json.dumps(data) if data is not None else None,
                params=params
        ) as response:

            response_data = await response.json()
            response_data = convert_json(response_data, camel_to_underscore)

            if is_exception(response):
                return MonoPayAPIException(**response_data)

            return response_data


def api_method(method: str, url: str):
    def outer(func):
        def inner(self, *args, **kwargs):

            func_args = {
                "method": method,
                "url": url.format(
                    base_url=self.__base_url__
                ),
                "headers": self.__headers__,
                ("params" if method == "get" else "data"): data_builder(**kwargs)
            }

            async def async_wrapper():
                response = await async_api_request(**func_args)

                if isinstance(response, MonoPayAPIException) or isinstance(response, MonobankAPIException):
                    return response

                return func(self, *args, **kwargs, response_data=response)

            def sync_wrapper():
                response = api_request(**func_args)

                if isinstance(response, MonoPayAPIException) or isinstance(response, MonobankAPIException):
                    return response

                return func(self, *args, **kwargs, response_data=response)

            if self.__is_async__:
                return async_wrapper()
            else:
                return sync_wrapper()

        return inner

    return outer

