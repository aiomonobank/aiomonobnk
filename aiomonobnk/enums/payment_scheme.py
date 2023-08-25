from enum import StrEnum


class PaymentScheme(StrEnum):
    FULL = "full"
    BNPL_PARTS_4 = "bnpl_parts_4"
    BNPL_LATER_30 = "bnpl_later_30"
