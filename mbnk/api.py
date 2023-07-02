from typing import Union, Optional

from mbnk.decorators import api_method
from mbnk.enums import APIPaths

from mbnk.exceptions import (
    MonobankAPIException,
    MonoPayAPIException
)

from mbnk.instances import *

from mbnk.responses import *


# Monobank Open API
class Public:

    __base_url__ = None
    __headers__ = {}

    def __init__(
            self,
            base_url: str,
            headers: dict,
            _async: bool
    ):
        self.__is_async__ = _async

        self.__base_url__ = base_url
        self.__headers__ = headers

    @api_method("get", url=APIPaths.currencies_list)
    def currency_rates(self, **kwargs) -> Union[CurrencyRatesResponse, MonobankAPIException]:

        return CurrencyRatesResponse(
            list=[
                CurrencyListItem(
                    **item
                ) for item in kwargs['response_data']
            ]
        )


class Personal:

    __base_url__ = None
    __headers__ = {}

    def __init__(
            self,
            base_url: str,
            headers: dict,
            _async: bool
    ):
        self.__is_async__ = _async

        self.__base_url__ = base_url
        self.__headers__ = headers

    @api_method("get", url=APIPaths.personal_info)
    def info(self, **kwargs) -> Union[ClientInfoResponse, MonobankAPIException]:
        """
        Source: https://api.monobank.ua/docs/#tag/Kliyentski-personalni-dani/paths/~1personal~1client-info/get

        :return:
        """

        return ClientInfoResponse(
            client_id=kwargs['response_data']['client_id'],
            name=kwargs['response_data']['name'],
            web_hook_url=kwargs['response_data']['web_hook_url'],
            permissions=kwargs['response_data']['permissions'],
            accounts=[
                Account(
                    **account
                ) for account in kwargs['response_data']['accounts']
            ],
            jars=[
                Jar(
                    **jar
                ) for jar in kwargs['response_data']['jars']
            ]
        )

    @api_method("post", url=APIPaths.personal_webhook)
    def set_webhook(self, web_hook_url: str) -> Union[EmptyResponse, MonobankAPIException]:
        """
        Source: https://api.monobank.ua/docs/#tag/Kliyentski-personalni-dani/paths/~1personal~1webhook/post

        :param web_hook_url:
        :return:
        """
        return EmptyResponse()

    @api_method("get", url=APIPaths.personal_statement)
    def statement(self, **kwargs) -> Union[StatementResponse, MonobankAPIException]:

        return StatementResponse(
            list=[
                Transaction(
                    **transaction
                ) for transaction in kwargs['response_data']
            ]
        )


class Corporate:

    __base_url__ = None
    __headers__ = {}

    def __init__(
            self,
            base_url: str,
            headers: dict,
            _async: bool
    ):
        self.__is_async__ = _async

        self.__base_url__ = base_url
        self.__headers__ = headers

        self.auth: Authorization = Authorization(
            base_url=self.__base_url__,
            headers=self.__headers__,
            _async=self.__is_async__
        )

        self.client: Client = Client(
            base_url=self.__base_url__,
            headers=self.__headers__,
            _async=self.__is_async__
        )

    def set_webhook(self):
        pass

    def info(self):
        pass


class Client:

    __base_url__ = None
    __headers__ = {}

    def __init__(
            self,
            base_url: str,
            headers: dict,
            _async: bool
    ):
        self.__is_async__ = _async

        self.__base_url__ = base_url
        self.__headers__ = headers

    def init_access(self):
        pass

    def check_access(self):
        pass


class Authorization:

    __base_url__ = None
    __headers__ = {}

    def __init__(
            self,
            base_url: str,
            headers: dict,
            _async: bool
    ):
        self.__is_async__ = _async

        self.__base_url__ = base_url
        self.__headers__ = headers

    def registration(self):
        pass

    def status(self):
        pass


class MonobankOpenAPI:

    __base_url__ = "https://api.monobank.ua"
    __api_token__ = None
    __headers__ = {}

    def __init__(self, api_token: str, _async: bool):
        self.__is_async__ = _async

        self.__api_token__ = api_token
        self.__headers__["X-Token"] = self.__api_token__

        self.public: Public = Public(
            base_url=self.__base_url__,
            headers=self.__headers__,
            _async=self.__is_async__
        )

        self.personal: Personal = Personal(
            base_url=self.__base_url__,
            headers=self.__headers__,
            _async=self.__is_async__
        )

        self.corporate: Corporate = Corporate(
            base_url=self.__base_url__,
            headers=self.__headers__,
            _async=self.__is_async__
        )


# MonoPay
class Merchant:

    __base_url__ = None
    __headers__ = {}

    def __init__(
            self,
            base_url: str,
            headers: dict,
            _async: bool
    ):
        self.__is_async__ = _async

        self.__base_url__ = base_url
        self.__headers__ = headers

    # @async_request(url=APIPaths.merchant_details, method="get")

    @api_method("get", url=APIPaths.merchant_details)
    def details(self, **kwargs) -> Union[MerchantDetailsResponse, MonoPayAPIException]:
        """
        Mono Acquiring API: https://api.monobank.ua/docs/acquiring.html#/paths/~1api~1merchant~1details/get

        :return: MerchantDetailsResponse
        """

        return MerchantDetailsResponse(**kwargs["response_data"])

    @api_method("get", url=APIPaths.merchant_statement)
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

    @api_method("get", url=APIPaths.merchant_pubkey)
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
            headers: dict,
            _async: bool
    ):
        self.__is_async__ = _async

        self.__base_url__ = base_url
        self.__headers__ = headers

    @api_method("post", url=APIPaths.invoice_create)
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

    @api_method("post", url=APIPaths.invoice_split)
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

    @api_method("post", url=APIPaths.invoice_cancel)
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

    @api_method("post", url=APIPaths.invoice_invalidation)
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
            headers: dict,
            _async: bool
    ):
        self.__is_async__ = _async

        self.__base_url__ = base_url
        self.__headers__ = headers

    @api_method("get", url=APIPaths.qr_list)
    def list(self, **kwargs) -> Union[QrListResponse, MonoPayAPIException]:
        return QrListResponse(
            list=[
                QrListItem(
                    **qr
                ) for qr in kwargs['response']['list']
            ]
        )

    @api_method("post", url=APIPaths.qr_details)
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

    @api_method("post", url=APIPaths.qr_reset_amount)
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
            headers: dict,
            _async: bool
    ):
        self.__is_async__ = _async

        self.__base_url__ = base_url
        self.__headers__ = headers

    @api_method("get", url=APIPaths.wallet_cards)
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

    @api_method("delete", url=APIPaths.wallet_delete_card)
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


class MonoPayAPI:

    __base_url__ = "https://api.monobank.ua"
    __api_token__ = None
    __headers__ = {}

    def __init__(self, api_token: str, _async: bool):
        self.__is_async__ = _async

        self.__api_token__ = api_token
        self.__headers__["X-Token"] = self.__api_token__

        self.merchant: Merchant = Merchant(
            base_url=self.__base_url__,
            headers=self.__headers__,
            _async=self.__is_async__
        )

        self.invoice: Invoice = Invoice(
            base_url=self.__base_url__,
            headers=self.__headers__,
            _async=self.__is_async__
        )

        self.qr: Qr = Qr(
            base_url=self.__base_url__,
            headers=self.__headers__,
            _async=self.__is_async__
        )

        self.wallet: Wallet = Wallet(
            base_url=self.__base_url__,
            headers=self.__headers__,
            _async=self.__is_async__
        )

    def get_api_token(self):
        return self.__api_token__
