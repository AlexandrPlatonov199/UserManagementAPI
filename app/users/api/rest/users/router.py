import fastapi
from . import handlers

router = fastapi.APIRouter()

"""A FastAPI router for handling user-related API requests.

This router defines the following API endpoints:

* `GET /users/{user_id}`: Get a user by ID.
* `POST /users`: Create a new user.
* `DELETE /users/{user_id}`: Delete a user by ID.
* `PATCH /users/{user_id}`: Update a user by ID.
"""

router.add_api_route(path="/{user_id}", methods=["GET"], endpoint=handlers.get_user)
router.add_api_route(path="/", methods=["GET"], endpoint=handlers.get_users)
router.add_api_route(path="/count_last_seven_days/", methods=["GET"], endpoint=handlers.get_users_count_last_seven_days)
router.add_api_route(path="/top_five_longest/", methods=["GET"], endpoint=handlers.get_users_top_five_longest)
router.add_api_route(path="/email_domain_ratio/", methods=["GET"], endpoint=handlers.get_email_domain_ratio)
router.add_api_route(path="/", methods=["POST"], endpoint=handlers.create_user)
router.add_api_route(path="/{user_id}", methods=["DELETE"], endpoint=handlers.delete_user)
router.add_api_route(path="/{user_id}", methods=["PATCH"], endpoint=handlers.update_user)
