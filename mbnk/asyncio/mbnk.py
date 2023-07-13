__all__ = [
    'AsyncMonoAcquiringAPI',
    'AsyncMonobankOpenAPI',
    'AsyncMonobankCorporateOpenAPI'
]

from typing import Optional, Union

from mbnk.exceptions import MonobankAPIException
from mbnk.types import *
from mbnk.api import (
    APIMethod,
    APIPaths
)


class Merchant(APIMethod):

    @APIMethod._request("get", path="/details")
    def details(self, **kwargs) -> Union[MerchantDetails, MonobankAPIException]:
        """
        Mono Acquiring API: https://api.monobank.ua/docs/acquiring.html#/paths/~1api~1merchant~1details/get

        :return: MerchantDetailsResponse
        """

        return MerchantDetails(**kwargs["response_data"])

    @APIMethod._request("get", path="/statement")
    def statement(
            self,
            from_timestamp: int,
            to_timestamp: Optional[int] = None,
            **kwargs
    ) -> Union[MerchantStatement, MonobankAPIException]:
        """
        Mono Acquiring API: https://api.monobank.ua/docs/acquiring.html#/paths/~1api~1merchant~1statement/get

        :param from_timestamp:
        :param to_timestamp:
        :param kwargs:
        :return:
        """

        return MerchantStatement(
            list=[
                MerchantStatementItem(
                    **statement_item,
                    cancel_list=[
                        CancelListItem(
                            **cancel_item
                        ) for cancel_item in statement_item['cancel_list']
                    ] if "cancel_list" in statement_item else None
                ) for statement_item in kwargs['response_data']['list']
            ]
        )

    @APIMethod._request("get", path="/pubkey")
    def pubkey(self, **kwargs) -> Union[MerchantPubKey, MonobankAPIException]:
        """
        Mono Acquiring API Docs: https://api.monobank.ua/docs/acquiring.html#/paths/~1api~1merchant~1pubkey/get

        :return: MerchantPubKeyResponse
        """

        return MerchantPubKey(**kwargs["response_data"])


class Invoice(APIMethod):

    @APIMethod._request("post", path="/create")
    async def create(
            self,
            amount: int,
            ccy: Optional[int] = None,
            merchant_paym_info: Optional[MerchantPaymInfo] = None,
            redirect_url: Optional[str] = None,
            web_hook_url: Optional[str] = None,
            validity: Optional[int] = None,
            payment_type: Optional[str] = None,
            qr_id: Optional = None,
            save_card_data: Optional[SaveCardData] = None,
            **kwargs
    ) -> Union[InvoiceCreated, MonobankAPIException]:
        """
        Mono Acquiring API: https://api.monobank.ua/docs/acquiring.html#/paths/~1api~1merchant~1invoice~1create/post

        :param amount:
        :param ccy:
        :param merchant_paym_info:
        :param redirect_url:
        :param web_hook_url:
        :param validity:
        :param payment_type:
        :param qr_id:
        :param save_card_data:
        :return:
        """

        return InvoiceCreated(**kwargs['response_data'])

    @APIMethod._request("post", path="/cancel")
    async def cancel(
            self,
            invoice_id: str,
            ext_ref: str = None,
            amount: int = None,
            items=None,
            **kwargs
    ) -> Union[InvoiceCanceled, MonobankAPIException]:
        """
        Mono Acquiring API: https://api.monobank.ua/docs/acquiring.html#/paths/~1api~1merchant~1invoice~1cancel/post

        :param invoice_id:
        :param ext_ref:
        :param amount:
        :param items:
        :param kwargs:
        :return:
        """
        return InvoiceCanceled(**kwargs['response_data'])

    @APIMethod._request("get", path="/status")
    async def status(
            self,
            invoice_id: str,
            **kwargs
    ) -> Union[InvoiceStatus, MonobankAPIException]:
        """
        Mono Acquiring API: https://api.monobank.ua/docs/acquiring.html#/paths/~1api~1merchant~1invoice~1status?invoiceId=%7BinvoiceId%7D/get

        :param invoice_id:
        :param kwargs:
        :return:
        """

        return kwargs["response_data"]

    @APIMethod._request("post", path="/remove")
    async def invalidation(
            self,
            invoice_id: str,
            **kwargs
    ) -> Union[EmptyResponse, MonobankAPIException]:
        """
        Source: https://api.monobank.ua/docs/acquiring.html#/paths/~1api~1merchant~1invoice~1remove/post

        :param invoice_id:
        :param kwargs:
        :return:
        """

        return EmptyResponse()

    @APIMethod._request("get", path="/info")
    async def info(
            self,
            invoice_id: str,
            **kwargs
    ) -> Union[InvoiceInfo, MonobankAPIException]:
        """
        Source: https://api.monobank.ua/docs/acquiring.html#/paths/~1api~1merchant~1invoice~1payment-info?invoiceId=%7BinvoiceId%7D/get

        :param invoice_id:
        :param kwargs:
        :return:
        """

        return kwargs['response_data']

    @APIMethod._async_request("get", path="/finalize")
    async def finalize(
            self,
            invoice_id: str,
            amount: int,
            **kwargs
    ) -> Union[FinalizeInvoice, MonobankAPIException]:
        """
        Source: https://api.monobank.ua/docs/acquiring.html#/paths/~1api~1merchant~1invoice~1finalize/post

        :param invoice_id:
        :param amount:
        :param kwargs:
        :return:
        """

        return FinalizeInvoice(
            **kwargs['response_data']
        )


