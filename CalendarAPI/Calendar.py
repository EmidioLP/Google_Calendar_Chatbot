from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import pickle

class CalendarAPI:
  def __init__(self):
        pass

  def MakeCalendarRequest(self, data_atual):
    #scopes = ['https://www.googleapis.com/auth/calendar.readonly']
    #flow = InstalledAppFlow.from_client_secrets_file("client_secret_calendar.json", scopes=scopes)
    credentials = pickle.load(open("token.pkl", "rb")) #Retirei o arquivo "Token.pkl" por razões óbvias, mas ele seria as credenciais de acesso a api do calendário criptografadas.
    service = build("calendar", "v3", credentials=credentials)

    events_result = service.events().list(calendarId='primary', singleEvents=True, orderBy='startTime', timeMin = data_atual).execute()
    events = events_result.get('items', [])

    for event in events:
      dataEvent = event['start'].get('dateTime')
      dataCalendarioTratada = ''
      dataTratada = ''
      for i in list(dataEvent):
        dataCalendarioTratada += i
        if i == 'T':
          break
      for f in list(data_atual):
        dataTratada += f
        if f == 'T':
          break
    if dataCalendarioTratada == dataTratada:
      return True
    else:
      return False
    
    
    










