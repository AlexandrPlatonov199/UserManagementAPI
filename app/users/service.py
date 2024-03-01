from facet import ServiceMixin

from . import api, database
from .settings import Settings


class Service(ServiceMixin):
    """Service class for the application.

    This class is used to manage the dependencies required by the application, including the API and database services.

    Attributes:
        _api (api.Service): The API service.
    """
    def __init__(self, api: api.Service):
        """Initialize the service.

        Args:
            api (api.Service): The API service.
        """
        self._api = api

    @property
    def dependencies(self) -> list[ServiceMixin]:
        """List of service dependencies.

        Returns:
            A list of service dependencies.
        """
        return [
            self._api,
        ]

    @property
    def api(self) -> api.Service:
        """The API service.

        Returns:
            The API service.
        """
        return self._api


def get_service(settings: Settings) -> Service:
    """Create and configure the service for the application.

    This function creates and configures the database and API services, and returns an instance of the `Service` class
    that is configured with the API service.

    Args:
        settings (Settings): The settings for the application.

    Returns:
        An instance of the `Service` class, configured with the API service.
    """
    database_service = database.get_service(settings=settings.database)
    api_service = api.get_service(
        database=database_service,
        settings=settings.api,
    )
    return Service(api=api_service)
