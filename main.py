import threading
from miner import Minerman
from gui import GuiWindow

theGui = GuiWindow()
theMine = Minerman()

mainThread = threading.Thread(target=theMine.mainLoop, args=(theGui,))
mainThread.start()
theGui.mainWindow()