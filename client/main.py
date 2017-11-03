from client.GuiHandler import GuiHandler
from client.SocketHandler import SocketHandler
#Startar socket
socketHandler = SocketHandler()
#Skickar socket till gui
guiHandler = GuiHandler(socketHandler)
#gör objekt av gui+socket
socketHandler.setGuiHandler(guiHandler)
#får ip och port från input i gui
ip,port = guiHandler.getIpAndPort()

#testar connecta om det inte går får man message"server is not found" annars connectar den och startar recivertråden och GUI
resultOfConnection = socketHandler.connect(ip,port)
if resultOfConnection == "no connection":
    guiHandler.showWarningMsg()
else:
    guiHandler.startGui()