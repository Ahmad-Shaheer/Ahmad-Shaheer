import subprocess
import requests
import json
import os
import shutil
import yaml

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
        result = subprocess.run(f"sudo {command}", shell=True, check=True)     
    
        if result.stderr:
            print("Error:\n", result.stderr)
        
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
        print("Error Output:", e.stderr)


def down_docker_compose():
    try:
        command = "docker compose down -v"
        result = subprocess.run(f"sudo {command}", shell=True, check=True)     
    
        if result.stderr:
            print("Error:\n", result.stderr)
        
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
        print("Error Output:", e.stderr)
        

def extract_signin_configs(services_dict, env_file_path='.env'):
    env_params_dict = {
        'airflow-db': ['POSTGRES_USER', 'POSTGRES_PASSWORD'],
        'superset-metadata-db': ['POSTGRES_USER_SUPERSET', 'POSTGRES_PASSWORD_SUPERSET'],
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
            
    if not services_dict:
        return  None
    for service, config_needed in services_dict.items():
        
        if service == 'superset':
            signin_configs[service] = {'USERNAME': 'admin', 'PASSWORD': 'admin'}
        elif service in env_params_dict:
            service_configs = {}
            for param in env_params_dict[service]:
                if param in env_dict:
                    service_configs[param] = env_dict[param]
                else:
                    service_configs[param] = None
            signin_configs[service] = service_configs
    
    return signin_configs


def infer(system, prompt):
    ollama_config = {
        "model": "llama3.1:8b-instruct-fp16",
        "max_tokens": 8192,
        "host": "172.16.19.80:11300"
    }

    data = {
        "model": ollama_config["model"],
        "max_tokens": ollama_config["max_tokens"],
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
            "temperature": 0.1  # change it as per requirement
        }
    }

    headers = {
        "Content-Type": "application/json"
    }
    ollama_url = f"http://{ollama_config['host']}/api/chat/"

    model_response = requests.post(
        url=ollama_url,
        json=data,
        headers=headers
    ).json()

    return model_response['message']['content']


SYSTEM_PROMPT = """
"You are a virtual assistant designed to guide users in planning and deploying their data pipelines. Your role is to help users make informed decisions based on their data type, processing needs, and end goals.

Your key functions include:

Providing practical recommendations for tools, frameworks, and strategies to process, transform, and store their data.
Explaining concepts in simple terms without unnecessary technical jargon unless explicitly requested.
Addressing common queries about data formats (e.g., CSV, JSON), data processing methods (batch or streaming), and pipeline tools (e.g., ETL, Apache Kafka).
Considerations:

Adapt recommendations based on user inputs, such as the nature of their data (structured, semi-structured, or mixed), their processing goals (storage, analytics, or graph-based databases), and whether transformations are needed.
Offer suggestions for both beginner-friendly and advanced tools depending on the user's expertise.
Maintain a concise, professional, and helpful tone throughout the conversation.
Tone Instructions:
YOU ARE NOT VERBOSE, your response should be at maximum 4 sentences
Formality: Use polite language with slight formality (e.g., "Please let us know," "We are happy to assist").
Clarity: Avoid technical jargon unless necessary.
Example: "Thank you for reaching out! Please let us know if you need further assistance."
"""


def check_containers_health():
    """
    Checks the health status of all running Docker containers using subprocess.
    Returns:
        - "no_containers" if no containers are running.
        - True, if all running containers are healthy.
        - A list of healthy container names, if not all containers are healthy.
          This list can be empty if none are healthy.
    """
 
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
            data = json.loads(inspect_result.stdout)
            container_info = data[0] if data else {}
            container_name = container_info.get("Name", "").lstrip("/")
            state = container_info.get("State", {})
            health = state.get("Health", {})
            health_status = health.get("Status")
            if health_status == "healthy":
                healthy_containers.append(container_name)
        except (json.JSONDecodeError, IndexError, KeyError) as e:
            print(f"Error parsing JSON for container {container_id}:", e)
            continue
 
    if len(healthy_containers) == len(container_ids):
        return True
    else:
        return healthy_containers
 

