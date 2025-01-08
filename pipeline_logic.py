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
                             'Storage' : 'MongoDB', 
                             'Processing': 'Apache Spark', 
                             'Intermediate Storage': 'MongoDB'},
                    
                    "no": {'Ingestion': 'NiFi', 
                             'Storage' : 'MongoDB'}
                },
                "dashboard": {
                    "yes": {'Ingestion': 'NiFi', 
                             'Storage' : 'Postgres', 
                             'Processing': 'Apache Spark', 
                             'Intermediate Storage': 'MongoDB',
                             'Visualization': 'Apache Superset'},
                    "no": {'Ingestion': 'NiFi', 
                             'Storage' : 'Postgres', 
                             'Processing': 'Apache Spark', 
                             'Intermediate Storage': 'MongoDB',
                             'Visualization': 'Apache Superset'}
                },
                "graph": {
                    "yes" :{'Ingestion': 'NiFi', 
                             'Storage' : 'Neo4j', 
                             'Processing': 'Apache Spark', 
                             'Intermediate Storage': 'MongoDB'},
                    
                    "no" : {'Ingestion': 'NiFi', 
                             'Storage' : 'Neo4j', 
                             'Processing': 'Apache Spark', 
                             'Intermediate Storage': 'MongoDB'}
                },
            },
            "mixture": {
                "storage": {
                    "yes": {'Ingestion': 'NiFi', 
                            'Structured' : 'Postgres', 
                            'Semi': 'MongoDB', 
                            'Processing': 'Apache Spark', 
                            'Storage': 'Postgres'},
                    
                    "no": {'Ingestion': 'NiFi', 
                            'Structured' : 'Postgres', 
                            'Semi': 'MongoDB'}
                },
                "dashboard": {
                    "yes": {'Ingestion': 'NiFi', 
                            'Structured' : 'Postgres', 
                            'Semi': 'MongoDB', 
                            'Processing': 'Apache Spark', 
                            'Storage': 'Postgres',
                            'Visualization' : 'Apache Superset'}
                    ,
                    "no": {'Ingestion': 'NiFi', 
                            'Structured' : 'Postgres', 
                            'Semi': 'MongoDB', 
                            'Processing': 'Apache Spark', 
                            'Storage': 'Postgres',
                            'Visualization' : 'Apache Superset'}
                },
                "graph": {
                    "yes" :{'Ingestion': 'NiFi', 
                            'Structured' : 'Postgres', 
                            'Semi': 'MongoDB', 
                            'Processing': 'Apache Spark', 
                            'Storage': 'Neo4j'},
                    
                    "no" : {'Ingestion': 'NiFi', 
                            'Structured' : 'Postgres', 
                            'Semi': 'MongoDB', 
                            'Processing': 'Apache Spark', 
                            'Storage': 'Neo4j'}
                },
            },
        },
        "streaming": {
            "structured": {
                "storage": {
                    "yes": {'Ingestion' :'Apache Kafka',
                            'Processing':' Apache Spark',
                            'Storage': 'Postgres'},
                    
                    "no": {'Ingestion' :'Apache Kafka',
                            'Storage': 'Postgres'}
                },
                "dashboard": {
                    "yes": {'Ingestion' :'Apache Kafka',
                            'Processing':' Apache Spark',
                            'Storage': 'Postgres',
                            'Visualization': 'Apache Superset'},
                    
                    "no": {'Ingestion' :'Apache Kafka',
                            'Storage': 'Postgres',
                            'Visualization': 'Apache Superset'}
                },
                
                "graph": {
                    "yes" :{'Ingestion': 'Apache Kafka', 
                             'Storage' : 'Neo4j', 
                             'Processing': 'Apache Spark'},
                    
                    "no" : {'Ingestion': 'Apache Kafka', 
                             'Storage' : 'Neo4j', 
                             'Processing': 'Apache Spark'}
                },
            },
            "semi-structured": {
                "storage": {
                    "yes":{'Ingestion' :'Apache Kafka',
                            'Processing':' Apache Spark',
                            'Storage': 'MongoDB'},
                    
                    "no": {'Ingestion' :'Apache Kafka',
                            'Storage': 'MongoDB'}
                },
                "dashboard": {
                    "yes": {'Ingestion' :'Apache Kafka',
                            'Processing':' Apache Spark',
                            'Storage': 'Postgres',
                            'Visualization': 'Apache Superset'},
                    
                    "no": {'Ingestion' :'Apache Kafka',
                            'Processing':' Apache Spark',  
                            'Storage': 'Postgres',
                            'Visualization': 'Apache Superset'}
                },
                
                "graph": {
                    "yes" :{'Ingestion': 'Apache Kafka', 
                             'Storage' : 'Neo4j', 
                             'Processing': 'Apache Spark'},
                    
                    "no" : {'Ingestion': 'Apache Kafka', 
                             'Storage' : 'Neo4j', 
                             'Processing': 'Apache Spark'}
                },
            },
            "mixture": {
                "storage": {
                    "yes": {'Ingestion': 'Apache Kafka',
                            'Processing': 'Apache Spark',  
                            'Structured' : 'Postgres', 
                            'Semi': 'MongoDB'},  # requires attention
                    "no": {'Ingestion': 'Apache Kafka', 
                            'Structured' : 'Postgres', 
                            'Semi': 'MongoDB'}
                },
                "dashboard": {
                    "yes": {'Ingestion': 'Apache Kafka',
                            'Processing': 'Apache Spark',  
                            'Storage' : 'Postgres', 
                            'Visualization': 'Apache Superset'},
                    "no": {'Ingestion': 'Apache Kafka',
                            'Processing': 'Apache Spark',  
                            'Storage' : 'Postgres', 
                            'Visualization': 'Apache Superset'}
                },
                
                "graph": {
                    "yes" :{'Ingestion': 'Apache Kafka',
                            'Processing': 'Apache Spark',  
                            'Structured' : 'Postgres', 
                            'Semi': 'MongoDB',
                            'Storage' :'Neo4j'},
                    
                    "no" : {'Ingestion': 'Apache Kafka',
                            'Structured' : 'Postgres', 
                            'Semi': 'MongoDB', 
                            'Storage' : 'Neo4j', 
                            'Processing': 'Apache Spark'}
                },
            },
        },
    }



    pipe=  pipelines[nature][data_type][end_goal][transformation]
    
    

    if pipe.get("Semi") == "MongoDB" or pipe.get("Structured") == "Postgres":
        pipe.update({
            'Alternate Structured Storage Tools': ["MySQL", "Hadoop Standalone"], 
            'Alternate Semi-Structured Storage Tools' :["Cassandra", "Hadoop Standalone"]
        })
    if pipe.get("Storage") == "Postgres":
         pipe.update({'Alternate Final Storage Tools': ["MySQL",  "Hadoop Standalone"]})
    if pipe.get("Storage") == "MongoDB":
         pipe.update({'Alternate Final Storage Tools': ["Cassandra", "Hadoop Standalone"]})
         
    if pipe.get('Intermediate Storage') == "Postgres":
        pipe.update({'Alternate Intermediate Storage Tools': ["MySQL", "Hadoop Standalone"]})
    elif pipe.get("Intermediate Storage") == "MongoDB":
        pipe.update({'Alternate Intermediate Storage Tools': ["Cassandra", "Hadoop Standalone"]})
    
    pipe.update({'Orchestration': 'Airflow'})
    pipe.update({'Alternate Orchestration': ['Prefect']})
    return pipe



if __name__ == '__main__':
    print(get_pipeline('structured', 'batch', 'dashboard', 'no'))