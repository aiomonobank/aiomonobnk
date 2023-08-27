from .client.client import Client

from .methods import (
    CreateInvoiceMethod,
    InvoiceStatusMethod,
    CancelInvoiceMethod,
    RemoveInvoiceMethod,
    MerchantPubKeyMethod,
    MerchantDetailsMethod,
    MerchantStatementMethod,
    SubmerchantListMethod,
    FiscalChecksMethod
)
from .enums import (
    CurrencyCode,
    PaymentType
)
from .types import (
    SaveCardData,
    Product,
    MerchantPaymInfo
)


class MonoPay(Client):

    def __init__(self, token: str, **kwargs):
        super().__init__(token=token, **kwargs)

    # Invoice Methods
    async def create_invoice(
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

    async def merchant_pubkey(
            self,
            request_timeout: int | None = None
    ):
        call = MerchantPubKeyMethod()

        return await self(call, request_timeout=request_timeout)

    async def merchant_details(
            self,
            request_timeout: int | None = None
    ):
        call = MerchantDetailsMethod()

        return await self(call, request_timeout=request_timeout)

    async def merchant_statement(
            self,
            from_: int | None = None,
            # unix utc timestamp
            to: int | None = None,
            # unix utc timestamp
            request_timeout: int | None = None
    ):
        call = MerchantStatementMethod(
            from_=from_,
            to=to
        )

        return await self(call, request_timeout=request_timeout)

    async def submerchants_list(
            self,
            request_timeout: int | None = None
    ):
        call = SubmerchantListMethod()

        return await self(call, request_timeout=request_timeout)

    async def fiscal_checks(
            self,
            invoice_id: str,
            request_timeout: int | None = None
    ):
        call = FiscalChecksMethod(
            invoice_id=invoice_id
        )

        return await self(call, request_timeout=request_timeout)
