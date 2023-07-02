from typing import Union

from requests import Response
from aiohttp import ClientResponse


def is_exception(response: Union[Response, ClientResponse]) -> bool:

    if isinstance(response, Response):
        if response.status_code != 200:
            return True

    if isinstance(response, ClientResponse):
        if response.status != 200:
            return True

    return False
