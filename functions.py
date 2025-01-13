import subprocess
from main2 import merge_docker_compose
import requests
import json

def tool_definition(pipeline_dict, tools_config):
    selected_tools = {key: value for key, value in pipeline_dict.items() if value}
    shortlisted_tools = {}
    for type_object, tool in selected_tools.items():
        if isinstance(tool, list):
            pass
        else:
            tool = tool.replace(' ', '')
            shortlisted_tools.update({tool : tools_config[tool]})
    
    return shortlisted_tools


def generate_env_file(config, output_file=".env"):
    with open(output_file, "w") as file:
        for service, details in config.items():
            if "EnvironmentVariables" in details:
                file.write(f"# {service} Environment Variables\n")
                for key, value in details["EnvironmentVariables"].items():
                    file.write(f"{key}={value}\n")
                file.write("\n")
                

def retrieve_config_details(form_data, docker_config ):
    tool_names = [tool_name for tool_name in form_data.getlist('tool_names')]
    updated_config = {}
    for tool_name in tool_names:
        if tool_name in docker_config:
            tool_config = docker_config[tool_name]
            updated_env_vars = {}

            for var_name, default_value in tool_config["EnvironmentVariables"].items():
                
                input_value = form_data.get(f"{tool_name}['EnvironmentVariables']'[{var_name}]")
                
                if input_value != None:
                    updated_env_vars[var_name] = input_value
                else:
                    updated_env_vars[var_name] = default_value
                    
                if not updated_env_vars:
                    updated_config[tool_name] = {
                        "EnvironmentVariables": "No config required"
                    }
               
                updated_config[tool_name] = {
                "EnvironmentVariables": updated_env_vars
            }
            ports = merge_docker_compose(tool_names)
            print(f'These are the ports - -------------------------------------------------------------------------{ports}')
    return updated_config, ports

def refine_access_links(ports):
    services_w_ports  = ['airflow-webserver', \
        'jobmanager', 'conduktor-console', 'spark-master', \
        'superset', 'namenode', 'mongo-express', 'phpmyadmin',\
        'neo4j', 'nifi', 'pgadmin', 'prefect-orion']
    extracted_services = {}
    for service in services_w_ports:
        if service in ports.keys():
            if service == 'nifi':
                extracted_services[service] = ports[service][1].split(':')[0]
            else:
                extracted_services[service] = ports[service][0].split(':')[0]  # Take the first value in the list
    
        
    return extracted_services
    

def run_docker_compose():
    try:
        command = "docker compose up --build"
        password = "CureMD786"
        result = subprocess.run(f"echo {password} | sudo {command}", shell=True, check=True)     
    
        if result.stderr:
            print("Error:\n", result.stderr)
        
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
        print("Error Output:", e.stderr)



def extract_signin_configs(services_dict, env_file_path='.env'):
    env_params_dict = {
        'airflow-db': ['POSTGRES_USER', 'POSTGRES_PASSWORD'],
        'superset-metadata-db': ['POSTGRES_USER_SUPERSET', 'POSTGRES_PASSWORD_SUPERSET'],
        'superset': ['USERNAME', 'PASSWORD'],
        'mongo': ['MONGO_INITDB_ROOT_USERNAME', 'MONGO_INITDB_ROOT_PASSWORD'],
        'mongo-express': ['ME_CONFIG_BASICAUTH_USERNAME', 'ME_CONFIG_BASICAUTH_PASSWORD'],
        'mysql': ['MYSQL_USER', 'MYSQL_PASSWORD'],
        'phpmyadmin': ['PMA_USER', 'PMA_PASSWORD'],
        'neo4j': ['NEO4J_AUTH'],
        'postgres': ['POSTGRES_USER_PG', 'POSTGRES_PASSWORD_PG'],
        'pgadmin': ['PGADMIN_DEFAULT_EMAIL', 'PGADMIN_DEFAULT_PASSWORD']
    }

    signin_configs = {}

    env_dict = {}
    with open(env_file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            key, value = line.split('=', 1)
            env_dict[key.strip()] = value.strip()

    for service, config_needed in services_dict.items():
        if service in env_params_dict:
            service_configs = {}
            for param in env_params_dict[service]:
                if param in env_dict:
                    service_configs[param] = env_dict[param]
                else:
                    service_configs[param] = None 
            signin_configs[service] = service_configs

    return signin_configs


def infer(system, prompt):
    data = {
        "model": "qwen2.5:32b-instruct-q8_0",
        "messages": [
            {
                "role": "system",
                "content": system
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "stream": False,
        "options": {
            "temperature": 0.1 # change it as per requirement
        }
    }
 
    headers = {
        "Content-Type": "application/json"
    }
    ollama_url = "http://172.16.101.171:11400/api/chat/"
    # ollama_url = "http://172.16.19.80:11567/api/chat/"
    model_response = requests.post(
        url=ollama_url,
        json=data,
        headers=headers
    ).json()
 
    return model_response['message']['content']


def check_containers_health():
    """
    Checks the health status of all running Docker containers using subprocess.
    Returns:
        - "no_containers" if no containers are running.
        - True, if all running containers are healthy.
        - A list of healthy container names, if not all containers are healthy.
          This list can be empty if none are healthy.
    """
 
    # 1. List all running containers (IDs)
    ps_cmd = ["sudo", "docker", "ps", "-q"]
    try:
        result = subprocess.run(ps_cmd, capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError as e:
        print("Error running docker ps:", e.stderr)
        return []
 
    container_ids = result.stdout.strip().split()
    if not container_ids:
        return []
 
    healthy_containers = []
    for container_id in container_ids:
        inspect_cmd = ["sudo", "docker", "inspect", container_id]
        try:
            inspect_result = subprocess.run(inspect_cmd, capture_output=True, text=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error inspecting container {container_id}:", e.stderr)
            continue  # skip this container
 
        try:
            # Parse the JSON output of 'docker inspect'
            data = json.loads(inspect_result.stdout)
            # Usually 'docker inspect' returns a list of container data, so take the first item
            container_info = data[0] if data else {}
            # Container name and health status
            container_name = container_info.get("Name", "").lstrip("/")
            state = container_info.get("State", {})
            health = state.get("Health", {})
            health_status = health.get("Status")
            # If health_status is "healthy", record the container name
            if health_status == "healthy":
                healthy_containers.append(container_name)
        except (json.JSONDecodeError, IndexError, KeyError) as e:
            print(f"Error parsing JSON for container {container_id}:", e)
            continue
 
    # 3. Compare the number of healthy containers to the total
    if len(healthy_containers) == len(container_ids):
        return True
    else:
        return healthy_containers
 
if __name__ == "__main__":
    result = check_containers_health()
    if result == []:
        print("No containers are running.")
    elif result is True:
        print("All running containers are healthy.")
    else:
        # result is a list of healthy containers
        if result:
            print("Some containers are not healthy.")
            print("Healthy containers:", result)
        else:
            print("No healthy containers found.")

if __name__ == '__main__':
    pass
            
