import json
import threading
import subprocess
from typing import Dict, Tuple, Union
from flask import Flask, request, render_template, redirect, url_for, session, jsonify


class MainController:
    """
    A controller class to organize Flask routes. 
    Holds references to the parent Flask app's managers and config data.
    """

    def __init__(self, app: Flask) -> None:
        """
        Initializes the MainController with a Flask app instance.

        Args:
            app (Flask): The parent Flask app instance, which holds references to the managers.
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

        pipeline = self.app.pipeline_manager.get_pipeline(
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

        shortlisted_tools = self.app.tool_config_manager.tool_definition(
            pipeline_dict, self.tools_config
        )

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
        updated_config, ports = self.app.tool_config_manager.retrieve_config_details(
            form_data=form_data, docker_config=docker_config
        )

        session["form_data"] = form_data
        session["updated_config"] = updated_config
        session["ports"] = ports
        session["flag"] = 0

        self.app.tool_config_manager.generate_env_file(updated_config, output_file=".env")

        thread = threading.Thread(target=self.app.docker_manager.run_docker_compose)
        thread.start()

        return redirect(url_for("loading"))

    def loading(self) -> str:
        """
        Displays the loading page while the pipeline is being deployed.

        Returns:
            str: Rendered HTML for the loading page.
        """
        services = session.get("ports", {})
        result, healthy_containers = self.app.docker_manager.check_containers_health()

        if result is True:
            flag = session.get("flag", 0)
            if flag == 2:
                session["flag"] = 0
                return redirect(url_for("final"))
            session["flag"] = flag + 1
            return render_template("loading.html",
                                   services=services,
                                   healthy_containers=healthy_containers)
        return render_template("loading.html",
                               services=services,
                               healthy_containers=healthy_containers)

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
            content = self.app.chat_bot.infer(user_prompt)
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
            session.clear()
            self.app.docker_manager.down_docker_compose()
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
        signin_conf = self.app.tool_config_manager.extract_signin_configs(ports)

        if not ports or not signin_conf:
            return render_template("deploy_error.html")

        if "nifi" in ports.keys():
            signin_conf.update({"nifi": ["admin", "ctsBtRBKHRAx69EqUghvvgEvjnaLjFEB"]})

        links = self.app.tool_config_manager.refine_access_links(ports=ports)
        return render_template("present.html",
                               ports=ports,
                               signin_conf=signin_conf,
                               links=links)
