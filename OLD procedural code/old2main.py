# main.py
"""
Main Flask application for pipeline deployment and management.
"""
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import threading
import subprocess
import json
from flask_session import Session

# Adjust these import paths as needed to match your project structure:
from backend.docker_manager import DockerManager
from backend.tool_config_manager import ToolConfigManager
from backend.pipeline_manager import PipelineManager
from backend.chat_bot_manager import ChatInferenceManager, SYSTEM_PROMPT


app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Instantiate OOP managers
docker_manager = DockerManager()
tool_config_manager = ToolConfigManager(docker_manager)
pipeline_manager = PipelineManager()
chat_inference_manager = ChatInferenceManager()


@app.route("/", methods=['GET', 'POST'])
def index():
    """
    Renders the main landing page.
    """
    return render_template('index.html')


@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    """
    Handles submission of the data pipeline form. It retrieves user inputs like
    data_type, end_goal, and so on, then delegates pipeline logic to
    PipelineManager.get_pipeline(). The resulting pipeline is rendered on
    submit_form.html.
    """
    data_type = request.form.get("data_type")
    end_goal = request.form.get("end_goal")
    nature = request.form.get("nature")
    transformation_needed = request.form.get("transformation")

    pipeline = pipeline_manager.get_pipeline(
        data_type=data_type,
        end_goal=end_goal,
        nature=nature,
        transformation=transformation_needed
    )

    return render_template('submit_form.html', pipeline=pipeline)


# Load tools_config from config.json once (global usage).
with open("config.json", "r", encoding='utf-8') as f:
    tools_config = json.load(f)


@app.route('/config', methods=['POST', 'GET'])
def config():
    """
    Renders the config page, which displays shortlisted tools based on user
    selections (ingestion, storage, etc.). The pipeline_dict is built from
    form inputs and passed to tool_config_manager.tool_definition().
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

    shortlisted_tools = tool_config_manager.tool_definition(pipeline_dict, tools_config)

    return render_template('config.html',
                           pipeline_dict=pipeline_dict,
                           tools=shortlisted_tools)


@app.route('/deploy', methods=['GET', 'POST'])
def deploy():
    """
    Deploys the selected configuration. Reads 'config.json' for Docker settings,
    retrieves updated configuration and ports from ToolConfigManager, generates
    an .env file, and spins up Docker containers in a background thread.
    """
    with open('config.json', 'r', encoding='utf-8') as f:
        docker_config = json.load(f)

    form_data = request.form

    updated_config, ports = tool_config_manager.retrieve_config_details(
        form_data=form_data,
        docker_config=docker_config
    )

    session['form_data'] = form_data
    session['updated_config'] = updated_config
    session['ports'] = ports
    session['flag'] = 0

    tool_config_manager.generate_env_file(updated_config, output_file=".env")

    thread = threading.Thread(target=docker_manager.run_docker_compose)
    thread.start()

    return redirect(url_for('loading'))


@app.route('/loading')
def loading():
    """
    Shows a loading page while containers are starting up. Checks container
    health via DockerManager. If all containers are healthy, it increments
    a session-based counter 'flag' to allow a couple of refreshes. After 2
    successful checks, redirects to the final page; otherwise, keeps reloading.
    """
    services = session.get('ports', {})
    result, healthy_containers = docker_manager.check_containers_health()

    if result is True:
        flag = session.get('flag', 0)
        if flag == 2:
            session['flag'] = 0
            return redirect(url_for("final"))
        session['flag'] = flag + 1
        return render_template(
            "loading.html",
            services=services,
            healthy_containers=healthy_containers
        )
    else:
        return render_template(
            "loading.html",
            services=services,
            healthy_containers=healthy_containers
        )


@app.route("/ollama_chat", methods=["POST"])
def ollama_chat():
    """
    Handles POST requests for chat-based inference. Uses ChatInferenceManager
    to process user prompts and return a response from the model.
    """
    request_data = request.get_json(force=True)
    user_prompt = request_data["prompt"]
    try:
        content = chat_inference_manager.infer(SYSTEM_PROMPT, user_prompt)
        return jsonify({"content": content}), 200
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500


@app.route('/create_pipeline', methods=['POST'])
def create_pipeline():
    """
    Clears the session and stops Docker containers (down). Then redirects to
    the index page. Used for resetting or starting a new pipeline selection.
    """
    try:
        session.clear()
        docker_manager.down_docker_compose()
        return redirect(url_for('index'))
    except subprocess.CalledProcessError as exc:
        return f"Error occurred: {exc}", 500


@app.route('/final')
def final():
    """
    Final page, showing the container ports, sign-in configs, and access links.
    If sign-in configs or ports do not exist, displays an error page.
    """
    ports = session.get('ports', None)
    signin_conf = tool_config_manager.extract_signin_configs(ports)

    if not ports or not signin_conf:
        return render_template('deploy_error.html')

    if 'nifi' in ports.keys():
        # Example special-case logic
        signin_conf.update({'nifi': ['admin', 'ctsBtRBKHRAx69EqUghvvgEvjnaLjFEB']})

    links = tool_config_manager.refine_access_links(ports=ports)

    return render_template('present.html',
                           ports=ports,
                           signin_conf=signin_conf,
                           links=links)


if __name__ == '__main__':
    app.run(debug=True)
