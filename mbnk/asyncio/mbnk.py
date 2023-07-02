from aiohttp import ClientSession

from typing import Union, Optional
from mbnk.decorators import (
    async_request,
    async_post_request
)
from mbnk.enums import MonoPayApiUrls

from mbnk.exceptions import (
    MonobankAPIException,
    MonoPayAPIException
)

from mbnk.instances import (
    MerchantStatementItem,
    CancelListItem,

    QrListItem
)

from mbnk.responses import (
    EmptyResponse,

    # Merchant Responses
    MerchantDetailsResponse,
    MerchantStatementResponse,
    MerchantPubKeyResponse,

    # Qr Responses
    QrDetailsResponse,
    QrListResponse,

    # Invoice Responses
    InvoiceCreatedResponse,
    SplitInvoiceResponse,
    InvoiceCanceledResponse,
    InvoiceStatusResponse,
    InvoiceInfoResponse,
    FinalizeInvoiceResponse
)


def api_request():
    pass


def async_api_request():
    def outer(func):
        async def inner(
                self,
                url: str,
                method: str,
                data: str = None,
                params: str = None,
                *args,
                **kwargs
        ):

            async with ClientSession() as session:
                request = getattr(session, method)
                async with request(
                        url=url.format(
                            base_url=self.__base_url__
                        ),
                        headers=self.__headers__,
                        data=data,
                        params=params
                ) as response:

                    return func(self, *args, **kwargs, response=response)

        return inner

    return outer


class APIMethod:
    def __init__(self):
        pass

    def get(self, url):
        print(self.__is_async)

    def post(self):
        pass

    def delete(self):
        pass


class Public:

    __base_url__ = None
    __headers__ = {}

    def __init__(
            self,
            base_url: str,
            headers: dict
    ):
        self.__base_url__ = base_url
        self.__headers__ = headers


class Personal:

    __base_url__ = None
    __headers__ = {}

    def __init__(
            self,
            base_url: str,
            headers: dict
    ):
        self.__base_url__ = base_url
        self.__headers__ = headers


class Monobank:

    __base_url__ = "https://api.monobank.ua"
    __api_token__ = None
    __headers__ = {}

    def __init__(self):
        self.public: Public = Public(
            base_url=self.__base_url__,
            headers=self.__headers__
        )

        self.personal: Personal = Personal(
            base_url=self.__base_url__,
            headers=self.__headers__
        )


