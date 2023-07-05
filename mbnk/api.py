__all__ = [
    'MonobankOpenAPIModel',
    'MonobankCorporateOpenAPIModel',
    'MonoAcquiringAPIModel'
]

import base64
import codecs

import ecdsa
import hashlib

import re
import json
import requests

from enum import Enum
from datetime import datetime

from requests import Response
from aiohttp import (
    ClientSession,
    ClientResponse
)
from typing import Union, Optional

from mbnk.exceptions import *

from mbnk.types import *

from mbnk.responses import *

import dataclasses


class APIMethod:

    __api_token = None
    __headers = {}

    def __init__(
            self,
            base_url: str,
            _async: bool,
            api_token: Optional[str] = None,
    ):
        self.__is_async: bool = _async
        self.__base_url: str = base_url

        if api_token is not None:
            self.__api_token: str = api_token
            self.__headers["X-Token"] = self.__api_token

    @staticmethod
    def __camel_to_underscore(text: str):
        camel_pat = re.compile(r'([A-Z])')
        return camel_pat.sub(lambda x: '_' + x.group(1).lower(), text)

    @staticmethod
    def __underscore_to_camel(text: str):
        under_pat = re.compile(r'_([a-z])')
        return under_pat.sub(lambda x: x.group(1).upper(), text)

    def __json_convert(self, data, convert):
        if isinstance(data, dict):
            new_data = {}
            for k, value in data.items():
                new_data[convert(k)] = self.__json_convert(value, convert) if (
                    isinstance(value, dict)
                ) else self.__json_convert(value, convert) if isinstance(value, list) else value
            return new_data
        elif isinstance(data, list):
            new_list = []
            for item in data:
                new_list.append(self.__json_convert(item, convert))
            return new_list

    def __load_response(self, response_data: Union[dict, list]):

        return self.__json_convert(response_data, self.__camel_to_underscore)

    def __build_data(self, **kwargs):
        data = {}

        for kwarg in kwargs:
            key = kwarg.replace("timestamp", "")
            key = self.__underscore_to_camel(key)

            value = kwargs.get(kwarg)

            if dataclasses.is_dataclass(value):
                data[key] = value.export()
            else:
                data[key] = value

        data = self.__json_convert(data, self.__underscore_to_camel)

        return data

    @staticmethod
    def __is_exception(response: Union[Response, ClientResponse]) -> bool:
        if isinstance(response, Response):
            status_code = response.status_code
        elif isinstance(response, ClientResponse):
            status_code = response.status
        else:
            return True

        if status_code != 200:
            return True

        return False

    @staticmethod
    def __get_exception(response: Union[Response, ClientResponse]):
        if isinstance(response, Response):
            status_code = response.status_code
        elif isinstance(response, ClientResponse):
            status_code = response.status
        else:
            return

        if status_code == 400:
            raise Exception
        elif status_code == 403:
            raise Exception
        elif status_code == 404:
            raise Exception
        elif status_code == 429:
            raise TooManyRequestsException
        else:
            return MonoPayAPIException

    def __sync_request(
            self,
            method: str,
            path: str,
            data: str = None,
            params: str = None
    ):
        request = getattr(requests, method)
        response = request(
            url=f"{self.__base_url}/{path}",
            headers=self.__headers,
            params=params,
            data=json.dumps(data) if data is not None else None
        )
        response_data = response.json()
        response_data = self.__load_response(response_data)

        if self.__is_exception(response):
            raise self.__get_exception(response)

        return response_data

    async def __async_request(
            self,
            method: str,
            path: str,
            data: str = None,
            params: str = None
    ):
        async with ClientSession() as session:
            request = getattr(session, method)
            async with request(
                    url=f"{self.__base_url}/{path}",
                    headers=self.__headers,
                    data=json.dumps(data) if data is not None else None,
                    params=params
            ) as response:
                response_data = await response.json()
                response_data = self.__load_response(response_data)

                if self.__is_exception(response):
                    raise self.__get_exception(response)

                return response_data

    @staticmethod
    def _time_header():
        def outer(func):
            def inner(self):
                self.__headers["X-Time"]: str = str(int(datetime.now().timestamp()))

            return inner

        return outer

    @staticmethod
    def _key_id_header():
        def outer(func):
            def inner(self):
                self.__headers["X-Key-Id"]: str = self.__key_id

            return inner

        return outer

    @staticmethod
    def __generate_request_id():
        request_id = ""

        return request_id

    @staticmethod
    def _request_id_header():
        def outer(func):
            def inner(self):
                self.__headers["X-Request-Id"]: str = self.__generate_request_id()

            return inner

        return outer

    @staticmethod
    def __create_signature(self):
        url = "https://api.monobank.ua"
        data = (self.__headers["X-Time"] + url).encode('utf-8')

        private_key = ecdsa.SigningKey.from_pem(self.__privkey, hashfunc=hashlib.sha256)

        sign = private_key.sign(data, hashfunc=hashlib.sha256)
        sign_base64 = base64.b64encode(sign)

        return sign_base64

    @staticmethod
    def _sign_header():
        def outer(func):
            def inner(self):
                self.__headers["X-Sign"]: str = self.__create_signature(self)
            return inner

        return outer

    @staticmethod
    def _request(
            request_method: str,
            path: str
    ):
        def outer(func):
            def inner(*args, **kwargs):
                self = args[0]
                args = args[1:]
                func_args = {
                    "method": request_method,
                    "path": path,
                    ("params" if request_method == "get" else "data"): self.__build_data(**kwargs)
                }

                async def async_wrapper():
                    response = await self.__async_request(**func_args)

                    if isinstance(response, MonoPayAPIException) or isinstance(response, MonobankAPIException):
                        return response

                    return func(self, *args, **kwargs, response_data=response)

                def sync_wrapper():
                    response = self.__sync_request(**func_args)

                    return func(self, *args, **kwargs, response_data=response)

                if self.__is_async:
                    return async_wrapper()
                else:
                    return sync_wrapper()

            return inner

        return outer


