#Imports
from datetime import datetime 

class Log:
    def __init__(self):
        pass
    #Essa função é responsável por salvar todas as interações de uma conversa com o bot no banco de dados.
    def saveConversations(self, sessionID, usermessage,botmessage,intent,dbConn):

        self.now = datetime.now()
        self.date = self.now.date()
        self.current_time = self.now.strftime("%H:%M:%S")

        
        mydict = {"sessionID":sessionID,"User Intent" : intent ,"User": usermessage, "Bot": botmessage, "Date": str(self.date) + "/" + str(self.current_time)}

        
        records = dbConn.chat_records
        records.insert_one(mydict)

       
    #Essa função é responsável por salvar as perguntas que não foram respondidas pelo bot.
    def saveQuestions(self, sessionID, usermessage, dbConn):
        self.now = datetime.now()
        self.date = self.now.date()
        self.current_time = self.now.strftime("%H:%M:%S")

        dicionario = {"sessionID":sessionID,  "User": usermessage, "Date": str(self.date) + "/" + str(self.current_time)}

        records = dbConn.question_records
        records.insert_one(dicionario)

