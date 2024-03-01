import fastapi


class HTTPNotFound(fastapi.HTTPException):
    """An HTTP exception to be raised when a resource is not found.

    This exception should be raised with a status code of `404 Not Found` and a detail message of `"Not found."`.
    """
    def __init__(self):
        super().__init__(
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
            detail="Not found.",
        )
