from .base import ClientObject
from pydantic import Field

from ..enums import TokenizedCardStatus


class WalletData(ClientObject):

    card_token: str = Field(alias="cardToken")
    wallet_id: str = Field(alias="walletId")
    status: TokenizedCardStatus

    def __init__(
            self,
            card_token: str,
            wallet_id: str,
            status: TokenizedCardStatus
    ):
        super().__init__(
            cardToken=card_token,
            walletId=wallet_id,
            status=status
        )
