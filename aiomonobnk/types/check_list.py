from .base import ClientObject
from .check import Check


class CheckList(ClientObject):

    checks: list[Check]
