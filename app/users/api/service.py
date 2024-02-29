import fastapi
from facet import ServiceMixin

from app.common.api.service import BaseAPIService
from app.common.utils.package import get_version
from app.users import database

from . import health, router
from .settings import Settings


class Service(BaseAPIService):
    """Service class for the API.

    This class is used to manage the dependencies required by the API, including the database service. It also sets up
    the API routes and includes the `router` router.

    Attributes:
        _database (database.Service): The database service.
    """
    def __init__(
            self,
            database: database.Service,
            version: str = "0.0.0",
            port: int = 8000,
    ):
        """Initialize the service.

        Args:
            database (database.Service): The database service.
            version (str): The version of the API.
            port (int): The port number for the API.
        """
        self._database = database

        super().__init__(
            title="Users",
            version=version,
            port=port,
        )

    def setup_app(self, app: fastapi.FastAPI):
        """Set up the API routes.

        This method sets up the `/health` route, which returns the health of the API, and includes the `router` router,
        which defines the API endpoints.

        Args:
            app (fastapi.FastAPI): The FastAPI application.
        """
        app.add_api_route(path="/health", endpoint=health.health)
        app.include_router(router.router, prefix="/api")

    @property
    def dependencies(self) -> list[ServiceMixin]:
        """List of service dependencies.

        Returns:
            A list of service dependencies.
        """
        return [
            self._database,
        ]

    @property
    def database(self) -> database.Service:
        """The database service.

        Returns:
            The database service.
        """
        return self._database


def get_service(
        database: database.Service,
        settings: Settings,
) -> Service:
    """Create and configure the service for the API.

    This function creates and configures the database service, and returns an instance of the `Service` class that is
    configured with the database service and the API settings.

    Args:
        database (database.Service): The database service.
        settings (Settings): The settings for the API.

    Returns:
        An instance of the `Service` class, configured with the database service and the API settings.
    """
    return Service(
        database=database,
        version=get_version() or "0.0.0",
        port=settings.port,
    )