def merge_docker_compose(tool_names, base_directory="docker_templates"):
    """
    Merges docker-compose.yml files from multiple tools into a single Compose file.
    Handles port conflicts, merges volumes, and detects environment variable conflicts.
    """

    # Initialize the merged Compose structure
    merged_compose = {
        'version': '3.9',
        'services': {},
        'networks': {
            'data_pipeline_network': {}
        },
        'volumes': {}
    }

    # Dictionary for allocated host ports => service
    allocated_ports = {}

    # Store final (host:container) port assignments for each service
    port_assignments = {}

    # Temporary directory for merging volume contents
    temp_merged_volumes = "temp_merged_volumes"
    os.makedirs(temp_merged_volumes, exist_ok=True)

    # For detecting environment variable conflicts across services
    # Structure: {service_name: {env_key: env_value, ...}}
    all_service_envs = {}

    # ------------------------------------------------------------
    # NEW: Track used service names so we only prefix if there's a conflict
    used_service_names = set()
    # ------------------------------------------------------------

    for tool_name in tool_names:
        tool_dir = os.path.join(base_directory, tool_name.lower())
        compose_file_path = os.path.join(tool_dir, "docker-compose.yml")

        # --- 1. Read the Tool's docker-compose.yml ---
        if not os.path.exists(compose_file_path):
            print(f"Warning: Compose file not found for tool '{tool_name}': {compose_file_path}")
            continue

        with open(compose_file_path, 'r') as f:
            try:
                tool_compose = yaml.safe_load(f)
            except yaml.YAMLError as e:
                print(f"Error parsing YAML for tool '{tool_name}': {e}")
                continue

        if not tool_compose or 'services' not in tool_compose:
            print(f"Warning: No services defined in {compose_file_path}")
            continue

        # --- 2. Check if the tool has a custom Dockerfile ---
        has_dockerfile = os.path.exists(os.path.join(tool_dir, "Dockerfile"))

        # --- 3. Merge Services ---
        for service_name, service_config in tool_compose['services'].items():

            # ------------------------------------------------------------
            # CHANGE: Check if this service_name is already used
            if service_name in used_service_names:
                # Conflict -> rename + print message
                new_service_name = f"{tool_name.lower()}_{service_name}"
                print(f"Service name conflict detected for '{service_name}'. Renaming to '{new_service_name}'")
            else:
                # No conflict -> keep name as-is
                new_service_name = service_name

            # Add the final name to the used_service_names
            used_service_names.add(new_service_name)
            # ------------------------------------------------------------

            merged_compose['services'][new_service_name] = service_config.copy()

            # Handle custom build or image references
            if has_dockerfile and 'build' in service_config:
                build_value = service_config['build']
                if isinstance(build_value, dict):
                    # Dictionary form
                    merged_compose['services'][new_service_name]['build']['context'] = tool_dir
                elif isinstance(build_value, str):
                    # String form -> convert to dict
                    merged_compose['services'][new_service_name]['build'] = {
                        'context': os.path.join(tool_dir, build_value)
                    }
                else:
                    print(f"Warning: 'build' format for '{new_service_name}' is unrecognized.")
            else:
                # If no Dockerfile, we expect an image field or something else
                if 'image' not in service_config:
                    print(f"Warning: Service '{new_service_name}' has no 'image' or 'build' definition.")

            # --- 4. Handle Volume Mounts ---
            if 'volumes' in service_config:
                new_volume_list = []
                for vol in service_config['volumes']:
                    if isinstance(vol, str):
                        parts = vol.split(':')
                        if len(parts) == 2:
                            source, dest = parts
                            if source.startswith('./') or os.path.isdir(os.path.join(tool_dir, source)):
                                abs_source_path = os.path.join(tool_dir, source)
                                merged_volume_dir = os.path.join(
                                    temp_merged_volumes,
                                    f"{tool_name.lower()}_{service_name}_{os.path.basename(source.strip('./'))}"
                                )
                                if os.path.exists(abs_source_path):
                                    if os.path.isdir(abs_source_path):
                                        try:
                                            shutil.copytree(abs_source_path, merged_volume_dir, dirs_exist_ok=True)
                                        except OSError:
                                            print(f"Skipping copy for {abs_source_path}: Directory not found.")
                                    else:
                                        # Single file
                                        if os.path.isfile(abs_source_path):
                                            os.makedirs(merged_volume_dir, exist_ok=True)
                                            shutil.copy2(abs_source_path, merged_volume_dir)
                                        else:
                                            print(f"Skipping {abs_source_path}, not found.")
                                new_volume_list.append(f"{os.path.abspath(merged_volume_dir)}:{dest}")
                            else:
                                # Named volume, prefix with tool+service
                                volume_name = f"{tool_name.lower()}_{service_name}_{source}"
                                merged_compose['volumes'][volume_name] = {}
                                new_volume_list.append(f"{volume_name}:{dest}")
                        else:
                            new_volume_list.append(vol)
                    elif isinstance(vol, dict):
                        for k, v in vol.items():
                            volume_name = f"{tool_name.lower()}_{service_name}_{k}"
                            merged_compose['volumes'][volume_name] = {}
                            new_volume_list.append({volume_name: v})
                    else:
                        new_volume_list.append(vol)

                merged_compose['services'][new_service_name]['volumes'] = new_volume_list

            # Add the service to the shared network
            merged_compose['services'][new_service_name]['networks'] = ['data_pipeline_network']

            # --- 5. Handle Port Conflicts ---
            if 'ports' in service_config:
                updated_ports = []
                for port_mapping in service_config['ports']:
                    host_port = None
                    container_port = None

                    if isinstance(port_mapping, str):
                        parts = port_mapping.split(':')
                        if len(parts) == 2:
                            host_port_str, container_port_str = parts
                            host_port = int(host_port_str)
                            container_port = int(container_port_str)
                    elif isinstance(port_mapping, int):
                        host_port = port_mapping
                        container_port = port_mapping
                    elif (isinstance(port_mapping, dict)
                          and 'published' in port_mapping
                          and 'target' in port_mapping):
                        host_port = int(port_mapping['published'])
                        container_port = int(port_mapping['target'])

                    if host_port is not None:
                        while host_port in allocated_ports:
                            host_port += 1  # increment until free

                        allocated_ports[host_port] = new_service_name

                        if isinstance(port_mapping, str):
                            updated_ports.append(f"{host_port}:{container_port}")
                            port_assignments.setdefault(new_service_name, []).append(f"{host_port}:{container_port}")
                        elif isinstance(port_mapping, int):
                            updated_ports.append(host_port)
                            port_assignments.setdefault(new_service_name, []).append(str(host_port))
                        elif isinstance(port_mapping, dict):
                            new_port_mapping = {
                                'published': host_port,
                                'target': container_port
                            }
                            for extra_key in ['protocol', 'mode']:
                                if extra_key in port_mapping:
                                    new_port_mapping[extra_key] = port_mapping[extra_key]

                            updated_ports.append(new_port_mapping)
                            port_assignments.setdefault(new_service_name, []).append(f"{host_port}:{container_port}")

                merged_compose['services'][new_service_name]['ports'] = updated_ports

            # --- 6. Handle depends_on references, prefixing those too ---
            if 'depends_on' in service_config:
                depends_config = service_config['depends_on']

                if isinstance(depends_config, dict):
                    new_depends = {}
                    for dep_service, dep_config in depends_config.items():
                        # If the original dep_service was renamed, we'll just prefix it
                        # the same way we do for volumes or do no prefix at all.
                        if dep_service in used_service_names:
                            new_depends[dep_service] = dep_config
                        else:
                            new_depends[dep_service] = dep_config
                    merged_compose['services'][new_service_name]['depends_on'] = new_depends

                elif isinstance(depends_config, list):
                    new_depends_list = []
                    for dep_service in depends_config:
                        if dep_service in used_service_names:
                            new_depends_list.append(dep_service)
                        else:
                            new_depends_list.append(dep_service)
                    merged_compose['services'][new_service_name]['depends_on'] = new_depends_list

            # --- 7. Accumulate environment variables for conflict detection ---
            env_vars = merged_compose['services'][new_service_name].get('environment', {})
            if isinstance(env_vars, list):
                env_dict = {}
                for env_item in env_vars:
                    if '=' in env_item:
                        k, v = env_item.split('=', 1)
                        env_dict[k] = v
                env_vars = env_dict

            if not isinstance(env_vars, dict):
                env_vars = {}

            all_service_envs[new_service_name] = env_vars

    env_conflicts = {}
    for service_name, envs in all_service_envs.items():
        for k, v in envs.items():
            env_conflicts.setdefault(k, {}).setdefault(v, []).append(service_name)

    for env_var, values_dict in env_conflicts.items():
        if len(values_dict) > 1:
            print(f"Warning: Conflict detected for ENV variable '{env_var}':")
            for val, services in values_dict.items():
                print(f"  Value '{val}' set by services: {services}")

    # --- 9. Write the merged Docker Compose file ---
    with open("docker-compose.yml", 'w') as outfile:
        yaml.dump(merged_compose, outfile, sort_keys=False, indent=2)

   
    return port_assignments


