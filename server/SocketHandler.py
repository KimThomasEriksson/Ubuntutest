import socket
import _thread
import sys
from server.Users import CollectionOfUsers

class SocketHandler:
    def __init__(self):
        self.serverSocket= socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.users = CollectionOfUsers()
        self.users.readUsersFromFile()
##Gör objet av GUI
    def setGuiHandler(self,guiHandler_):
        self.guiHandler = guiHandler_
##Stänger allt
    def closeEveryThing(self):
        self.serverSocket.close()
        self.users.writeUsersToFile()
        sys.exit(0)
#Börjat acceptera connection och startar lyssnar tråd samt lägger dem i en lista
    def startAccepting(self):
        while True:
            try:
                clientSocket, clientAddr = self.serverSocket.accept()
                self.list_of_unknown_clientSockets.append(clientSocket)
                self.list_of_unknown_clientAddr.append(clientAddr)
                self.startReceiverThread(clientSocket, clientAddr)

            except:
                pass
#binder ip ocj port man fått från gui samt startar gör listor
    def startToAcceptConnection(self,port):
        try:
            self.serverSocket.bind(('',int(port)))
        except:
            return "failed"
        self.serverSocket.listen()

        self.list_of_known_clientSockets = []
        self.list_of_known_clientAddr = []

        self.list_of_unknown_clientSockets = []
        self.list_of_unknown_clientAddr = []

        _thread.start_new_thread(self.startAccepting,())
        return "succeed"
#Skickar meddelande till alla som inte loggat in HHAHA Nafwal här kan man komma in om man e ruskigt snabb :D
    def sendAndShowMsg(self, text):
        self.guiHandler.showMessage(text)
        for clientSock in self.list_of_known_clientSockets:
            clientSock.send(str.encode(text))
#startar tråd för att ta imot
    def startReceiverThread(self, clientSocket, clientAddr):
        _thread.start_new_thread(self.startReceiving,(clientSocket,clientAddr,))
#här är vad tråden vi skapat ska göra, om man man lyckades logga in så ska läggs ens namn till i listan av users som är kända(inloggade) samt lägger till den i kända clienterlisten
    def startReceiving(self,clientSocket, clientAddr):
        resultOfLogin = self.listenToUnknownClinet(clientSocket,clientAddr)

        if resultOfLogin !=False:
            username = resultOfLogin
            self.list_of_unknown_clientSockets.remove(clientSocket)
            self.list_of_unknown_clientAddr.remove(clientAddr)

            self.list_of_known_clientSockets.append(clientSocket)
            self.list_of_known_clientAddr.append(clientAddr)

            self.listenToknownClinet(clientSocket,clientAddr,username)
#function för folk som inte loggat in men försöker logga in om allt går rätt till. även functionen som registrerar ett konto
    def listenToUnknownClinet(self,clientSocket, clientAddr):
        while True:
            try:
                msg = clientSocket.recv(1024).decode()
            except:
                self.list_of_unknown_clientSockets.remove(clientSocket)
                self.list_of_unknown_clientAddr.remove(clientAddr)
                return False

            args = msg.split(' ')
            if len(args) == 3 and args[0] == "login":
                username = args[1]
                password = args[2]
                if self.users.doesThisUserExistAndNotActive(username,password):
                    clientSocket.send(str.encode("ok"))
                    self.sendAndShowMsg(username + " is connected")
                    return username
                else:
                    clientSocket.send(str.encode("not ok"))

            if len(args) >= 5 and args[0] == "register":
                username = args[1]
                password = args[2]
                email = args[3]
                name = ""
                for rest in args[4:]:
                    name += rest + " "
                if username != "" and password != "" and email != "" and name != "":
                    resultOfAdding = self.users.add_user(username,password,email,name)
                    if resultOfAdding == True:
                        clientSocket.send(str.encode("fine"))
                    else:
                        clientSocket.send(str.encode("not fine"))
                else:
                    clientSocket.send(str.encode("not fine"))
##tråd som lyssnar på alla som loggat in och och skickar medelandet till dem som har connectat till servern
    def listenToknownClinet(self,clientSocket, clientAddr,username):
        while True:
            try:
                msg = clientSocket.recv(1024).decode()
                self.sendAndShowMsg(username + ": " + msg)
            except:
                self.list_of_known_clientSockets.remove(clientSocket)
                self.list_of_known_clientAddr.remove(clientAddr)
                self.sendAndShowMsg(username+" disconnected")
                self.users.inactiveUser(username)
                return
