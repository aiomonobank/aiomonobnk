from .base import (
    ClientMethod,
    RequestMethod
)

from ..types import MerchantDetails


class MerchantDetailsMethod(ClientMethod):

    __request_method__ = RequestMethod.GET
    __request_path__ = '/api/merchant/details'
    __returning__ = MerchantDetails
