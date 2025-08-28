import tkinter, typing, threading

class GuiWindow:

    def __init__(self, closingCallback: typing.Callable = None):
        
        self.createWidgets()

        self.closingCallback = closingCallback

        self.root.protocol('WM_DELETE_WINDOW', lambda: self.onClosing(self.closingCallback))

    def runMainWindow(self):
        self.layoutWindowWidgets()

        self.root.mainloop()

    def createWidgets(self):
        self.root = tkinter.Tk()
        self.root.title('Minecraft Easy Server')
        self.title=tkinter.Label(self.root, text="Minecraft Easy Server")
        self.output = tkinter.Text(self.root)
        self.button = tkinter.Button(self.root, text='Run', width=30)

    def layoutWindowWidgets(self):
        self.title.grid(row=0, column=0)
        self.output.grid(row=0, column=1)
        self.button.grid(row=1, column=0, columnspan=2)

    def printOutput(self, text :str):
        self.output.insert(tkinter.END, text)

    def onClosing(self, callback: typing.Callable):
        if callback:
            callback()
        else:
            exit(0)

