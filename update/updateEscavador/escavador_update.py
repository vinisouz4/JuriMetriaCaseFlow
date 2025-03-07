import datetime
import sys
import os
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))


from src.adapter.core.config import Settings
from src.utils.utils import Utils
from src.adapter.dataframe.pandas.index import PandasDataFrame
from src.adapter.logging.logging import LoggerHandler
from src.api.escavador.escavador import apiEscavador
from src.use_case.dataCaseFlow.readData import ReadCaseFlowData


logger = LoggerHandler("Atualização Escavador")




utils = Utils()

settings = Settings()

def run_monthly_update():
    today = utils.getToday()

    startDay = int(settings.UPDATE_DAY)
    startHour = int(settings.UPDATE_HOUR)

    if today.day == startDay and today.hour == startHour:
        
        logger.INFO("Started Update Escavador")

        escavador = apiEscavador()

        case = ReadCaseFlowData(PandasDataFrame())

        df = case.getData("Case", "true", True)

        listProcess = escavador.formatListProcess(df)

        logger.INFO(f"Quantidade de Numero de Processos Validados e Corretos {len(listProcess)}")

        escavador.saveData(listProcess)

        logger.INFO("Finished Update Escavador")


    # Calcula o próximo primeiro dia do mês
    next_month = today.month + 1 if today.month < 12 else 1
    next_year = today.year + 1 if today.month == 12 else today.year
    next_execute = datetime.datetime(next_year, next_month, startDay, startHour, 0, 0)

    # Tempo até o próximo primeiro dia do mês
    sleep_time = (next_execute - datetime.datetime.now()).total_seconds()
    logger.INFO(f"Next execute at: {next_execute}, sleeping for {sleep_time} seconds")

    return sleep_time

if __name__ == "__main__":
    while True:
        sleep_time = run_monthly_update()
        time.sleep(sleep_time)
        