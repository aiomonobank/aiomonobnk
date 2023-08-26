from .base import ClientObject
from .submerchant_data import SubmerchantData


class SubmerchantList(ClientObject):
    list: list[SubmerchantData]
