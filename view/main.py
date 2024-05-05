# main.py
from view.homeView import ChatInterface
from model.homeModel import Model
from controller.backend import Backend, ClientWebSocket
from tkinter import *
from pubsub import pub
import logging
from model.event_classes import EventType

import logging
from controller.homeController import Controller

class Main():
    # Configure logging if needed
    logging.basicConfig(level=logging.INFO)
    def __init__(self):
        # Create and start the application using the Controller class
        self.controller = Controller()
        


if __name__ == "__main__":
    app = Main()
