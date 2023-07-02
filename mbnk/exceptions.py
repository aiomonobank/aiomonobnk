__all__ = [
    'MonobankAPIException',
    'MonoPayAPIException'
]

from dataclasses import dataclass


@dataclass
class MonobankAPIException:
    err_description: str = None


@dataclass
class MonoPayAPIException:
    err_code: str = None
    err_text: str = None
    error_description: str = None
