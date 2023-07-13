__all__ = [
    'MonoAcquiringAPI',
    'MonobankOpenAPI',
    'MonobankCorporateOpenAPI'
]

from typing import Optional

from mbnk.api import (
    APIMethod,
    APIPaths
)


class Merchant(APIMethod):

    @APIMethod._request("get", path=APIPaths.merchant_details)
    def details(self, **kwargs) -> Union[MerchantDetails, MonobankAPIException]:
        """
        Mono Acquiring API: https://api.monobank.ua/docs/acquiring.html#/paths/~1api~1merchant~1details/get

        :return: MerchantDetailsResponse
        """

        return MerchantDetails(**kwargs["response_data"])

    @APIMethod._request("get", path=APIPaths.merchant_statement)
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

    @APIMethod._request("get", path=APIPaths.merchant_pubkey)
    def pubkey(self, **kwargs) -> Union[MerchantPubKey, MonobankAPIException]:
        """
        Mono Acquiring API Docs: https://api.monobank.ua/docs/acquiring.html#/paths/~1api~1merchant~1pubkey/get

        :return: MerchantPubKeyResponse
        """

        return MerchantPubKey(**kwargs["response_data"])


class Invoice(APIMethod):

    @APIMethod._request("post", path=APIPaths.invoice_create)
    def create(
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

    @APIMethod._request("post", path=APIPaths.invoice_cancel)
    def cancel(
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

    def status(
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

    @APIMethod._request("post", path=APIPaths.invoice_invalidation)
    def invalidation(
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

    @APIMethod._request("get", path=APIPaths.invoice_info)
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

    @APIMethod._request("get", path=APIPaths.invoice_finalize)
    def finalize(
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

    @APIMethod._request("get", path=APIPaths.qr_list)
    def list(self, **kwargs) -> Union[QrList, MonobankAPIException]:
        return QrList(
            list=[
                QrListItem(
                    **qr
                ) for qr in kwargs['response']['list']
            ]
        )

    @APIMethod._request("post", path=APIPaths.qr_details)
    def details(
            self,
            qr_id: str,
            **kwargs
    ) -> Union[QrDetails, MonobankAPIException]:
        """
        :param qr_id:
        :return:
        """
        return QrDetails(**kwargs['response_data'])

    @APIMethod._request("post", path=APIPaths.qr_reset_amount)
    def reset_amount(
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

    @APIMethod._request("get", path=APIPaths.wallet_cards)
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

    @APIMethod._request("post", path=APIPaths.wallet_payment)
    async def payment(self):
        """
        Source: https://api.monobank.ua/docs/acquiring.html#/paths/~1api~1merchant~1wallet~1payment/post
        :return:
        """
        pass

    @APIMethod._request("delete", path=APIPaths.wallet_delete_card)
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


class MonoAcquiringAPI(MonoAcquiringAPIModel):
    """
    Synchronous version MonoAcquiringAPI
    Source: https://api.monobank.ua/docs/acquiring.html
    """

    __base_url: str = "https://api.monobank.ua/api"

    def __init__(self, api_token: str):

        self.__api_token: str = api_token

        kwargs = {
            'api_token': self.__api_token,
            'base_url': self.__base_url
        }

        self.merchant: Merchant = Merchant(**kwargs)

        self.invoice: Invoice = Invoice(**kwargs)

        self.qr: Qr = Qr(**kwargs)

        self.wallet: Wallet = Wallet(**kwargs)

    def get_api_token(self):
        return self.__api_token


# Monobank Open API
class Public(APIMethod):

    @APIMethod._request("get", path=APIPaths.currencies_list)
    def currency(self, **kwargs) -> Union[CurrencyList, MonobankAPIException]:

        return CurrencyList.model_validate(kwargs['response_data'])


class Personal(APIMethod):

    @APIMethod._request("get", path=APIPaths.personal_info)
    def info(self, **kwargs) -> Union[ClientInfo, MonobankAPIException]:
        """
        Source: https://api.monobank.ua/docs/#tag/Kliyentski-personalni-dani/paths/~1personal~1client-info/get

        :return:
        """

        return ClientInfo.model_validate(kwargs['response_data'])

    @APIMethod._request("post", path=APIPaths.personal_webhook)
    def set_web_hook(self, web_hook_url: str) -> Union[EmptyResponse, MonobankAPIException]:
        """
        Source: https://api.monobank.ua/docs/#tag/Kliyentski-personalni-dani/paths/~1personal~1webhook/post

        :param web_hook_url:
        :return:
        """
        return EmptyResponse()

    @APIMethod._request("get", path=APIPaths.personal_statement)
    def statement(self, **kwargs) -> Union[Statement, MonobankAPIException]:

        return Statement(
            list=[
                Transaction(
                    **transaction
                ) for transaction in kwargs['response_data']
            ]
        )


class MonobankOpenAPI:
    """
    Synchronous version MonobankOpenAPI
    Source: https://api.monobank.ua/docs/
    """

    __base_url = "https://api.monobank.ua"
    __api_token: str = None

    def __init__(self, api_token: Optional[str] = None):
        self.__api_token = api_token

        kwargs = {
            'base_url': self.__base_url,
            'api_token': self.__api_token
        }

        self.public: Public = Public(**kwargs)

        self.personal: Personal = Personal(**kwargs)

    def set_api_token(self, api_token: str):
        self.__api_token: str = api_token

    def get_api_token(self) -> str:
        return self.__api_token


class MonobankCorporateOpenAPI:
    """
    Synchronous version MonobankCorporateOpenAPI
    Source: https://api.monobank.ua/docs/corporate.html
    """

    __base_url: str = "https://api.monobank.ua"
    __headers: dict = {}

    __key_id: str = None

    __priv_key: str = None
    __pub_key: str = None

    def __init__(self):

        self.public: Public = Public(
            base_url=self.__base_url
        )

        self.auth: Authorization = Authorization(
            base_url=self.__base_url
        )

        self.client: Client = Client(
            base_url=self.__base_url
        )

    def set_key_id(self, key_id: str):
        self.__key_id: str = key_id

    def set_priv_key(self, priv_key_path: str):
        with codecs.open(priv_key_path, 'r', 'utf-8') as f:
            priv_key = f.read()
            f.close()

        self.__priv_key = priv_key

    def set_pub_key(self, pub_key_path: str):
        with codecs.open(pub_key_path, 'r', 'utf-8') as f:
            pub_key = f.read()
            f.close()

        self.__pub_key = pub_key
