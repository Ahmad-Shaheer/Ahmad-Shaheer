import subprocess
import time
import re
from main2 import merge_docker_compose

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
        
    return updated_config, ports



def run_docker_compose():
    try:
        command = "docker compose up -d"
        password = "CureMD786"

        result = subprocess.run(f"echo {password} | sudo {command}", shell=True, check=True)
        # result = subprocess.run(['docker compose', 'up'], capture_output=True, text=True, check=True)
     
        
        wait_for_containers()
        if result.stderr:
            print("Error:\n", result.stderr)
        
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
        print("Error Output:", e.stderr)




def get_running_containers():
    # Get the list of all running container names dynamically
    containers = subprocess.check_output("docker ps --format '{{.Names}}'", shell=True).decode('utf-8').splitlines()
    return containers

def check_containers():
    containers = get_running_containers()
    
    for container in containers:
        # Check if the container is running
        status = subprocess.check_output(f"docker inspect -f '{{{{.State.Status}}}}' {container}", shell=True).decode('utf-8').strip()
        if status != "running":
            print(f"{container} is not running. Waiting...")
            return False
    return True

def wait_for_containers():
    print("Waiting for all containers to be up and running...")
    while not check_containers():
        print("Waiting for all containers to be up and running...")
        time.sleep(2)  # Wait for 2 seconds before checking again
    print("All containers are running. Proceeding with web page display.")


def extract_signin_configs(services_dict, env_file_path='.env'):
    # Specific environment variables for each service
    env_params_dict = {
        'airflow-db': ['POSTGRES_USER', 'POSTGRES_PASSWORD'],
        'superset-metadata-db': ['POSTGRES_USER_SUPERSET', 'POSTGRES_PASSWORD_SUPERSET'],
        'superset': ['POSTGRES_PASSWORD_SUPERSET', 'SUPERSET_SECRET_KEY'],
        'mongodb': ['MONGO_INITDB_ROOT_USERNAME', 'MONGO_INITDB_ROOT_PASSWORD'],
        'mongo-express': ['ME_CONFIG_BASICAUTH_USERNAME', 'ME_CONFIG_BASICAUTH_PASSWORD'],
        'mysql': ['MYSQL_USER', 'MYSQL_PASSWORD'],
        'phpmyadmin': ['PMA_USER', 'PMA_PASSWORD'],
        'neo4j': ['NEO4J_AUTH'],
        'postgres': ['POSTGRES_USER_PG', 'POSTGRES_PASSWORD_PG'],
        'pgadmin': ['PGADMIN_DEFAULT_EMAIL', 'PGADMIN_DEFAULT_PASSWORD']
    }

    signin_configs = {}

    # Read the content of the .env file into a dictionary
    env_dict = {}
    with open(env_file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            key, value = line.split('=', 1)
            env_dict[key.strip()] = value.strip()

    # Extract signin configurations for each service in the services_dict
    for service, config_needed in services_dict.items():
        if service in env_params_dict:
            service_configs = {}
            for param in env_params_dict[service]:
                if param in env_dict:
                    service_configs[param] = env_dict[param]
                else:
                    service_configs[param] = None  # If no value is found, set it to None
            signin_configs[service] = service_configs

    return signin_configs

def extract_nifi_credentials():
    # Run the docker logs command and capture the output
    try:
        command = "sudo docker logs nifi | grep -E 'Generated Username|Generated Password' | grep -v 'tail:'"
        logs = subprocess.check_output(command, shell=True, text=True)
        
        # Split the logs into lines
        lines = logs.splitlines()
        
        # Extract the username and password from the logs
        username = None
        password = None
        
        for line in lines:
            if "Generated Username" in line:
                username = line.replace("Generated Username:", '').strip()
            elif "Generated Password" in line:
                password = line.replace("Generated Password:", '').strip()
        
        return username, password

    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        return None, None

# Example usage
username, password = extract_nifi_credentials()

if username and password:
    print(f"Extracted Username: {username}")
    print(f"Extracted Password: {password}")
else:
    print("Failed to extract credentials.")
    
    
def wait_for_docker_containers(timeout=60):
    """
    Waits for Docker containers to be ready by checking the logs.
    If containers are not ready within the timeout, it will raise an exception.
    """
    start_time = time.time()  # Track the start time to enforce timeout
    while True:
        # Run the docker-compose logs command to fetch logs of all containers
        result = subprocess.run(
            ['docker-compose', 'logs', '--tail', '10'], capture_output=True, text=True
        )
        logs = result.stdout
        
        # Look for any "Running X/Y" pattern in the logs
        if re.search(r"Running \d+/\d+", logs):  # Regex to match "Running X/Y"
            return True  # Services are ready, return True

        # Check if the timeout has been exceeded
        elapsed_time = time.time() - start_time
        if elapsed_time > timeout:
            return False  # Timeout, services are not ready

        # Wait for 5 seconds before checking again
        time.sleep(5)
        
        
        
        
if __name__ == '__main__':
    pass
            
