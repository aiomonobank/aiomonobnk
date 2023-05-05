import json

from mbnk.exceptions import MonobankBaseException
from mbnk.utils import data_builder, is_exception
import requests


def request(url):
    def outer(func):
        def inner(self, *args, **kwargs):
            params = data_builder(**kwargs)

            response = requests.get(
                url=self.__dict__.get(url),
                headers=self.headers,
                params=params
            )

            response_data = response.json()

            if is_exception(response):
                return MonobankBaseException(
                    err_description=response_data['errorDescription']
                )

            return func(self, *args, **kwargs, response_data=response_data)

        return inner

    return outer


def post_request(url):
    def outer(func):
        def inner(self, *args, **kwargs):
            data = data_builder(**kwargs)

            print(data)

            response = requests.post(
                url=self.__dict__.get(url),
                headers=self.headers,
                data=json.dumps(data)
            )

            response_data = response.json()

            # if is_exception(response):
            #     return MonobankBaseException(
            #         err_code=response_data['errCode'],
            #         err_text=response_data['errText']
            #     )

            return func(self, *args, **kwargs, response_data=response_data)

        return inner

    return outer
