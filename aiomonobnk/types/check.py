from .base import ClientObject
from pydantic import Field

from ..enums import (
    CheckType,
    CheckStatus,
    FiscalizationSource
)


class Check(ClientObject):

    id: str
    type: CheckType
    status: CheckStatus
    status_description: str | None = Field(alias='statusDescription', default=None)
    tax_url: str | None = Field(alias='taxUrl', default=None)
    file: str | None = None
    fiscalization_source: FiscalizationSource = Field(alias='fiscalizationSource')

