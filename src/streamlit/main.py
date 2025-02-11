import streamlit as st
import sys
import os
import pydeck as pdk

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from src.adapter.dataframe.pandas.index import PandasDataFrame
from src.use_case.insights.insights import Insights
from src.use_case.dataCaseFlow.readData import ReadCaseFlowData
from src.api.apiDataJud.getAPIDataJud import ReadDataJud


insights = Insights(PandasDataFrame())
dataCaseFlow = ReadCaseFlowData(PandasDataFrame())
dataJud = ReadDataJud(PandasDataFrame())

dataCase = dataCaseFlow.getData("Case", "true")
