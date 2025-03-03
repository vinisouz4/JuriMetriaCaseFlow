import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))



from src.adapter.dataframe.pandas.index import PandasDataFrame
from src.adapter.logging.logging import LoggerHandler
from src.api.escavador.escavador import apiEscavador
from src.use_case.dataCaseFlow.readData import ReadCaseFlowData


logger = LoggerHandler("Atualização Escavador")


logger.INFO("Started Update Escavador")

escavador = apiEscavador()

case = ReadCaseFlowData(PandasDataFrame())

df = case.getData("Case", "true", True)

listProcess = escavador.formatListProcess(df)

escavador.saveData(listProcess[:40])

logger.INFO("Finished Update Escavador")