import json
import threading
import subprocess
from typing import Dict, Tuple, Union
from flask import Flask, request, render_template, redirect, url_for, session, jsonify


class SupervisorAgent:
    """
    A supervisor agent to organize Flask routes. 
    Holds references to the parent Flask app's agents and config data.
    """

    def __init__(self, app: Flask) -> None:
        """
        Initializes the SupervisorAgent with a Flask app instance.

        Args:
            app (Flask): The parent Flask app instance, which holds references to the agents.
        """
        self.app = app
        # Load the tools configuration from a JSON file
        with open("config.json", "r", encoding="utf-8") as f:
            self.tools_config: Dict[str, Dict] = json.load(f)

    def register_routes(self) -> None:
        """
        Registers all routes to the Flask app instance.
        """
        self.app.add_url_rule("/", view_func=self.index, methods=["GET", "POST"])
        self.app.add_url_rule("/submit_form", view_func=self.submit_form, methods=["POST", "GET"])
        self.app.add_url_rule("/config", view_func=self.config_route, methods=["POST", "GET"])
        self.app.add_url_rule("/deploy", view_func=self.deploy, methods=["GET", "POST"])
        self.app.add_url_rule("/loading", view_func=self.loading, methods=["GET"])
        self.app.add_url_rule("/ollama_chat", view_func=self.ollama_chat, methods=["POST"])
        self.app.add_url_rule("/create_pipeline", view_func=self.create_pipeline, methods=["POST"])
        self.app.add_url_rule("/final", view_func=self.final, methods=["GET"])

    # ROUTE HANDLERS
    def index(self) -> str:
        """
        Renders the index page.

        Returns:
            str: Rendered HTML for the index page.
        """
        return render_template("index.html")

    def submit_form(self) -> str:
        """
        Handles form submission for pipeline configuration.

        Returns:
            str: Rendered HTML displaying the selected pipeline configuration.
        """
        data_type = request.form.get("data_type")
        end_goal = request.form.get("end_goal")
        nature = request.form.get("nature")
        transformation_needed = request.form.get("transformation")

        pipeline = self.app.pipeline_agent.get_pipeline(
            data_type=data_type,
            end_goal=end_goal,
            nature=nature,
            transformation=transformation_needed
        )
        return render_template("submit_form.html", pipeline=pipeline)

    def config_route(self) -> str:
        """
        Handles tool configuration selection based on the pipeline.

        Returns:
            str: Rendered HTML with the pipeline tools configuration.
        """
        ingestion_tool = request.form.get('ingestion_tool')
        storage_tool = request.form.get('storage_tool')
        processing_tool = request.form.get('processing_tool')
        intermediate_storage_tool = request.form.get('intermediate_storage_tool')
        visualization_tool = request.form.get('visualization_tool')
        structured_tool = request.form.get('structured_tool')
        semi_structured_tool = request.form.get('semi_structured_tool')
        orchestration_tool = request.form.get('orchestration_tool')

        pipeline_dict = {
            "Ingestion": ingestion_tool,
            "Storage": storage_tool,
            "Processing": processing_tool,
            "Intermediate Storage": intermediate_storage_tool,
            "Visualization": visualization_tool,
            "Structured Storage Tool": structured_tool,
            "Semi Structured Storage Tool": semi_structured_tool,
            "Orchestration Tool": orchestration_tool
        }

        tool_config_state = {
            "pipeline_dict": pipeline_dict,
            "tools_config": self.tools_config,
            "config": {},
            "tool_names": [],
            "ports": {},
            "services_dict": {},
            "env_file_path": ".env",
            "updated_config": {},
        }

        tool_config_state = self.app.tool_config_agent.invoke_tool_definition(tool_config_state)
        shortlisted_tools = tool_config_state["updated_config"]

        return render_template("config.html",
                               pipeline_dict=pipeline_dict,
                               tools=shortlisted_tools)

    def deploy(self) -> str:
        """
        Deploys the pipeline by generating environment files, merging Docker Compose configurations,
        and running the Docker Compose commands.

        Returns:
            str: Redirects to the loading page.
        """
        with open("config.json", "r", encoding="utf-8") as f:
            docker_config = json.load(f)

        form_data = request.form

        tool_config_state = {
            "pipeline_dict": {},
            "tools_config": self.tools_config,
            "config": {},
            "tool_names": form_data.getlist('tool_names'),
            "ports": {},
            "services_dict": {},
            "env_file_path": ".env",
            "updated_config": {},
        }

        tool_config_state = self.app.tool_config_agent.invoke_config_details_retrieval(tool_config_state)
        updated_config = tool_config_state["updated_config"]
        ports = tool_config_state["ports"]

        session["form_data"] = form_data
        session["updated_config"] = updated_config
        session["ports"] = ports
        session["flag"] = 0
        
        tool_config_state = self.app.tool_config_agent.invoke_env_file_generation(tool_config_state)

        # Prepare DockerState for merging Docker Compose files
        docker_state = {
            "command": "",
            "tool_names": form_data.getlist('tool_names'),
            "base_directory": "docker_templates",
            "ports": {},
            "compose_file_path": "docker-compose.yml",
            "success": False,
            "error": "",
        }
        thread = threading.Thread(target=lambda: self.app.docker_agent.invoke_up(docker_state))
        thread.start()

        return redirect(url_for("loading"))

    def loading(self) -> str:
        """
        Displays the loading page while the pipeline is being deployed.

        Returns:
            str: Rendered HTML for the loading page.
        """
        services = session.get("ports", {})
        docker_state = {
            "command": "",
            "tool_names": [],
            "base_directory": "",
            "ports": services,
            "compose_file_path": "",
            "success": False,
            "error": "",
        }

        docker_state = self.app.docker_agent.invoke_health(docker_state)
        if docker_state["success"]:
            flag = session.get("flag", 0)
            if flag == 2:
                session["flag"] = 0
                return redirect(url_for("final"))
            session["flag"] = flag + 1
            return render_template("loading.html",
                                   services=services,
                                   healthy_containers=docker_state.get("ports", []))
        return render_template("loading.html",
                               services=services,
                               healthy_containers=docker_state.get("ports", []))

    def ollama_chat(self) -> Tuple[Dict[str, Union[str, Dict]], int]:
        """
        Handles chat requests for the AI assistant.

        Returns:
            Tuple[Dict[str, Union[str, Dict]], int]: A JSON response with the assistant's reply or an error message,
            along with the HTTP status code.
        """
        request_data = request.get_json(force=True)
        user_prompt = request_data["prompt"]
        try:
            content = self.app.chat_bot.get_response(user_prompt)
            return jsonify({"content": content}), 200
        except Exception as exc:
            return jsonify({"error": str(exc)}), 500

    def create_pipeline(self) -> Union[str, Tuple[str, int]]:
        """
        Resets the pipeline by clearing the session and stopping running containers.

        Returns:
            Union[str, Tuple[str, int]]: Redirects to the index page or returns an error message.
        """
        try:
            docker_state = {
                "command": "",
                "tool_names": [],
                "base_directory": "",
                "ports": {},
                "compose_file_path": "",
                "success": False,
                "error": "",
            }

            self.app.docker_agent.invoke_down(docker_state)
            session.clear()
            return redirect(url_for("index"))
        except subprocess.CalledProcessError as exc:
            return f"Error occurred: {exc}", 500

    def final(self) -> str:
        """
        Displays the final deployment page with access links and sign-in configurations.

        Returns:
            str: Rendered HTML for the final deployment page or an error page.
        """
        ports = session.get("ports", None)

        tool_config_state = {
            "pipeline_dict": {},
            "tools_config": self.tools_config,
            "config": {},
            "tool_names": [],
            "ports": ports,
            "services_dict": ports,
            "env_file_path": ".env",
            "updated_config": {},
        }

        tool_config_state = self.app.tool_config_agent.invoke_signin_configs_extraction(tool_config_state)
        signin_conf = tool_config_state["updated_config"].get("signin_configs", {})

        if not ports or not signin_conf:
            return render_template("deploy_error.html")

        if "nifi" in ports.keys():
            signin_conf.update({"nifi": ["admin", "ctsBtRBKHRAx69EqUghvvgEvjnaLjFEB"]})

        tool_config_state = self.app.tool_config_agent.invoke_refine_access_links(tool_config_state)
        links = tool_config_state["updated_config"].get("access_links", {})

        return render_template("present.html",
                               ports=ports,
                               signin_conf=signin_conf,
                               links=links)
