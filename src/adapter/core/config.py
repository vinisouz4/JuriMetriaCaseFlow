from dotenv import load_dotenv
import os 

load_dotenv()


class Settings():
    try:
        API_SUPABASE_URL = os.getenv("API_SUPABASE_URL")
        API_SUPABASE_KEY = os.getenv("API_SUPABASE_KEY")

        API_PUBLI_DATAJUD = os.getenv("API_PUBLI_DATAJUD")
        API_PUBLI_DATAJUD_KEY = os.getenv("API_PUBLI_DATAJUD_KEY")

        PATH_EXCEL_TESTE = os.getenv("PATH_EXCEL_TESTE")

        DATALAKE_URL = os.getenv("DATALAKE_URL")

        ESCAVADOR_KEY = os.getenv("ESCAVADOR_KEY")

        UPDATE_DAY = os.getenv("UPDATE_DAY")
        UPDATE_HOUR = os.getenv("UPDATE_HOUR")

    except Exception as e:
        API_SUPABASE_URL = None
        API_SUPABASE_KEY = None

        API_PUBLI_DATAJUD = None
        API_PUBLI_DATAJUD_KEY = None

        PATH_EXCEL_TESTE = None

        DATALAKE_URL = None

        UPDATE_DAY = None