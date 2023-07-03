# __all__ = [
#     'MonobankAPIException',
#     'MonoPayAPIException'
# ]

from dataclasses import dataclass


class MonobankOpenAPIException(Exception):
    error_description: str = ""


class TooManyRequestsException(MonobankOpenAPIException):
    error_description: str = "MonobankException: Too many requests"


@dataclass
class MonobankAPIException:
    err_description: str = None


@dataclass
class MonoPayAPIException:
    err_code: str = None
    err_text: str = None
    error_description: str = None


class MonobankBadRequest(MonobankOpenAPIException):
    pass
