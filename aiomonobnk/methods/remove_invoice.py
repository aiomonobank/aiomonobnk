from .base import (
    ClientMethod,
    RequestMethod
)
from pydantic import Field
from ..types.empty_response import EmptyResponse


class RemoveInvoiceMethod(ClientMethod):

    __request_method__ = RequestMethod.POST
    __request_path__ = '/api/merchant/invoice/remove'
    __returning__ = EmptyResponse

    invoice_id: str = Field(alias='invoiceId')

    def __init__(
            self,
            invoice_id: str
    ):
        super().__init__(
            invoiceId=invoice_id
        )
