from .base import ClientObject
from pydantic import Field


class SaveCardData(ClientObject):

    save_card: bool = Field(alias="saveCard")
    wallet_id: str | None = Field(alias="walletId", default=None)

    def __init__(
            self,
            save_card: bool,
            wallet_id: str | None = None
    ):
        super().__init__(
            saveCard=save_card,
            walletId=wallet_id
        )