class Qr(APIMethod):

    @APIMethod._request("get", path="/list")
    async def list(self, **kwargs) -> Union[QrList, MonobankAPIException]:
        return QrList(
            list=[
                QrListItem(
                    **qr
                ) for qr in kwargs['response']['list']
            ]
        )

    @APIMethod._request("get", path="/details")
    async def details(
            self,
            qr_id: str,
            **kwargs
    ) -> Union[QrDetails, MonobankAPIException]:
        """
        :param qr_id:
        :return:
        """
        return QrDetails(**kwargs['response_data'])

    @APIMethod._request("post", path="/reset-amount")
    async def reset_amount(
            self,
            qr_id: str,
            **kwargs
    ) -> Union[EmptyResponse, MonobankAPIException]:
        """
        :param qr_id:
        :return:
        """
        return EmptyResponse()


class Wallet(APIMethod):

    @APIMethod._request("get", path="")
    async def cards(
            self,
            wallet_id: str,
            **kwargs
    ):
        """
        Source: https://api.monobank.ua/docs/acquiring.html#/paths/~1api~1merchant~1wallet/get

        :param wallet_id:
        :param kwargs:
        :return:
        """

        return kwargs["response_data"]

    @APIMethod._request("post", path="/payment")
    async def payment(self):
        """
        Source: https://api.monobank.ua/docs/acquiring.html#/paths/~1api~1merchant~1wallet~1payment/post
        :return:
        """

        pass

    @APIMethod._request("delete", path="/card")
    async def delete_card(
            self,
            card_token: str,
            **kwargs
    ):
        """
        This method delete tokenized card from wallet
        Source: https://api.monobank.ua/docs/acquiring.html#/paths/~1api~1merchant~1wallet~1card/delete

        :param card_token:
        :param kwargs:
        :return:
        """

        return kwargs["response_data"]


class AsyncMonoAcquiringAPI:
    """
    Asynchronous version MonoAcquiringAPI
    Source: https://api.monobank.ua/docs/acquiring.html
    """

    __base_url: str = "https://api.monobank.ua/api"

    def __init__(self, api_token: str):
        self.__api_token: str = api_token

        kwargs = {
            "api_token": self.__api_token,
            "base_url": self.__base_url
        }

        self.merchant: Merchant = Merchant(**kwargs)

        self.invoice: Invoice = Invoice(**kwargs)

        self.qr: Qr = Qr(**kwargs)

        self.wallet: Wallet = Wallet(**kwargs)

    def get_api_token(self):
        return self.__api_token


class AsyncMonobankOpenAPI:
    """
    Asynchronous version MonobankOpenAPI
    Source: https://api.monobank.ua/docs/
    """

    def __init__(self, api_token: Optional[str] = None):
        super().__init__(api_token=api_token, _async=True)


class AsyncMonobankCorporateOpenAPI(MonobankCorporateOpenAPIModel):
    """
    Asynchronous version MonobankCorporateOpenAPI
    Source: https://api.monobank.ua/docs/corporate.html
    """

    def __init__(self):
        super().__init__(_async=True)
