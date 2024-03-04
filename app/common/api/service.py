import fastapi
import uvicorn
from facet import ServiceMixin
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from .uvicorn_server import UvicornServer


class BaseAPIService(ServiceMixin):
    """
    A base class for creating API services.

    Attributes:
        _title (str): The title of the API.
        _version (str): The version of the API.
        _port (int): The port number to use for the API server.

    Methods:
        get_app: Returns a FastAPI application instance.
        setup_app: Overrides the default setup of the FastAPI application.
        start: Starts the API service.
        stop: Stops the API service.
    """
    def __init__(
        self,
        title: str,
        version: str,
        port: int = 8000,
    ):
        """
        Initializes the API service with the given parameters.

        Args:
            title (str): The title of the API.
            version (str): The version of the API.
            port (int, optional): The port number to use for the API server. Defaults to 8000.
        """
        self._title = title
        self._version = version
        self._port = port

    def get_app(self) -> fastapi.FastAPI:
        """
        Returns a FastAPI application instance.

        Returns:
            fastapi.FastAPI: A FastAPI application instance.
        """

        app = fastapi.FastAPI(title=self._title, version=self._version)
        app.add_middleware(
            CORSMiddleware,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        app.service = self
        self.setup_app(app=app)

        return app

    def setup_app(self, app: fastapi.FastAPI):
        """
        Overrides the default setup of the FastAPI application.

        Args:
            app (fastapi.FastAPI): The FastAPI application instance.
        """
        pass

    async def start(self):
        """
        Starts the API service.
        """
        config = uvicorn.Config(app=self.get_app(), host="0.0.0.0", port=self._port)
        server = UvicornServer(config)

        logger.info("Start API service {name}", name=self._title)
        self.add_task(server.serve())

    async def stop(self):
        """
        Stops the API service.
        """
        logger.info("Stop API service {name}", name=self._title)