class APIPaths(str, Enum):
    # Mono Acquiring API
    merchant_details = "merchant/details"
    merchant_statement = "merchant/statement"
    merchant_pubkey = "merchant/pubkey"

    invoice_create = "merchant/invoice/create"
    invoice_split = "merchant/invoice/split-payments"
    invoice_cancel = "merchant/invoice/cancel"
    invoice_status = "merchant/invoice/status"
    invoice_invalidation = "merchant/invoice/remove"
    invoice_info = "merchant/invoice/payment-info"
    invoice_finalize = "merchant/invoice/finalize"

    qr_list = "merchant/qr/list"
    qr_details = "merchant/qr/details"
    qr_reset_amount = "merchant/qr/reset-amount"

    wallet_cards = "merchant/wallet"
    wallet_payment = "merchant/wallet/payment"
    wallet_delete_card = "merchant/wallet/card"

    # Monobank Open API
    currencies_list = "bank/currency"

    personal_info = "personal/client-info"
    personal_webhook = "personal/webhook"
    personal_statement = "personal/statement/{account}/{from}/{to}"

    # Monobank Corporate Open API
    auth_registration = "personal/auth/registration"
    auth_status = "personal/auth/registration/status"

    corporate_webhook = "personal/corp/webhook"
    corporate_info = "personal/corp/settings"

    init_access = "personal/auth/request"
    check_access = "personal/auth/request"


# Monobank Open API
class Public(APIMethod):

    @APIMethod._request("get", path=APIPaths.currencies_list)
    def currency(self, **kwargs) -> Union[CurrencyList, MonobankAPIException]:

        return CurrencyList(
            list=[
                CurrencyListItem(
                    **item
                ) for item in kwargs['response_data']
            ]
        )


