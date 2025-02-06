from dotenv import load_dotenv

load_dotenv()

from modules import app, app_mats


#Prueba de funcionamiento de PDF a información
response = app_mats.invoke({"messages": "Extrae la info, porfavor"})

print(response["materiales"])


#