def get_pipeline(data_type, nature, end_goal, transformation):
    pipelines = {
        "batch": {
            "structured": {
                "storage": {
                    "yes":  {'Ingestion': 'NiFi', 
                             'Storage' : 'Postgres', 
                             'Processing': 'Apache Spark', 
                             'Intermediate Storage': 'Postgres'},
                    
                    "no": {'Ingestion': 'NiFi', 
                             'Storage' : 'Postgres', 
                             }
                },
                "dashboard": {
                    "yes": {'Ingestion': 'NiFi', 
                             'Storage' : 'Postgres', 
                             'Processing': 'Apache Spark', 
                             'Intermediate Storage': 'Postgres',
                             'Visualization': 'Apache Superset'},
                    "no": {'Ingestion': 'NiFi', 
                             'Storage' : 'Postgres', 
                             'Visualization': 'Apache Superset'}
                },
                "graph": {
                    "yes" :{'Ingestion': 'NiFi', 
                             'Storage' : 'Neo4j', 
                             'Processing': 'Apache Spark', 
                             'Intermediate Storage': 'Postgres'},
                    
                    "no" : {'Ingestion': 'NiFi', 
                             'Storage' : 'Neo4j', 
                             'Processing': 'Apache Spark', 
                             'Intermediate Storage': 'Postgres'}
                    
                }
            },
            "semi-structured": {
                "storage": {
                    "yes": {'Ingestion': 'NiFi', 
                             'Storage' : 'Mongo', 
                             'Processing': 'Apache Spark', 
                             'Intermediate Storage': 'Mongo'},
                    
                    "no": {'Ingestion': 'NiFi', 
                             'Storage' : 'Mongo'}
                },
                "dashboard": {
                    "yes": {'Ingestion': 'NiFi', 
                             'Storage' : 'Postgres', 
                             'Processing': 'Apache Spark', 
                             'Intermediate Storage': 'Mongo',
                             'Visualization': 'Apache Superset'},
                    "no": {'Ingestion': 'NiFi', 
                             'Storage' : 'Postgres', 
                             'Processing': 'Apache Spark', 
                             'Intermediate Storage': 'Mongo',
                             'Visualization': 'Apache Superset'}
                },
                "graph": {
                    "yes" :{'Ingestion': 'NiFi', 
                             'Storage' : 'Neo4j', 
                             'Processing': 'Apache Spark', 
                             'Intermediate Storage': 'Mongo'},
                    
                    "no" : {'Ingestion': 'NiFi', 
                             'Storage' : 'Neo4j', 
                             'Processing': 'Apache Spark', 
                             'Intermediate Storage': 'Mongo'}
                },
            },
            "mixture": {
                "storage": {
                    "yes": {'Ingestion': 'NiFi', 
                            'Structured' : 'Postgres', 
                            'Semi': 'Mongo', 
                            'Processing': 'Apache Spark', 
                            'Final Structured' :'Postgres',
                            'Final Semi': 'Mongo'},
                    
                    "no": {'Ingestion': 'NiFi', 
                            'Structured' : 'Postgres', 
                            'Semi': 'Mongo'}
                },
                "dashboard": {
                    "yes": {'Ingestion': 'NiFi', 
                            'Structured' : 'Postgres', 
                            'Semi': 'Mongo', 
                            'Processing': 'Apache Spark', 
                            'Storage': 'Postgres',
                            'Visualization' : 'Apache Superset'}
                    ,
                    "no": {'Ingestion': 'NiFi', 
                            'Structured' : 'Postgres', 
                            'Semi': 'Mongo', 
                            'Processing': 'Apache Spark', 
                            'Storage': 'Postgres',
                            'Visualization' : 'Apache Superset'}
                },
                "graph": {
                    "yes" :{'Ingestion': 'NiFi', 
                            'Structured' : 'Postgres', 
                            'Semi': 'Mongo', 
                            'Processing': 'Apache Spark', 
                            'Storage': 'Neo4j'},
                    
                    "no" : {'Ingestion': 'NiFi', 
                            'Structured' : 'Postgres', 
                            'Semi': 'Mongo', 
                            'Processing': 'Apache Spark', 
                            'Storage': 'Neo4j'}
                },
            },
        },
        "streaming": {
            "structured": {
                "storage": {
                    "yes": {'Ingestion' :'Apache Kafka',
                            'Processing':'Apache Flink',
                            'Storage': 'Postgres'},
                    
                    "no": {'Ingestion' :'Apache Kafka',
                            'Storage': 'Postgres'}
                },
                "dashboard": {
                    "yes": {'Ingestion' :'Apache Kafka',
                            'Processing':'Apache Flink',
                            'Storage': 'Postgres',
                            'Visualization': 'Apache Superset'},
                    
                    "no": {'Ingestion' :'Apache Kafka',
                            'Storage': 'Postgres',
                            'Visualization': 'Apache Superset'}
                },
                
                "graph": {
                    "yes" :{'Ingestion': 'Apache Kafka', 
                             'Storage' : 'Neo4j', 
                             'Processing': 'Apache Flink'},
                    
                    "no" : {'Ingestion': 'Apache Kafka', 
                             'Storage' : 'Neo4j', 
                             'Processing': 'Apache Flink'}
                },
            },
            "semi-structured": {
                "storage": {
                    "yes":{'Ingestion' :'Apache Kafka',
                            'Processing':'Apache Flink',
                            'Storage': 'Mongo'},
                    
                    "no": {'Ingestion' :'Apache Kafka',
                            'Storage': 'Mongo'}
                },
                "dashboard": {
                    "yes": {'Ingestion' :'Apache Kafka',
                            'Processing':'Apache Flink',
                            'Storage': 'Postgres',
                            'Visualization': 'Apache Superset'},
                    
                    "no": {'Ingestion' :'Apache Kafka',
                            'Processing':'Apache Flink',  
                            'Storage': 'Postgres',
                            'Visualization': 'Apache Superset'}
                },
                
                "graph": {
                    "yes" :{'Ingestion': 'Apache Kafka', 
                             'Storage' : 'Neo4j', 
                             'Processing': 'Apache Flink'},
                    
                    "no" : {'Ingestion': 'Apache Kafka', 
                             'Storage' : 'Neo4j', 
                             'Processing': 'Apache Flink'}
                },
            },
            "mixture": {
                "storage": {
                    "yes": {'Ingestion': 'Apache Kafka',
                            'Processing': 'Apache Flink',  
                            'Structured' : 'Postgres', 
                            'Semi': 'Mongo',
                            'Final Structured' :'Postgres',
                            'Final Semi': 'Mongo'
                            },  # requires attention
                    "no": {'Ingestion': 'Apache Kafka', 
                            'Structured' : 'Postgres', 
                            'Semi': 'Mongo'}
                },
                "dashboard": {
                    "yes": {'Ingestion': 'Apache Kafka',
                            'Processing': 'Apache Flink',  
                            'Storage' : 'Postgres', 
                            'Visualization': 'Apache Superset'},
                    "no": {'Ingestion': 'Apache Kafka',
                            'Processing': 'Apache Flink',  
                            'Storage' : 'Postgres', 
                            'Visualization': 'Apache Superset'}
                },
                
                "graph": {
                    "yes" :{'Ingestion': 'Apache Kafka',
                            'Processing': 'Apache Flink',  
                            'Structured' : 'Postgres', 
                            'Semi': 'Mongo',
                            'Storage' :'Neo4j'},
                    
                    "no" : {'Ingestion': 'Apache Kafka',
                            'Structured' : 'Postgres', 
                            'Semi': 'Mongo', 
                            'Storage' : 'Neo4j', 
                            'Processing': 'Apache Flink'}
                },
            },
        },
    }



    pipe=  pipelines[nature][data_type][end_goal][transformation]
    
    

    if pipe.get("Semi") == "Mongo" or pipe.get("Structured") == "Postgres":
        pipe.update({
            'Alternate Structured Storage Tools': ["MySQL", "Hadoop Standalone"], 
            'Alternate Semi-Structured Storage Tools' :["Cassandra", "Hadoop Standalone"]
        })
    if pipe.get("Storage") == "Postgres":
         pipe.update({'Alternate Final Storage Tools': ["MySQL",  "Hadoop Standalone"]})
    if pipe.get("Storage") == "Mongo":
         pipe.update({'Alternate Final Storage Tools': ["Cassandra", "Hadoop Standalone"]})
    
    if pipe.get("Final Structured") == "Postgres":
        pipe.update({'Alternate Final Structured Storage Tools': ["MySQL",  "Hadoop Standalone"]})
    if pipe.get("Final Semi") == "Mongo":
        pipe.update({'Alternate Final Semi Storage Tools': ["Cassandra", "Hadoop Standalone"]})
        
        
        
    if pipe.get('Intermediate Storage') == "Postgres":
        pipe.update({'Alternate Intermediate Storage Tools': ["MySQL", "Hadoop Standalone"]})
    elif pipe.get("Intermediate Storage") == "Mongo":
        pipe.update({'Alternate Intermediate Storage Tools': ["Cassandra", "Hadoop Standalone"]})
    if pipe.get('Processing') == "Apache Flink":
        pipe.update({'Alternate Processing Tools': ["Apache Spark"]})
    if pipe.get('Processing') == "Apache Spark":
        pipe.update({'Alternate Processing Tools': ["Apache Flink"]})
        
    pipe.update({'Orchestration': 'Airflow'})
    pipe.update({'Alternate Orchestration': ['Prefect']})
    return pipe


