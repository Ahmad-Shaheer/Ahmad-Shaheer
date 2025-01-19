from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
import requests

class ChatBotState(TypedDict):
    prompt: str
    response: str
    headers: dict
    ollama_url: str
    request_data: dict

class ChatBotAgent:
    def __init__(self):
        """
        Initializes the ChatBotAgent by defining the state and building the graph.
        """
        self.graph = StateGraph(ChatBotState)
        self.graph.add_node("PrepareRequest", self._prepare_request)
        self.graph.add_node("SendRequest", self._send_request)

        self.graph.add_edge(START, "PrepareRequest")
        self.graph.add_edge("PrepareRequest", "SendRequest")
        self.graph.add_edge("SendRequest", END)

        self.compiled_chatbot = self.graph.compile()

    def _prepare_request(self, state: ChatBotState) -> ChatBotState:
        """
        Prepares the request data for the chatbot API.
        """
        ollama_config = {
            "model": "llama3.1:8b-instruct-fp16",
            "max_tokens": 8192,
            "host": "172.16.19.80:11300"
        }
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

        state['request_data'] = {
            "model": ollama_config["model"],
            "max_tokens": ollama_config["max_tokens"],
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": state['prompt']}
            ],
            "stream": False,
            "options": {"temperature": 0.1}
        }
        state['headers'] = {"Content-Type": "application/json"}
        state['ollama_url'] = f"http://{ollama_config['host']}/api/chat/"
        return state

    def _send_request(self, state: ChatBotState) -> ChatBotState:
        """
        Sends the request to the chatbot API and retrieves the response.
        """
        response = requests.post(
            url=state['ollama_url'],
            json=state['request_data'],
            headers=state['headers']
        ).json()
        state['response'] = response['message']['content']
        return state

    def _invoke(self, initial_state: ChatBotState) -> ChatBotState:
        """
        Invokes the compiled chatbot graph with the given initial state.

        Args:
            initial_state (ChatBotState): The initial state to pass through the graph.

        Returns:
            ChatBotState: The final state after processing.
        """
        return self.compiled_chatbot.invoke(initial_state)

    def get_response(self, prompt: str) -> str:
        """
        Generates a response from the chatbot based on the user prompt.

        Args:
            prompt (str): The user input prompt.

        Returns:
            str: The chatbot response.
        """
        initial_state = ChatBotState(
            prompt=prompt,
            response="",
            headers={},
            ollama_url="",
            request_data={}
        )
        result = self._invoke(initial_state)
        return result['response']

# Example usage
if __name__ == "__main__":
    chatbot_agent = ChatBotAgent()
    user_input = "What is the best tool for batch data processing?"
    result = chatbot_agent.get_response(user_input)
    print(result)
