from enum import StrEnum


class RegistrationStatus(StrEnum):
    NEW = "New"
    DECLINED = "Declined"
    APPROVED = "Approved"
