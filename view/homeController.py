# from model.homeModel import homeModel
from homeView import View
from homeModel import Model
from backend import Backend
from tkinter import *
from pubsub import pub
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class Controller:
    def __init__(self):  # parent is tkinter main window
        self.model = Model()
        self.backend = Backend()
        pub.subscribe(self.addfile_btn_pressed, "AddFile_Button_Pressed")

        self.view = View()

    def addfile_btn_pressed(self):
        print("CONTROLLED RECEIVED BUTTON PRESS.\n")
        self.model.loadDocument()


if __name__ == "__main__":
    app = Controller()
