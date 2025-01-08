from flask import Flask, render_template, request
from flask_session import Session
from pipeline_logic import get_pipeline
from functions import generate_env_file, retrieve_config_details, tool_definition
import json




app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)


@app.route("/",  methods=['GET', 'POST'])
def index():
  return render_template('index.html')


@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
  
    data_type = request.form.get("data_type")
    end_goal = request.form.get("end_goal")
    nature= request.form.get("nature")
    transformation_needed = request.form.get("transformation")

    pipeline = get_pipeline(
    data_type = data_type,
    end_goal=end_goal,
    nature=nature,
    transformation=transformation_needed
    )
    
    return render_template('submit_form.html', pipeline=pipeline)



with open("config.json", "r") as f:
    tools_config = json.load(f)

@app.route('/config', methods=['POST', 'GET'])
def config():
    
    ingestion_tool = request.form.get('ingestion_tool')  
    storage_tool = request.form.get('storage_tool')
    processing_tool = request.form.get('processing_tool')
    intermediate_storage_tool = request.form.get('intermediate_storage_tool')
    visualization_tool = request.form.get('visualization_tool')
    structured_tool = request.form.get('structured_tool')
    semi_structured_tool = request.form.get('semi_structured_tool')

    pipeline_dict = {
        "Ingestion": ingestion_tool,
        "Storage": storage_tool,
        "Processing": processing_tool,
        "Intermediate Storage": intermediate_storage_tool,
        "Visualization": visualization_tool,
        "Structured Storage Tool" : structured_tool,
        "Semi Structured Storage Tool" : semi_structured_tool,

    }

    shortlisted_tools = tool_definition(pipeline_dict, tools_config)
    return render_template('config.html', pipeline_dict=pipeline_dict, tools=shortlisted_tools)



@app.route('/deploy', methods = ['GET', 'POST'])
def deploy():
 
  with open('config.json', 'r') as f:
        docker_config = json.load(f)
        
  form_data = request.form
  
  updated_config = retrieve_config_details(form_data=form_data, docker_config=docker_config)
    
  generate_env_file(updated_config, output_file=".env")

    
  return updated_config

if __name__ == '__main__':
  app.run(debug=True)