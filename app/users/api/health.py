from app.common.api.schemas.health import HealthResponse
from app.common.utils.package import get_version


def health() -> HealthResponse:
    """Check the health of the application.

    This function returns a `HealthResponse` object that indicates the version and name of the application.

    Returns:
        A `HealthResponse` object with the version and name of the application.
    """
    return HealthResponse(
        version=get_version() or "0.0.0",
        name="Users",
    )

