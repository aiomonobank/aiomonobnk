import requests
import aiohttp
import json
from mbnk.utils import data_builder, is_exception
from mbnk.utils.format import convert_json, camel_to_underscore
from mbnk.exceptions import MonoPayAPIException


def request(url):
    def outer(func):
        def inner(self, *args, **kwargs):
            params = data_builder(**kwargs)

            response = requests.get(
                url=self.__base_url__,
                headers=self.__headers__,
                params=params
            )

            response_data = response.json()
            response_data = convert_json(response_data, camel_to_underscore)

            if is_exception(response):
                return MonoPayAPIException(**response_data)

            return func(self, *args, **kwargs, response_data=response_data)

        return inner

    return outer


def async_request(url, method):
    def outer(func):
        async def inner(self, *args, **kwargs):
            params = data_builder(**kwargs)

            async with aiohttp.ClientSession() as session:
                api_request = getattr(session, method)
                async with api_request(
                    url=url.format(
                        base_url=self.__base_url__
                    ),
                    headers=self.__headers__,
                    params=params if method == "get" else None,
                    data=json.dumps(params) if method != "get" else None
                ) as response:

                    response_data = await response.json()
                    response_data = convert_json(response_data, camel_to_underscore)

                    if is_exception(response):
                        return MonoPayAPIException(**response_data)

                    return func(self, *args, **kwargs, response_data=response_data)

        return inner

    return outer


def async_post_request(url):
    def outer(func):
        async def inner(self, *args, **kwargs):
            data = data_builder(**kwargs)

            async with aiohttp.ClientSession() as session:
                async with session.post(
                    url=url.format(
                        base_url=self.__base_url__
                    ),
                    headers=self.__headers__,
                    data=json.dumps(data)
                ) as response:
                    response_data = await response.json()

                    return func(self, *args, **kwargs, response_data=response_data)

        return inner

    return outer


def async_delete_request(url):
    def outer(func):
        async def inner(self, *args, **kwargs):
            data = data_builder(**kwargs)

            async with aiohttp.ClientSession() as session:
                async with session.delete(
                    url=url.format(
                        base_url=self.__base_url__
                    ),
                    headers=self.__headers__,
                    params=data
                ) as response:
                    response_data = await response.json()

                    return func(self, *args, **kwargs, response_data=response_data)

        return inner

    return outer

