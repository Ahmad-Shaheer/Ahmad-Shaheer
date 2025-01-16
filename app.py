# app.py
from flask import Flask, session
from flask_session import Session
from controllers.main_controller import MainController
from backend.docker_manager import DockerManager
from backend.tool_config_manager import ToolConfigManager
from backend.pipeline_manager import PipelineManager
from backend.chat_inference_manager import ChatInferenceManager


class MyFlaskApp(Flask):
    """
    Extends Flask to hold global references to managers and register routes
    through a controller class (or multiple controllers).
    """

    def __init__(self, import_name: str, **kwargs):
        super().__init__(import_name, **kwargs)
        self.secret_key = "your_secret_key"
        self.config["SESSION_TYPE"] = "filesystem"
        
        # Instantiate managers
        self.docker_manager = DockerManager()
        self.tool_config_manager = ToolConfigManager(self.docker_manager)
        self.pipeline_manager = PipelineManager()
        self.chat_inference_manager = ChatInferenceManager()

        # Setup the session
        Session(self)

        # Instantiate Controller(s) and register routes
        self.main_controller = MainController(self)
        self.main_controller.register_routes()


def create_app() -> MyFlaskApp:
    """
    Factory function to create and configure the Flask application.
    """
    app = MyFlaskApp(__name__)
    return app


if __name__ == "__main__":
    application = create_app()
    application.run(debug=True)
