__all__ = [
    'EmptyResponse',

    # Monobank Open API Responses
    'CurrencyRatesResponse',
    'ClientInfoResponse',
    'StatementResponse',

    # Monobank Corp Open API Responses

    # MonoPay API Responses
    'InvoiceCreatedResponse',
    'InvoiceCanceledResponse',
    'InvoiceStatusResponse',
    'InvoiceInfoResponse',
    'SplitInvoiceResponse',
    'FinalizeInvoiceResponse',
    'QrListResponse',
    'QrDetailsResponse',
    'MerchantDetailsResponse',
    'MerchantStatementResponse',
    'MerchantPubKeyResponse',
    'WalletCardsResponse'
]


from typing import List, Optional
from dataclasses import dataclass

# Monobank Open API Instances
from mbnk.instances import CurrencyListItem
from mbnk.instances import Account
from mbnk.instances import Jar
from mbnk.instances import Transaction

# MonoPay API Instances
from mbnk.instances import QrListItem
from mbnk.instances import MerchantStatementItem
from mbnk.instances import WalletItem


@dataclass
class EmptyResponse:
    pass


# Monobank API Responses
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


# MonoPay API Responses
@dataclass
class InvoiceCreatedResponse:
    invoice_id: str
    page_url: str


@dataclass
class InvoiceCanceledResponse:
    status: str
    created_date: str
    modified_date: str


@dataclass
class SplitInvoiceResponse:
    reference: str


@dataclass
class InvoiceStatusResponse:
    pass


@dataclass
class InvoiceInfoResponse:
    pass


@dataclass
class FinalizeInvoiceResponse:
    status: str


@dataclass
class QrListResponse:
    list: List[QrListItem]


@dataclass
class QrDetailsResponse:
    short_qr_id: str
    invoice_id: Optional[str]
    amount: Optional[int]
    ccy: Optional[int]


@dataclass
class MerchantDetailsResponse:
    merchant_id: str
    merchant_name: str


@dataclass
class MerchantStatementResponse:
    list: List[MerchantStatementItem]


@dataclass
class MerchantPubKeyResponse:
    key: str


@dataclass
class WalletCardsResponse:
    wallets: List[WalletItem]
