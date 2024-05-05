from view.homeView import ChatInterface
from model.homeModel import Model
from controller.backend import Backend, ClientWebSocket
from tkinter import *
from pubsub import pub
import logging
from model.event_classes import EventType

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class Controller:
    def __init__(self):  # parent is tkinter main window
        # try:
        self.client = ClientWebSocket("ws://localhost:8000/ws")
        root = Tk()
        self.view = ChatInterface(root)
        
        self.client.attach(EventType.NEW_RESPONSE, self.view)
        
        self.model = Model()
        self.backend = Backend()
        
        pub.subscribe(self.send_to_llm_btn_pressed, "SendToLLM_Button_Pressed")
        
        self.client.start()
        
        root.mainloop()                   
        # except KeyboardInterrupt:
        #     print('Stopping event loop')  
        
        # pub.subscribe(self.addfile_btn_pressed, "AddFile_Button_Pressed")
        pub.subscribe(self.send_to_llm_btn_pressed, "SendToLLM_Button_Pressed")
        # pub.subscribe(self.new_response, "messageReceived")
        
        
    # def addfile_btn_pressed(self):
    #     print("CONTROLLED RECEIVED BUTTON PRESS.\n")
    #     self.model.loadDocument()
    
    def send_to_llm_btn_pressed(self, query):
        # Handler to send a message to the WebSocket server when the new button is pressed
        self.client.send_message(query)
        
    # def new_response(self, response):
    #     self.view.update_response(self.view, response=response)


# if __name__ == "__main__":
#     app = Controller()
