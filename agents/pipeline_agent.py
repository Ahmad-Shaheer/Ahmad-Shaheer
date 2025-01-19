from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END

class PipelineState(TypedDict):
    data_type: str
    nature: str
    end_goal: str
    transformation: str
    pipeline: dict

class PipelineAgent:
    def __init__(self):
        """
        Initializes the PipelineAgent by defining the state and building the graph.
        """
        self.graph = StateGraph(PipelineState)
        self.graph.add_node("RetrievePipeline", self._retrieve_pipeline)
        self.graph.add_edge(START, "RetrievePipeline")
        self.graph.add_edge("RetrievePipeline", END)

        self.compiled_pipeline = self.graph.compile()

    def _retrieve_pipeline(self, state: PipelineState) -> PipelineState:
        """
        Retrieves the pipeline configuration based on the state values.
        """
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
        # Retrieve the pipeline configuration
        pipe = pipelines[state['nature']][state['data_type']][state['end_goal']][state['transformation']]

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

        state['pipeline'] = pipe
        return state

    def _invoke(self, initial_state: PipelineState) -> PipelineState:
        """
        Invokes the compiled pipeline graph with the given initial state.

        Args:
            initial_state (PipelineState): The initial state to pass through the graph.

        Returns:
            PipelineState: The final state after processing.
        """
        return self.compiled_pipeline.invoke(initial_state)

    def get_pipeline(self, data_type: str, nature: str, end_goal: str, transformation: str) -> dict:
        """
        Generates a pipeline configuration based on the given parameters.

        Args:
            data_type (str): Type of data to process.
            nature (str): Nature of the pipeline (batch/streaming).
            end_goal (str): Purpose of the pipeline (storage/dashboard/graph).
            transformation (str): Whether transformations are required.

        Returns:
            dict: The generated pipeline configuration.
        """
        initial_state = PipelineState(
            data_type=data_type,
            nature=nature,
            end_goal=end_goal,
            transformation=transformation,
            pipeline={}
        )
        result = self._invoke(initial_state)
        return result['pipeline']

# Example usage
if __name__ == "__main__":
    pipeline_agent = PipelineAgent()
    pipeline = pipeline_agent.get_pipeline("structured", "batch", "dashboard", "yes")
    print(pipeline)
