from enum import StrEnum


class PaymentMethod(StrEnum):
    PAN = "pan"
    APPLE = "apple"
    GOOGLE = "google"
    MONOBANK = "monobank"
