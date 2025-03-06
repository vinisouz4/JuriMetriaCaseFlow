import datetime
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))


from src.adapter.dataframe.pandas.index import PandasDataFrame
from src.adapter.logging.logging import LoggerHandler
from src.api.apiDataJud.getAPIDataJud import getDataJud
from src.use_case.dataEscavador.readDataEscavador import ReadEscavador
from src.utils.utils import Utils


logger = LoggerHandler("Atualização DataJud")

utils = Utils()


while True:
    today = utils.getToday()

    if today.day == 1:
        logger.INFO("Started Update DataJud")

        nextMonth = today.month + 1 if today.month < 12 else 1

        nextYear = today.year + 1 if today.month < 12 else today.year + 1

        nextExecute = datetime.datetime(nextYear, nextMonth, 1, 0, 0, 0)

        logger.INFO(f"Next execute: {nextExecute}")

    
    datetime.time.sleep(3600)



logger.INFO("Started Update DataJud")

datajud = getDataJud()

escavador = ReadEscavador(PandasDataFrame())

df = escavador.getData()

datajud.saveData(df)

logger.INFO("Finished Update DataJud")