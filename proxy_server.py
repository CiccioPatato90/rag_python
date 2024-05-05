from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import requests
import json
import logging

# Set up logging
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)

app = FastAPI()


class ConnectionManager:
    """Class defining socket events"""
    def __init__(self):
        """init method, keeping track of connections"""
        self.active_connections = []
    
    async def connect(self, websocket: WebSocket):
        """connect event"""
        await websocket.accept()
        self.active_connections.append(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        """Direct Message"""
        await websocket.send_text(message)
    
    def disconnect(self, websocket: WebSocket):
        """disconnect event"""
        self.active_connections.remove(websocket)
        
        
manager = ConnectionManager()


@app.websocket("/")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            query = await websocket.receive_text()  # Receive queries from the client
            # Process the query and send responses

            # Define the Ollama endpoint and the request payload
            ollama_endpoint = (
                "http://ollama-api:11434/api/generate"  # Note the container name
            )
            payload = {
                "model": "api-model:latest",
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
            await manager.send_personal_message(return_message)
            
    except WebSocketDisconnect as e:
        # Handle WebSocket disconnects
        print("WebSocket disconnected:", e)
        await manager.send_personal_message(f"Bye!!")
    except Exception as e:
        await manager.send_personal_message(f"WebSocket error: {e}")
