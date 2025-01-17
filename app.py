from flask import Flask, session
from flask_session import Session
from controllers.supervisor_agent import SupervisorAgent
from backend.docker_agent import DockerAgent
from backend.tool_config_agent import ToolConfigAgent
from backend.pipeline_agent import PipelineAgent
from backend.chat_bot_agent import ChatBotAgent


class MyFlaskApp(Flask):
    """
    Extends the Flask application to include global references to Agents and 
    register routes through controller classes.

    Attributes:
        docker_agent (DockerAgent): Manages Docker-related operations like running and stopping containers.
        tool_config_agent (ToolConfigAgent): Handles tool definitions and configuration management.
        pipeline_agent (PipelineAgent): Manages pipeline selection and configuration.
        chat_bot (ChatBotAgent): Handles chatbot inference for user interaction.
        main_controller (SupervisorAgent): The primary controller that registers application routes.
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

        # Instantiate Agents
        self.docker_agent = DockerAgent()
        self.tool_config_agent = ToolConfigAgent(self.docker_agent)
        self.pipeline_agent = PipelineAgent()
        self.chat_bot = ChatBotAgent()

        # Setup the session
        Session(self)

        # Instantiate Controller(s) and register routes
        self.main_controller = SupervisorAgent(self)
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
