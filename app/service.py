import asyncio

from facet import ServiceMixin

from . import users
from .settings import Settings


class Service(ServiceMixin):
    """Service class for managing application dependencies.

    This class is used to manage the dependencies required by the application, such as the user service.

    Attributes:
        _users (users.Service): An instance of the user service.
    """
    def __init__(
            self,
            users: users.Service,
    ):
        """Initialize the service.

        Args:
            users (users.Service): An instance of the user service.
        """
        self._users = users

    @property
    def dependencies(self) -> list[ServiceMixin]:
        """List of service dependencies.

        Returns:
            A list of service dependencies.
        """
        return [
            self._users,
        ]

    @property
    def users(self) -> users.Service:
        """Getter for the user service.

        Returns:
            An instance of the user service.
        """
        return self._users


def get_service(loop: asyncio.AbstractEventLoop, settings: Settings) -> Service:
    """Create and configure the application service.

    This function creates an instance of the user service and returns an instance of the Service class,
    which is configured with the user service.

    Args:
        loop (asyncio.AbstractEventLoop): The event loop to use for the service.
        settings (Settings): The application settings.

    Returns:
        An instance of the Service class.
    """
    users_service = users.get_service(settings=settings.users)

    return Service(
        users=users_service,
    )
