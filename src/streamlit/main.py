import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))


import streamlit as st
import plotly.express as px

from src.adapter.dataframe.pandas.index import PandasDataFrame
from src.use_case.insights.insights import Insights
from src.use_case.dataCaseFlow.readData import ReadCaseFlowData
from src.use_case.dataDataJud.readDataJud import ReadDataJud


insights = Insights(PandasDataFrame())
dataCaseFlow = ReadCaseFlowData(PandasDataFrame())
dataJud = ReadDataJud(PandasDataFrame())

# =============================================================================

dataCase = dataCaseFlow.getData("Case", "true")

df = dataJud.readDataJud()

groupedJud = dataJud.statusGrouped(df)

# =============================================================================

# =============================================================================
"""
Chamda dos métodos para plotar o grafico de barras do plotly
"""

ufDf = insights.totalUf(dataCase)

fig = px.bar(
    ufDf,
    x="uf",
    y="uf_count",
    title="Total de processos por UF",
    labels={"uf_count": "Total de processos", "uf": "UF"},
    color="uf",
    orientation="v",
    text="uf_count",
    category_orders={"uf_count": ufDf["uf_count"].tolist()}
)

fig.update_traces(textposition='outside')


thirtyDaysProcess, sevenDaysProcess = insights.distributionData(dataCase, "distribution_date")

st.title("Jurismetria")

totaProcesso, processoPeriodos = st.columns(2)

totaProcesso.metric("Total de processos", insights.totalProcess(dataCase))
processoPeriodos.metric("Distribuídos Últimos 30 dias", thirtyDaysProcess)


st.metric("Valor total das causas", f"R$ {insights.totalValueCause(dataCase):.2f}")

st.plotly_chart(fig)




st.dataframe(groupedJud)
