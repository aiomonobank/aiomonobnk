from .base import ClientObject


class CardData(ClientObject):

    pan: str
    """card number"""

    exp: str
    """card expiration in format mmyy"""

    cvv: str
