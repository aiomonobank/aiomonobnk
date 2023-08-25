from typing import TYPE_CHECKING, Any, Optional

from pydantic import BaseModel, PrivateAttr
from typing_extensions import Self

if TYPE_CHECKING:
    from .client import Client


class ClientContextController(BaseModel):
    _client: Optional['Client'] = PrivateAttr()

    def model_post_init(self, __context: Any) -> None:
        self._client = __context.get("client") if __context else None

    def as_(self, client: Optional['Client']) -> Self:
        """
        Bind object to a client instance.

        :param client: Client instance
        :return: self
        """
        self._client = client
        return self

    @property
    def client(self) -> Optional['Client']:
        """
        Get client instance.

        :return: Client instance
        """
        return self._client
