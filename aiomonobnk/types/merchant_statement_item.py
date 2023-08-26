from .base import ClientObject
from pydantic import Field

from ..enums import (
    PaymentScheme,
    CurrencyCode
)


class MerchantStatementItem(ClientObject):

    invoice_id: str = Field(alias="invoiceId")
    status: str
    masked_pan: str = Field(alias="maskedPan")
    date: str
    payment_scheme: PaymentScheme = Field(alias="paymentScheme")
    amount: int
    ccy: CurrencyCode
    profit: int | None = None
    approval_code: str | None = Field(alias="approvalCode", default=None)
    reference: str | None = None
    cancel_list: list[dict] | None = Field(alias="cancelList", default=None)
    rrn: str | None = Field(default=None)
    short_qr_id: str | None = Field(alias="shortQrId", default=None)
