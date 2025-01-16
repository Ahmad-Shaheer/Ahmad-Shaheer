from typing import Dict, Union

class PipelineManager:
    """
    Manages pipeline selection and configuration.

    This class provides a method to retrieve pipeline configurations
    based on data type, processing nature, end goals, and transformations.
    """

    def get_pipeline(
        self,
        data_type: str,
        nature: str,
        end_goal: str,
        transformation: str
    ) -> Dict[str, Union[str, list]]:
        """
        Retrieves the configuration for a data pipeline based on the specified criteria.

        Args:
            data_type (str): The type of data the pipeline will process.
                - "structured": For structured data (e.g., relational databases).
                - "semi-structured": For semi-structured data (e.g., JSON, XML).
                - "mixture": A combination of structured and semi-structured data.
            nature (str): The nature of the pipeline.
                - "batch": For batch processing pipelines.
                - "streaming": For real-time or streaming pipelines.
            end_goal (str): The purpose or outcome of the pipeline.
                - "storage": Focuses on data ingestion and storage.
                - "dashboard": Includes storage and visualization components.
                - "graph": Utilizes graph databases for storage and analysis.
            transformation (str): Specifies whether intermediate processing or storage is involved.
                - "yes": Includes intermediate processing and storage steps.
                - "no": Directly maps the ingestion to the end storage or visualization.

        Returns:
            Dict[str, Union[str, list]]: A dictionary containing the tools and configurations for
            the selected pipeline. Includes ingestion, storage, processing, and optional visualization details,
            as well as alternate tools for flexibility.

        Example:
            >>> pm = PipelineManager()
            >>> pipeline = pm.get_pipeline("structured", "batch", "dashboard", "yes")
            >>> print(pipeline)
            {
                'Ingestion': 'NiFi',
                'Storage': 'Postgres',
                'Processing': 'Apache Spark',
                'Intermediate Storage': 'Postgres',
                'Visualization': 'Apache Superset',
                'Alternate Structured Storage Tools': ['MySQL', 'Hadoop Standalone'],
                'Alternate Processing Tools': ['Apache Flink'],
                'Orchestration': 'Airflow',
                'Alternate Orchestration': ['Prefect']
            }

        Notes:
            - Adds alternate tools for storage, processing, and orchestration based on the primary tools selected.
            - Designed for both batch and streaming pipelines with support for structured, semi-structured,
              and mixed data types.
        """
        pipelines: Dict[str, Dict] = {
            "batch": {
                "structured": {
                    "storage": {
                        "yes": {
                            'Ingestion': 'NiFi',
                            'Storage': 'Postgres',
                            'Processing': 'Apache Spark',
                            'Intermediate Storage': 'Postgres'
                        },
                        "no": {
                            'Ingestion': 'NiFi',
                            'Storage': 'Postgres'
                        }
                    },
                    "dashboard": {
                        "yes": {
                            'Ingestion': 'NiFi',
                            'Storage': 'Postgres',
                            'Processing': 'Apache Spark',
                            'Intermediate Storage': 'Postgres',
                            'Visualization': 'Apache Superset'
                        },
                        "no": {
                            'Ingestion': 'NiFi',
                            'Storage': 'Postgres',
                            'Visualization': 'Apache Superset'
                        }
                    },
                    "graph": {
                        "yes": {
                            'Ingestion': 'NiFi',
                            'Storage': 'Neo4j',
                            'Processing': 'Apache Spark',
                            'Intermediate Storage': 'Postgres'
                        },
                        "no": {
                            'Ingestion': 'NiFi',
                            'Storage': 'Neo4j',
                            'Processing': 'Apache Spark',
                            'Intermediate Storage': 'Postgres'
                        }
                    }
                },
                "semi-structured": {
                    "storage": {
                        "yes": {
                            'Ingestion': 'NiFi',
                            'Storage': 'Mongo',
                            'Processing': 'Apache Spark',
                            'Intermediate Storage': 'Mongo'
                        },
                        "no": {
                            'Ingestion': 'NiFi',
                            'Storage': 'Mongo'
                        }
                    },
                    "dashboard": {
                        "yes": {
                            'Ingestion': 'NiFi',
                            'Storage': 'Postgres',
                            'Processing': 'Apache Spark',
                            'Intermediate Storage': 'Mongo',
                            'Visualization': 'Apache Superset'
                        },
                        "no": {
                            'Ingestion': 'NiFi',
                            'Storage': 'Postgres',
                            'Processing': 'Apache Spark',
                            'Intermediate Storage': 'Mongo',
                            'Visualization': 'Apache Superset'
                        }
                    },
                    "graph": {
                        "yes": {
                            'Ingestion': 'NiFi',
                            'Storage': 'Neo4j',
                            'Processing': 'Apache Spark',
                            'Intermediate Storage': 'Mongo'
                        },
                        "no": {
                            'Ingestion': 'NiFi',
                            'Storage': 'Neo4j',
                            'Processing': 'Apache Spark',
                            'Intermediate Storage': 'Mongo'
                        }
                    }
                },
                "mixture": {
                    "storage": {
                        "yes": {
                            'Ingestion': 'NiFi',
                            'Structured': 'Postgres',
                            'Semi': 'Mongo',
                            'Processing': 'Apache Spark',
                            'Final Structured': 'Postgres',
                            'Final Semi': 'Mongo'
                        },
                        "no": {
                            'Ingestion': 'NiFi',
                            'Structured': 'Postgres',
                            'Semi': 'Mongo'
                        }
                    },
                    "dashboard": {
                        "yes": {
                            'Ingestion': 'NiFi',
                            'Structured': 'Postgres',
                            'Semi': 'Mongo',
                            'Processing': 'Apache Spark',
                            'Storage': 'Postgres',
                            'Visualization': 'Apache Superset'
                        },
                        "no": {
                            'Ingestion': 'NiFi',
                            'Structured': 'Postgres',
                            'Semi': 'Mongo',
                            'Processing': 'Apache Spark',
                            'Storage': 'Postgres',
                            'Visualization': 'Apache Superset'
                        }
                    },
                    "graph": {
                        "yes": {
                            'Ingestion': 'NiFi',
                            'Structured': 'Postgres',
                            'Semi': 'Mongo',
                            'Processing': 'Apache Spark',
                            'Storage': 'Neo4j'
                        },
                        "no": {
                            'Ingestion': 'NiFi',
                            'Structured': 'Postgres',
                            'Semi': 'Mongo',
                            'Processing': 'Apache Spark',
                            'Storage': 'Neo4j'
                        }
                    }
                }
            },
            "streaming": {
                "structured": {
                    "storage": {
                        "yes": {
                            'Ingestion': 'Apache Kafka',
                            'Processing': 'Apache Flink',
                            'Storage': 'Postgres'
                        },
                        "no": {
                            'Ingestion': 'Apache Kafka',
                            'Storage': 'Postgres'
                        }
                    },
                    "dashboard": {
                        "yes": {
                            'Ingestion': 'Apache Kafka',
                            'Processing': 'Apache Flink',
                            'Storage': 'Postgres',
                            'Visualization': 'Apache Superset'
                        },
                        "no": {
                            'Ingestion': 'Apache Kafka',
                            'Storage': 'Postgres',
                            'Visualization': 'Apache Superset'
                        }
                    },
                    "graph": {
                        "yes": {
                            'Ingestion': 'Apache Kafka',
                            'Storage': 'Neo4j',
                            'Processing': 'Apache Flink'
                        },
                        "no": {
                            'Ingestion': 'Apache Kafka',
                            'Storage': 'Neo4j',
                            'Processing': 'Apache Flink'
                        }
                    }
                },
                "semi-structured": {
                    "storage": {
                        "yes": {
                            'Ingestion': 'Apache Kafka',
                            'Processing': 'Apache Flink',
                            'Storage': 'Mongo'
                        },
                        "no": {
                            'Ingestion': 'Apache Kafka',
                            'Storage': 'Mongo'
                        }
                    },
                    "dashboard": {
                        "yes": {
                            'Ingestion': 'Apache Kafka',
                            'Processing': 'Apache Flink',
                            'Storage': 'Postgres',
                            'Visualization': 'Apache Superset'
                        },
                        "no": {
                            'Ingestion': 'Apache Kafka',
                            'Processing': 'Apache Flink',
                            'Storage': 'Postgres',
                            'Visualization': 'Apache Superset'
                        }
                    },
                    "graph": {
                        "yes": {
                            'Ingestion': 'Apache Kafka',
                            'Storage': 'Neo4j',
                            'Processing': 'Apache Flink'
                        },
                        "no": {
                            'Ingestion': 'Apache Kafka',
                            'Storage': 'Neo4j',
                            'Processing': 'Apache Flink'
                        }
                    }
                },
                "mixture": {
                    "storage": {
                        "yes": {
                            'Ingestion': 'Apache Kafka',
                            'Processing': 'Apache Flink',
                            'Structured': 'Postgres',
                            'Semi': 'Mongo',
                            'Final Structured': 'Postgres',
                            'Final Semi': 'Mongo'
                        },
                        "no": {
                            'Ingestion': 'Apache Kafka',
                            'Structured': 'Postgres',
                            'Semi': 'Mongo'
                        }
                    },
                    "dashboard": {
                        "yes": {
                            'Ingestion': 'Apache Kafka',
                            'Processing': 'Apache Flink',
                            'Storage': 'Postgres',
                            'Visualization': 'Apache Superset'
                        },
                        "no": {
                            'Ingestion': 'Apache Kafka',
                            'Processing': 'Apache Flink',
                            'Storage': 'Postgres',
                            'Visualization': 'Apache Superset'
                        }
                    },
                    "graph": {
                        "yes": {
                            'Ingestion': 'Apache Kafka',
                            'Processing': 'Apache Flink',
                            'Structured': 'Postgres',
                            'Semi': 'Mongo',
                            'Storage': 'Neo4j'
                        },
                        "no": {
                            'Ingestion': 'Apache Kafka',
                            'Structured': 'Postgres',
                            'Semi': 'Mongo',
                            'Storage': 'Neo4j',
                            'Processing': 'Apache Flink'
                        }
                    }
                }
            }
        }
        # Retrieve the pipeline configuration
        pipe = pipelines[nature][data_type][end_goal][transformation]

        # Add alternate tools for flexibility
        if pipe.get("Semi") == "Mongo" or pipe.get("Structured") == "Postgres":
            pipe.update({
                'Alternate Structured Storage Tools': ["MySQL", "Hadoop Standalone"],
                'Alternate Semi-Structured Storage Tools': ["Cassandra", "Hadoop Standalone"]
            })
        if pipe.get("Storage") == "Postgres":
            pipe.update({'Alternate Final Storage Tools': ["MySQL", "Hadoop Standalone"]})
        if pipe.get("Storage") == "Mongo":
            pipe.update({'Alternate Final Storage Tools': ["Cassandra", "Hadoop Standalone"]})
        if pipe.get("Final Structured") == "Postgres":
            pipe.update({'Alternate Final Structured Storage Tools': ["MySQL", "Hadoop Standalone"]})
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

        # Add orchestration options
        pipe.update({'Orchestration': 'Airflow'})
        pipe.update({'Alternate Orchestration': ['Prefect']})

        return pipe