# MonoPay
class Merchant:

    __base_url__ = None
    __headers__ = {}

    def __init__(
            self,
            base_url: str,
            headers: dict
    ):
        self.__base_url__ = base_url
        self.__headers__ = headers

    @async_request(url=MonoPayApiUrls.merchant_details, method="get")
    def details(self, **kwargs) -> Union[MerchantDetailsResponse, MonoPayAPIException]:
        """
        Mono Acquiring API: https://api.monobank.ua/docs/acquiring.html#/paths/~1api~1merchant~1details/get

        :return: MerchantDetailsResponse
        """

        return MerchantDetailsResponse(**kwargs["response_data"])

    @async_request(url=MonoPayApiUrls.merchant_statement, method="get")
    def statement(
            self,
            from_timestamp: int,
            to_timestamp: Optional[int] = None,
            **kwargs
    ) -> Union[MerchantStatementResponse, MonoPayAPIException]:
        """
        Mono Acquiring API: https://api.monobank.ua/docs/acquiring.html#/paths/~1api~1merchant~1statement/get

        :param from_timestamp:
        :param to_timestamp:
        :param kwargs:
        :return:
        """

        return MerchantStatementResponse(
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

    @async_request(url=MonoPayApiUrls.merchant_pubkey, method="get")
    def pubkey(self, **kwargs) -> Union[MerchantPubKeyResponse, MonoPayAPIException]:
        """
        Mono Acquiring API Docs: https://api.monobank.ua/docs/acquiring.html#/paths/~1api~1merchant~1pubkey/get

        :return: MerchantPubKeyResponse
        """

        return MerchantPubKeyResponse(**kwargs["response_data"])


class Invoice:

    __base_url__ = None
    __headers__ = {}

    def __init__(
            self,
            base_url: str,
            headers: dict
    ):
        self.__base_url__ = base_url
        self.__headers__ = headers

    @async_post_request(url=MonoPayApiUrls.invoice_create)
    def create(
            self,
            amount: int,
            ccy: Optional[int] = None,
            merchant_paym_info: Optional = None,
            redirect_url: Optional[str] = None,
            web_hook_url: Optional[str] = None,
            validity: Optional[int] = None,
            payment_type: Optional[str] = None,
            qr_id: Optional = None,
            save_card_data: Optional = None,
            **kwargs
    ) -> Union[InvoiceCreatedResponse, MonoPayAPIException]:
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

        return InvoiceCreatedResponse(**kwargs['response_data'])

    @async_request(url=MonoPayApiUrls.invoice_split, method="post")
    def split(
            self,
            invoice_id: str,
            **kwargs
    ) -> Union[SplitInvoiceResponse, MonoPayAPIException]:
        """
        Mono Acquiring API:

        :param invoice_id:
        :param kwargs:
        :return:
        """

        return SplitInvoiceResponse(**kwargs['response_data'])

    @async_request(url=MonoPayApiUrls.invoice_cancel, method="post")
    def cancel(
            self,
            invoice_id: str,
            ext_ref: str = None,
            amount: int = None,
            items=None,
            **kwargs
    ) -> Union[InvoiceCanceledResponse, MonoPayAPIException]:
        """
        Mono Acquiring API: https://api.monobank.ua/docs/acquiring.html#/paths/~1api~1merchant~1invoice~1cancel/post

        :param invoice_id:
        :param ext_ref:
        :param amount:
        :param items:
        :param kwargs:
        :return:
        """
        return InvoiceCanceledResponse(**kwargs['response_data'])

    def status(
            self,
            invoice_id: str,
            **kwargs
    ) -> Union[InvoiceStatusResponse, MonoPayAPIException]:
        """
        Mono Acquiring API: https://api.monobank.ua/docs/acquiring.html#/paths/~1api~1merchant~1invoice~1status?invoiceId=%7BinvoiceId%7D/get

        :param invoice_id:
        :param kwargs:
        :return:
        """

        return kwargs["response_data"]

    @async_request(url=MonoPayApiUrls.invoice_invalidation, method="post")
    def invalidation(
            self,
            invoice_id: str,
            **kwargs
    ) -> Union[EmptyResponse, MonoPayAPIException]:
        """
        Source: https://api.monobank.ua/docs/acquiring.html#/paths/~1api~1merchant~1invoice~1remove/post

        :param invoice_id:
        :param kwargs:
        :return:
        """

        return EmptyResponse()

    async def info(
            self,
            invoice_id: str,
            **kwargs
    ) -> Union[InvoiceInfoResponse, MonoPayAPIException]:
        """
        Source: https://api.monobank.ua/docs/acquiring.html#/paths/~1api~1merchant~1invoice~1payment-info?invoiceId=%7BinvoiceId%7D/get

        :param invoice_id:
        :param kwargs:
        :return:
        """

        return kwargs['response_data']

    def finalize(
            self,
            invoice_id: str,
            amount: int,
            **kwargs
    ) -> Union[FinalizeInvoiceResponse, MonoPayAPIException]:
        """
        Source: https://api.monobank.ua/docs/acquiring.html#/paths/~1api~1merchant~1invoice~1finalize/post

        :param invoice_id:
        :param amount:
        :param kwargs:
        :return:
        """
        return FinalizeInvoiceResponse(
            **kwargs['response_data']
        )


class Qr:

    __base_url__ = None
    __headers__ = {}

    def __init__(
            self,
            base_url: str,
            headers: dict
    ):
        self.__base_url__ = base_url
        self.__headers__ = headers

    @async_request(url=MonoPayApiUrls.qr_list, method="get")
    def list(self, **kwargs) -> Union[QrListResponse, MonoPayAPIException]:
        return QrListResponse(
            list=[
                QrListItem(
                    **qr
                ) for qr in kwargs['response']['list']
            ]
        )

    @async_request(url=MonoPayApiUrls.qr_details, method="post")
    def details(
            self,
            qr_id: str,
            **kwargs
    ) -> Union[QrDetailsResponse, MonoPayAPIException]:
        """
        :param qr_id:
        :return:
        """
        return QrDetailsResponse(**kwargs['response_data'])

    @async_request(url=MonoPayApiUrls.qr_reset_amount, method="post")
    def reset_amount(
            self,
            qr_id: str,
            **kwargs
    ) -> Union[EmptyResponse, MonoPayAPIException]:
        """
        :param qr_id:
        :return:
        """
        return EmptyResponse()


class Wallet:

    __base_url__ = None
    __headers__ = {}

    def __init__(
            self,
            base_url: str,
            headers: dict
    ):
        self.__base_url__ = base_url
        self.__headers__ = headers

    @async_request(url=MonoPayApiUrls.wallet_cards, method="get")
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

    async def payment(self):
        """
        Source: https://api.monobank.ua/docs/acquiring.html#/paths/~1api~1merchant~1wallet~1payment/post
        :return:
        """
        pass

    @async_request(url=MonoPayApiUrls.wallet_delete_card, method="delete")
    def delete_card(
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


class AsyncMonoPay:

    __base_url__ = "https://api.monobank.ua"
    __api_token__ = None
    __headers__ = {}

    def __init__(self, api_token: str):
        self.__api_token__ = api_token
        self.__headers__["X-Token"] = self.__api_token__

        self.merchant: Merchant = Merchant(
            base_url=self.__base_url__,
            headers=self.__headers__
        )

        self.invoice: Invoice = Invoice(
            base_url=self.__base_url__,
            headers=self.__headers__
        )

        self.qr: Qr = Qr(
            base_url=self.__base_url__,
            headers=self.__headers__
        )

        self.wallet: Wallet = Wallet(
            base_url=self.__base_url__,
            headers=self.__headers__
        )

    def get_api_token(self):
        return self.__api_token__
