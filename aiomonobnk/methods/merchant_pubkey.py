from .base import (
    ClientMethod,
    RequestMethod
)

from ..types import MerchantPubKey


class MerchantPubKeyMethod(ClientMethod):

    __request_method__ = RequestMethod.GET
    __request_path__ = '/api/merchant/pubkey'
    __returning__ = MerchantPubKey
