__all__ = [
    # Monobank Open API Types
    'Currency',
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
    'InvoiceCanceled',
    'InvoiceInfo',
    'FinalizeInvoice',
    'CancelListItem',
    'WalletItem',
    'WalletCards',
]

from typing import List, Optional, Union
from pydantic import BaseModel, Field
from pydantic.dataclasses import dataclass
from .enums import *


# Monobank Open API Types

# Public
@dataclass
class Currency(BaseModel):
    currency_code_a: CurrencyCode = Field(alias='currencyCodeA')
    currency_code_b: CurrencyCode = Field(alias='currencyCodeB')
    date: int
    rate_sell: float = Field(alias='rateSell')
    rate_buy: float = Field(alias='rateBuy')
    rate_cross: float = Field(alias='rateCross')


@dataclass
class CurrencyList(BaseModel):
    list: List[Currency]


# Personal
@dataclass
class Account(BaseModel):
    id: str
    send_id: str = Field(alias="sendId")
    balance: int
    credit_limit: int = Field(alias="creditLimit")
    type: AccountType
    currency_code: CurrencyCode = Field(alias="currencyCode")
    masked_pan: List[str] = Field(alias="maskedPan")
    iban: str
    cashback_type: Optional[CashbackType] = Field(default=None, alias="cashbackType")


@dataclass
class Jar(BaseModel):
    id: str
    send_id: str = Field(alias="sendId")
    title: str
    description: str
    currency_code: CurrencyCode = Field(alias="currencyCode")
    balance: int
    goal: int


@dataclass
class Transaction(BaseModel):
    id: str
    time: int
    description: str
    mcc: int
    original_mcc: int = Field(alias="originMcc")
    hold: bool
    amount: int
    operation_amount: int = Field(alias="operationAmount")
    currency_code: CurrencyCode = Field(alias="currencyCode")
    commission_rate: int = Field(alias="commissionRate")
    cashback_amount: int = Field(alias="cashbackAmount")
    balance: int
    comment: Optional[str] = None
    receipt_id: Optional[str] = Field(default=None, alias="receiptId")
    invoice_id: Optional[str] = Field(default=None, alias="invoiceId")
    counter_edrpou: Optional[str] = Field(default=None, alias="counterEdrpou")
    counter_iban: Optional[str] = Field(default=None, alias="counterIban")
    counter_name: Optional[str] = Field(default=None, alias="counterName")


class ClientInfo(BaseModel):
    client_id: str = Field(alias="clientId")
    name: str
    web_hook_url: str = Field(alias="webHookUrl")
    permissions: str
    accounts: List[Account]
    jars: List[Jar]


class Statement(BaseModel):
    list: List[Transaction]


# Mono Acquiring API

# Qr
class QrListItem(BaseModel):
    short_qr_id: str = Field(alias="shortQrId")
    qr_id: str = Field(alias="qrId")
    amount_type: AmountType = Field(alias="amountType")
    page_url: str = Field(alias="pageUrl")


class QrList(BaseModel):
    list: List[QrListItem]


class QrDetails(BaseModel):
    short_qr_id: str = Field(alias="shortQrId")
    invoice_id: Optional[str] = Field(default=None, alias="invoiceId")
    amount: Optional[int] = Field(default=None)
    ccy: Optional[int] = Field(default=None)


# Invoice
class InvoiceCanceled(BaseModel):
    status: str
    created_date: str = Field(alias="createdDate")
    modified_date: str = Field(alias="modifiedDate")


class InvoiceInfo(BaseModel):
    masked_pan: str
    approval_code: str
    rrn: str
    amount: int
    ccy: CurrencyCode
    final_amount: int
    terminal: str
    payment_scheme: PaymentScheme
    payment_method: PaymentMethod
    domestic_card: bool
    country: str
    # created_date = Optional[str] = None
    fee: Optional[int] = None
    cancel_list: Optional[CanceledItem] = None


@dataclass
class FinalizeInvoice:
    status: str


@dataclass
class CancelListItem(BaseModel):
    amount: int
    ccy: CurrencyCode
    date: str
    masked_pan: str = Field(default=None, alias="maskedPan")
    approval_code: Optional[str] = Field(default=None, alias="approvalCode")
    rrn: Optional[str] = Field(default=None)


# Wallet
@dataclass
class WalletItem(BaseModel):
    card_token: str = Field(alias="cardToken")
    masked_pan: str = Field(alias="maskedPan")
    country: Optional[str] = Field(default=None)


@dataclass
class WalletCards(BaseModel):
    wallets: List[WalletItem]
