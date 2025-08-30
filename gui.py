import tkinter as tk 
import typing
import threading

class GuiWindow:

    def __init__(self, closingCallback: typing.Callable = None):
        
        self.createWidgets()

        self.closingCallback = closingCallback

        self.root.protocol('WM_DELETE_WINDOW', lambda: self.onClosing(self.closingCallback))

    def runMainWindow(self):
        self.layoutWindowWidgets()
        self.root.mainloop()

    def createWidgets(self):        
        self.root = tk.Tk()
        self.root.title('Minecraft Easy Server')
        self.root.minsize(600, 400) # set minimum window size

        # === Widgets ===

        # Create analytics frame
        self.analyticsFrame = tk.Frame(self.root, padx=10, pady=0)
        self.analyticsFrameTitle = tk.Label(self.analyticsFrame, text="Analytics", padx=10, pady=5)

        self.outputTextWindow = tk.Text(self.root, state="disabled")
        self.run_stopButton = tk.Button(self.root, text='Run', width=30)

        # === END Widgets ===

    def layoutWindowWidgets(self):
        # Configure rows/columns expanding
        self.root.rowconfigure(0, weight=1) # ID, Should widget resize: 0 = no resize, 1 = resize
        self.root.rowconfigure(1, weight=0) # row 1 (button row) stays fixed
        self.root.columnconfigure(0, weight=0) # column 0 (title) fixed width
        self.root.columnconfigure(1, weight=1) # column 1 (output box) expands horizontally

        # organize widgets on GUI
        self.analyticsFrame.grid(row=0, column=0, sticky="n")
        self.analyticsFrameTitle.grid(row=0, column=0)

        #self.titleLabel.grid(row=0, column=0)
        self.outputTextWindow.grid(row=0, column=1, sticky="nsew")
        self.run_stopButton.grid(row=1, column=1)

    def printOutput(self, text :str):
        self.outputTextWindow.config(state="normal") # allow code to insert
        self.outputTextWindow.insert(tk.END, text)
        self.outputTextWindow.see(tk.END) # scroll to the end
        self.outputTextWindow.config(state="disabled") # read-only no typing allowed

    def onClosing(self, callback: typing.Callable):
        if callback:
            callback()
        else:
            self.root.destroy()

