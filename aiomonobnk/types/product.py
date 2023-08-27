from .base import ClientObject


class Product(ClientObject):

    name: str
    qty: float
    sum: int
    code: str
    icon: str | None = None
    unit: str | None = None
    barcode: str | None = None
    header: str | None = None
    footer: str | None = None
    tax: list[int] | None = None
    uktzed: str | None = None

    def __init__(
            self,
            name: str,
            qty: float,
            sum: int,
            code: str,
            icon: str | None = None,
            unit: str | None = None,
            barcode: str | None = None,
            header: str | None = None,
            footer: str | None = None,
            tax: list[int] | None = None,
            uktzed: str | None = None
    ):
        super().__init__(
            name=name,
            qty=qty,
            sum=sum,
            code=code,
            icon=icon,
            unit=unit,
            barcode=barcode,
            header=header,
            footer=footer,
            tax=tax,
            uktzed=uktzed
        )
