from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from typing import Dict, List, Tuple, Union
import os

class ToolConfigState(TypedDict):
    pipeline_dict: Dict[str, Union[str, List[str]]]
    tools_config: Dict[str, Dict]
    config: Dict[str, Dict]
    tool_names: List[str]
    ports: Dict[str, List[str]]
    services_dict: Dict[str, Dict]
    env_file_path: str
    updated_config: Dict[str, Dict]

class ToolConfigAgent:
    """
    Manages tool definitions, environment files, and other configurations.
    """

    def __init__(self, docker_agent) -> None:
        """
        Initializes the ToolConfigAgent with a DockerAgent instance.

        Args:
            docker_agent (DockerAgent): An instance of DockerAgent.
        """
        self.docker_agent = docker_agent
        self.tool_dependencies = {
            "airflow-webserver": ["airflow-db", "airflow-init", "airflow-scheduler", "airflow-webserver"],
            "jobmanager": ["jobmanager", "taskmanager"],
            "zoo1": [ "zoo1", "kafka1", "kafka-schema-registry", "kafka-rest-proxy", "kafka-connect"],
            "spark-master": ["spark-master", "spark-worker"],
            "superset": ["superset-metadata-db", "superset"],
            "namenode": ["namenode", "datanode"],
            "mongo-express": ["mongo", "mongo-express"],
            "phpmyadmin": ["mysql", "phpmyadmin"],
            "neo4j": ["neo4j"],
            "nifi": ["nifi"],
            "pgadmin": ["postgres", "pgadmin"],
            "prefect-orion": ["prefect-orion", "prefect-worker"],
            "cassandra" : ["cassandra"],
            "conduktorDB" : ["conduktorDB", "conduktor-console"]
        }
        # Graph for tool definition
        self.tool_def_graph = StateGraph(ToolConfigState)
        self.tool_def_graph.add_node("DefineTools", self._tool_definition)
        self.tool_def_graph.add_edge(START, "DefineTools")
        self.tool_def_graph.add_edge("DefineTools", END)
        self.compiled_tool_def_graph = self.tool_def_graph.compile()

        # Graph for generating environment files
        self.env_file_graph = StateGraph(ToolConfigState)
        self.env_file_graph.add_node("GenerateEnv", self._generate_env_file)
        self.env_file_graph.add_edge(START, "GenerateEnv")
        self.env_file_graph.add_edge("GenerateEnv", END)
        self.compiled_env_file_graph = self.env_file_graph.compile()

        # Graph for retrieving configuration details
        self.config_details_graph = StateGraph(ToolConfigState)
        self.config_details_graph.add_node("RetrieveConfig", self._retrieve_config_details)
        self.config_details_graph.add_edge(START, "RetrieveConfig")
        self.config_details_graph.add_edge("RetrieveConfig", END)
        self.compiled_config_details_graph = self.config_details_graph.compile()

        # Graph for refining access links
        self.refine_links_graph = StateGraph(ToolConfigState)
        self.refine_links_graph.add_node("RefineLinks", self._refine_access_links)
        self.refine_links_graph.add_edge(START, "RefineLinks")
        self.refine_links_graph.add_edge("RefineLinks", END)
        self.compiled_refine_links_graph = self.refine_links_graph.compile()

        # Graph for extracting sign-in configurations
        self.signin_config_graph = StateGraph(ToolConfigState)
        self.signin_config_graph.add_node("ExtractSigninConfigs", self._extract_signin_configs)
        self.signin_config_graph.add_edge(START, "ExtractSigninConfigs")
        self.signin_config_graph.add_edge("ExtractSigninConfigs", END)
        self.compiled_signin_config_graph = self.signin_config_graph.compile()
        
        # Graph for extracting sign-in configurations
        self.all_services_graph = StateGraph(ToolConfigState)
        self.all_services_graph.add_node("ExtractAllDependencies", self._all_services)
        self.all_services_graph.add_edge(START, "ExtractAllDependencies")
        self.all_services_graph.add_edge("ExtractAllDependencies", END)
        self.compiled_all_services_graph = self.all_services_graph.compile()

    # NODE IMPLEMENTATIONS
    def _tool_definition(self, state: ToolConfigState) -> ToolConfigState:
        selected_tools = {key: value for key, value in state["pipeline_dict"].items() if value}
        shortlisted_tools = {}
        for type_object, tool in selected_tools.items():
            if isinstance(tool, list):
                pass
            else:
                tool = tool.replace(" ", "")
                shortlisted_tools.update({tool: state["tools_config"][tool]})
        state["updated_config"] = shortlisted_tools
        return state

    def _generate_env_file(self, state: ToolConfigState) -> ToolConfigState:
        with open(state["env_file_path"], "w") as file:
            for service, details in state["updated_config"].items():
                if "EnvironmentVariables" in details:
                    file.write(f"# {service} Environment Variables\n")
                    for key, value in details["EnvironmentVariables"].items():
                        file.write(f"{key}={value}\n")
                    file.write("\n")
        return state

    def _retrieve_config_details(self, state: ToolConfigState) -> ToolConfigState:
        tool_names = state["tool_names"]
        updated_config = {}

        for tool_name in tool_names:
            if tool_name in state["tools_config"]:
                tool_config = state["tools_config"][tool_name]
                updated_env_vars = {}

                for var_name, default_value in tool_config["EnvironmentVariables"].items():
                    input_value = None  # Placeholder for form data
                    updated_env_vars[var_name] = input_value or default_value

                updated_config[tool_name] = {"EnvironmentVariables": updated_env_vars}

        docker_state = {
            "command": "",
            "tool_names": tool_names,
            "base_directory": "docker_templates",
            "ports": {},
            "compose_file_path": "docker-compose.yml",
            "success": False,
            "error": "",
        }

        docker_state = self.docker_agent.invoke_merge(docker_state)

        if not docker_state["success"]:
            state["updated_config"] = {}
            state["ports"] = {}
            raise RuntimeError(f"Error merging Docker Compose files: {docker_state['error']}")
        print(f'These are the updated configs')
        state["updated_config"] = updated_config
        state["ports"] = docker_state["ports"]
        return state

    def _refine_access_links(self, state: ToolConfigState) -> ToolConfigState:
        services_with_ports = [
            "airflow-webserver", "jobmanager", "conduktor-console", "spark-master",
            "superset", "namenode", "mongo-express", "phpmyadmin",
            "neo4j", "nifi", "pgadmin", "prefect-orion",
        ]
        extracted_services = {}
        for service in services_with_ports:
            if service in state["ports"]:
                if service == "nifi":
                    extracted_services[service] = state["ports"][service][1].split(":")[0]
                else:
                    extracted_services[service] = state["ports"][service][0].split(":")[0]
        state["updated_config"]["access_links"] = extracted_services
        print(f'these are the extracted services --------------------{extracted_services}')
        return state

    def _extract_signin_configs(self, state: ToolConfigState) -> ToolConfigState:
        env_params_dict = {
            'airflow-db': ['POSTGRES_USER', 'POSTGRES_PASSWORD'],
            'superset-metadata-db': ['POSTGRES_USER_SUPERSET', 'POSTGRES_PASSWORD_SUPERSET'],
            'airflow-webserver': ['AIRFLOW_ADMIN_USER', 'AIRFLOW_ADMIN_PASS'],
            'mongo': ['MONGO_INITDB_ROOT_USERNAME', 'MONGO_INITDB_ROOT_PASSWORD'],
            'mongo-express': ['ME_CONFIG_BASICAUTH_USERNAME', 'ME_CONFIG_BASICAUTH_PASSWORD'],
            'mysql': ['MYSQL_USER', 'MYSQL_PASSWORD'],
            'phpmyadmin': ['PMA_USER', 'PMA_PASSWORD'],
            'neo4j': ['NEO4J_AUTH'],
            'postgres': ['POSTGRES_USER_PG', 'POSTGRES_PASSWORD_PG'],
            'pgadmin': ['PGADMIN_DEFAULT_EMAIL', 'PGADMIN_DEFAULT_PASSWORD']
        }
        signin_configs = {}
        if not os.path.exists(state["env_file_path"]):
            return state

        env_dict = {}
        with open(state["env_file_path"], "r") as file:
            for line in file:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                key, value = line.split("=", 1)
                env_dict[key.strip()] = value.strip()

        for service, config_needed in state["services_dict"].items():
            service_configs = {param: env_dict.get(param, None) for param in env_params_dict.get(service, [])}
            signin_configs[service] = service_configs
        state["updated_config"]["signin_configs"] = signin_configs

        return state
    
    

    
    def _all_services(self, state: ToolConfigState):
        filtered_dependencies = {}
        for key in state['ports'].keys():
            if key in self.tool_dependencies:
                filtered_dependencies[key] = self.tool_dependencies[key]
        state['ports'] = filtered_dependencies
                
        return state

    # PUBLIC METHODS TO INVOKE GRAPHS
    def invoke_tool_definition(self, state: ToolConfigState) -> ToolConfigState:
        return self.compiled_tool_def_graph.invoke(state)

    def invoke_env_file_generation(self, state: ToolConfigState) -> ToolConfigState:
        return self.compiled_env_file_graph.invoke(state)

    def invoke_config_details_retrieval(self, state: ToolConfigState) -> ToolConfigState:
        return self.compiled_config_details_graph.invoke(state)

    def invoke_refine_access_links(self, state: ToolConfigState) -> ToolConfigState:
        return self.compiled_refine_links_graph.invoke(state)

    def invoke_signin_configs_extraction(self, state: ToolConfigState) -> ToolConfigState:
        return self.compiled_signin_config_graph.invoke(state)
    
    def invoke_all_services(self, state: ToolConfigState) -> ToolConfigState:
        return self.compiled_all_services_graph.invoke(state)
