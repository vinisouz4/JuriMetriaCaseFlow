import datetime
import sys
import os
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))


from src.adapter.core.config import Settings
from src.adapter.dataframe.pandas.index import PandasDataFrame
from src.adapter.logging.logging import LoggerHandler
from src.api.apiDataJud.getAPIDataJud import getDataJud
from src.use_case.dataEscavador.readDataEscavador import ReadEscavador
from src.utils.utils import Utils


logger = LoggerHandler("Atualização DataJud")

utils = Utils()

settings = Settings()

def run_monthly_update():
    today = utils.getToday()

    startDay = int(settings.UPDATE_DAY)

    if today.day == startDay:
        logger.INFO(f"Started Update DataJud - {today}")

        datajud = getDataJud()
        escavador = ReadEscavador(dataframe=PandasDataFrame())

        df = escavador.getData()
        
        datajud.saveData(df)

        logger.INFO("Finished Update DataJud")

    # Calcula o próximo primeiro dia do mês
    next_month = today.month + 1 if today.month < 12 else 1
    next_year = today.year + 1 if today.month == 12 else today.year
    next_execute = datetime.datetime(next_year, next_month, startDay, 0, 0, 0)

    # Tempo até o próximo primeiro dia do mês
    sleep_time = (next_execute - datetime.datetime.now()).total_seconds()
    logger.INFO(f"Next execute at: {next_execute}, sleeping for {sleep_time} seconds")

    return sleep_time

if __name__ == "__main__":
    while True:
        sleep_time = run_monthly_update()
        time.sleep(sleep_time)
