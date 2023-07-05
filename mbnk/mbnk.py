__all__ = [
    'MonoAcquiringAPI',
    'MonobankOpenAPI',
    'MonobankCorporateOpenAPI'
]

from typing import Optional

from mbnk.api import (
    MonoAcquiringAPIModel,
    MonobankOpenAPIModel,
    MonobankCorporateOpenAPIModel
)


class MonoAcquiringAPI(MonoAcquiringAPIModel):
    """
    Synchronous version MonoAcquiringAPI
    Source: https://api.monobank.ua/docs/acquiring.html
    """

    def __init__(self, api_token: str):
        super().__init__(api_token=api_token, _async=False)


class MonobankOpenAPI(MonobankOpenAPIModel):
    """
    Synchronous version MonobankOpenAPI
    Source: https://api.monobank.ua/docs/
    """

    def __init__(self, api_token: Optional[str] = None):
        super().__init__(api_token=api_token, _async=False)


class MonobankCorporateOpenAPI(MonobankCorporateOpenAPIModel):
    """
    Synchronous version MonobankCorporateOpenAPI
    Source: https://api.monobank.ua/docs/corporate.html
    """

    def __init__(self):
        super().__init__(_async=False)
