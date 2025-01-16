import requests
import json

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

class ChatInferenceManager:
    """
    Manages the inference/chat logic using the 'infer()' method.
    Preserves the original function signature and logic.
    """

    def infer(self, system, prompt):
        """
        Equivalent to the original infer() function.
        """
        ollama_config = {
            "model": "llama3.1:8b-instruct-fp16",
            "max_tokens": 8192,
            "host": "172.16.19.80:11300"
        }

        data = {
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

        headers = {
            "Content-Type": "application/json"
        }
        ollama_url = f"http://{ollama_config['host']}/api/chat/"

        model_response = requests.post(
            url=ollama_url,
            json=data,
            headers=headers
        ).json()

        return model_response['message']['content']
