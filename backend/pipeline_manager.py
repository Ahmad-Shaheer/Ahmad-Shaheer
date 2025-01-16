class PipelineManager:
    """
    Manages pipeline selection and configuration.
    Preserves the original get_pipeline() function logic.
    """

    def get_pipeline(self, data_type, nature, end_goal, transformation):
        pipelines = {
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

        pipe = pipelines[nature][data_type][end_goal][transformation]

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

        pipe.update({'Orchestration': 'Airflow'})
        pipe.update({'Alternate Orchestration': ['Prefect']})

        return pipe
