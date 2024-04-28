from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import requests
import json
import logging

# Set up logging
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)

app = FastAPI()
connected = True


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while connected:
            query = await websocket.receive_text()  # Receive queries from the client
            # Process the query and send responses

            # Define the Ollama endpoint and the request payload
            ollama_endpoint = (
                "http://ollama-api:11434/api/generate"  # Note the container name
            )
            payload = {
                "model": "tinyllama",
                "stream": False,
                "prompt": query,
            }

            # Send the request to Ollama
            response = requests.post(
                ollama_endpoint,
                data=json.dumps(payload),
                headers={"Content-Type": "application/json"},
            )

            # Send the response back to the WebSocket client
            if response.status_code == 200:
                result = json.loads(response.text)
                return_message = result["response"]
            else:
                return_message = f"Error: {response.status_code}, {response.text}"

            await websocket.send_text(return_message)

    except WebSocketDisconnect as e:
        # Handle WebSocket disconnects
        print("WebSocket disconnected:", e)
    except Exception as e:
        await websocket.send_text(f"WebSocket error: {e}")
