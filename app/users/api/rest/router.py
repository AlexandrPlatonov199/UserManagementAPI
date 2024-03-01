import fastapi

from . import users

router = fastapi.APIRouter()

"""Router for the API.

This router includes the `users` router, which defines the API endpoints for managing users. The `users` router is
included with the prefix `/users`, so all of its endpoints will be available at `/users/*`. The `tags` parameter is
used to specify the tags for the included router, which can be used to group related endpoints together.
"""

router.include_router(users.router, prefix="/users", tags=["Users"])

