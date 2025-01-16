import os
from typing import Dict, List, Tuple, Union


class ToolConfigManager:
    """
    Manages tool definitions, environment files, and other configurations.

    This class provides methods to define tools, generate environment files,
    retrieve configuration details, refine access links for services, and extract
    sign-in configurations from environment files.
    """

    def __init__(self, docker_manager) -> None:
        """
        Initializes the ToolConfigManager with a DockerManager instance.

        Args:
            docker_manager (DockerManager): An instance of DockerManager, allowing
                                            interaction with Docker-related functionality.
        """
        self.docker_manager = docker_manager

    def tool_definition(self, pipeline_dict: Dict[str, Union[str, List[str]]], tools_config: Dict[str, Dict]) -> Dict[str, Dict]:
        """
        Filters and formats tools based on a pipeline dictionary.

        Args:
            pipeline_dict (Dict[str, Union[str, List[str]]]): A dictionary containing tool types and their selections.
            tools_config (Dict[str, Dict]): A dictionary containing configurations for all available tools.

        Returns:
            Dict[str, Dict]: A dictionary of shortlisted tools with their configurations.
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

    def generate_env_file(self, config: Dict[str, Dict], output_file: str = ".env") -> None:
        """
        Generates an environment file (.env) from the given configuration.

        Args:
            config (Dict[str, Dict]): A dictionary containing service configurations, including environment variables.
            output_file (str): The name of the output .env file. Defaults to ".env".

        Returns:
            None
        """
        with open(output_file, "w") as file:
            for service, details in config.items():
                if "EnvironmentVariables" in details:
                    file.write(f"# {service} Environment Variables\n")
                    for key, value in details["EnvironmentVariables"].items():
                        file.write(f"{key}={value}\n")
                    file.write("\n")

    def retrieve_config_details(self, form_data, docker_config: Dict[str, Dict]) -> Tuple[Dict[str, Dict], Dict[str, List[str]]]:
        """
        Retrieves updated configuration details and merges Docker Compose files.

        Args:
            form_data (FormData): A form-like object containing submitted tool names and configurations.
            docker_config (Dict[str, Dict]): A dictionary of tool configurations, including environment variables.

        Returns:
            Tuple[Dict[str, Dict], Dict[str, List[str]]]:
                - A dictionary of updated configurations.
                - A dictionary of port mappings for the merged Docker Compose file.
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

    def refine_access_links(self, ports: Dict[str, List[str]]) -> Dict[str, str]:
        """
        Refines access links for services with mapped ports.

        Args:
            ports (Dict[str, List[str]]): A dictionary of services and their assigned ports.

        Returns:
            Dict[str, str]: A dictionary mapping service names to their access links.
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

    def extract_signin_configs(self, services_dict: Dict[str, Dict], env_file_path: str = '.env') -> Union[Dict[str, Dict], None]:
        """
        Extracts sign-in configurations for services from the environment file.

        Args:
            services_dict (Dict[str, Dict]): A dictionary of services and the parameters needed for sign-in.
            env_file_path (str): Path to the .env file. Defaults to '.env'.

        Returns:
            Union[Dict[str, Dict], None]: A dictionary of sign-in configurations for each service,
                                          or None if the .env file is missing or empty.
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
