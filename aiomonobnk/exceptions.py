class ClientError(Exception):
    """
    Base exception for all TGJar api client errors
    """


class ClientBadRequestError(ClientError):
    """
    BadRequest one or more parameters is invalid
    """


class ClientNotFoundError(ClientError):
    """
    Entity not found
    """


class ClientForbiddenError(ClientError):
    """
    ForbiddenError when method don't allowed for you
    """


class ClientUnauthorizedError(ClientError):
    """
    Authorization token is invalid
    """
