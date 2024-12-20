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
                print(updated_env_vars)
                
                updated_config[tool_name] = {
                "EnvironmentVariables": updated_env_vars
            }
    return updated_config