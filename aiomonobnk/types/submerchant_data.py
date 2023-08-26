from .base import ClientObject


class SubmerchantData(ClientObject):

    code: str
    edrpou: str | None = None
    iban: str
