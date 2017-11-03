import socket
import _thread

class SocketHandler:
    def __init__(self):
        self.clientSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    def setGuiHandler(self,guiHandler_):
        self.guiHandler = guiHandler_
##Testar att skapa socket
    def connect(self,ip, port):
        try:
            self.clientSocket.connect((ip,int(port)))
            self.startReceiverThread()
        except:
            return "no connection"
#Function som sänder text till servern
    def sendMsg(self,text):
        try:
            self.clientSocket.send(str.encode(text))
        except:
            pass
#startar ny tråd för att taimot meddelande
    def startReceiverThread(self):
        _thread.start_new_thread(self.startReceiving,())
#tråden vi just skapat ska göra detta
    def startReceiving(self):
        while True:
            try:
                msg = self.clientSocket.recv(1024).decode()
                self.guiHandler.showMessage(msg)
            except:
                self.guiHandler.showMessage("desconnected...")
                return