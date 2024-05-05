import chromadb
from chromadb.utils import embedding_functions
import chromadb
from socket import *
from threading import *
import logging
from pubsub import pub

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

import asyncio
import websockets

from chromadb.utils import embedding_functions
import threading
from model.event_classes import ConcreteSubject, EventType, State
        
  
  
# class ClientWebSocket:
#     def __init__(self, uri, queue):
#         self.queue = queue
#         self.uri = uri
#         self.loop = asyncio.new_event_loop()
#         threading.Thread(target=self.start_loop, daemon=True).start()
#         self.connected = asyncio.Event()

#     def start_loop(self):
#         asyncio.set_event_loop(self.loop)
#         self.loop.run_forever()

#     async def connect(self):
#         try:
#             self.websocket = await websockets.connect(self.uri)
#             self.connected.set()  # Signal that the connection is established
#             logging.info("WebSocket initialized successfully.")
#             asyncio.create_task(self.listen())
#             asyncio.create_task(self.process_queue())
#         except Exception as e:
#             logging.error(f"WebSocket failed to initialize: {e}")

#     async def listen(self):
#         while True:
#             message = await self.websocket.recv()
#             logging.info(f"Received: {message}")

#     async def process_queue(self):
#         while True:
#             if self.connected.is_set():
#                 try:
#                     message = self.queue.get()
#                     await self.websocket.send(message)
#                     logging.info(f"Sent message: {message}")
#                 except queue.Empty:
#                     continue
#             else:
#                 await asyncio.sleep(0.1)  # Sleep briefly to avoid a tight loop

#     def send_message(self, message):
#         if not self.connected.is_set():
#             logging.error("WebSocket is not connected.")
#             return
#         self.loop.call_soon_threadsafe(asyncio.create_task, self.websocket.send(message))
#         logging.info(f"Queued message for sending: {message}")

#     def start(self):
#         asyncio.run_coroutine_threadsafe(self.connect(), self.loop)
        
      
class ClientWebSocket(ConcreteSubject):
    def __init__(self, uri):
        self.uri = uri
        self.loop = asyncio.new_event_loop()
        threading.Thread(target=self.start_loop, daemon=True).start()
        self.connected = asyncio.Event()
        self._state = State()

    def start_loop(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()

    async def connect(self):
        try:
            self.websocket = await websockets.connect(self.uri)
            self.connected.set()  # Signal that the connection is established
            logging.info("WebSocket initialized successfully.")
            self._state.connected = True
            asyncio.create_task(self.listen())
        except Exception as e:
            self._state.connected = False
            logging.error(f"WebSocket failed to initialize: {e}")

    async def listen(self):
        while True:
            message = await self.websocket.recv()
            self.update_state(last_response=message)
            self.notify(EventType.NEW_RESPONSE)
            # pub.sendMessage("messageReceived", response=message)
            logging.info(f"Received: {message}")

    def send_message(self, message):
        if not self.connected.is_set():
            logging.error("WebSocket is not connected.")
            return
        message_prompted = self.build_prompt(message)
        self.loop.call_soon_threadsafe(asyncio.create_task, self.websocket.send(message_prompted))
        logging.info(f"Queued message for sending: {message}")

    def start(self):
        asyncio.run_coroutine_threadsafe(self.connect(), self.loop)
        
    def build_prompt(self, message):
        return f"""You are an AI assistant and this is the initialization message to check if you are up and ready to receive new requests.
                    Please answer by mirroring the same message you receive. This is the message: {message}"""


    def update_state(self, last_query=None, last_response=None):
        """
        Update the state object with a new query or response.
        """
        if last_query is not None:
            self._state.last_query = last_query
        if last_response is not None:
            self._state.last_response = last_response
    
class Backend:
    def __init__(self):
        try:
            device = "cpu"
            self.embedding_model = (
                embedding_functions.SentenceTransformerEmbeddingFunction(
                    model_name="all-mpnet-base-v2", device=device
                )
            )
            self.clientDb = chromadb.PersistentClient(path="../../vectore_store")
        except Exception as e:
            # Handle any exception
            print(f"EXPECTION BACKEND: {e}")
            raise
    def count_collection(collection):
        try:
            # Code that might cause an exception
            return collection.count()
        except Exception as e:
            # Handle any exception
            print(f"!!!Count collections error!!!: {e}")
