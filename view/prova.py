import tkinter as tk
import asyncio
import websockets
import threading
import queue
import logging

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


class WebSocketClientApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tkinter WebSocket Client")
        self.geometry("300x200")

        # Widgets for the GUI
        self.message_label = tk.Label(self, text="Not connected")
        self.message_label.pack(pady=10)

        self.query_entry = tk.Entry(self)
        self.query_entry.pack(pady=10)

        self.query_button = tk.Button(
            self, text="Send Query", command=self.send_query, state="disabled"
        )
        self.query_button.pack(pady=10)

        self.connect_button = tk.Button(
            self, text="Connect", command=self.start_websocket_thread
        )
        self.connect_button.pack(pady=10)

        self.disconnect_button = tk.Button(
            self, text="Disconnect", command=self.close_websocket, state="disabled"
        )
        self.disconnect_button.pack(pady=10)

        # Thread-safe queue for communication between asyncio and Tkinter
        self.queue = queue.Queue()

        # Variables to keep track of the WebSocket and the event loop thread
        self.websocket = None
        self.event_loop_thread = None

        # Periodically check the queue for updates
        self.after(100, self.process_queue)

    def start_websocket_thread(self):
        logging.debug("Starting WebSocket thread")
        if self.event_loop_thread and self.event_loop_thread.is_alive():
            logging.warning("WebSocket thread is already running")
            return

        self.event_loop_thread = threading.Thread(target=self.run_event_loop)
        self.event_loop_thread.start()

        # Update button states
        self.connect_button.config(state="disabled")
        self.disconnect_button.config(state="normal")
        self.query_button.config(state="normal")

        logging.info("WebSocket thread started")

    def run_event_loop(self):
        logging.debug("Creating new asyncio event loop")
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.connect_to_websocket())
        loop.close()  # Properly close the event loop
        logging.info("Asyncio event loop running")

    async def connect_to_websocket(self):
        uri = "ws://localhost:8000/ws"
        try:
            logging.info("Connecting to WebSocket")
            self.websocket = await websockets.connect(uri)
            await self.websocket.send("Hello from Tkinter")
            logging.info("Connected to WebSocket")
            while self.websocket.open:
                response = await self.websocket.recv()  # Receive responses
                logging.debug(f"Received response: {response}")
                self.queue.put(response)  # Store in the queue for Tkinter
        except Exception as e:
            logging.error(f"Error in WebSocket connection: {e}")
        finally:
            if self.websocket and not self.websocket.closed:
                await self.websocket.close()
                logging.info("WebSocket connection closed")

    def send_query(self):
        query = self.query_entry.get()  # Get the query from the Tkinter entry
        if self.websocket and self.websocket.open:
            logging.debug(f"Sending query: {query}")
            asyncio.run_coroutine_threadsafe(
                self.websocket.send(query), asyncio.get_event_loop()
            )
        else:
            logging.warning("Cannot send query, WebSocket is closed")

    def close_websocket(self):
        if self.websocket and self.websocket.open:
            logging.info("Closing WebSocket connection")
            asyncio.run_coroutine_threadsafe(
                self.websocket.close(), asyncio.get_event_loop()
            )  # Close asynchronously
            self.disconnect_button.config(state="disabled")
            self.connect_button.config(state="normal")
            self.query_button.config(state="disabled")

    def process_queue(self):
        while not self.queue.empty():
            message = self.queue.get()
            logging.debug(f"Processing queue message: {message}")
            self.message_label.config(text=message)

        self.after(100, self.process_queue)  # Re-check the queue every 100 ms


if __name__ == "__main__":
    app = WebSocketClientApp()
    try:
        app.mainloop()
    finally:
        if app.event_loop_thread and app.event_loop_thread.is_alive():
            asyncio.run_coroutine_threadsafe(
                app.websocket.close(), asyncio.get_event_loop()
            )
            app.event_loop_thread.join()  # Ensure the event loop thread is properly closed
