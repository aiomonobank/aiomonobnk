from .base import ClientObject


class Product(ClientObject):
    name: str
    qty: float
    sum: int
    icon: str | None = None
    unit: str | None = None
    code: str | None = None
    barcode: str | None = None
    header: str | None = None
    footer: str | None = None
    tax: list[int] | None = None
    uktzed: str | None = None
