from enum import StrEnum


class CancellationStatus(StrEnum):
    PROCESSING = "processing"
    SUCCESS = "success"
    FAILURE = "failure"
