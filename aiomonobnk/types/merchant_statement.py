from .base import ClientObject
from ..types.merchant_statement_item import MerchantStatementItem


class MerchantStatement(ClientObject):

    list: list[MerchantStatementItem]
