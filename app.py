from flask import Flask, session
from flask_session import Session
from controllers.main_controller import MainController
from backend.docker_manager import DockerManager
from backend.tool_config_manager import ToolConfigManager
from backend.pipeline_manager import PipelineManager
from backend.chat_bot_manager import ChatBotManager


class MyFlaskApp(Flask):
    """
    Extends the Flask application to include global references to managers and 
    register routes through controller classes.

    Attributes:
        docker_manager (DockerManager): Manages Docker-related operations like running and stopping containers.
        tool_config_manager (ToolConfigManager): Handles tool definitions and configuration management.
        pipeline_manager (PipelineManager): Manages pipeline selection and configuration.
        chat_bot (ChatBotManager): Handles chatbot inference for user interaction.
        main_controller (MainController): The primary controller that registers application routes.
    """

    def __init__(self, import_name: str, **kwargs) -> None:
        """
        Initializes the Flask application, sets up session handling, and registers routes.

        Args:
            import_name (str): The name of the application module.
            **kwargs: Additional keyword arguments for Flask initialization.
        """
        super().__init__(import_name, **kwargs)
        self.secret_key = "your_secret_key"
        self.config["SESSION_TYPE"] = "filesystem"

        # Instantiate managers
        self.docker_manager = DockerManager()
        self.tool_config_manager = ToolConfigManager(self.docker_manager)
        self.pipeline_manager = PipelineManager()
        self.chat_bot = ChatBotManager()

        # Setup the session
        Session(self)

        # Instantiate Controller(s) and register routes
        self.main_controller = MainController(self)
        self.main_controller.register_routes()


def create_app() -> MyFlaskApp:
    """
    Factory function to create and configure the Flask application.

    Returns:
        MyFlaskApp: The configured Flask application instance.
    """
    app = MyFlaskApp(__name__)
    return app


if __name__ == "__main__":
    application = create_app()
    application.run(debug=True)
