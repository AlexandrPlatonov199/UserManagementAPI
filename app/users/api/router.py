import fastapi

from . import rest

router = fastapi.APIRouter()

"""Router for the API.

This router includes the `rest` router, which defines the RESTful API endpoints for the application. The `rest` router
is included with the prefix `/rest`, so all of its endpoints will be available at `/rest/*`.
"""

router.include_router(rest.router, prefix="/rest")
