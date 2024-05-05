from tkinter.filedialog import askopenfilename

class Model:
    def __init__(self):
        return 
    
    def loadDocument(self): #loadDocument and create embeddings
        path= askopenfilename(initialdir="./",
                       filetypes=[("Image File", "*.jpg"),("All Files","*.*")],
                        title = "Choose a file."
        )
        print (path)
        return 