from dotenv import load_dotenv

load_dotenv()

from modules import app, app_mats, app_price


doc = "lic_2"

# #Prueba de funcionamiento de PDF a información
# response_data = app.invoke({"messages": "Extrae la info, porfavor", "doc": doc})

# print(response_data["DataInfo"])


# #Prueba de funcionamiento de PDF a información
# response_mats = app_mats.invoke({"messages": "Extrae la info, porfavor", "doc": doc})

# print(response_mats["materiales"])

response_price = app_price.invoke({"messages": "Extrae la info, porfavor", "doc": doc})

print(response_price["mat_prices"])