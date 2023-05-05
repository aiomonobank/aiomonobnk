from typing import List
from dataclasses import dataclass
from mbnk.instances import CurrencyListItem
from mbnk.instances import Account
from mbnk.instances import Jar
from mbnk.instances import Transaction


@dataclass
class EmptyResponse:
    pass


@dataclass
class CurrencyRatesResponse:
    list: List[CurrencyListItem]


@dataclass
class ClientInfoResponse:
    client_id: str
    name: str
    web_hook_url: str
    permissions: str
    accounts: List[Account]
    jars: List[Jar]


@dataclass
class StatementResponse:
    list: List[Transaction]
