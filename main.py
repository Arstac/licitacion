from dotenv import load_dotenv


load_dotenv()

from modules import app_normativa



response = app_normativa.invoke({"path_pliego": "Data/pliego.pdf"})

print(response["cumplimiento_normativa"])