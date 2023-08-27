from typing import Any


class ClientError(Exception):
    """
    Base exception for all TGJar api client errors
    """


class ClientDetailedError(ClientError):
    """
    Client detailed error with errors
    """

    def __init__(
            self,
            err_code: str | None = None,
            err_text: str | None = None
    ):
        self.err_code: str | None = err_code
        self.err_text: str | None = err_text

    def __str__(self):
        err_code: str | None = self.err_code
        err_text: str | None = self.err_text

        message: str = f"{err_code}: {err_text}"

        return message

    def __repr__(self) -> str:
        return f"{type(self).__name__}('{self}')"


class ClientBadRequestError(ClientDetailedError):
    """
    BadRequest one or more parameters is invalid
    """


class ClientNotFoundError(ClientDetailedError):
    """
    Entity not found
    """


class ClientForbiddenError(ClientDetailedError):
    """
    ForbiddenError when method don't allowed for you
    """


class ClientUnauthorizedError(ClientError):
    """
    Authorization token is invalid
    """


class ClientDecodeError(ClientError):
    """
    Exception raised when client can't decode response. (Malformed response, etc.)
    """

    def __init__(self, message: str, original: Exception, data: Any) -> None:
        self.message = message
        self.original = original
        self.data = data

    def __str__(self) -> str:
        original_type = type(self.original)
        return (
            f"{self.message}\n"
            f"Caused from error: "
            f"{original_type.__module__}.{original_type.__name__}: {self.original}\n"
            f"Content: {self.data}"
        )
