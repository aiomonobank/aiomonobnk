from dataclasses import dataclass


@dataclass
class MonobankBaseException:
    err_description: str
