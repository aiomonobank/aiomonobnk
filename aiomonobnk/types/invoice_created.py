from .base import ClientObject
from pydantic import Field


class InvoiceCreated(ClientObject):

    invoice_id: str = Field(alias='invoiceId')
    page_url: str = Field(alias='pageUrl')
