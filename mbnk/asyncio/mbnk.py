from mbnk.api import MonoPayAPI, MonobankOpenAPI


class AsyncMonoPay(MonoPayAPI):

    def __init__(self, api_token: str):
        super().__init__(api_token=api_token, _async=True)


class AsyncMonobank(MonobankOpenAPI):

    def __init__(self, api_token: str):
        super().__init__(api_token=api_token, _async=True)
