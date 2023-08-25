from enum import StrEnum


class AmountType(StrEnum):
    MERCHANT = "merchant"
    CLIENT = "client"
    FIX = "fix"
