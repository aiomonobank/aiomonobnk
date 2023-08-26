from enum import StrEnum


class CheckStatus(StrEnum):
    NEW = "new"
    PROCESS = "process"
    DONE = "done"
    FAILED = "failed"
