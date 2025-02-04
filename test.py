from src.adapter.dataframe.pandas.index import PandasDataFrame
# from src.adapter.dataframe.polars.index import PolarsDataFrame
from src.use_case.dataCaseFlow.readData import ReadCaseFlowData
from src.use_case.dataDataJud.readDataJud import ReadDataJud
from src.adapter.core.config import Settings
import asyncio

teste = ReadDataJud()

settings = Settings()






asyncio.run(teste.getData(
    url = settings.API_PUBLI_DATAJUD, 
    processNumber=["10013836720245020262"], 
    headers={
        "Authorization": settings.API_PUBLI_DATAJUD_KEY,
        "Content-Type": "application/json"
    },
    numberEndPoint=2
))