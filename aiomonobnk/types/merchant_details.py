from .base import ClientObject
from pydantic import Field


class MerchantDetails(ClientObject):

    merchant_id: str = Field(alias='merchantId')
    merchant_name: str = Field(alias='merchantName')
    edrpou: str
