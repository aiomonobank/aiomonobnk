__all__ = [
    # Monobank API Instances
    'CurrencyListItem',
    'Account',
    'Jar',
    'Transaction',
    # MonoPay API Instances
    'QrListItem',
    'WalletItem',
    'CancelListItem',
    'MerchantStatementItem'
]


from typing import List, Optional
from dataclasses import dataclass


# Monobank API Instances
@dataclass
class CurrencyListItem:
    currency_code_a: int
    currency_code_b: int
    date: int
    rate_sell: float
    rate_buy: float
    rate_cross: float


@dataclass
class Account:
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
class Jar:
    id: str
    send_id: str
    title: str
    description: str
    currency_code: int
    balance: int
    goal: int


@dataclass
class Transaction:
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


# MonoPay API Instances


@dataclass
class QrListItem:
    short_qr_id: str
    qr_id: str
    amount_type: str
    page_url: str


@dataclass
class CanceledItem:
    pass


@dataclass
class CancelListItem:
    amount: int
    ccy: int
    date: str
    masked_pan: str
    approval_code: Optional[str] = None
    rrn: Optional[str] = None


@dataclass
class MerchantStatementItem:
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
class WalletItem:
    card_token: str
    masked_pan: str
    country: Optional[str] = None

