# controllers/main_controller.py

import json
import threading
import subprocess
from flask import request, render_template, redirect, url_for, session, jsonify
from backend.chat_bot_manager import SYSTEM_PROMPT


class MainController:
    """
    A controller class to organize Flask routes. 
    Holds references to the parent Flask app's managers.
    """

    def __init__(self, app):
        self.app = app
        # We can load tools_config once here, or inside a route
        with open("config.json", "r", encoding="utf-8") as f:
            self.tools_config = json.load(f)

    def register_routes(self):
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

    # --------------------
    # ROUTE HANDLERS
    # --------------------
    def index(self):
        return render_template("index.html")

    def submit_form(self):
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

    def config_route(self):
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

    def deploy(self):
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

    def loading(self):
        services = session.get("ports", {})
        # The original check_containers_health() might return a (bool, list)
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

    def ollama_chat(self):
        request_data = request.get_json(force=True)
        user_prompt = request_data["prompt"]
        try:
            content = self.app.chat_inference_manager.infer(SYSTEM_PROMPT, user_prompt)
            return jsonify({"content": content}), 200
        except Exception as exc:
            return jsonify({"error": str(exc)}), 500

    def create_pipeline(self):
        try:
            session.clear()
            self.app.docker_manager.down_docker_compose()
            return redirect(url_for("index"))
        except subprocess.CalledProcessError as exc:
            return f"Error occurred: {exc}", 500

    def final(self):
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
