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

def refine_access_links(ports):
    services_w_ports  = ['airflow-webserver', \
        'jobmanager', 'conduktor-console', 'spark-master', \
        'superset', 'namenode', 'mongo-express', 'phpmyadmin',\
        'neo4j', 'nifi', 'pgadmin']
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
        'superset': ['POSTGRES_PASSWORD_SUPERSET', 'SUPERSET_SECRET_KEY'],
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

def extract_nifi_credentials():
    try:
        command = "sudo docker logs nifi | grep -E 'Generated Username|Generated Password' | grep -v 'tail:'"
        logs = subprocess.check_output(command, shell=True, text=True)
        
        lines = logs.splitlines()
        
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
        
if __name__ == '__main__':
    pass
            
