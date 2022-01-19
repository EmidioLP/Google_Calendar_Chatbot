#Imports
from re import fullmatch
from flask import Flask, render_template, request, jsonify, make_response
from flask_cors import CORS, cross_origin
import pymongo
import json
from saveConversation import Conversations
from pymongo import MongoClient
from CalendarAPI.Calendar import CalendarAPI
from CalendarAPI import Calendar
from flask_ngrok import run_with_ngrok


app = Flask(__name__)  # Inicializando a aplicação Flask com o nome "app"
run_with_ngrok(app)


# Recebendo e enviando respostas para o Dialogflow
@app.route('/webhook', methods=['POST'])
@cross_origin()
def webhook():
    req = request.get_json(silent=True, force=True)
    res = processRequest(req)
    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


# Processando as requests do Dialogflow
def processRequest(req):
    log = Conversations.Log()
    calendar = Calendar.CalendarAPI()
    sessionID = req.get('responseId')
    result = req.get("queryResult")
    intent = result.get("intent").get('displayName')
    query_text = result.get("queryText")
    parameters = result.get("parameters")
    db = configureDataBase()

    if intent == "Calendario":
        date= result.get("parameters").get('date-time')
        data = calendar.MakeCalendarRequest(date)
        if data == True:
            fulfillmentText = "Sim."
            log.saveConversations(sessionID, query_text, fulfillmentText, intent, db)
            return{

                "fulfillmentMessages": [
                    {
                        "text": {
                            "text": [
                                "Sim."
                            ]
                        }
                    }
                ]
            }
                
        elif data == False:
            fulfillmentText = "Não."
            log.saveConversations(sessionID, query_text, fulfillmentText, intent, db)
            return{

                "fulfillmentMessages": [
                    {
                        "text": {
                            "text": [
                                "Não."
                            ]
                        }
                    }
                ]
            }
           
    elif intent == "Default Fallback Intent":
        fulfillmentText = result.get("fulfillmentText")
        log.saveQuestions(sessionID, query_text, db)
      
    else:
        fulfillmentText = result.get("fulfillmentText")
        log.saveConversations(sessionID, query_text, fulfillmentText, intent, db)

#Conectando ao banco de dados
def configureDataBase():
    client = MongoClient("mongodb+srv://Seu Cliente")
    return client.get_database('Nome do seu cliente')




if __name__ == '__main__':
    app.run()
