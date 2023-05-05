from typing import List, Optional
from dataclasses import dataclass


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
    cashback_type: Optional[str]
    masked_pan: List[str]
    iban: str


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
    comment: Optional[str]
    receipt_id: Optional[str]
    invoice_id: Optional[str]
    counter_edrpou: Optional[str]
    counter_iban: Optional[str]
    counter_name: Optional[str]
