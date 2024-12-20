import json


with open('config.json', "r") as f:
    tools_config = json.load(f)  # converts it into pythin data structures

selected_tools = {'Ingestion': 'Apache Flume', 
    'Storage': 'Hadoop Standalone', 
    'Processing': 'Apache Spark', 
    'Intermediate Storage': 0,
    'Visualization': None, 
    'Orchestration': 'Cron',
    'Alternate Ingestion Tools': ['Python', 'Apache Sqoop'], 
    'Alternate Storage Tools': ['MongoDB']}

# Leaving out None values
selected_tools = {key: value for key, value in selected_tools.items() if value}



shortlisted_tools = {}
for type_object, tool in selected_tools.items():
    if isinstance(tool, list):
        pass
    else:
        tool = tool.replace(' ', '')
        shortlisted_tools.update({tool : tools_config[tool]['EnvironmentVariables']})
        print('Tool successfully added', tool)
        

print(shortlisted_tools)