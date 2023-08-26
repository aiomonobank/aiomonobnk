from .base import (
    ClientMethod,
    RequestMethod
)
from ..types.merchant_statement import MerchantStatement


class MerchantStatementMethod(ClientMethod):

    __request_method__ = RequestMethod.GET
    __request_path__ = '/api/merchant/statement'
    __returning__ = MerchantStatement

    from_: int | None
    to: int | None

    def __init__(
            self,
            from_: int | None = None,
            to: int | None = None
    ):
        super().__init__(
            from_=from_,
            to=to
        )
