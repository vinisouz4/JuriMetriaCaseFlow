import asyncio
from src.api.apiDataJud.getAPIDataJud import getDataJud
from src.adapter.dataframe.pandas.index import PandasDataFrame
# # from src.adapter.dataframe.polars.index import PolarsDataFrame
from src.api.escavador.escavador import apiEscavador
from src.use_case.dataCaseFlow.readData import ReadCaseFlowData
from src.use_case.dataEscavador.readDataEscavador import ReadEscavador

escavador = apiEscavador()

case = ReadCaseFlowData(PandasDataFrame())


# getDataJud.saveData(teste)


df = case.getData("Case", "true", True)

teste = escavador.formatListProcess(df)

print(teste[:10])

escavador.saveData(teste[:10])
# atualizacao = getDataJud()
# atualizacao.saveData(df)



print("FIm")