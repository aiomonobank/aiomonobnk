from .base import ClientObject
from pydantic import Field

from ..types.product import Product


class MerchantPaymInfo(ClientObject):

    reference: str | None = None

    destination: str | None = Field(max_length=280, default=None)
    """Payment destination"""

    comment: str | None = Field(max_length=280, default=None)
    """service info field"""

    basket_order: list[Product] | None = Field(alias='basketOrder', default=None)
    """list of products"""

    def __init__(
            self,
            reference: str | None = None,
            destination: str | None = None,
            comment: str | None = None,
            basket_order: list[Product] | None = None
    ):
        super().__init__(
            reference=reference,
            destination=destination,
            comment=comment,
            basketOrder=basket_order
        )
