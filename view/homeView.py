import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import backend as be
from pubsub import pub


class View:
    def __init__(self):
        App("Local Rag Python", (1000, 600))

    # initialize variables

    # def setup(): # run first
    # 	"""Calls methods to setup the user interface."""


class App(ttk.Window):
    def __init__(self, title, size):
        # main setup
        super().__init__(themename="darkly")
        self.title(title)
        self.geometry(f"{size[0]}x{size[1]}")
        self.minsize(size[0], size[1])

        # widgets
        self.menu = Menu(self)
        self.main = Main(self)

        # run
        self.mainloop()


class Menu(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.place(x=0, y=0, relwidth=0.2, relheight=1)

        self.create_widgets()

    def create_widgets(self):

        # create the widgets
        menu_button1 = ttk.Button(self, text="Edit Collections", bootstyle="success")
        menu_button2 = ttk.Button(self, text="Button 2", bootstyle="secondary")
        menu_button3 = ttk.Button(self, text="Button 3", bootstyle="secondary")

        # create the grid
        self.columnconfigure((0, 1), weight=1, uniform="a")
        self.rowconfigure((tuple(range(20))), weight=1, uniform="a")

        # place the widgets
        menu_button1.grid(row=0, column=0, sticky="nswe", columnspan=2)
        menu_button2.grid(row=1, column=0, sticky="nswe", columnspan=2)
        menu_button3.grid(row=2, column=0, sticky="nswe", columnspan=2)


class Main(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.place(relx=0.2, y=0, relwidth=0.8, relheight=1)
        Entry(self, "What can I help you with today?", "Search", "green", self.queryLLM)
        Entry(self, "", "Add document", "purple", self.loadDocument)
        # self.after(100, self.connect_to_db)

    def loadDocument(self):
        print("load document method!")
        pub.sendMessage("AddFile_Button_Pressed")

    def queryLLM(self):
        print("queryLLM method!")

    # def connect_to_db(self):
    # 	collection = be.initialize_db_connection()
    # 	if collection is not None:
    # 		# Show a success message
    # 		InfoMessage(self, "Successfully connected to the vector database!", SUCCESS)
    # 	else:
    # 		# Show an error message
    # 		InfoMessage(self, "Failed to connect to the vector database.", DANGER)


class Entry(ttk.Frame):
    def __init__(self, parent, label_text, button_text, label_background, commandArgs):
        super().__init__(parent)
        if label_text != "":
            entry = ttk.Entry(
                self,
                font=("Helvetica", 20),
            )
            entry.pack(expand=False, fill="both")
        if button_text != "":
            if commandArgs != "":
                button = ttk.Button(self, text=button_text, command=commandArgs)
            else:
                button = ttk.Button(self, text=button_text)
            button.pack(expand=False, fill="both", pady=10)

        self.pack(side="left", expand=True, fill="both", padx=20, pady=20)


# Custom Info Message Frame
class InfoMessage(ttk.Frame):
    def __init__(self, parent, message, status):
        super().__init__(parent)

        # Background color based on status
        bg_color = "green" if status == SUCCESS else "red"

        # Icon (could be replaced with an actual image or symbol)
        icon = ttk.Label(
            self, text="●", foreground=bg_color
        )  # Using a dot for simplicity

        # Label for the message
        label = ttk.Label(self, text=message)

        # Pack the icon and label horizontally
        icon.pack(side="left", padx=5)
        label.pack(side="left")

        # Pack the whole frame
        self.pack(fill="x", padx=10, pady=5)


# Main Tkinter App
if __name__ == "__main__":
    App("Local Rag Python", (1000, 600))
