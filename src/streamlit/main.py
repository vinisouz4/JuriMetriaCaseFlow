import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))


import streamlit as st
import plotly.express as px

from src.adapter.dataframe.pandas.index import PandasDataFrame
from src.use_case.insights.insights import Insights
from src.use_case.dataCaseFlow.readData import ReadCaseFlowData
from src.use_case.dataDataJud.readDataJud import ReadDataJud
from src.utils.utils import Utils

insights = Insights(PandasDataFrame())
dataCaseFlow = ReadCaseFlowData(PandasDataFrame())
dataJud = ReadDataJud(PandasDataFrame())
util = Utils()


# Variaveis com os dataframes

dfCaseFlow = dataCaseFlow.getData(
    table="Case", 
    activedFilter="True", 
    removeSpecialCharacters=True
)

dfDataJud = dataJud.readDataJud()

st.title("Jurimetria")

st.dataframe(dfCaseFlow)