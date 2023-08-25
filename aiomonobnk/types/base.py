from pydantic import BaseModel, ConfigDict
from ..client.context import ClientContextController


class ClientObject(ClientContextController, BaseModel):
    model_config = ConfigDict(
        use_enum_values=True,
        extra="allow",
        validate_assignment=True,
        frozen=True,
        populate_by_name=True,
        arbitrary_types_allowed=True
    )
