__all__ = [
    # Monobank Open API Types
    'CurrencyListItem',
    'Account',
    'Jar',
    'Transaction',
    'CurrencyList',
    'ClientInfo',
    'Statement',

    # Monobank Corporate Open API Types

    # Mono Acquiring API Types
    'QrListItem',
    'QrList',
    'QrDetails',
    'InvoiceCreated',
    'InvoiceCanceled',
    'InvoiceStatus',
    'InvoiceInfo',
    'FinalizeInvoice',
    'Product',
    'MerchantPaymInfo',
    'SaveCardData',
    'CancelListItem',
    'WalletItem',
    'WalletCards',
    'MerchantStatementItem',
    'MerchantDetails',
    'MerchantStatement',
    'MerchantPubKey'
]

import dataclasses
import json

from typing import List, Optional, Union
from dataclasses import dataclass


@dataclass
class BaseType:
    def export(self):
        data = {}
        for key in self.__dict__:
            if self.__dict__[key] is None:
                continue

            if type(self.__dict__[key]) == list:
                data[key] = [
                    (
                        item.export() if dataclasses.is_dataclass(item) else item
                    ) for item in self.__dict__[key]
                ]
            else:
                data[key] = self.__dict__[key]
        return data

    @classmethod
    def parse(cls, data: Union[str, dict]):
        if type(data) == str:
            data = json.loads(data)

        for field, field_type in cls.__annotations__.items():
            if "__origin__" in field_type.__dict__ and field_type.__dict__["__origin__"] == list:
                data[field] = [field_type.__args__[0].parse(item) for item in data[field]]

        return cls(**data)


# Monobank Open API Types

# Public
@dataclass
class CurrencyListItem(BaseType):
    currency_code_a: int
    currency_code_b: int
    date: int
    rate_sell: float
    rate_buy: float
    rate_cross: float


@dataclass
class CurrencyList:
    list: List[CurrencyListItem]


# Personal
@dataclass
class Account(BaseType):
    id: str
    send_id: str
    balance: int
    credit_limit: int
    type: str
    currency_code: int
    masked_pan: List[str]
    iban: str
    cashback_type: Optional[str] = None


@dataclass
class Jar(BaseType):
    id: str
    send_id: str
    title: str
    description: str
    currency_code: int
    balance: int
    goal: int


@dataclass
class Transaction(BaseType):
    id: str
    time: int
    description: str
    mcc: int
    original_mcc: int
    hold: bool
    amount: int
    operation_amount: int
    currency_code: int
    commission_rate: int
    cashback_amount: int
    balance: int
    comment: Optional[str] = None
    receipt_id: Optional[str] = None
    invoice_id: Optional[str] = None
    counter_edrpou: Optional[str] = None
    counter_iban: Optional[str] = None
    counter_name: Optional[str] = None


@dataclass
class ClientInfo:
    client_id: str
    name: str
    web_hook_url: str
    permissions: str
    accounts: List[Account]
    jars: List[Jar]


@dataclass
class Statement:
    list: List[Transaction]


# Mono Acquiring API

# Qr
@dataclass
class QrListItem(BaseType):
    short_qr_id: str
    qr_id: str
    amount_type: str
    page_url: str


@dataclass
class QrList:
    list: List[QrListItem]


@dataclass
class QrDetails:
    short_qr_id: str
    invoice_id: Optional[str]
    amount: Optional[int]
    ccy: Optional[int]


# Invoice
@dataclass
class CanceledItem(BaseType):
    pass


@dataclass
class InvoiceCreated:
    invoice_id: str
    page_url: str


@dataclass
class InvoiceCanceled:
    status: str
    created_date: str
    modified_date: str


@dataclass
class InvoiceStatus:
    pass


@dataclass
class InvoiceInfo:
    pass


@dataclass
class FinalizeInvoice:
    status: str


@dataclass
class Product(BaseType):
    name: str
    qty: float
    sum: int
    icon: Optional[str] = None
    unit: Optional[str] = None
    code: Optional[str] = None
    barcode: Optional[str] = None
    header: Optional[str] = None
    footer: Optional[str] = None
    tax: Optional[List[int]] = None
    uktzed: Optional[str] = None


@dataclass
class MerchantPaymInfo(BaseType):
    reference: str
    destination: str
    basket_order: List[Product]


@dataclass
class SaveCardData(BaseType):
    save_card: bool
    wallet_id: Optional[str] = None


@dataclass
class CancelListItem(BaseType):
    amount: int
    ccy: int
    date: str
    masked_pan: str
    approval_code: Optional[str] = None
    rrn: Optional[str] = None


# Merchant
@dataclass
class MerchantStatementItem(BaseType):
    invoice_id: str
    status: str
    masked_pan: str
    date: str
    payment_scheme: str
    amount: int
    ccy: int
    profit: Optional[int] = None
    approval_code: Optional[str] = None
    reference: Optional[str] = None
    cancel_list: List[CancelListItem] = None
    rrn: Optional[str] = None
    short_qr_id: Optional[str] = None


@dataclass
class MerchantDetails(BaseType):
    merchant_id: str
    merchant_name: str


@dataclass
class MerchantStatement(BaseType):
    list: List[MerchantStatementItem]


@dataclass
class MerchantPubKey(BaseType):
    key: str


# Wallet
@dataclass
class WalletItem(BaseType):
    card_token: str
    masked_pan: str
    country: Optional[str] = None


@dataclass
class WalletCards(BaseType):
    wallets: List[WalletItem]