class Personal(APIMethod):

    @APIMethod._request("get", path=APIPaths.personal_info)
    def info(self, **kwargs) -> Union[ClientInfo, MonobankAPIException]:
        """
        Source: https://api.monobank.ua/docs/#tag/Kliyentski-personalni-dani/paths/~1personal~1client-info/get

        :return:
        """

        return ClientInfo(
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


class MonobankOpenAPIModel:

    __base_url = "https://api.monobank.ua"
    __is_async: bool = False
    __api_token: str = None

    def __init__(self, _async: bool, api_token: Optional[str] = None):

        self.__is_async = _async
        self.__api_token = api_token

        kwargs = {
            'base_url': self.__base_url,
            'api_token': self.__api_token,
            '_async': self.__is_async
        }

        self.public: Public = Public(**kwargs)

        self.personal: Personal = Personal(**kwargs)

    def set_api_token(self, api_token: str):
        self.__api_token: str = api_token

    def get_api_token(self) -> str:
        return self.__api_token


class Client(APIMethod):

    @APIMethod._request("post", path=APIPaths.init_access)
    def init_access(self):
        pass

    @APIMethod._request("get", path=APIPaths.check_access)
    def check_access(self):
        pass


class Authorization(APIMethod):

    @APIMethod._request("post", path=APIPaths.auth_registration)
    def registration(self):
        pass

    @APIMethod._request("post", path=APIPaths.auth_status)
    def status(self):
        pass


class MonobankCorporateOpenAPIModel:

    __base_url: str = "https://api.monobank.ua"
    __headers: dict = {}

    __key_id: str = None

    __priv_key: str = None
    __pub_key: str = None

    def __init__(self, _async: bool):
        self.__is_async: bool = _async

        self.public: Public = Public(
            base_url=self.__base_url,
            _async=self.__is_async
        )

        self.auth: Authorization = Authorization(
            base_url=self.__base_url,
            _async=self.__is_async
        )

        self.client: Client = Client(
            base_url=self.__base_url,
            _async=self.__is_async
        )

    def set_web_hook(self):
        pass

    def info(self):
        pass

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


# MonoPay
class Merchant(APIMethod):

    @APIMethod._request("get", path=APIPaths.merchant_details)
    def details(self, **kwargs) -> Union[MerchantDetails, MonoPayAPIException]:
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
    ) -> Union[MerchantStatement, MonoPayAPIException]:
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
    def pubkey(self, **kwargs) -> Union[MerchantPubKey, MonoPayAPIException]:
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
    ) -> Union[InvoiceCreated, MonoPayAPIException]:
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
    ) -> Union[InvoiceCanceled, MonoPayAPIException]:
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
    ) -> Union[InvoiceStatus, MonoPayAPIException]:
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
    ) -> Union[EmptyResponse, MonoPayAPIException]:
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
    ) -> Union[InvoiceInfo, MonoPayAPIException]:
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
    ) -> Union[FinalizeInvoice, MonoPayAPIException]:
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
    def list(self, **kwargs) -> Union[QrList, MonoPayAPIException]:
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
    ) -> Union[QrDetails, MonoPayAPIException]:
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
    ) -> Union[EmptyResponse, MonoPayAPIException]:
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


class MonoAcquiringAPIModel:

    __base_url: str = "https://api.monobank.ua/api"
    __is_async: bool = False

    def __init__(self, api_token: str, _async: bool):

        self.__is_async: bool = _async
        self.__api_token: str = api_token

        self.merchant: Merchant = Merchant(
            api_token=self.__api_token,
            base_url=self.__base_url,
            _async=self.__is_async
        )

        self.invoice: Invoice = Invoice(
            api_token=self.__api_token,
            base_url=self.__base_url,
            _async=self.__is_async
        )

        self.qr: Qr = Qr(
            api_token=self.__api_token,
            base_url=self.__base_url,
            _async=self.__is_async
        )

        self.wallet: Wallet = Wallet(
            api_token=self.__api_token,
            base_url=self.__base_url,
            _async=self.__is_async
        )

    def get_api_token(self):
        return self.__api_token
