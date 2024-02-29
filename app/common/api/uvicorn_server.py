import uvicorn


class UvicornServer(uvicorn.Server):
    """
    A customized version of the Uvicorn server that disables signal handlers.

    Methods:
        install_signal_handlers: Overrides the Uvicorn Server's `install_signal_handlers` method to do nothing.
    """
    def install_signal_handlers(self):
        """
        Overrides the Uvicorn Server's `install_signal_handlers` method to do nothing.
        """
        pass