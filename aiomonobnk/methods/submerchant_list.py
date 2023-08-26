from .base import (
    ClientMethod,
    RequestMethod
)
from ..types import SubmerchantList


class SubmerchantListMethod(ClientMethod):

    __request_method__ = RequestMethod.GET
    __request_path__ = '/api/merchant/submerchant/list'
    __returning__ = SubmerchantList
