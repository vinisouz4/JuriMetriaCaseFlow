import streamlit as st
import sys
import os
import plotly.express as px

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from src.adapter.dataframe.pandas.index import PandasDataFrame
from src.use_case.insights.insights import Insights
from src.use_case.dataCaseFlow.readData import ReadCaseFlowData



insights = Insights(PandasDataFrame())
dataCaseFlow = ReadCaseFlowData(PandasDataFrame())

dataCase = dataCaseFlow.getData("Case", "true")
ufDf = insights.totalUf(dataCase)

@st.cache_data
def get_data():
    return dataCaseFlow.getData("Case", "true")

data = insights.totalUf(get_data())

st.title("Indicadores")


st.subheader("Mapa de calor")

fig = px.scatter_map(
    data, 
    lat="latitude", 
    lon="longitude", 
    hover_data={"uf": True, "value_cause": False},
    color="value_cause", 
    size="value_cause", 
    color_continuous_scale=px.colors.sequential.Viridis, 
    size_max=15, 
    zoom=2
)

fig.update_traces(
    hovertemplate="<br>".join(
        [
            "UF: %{customdata[0]}",
            "Valor da causa: R$ %{customdata[1]:,.2f}",
        ]
    )
)


st.plotly_chart(fig)


st.subheader("Total de processos por UF")
# Gráfico de barras

figBar = px.bar(
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

figBar.update_traces(textposition='outside')

st.plotly_chart(figBar)
