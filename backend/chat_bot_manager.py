import requests
import json
from typing import Dict


SYSTEM_PROMPT = """
"You are a virtual assistant designed to guide users in planning and deploying their data pipelines. Your role is to help users make informed decisions based on their data type, processing needs, and end goals.

Your key functions include:

Providing practical recommendations for tools, frameworks, and strategies to process, transform, and store their data.
Explaining concepts in simple terms without unnecessary technical jargon unless explicitly requested.
Addressing common queries about data formats (e.g., CSV, JSON), data processing methods (batch or streaming), and pipeline tools (e.g., ETL, Apache Kafka).
Considerations:

Adapt recommendations based on user inputs, such as the nature of their data (structured, semi-structured, or mixed), their processing goals (storage, analytics, or graph-based databases), and whether transformations are needed.
Offer suggestions for both beginner-friendly and advanced tools depending on the user's expertise.
Maintain a concise, professional, and helpful tone throughout the conversation.
Tone Instructions:
YOU ARE NOT VERBOSE, your response should be at maximum 4 sentences
Formality: Use polite language with slight formality (e.g., "Please let us know," "We are happy to assist").
Clarity: Avoid technical jargon unless necessary.
Example: "Thank you for reaching out! Please let us know if you need further assistance."
"""


class ChatBotManager:
    """
    Manages the inference/chat logic for interacting with a language model.

    This class allows users to send prompts and receive responses from a virtual assistant 
    tailored to guide users in planning and deploying data pipelines.

    Attributes:
        ollama_config (Dict[str, Union[str, int]]): A configuration dictionary specifying
            model details, maximum tokens, and the host address for the language model.
    """

    def infer(self, system: str, prompt: str) -> str:
        """
        Sends a prompt to the language model and retrieves the response.

        Args:
            system (str): The system role definition or guidelines for the assistant.
                          This defines the behavior and tone of the assistant.
            prompt (str): The user's prompt or query that will be sent to the model.

        Returns:
            str: The content of the model's response to the user's query.

        Example:
            >>> manager = ChatBotManager()
            >>> system_prompt = "You are an assistant helping users with data pipelines."
            >>> user_prompt = "What is the best way to process JSON files?"
            >>> response = manager.infer(system_prompt, user_prompt)
            >>> print(response)
            "The best way to process JSON files is to use tools like Apache Spark for scalability 
            or Python's pandas for smaller datasets."

        Raises:
            requests.exceptions.RequestException: If there is an issue with the HTTP request.
            KeyError: If the response JSON does not contain the expected 'message' key.
        """
        ollama_config: Dict[str, str | int] = {
            "model": "llama3.1:8b-instruct-fp16",
            "max_tokens": 8192,
            "host": "172.16.19.80:11300"
        }

        data: Dict = {
            "model": ollama_config["model"],
            "max_tokens": ollama_config["max_tokens"],
            "messages": [
                {
                    "role": "system",
                    "content": system
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "stream": False,
            "options": {
                "temperature": 0.1
            }
        }

        headers: Dict[str, str] = {
            "Content-Type": "application/json"
        }
        ollama_url: str = f"http://{ollama_config['host']}/api/chat/"

        model_response = requests.post(
            url=ollama_url,
            json=data,
            headers=headers
        ).json()

        return model_response['message']['content']
