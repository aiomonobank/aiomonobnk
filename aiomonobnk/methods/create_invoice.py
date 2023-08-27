from .base import (
    ClientMethod,
    RequestMethod
)
from ..enums import (
    CurrencyCode,
    PaymentType
)
from ..types import (
    InvoiceCreated,
    SaveCardData,
    MerchantPaymInfo
)
from pydantic import Field


class CreateInvoiceMethod(ClientMethod):

    __request_method__ = RequestMethod.POST
    __request_path__ = '/api/merchant/invoice/create'
    __returning__ = InvoiceCreated

    amount: int
    ccy: CurrencyCode | None = None
    merchant_paym_info: MerchantPaymInfo | None = Field(alias='merchantPaymInfo', default=None)
    redirect_url: str | None = Field(alias='redirectUrl', default=None)
    web_hook_url: str | None = Field(alias='webHookUrl', default=None)
    validity: int | None = None
    """in seconds"""
    payment_type: PaymentType | None = Field(alias='paymentType', default=None)
    qr_id: str | None = Field(alias='qrId', default=None)
    code: str | None = None
    save_card_data: SaveCardData | None = Field(alias='saveCardData', default=None)

    def __init__(
            self,
            amount: int,
            ccy: CurrencyCode | None = None,
            merchant_paym_info: MerchantPaymInfo | None = None,
            redirect_url: str | None = None,
            web_hook_url: str | None = None,
            validity: int | None = None,
            payment_type: PaymentType | None = None,
            qr_id: str | None = None,
            code: str | None = None,
            save_card_data: SaveCardData | None = None
    ):
        super().__init__(
            amount=amount,
            ccy=ccy,
            merchantPaymInfo=merchant_paym_info,
            redirectUrl=redirect_url,
            webHookUrl=web_hook_url,
            validity=validity,
            paymentType=payment_type,
            qrId=qr_id,
            code=code,
            saveCardData=save_card_data
        )
