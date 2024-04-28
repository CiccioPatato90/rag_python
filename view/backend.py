import chromadb
from chromadb.utils import embedding_functions
import chromadb
import logging
import json
import requests

from chromadb.utils import embedding_functions

client = None  # Initialized to None


class Backend:
    def __init__(self):
        try:
            device = "cpu"
            self.embedding_model = (
                embedding_functions.SentenceTransformerEmbeddingFunction(
                    model_name="all-mpnet-base-v2", device=device
                )
            )
            self.client = chromadb.PersistentClient(path="../../vectore_store")
            # self.init_websocket_connection()

        except Exception as e:
            # Handle any exception
            print(f"EXPECTION BACKEND: {e}")
            raise

    # def init_websocket_connection(self):
    #     pass

    def query_llm(self, query):
        logging.info(f"Querying LLM")
        # Endpoint for the Ollama service
        ollama_endpoint = "http://localhost:11434/api/generate"

        # Define the request payload
        payload = {
            "model": "tinyllama",
            "stream": False,
            "prompt": f"{query}",
        }

        logging.info(f"Sending request")
        # Send the request
        response = requests.post(
            ollama_endpoint,
            data=json.dumps(payload),
            headers={"Content-Type": "application/json"},
        )

        # Check the response
        if response.status_code == 200:
            logging.info(f"Received response")
            output = json.loads(response.text)
            print(output["response"] + "\n")
        else:
            print("Error:", response.status_code, response.text)

    def count_collection(collection):
        try:
            # Code that might cause an exception
            return collection.count()
        except Exception as e:
            # Handle any exception
            print(f"!!!Count collections error!!!: {e}")
