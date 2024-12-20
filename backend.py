
def build_pipeline(format, endgoal, nature, transformation, num_transformations):


    ingestion_tool = None
    storage_tool = None
    intermediate_storage_tool = None
    processing_tool = None
    visualization_tool = None
    orchestration_tool = None
    alternate_storage = []
    alternate_ingestion = ['Python']
  
    
    if nature == "streaming_data":
        ingestion_tool = "Apache Kafka"
    elif nature == "batch_data":
        ingestion_tool = "Apache Sqoop" if format in ["structured", "semi_structured"] else "Apache Flume"
        alternate_ingestion.append('Apache Sqoop') if ingestion_tool == 'Apache Flume' else alternate_ingestion.append('Apache Flume')
        
    
    # Step 3: Select Storage Tool
    if format == "structured":
        storage_tool = "Postgres"
        alternate_storage.append('MySQL')
    elif format == "semi_structured":
        storage_tool = "Cassandra"
        alternate_storage.append('MongoDB')
    elif format == 'graph':
        storage_tool = 'Neo4j'
    elif format == "mixed_format" or nature == "batch_data":
        storage_tool = "Hadoop Standalone"
        alternate_storage.append('MongoDB')
    elif format == "graphs":
        storage_tool = "Neo4j"
        


    # Step 4: Select Processing Tool
    if transformation == "yes":
        processing_tool = "Apache Spark"
        
    if int(num_transformations) > 1 and format =='structured' or format =='mixed_format':
        intermediate_storage_tool = 'Hadoop Standalone'
    elif  int(num_transformations) > 1 and format =='semi_structured':
        intermediate_storage_tool = 'MongoDB'
    elif  int(num_transformations) > 1 and format =='graph':
        intermediate_storage_tool = 'Neo4j'
    else:
        intermediate_storage_tool = 0
        
        
    # Step 6: Select Visualization Tool
    if endgoal == "analytics_dashboard":
        visualization_tool = "Apache Superset"
    orchestration_tool = 'Airflow'
    return {
        "Ingestion": ingestion_tool,
        "Storage": storage_tool,
        "Processing": processing_tool,
        'Intermediate Storage': intermediate_storage_tool,
        "Visualization": visualization_tool,
        'Alternate Ingestion Tools': alternate_ingestion,
        'Alternate Storage Tools' : alternate_storage,
    }



