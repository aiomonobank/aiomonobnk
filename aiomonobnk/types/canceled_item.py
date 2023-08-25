from .base import ClientObject
from pydantic import Field

from ..enums import (
    CancellationStatus,
    CurrencyCode
)


class CanceledItem(ClientObject):
    status: CancellationStatus
    created_date: str = Field(alias="createdDate")
    modified_date: str = Field(alias="modifiedDate")
    amount: int | None = None
    ccy: CurrencyCode | None = None
    approval_code: str | None = Field(alias="approvalCode", default=None)
    rrn: str | None = None
    ext_ref: str | None = Field(alias="extRef", default=None)

    def __init__(
            self,
            status: CancellationStatus,
            created_date: str,
            modified_date: str,
            amount: int | None = None,
            ccy: CurrencyCode | None = None,
            approval_code: str | None = None,
            rrn: str | None = None,
            ext_ref: str | None = None
    ):
        super().__init__(
            status=status,
            createdDate=created_date,
            modifiedDate=modified_date,
            amount=amount,
            ccy=ccy,
            approvalCode=approval_code,
            rrn=rrn,
            extRef=ext_ref
        )
