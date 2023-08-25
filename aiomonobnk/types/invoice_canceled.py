from .base import ClientObject
from pydantic import Field

from ..enums.transaction_status import TransactionStatus
from datetime import datetime


class InvoiceCanceled(ClientObject):

    status: TransactionStatus

    created_date: datetime = Field(alias='createdDate')
    modified_date: datetime = Field(alias='modifiedDate')
