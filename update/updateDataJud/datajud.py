import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))


from src.adapter.dataframe.pandas.index import PandasDataFrame
from src.adapter.logging.logging import LoggerHandler
from src.api.apiDataJud.getAPIDataJud import getDataJud
from src.use_case.dataEscavador.readDataEscavador import ReadEscavador


logger = LoggerHandler("Atualização DataJud")


logger.INFO("Started Update DataJud")

datajud = getDataJud()

escavador = ReadEscavador(PandasDataFrame())

df = escavador.getData()

datajud.saveData(df)

logger.INFO("Finished Update DataJud")