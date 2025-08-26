import tkinter

class GuiWindow:

    def __init__(self):
        self.root = tkinter.Tk()
        self.root.title('Minecraft Easy Server')
        self.title=tkinter.Label(self.root, text="Minecraft Easy Server")
        self.output = tkinter.Text(self.root)
        self.button = tkinter.Button(self.root, text='ACHTUNG!', width=30, command=self.root.destroy)

    def mainWindow(self):
        self.title.pack()
        self.output.pack()
        self.button.pack()

        self.root.mainloop()

    def printOutput(self, text :str):
        self.output.insert(tkinter.END, text)


