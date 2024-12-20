import json

# Function to collect user input for the scenario
def get_scenario_input():
    print("Welcome to the Data Pipeline Creation System!")
    
    # Collect data source type
    source_type = input("Enter data source type (e.g., 'database', 'api', 'file'): ")
    
    # Collect transformation needs
    transformation = input("Enter transformation type (e.g., 'batch', 'streaming'): ")
    
    # Collect sink type
    sink_type = input("Enter data sink type (e.g., 'dashboard', 'storage'): ")
    
    # Collect non-functional requirements (e.g., scalability, cost)
    scalability = input("Enter scalability requirement (e.g., 'high', 'low'): ")
    latency = input("Enter latency requirement (e.g., 'low', 'high'): ")
    cost = input("Enter cost constraints (e.g., 'low', 'high'): ")
    
    # Return the collected data in a dictionary format
    scenario = {
        "source_type": source_type,
        "transformation": transformation,
        "sink_type": sink_type,
        "scalability": scalability,
        "latency": latency,
        "cost": cost
    }
    
    return scenario

# Function to recommend tools based on the scenario
def recommend_tools(scenario):
    print("\nBased on the scenario, the recommended tools are:\n")
    
    # Select tools for the source type
    if scenario["source_type"] == "database":
        source_tool = "Sqoop"
    elif scenario["source_type"] == "api":
        source_tool = "Python (Requests)"
    else:
        source_tool = "Python (File Handling)"
    
    # Select transformation tools
    if scenario["transformation"] == "batch":
        transformation_tool = "Spark"
    else:
        transformation_tool = "Flink"
    
    # Select sink tools
    if scenario["sink_type"] == "dashboard":
        sink_tool = "Superset"
    else:
        sink_tool = "Hadoop"
    
    # Suggest a possible orchestration tool
    orchestration_tool = "Airflow"  # Default orchestration tool
    
    # Return the selected tools as a dictionary
    tools = {
        "source_tool": source_tool,
        "transformation_tool": transformation_tool,
        "sink_tool": sink_tool,
        "orchestration_tool": orchestration_tool
    }
    
    return tools

# Function to simulate the pipeline deployment
def deploy_pipeline(scenario, tools):
    print("\nDeploying pipeline based on the following configuration:\n")
    
    # Display the user's scenario input
    print("Scenario: ")
    print(json.dumps(scenario, indent=4))
    
    # Display the recommended tools
    print("\nRecommended Tools: ")
    print(json.dumps(tools, indent=4))
    
    # Here, in a real implementation, you would integrate with tool-specific APIs or configurations
    print("\nPipeline deployed successfully with the selected tools and configurations!")

# Main function to run the process
def main():
    # Step 1: Collect user input for the scenario
    scenario = get_scenario_input()
    
    # Step 2: Recommend tools based on the input scenario
    tools = recommend_tools(scenario)
    
    # Step 3: Deploy the pipeline based on the selected tools
    deploy_pipeline(scenario, tools)

# Run the main function
if __name__ == "__main__":
    main()
