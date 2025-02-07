from src.adapter.dataframe.pandas.index import PandasDataFrame
# from src.adapter.dataframe.polars.index import PolarsDataFrame
from src.use_case.dataCaseFlow.readData import ReadCaseFlowData
from src.use_case.dataDataJud.readDataJud import ReadDataJud
from src.adapter.core.config import Settings
import asyncio

from src.use_case.insights.insights import Insights

teste = ReadDataJud()

settings = Settings()

insights = Insights(PandasDataFrame())

testeSupa = ReadCaseFlowData(PandasDataFrame())

df = testeSupa.getData("Case", "true")

print(insights.totalUf(df))




# asyncio.run(teste.getData(
#     url = settings.API_PUBLI_DATAJUD, 
#     processNumber=["10013836720245020262"], 
#     headers={
#         "Authorization": settings.API_PUBLI_DATAJUD_KEY,
#         "Content-Type": "application/json"
#     },
#     numberEndPoint=2
# ))