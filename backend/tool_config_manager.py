import os


class ToolConfigManager:
    """
    Manages tool definitions, environment files, and other configurations.
    Preserves the original function signatures and logic.
    """

    def __init__(self, docker_manager):
        """
        docker_manager: An instance of DockerManager, so we can call
                        docker_manager.merge_docker_compose() inside retrieve_config_details().
        """
        self.docker_manager = docker_manager

    def tool_definition(self, pipeline_dict, tools_config):
        """
        Equivalent to the original tool_definition().
        """
        selected_tools = {key: value for key, value in pipeline_dict.items() if value}
        shortlisted_tools = {}
        for type_object, tool in selected_tools.items():
            if isinstance(tool, list):
                pass
            else:
                tool = tool.replace(' ', '')
                shortlisted_tools.update({tool: tools_config[tool]})
        return shortlisted_tools

    def generate_env_file(self, config, output_file=".env"):
        """
        Equivalent to the original generate_env_file().
        """
        with open(output_file, "w") as file:
            for service, details in config.items():
                if "EnvironmentVariables" in details:
                    file.write(f"# {service} Environment Variables\n")
                    for key, value in details["EnvironmentVariables"].items():
                        file.write(f"{key}={value}\n")
                    file.write("\n")

    def retrieve_config_details(self, form_data, docker_config):
        """
        Equivalent to the original retrieve_config_details().
        Invokes merge_docker_compose() from DockerManager.
        """
        tool_names = [tool_name for tool_name in form_data.getlist('tool_names')]
        updated_config = {}
        ports = {}

        for tool_name in tool_names:
            if tool_name in docker_config:
                tool_config = docker_config[tool_name]
                updated_env_vars = {}

                for var_name, default_value in tool_config["EnvironmentVariables"].items():
                    input_value = form_data.get(f"{tool_name}['EnvironmentVariables']'[{var_name}]")

                    if input_value is not None:
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

        # Call merge_docker_compose using the DockerManager
        if tool_names:
            ports = self.docker_manager.merge_docker_compose(tool_names)

        return updated_config, ports

    def refine_access_links(self, ports):
        """
        Equivalent to the original refine_access_links().
        """
        services_w_ports = [
            'airflow-webserver', 'jobmanager', 'conduktor-console', 'spark-master',
            'superset', 'namenode', 'mongo-express', 'phpmyadmin',
            'neo4j', 'nifi', 'pgadmin', 'prefect-orion'
        ]
        extracted_services = {}
        for service in services_w_ports:
            if service in ports.keys():
                if service == 'nifi':
                    extracted_services[service] = ports[service][1].split(':')[0]
                else:
                    extracted_services[service] = ports[service][0].split(':')[0]
        return extracted_services

    def extract_signin_configs(self, services_dict, env_file_path='.env'):
        """
        Equivalent to the original extract_signin_configs().
        """
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

        if not os.path.exists(env_file_path):
            # If .env doesn't exist, we can return None or handle accordingly
            return None

        with open(env_file_path, 'r') as file:
            for line in file:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                key, value = line.split('=', 1)
                env_dict[key.strip()] = value.strip()

        if not services_dict:
            return None

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
