import requests

from typing import Union

from mbnk.decorators import request, post_request
from mbnk.responses import CurrencyRatesResponse
from mbnk.responses import ClientInfoResponse
from mbnk.responses import StatementResponse

from mbnk.instances import CurrencyListItem
from mbnk.instances import Account
from mbnk.instances import Jar
from mbnk.instances import Transaction

from mbnk.exceptions import MonobankBaseException

from mbnk.utils import is_exception


class PublicData:
    def __init__(
        self,
        base_url: str,
        headers
    ):
        self.base__url = base_url
        self.headers = headers

        self.currency_rates_url = f"{self.base__url}/bank/currency"

    @request(url='currency_rates_url')
    def currency_rates(self, response_data) -> Union[CurrencyRatesResponse, MonobankBaseException]:

        return CurrencyRatesResponse(
            list=[
                CurrencyListItem(
                    currency_code_a=int(response_item['currencyCodeA']),
                    currency_code_b=int(response_item['currencyCodeB']),
                    date=response_item['date'],
                    rate_sell=response_item['rateSell'],
                    rate_buy=response_item['rateBuy'],
                    rate_cross=response_item['rateCross']
                ) for response_item in response_data
            ]
        )


class Personal:
    def __init__(
        self,
        base_url: str,
        headers
    ):
        self.base__url = base_url
        self.headers = headers

        self.client_info_url = f"{self.base__url}/personal/client-info"
        self.set_webhook_url = f"{self.base__url}/personal/webhook"
        self.statement_url = self.base__url + "/personal/statement/{account}/{from_date}"

    @request(url='client_info_url')
    def info(self, response_data):

        return ClientInfoResponse(
            client_id=response_data['clientId'],
            name=response_data['name'],
            web_hook_url=response_data['webHookUrl'],
            permissions=response_data['permissions'],
            accounts=[
                Account(
                    id=account['id'],
                    send_id=account['sendId'],
                    balance=int(account['balance']),
                    credit_limit=int(account['creditLimit']),
                    type=account['type'],
                    currency_code=int(account['currencyCode']),
                    cashback_type=account['cashbackType'] if 'cashbackType' in account else None,
                    masked_pan=account['maskedPan'],
                    iban=account['iban'],
                ) for account in response_data['accounts']
            ],
            jars=[
                Jar(
                    id=jar['id'],
                    send_id=jar['sendId'],
                    title=jar['title'],
                    description=jar['description'],
                    currency_code=int(jar['currencyCode']),
                    balance=int(jar['balance']),
                    goal=int(jar['goal'])
                ) for jar in response_data['jars']
            ]
        )

    @post_request
    def set_webhook(self, web_hook_url: str):
        pass

    def statement(self, from_date: int, to_date: int = None, account: str = 0):
        print(self.statement_url.format(
                account=account,
                from_date=from_date,
                # to_date=to_date if to_date else '',
            ))
        response = requests.get(
            url=self.statement_url.format(
                account=account,
                from_date=from_date,
                to_date=to_date,
            ),
            headers=self.headers
        )

        response_data = response.json()

        if is_exception(response):
            return MonobankBaseException(
                err_description=response_data['errorDescription']
            )

        return StatementResponse(
            list=[
                Transaction(
                    id=transaction['id'],
                    time=transaction['time'],
                    description=transaction['description'],
                    mcc=transaction['mcc'],
                    original_mcc=transaction['originalMcc'],
                    hold=transaction['hold'],
                    amount=transaction['amount'],
                    operation_amount=transaction['operationAmount'],
                    currency_code=transaction['currencyCode'],
                    commission_rate=transaction['commissionRate'],
                    cashback_amount=transaction['cashbackAmount'],
                    balance=transaction['balance'],
                    comment=transaction['comment'] if 'comment' in transaction else None,
                    receipt_id=transaction['receiptId'] if 'receiptId' in transaction else None,
                    invoice_id=transaction['invoiceId'] if 'invoiceId' in transaction else None,
                    counter_edrpou=transaction['counterEdrpou'] if 'counterEdrpou' in transaction else None,
                    counter_iban=transaction['counterIban'] if 'counterIban' in transaction else None,
                    counter_name=transaction['counterName'] if 'counterName' in transaction else None,
                ) for transaction in response_data
            ]
        )


class Monobank:
    def __init__(self, api_token):
        self.api_token = api_token
        self.base_url = "https://api.monobank.ua"
        self.headers = {
            "X-Token": self.api_token
        }

        self.public = PublicData(
            base_url=self.base_url,
            headers=self.headers
        )
        self.personal = Personal(
            base_url=self.base_url,
            headers=self.headers
        )
