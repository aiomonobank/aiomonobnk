from enum import StrEnum


class TransactionStatus(StrEnum):
    CREATED = "created"
    PROCESSING = "processing"
    HOLD = "hold"
    SUCCESS = "success"
    FAILURE = "failure"
    REVERSER = "reversed"
    EXPIRED = "expired"
    