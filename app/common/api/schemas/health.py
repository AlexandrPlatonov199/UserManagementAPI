from pydantic import BaseModel


class HealthResponse(BaseModel):
    """
    A model for the response of the health check endpoint.

    Attributes:
        version (str): The version of the application.
        name (str): The name of the application.
    """
    version: str
    name: str
