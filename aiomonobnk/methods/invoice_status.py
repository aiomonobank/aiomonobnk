from .base import (
    ClientMethod,
    RequestMethod
)
from pydantic import Field
from ..types import InvoiceStatus


class InvoiceStatusMethod(ClientMethod):

    __request_method__ = RequestMethod.GET
    __request_path__ = '/api/merchant/invoice/status'
    __returning__ = InvoiceStatus

    invoice_id: str = Field(alias='invoiceId')

    def __init__(
            self,
            invoice_id: str
    ):
        super().__init__(
            invoiceId=invoice_id
        )
