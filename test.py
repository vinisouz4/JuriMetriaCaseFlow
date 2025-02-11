from src.api.apiDataJud.getAPIDataJud import getDataJud
from src.adapter.dataframe.pandas.index import PandasDataFrame
# # from src.adapter.dataframe.polars.index import PolarsDataFrame
from src.use_case.dataCaseFlow.readData import ReadCaseFlowData
from src.use_case.dataDataJud.readDataJud import ReadDataJud
# from src.api.apiDataJud.getAPIDataJud import ReadDataJud
# from src.adapter.core.config import Settings

# import json
# import asyncio

# from src.use_case.insights.insights import Insights
# from src.use_case.tribunais.tribunais import getTribunalNumber
# from src.utils.utils import Utils

# teste = ReadDataJud()

# settings = Settings()

# insights = Insights(PandasDataFrame())

# datajud = ReadDataJud()

# dataJud = getDataJud()

# testeSupa = ReadCaseFlowData(PandasDataFrame())

# util = Utils()

# df = testeSupa.getData("Case", "true", True)

# dataJud.saveData(df)

# # Retirar isso depois da aprovacao do projeto
# df = df[df["client_id"].isin([13, 30, 1248]) & df["uf"].isin(["SP"])]

# df["endpoint_tribunal"] = df["tribunal_justica"].apply(getTribunalNumber)

# with open(f"./src/data/lake/data_{util.getToday()}.json", "w") as f:
#     for i in df["endpoint_tribunal"].unique():
#         print(i)
#         listNumbers = df[df["endpoint_tribunal"] == i]["external_number"].tolist()
#         request = asyncio.run(datajud.getData(
#             url = settings.API_PUBLI_DATAJUD, 
#             processNumber=listNumbers, 
#             headers={
#                 "Authorization": settings.API_PUBLI_DATAJUD_KEY,
#                 "Content-Type": "application/json"
#             },
#             numberEndPoint=i
#         ))
        
#         json.dump(request, f, indent=4, ensure_ascii=False)


# from src.use_case.dataDataJud.readDataJud import ReadDataJud


teste = ReadDataJud(PandasDataFrame())

teste.readDataJud()

    