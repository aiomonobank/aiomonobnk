__all__ = [
    'AsyncMonoAcquiringAPI',
    'AsyncMonobankOpenAPI',
    'AsyncMonobankCorporateOpenAPI'
]

from typing import Optional

from mbnk.api import (
    MonoAcquiringAPIModel,
    MonobankOpenAPIModel,
    MonobankCorporateOpenAPIModel
)


class AsyncMonoAcquiringAPI(MonoAcquiringAPIModel):
    """
    Asynchronous version MonoAcquiringAPI
    Source: https://api.monobank.ua/docs/acquiring.html
    """

    def __init__(self, api_token: str):
        super().__init__(api_token=api_token, _async=True)


class AsyncMonobankOpenAPI(MonobankOpenAPIModel):
    """
    Asynchronous version MonobankOpenAPI
    Source: https://api.monobank.ua/docs/
    """

    def __init__(self, api_token: Optional[str] = None):
        super().__init__(api_token=api_token, _async=True)


class AsyncMonobankCorporateOpenAPI(MonobankCorporateOpenAPIModel):
    """
    Asynchronous version MonobankCorporateOpenAPI
    Source: https://api.monobank.ua/docs/corporate.html
    """

    def __init__(self):
        super().__init__(_async=True)
