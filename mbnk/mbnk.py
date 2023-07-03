__all__ = [
    'MonoPay',
    'MonobankOpenAPI'
]

from mbnk.api import MonoPayAPI, MonobankOpenAPI as MonobankAPI


class MonoPay(MonoPayAPI):

    def __init__(self, api_token: str):
        super().__init__(api_token=api_token, _async=False)


class MonobankOpenAPI(MonobankAPI):

    def __init__(self, api_token: str):
        super().__init__(api_token=api_token, _async=False)
