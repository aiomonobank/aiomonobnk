from .base import ClientObject
from pydantic import Field

from ..enums import (
    TransactionStatus,
    CurrencyCode
)

from ..types.wallet_data import WalletData
from ..types.canceled_item import CanceledItem

from datetime import datetime


class InvoiceStatus(ClientObject):

    invoice_id: str = Field(alias='invoiceId')
    status: TransactionStatus
    amount: int
    ccy: CurrencyCode
    failure_reason: str | None = Field(alias='failureReason', default=None)
    final_amount: int | None = Field(alias='finalAmount', default=None)
    created_date: datetime | None = Field(alias='createdDate', default=None)
    modified_date: datetime | None = Field(alias='modifiedDate', default=None)
    reference: str | None = None
    cancel_list: CanceledItem = Field(alias='cancelList', default=None)
    wallet_data: WalletData = Field(alias='walletData', default=None)
