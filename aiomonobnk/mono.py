from .client.client import Client

from .methods import (
    CreateInvoiceMethod,
    InvoiceStatusMethod,
    CancelInvoiceMethod,
    RemoveInvoiceMethod
)
from .enums import (
    CurrencyCode,
    PaymentType
)
from .types import (
    SaveCardData,
    Product
)


class MonoPay(Client):

    def __init__(self, token: str, **kwargs):
        super().__init__(token=token, **kwargs)

    # Invoice Methods
    async def create_invoice(
            self,
            amount: int,
            ccy: CurrencyCode | None = None,
            merchant_paym_info: dict | None = None,
            redirect_url: str | None = None,
            web_hook_url: str | None = None,
            validity: int | None = None,
            payment_type: PaymentType | None = None,
            qr_id: str | None = None,
            code: str | None = None,
            save_card_data: SaveCardData | None = None,
            request_timeout: int | None = None
    ):
        call = CreateInvoiceMethod(
            amount=amount,
            ccy=ccy,
            merchant_paym_info=merchant_paym_info,
            redirect_url=redirect_url,
            web_hook_url=web_hook_url,
            validity=validity,
            payment_type=payment_type,
            qr_id=qr_id,
            code=code,
            save_card_data=save_card_data
        )

        return await self(call, request_timeout=request_timeout)

    async def invoice_status(
            self,
            invoice_id: str,
            request_timeout: int | None = None
    ):
        call = InvoiceStatusMethod(
            invoice_id=invoice_id
        )

        return await self(call, request_timeout=request_timeout)

    async def cancel_invoice(
            self,
            invoice_id: str,
            ext_ref: str | None = None,
            amount: int | None = None,
            items: list[Product] | None = None,
            request_timeout: int | None = None
    ):
        call = CancelInvoiceMethod(
            invoice_id=invoice_id,
            ext_ref=ext_ref,
            amount=amount,
            items=items
        )
        return await self(call, request_timeout=request_timeout)

    async def remove_invoice(
            self,
            invoice_id: str,
            request_timeout: int | None = None
    ):
        call = RemoveInvoiceMethod(
            invoice_id=invoice_id
        )

        return await self(call, request_timeout=request_timeout)
