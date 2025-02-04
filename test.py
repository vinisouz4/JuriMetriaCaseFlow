from src.adapter.dataframe.pandas.index import PandasDataFrame
# from src.adapter.dataframe.polars.index import PolarsDataFrame
from src.use_case.dataCaseFlow.readData import ReadCaseFlowData
from src.use_case.dataDataJud.readDataJud import ReadDataJud
from src.adapter.core.config import Settings()

teste = ReadDataJud()

settings = Settings()









teste.getData(
    url = settings.API_PUBLI_DATAJUD, 
    processNumber=["10000012520255020029", "10000012520255020028", "10000012520255020027"], 
    headers={
        "Authorization": settings.API_PUBLI_DATAJUD_KEY,
        "Content-Type": "application/json"
        }, 
    payload={"data": "data"})