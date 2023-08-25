from .base import (
    ClientMethod,
    RequestMethod
)
from pydantic import Field

from ..types.product import Product


class CancelInvoiceMethod(ClientMethod):

    __request_method__ = RequestMethod.POST
    __request_path__ = '/api/merchant/invoice/cancel'
    __returning__ = bool

    invoice_id: str = Field(alias='invoiceId')

    ext_ref: str | None = Field(alias='extRef', default=None)

    amount: int | None = None

    items: list[Product] | None = None

    def __init__(
            self,
            invoice_id: str,
            ext_ref: str | None = None,
            amount: int | None = None,
            items: list[Product] | None = None
    ):
        super().__init__(
            invoiceId=invoice_id,
            extRef=ext_ref,
            amount=amount,
            items=items
        )
