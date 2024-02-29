from pydantic import AnyHttpUrl, BaseModel, conint


class BaseAPISettings(BaseModel):
    """Base model for API settings.

    This class is used to represent the basic settings required for an API, such as the port number.

    Attributes:
        port (conint): The port number to use for the API. This should be an integer between 1 and 65535, inclusive.
    """
    port: conint(ge=1, le=65535) = 8000