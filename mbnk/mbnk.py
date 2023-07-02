from mbnk.api import MonoPayAPI, MonobankOpenAPI


class MonoPay(MonoPayAPI):

    def __init__(self, api_token: str):
        super().__init__(api_token=api_token, _async=False)


class Monobank(MonobankOpenAPI):

    def __init__(self, api_token: str):
        super().__init__(api_token=api_token, _async=False)
