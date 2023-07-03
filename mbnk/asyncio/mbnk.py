__all__ = [
    'AsyncMonoPay',
    'AsyncMonobankOpenAPI'
]

from mbnk.api import MonoPayAPI, MonobankOpenAPI as MonobankAPI


class AsyncMonoPay(MonoPayAPI):
    """ Asynchronous version MonoPayAPI """

    def __init__(self, api_token: str):
        super().__init__(api_token=api_token, _async=True)


class AsyncMonobankOpenAPI(MonobankAPI):
    """ Asynchronous version MonobankOpenAPI """

    def __init__(self, api_token: str):
        super().__init__(api_token=api_token, _async=True)
