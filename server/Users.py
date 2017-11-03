
class User:
    def __init__(self,username_,password_,email_,name_):
        self.username = username_
        self.password = password_
        self.email = email_
        self.name = name_
        self.activeInChat = False
#kollar om lösenord och username stämmer
    def isTheUser(self,username_,password_):
        if password_ == self.password and username_ == self.username:
            return True
        else:
            return False
#lista med alla users
class CollectionOfUsers:
    def __init__(self):
        self.list_of_users = []
#registrerar ny användare och kollar om det redan finns ett username som stämmer med detta samt lägger till den i listan av users
    def add_user(self,username_,password_,email_,name_):
        usernameExists = False
        for user in self.list_of_users:
            if user.username == username_:
                usernameExists = True
                break
        if usernameExists == True:
            return False
        else:
            user = User(username_,password_,email_,name_)
            self.list_of_users.append(user)
            return True

#kollar om kontot man försöker logga in på finns och kollar så den inte är online
    def doesThisUserExistAndNotActive(self,username_,password_):
        for user in self.list_of_users:
            if user.isTheUser(username_,password_):
                if user.activeInChat == False:
                    user.activeInChat = True
                    return True
                else:
                    return False
        return False
#någon loggar ut
    def inactiveUser(self,usernameToInactive):
        for user in self.list_of_users:
            if user.username == usernameToInactive:
                user.activeInChat = False
#tabort en user
    def remove_user(self,username_):
        for i in range(self.list_of_users):
            if self.list_of_users[i].username == username_:
                self.list_of_users.pop(i)
                return True

        return False
#söker upp username i listan
    def getUserObjByUsername(self,username_):
        for i in range(self.list_of_users):
            if self.list_of_users[i].username == username_:
                return self.list_of_users[i]

        return "non"
#läseer in filerna
    def readUsersFromFile(self):
        try:
            file = open("users.txt",'r')
            allLines = file.read().split('\n')
            file.close()
        except:
            return False

        index_of_current_line = 0

        while True:
            username = allLines[index_of_current_line]
            index_of_current_line+=1
            if username == "":
                return True

            password = allLines[index_of_current_line]
            index_of_current_line += 1
            if password == "":
                return False

            email = allLines[index_of_current_line]
            index_of_current_line += 1
            if email == "":
                return False

            name = allLines[index_of_current_line]
            index_of_current_line += 1
            if name == "":
                return False

            emptyLine = allLines[index_of_current_line]
            index_of_current_line+=1
            if emptyLine != "":
                return False
##Lägger till i listan och börjar om
            self.add_user(username,password,email,name)
#om linjerna dne läst stämmer med längden av listan så har allt gått bra
            if index_of_current_line == len(allLines):
                return True

#Sparar ner alla users
    def writeUsersToFile(self):
        allContent = ""

        for user in self.list_of_users:
            allContent+=user.username+"\n"
            allContent+=user.password+"\n"
            allContent+=user.email+"\n"
            allContent+=user.name+"\n"
            allContent+="\n"

        try:
            file = open("users.txt",'w')
            file.write(allContent)
            file.close()
            return True
        except:
            return False
